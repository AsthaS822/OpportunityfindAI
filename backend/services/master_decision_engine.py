"""
MASTER DECISION ENGINE — backend brain orchestrating the full pipeline.
"""

from dataclasses import asdict
from typing import Dict, List, Any
from datetime import datetime
from ..models.opportunity import InternalOpportunity
from ..config import MAX_VERIFY
from .query_parser import query_parser
from .query_sanity import is_nonsense_query, requires_high_confidence_match
from .multi_search import multi_search
from .deduplicator import deduplicator
from .eligibility_checker import eligibility_checker
from .decision_engine import decision_engine
from .chance_estimator import alternative_suggester
from .verifier import verifier
from .dataset_loader import dataset_loader
from ..cache.memory import session_history
from ..utils.logger import get_logger

logger = get_logger(__name__)

THINKING_STEPS = [
    "Searching datasets...",
    "Ranking opportunities...",
    "Verifying official sources...",
    "Analyzing eligibility...",
    "Generating explanation...",
]


class MasterDecisionEngine:
    async def discover(
        self,
        query: str,
        language: str = "en",
        session_id: str = "default",
    ) -> Dict[str, Any]:
        start_time = datetime.now()
        thinking_steps: List[str] = []

        try:
            # Sanity check — block hallucination bait
            is_nonsense, nonsense_msg = is_nonsense_query(query)
            if is_nonsense:
                return self._empty_response(query, language, nonsense_msg, thinking_steps)

            # STEP 1: Intent detection + entity extraction (with session memory)
            thinking_steps.append(THINKING_STEPS[0])
            session_profile = session_history.get_profile(session_id)
            intent = query_parser.parse(query, session_profile)
            session_history.update_profile(session_id, intent)
            user_profile = session_history.intent_to_profile(intent)

            # Follow-up gating
            if intent.get("follow_up_required"):
                return {
                    "status": "follow_up",
                    "query": query,
                    "language": language,
                    "thinking_steps": ["Understanding your requirements..."],
                    "follow_up_required": True,
                    "follow_up_questions": intent.get("follow_up_questions", []),
                    "missing_information": intent.get("missing_information", []),
                    "user_intent": intent.get("intent"),
                    "opportunities": [],
                    "alternatives": [],
                    "summary": "Please provide a few more details so I can find the best verified opportunities for you.",
                }

            # STEP 2: Multi-step dataset search
            thinking_steps.append("Ranking opportunities...")
            dataset_candidates = multi_search.search(intent, top_k=25)

            if requires_high_confidence_match(query):
                dataset_candidates = [o for o in dataset_candidates if o.match_score >= 55]

            if not dataset_candidates:
                return self._empty_response(
                    query, language,
                    "No verified opportunities found matching your criteria.",
                    thinking_steps,
                    intent,
                )

            # STEP 3: Deduplicate
            dataset_candidates = deduplicator.deduplicate(dataset_candidates)

            # STEP 4: Jina verify top N (concurrent)
            thinking_steps.append(THINKING_STEPS[2])
            to_verify = dataset_candidates[:MAX_VERIFY]
            verified_opportunities = await verifier.verify_opportunities(to_verify)

            # STEP 5: Validate + merge
            valid_verified = self._validate_opportunities(verified_opportunities)
            remaining = [o for o in dataset_candidates[MAX_VERIFY:] if o.id not in {v.id for v in valid_verified}]
            combined = deduplicator.deduplicate(valid_verified + remaining)

            # STEP 6: Score + filter
            thinking_steps.append(THINKING_STEPS[3])
            scored = self._score_opportunities(combined, user_profile)
            filtered = self._filter_invalid(scored)

            if not filtered:
                return self._empty_response(
                    query, language,
                    "No verified opportunities found matching your criteria.",
                    thinking_steps,
                    intent,
                )

            # STEP 7: Eligibility + decision analysis
            explained: List[InternalOpportunity] = []
            for opp in filtered[:10]:
                elig = eligibility_checker.check_eligibility(user_profile, opp)
                opp.eligibility_analysis = elig
                opp.decision_analysis = decision_engine.analyze(user_profile, opp, elig)
                explained.append(opp)

            # STEP 8: Rank
            ranked = sorted(explained, key=lambda x: x.match_score, reverse=True)[:15]

            # STEP 9: Alternatives
            alternatives_raw = alternative_suggester.suggest_alternatives(
                user_profile, dataset_loader.opportunities, ranked[0] if ranked else None
            )
            alternatives = [
                {
                    "type": a["type"],
                    "title": a["opportunity"].title,
                    "provider": a["opportunity"].provider,
                    "country": a["opportunity"].country,
                    "reason": a["reason"],
                    "advantage": a["advantage"],
                    "official_url": a["opportunity"].official_url,
                }
                for a in alternatives_raw
            ]

            thinking_steps.append(THINKING_STEPS[4])

            return {
                "status": "success",
                "query": query,
                "language": language,
                "thinking_steps": thinking_steps,
                "user_intent": intent.get("intent"),
                "missing_information": intent.get("missing_information", []),
                "follow_up_required": False,
                "follow_up_questions": [],
                "opportunities": [self._format_opportunity(o) for o in ranked],
                "alternatives": alternatives,
                "total_found": len(ranked),
                "verified_count": sum(1 for o in ranked if "Live Verified" in (o.verification or {}).get("status", "")),
                "validation_time": str(datetime.now() - start_time),
                "summary": self._generate_summary(ranked, user_profile),
            }

        except Exception as e:
            logger.error(f"Discovery error: {e}", exc_info=True)
            return {"status": "error", "message": str(e), "thinking_steps": thinking_steps}

    def _empty_response(self, query, language, msg, steps, intent=None):
        return {
            "status": "success",
            "query": query,
            "language": language,
            "thinking_steps": steps or ["Searching datasets..."],
            "opportunities": [],
            "alternatives": [],
            "total_found": 0,
            "verified_count": 0,
            "summary": msg,
            "user_intent": intent.get("intent") if intent else None,
            "missing_information": intent.get("missing_information", []) if intent else [],
            "follow_up_required": False,
        }

    def _validate_opportunities(self, opportunities: List[InternalOpportunity]) -> List[InternalOpportunity]:
        valid = []
        for opp in opportunities:
            if not opp.title or len(opp.title.strip()) < 3:
                continue
            if opp.provider and "unknown" in opp.provider.lower() and not opp.description:
                continue
            if opp.live_deadline and opp.live_deadline != "Unknown":
                opp.deadline = opp.live_deadline
            valid.append(opp)
        return valid

    def _parse_deadline(self, deadline_str: str):
        if not deadline_str or deadline_str == "Unknown":
            return None
        formats = ["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%B %d, %Y", "%b %d, %Y", "%d %B %Y"]
        for fmt in formats:
            try:
                return datetime.strptime(deadline_str.strip(), fmt)
            except ValueError:
                pass
        return None

    def _score_opportunities(self, opportunities, user_profile):
        for opp in opportunities:
            base = opp.match_score or 0
            if user_profile.get("target_country") and opp.country:
                if user_profile["target_country"].lower() in opp.country.lower():
                    base += 15
            if user_profile.get("target_degree") and opp.degree:
                if user_profile["target_degree"].lower() in opp.degree.lower():
                    base += 15
            if user_profile.get("funding_requirement") and opp.funding_type:
                if user_profile["funding_requirement"].lower() in opp.funding_type.lower():
                    base += 10
            field = user_profile.get("stream") or user_profile.get("field")
            if field and (field.lower() in (opp.title or "").lower() or field.lower() in (opp.description or "").lower()):
                base += 10
            if "Live Verified" in (opp.verification or {}).get("status", ""):
                base += 10
            opp.match_score = base
        return opportunities

    def _filter_invalid(self, opportunities):
        valid = []
        for opp in opportunities:
            if opp.deadline and opp.deadline != "Unknown":
                dl = self._parse_deadline(opp.deadline)
                if dl and dl < datetime.now():
                    continue
            if (opp.match_score or 0) < 15:
                continue
            valid.append(opp)
        return valid

    def _format_opportunity(self, opp: InternalOpportunity) -> Dict[str, Any]:
        da = opp.decision_analysis or {}
        elig = opp.eligibility_analysis or {}
        return {
            "id": opp.id,
            "title": opp.title,
            "provider": opp.provider,
            "country": opp.country,
            "category": opp.category,
            "degree": opp.degree,
            "funding": opp.funding_type,
            "funding_type": opp.funding_type,
            "deadline": opp.deadline or opp.live_deadline,
            "eligibility": opp.eligibility,
            "description": opp.description,
            "official_url": opp.verified_url or opp.official_url,
            "match_score": round(opp.match_score or 0, 1),
            "verification": opp.verification,
            "source": opp.source_type,
            "source_type": opp.source_type,
            "dataset_deadline": opp.dataset_deadline,
            "live_deadline": opp.live_deadline,
            "dataset_ranking": opp.dataset_ranking,
            "live_ranking": opp.live_ranking,
            "decision_analysis": da,
            "eligibility_checks": elig,
            "next_steps": elig.get("next_steps", []),
        }

    def _generate_summary(self, opportunities, user_profile):
        if not opportunities:
            return "No verified opportunities found."
        top = opportunities[0]
        rec = (top.decision_analysis or {}).get("overall_recommendation", "Review Carefully")
        return f"Found {len(opportunities)} verified opportunities. Top recommendation: {top.title} — {rec}."


master_decision_engine = MasterDecisionEngine()
