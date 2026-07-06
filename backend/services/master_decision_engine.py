"""
Master Decision Engine: Orchestrates the complete pipeline from user query to personalized recommendations.
Flow: Intent Detection → Dataset Search → Web Verification → Ranking → Explanation
"""

from dataclasses import asdict
from typing import Dict, List, Any
from datetime import datetime
from ..models.opportunity import InternalOpportunity
from ..config import MAX_VERIFY
from .query_parser import query_parser
from .query_sanity import is_nonsense_query, requires_high_confidence_match
from .multi_search import multi_search
from .planner import planner
from .reasoning_engine import reasoning_engine
from .deduplicator import deduplicator
from .eligibility_checker import eligibility_checker
from .decision_engine import decision_engine
from .chance_estimator import alternative_suggester
from .verifier import verifier
from .dataset_loader import dataset_loader
from .groq_intent_extractor import groq_intent_extractor
from .groq_reasoning_engine import groq_reasoning_engine
from .intent_router import intent_router
from ..cache.memory import session_history
from ..utils.logger import get_logger

logger = get_logger(__name__)

THINKING_STEPS = [
    "Understanding your request",
    "Searching dataset and live sources",
    "Verifying official information",
    "Ranking opportunities by relevance",
    "Explaining why they match you",
    "Preparing your results",
]


class MasterDecisionEngine:
    async def discover(
        self,
        query: str,
        session_id: str = "default",
    ) -> Dict[str, Any]:
        start_time = datetime.now()
        thinking_steps: List[str] = []

        try:
            is_nonsense, nonsense_msg = is_nonsense_query(query)
            if is_nonsense:
                summary = nonsense_msg if "I couldn't" in nonsense_msg else "I'm here to help you find educational opportunities. Could you rephrase your question?"
                return self._empty_response(query, summary, thinking_steps)

            thinking_steps.append(THINKING_STEPS[0])
            session_profile = session_history.get_profile(session_id)

            groq_intent = await groq_intent_extractor.extract(query)
            primary_intent = groq_intent.get("primary_intent", "Opportunity Search")
            search_targets = groq_intent.get("search_targets", [])
            query_type = groq_intent.get("query_type", "exploratory")
            needs_personalization = groq_intent.get("needs_personalization", False)
            missing_fields = groq_intent.get("missing_fields", [])
            suggested_follow_up = groq_intent.get("suggested_follow_up", [])
            entities = groq_intent.get("entities", {})

            intent = query_parser.parse(query, session_profile)
            intent["primary_intent"] = primary_intent
            intent["search_targets"] = search_targets
            intent["query_type"] = query_type
            intent["entities"] = entities
            intent["is_exploratory"] = query_type == "exploratory"

            if entities.get("country") and not intent.get("country"):
                intent["country"] = entities["country"]
            if entities.get("degree") and not intent.get("degree"):
                intent["degree"] = entities["degree"]
            if entities.get("field") and not intent.get("field"):
                intent["field"] = entities["field"]

            session_history.update_profile(session_id, intent)
            user_profile = session_history.intent_to_profile(intent)

            route_plan = intent_router.route(groq_intent)
            intent["_route"] = route_plan

            if needs_personalization and missing_fields and suggested_follow_up:
                thinking_steps.append("Collecting your profile information")
                return {
                    "status": "follow_up",
                    "query": query,
                    "thinking_steps": thinking_steps,
                    "follow_up_required": True,
                    "follow_up_questions": suggested_follow_up,
                    "missing_information": missing_fields,
                    "user_intent": primary_intent,
                    "opportunities": [],
                    "alternatives": [],
                    "career_paths": [],
                    "summary": "To find the best opportunities for you, I need a bit more information.",
                }

            # STEP 2: Multi-source search — search only intent-relevant categories + live web
            thinking_steps.append(THINKING_STEPS[1])
            restricted_categories = route_plan.get("categories", [])
            if restricted_categories:
                intent["search_categories"] = restricted_categories
                logger.info(f"Restricted search to categories: {restricted_categories} for intent: {primary_intent}")
            dataset_candidates = await multi_search.search(intent, top_k=route_plan.get("top_k", 25))

            if requires_high_confidence_match(query):
                dataset_candidates = [o for o in dataset_candidates if o.match_score >= 55]

            # Apply per-intent threshold from planner (fallback)
            threshold = planner.get_threshold(primary_intent)
            dataset_candidates = [o for o in dataset_candidates if (o.match_score or 0) >= threshold]

            if not dataset_candidates:
                return self._empty_response(
                    query, self._no_results_message(primary_intent),
                    thinking_steps,
                    intent,
                )

            # STEP 3: Deduplicate
            thinking_steps.append("Deduplicating results")
            dataset_candidates = deduplicator.deduplicate(dataset_candidates)

            # STEP 4: Verify top candidates — only top 8 (cost-effective)
            thinking_steps.append(THINKING_STEPS[2])
            verify_count = min(MAX_VERIFY, 8)
            to_verify = dataset_candidates[:verify_count]
            verified_opportunities = await verifier.verify_opportunities(to_verify)

            # Validate verified
            valid_verified = self._validate_opportunities(verified_opportunities)
            remaining = [o for o in dataset_candidates[MAX_VERIFY:] if o.id not in {v.id for v in valid_verified}]
            combined = deduplicator.deduplicate(valid_verified + remaining)

            # Build verified data map for Groq reasoning
            verified_map = {}
            for opp in valid_verified:
                if opp.verification:
                    verified_map[opp.id] = {
                        "status": opp.verification.get("status", ""),
                        "source": opp.verified_url or opp.official_url or "",
                        "deadline": opp.live_deadline or opp.deadline or "",
                        "eligibility": opp.eligibility or "",
                    }

            # STEP 5: Score and rank combined results
            thinking_steps.append(THINKING_STEPS[3])
            for opp in combined:
                opp.match_score = reasoning_engine.multi_factor_score(opp, user_profile)
            scored = sorted(combined, key=lambda x: x.match_score, reverse=True)
            filtered = self._filter_invalid(scored, field=user_profile.get("stream") or intent.get("inferred_field"))

            if not filtered:
                return self._empty_response(
                    query, self._no_results_message(primary_intent),
                    thinking_steps,
                    intent,
                )

            # Confidence check: if best match is weak, say so
            if filtered[0].match_score and filtered[0].match_score < 35:
                weak_msg = f"I couldn't find strong matches for {intent.get('primary_intent', 'opportunities').lower()} in the current database. Here are the closest options available."
                thinking_steps.append(f"Low confidence — best score {filtered[0].match_score:.0f}/100")

            # STEP 6: Eligibility + decision analysis for top candidates
            explained: List[InternalOpportunity] = []
            for opp in filtered[:30]:
                elig = eligibility_checker.check_eligibility(user_profile, opp)
                opp.eligibility_analysis = elig
                opp.decision_analysis = decision_engine.analyze(user_profile, opp, elig)
                opp.chance_estimate = reasoning_engine.estimate_chance(user_profile, opp)
                explained.append(opp)

            # Categorize
            ranked = sorted(explained, key=lambda x: x.match_score, reverse=True)[:30]
            recommendation_categories = reasoning_engine.categorize_recommendations(ranked, user_profile)

            # STEP 7: Groq Reasoning Engine — real reasoning over top 30 candidates
            thinking_steps.append(THINKING_STEPS[4])
            groq_reasoning = await groq_reasoning_engine.reason(
                query=query,
                opportunities=ranked,
                verified_data=verified_map,
                user_profile=user_profile,
                intent_data=groq_intent,
                route_plan=route_plan,
            )

            # STEP 8: Alternatives
            thinking_steps.append(THINKING_STEPS[5])
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

            # Use Groq's summary if available, otherwise fallback
            summary = groq_reasoning.get("summary", "")
            if not summary or not groq_reasoning.get("ai_available"):
                summary = self._generate_summary(ranked, user_profile, primary_intent)

            # Answer-first style: answer the user's question, then recommend opportunities
            response_style = route_plan.get("response_style", "opportunities_first")
            if response_style == "answer_first":
                thinking_steps = [
                    "Understanding what you're looking for",
                    "Analyzing your options",
                    "Preparing your answer",
                ]
                if not groq_reasoning.get("ai_available"):
                    summary = self._answer_first_fallback(intent, user_profile, ranked)

            return {
                "status": "success",
                "query": query,
                "thinking_steps": thinking_steps,
                "user_intent": primary_intent,
                "missing_information": intent.get("missing_information", []),
                "follow_up_required": False,
                "follow_up_questions": [],
                "opportunities": [self._format_opportunity(o) for o in ranked[:15]],
                "alternatives": alternatives,
                "total_found": len(ranked),
                "verified_count": sum(1 for o in ranked if "Live Verified" in (o.verification or {}).get("status", "")),
                "validation_time": str(datetime.now() - start_time),
                "summary": summary,
                "groq_reasoning": {
                    "reasoning": groq_reasoning.get("reasoning", []),
                    "recommendations": groq_reasoning.get("recommendations", []),
                    "comparison": groq_reasoning.get("comparison"),
                    "roadmap": groq_reasoning.get("roadmap", []),
                    "action_checklist": groq_reasoning.get("action_checklist", []),
                    "preparation_tips": groq_reasoning.get("preparation_tips", {}),
                    "ai_available": groq_reasoning.get("ai_available", False),
                },
                "recommendation_categories": {
                    k: self._format_opportunity(v) if v else None
                    for k, v in recommendation_categories.items() if k != "others"
                },
                "recommendation_others": [self._format_opportunity(o) for o in recommendation_categories.get("others", [])],
                "user_profile": {
                    "qualification": user_profile.get("current_education"),
                    "field": user_profile.get("stream") or intent.get("inferred_field"),
                    "country": user_profile.get("target_country") or "India",
                    "career_paths": intent.get("inferred_career_paths", []),
                },
            }

        except Exception as e:
            logger.error(f"Discovery error: {e}", exc_info=True)
            return {"status": "error", "message": str(e), "thinking_steps": thinking_steps}

    VALID_QUALS = {"bsc", "bca", "b.tech", "be", "ba", "bcom", "bba", "mca",
                   "msc", "m.tech", "me", "ma", "mcom", "mba", "mbbs", "phd",
                   "bachelor", "master", "graduate", "postgraduate", "12th",
                   "diploma", "iti", "intermediate"}

    def _safe_qual(self, qual: str) -> str:
        """Validate qualification — never display raw parser values like 'Me'."""
        if not qual:
            return "your qualification"
        q = qual.strip().lower()
        if q in self.VALID_QUALS:
            return qual.strip()
        return "your qualification"

    def _answer_first_fallback(self, intent: Dict, user_profile: Dict, opportunities: List) -> str:
        """Fallback summary when Groq reasoning is unavailable — answers the question directly."""
        intent_type = intent.get("primary_intent", "Opportunity Search").lower()
        qual = self._safe_qual(user_profile.get("current_education") or intent.get("qualification") or "")
        field = user_profile.get("stream") or intent.get("field") or "your field"

        if "loan" in intent_type or "education loan" in intent_type:
            parts = [f"Here's an overview of education loans for {qual} graduates."]
            if opportunities:
                parts.append(f"Top options: {', '.join(o.title for o in opportunities[:3])}.")
            parts.append("Education loans are available through banks and government schemes. Check eligibility, interest rates, and repayment terms before applying.")
            return " ".join(parts)

        if "career" in intent_type:
            parts = [f"Here are career options for {qual} graduates in {field}."]
            if opportunities:
                parts.append(f"Relevant opportunities include: {', '.join(o.title for o in opportunities[:3])}.")
            parts.append("Consider your interests, job market demand, and further study options when choosing a path.")
            return " ".join(parts)

        if "government" in intent_type or "scheme" in intent_type:
            parts = [f"Here are government schemes relevant to {qual} students."]
            if opportunities:
                parts.append(f"Found: {', '.join(o.title for o in opportunities[:3])}.")
            parts.append("Government schemes often have specific eligibility criteria — verify each before applying.")
            return " ".join(parts)

        if "phd" in intent_type or "doctorate" in intent_type:
            parts = [f"Here are PhD opportunities matching your profile in {field}."]
            if opportunities:
                parts.append(f"Top positions: {', '.join(o.title for o in opportunities[:3])}.")
            parts.append("Funded PhD positions include stipends and research budgets. Check application deadlines and supervisor availability.")
            return " ".join(parts)

        if "startup" in intent_type or "entrepreneur" in intent_type:
            parts = ["Here are startup grants and programs you can explore."]
            if opportunities:
                parts.append(f"Relevant programs: {', '.join(o.title for o in opportunities[:3])}.")
            parts.append("Startup programs offer funding, mentorship, and incubation support. Check eligibility criteria before applying.")
            return " ".join(parts)

        if "master" in intent_type or "bachelor" in intent_type:
            parts = [f"Here are {'Masters' if 'master' in intent_type else 'Bachelor'} programs for {qual} students in {field}."]
            if opportunities:
                parts.append(f"Found: {', '.join(o.title for o in opportunities[:3])}.")
            return " ".join(parts)

        return self._no_results_message(intent_type)

    def _no_results_message(self, intent: str) -> str:
        """Build intent-aware fallback message — never hardcode 'scholarship'."""
        intent_lower = intent.lower()
        if "loan" in intent_lower:
            return "I couldn't find any education loans matching your request. Try a different loan amount, country, or check with major banks directly."
        if "job" in intent_lower or "career" in intent_lower:
            return "I couldn't find job or career opportunities matching your profile. Try different keywords or broaden your search to related fields."
        if "internship" in intent_lower:
            return "I couldn't find internships matching your request. Try a different field or check company career pages directly."
        if "phd" in intent_lower or "doctorate" in intent_lower or "doctoral" in intent_lower:
            return "I couldn't find PhD positions matching your request. Try broadening your search — different country, field, or funded doctoral programs."
        if "master" in intent_lower:
            return "I couldn't find Masters programs matching your request. Try different country, field, or funding preference."
        if "bachelor" in intent_lower:
            return "I couldn't find Bachelor programs matching your request. Try a different country or field of study."
        if "fellowship" in intent_lower:
            return "I couldn't find fellowships matching your request. Try different research area or eligibility criteria."
        if "grant" in intent_lower:
            return "I couldn't find grants matching your request. Try a different research area or funding body."
        if "competition" in intent_lower or "hackathon" in intent_lower:
            return "I couldn't find competitions matching your request. Try different categories or check again later for new ones."
        if "startup" in intent_lower or "entrepreneur" in intent_lower:
            return "I couldn't find startup programs matching your request. Try different stage or funding type."
        if "conference" in intent_lower:
            return "I couldn't find conferences matching your request. Try a different field or location."
        if "journal" in intent_lower or "publication" in intent_lower:
            return "I couldn't find journals or publications matching your request. Try a different research area."
        if "visa" in intent_lower:
            return "I couldn't find visa information matching your request. Try different country or visa type."
        if "admission" in intent_lower:
            return "I couldn't find admission information matching your request. Try different university or program."
        if "ranking" in intent_lower:
            return "I couldn't find rankings matching your request. Try a different category or country."
        if "university" in intent_lower or "college" in intent_lower:
            return "I couldn't find universities matching your request. Try different country or program type."
        if "course" in intent_lower:
            return "I couldn't find courses matching your request. Try a different field or institution."
        if "exchange" in intent_lower:
            return "I couldn't find exchange programs matching your request. Try different destination or eligibility."
        if "government" in intent_lower or "scheme" in intent_lower:
            return "I couldn't find government schemes matching your request. Try different category or check your eligibility."
        if "research" in intent_lower:
            return "I couldn't find research opportunities matching your request. Try different field or institution."
        if "eligibility" in intent_lower:
            return "I couldn't determine eligibility — the specific program wasn't found. Try a different program or provide more details."
        if "scholarship" in intent_lower or "funding" in intent_lower or "financial" in intent_lower:
            return "I couldn't find scholarships or funding matching your request. Try different country, field, or eligibility criteria."
        return "I couldn't find any opportunities matching your request. Try broadening your search — different country, field, or program type."

    def _empty_response(self, query, msg, steps, intent=None):
        return {
            "status": "success", "query": query,
            "thinking_steps": steps or ["Searching datasets..."],
            "opportunities": [], "alternatives": [], "total_found": 0, "verified_count": 0,
            "summary": msg,
            "user_intent": intent.get("intent") if intent else None,
            "missing_information": intent.get("missing_information", []) if intent else [],
            "follow_up_required": False, "career_paths": [],
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

    def _filter_invalid(self, opportunities, field: str = None):
        valid = []
        irrelevant_keywords = {
            "Computer Science": ["agriculture", "forest", "marine", "fishery", "veterinary", "dental", "pharmacy", "nursing", "hotel", "tourism"],
            "Science": ["commerce", "mba", "marketing", "hotel"],
            "Commerce": ["engineering", "computer", "mechanical", "electrical", "civil", "physics", "chemistry", "biology"],
        }
        exclude = irrelevant_keywords.get(field, []) if field else []

        for opp in opportunities:
            if opp.deadline and opp.deadline != "Unknown":
                dl = self._parse_deadline(opp.deadline)
                if dl and dl < datetime.now():
                    continue
            if (opp.match_score or 0) < 25:
                continue
            if exclude:
                title_lower = (opp.title or "").lower()
                desc_lower = (opp.description or "").lower()
                cat_lower = (opp.category or "").lower()
                combined = f"{title_lower} {desc_lower} {cat_lower}"
                if any(kw in combined for kw in exclude):
                    opp.match_score = max(0, (opp.match_score or 0) - 30)
                    if (opp.match_score or 0) < 10:
                        continue
            valid.append(opp)
        return valid

    def _format_opportunity(self, opp: InternalOpportunity) -> Dict[str, Any]:
        da = opp.decision_analysis or {}
        elig = opp.eligibility_analysis or {}
        return {
            "id": opp.id, "title": opp.title,
            "provider": "Official source" if not opp.provider or opp.provider in ("Unknown", "Unknown Provider", "N/A") else opp.provider,
            "country": opp.country, "category": opp.category, "degree": opp.degree,
            "funding": opp.funding_type or "", "funding_type": opp.funding_type or "",
            "deadline": opp.deadline or opp.live_deadline,
            "eligibility": opp.eligibility, "description": opp.description,
            "official_url": opp.verified_url or opp.official_url,
            "match_score": round(opp.match_score or 0, 1),
            "decision_analysis": da, "eligibility_checks": elig,
            "next_steps": elig.get("next_steps", []),
        }

    def _generate_summary(self, opportunities, user_profile, intent=""):
        if not opportunities:
            return "I couldn't find any active opportunities matching your request. Try broadening your search."
        qual = user_profile.get("current_education") or user_profile.get("qualification") or ""
        field = user_profile.get("stream") or user_profile.get("field") or ""
        top = opportunities[0]

        parts = []
        if qual:
            parts.append(f"as a {qual} graduate")
        if field:
            parts.append(f"in {field}")
        profile_str = f"Based on your profile{' ' + ' '.join(parts) if parts else ''}"

        intent_label = intent.replace("_", " ").title() if intent else "opportunities"
        return f"{profile_str}, here are the best matching {intent_label}. Top recommendation: {top.title}."


master_decision_engine = MasterDecisionEngine()
