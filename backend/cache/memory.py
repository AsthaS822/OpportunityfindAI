from cachetools import TTLCache
from typing import Dict, Any, List, Optional
from ..config import CACHE_SEARCH_TTL, CACHE_JINA_TTL, CACHE_GROQ_TTL

search_cache = TTLCache(maxsize=1000, ttl=CACHE_SEARCH_TTL)
jina_cache = TTLCache(maxsize=1000, ttl=CACHE_JINA_TTL)
groq_cache = TTLCache(maxsize=1000, ttl=CACHE_GROQ_TTL)

_cache_stats = {
    "search_hits": 0,
    "search_misses": 0,
    "jina_hits": 0,
    "jina_misses": 0,
    "groq_hits": 0,
    "groq_misses": 0,
}


def get_cache_stats() -> Dict[str, Any]:
    return {
        **_cache_stats,
        "search_size": len(search_cache),
        "jina_size": len(jina_cache),
        "groq_size": len(groq_cache),
    }


def cache_get(cache: TTLCache, key: str, stat_prefix: str):
    val = cache.get(key)
    if val is not None:
        _cache_stats[f"{stat_prefix}_hits"] = _cache_stats.get(f"{stat_prefix}_hits", 0) + 1
    else:
        _cache_stats[f"{stat_prefix}_misses"] = _cache_stats.get(f"{stat_prefix}_misses", 0) + 1
    return val


class SessionHistory:
    def __init__(self, max_history: int = 10):
        self.history: List[str] = []
        self.profiles: Dict[str, Dict[str, Any]] = {}
        self.max_history = max_history

    def add(self, query: str, session_id: str = "default"):
        if query not in self.history:
            self.history.insert(0, query)
            if len(self.history) > self.max_history:
                self.history.pop()

    def get_profile(self, session_id: str = "default") -> Dict[str, Any]:
        return self.profiles.get(session_id, {})

    def update_profile(self, session_id: str, intent: Dict[str, Any]):
        existing = self.profiles.get(session_id, {})
        for key, val in intent.items():
            if val is not None and val != [] and val != {} and val != "" and val is not False:
                if key not in ("original_query", "missing_information", "follow_up_required", "follow_up_questions", "keywords"):
                    existing[key] = val
        self.profiles[session_id] = existing

    def intent_to_profile(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """Convert structured intent to eligibility_checker profile format."""
        marks = intent.get("marks") or {}
        if intent.get("cgpa") and "cgpa" not in marks:
            marks["cgpa"] = intent["cgpa"]
        if intent.get("percentage") and "percentage" not in marks:
            marks["percentage"] = intent["percentage"]

        test_scores = {}
        for t in ("ielts", "toefl", "gre", "gmat", "sat", "act"):
            if intent.get(t):
                test_scores[t] = intent[t]

        return {
            "query": intent.get("original_query", ""),
            "intent": intent.get("intent", ""),
            "current_education": intent.get("qualification"),
            "target_degree": intent.get("degree") or intent.get("desired_qualification"),
            "target_country": intent.get("country"),
            "stream": intent.get("field") or intent.get("specialization"),
            "funding_requirement": intent.get("funding"),
            "marks": marks if marks else None,
            "work_experience": intent.get("work_experience"),
            "test_scores": test_scores if test_scores else None,
            "age": intent.get("age"),
            "budget": intent.get("budget"),
            "is_domestic": intent.get("country") == "India" if intent.get("country") else None,
            "missing_information": intent.get("missing_information", []),
            "field": intent.get("field"),
            "qualification": intent.get("qualification"),
            "cgpa": intent.get("cgpa"),
            "countries": intent.get("countries", []),
        }


session_history = SessionHistory()
