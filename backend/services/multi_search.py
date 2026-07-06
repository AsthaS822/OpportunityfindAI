"""
Multi-source search engine combining dataset analysis with live web verification.
Intelligently searches both internal dataset and live web to provide comprehensive results.
"""

import uuid
from typing import Dict, List, Any, Set, Optional
from datetime import datetime
from ..models.opportunity import InternalOpportunity
from .search_engine import search_engine
from .jina_search import jina_search
from .dataset_analyzer import dataset_analyzer
from .synonyms import expand_field_terms, INTENT_PROVIDERS
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MultiSearch:
    """Execute multiple search strategies and merge results.
    Supports both hardcoded per-intent strategies AND dynamic Groq-generated search targets.
    """

    PROVIDER_KEYWORDS = {
        "daad": "DAAD", "erasmus": "Erasmus",
        "deutschlandstipendium": "Deutschlandstipendium",
        "fulbright": "Fulbright", "chevening": "Chevening",
        "commonwealth": "Commonwealth", "aicte": "AICTE",
        "ugc": "UGC",
    }

    # Per-intent search strategy builders (fallback when Groq is unavailable)
    INTENT_STRATEGIES = {
        "Scholarship": lambda s, b, i: s._scholarship_strategies(b, i),
        "University Search": lambda s, b, i: s._university_strategies(b, i),
        "Course Search": lambda s, b, i: s._course_strategies(b, i),
        "Career Advice": lambda s, b, i: s._career_strategies(b, i),
        "Job Search": lambda s, b, i: s._job_strategies(b, i),
        "Internship": lambda s, b, i: s._internship_strategies(b, i),
        "Government Scheme": lambda s, b, i: s._govt_strategies(b, i),
        "Loan Search": lambda s, b, i: s._loan_strategies(b, i),
        "Funding": lambda s, b, i: s._funding_strategies(b, i),
        "Admission Search": lambda s, b, i: s._admission_strategies(b, i),
        "Visa Search": lambda s, b, i: s._visa_strategies(b, i),
        "Research Search": lambda s, b, i: s._research_strategies(b, i),
        "Grant Search": lambda s, b, i: s._research_grant_strategies(b, i),
        "Research Position": lambda s, b, i: s._research_position_strategies(b, i),
        "PhD Search": lambda s, b, i: s._phd_strategies(b, i),
        "Masters Search": lambda s, b, i: s._masters_strategies(b, i),
        "Bachelor Search": lambda s, b, i: s._bachelor_strategies(b, i),
        "Exchange Search": lambda s, b, i: s._exchange_strategies(b, i),
        "Fellowship Search": lambda s, b, i: s._fellowship_strategies(b, i),
        "Competition Search": lambda s, b, i: s._competition_strategies(b, i),
        "Startup Search": lambda s, b, i: s._startup_strategies(b, i),
        "Conference Search": lambda s, b, i: s._conference_strategies(b, i),
        "Journal Search": lambda s, b, i: s._journal_strategies(b, i),
        "Ranking Search": lambda s, b, i: s._ranking_strategies(b, i),
        "Comparison": lambda s, b, i: s._comparison_strategies(b, i),
        "Eligibility Check": lambda s, b, i: s._eligibility_strategies(b, i),
        "Grant Search": lambda s, b, i: s._grant_strategies(b, i),
        "Study Abroad": lambda s, b, i: s._study_abroad_strategies(b, i),
        "Opportunity Search": lambda s, b, i: s._general_strategies(b, i),
        "General Search": lambda s, b, i: s._general_strategies(b, i),
    }

    async def search(self, intent: Dict[str, Any], top_k: int = 50) -> List[InternalOpportunity]:
        """
        Hybrid intelligent search combining:
        1. Dataset analysis (understand what exists)
        2. Smart expansion (what else to search)
        3. Live web search (verify + find new)
        4. Merge + rank (best of both)
        """
        all_results: List[InternalOpportunity] = []
        seen_ids: Set[str] = set()
        intent_type = intent.get("intent", intent.get("primary_intent", "Opportunity Search"))

        # STEP 1: Dataset Intelligence - Analyze and expand search
        logger.info(f"[DATASET ANALYZER] Starting intelligent analysis for: {intent_type}")
        expansion = dataset_analyzer.smart_search_expansion(intent)
        
        expanded_categories = expansion.get("expanded_categories", [])
        smart_targets = expansion.get("search_targets", [])
        semantic_tags = expansion.get("semantic_tags", [])
        
        logger.info(f"[EXPANSION] Categories: {expanded_categories}, Targets: {len(smart_targets)}, Tags: {semantic_tags}")

        base_params = self._intent_to_params(intent)
        
        # Override categories with expanded ones
        if expanded_categories:
            base_params["categories"] = expanded_categories

        # Inject intent-restricted categories if set (from Intent Router)
        search_categories = intent.get("search_categories")
        if search_categories:
            base_params["categories"] = search_categories
            logger.info(f"Using intent-restricted categories: {search_categories}")

        # Use Groq targets if available, otherwise use dataset analyzer's smart targets
        search_targets = intent.get("search_targets", [])
        if not search_targets and smart_targets:
            search_targets = smart_targets
            logger.info(f"Using dataset analyzer targets: {search_targets}")

        # Build strategies
        if search_targets:
            strategies = self._build_from_targets(search_targets, base_params, intent)
        else:
            strategy_builder = self.INTENT_STRATEGIES.get(intent_type, self._general_strategies)
            strategies = strategy_builder(self, base_params, intent)

        # STEP 2: Search dataset with expanded parameters
        logger.info(f"[DATASET SEARCH] Executing {len(strategies)} strategies")
        for strategy_name, params in strategies:
            results = search_engine.search(params, top_k=50)
            added = 0
            for opp in results:
                if opp.id not in seen_ids:
                    seen_ids.add(opp.id)
                    opp.source_type = "Dataset"
                    all_results.append(opp)
                    added += 1
            if added > 0:
                logger.info(f"  [{strategy_name}]: {added} results")

        dataset_count = len(all_results)
        logger.info(f"[DATASET TOTAL] {dataset_count} opportunities found")

        # STEP 3: Apply semantic filtering if tags available
        if semantic_tags and all_results:
            tagged_results = []
            for opp in all_results:
                opp_text = f"{opp.title} {opp.description}".lower()
                tag_match = any(tag in opp_text for tag in semantic_tags)
                if tag_match:
                    opp.match_score += 10.0  # Boost semantic matches
                    tagged_results.append(opp)
            if len(tagged_results) > dataset_count * 0.3:  # If >30% match, use filtered
                all_results = tagged_results
                logger.info(f"[SEMANTIC FILTER] Reduced to {len(all_results)} semantically relevant results")

        # STEP 4: Decide if web search is needed
        needs_web_search = False
        web_search_reason = ""
        
        country_requested = (intent.get("country") or "").lower()
        if country_requested:
            # Check if we have country-specific results
            country_matches = [r for r in all_results if country_requested in (r.country or "").lower()]
            if len(country_matches) < 5:
                needs_web_search = True
                web_search_reason = f"Low country-specific results ({len(country_matches)})"
        
        if dataset_count < 8:
            needs_web_search = True
            web_search_reason = f"Insufficient dataset results ({dataset_count})"
        
        # Always search web for verification and new opportunities
        if dataset_count > 0:
            needs_web_search = True
            web_search_reason = "Verifying dataset + finding new opportunities"
        
        # STEP 5: Live web search
        if needs_web_search:
            logger.info(f"[WEB SEARCH] Triggered: {web_search_reason}")
            
            # Build smart web queries
            live_targets = search_targets if search_targets else self._build_web_queries(intent)
            
            for idx, target in enumerate(live_targets[:6], 1):  # Limit to 6 web searches
                if target.strip():
                    live_results = await self._search_live_web(target, seen_ids)
                    
                    # Mark as verified from web
                    for lr in live_results:
                        lr.source_type = "Live Web - Verified"
                        lr.match_score += 5.0  # Slight boost for fresh web results
                    
                    all_results.extend(live_results)
                    logger.info(f"  [Web {idx}] '{target[:50]}': {len(live_results)} results")
        
        total_results = len(all_results)
        web_results = total_results - dataset_count
        logger.info(f"[TOTAL] {total_results} opportunities (Dataset: {dataset_count}, Web: {web_results})")

        # STEP 6: Post-processing filters
        # Filter by user profile if available
        user_profile = {
            "degree": intent.get("degree") or intent.get("qualification"),
            "field": intent.get("field") or intent.get("inferred_field"),
            "budget": intent.get("budget"),
        }
        if any(user_profile.values()):
            all_results = dataset_analyzer.filter_by_profile(all_results, user_profile)
            logger.info(f"[PROFILE FILTER] Filtered to {len(all_results)} profile-relevant results")
        
        # Boost country-specific results if country requested
        if country_requested and len(all_results) > 10:
            for r in all_results:
                if country_requested in (r.country or "").lower():
                    r.match_score += 15.0
            logger.info(f"[COUNTRY BOOST] Applied to {country_requested} results")

        # STEP 7: Final ranking
        all_results.sort(key=lambda x: x.match_score, reverse=True)
        
        # Add explanation metadata to results
        for r in all_results[:top_k]:
            if not hasattr(r, 'search_metadata'):
                r.search_metadata = {}
            r.search_metadata['found_via'] = r.source_type or "Dataset"
            r.search_metadata['confidence'] = "High" if r.match_score > 70 else "Medium" if r.match_score > 50 else "Moderate"
        
        return all_results[:top_k]

    def _build_web_queries(self, intent: Dict) -> List[str]:
        """Build smart web search queries based on user intent and profile."""
        queries = []
        intent_type = intent.get("intent", "")
        country = intent.get("country") or ""
        field = intent.get("field") or intent.get("inferred_field") or ""
        degree = intent.get("degree") or intent.get("qualification") or intent.get("desired_qualification") or ""
        
        # Career-specific queries based on user profile
        if intent_type == "Career Advice":
            if "mca" in degree.lower() or "computer" in field.lower():
                if country and country.lower() != "india":
                    queries.extend([
                        f"Software Engineering jobs {country} 2026",
                        f"Computer Science Masters scholarships {country}",
                        f"Tech internships {country} 2026",
                    ])
                else:
                    queries.extend([
                        "MCA career opportunities India 2026",
                        "Software Engineering jobs India freshers",
                        "Computer Science higher studies India",
                    ])
            elif "btech" in degree.lower() or "engineering" in field.lower():
                if country:
                    queries.extend([
                        f"Engineering jobs {country} 2026",
                        f"Masters Engineering {country} scholarships",
                    ])
                else:
                    queries.extend([
                        "B.Tech career options India 2026",
                        "Engineering jobs India freshers",
                    ])
            elif "mba" in degree.lower() or "business" in field.lower():
                if country:
                    queries.extend([
                        f"MBA programs {country} 2026",
                        f"Business Management careers {country}",
                    ])
                else:
                    queries.extend([
                        "MBA career opportunities India",
                        "Management Consulting jobs India",
                    ])
        
        # Internship queries
        elif intent_type == "Internship":
            base_query = f"{field or 'Engineering'} internships {country or 'India'} 2026"
            queries.extend([
                base_query,
                f"Summer internships {country or 'India'} {field or 'tech'} students",
                f"Paid internships {country or 'India'} 2026",
            ])
        
        # Job search queries
        elif intent_type == "Job Search":
            queries.extend([
                f"{field or degree or 'Engineering'} jobs {country or 'India'} 2026",
                f"Entry level {field or 'tech'} jobs {country or 'India'}",
                f"Freshers jobs {country or 'India'} {field or ''}",
            ])
        
        # Scholarship queries
        elif intent_type == "Scholarship" or "Funding" in intent_type:
            queries.extend([
                f"{degree or 'Masters'} scholarships {country or 'abroad'} {field or ''} 2026",
                f"Fully funded scholarships {country or 'Europe'} {field or ''} 2026",
                f"PhD fellowships {country or 'USA'} {field or ''}",
            ])
        
        # PhD queries
        elif intent_type == "PhD":
            queries.extend([
                f"PhD positions {field or 'Computer Science'} {country or 'Germany'} 2026",
                f"Funded PhD programs {country or 'USA'} {field or ''} 2026",
                f"Doctoral research fellowships {field or ''} {country or 'Europe'}",
            ])
        
        # University search
        elif intent_type == "University Search":
            queries.extend([
                f"Top universities {country or 'USA'} {field or ''} 2026",
                f"Best {degree or 'Masters'} programs {country or 'Europe'} {field or ''}",
            ])
        
        # Default fallback
        if not queries:
            original_query = intent.get("original_query", "")
            if original_query:
                queries.append(f"{original_query} official opportunities 2026")
        
        return queries[:5]  # Limit to 5 queries

    async def _search_live_web(self, query: str, seen_ids: Set[str]) -> List[InternalOpportunity]:
        """Search live web via Jina and convert results to InternalOpportunity objects."""
        raw_results = await jina_search.search(query)
        if not raw_results:
            return []

        results = []
        for item in raw_results[:10]:
            title = item.get("title", "") or ""
            url = item.get("url", "") or ""
            description = item.get("description", "") or ""

            if not title or not url:
                continue

            # Generate a unique ID for web results
            web_id = f"web_{uuid.uuid4().hex[:12]}"
            if web_id in seen_ids:
                continue
            seen_ids.add(web_id)

            opp = InternalOpportunity(
                id=web_id,
                title=title[:200],
                provider="Official source",
                country="",
                category="",
                degree="",
                funding_type="",
                deadline="Unknown",
                eligibility="",
                description=description[:500],
                official_url=url[:500],
                verified_url=url[:500],
                match_score=50.0,
                source_type="Live Web",
                source_dataset="Live Web",
                verification={"status": "Live Web", "confidence": "Medium", "source": url},
                live_deadline="Unknown",
            )
            results.append(opp)

        return results

    def _build_from_targets(self, targets: List[str], base: Dict, intent: Dict) -> List[tuple]:
        """Build search strategies from Groq-generated search targets."""
        strategies = []
        for target in targets:
            params = {**base}
            # If target has a country mention, try to extract it
            country = intent.get("entities", {}).get("country", intent.get("country"))
            if country and country.lower() not in target.lower():
                params["keywords"] = target
                params["countries"] = [country.lower()]
            else:
                params["keywords"] = target
            # Broaden categories based on target keywords
            target_lower = target.lower()
            if any(w in target_lower for w in ["phd", "doctoral", "doctorate"]):
                params["categories"] = params.get("categories", []) + ["research", "fellowship"]
            elif any(w in target_lower for w in ["master", "postgraduate"]):
                params["categories"] = params.get("categories", []) + ["scholarship", "fellowship"]
            elif any(w in target_lower for w in ["loan", "financing", "education loan"]):
                params["categories"] = params.get("categories", []) + ["loan"]
            elif any(w in target_lower for w in ["job", "career", "employment"]):
                params["categories"] = params.get("categories", []) + ["job", "internship"]
            elif any(w in target_lower for w in ["internship", "training"]):
                params["categories"] = params.get("categories", []) + ["internship"]
            elif any(w in target_lower for w in ["fellowship"]):
                params["categories"] = params.get("categories", []) + ["fellowship"]
            elif any(w in target_lower for w in ["grant", "funding"]):
                params["categories"] = params.get("categories", []) + ["grant", "scholarship"]
            elif any(w in target_lower for w in ["scholarship", "financial aid"]):
                params["categories"] = params.get("categories", []) + ["scholarship"]
            elif any(w in target_lower for w in ["competition", "hackathon"]):
                params["categories"] = params.get("categories", []) + ["competition"]
            elif any(w in target_lower for w in ["conference"]):
                params["categories"] = params.get("categories", []) + []
            elif any(w in target_lower for w in ["university", "college", "institute"]):
                params["categories"] = params.get("categories", []) + []
            elif any(w in target_lower for w in ["startup", "entrepreneur"]):
                params["categories"] = params.get("categories", []) + ["grant", "scheme"]
            elif any(w in target_lower for w in ["exchange"]):
                params["categories"] = params.get("categories", []) + ["exchange program"]
            else:
                params["categories"] = params.get("categories", [])
            # Remove duplicate categories
            params["categories"] = list(set(params["categories"]))
            strategies.append((f"groq_{target[:25]}", params))
        return strategies

    def _intent_to_params(self, intent: Dict) -> Dict[str, Any]:
        from .query_parser import query_parser
        return query_parser.to_search_params(intent)

    def _add_country_field(self, strategies: List[tuple], base: Dict, intent: Dict):
        country = (intent.get("country") or intent.get("entities", {}).get("country") or "").lower()
        field = intent.get("field") or intent.get("inferred_field") or intent.get("entities", {}).get("field")
        if country:
            strategies.append(("country", {**base, "keywords": f"{base.get('keywords', '')} {country}", "countries": [country]}))
        if field:
            for term in expand_field_terms(field):
                strategies.append((f"field_{term[:20]}", {**base, "keywords": f"{base.get('keywords', '')} {term}", "field": term}))
        if intent.get("entities", {}).get("funding") == "Fully Funded" or intent.get("fully_funded"):
            strategies.append(("fully_funded", {**base, "funding": ["fully funded", "full ride"]}))

    def _scholarship_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("scholarships", {**base, "categories": ["scholarship"]})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _university_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [
            ("universities", {**base, "keywords": f"university {base.get('keywords', '')}", "categories": []}),
            ("university_scholarships", {**base, "keywords": f"university scholarship {base.get('keywords', '')}", "categories": ["scholarship"]}),
        ]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _course_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("courses", {**base, "keywords": f"course program {base.get('keywords', '')}", "categories": []})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _career_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [
            ("career_jobs", {**base, "categories": ["job", "internship"]}),
            ("career_higher_studies", {**base, "keywords": "higher studies masters", "categories": []}),
            ("career_funding", {**base, "categories": ["scholarship", "fellowship"]}),
            ("career_research", {**base, "categories": ["research", "fellowship"]}),
        ]
        country = (intent.get("country") or "").lower()
        if not country or country in ("india", ""):
            strategies.append(("govt_exams", {**base, "keywords": "government exam", "categories": ["scheme"]}))
            strategies.append(("govt_loans", {**base, "keywords": "education loan", "categories": ["loan"]}))
        field = intent.get("field") or intent.get("inferred_field")
        if field:
            strategies.append((f"career_{field.lower()[:10]}", {**base, "keywords": f"{field} career opportunities"}))
        self._add_country_field(strategies, base, intent)
        return strategies

    def _job_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("jobs", {**base, "categories": ["job", "internship"]})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _internship_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("internships", {**base, "categories": ["internship"]})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _govt_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("govt_schemes", {**base, "keywords": "government scheme", "categories": ["scheme"]})]
        if intent.get("category"):
            strategies.append((f"govt_{intent['category'].lower()}", {**base, "keywords": f"{intent['category']} government scheme", "categories": ["scheme"]}))
        return strategies

    def _loan_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("loans", {**base, "keywords": "education loan", "categories": ["loan"]})]
        country = (intent.get("country") or "").lower()
        if country:
            strategies.append((f"loan_{country}", {**base, "keywords": f"education loan {country}", "categories": ["loan"]}))
        return strategies

    def _funding_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [
            ("funding_scholarships", {**base, "categories": ["scholarship", "fellowship"]}),
            ("funding_grants", {**base, "categories": ["grant"]}),
            ("funding_loans", {**base, "categories": ["loan"]}),
        ]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _admission_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("admissions", {**base, "keywords": f"admission {base.get('keywords', '')}", "categories": []})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _visa_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("visa", {**base, "keywords": f"visa {base.get('keywords', '')}", "categories": []})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _research_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("research", {**base, "categories": ["research", "fellowship"]})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _research_grant_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("research_grants", {**base, "categories": ["grant", "research"]})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _research_position_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("research_positions", {**base, "categories": ["research", "fellowship"]})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _phd_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [
            ("phd_positions", {**base, "keywords": f"phd position {base.get('keywords', '')}", "categories": ["research"]}),
            ("phd_fellowships", {**base, "keywords": f"phd fellowship {base.get('keywords', '')}", "categories": ["fellowship", "research"]}),
            ("phd_assistantships", {**base, "keywords": f"research assistantship phd {base.get('keywords', '')}", "categories": ["research"]}),
            ("funded_phd", {**base, "keywords": f"funded phd doctoral {base.get('keywords', '')}", "categories": ["research", "fellowship"]}),
        ]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _masters_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [
            ("masters_programs", {**base, "keywords": f"masters program {base.get('keywords', '')}", "categories": []}),
            ("masters_funding", {**base, "keywords": f"masters funding scholarship {base.get('keywords', '')}", "categories": ["scholarship", "fellowship"]}),
        ]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _bachelor_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [
            ("bachelor_programs", {**base, "keywords": f"bachelor program {base.get('keywords', '')}", "categories": []}),
            ("bachelor_funding", {**base, "keywords": f"bachelor scholarship funding {base.get('keywords', '')}", "categories": ["scholarship"]}),
        ]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _exchange_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("exchange", {**base, "categories": ["exchange program"]})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _fellowship_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("fellowships", {**base, "categories": ["fellowship"]})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _competition_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("competitions", {**base, "categories": ["competition"]})]
        return strategies

    def _startup_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("startups", {**base, "keywords": "startup funding grant", "categories": ["grant", "scheme"]})]
        return strategies

    def _conference_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("conferences", {**base, "keywords": f"conference {base.get('keywords', '')}"})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _journal_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("journals", {**base, "keywords": f"journal publication {base.get('keywords', '')}"})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _ranking_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("rankings", {**base, "keywords": "ranking top university", "categories": []})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _comparison_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("comparison", {**base, "categories": []})]
        return strategies

    def _eligibility_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("eligibility", {**base, "categories": []})]
        if intent.get("keywords"):
            strategies.append(("eligibility_target", {**base, "keywords": intent["keywords"], "categories": []}))
        return strategies

    def _grant_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("grants", {**base, "categories": ["grant"]})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _study_abroad_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [
            ("abroad_universities", {**base, "keywords": "universities abroad", "categories": []}),
            ("abroad_scholarships", {**base, "keywords": "study abroad scholarship", "categories": ["scholarship", "fellowship"]}),
            ("abroad_loans", {**base, "keywords": "education loan abroad", "categories": ["loan"]}),
            ("abroad_exchange", {**base, "keywords": "exchange program abroad", "categories": ["exchange program"]}),
            ("abroad_visa", {**base, "keywords": "student visa", "categories": []}),
            ("abroad_funding", {**base, "keywords": "study abroad funding", "categories": ["grant"]}),
        ]
        country = (intent.get("country") or "").lower()
        if country:
            for kw in ["universities", "scholarships", "loans", "visa"]:
                strategies.append((f"abroad_{country}_{kw}", {**base, "keywords": f"study {kw} {country}", "categories": []}))
        return strategies

    def _general_strategies(self, base: Dict, intent: Dict) -> List[tuple]:
        strategies = [("general", {**base, "categories": []})]
        self._add_country_field(strategies, base, intent)
        return strategies

    def _build_strategies(self, intent: Dict, base: Dict) -> List[tuple]:
        intent_type = intent.get("intent", intent.get("primary_intent", "Opportunity Search"))
        builder = self.INTENT_STRATEGIES.get(intent_type, self._general_strategies)
        return builder(self, base, intent)


multi_search = MultiSearch()
