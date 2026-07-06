from typing import List, Dict, Any
from rapidfuzz import fuzz
from ..models.opportunity import InternalOpportunity
from .dataset_loader import dataset_loader
from .synonyms import expand_query_terms, normalize_term, DEGREE_SYNONYMS, FIELD_SYNONYMS
from ..utils.logger import get_logger

logger = get_logger(__name__)


class SearchEngine:
    """Weighted ranking: RapidFuzz + provider + country + course + field + synonyms."""

    def search(self, parsed_query: Dict[str, Any], top_k: int = 20) -> List[InternalOpportunity]:
        opportunities = dataset_loader.opportunities
        if not opportunities:
            return []

        keywords = parsed_query.get("keywords", "") or ""
        countries = parsed_query.get("countries", []) or []
        categories = parsed_query.get("categories", []) or []
        degrees = parsed_query.get("degrees", []) or []
        funding = parsed_query.get("funding", []) or []
        field = parsed_query.get("field", "") or ""
        provider_hints = parsed_query.get("provider_hints", []) or []

        expanded_keywords = expand_query_terms(keywords)
        if field:
            expanded_keywords.update(expand_query_terms(field))

        scored_opportunities = []

        for opp in opportunities:
            fuzz_score = 0.0
            country_score = 0.0
            degree_score = 0.0
            funding_score = 0.0
            category_score = 0.0
            provider_score = 0.0
            field_score = 0.0
            course_score = 0.0

            opp_text = f"{opp.title} {opp.provider} {opp.description or ''} {opp.category or ''}".lower()

            # Country match (15%)
            if countries and opp.country:
                opp_c = opp.country.lower()
                if any(c in opp_c or opp_c in c for c in countries):
                    country_score = 15.0

            # Degree match (10%)
            if degrees and opp.degree:
                opp_deg = normalize_term(opp.degree.lower(), DEGREE_SYNONYMS)
                if any(normalize_term(d, DEGREE_SYNONYMS) in opp_deg or opp_deg in normalize_term(d, DEGREE_SYNONYMS) for d in degrees):
                    degree_score = 10.0
            elif degrees:
                for d in degrees:
                    if normalize_term(d, DEGREE_SYNONYMS) in opp_text:
                        degree_score = 8.0
                        break

            # Category match (5%)
            if categories and opp.category:
                opp_cat = opp.category.lower()
                if any(cat in opp_cat for cat in categories):
                    category_score = 5.0

            # Funding match (10%)
            if funding and opp.funding_type:
                opp_fund = opp.funding_type.lower()
                if any(f in opp_fund for f in funding):
                    funding_score = 10.0

            # Provider match (10%)
            if provider_hints and opp.provider:
                prov_lower = opp.provider.lower()
                for hint in provider_hints:
                    if hint.lower() in prov_lower or hint.lower() in opp_text:
                        provider_score = 10.0
                        break

            # Field / course match (10%)
            if field:
                field_norm = normalize_term(field.lower(), FIELD_SYNONYMS)
                if field_norm in opp_text or field.lower() in opp_text:
                    field_score = 10.0
                else:
                    for term in expanded_keywords:
                        if len(term) > 2 and term in opp_text:
                            field_score = max(field_score, 5.0)

            # Course match via keywords
            if keywords:
                kw_lower = keywords.lower()
                if kw_lower in opp.title.lower() or kw_lower in (opp.description or "").lower():
                    course_score = 5.0

            # RapidFuzz (40%) — with synonym-expanded query
            search_text = keywords
            if field:
                search_text = f"{search_text} {field}"
            if expanded_keywords:
                search_text = f"{search_text} {' '.join(expanded_keywords)}"

            if search_text.strip():
                text_to_search = f"{opp.title} {opp.provider} {opp.description or ''}"
                raw_fuzz = fuzz.token_set_ratio(search_text.lower(), text_to_search.lower())
                fuzz_score = raw_fuzz * 0.40
            else:
                fuzz_score = 20.0

            total_score = (
                fuzz_score + country_score + degree_score + funding_score
                + category_score + provider_score + field_score + course_score
            )

            if total_score > 30.0:
                from dataclasses import replace
                opp_copy = replace(opp, match_score=total_score)
                scored_opportunities.append(opp_copy)

        scored_opportunities.sort(key=lambda x: x.match_score, reverse=True)
        return scored_opportunities[:top_k]


search_engine = SearchEngine()
