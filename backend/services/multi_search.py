"""Multi-step search strategies — merge, rank, deduplicate."""

from typing import Dict, List, Any, Set
from ..models.opportunity import InternalOpportunity
from .search_engine import search_engine
from .synonyms import expand_field_terms, INTENT_PROVIDERS, COUNTRY_SYNONYMS
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MultiSearch:
    """Execute multiple search strategies and merge results."""

    PROVIDER_KEYWORDS = {
        "daad": "DAAD",
        "erasmus": "Erasmus",
        "deutschlandstipendium": "Deutschlandstipendium",
        "fulbright": "Fulbright",
        "chevening": "Chevening",
        "commonwealth": "Commonwealth",
        "aicte": "AICTE",
        "ugc": "UGC",
    }

    def search(self, intent: Dict[str, Any], top_k: int = 25) -> List[InternalOpportunity]:
        all_results: List[InternalOpportunity] = []
        seen_ids: Set[str] = set()

        base_params = self._intent_to_params(intent)
        strategies = self._build_strategies(intent, base_params)

        for strategy_name, params in strategies:
            results = search_engine.search(params, top_k=top_k)
            added = 0
            for opp in results:
                if opp.id not in seen_ids:
                    seen_ids.add(opp.id)
                    all_results.append(opp)
                    added += 1
            logger.info(f"Multi-search [{strategy_name}]: {added} new results")

        all_results.sort(key=lambda x: x.match_score, reverse=True)
        return all_results[:top_k]

    def _intent_to_params(self, intent: Dict) -> Dict[str, Any]:
        from .query_parser import query_parser
        return query_parser.to_search_params(intent)

    def _build_strategies(self, intent: Dict, base: Dict) -> List[tuple]:
        strategies = [("primary", base)]

        country = (intent.get("country") or "").lower()
        if country:
            strategies.append(("country", {**base, "keywords": country, "countries": [country]}))

            providers = INTENT_PROVIDERS.get(country, INTENT_PROVIDERS.get("study_abroad", []))
            for provider in providers:
                strategies.append((
                    f"provider_{provider}",
                    {**base, "keywords": provider, "provider_hints": [provider]},
                ))

            if country == "germany":
                strategies.append(("university_scholarships", {
                    **base, "keywords": "university scholarship germany", "countries": ["germany"],
                }))

        field = intent.get("field") or intent.get("specialization")
        if field:
            for term in expand_field_terms(field):
                strategies.append((
                    f"field_{term[:20]}",
                    {**base, "keywords": term, "field": term},
                ))

        intent_type = intent.get("intent", "")
        if intent_type == "Government Scheme":
            strategies.append(("govt_schemes", {**base, "keywords": "government scheme india", "categories": ["scheme"]}))
        elif intent_type == "Education Loan":
            strategies.append(("loans", {**base, "keywords": "education loan", "categories": ["loan"]}))
        elif intent_type == "Internship":
            strategies.append(("internships", {**base, "keywords": "internship", "categories": ["internship"]}))

        if intent.get("fully_funded") or intent.get("funding") == "Fully Funded":
            strategies.append(("fully_funded", {**base, "funding": ["fully funded", "full ride"]}))

        return strategies


multi_search = MultiSearch()
