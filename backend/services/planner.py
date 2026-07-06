"""
AI PLANNER — decides WHAT to do: search immediately, ask follow-up, show career paths, or compare.
"""

from typing import Dict, List, Optional, Any
from ..utils.logger import get_logger

logger = get_logger(__name__)

CAREER_PATHS_BY_DEGREE = {
    "mca": [
        {"id": "jobs", "label": "💼 Jobs", "desc": "Software Engineering, Data Science, Cloud, DevOps"},
        {"id": "higher_studies", "label": "🎓 Higher Studies", "desc": "M.Tech, MS, PhD abroad or in India"},
        {"id": "study_abroad", "label": "🌍 Study Abroad", "desc": "Germany, Canada, Ireland, Finland, Sweden"},
        {"id": "research", "label": "📚 Research", "desc": "AI/ML research, PhD, Research Assistant"},
        {"id": "scholarships", "label": "💰 Scholarships", "desc": "DAAD, Erasmus, Commonwealth, Fulbright"},
        {"id": "certifications", "label": "📜 Certifications", "desc": "Cloud (AWS/Azure), AI/ML, DevOps"},
        {"id": "startups", "label": "🚀 Startups", "desc": "Build your own product or join early-stage startup"},
        {"id": "govt_exams", "label": "🏛 Government Exams", "desc": "UPSC, State PSC, Banking, SSC"},
    ],
    "bca": [
        {"id": "higher_studies", "label": "🎓 Higher Studies", "desc": "MCA, M.Tech, MS, MBA"},
        {"id": "jobs", "label": "💼 Jobs", "desc": "Software Developer, Web Developer, IT Support, Data Analytics"},
        {"id": "study_abroad", "label": "🌍 Study Abroad", "desc": "MS in CS/IT abroad"},
        {"id": "certifications", "label": "📜 Certifications", "desc": "AWS, Azure, Google Cloud, CCNA"},
    ],
    "b.tech": [
        {"id": "higher_studies", "label": "🎓 Higher Studies", "desc": "M.Tech, MS, MBA, PhD"},
        {"id": "jobs", "label": "💼 Jobs", "desc": "Core Engineering, Software, Consulting, R&D"},
        {"id": "study_abroad", "label": "🌍 Study Abroad", "desc": "MS in Engineering/CS abroad"},
        {"id": "research", "label": "📚 Research", "desc": "PhD, Research Assistant, Innovation"},
    ],
    "bsc": [
        {"id": "higher_studies", "label": "🎓 Higher Studies", "desc": "MSc, PhD, Integrated PhD"},
        {"id": "jobs", "label": "💼 Jobs", "desc": "Research, Lab, Data Analysis, Science Communication"},
        {"id": "research", "label": "📚 Research", "desc": "Academic research, PhD"},
    ],
    "b.com": [
        {"id": "higher_studies", "label": "🎓 Higher Studies", "desc": "M.Com, MBA, CA, CFA"},
        {"id": "jobs", "label": "💼 Jobs", "desc": "Banking, Finance, Accounting, Audit, Consulting"},
        {"id": "study_abroad", "label": "🌍 Study Abroad", "desc": "MS in Finance, International Business"},
    ],
    "mba": [
        {"id": "jobs", "label": "💼 Jobs", "desc": "Management Consulting, Product, Finance, Marketing"},
        {"id": "startups", "label": "🚀 Startups", "desc": "Entrepreneurship, Venture Capital"},
        {"id": "study_abroad", "label": "🌍 Study Abroad", "desc": "Executive MBA, Global MBA"},
    ],
}

INTENT_SEARCH_MAP = {
    "Scholarship": {"search": True, "strategies": ["scholarships"], "priority": "normal"},
    "Scholarship Search": {"search": True, "strategies": ["scholarships"], "priority": "normal"},
    "University Search": {"search": True, "strategies": ["universities"], "priority": "normal"},
    "Course Search": {"search": True, "strategies": ["courses"], "priority": "normal"},
    "Career Advice": {"search": False, "strategies": ["career_paths"], "priority": "career_first"},
    "Job Search": {"search": True, "strategies": ["jobs"], "priority": "normal"},
    "Internship Search": {"search": True, "strategies": ["internships"], "priority": "normal"},
    "Government Scheme": {"search": True, "strategies": ["govt_schemes"], "priority": "normal"},
    "Loan Search": {"search": True, "strategies": ["loans"], "priority": "normal"},
    "Funding": {"search": True, "strategies": ["funding"], "priority": "normal"},
    "Admission Search": {"search": True, "strategies": ["admissions"], "priority": "normal"},
    "Visa Search": {"search": True, "strategies": ["visa"], "priority": "normal"},
    "Research Search": {"search": True, "strategies": ["research"], "priority": "normal"},
    "Grant Search": {"search": True, "strategies": ["grants"], "priority": "normal"},
    "Research Grant": {"search": True, "strategies": ["research_grants"], "priority": "normal"},
    "Research Position": {"search": True, "strategies": ["research"], "priority": "normal"},
    "PhD Search": {"search": True, "strategies": ["phd"], "priority": "normal"},
    "Masters Search": {"search": True, "strategies": ["masters"], "priority": "normal"},
    "Bachelor Search": {"search": True, "strategies": ["bachelor"], "priority": "normal"},
    "Exchange Search": {"search": True, "strategies": ["exchange"], "priority": "normal"},
    "Fellowship Search": {"search": True, "strategies": ["fellowships"], "priority": "normal"},
    "Competition Search": {"search": True, "strategies": ["competitions"], "priority": "normal"},
    "Startup Search": {"search": True, "strategies": ["startups", "grants"], "priority": "normal"},
    "Conference Search": {"search": True, "strategies": ["conferences"], "priority": "normal"},
    "Journal Search": {"search": True, "strategies": ["journals"], "priority": "normal"},
    "Ranking Search": {"search": True, "strategies": ["rankings"], "priority": "normal"},
    "Comparison": {"search": True, "strategies": ["comparison"], "priority": "normal"},
    "Eligibility Check": {"search": True, "strategies": ["eligibility"], "priority": "normal"},
    "Explain": {"search": True, "strategies": ["explain"], "priority": "normal"},
    "Decision": {"search": True, "strategies": ["decisions"], "priority": "normal"},
    "Decision Help": {"search": True, "strategies": ["decisions"], "priority": "normal"},
    "Roadmap": {"search": True, "strategies": ["roadmap"], "priority": "normal"},
    "Grant": {"search": True, "strategies": ["grants"], "priority": "normal"},
    "Study Abroad": {"search": True, "strategies": ["study_abroad"], "priority": "normal"},
    "Opportunity Search": {"search": True, "strategies": ["general"], "priority": "normal"},
    "General Search": {"search": True, "strategies": ["general"], "priority": "normal"},
}

# Thresholds per intent — only filter results, don't gate search
INTENT_THRESHOLDS = {
    "Scholarship": 45, "Loan": 25, "University Search": 35,
    "Government Scheme": 30, "Career Advice": 20, "Job Search": 20,
    "Internship": 20, "PhD": 25, "Masters": 25, "Bachelor": 25,
    "Fellowship": 35, "Exchange": 30, "Grant": 30, "Research Grant": 30,
    "Research Position": 25, "Funding": 35, "Competition": 20,
    "Startup": 20, "Conference": 20, "Journal": 20,
    "Study Abroad": 35, "Opportunity Search": 30,
}


class Planner:
    """Decides WHAT to do — search immediately or ask follow-up."""

    def classify_intent(self, query: str, parsed: Dict) -> str:
        """Return the primary intent from the parsed query."""
        return parsed.get("intent", "Opportunity Search")

    def plan_approach(self, intent: str, parsed: Dict, query: str) -> Dict:
        """Decide the approach based on intent + exploratory flag."""
        plan = {
            "intent": intent,
            "needs_clarification": False,
            "clarification_questions": [],
            "search_strategies": [],
            "needs_career_paths": False,
            "career_paths": [],
            "needs_comparison": False,
            "comparison_items": [],
            "needs_eligibility": False,
            "eligibility_target": None,
            "should_search": True,
            "priority": "normal",
        }

        # Get the base config for this intent
        config = INTENT_SEARCH_MAP.get(intent, {"search": True, "strategies": [], "priority": "normal"})
        plan["search_strategies"] = list(config.get("strategies", []))
        plan["priority"] = config.get("priority", "normal")

        if intent == "Career Advice":
            plan["needs_career_paths"] = True
            qual = (parsed.get("qualification") or "").lower().replace(".", "")
            # Try raw qual first, then try to match from the original query
            raw_qual = (parsed.get("original_query", "") or "").lower()
            degree_key = self._match_degree(qual) or self._match_degree(raw_qual)
            if degree_key and degree_key in CAREER_PATHS_BY_DEGREE:
                plan["career_paths"] = CAREER_PATHS_BY_DEGREE[degree_key]
            # Fallback: try matching "mca", "bca", etc. directly in raw query
            if not plan["career_paths"]:
                import re
                m = re.search(r'\b(mca|bca|b\.tech|m\.tech|bsc|msc|bcom|mcom|bba|mba)\b', raw_qual)
                if m:
                    raw_key = m.group(1).replace(".", "")
                    if raw_key in CAREER_PATHS_BY_DEGREE:
                        plan["career_paths"] = CAREER_PATHS_BY_DEGREE[raw_key]
            # If exploratory career query, still show paths but don't block
            if parsed.get("is_exploratory"):
                plan["should_search"] = True
                plan["priority"] = "normal"
            else:
                plan["needs_clarification"] = True
                plan["should_search"] = False
                plan["priority"] = "career_first"
                questions = []
                if plan["career_paths"]:
                    questions.append("Which direction interests you? Choose a path or describe your preference.")
                else:
                    questions.append("What is your current qualification?")
                plan["clarification_questions"] = questions

        elif intent == "Comparison":
            plan["needs_comparison"] = True
            import re
            parts = re.split(r'\b(vs|versus|and|or)\b', query, flags=re.IGNORECASE)
            plan["comparison_items"] = [p.strip() for p in parts if p.strip() and len(p.strip()) > 2 and p.strip().lower() not in ("vs", "versus", "and", "or")]
            if len(plan["comparison_items"]) < 2:
                plan["comparison_items"] = [query, ""]
            plan["should_search"] = True

        elif intent == "Eligibility Check":
            plan["needs_eligibility"] = True
            plan["eligibility_target"] = parsed.get("keywords") or query
            import re
            for kw in ["daad", "erasmus", "fulbright", "chevening", "commonwealth"]:
                if kw in query.lower():
                    plan["eligibility_target"] = kw.title()
                    break
            plan["should_search"] = True

        # If NOT exploratory and follow-up is required — ask first
        if not parsed.get("is_exploratory") and parsed.get("follow_up_required"):
            plan["needs_clarification"] = True
            plan["clarification_questions"] = parsed.get("follow_up_questions", [])
            plan["should_search"] = False
            plan["priority"] = "ask_first"

        # Always add country/field-based strategies
        country = parsed.get("country")
        if country:
            plan["search_strategies"].append(f"country_{country.lower()}")

        field = parsed.get("field") or parsed.get("inferred_field")
        if field:
            plan["search_strategies"].append(f"field_{field.lower()}")

        logger.info(f"Plan: intent={intent}, search={plan['should_search']}, priority={plan['priority']}, strategies={plan['search_strategies']}")
        return plan

    def get_career_path_questions(self, paths: List[Dict]) -> List[str]:
        if not paths:
            return []
        return ["Which direction interests you? Choose a path or describe your preference."]

    def get_threshold(self, intent: str) -> int:
        return INTENT_THRESHOLDS.get(intent, 30)

    def _match_degree(self, qual: str) -> Optional[str]:
        if not qual:
            return None
        for key in CAREER_PATHS_BY_DEGREE:
            if key in qual:
                return key
        return None


planner = Planner()
