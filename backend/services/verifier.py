import asyncio
from typing import List, Optional, Dict
from datetime import datetime, timezone
from ..models.opportunity import InternalOpportunity
from .jina_search import jina_search
from .jina_reader import jina_reader
from .official_source_selector import official_source_selector
from .groq_service import groq_service
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

        # Step 1: Search for the opportunity
        search_query = f"{opp.title} {opp.provider} official site eligibility deadline application"
        jina_results = await jina_search.search(search_query)

        if not jina_results:
            opp.verification = {
                "status": "Could Not Verify", "confidence": "Low",
                "source": opp.official_url or "None", "last_checked": now_str,
            }
            opp.source_type = "Dataset Only"
            return opp

        # Step 2: Select best official URL (whitelist-aware)
        official_url, confidence = official_source_selector.select_best_url(jina_results)
        if not official_url:
            opp.verification = {
                "status": "Could Not Verify", "confidence": "Low",
                "source": "None", "last_checked": now_str,
            }
            opp.source_type = "Dataset Only"
            return opp

        opp.verified_url = official_url

        # Step 3: Read the page content
        page_content = await jina_reader.read(official_url)

        if not page_content:
            opp.verification = {
                "status": "Could Not Verify", "confidence": confidence,
                "source": official_url, "last_checked": now_str,
            }
            opp.source_type = "Dataset Only"
            return opp

        # Step 4: Extract structured data via Groq
        extracted = await groq_service.extract_details(page_content, opp.title)

        if extracted:
            opp.live_deadline = extracted.get("deadline") if extracted.get("deadline") != "Unknown" else None
            opp.live_ranking = extracted.get("ranking") if extracted.get("ranking") != "Unknown" else None
            opp.verified_details = extracted
            if extracted.get("eligibility") and extracted["eligibility"] != "Unknown":
                opp.eligibility = extracted["eligibility"]

            # Step 5: Conflict detection — compare extracted data with dataset
            conflicts = self._detect_conflicts(opp, extracted)
            if conflicts:
                logger.warning(f"Conflicts detected for {opp.title}: {conflicts}")
                # Mark as Dataset + Live Verification but note conflicts
                opp.verification = {
                    "status": "Live Verified (with conflicts)",
                    "confidence": confidence,
                    "source": official_url,
                    "last_checked": now_str,
                    "conflicts": conflicts,
                }
                opp.source_type = "Dataset + Live Verification"
            else:
                opp.verification = {
                    "status": "Live Verified",
                    "confidence": confidence,
                    "source": official_url,
                    "last_checked": now_str,
                }
                opp.source_type = "Dataset + Live Verification"
        else:
            opp.verification = {
                "status": "Dataset Only", "confidence": "Medium",
                "source": official_url, "last_checked": now_str,
            }
            opp.source_type = "Dataset Only"

        return opp

    def _detect_conflicts(self, opp: InternalOpportunity, extracted: Dict) -> List[str]:
        """Detect conflicts between dataset and live-extracted data. Never blindly overwrite."""
        conflicts = []

        # Check deadline conflict
        if opp.deadline and extracted.get("deadline") and extracted["deadline"] != "Unknown":
            if opp.deadline.lower() != extracted["deadline"].lower():
                conflicts.append(f"Deadline differs: dataset says '{opp.deadline}', live source says '{extracted['deadline']}'")

        # Check eligibility conflict
        if opp.eligibility and extracted.get("eligibility") and extracted["eligibility"] != "Unknown":
            if len(opp.eligibility) > 20 and len(extracted["eligibility"]) > 20:
                if opp.eligibility.lower()[:50] != extracted["eligibility"].lower()[:50]:
                    conflicts.append("Eligibility criteria differ between dataset and live source")

        return conflicts


verifier = Verifier()
