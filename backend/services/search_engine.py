from typing import List, Dict, Any
from datetime import datetime
from rapidfuzz import fuzz
from ..models.opportunity import InternalOpportunity
from .dataset_loader import dataset_loader
from .synonyms import expand_query_terms, normalize_term, DEGREE_SYNONYMS, FIELD_SYNONYMS
from ..utils.logger import get_logger

logger = get_logger(__name__)

VALID_QUALIFICATIONS = {"bsc", "bca", "b.tech", "be", "ba", "bcom", "bba", "mca", "msc", "m.tech", "me",
                        "ma", "mcom", "mba", "mbbs", "phd", "bachelor", "master", "graduate", "postgraduate",
                        "12th", "diploma", "iti", "intermediate"}


class SearchEngine:
    """Weighted ranking: RapidFuzz + provider + country + course + field + synonyms.
    Applies hard filters (country, category, active status) before scoring.
    """

    def search(self, parsed_query: Dict[str, Any], top_k: int = 50) -> List[InternalOpportunity]:
        opportunities = dataset_loader.opportunities
        if not opportunities:
            return []

        keywords = parsed_query.get("keywords", "") or ""
        countries = parsed_query.get("countries", []) or []
        categories = parsed_query.get("categories", []) or []
        degrees = parsed_query.get("degrees", []) or []
        funding = parsed_query.get("funding", []) or []
        field = parsed_query.get("field", "") or ""

        expanded_keywords = expand_query_terms(keywords)
        if field:
            expanded_keywords.update(expand_query_terms(field))

        scored_opportunities = []

        for opp in opportunities:
            # HARD FILTER 1: Category — broad match against full text, not just category field
            # Dataset categories can be single-letter codes (QS rankings) or multi-tag (schemes)
            if categories:
                opp_cat = (opp.category or "").lower()
                opp_full = opp_text if 'opp_text' in dir() else f"{opp.title or ''} {opp.provider or ''} {(opp.description or '')} {(opp.category or '')}".lower()
                # Check category field first (precise), then full text (broad)
                cat_match = any(cat in opp_cat for cat in categories)
                if not cat_match:
                    cat_match = any(cat in opp_full for cat in categories)
                if not cat_match:
                    # For datasets with single-letter categories (QS), don't hard-filter
                    if len(opp_cat) == 1 or opp_cat in ("xs", "s", "m", "l", "xl"):
                        pass  # skip filter — this is a size category, not a content category
                    else:
                        continue

            # HARD FILTER 2: Country — skip if countries specified and opp has a different country
            if countries and opp.country:
                opp_c = opp.country.lower()
                if not any(c in opp_c or opp_c in c for c in countries):
                    continue

            # HARD FILTER 3: Active/valid — skip expired or empty opportunities
            if not opp.title or len((opp.title or "").strip()) < 3:
                continue
            if opp.provider and "unknown" in opp.provider.lower() and not opp.description:
                continue
            if opp.deadline and opp.deadline != "Unknown":
                try:
                    dl = datetime.strptime(opp.deadline.strip(), "%Y-%m-%d")
                    if dl < datetime.now():
                        continue
                except ValueError:
                    pass

            # SCORING
            fuzz_score = 0.0
            country_score = 0.0
            degree_score = 0.0
            funding_score = 0.0
            category_score = 0.0
            field_score = 0.0
            title_score = 0.0

            opp_text = f"{opp.title or ''} {opp.provider or ''} {(opp.description or '')} {(opp.category or '')}".lower()

            # Country match (10%)
            if countries and opp.country:
                opp_c = opp.country.lower()
                if any(c in opp_c or opp_c in c for c in countries):
                    country_score = 10.0

            # Degree match (10%) — soft signal since dataset lacks structured degree field
            if degrees and opp.degree:
                opp_deg = normalize_term(opp.degree.lower(), DEGREE_SYNONYMS)
                if any(normalize_term(d, DEGREE_SYNONYMS) in opp_deg or opp_deg in normalize_term(d, DEGREE_SYNONYMS) for d in degrees):
                    degree_score = 10.0
            elif degrees:
                deg_words = set()
                for d in degrees:
                    norm = normalize_term(d, DEGREE_SYNONYMS)
                    deg_words.add(norm)
                    for part in norm.replace("-", " ").split():
                        deg_words.add(part)
                if deg_words & set(opp_text.split()):
                    degree_score = 6.0
                for d in degrees:
                    if normalize_term(d, DEGREE_SYNONYMS) in opp_text:
                        degree_score = 8.0
                        break

            # Category match (10%)
            if categories and opp.category:
                opp_cat = opp.category.lower()
                if any(cat in opp_cat for cat in categories):
                    category_score = 10.0

            # Funding match (5%)
            if funding and opp.funding_type:
                opp_fund = opp.funding_type.lower()
                if any(f in opp_fund for f in funding):
                    funding_score = 5.0

            # Field / course match (10%)
            if field:
                field_norm = normalize_term(field.lower(), FIELD_SYNONYMS)
                if field_norm in opp_text or field.lower() in opp_text:
                    field_score = 10.0
                else:
                    for term in expanded_keywords:
                        if len(term) > 2 and term in opp_text:
                            field_score = max(field_score, 5.0)

            # Title match bonus (5%)
            if keywords and opp.title:
                kw_lower = keywords.lower()
                title_lower = opp.title.lower()
                if kw_lower in title_lower:
                    title_score = 8.0
                elif any(word in title_lower for word in kw_lower.split() if len(word) > 2):
                    title_score = 4.0

            # RapidFuzz (40%)
            search_text = keywords
            if field:
                search_text = f"{search_text} {field}"
            if expanded_keywords:
                search_text = f"{search_text} {' '.join(expanded_keywords)}"

            if search_text.strip():
                text_to_search = f"{opp.title or ''} {opp.provider or ''} {(opp.description or '')}"
                raw_fuzz = fuzz.token_set_ratio(search_text.lower(), text_to_search.lower())
                fuzz_score = raw_fuzz * 0.40
            else:
                fuzz_score = 20.0

            total_score = (
                fuzz_score + country_score + degree_score + funding_score
                + category_score + field_score + title_score
            )

            if total_score > 25.0:
                from dataclasses import replace
                opp_copy = replace(opp, match_score=total_score)
                scored_opportunities.append(opp_copy)

        scored_opportunities.sort(key=lambda x: x.match_score, reverse=True)
        return scored_opportunities[:max(top_k, 100)]


search_engine = SearchEngine()
