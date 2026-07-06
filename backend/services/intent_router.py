"""
INTENT ROUTER — decides WHAT to search, WHICH datasets to use, and HOW to respond.
Maps intent → search strategy, dataset filter, response style.
"""

from typing import Dict, List, Any
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Category whitelist per intent — only these dataset categories are searched
INTENT_CATEGORY_MAP = {
    "Scholarship": ["scholarship"],
    "Scholarship Search": ["scholarship"],
    "Loan": ["loan"],
    "Loan Search": ["loan"],
    "Government Scheme": ["scheme"],
    "Internship": ["internship"],
    "Internship Search": ["internship"],
    "Fellowship": ["fellowship"],
    "Fellowship Search": ["fellowship"],
    "Grant": ["grant"],
    "Grant Search": ["grant"],
    "Research Grant": ["research", "grant"],
    "Research Search": ["research", "fellowship"],
    "Research Position": ["research", "fellowship"],
    "PhD Search": ["research", "fellowship"],
    "Masters Search": ["scholarship"],
    "Bachelor Search": ["scholarship"],
    "Exchange Search": ["exchange program"],
    "Competition": ["competition"],
    "Competition Search": ["competition"],
    "Startup": ["grant", "scheme"],
    "Startup Search": ["grant", "scheme"],
    "Study Abroad": [],
    "Career Advice": [],
    "Job Search": [],
    "University Search": [],
    "Course Search": [],
    "Conference Search": [],
    "Journal Search": [],
    "Visa Search": [],
    "Admission Search": [],
    "Ranking Search": [],
    "Comparison": [],
    "Eligibility Check": [],
    "Explain": [],
    "Decision": [],
    "Decision Help": [],
    "Roadmap": [],
    "Funding": [],
    "Opportunity Search": [],
    "General Search": [],
}

# Response style per intent
INTENT_RESPONSE_STYLE = {
    "Career Advice": "answer_first",
    "Loan": "answer_first",
    "Loan Search": "answer_first",
    "Government Scheme": "answer_first",
    "Startup": "answer_first",
    "Startup Search": "answer_first",
    "Scholarship": "opportunities_first",
    "Scholarship Search": "opportunities_first",
    "PhD Search": "answer_first",
    "Masters Search": "answer_first",
    "Bachelor Search": "answer_first",
    "Explain": "answer_first",
    "Decision": "answer_first",
    "Decision Help": "answer_first",
    "Roadmap": "answer_first",
    "Comparison": "answer_first",
    "Eligibility Check": "answer_first",
    "Job Search": "answer_first",
    "Internship": "opportunities_first",
    "Internship Search": "opportunities_first",
    "Fellowship": "opportunities_first",
    "Fellowship Search": "opportunities_first",
    "Research Search": "opportunities_first",
    "Research Position": "opportunities_first",
    "Grant": "opportunities_first",
    "Grant Search": "opportunities_first",
    "Research Grant": "opportunities_first",
    "Exchange Search": "opportunities_first",
    "Competition": "opportunities_first",
    "Competition Search": "opportunities_first",
    "Funding": "opportunities_first",
}

# Web search needed per intent
INTENT_WEB_SEARCH = {
    "Career Advice": True,
    "Loan": True,
    "Loan Search": True,
    "Government Scheme": True,
    "Startup": True,
    "Startup Search": True,
    "Scholarship": True,
    "Scholarship Search": True,
    "PhD Search": True,
    "Study Abroad": True,
    "Job Search": True,
    "Internship": True,
    "Internship Search": True,
    "Research Search": True,
    "Research Position": True,
    "Fellowship": True,
    "Fellowship Search": True,
    "Conference Search": True,
    "Journal Search": True,
    "Ranking Search": True,
    "Visa Search": True,
    "Admission Search": True,
}


class IntentRouter:
    """Routes intent to the correct search strategy, datasets, and response format."""

    def route(self, intent_data: Dict[str, Any]) -> Dict[str, Any]:
        primary_intent = intent_data.get("primary_intent", intent_data.get("intent", "Opportunity Search"))

        # Map to known intent keys (try variations)
        intent_key = self._resolve_intent_key(primary_intent)

        categories = INTENT_CATEGORY_MAP.get(intent_key, [])
        response_style = INTENT_RESPONSE_STYLE.get(intent_key, "opportunities_first")
        needs_web = INTENT_WEB_SEARCH.get(intent_key, False)

        # Determine if dataset should be searched at all
        search_dataset = intent_key not in (
            "Career Advice", "Explain", "Decision", "Decision Help",
            "Roadmap", "Comparison", "Visa Search", "Admission Search"
        )

        # Max candidates to retrieve
        top_k = 50 if search_dataset else 10

        plan = {
            "intent_key": intent_key,
            "categories": categories,
            "response_style": response_style,
            "needs_web_search": needs_web,
            "search_dataset": search_dataset,
            "top_k": top_k,
            "needs_verification": search_dataset and intent_key not in ("Career Advice", "Explain"),
        }

        logger.info(
            f"IntentRouter: {intent_key} -> "
            f"categories={categories}, "
            f"style={response_style}, "
            f"web={needs_web}, "
            f"dataset={search_dataset}"
        )
        return plan

    def _resolve_intent_key(self, intent: str) -> str:
        """Normalize intent string to known keys."""
        if not intent:
            return "Opportunity Search"
        # Exact match
        if intent in INTENT_CATEGORY_MAP:
            return intent
        # Try "X Search" -> "X"
        if intent.endswith(" Search") and intent[:-7] in INTENT_CATEGORY_MAP:
            return intent[:-7]
        # Unknown — return as-is (will fall to empty categories)
        return intent


intent_router = IntentRouter()
