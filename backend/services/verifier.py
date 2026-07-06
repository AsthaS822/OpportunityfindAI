import asyncio
from typing import List
from datetime import datetime, timezone
from ..models.opportunity import InternalOpportunity
from .jina_search import jina_search
from .jina_reader import jina_reader
from .official_source_selector import official_source_selector
from .gemini_service import gemini_service
from ..utils.logger import get_logger

logger = get_logger(__name__)


class Verifier:
    async def verify_opportunities(self, opportunities: List[InternalOpportunity]) -> List[InternalOpportunity]:
        if not opportunities:
            return []

        tasks = [self._verify_single(opp) for opp in opportunities]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        verified_opps = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error verifying {opportunities[i].title}: {result}")
                opportunities[i].verification["status"] = "Could Not Verify"
                opportunities[i].source_type = "Dataset Only"
                verified_opps.append(opportunities[i])
            else:
                verified_opps.append(result)
        return verified_opps

    async def _verify_single(self, opp: InternalOpportunity) -> InternalOpportunity:
        logger.info(f"Verifying: {opp.title} from {opp.provider}")
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        search_query = f"{opp.title} {opp.provider} official site eligibility deadline application"
        jina_results = await jina_search.search(search_query)

        if not jina_results:
            opp.verification = {
                "status": "Could Not Verify",
                "confidence": "Low",
                "source": opp.official_url or "None",
                "last_checked": now_str,
            }
            opp.source_type = "Dataset Only"
            return opp

        official_url, confidence = official_source_selector.select_best_url(jina_results)
        if not official_url:
            opp.verification = {
                "status": "Could Not Verify",
                "confidence": "Low",
                "source": "None",
                "last_checked": now_str,
            }
            opp.source_type = "Dataset Only"
            return opp

        opp.verified_url = official_url
        page_content = await jina_reader.read(official_url)

        if not page_content:
            opp.verification = {
                "status": "Could Not Verify",
                "confidence": confidence,
                "source": official_url,
                "last_checked": now_str,
            }
            opp.source_type = "Dataset Only"
            return opp

        extracted = await gemini_service.extract_details(page_content, opp.title)

        if extracted:
            opp.live_deadline = extracted.get("deadline") if extracted.get("deadline") != "Unknown" else None
            opp.live_ranking = extracted.get("ranking") if extracted.get("ranking") != "Unknown" else None
            opp.verified_details = extracted
            if extracted.get("eligibility") and extracted["eligibility"] != "Unknown":
                opp.eligibility = extracted["eligibility"]
            opp.verification = {
                "status": "Live Verified",
                "confidence": confidence,
                "source": official_url,
                "last_checked": now_str,
            }
            opp.source_type = "Dataset + Live Verification"
        else:
            opp.verification = {
                "status": "Dataset Only",
                "confidence": "Medium",
                "source": official_url,
                "last_checked": now_str,
            }
            opp.source_type = "Dataset Only"

        return opp


verifier = Verifier()
