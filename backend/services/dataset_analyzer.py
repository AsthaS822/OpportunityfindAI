"""
Dataset Analysis Engine - Intelligent dataset understanding and semantic search.
Analyzes dataset structure, creates knowledge graphs, and provides insights.
"""

from typing import List, Dict, Any, Set, Tuple, Optional
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from ..models.opportunity import InternalOpportunity
from .dataset_loader import dataset_loader
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DatasetAnalyzer:
    """
    Intelligent dataset analysis engine that:
    1. Understands dataset structure and content
    2. Creates semantic mappings and knowledge graphs
    3. Provides insights and statistics
    4. Enables smart query expansion
    """
    
    def __init__(self):
        self.knowledge_graph: Dict[str, Set[str]] = defaultdict(set)
        self.semantic_index: Dict[str, List[str]] = defaultdict(list)
        self.dataset_stats: Dict[str, Any] = {}
        self.indexed = False
    
    def analyze_and_index(self):
        """Analyze dataset and build knowledge graph + semantic index."""
        opportunities = dataset_loader.opportunities
        if not opportunities:
            logger.warning("No opportunities to analyze")
            return
        
        logger.info(f"Analyzing {len(opportunities)} opportunities...")
        
        # Build knowledge graph
        for opp in opportunities:
            # Country connections
            if opp.country:
                country = opp.country.lower()
                self.knowledge_graph[f"country:{country}"].add(opp.id)
                
                # Provider → Country
                if opp.provider:
                    self.knowledge_graph[f"provider:{opp.provider.lower()}"].add(f"country:{country}")
                
                # Category → Country
                if opp.category:
                    self.knowledge_graph[f"category:{opp.category.lower()}"].add(f"country:{country}")
            
            # Category connections
            if opp.category:
                category = opp.category.lower()
                self.knowledge_graph[f"category:{category}"].add(opp.id)
                
                # Funding → Category
                if opp.funding_type:
                    self.knowledge_graph[f"funding:{opp.funding_type.lower()}"].add(f"category:{category}")
            
            # Degree connections
            if opp.degree:
                degree = opp.degree.lower()
                self.knowledge_graph[f"degree:{degree}"].add(opp.id)
            
            # Provider connections
            if opp.provider:
                provider = opp.provider.lower()
                self.knowledge_graph[f"provider:{provider}"].add(opp.id)
            
            # Semantic indexing (text-based)
            searchable_text = f"{opp.title} {opp.description} {opp.eligibility}".lower()
            
            # Index by semantic tags
            if any(term in searchable_text for term in ["artificial intelligence", "ai", "machine learning", "ml"]):
                self.semantic_index["ai"].append(opp.id)
            if any(term in searchable_text for term in ["computer science", "cs", "computing", "software"]):
                self.semantic_index["computer_science"].append(opp.id)
            if any(term in searchable_text for term in ["data science", "data analytics", "big data"]):
                self.semantic_index["data_science"].append(opp.id)
            if any(term in searchable_text for term in ["engineering", "engineer"]):
                self.semantic_index["engineering"].append(opp.id)
            if any(term in searchable_text for term in ["business", "management", "mba"]):
                self.semantic_index["business"].append(opp.id)
            if any(term in searchable_text for term in ["research", "phd", "doctoral"]):
                self.semantic_index["research"].append(opp.id)
            if any(term in searchable_text for term in ["women", "female", "girl"]):
                self.semantic_index["women"].append(opp.id)
            if any(term in searchable_text for term in ["stem", "science", "technology"]):
                self.semantic_index["stem"].append(opp.id)
            if any(term in searchable_text for term in ["fully funded", "full funding", "tuition free"]):
                self.semantic_index["fully_funded"].append(opp.id)
            if any(term in searchable_text for term in ["undergraduate", "bachelor", "bsc", "btech", "ba"]):
                self.semantic_index["undergraduate"].append(opp.id)
            if any(term in searchable_text for term in ["postgraduate", "masters", "msc", "mtech", "ma", "mba"]):
                self.semantic_index["postgraduate"].append(opp.id)
        
        # Calculate statistics
        self._calculate_statistics()
        
        self.indexed = True
        logger.info(f"Dataset indexed: {len(self.knowledge_graph)} graph nodes, {len(self.semantic_index)} semantic tags")
    
    def _calculate_statistics(self):
        """Calculate dataset statistics for insights."""
        opportunities = dataset_loader.opportunities
        
        # Count by country
        country_counts = Counter()
        category_counts = Counter()
        provider_counts = Counter()
        funding_counts = Counter()
        
        for opp in opportunities:
            if opp.country:
                country_counts[opp.country] += 1
            if opp.category:
                category_counts[opp.category] += 1
            if opp.provider:
                provider_counts[opp.provider] += 1
            if opp.funding_type:
                funding_counts[opp.funding_type] += 1
        
        self.dataset_stats = {
            "total_opportunities": len(opportunities),
            "countries": dict(country_counts.most_common(20)),
            "categories": dict(category_counts.most_common(20)),
            "providers": dict(provider_counts.most_common(20)),
            "funding_types": dict(funding_counts.most_common(10)),
        }
    
    def smart_search_expansion(self, intent: Dict[str, Any]) -> Dict[str, Any]:
        """
        Expand search based on dataset intelligence.
        Returns enhanced search parameters with expanded categories and targets.
        """
        if not self.indexed:
            self.analyze_and_index()
        
        intent_type = intent.get("intent", "")
        country = (intent.get("country") or "").lower()
        field = (intent.get("field") or intent.get("inferred_field") or "").lower()
        degree = (intent.get("degree") or intent.get("qualification") or "").lower()
        
        expanded_categories = set(intent.get("categories", []) or [])
        search_targets = []
        relevant_providers = []
        
        # Career Advice expansion based on profile
        if intent_type == "Career Advice":
            # Based on degree, expand to relevant opportunity types
            if "bsc" in degree or "b.sc" in degree:
                expanded_categories.update(["scholarship", "fellowship", "research"])
                search_targets.extend([
                    f"MSc programs {field or 'Science'}",
                    f"Integrated PhD {field or 'Science'}",
                    f"Research fellowships {field or 'Science'}",
                    "Education loans for higher studies",
                ])
            elif "mca" in degree or "bca" in degree or "computer" in field:
                expanded_categories.update(["job", "internship", "scholarship", "fellowship"])
                search_targets.extend([
                    "Software Engineering jobs",
                    "Computer Science Masters scholarships",
                    "Tech internships",
                    "Data Science opportunities",
                ])
            elif "btech" in degree or "b.tech" in degree or "engineering" in field:
                expanded_categories.update(["job", "internship", "scholarship", "research"])
                search_targets.extend([
                    "Engineering jobs freshers",
                    "Masters Engineering scholarships",
                    "Research assistantship Engineering",
                    "Technical internships",
                ])
            elif "mba" in degree or "business" in field or "management" in field:
                expanded_categories.update(["job", "scholarship", "internship"])
                search_targets.extend([
                    "MBA programs",
                    "Management Consulting jobs",
                    "Business internships",
                    "Executive fellowships",
                ])
        
        # Country-based expansion
        if country:
            # Find providers associated with this country
            country_node = f"country:{country}"
            if country_node in self.knowledge_graph:
                # Find connected providers
                for node in self.knowledge_graph:
                    if node.startswith("provider:") and country_node in self.knowledge_graph[node]:
                        provider_name = node.replace("provider:", "")
                        relevant_providers.append(provider_name)
            
            # Country-specific expansions
            if country in ["germany", "deutschland"]:
                relevant_providers.extend(["daad", "deutschlandstipendium", "erasmus"])
                search_targets.append("DAAD scholarships")
            elif country in ["usa", "us", "united states"]:
                relevant_providers.extend(["fulbright", "usief"])
                search_targets.append("Fulbright scholarships")
            elif country in ["uk", "united kingdom"]:
                relevant_providers.extend(["chevening", "commonwealth"])
                search_targets.append("Chevening scholarships")
        
        # Field-based semantic expansion
        if "computer" in field or "software" in field or "ai" in field or "ml" in field:
            if "ai" in self.semantic_index:
                search_targets.append("AI research opportunities")
            if "computer_science" in self.semantic_index:
                search_targets.append("Computer Science scholarships")
        
        # Internship expansion
        if intent_type == "Internship":
            expanded_categories.add("internship")
            if country:
                search_targets.append(f"Internships {country} {field or 'tech'}")
            else:
                search_targets.append(f"Internships India {field or 'Engineering'}")
        
        # Job search expansion
        if intent_type == "Job Search":
            expanded_categories.update(["job", "internship"])
            if country:
                search_targets.append(f"Jobs {country} {field or degree}")
            else:
                search_targets.append(f"Jobs India {field or degree} freshers")
        
        # Scholarship expansion
        if intent_type == "Scholarship" or "scholarship" in expanded_categories:
            expanded_categories.add("scholarship")
            if intent.get("fully_funded"):
                search_targets.append("Fully funded scholarships")
        
        # PhD expansion
        if intent_type == "PhD" or "phd" in degree:
            expanded_categories.update(["research", "fellowship"])
            search_targets.extend([
                f"PhD positions {field or 'Research'}",
                f"Doctoral fellowships {country or 'Europe'}",
            ])
        
        # Masters expansion
        if intent_type == "Masters" or "masters" in degree or "msc" in degree:
            expanded_categories.update(["scholarship", "fellowship"])
            search_targets.extend([
                f"Masters scholarships {country or 'abroad'} {field or ''}",
                f"Postgraduate funding {field or ''}",
            ])
        
        return {
            "expanded_categories": list(expanded_categories),
            "search_targets": search_targets[:8],  # Limit to 8 targets
            "relevant_providers": relevant_providers[:5],
            "semantic_tags": self._get_relevant_semantic_tags(intent),
        }
    
    def _get_relevant_semantic_tags(self, intent: Dict) -> List[str]:
        """Get relevant semantic tags based on intent."""
        tags = []
        field = (intent.get("field") or intent.get("inferred_field") or "").lower()
        degree = (intent.get("degree") or "").lower()
        
        if "computer" in field or "software" in field:
            tags.extend(["ai", "computer_science", "data_science"])
        if "research" in field or "phd" in degree:
            tags.append("research")
        if "msc" in degree or "masters" in degree or "postgraduate" in degree:
            tags.append("postgraduate")
        if "bsc" in degree or "bachelor" in degree:
            tags.append("undergraduate")
        if intent.get("fully_funded"):
            tags.append("fully_funded")
        if intent.get("gender") == "Female":
            tags.append("women")
        
        return tags
    
    def get_insights(self, query: str) -> Dict[str, Any]:
        """Get dataset insights for analytical queries."""
        if not self.indexed:
            self.analyze_and_index()
        
        query_lower = query.lower()
        insights = {}
        
        # "Which country has the most..."
        if "which country" in query_lower or "most opportunities" in query_lower:
            insights["top_countries"] = list(self.dataset_stats.get("countries", {}).items())[:10]
        
        # "Most scholarships"
        if "most scholarship" in query_lower or "scholarships by country" in query_lower:
            scholarship_by_country = self._count_by_category_and_country("scholarship")
            insights["scholarships_by_country"] = scholarship_by_country[:10]
        
        # "Which provider"
        if "provider" in query_lower or "organization" in query_lower:
            insights["top_providers"] = list(self.dataset_stats.get("providers", {}).items())[:10]
        
        # "Deadlines this month"
        if "deadline" in query_lower:
            insights["upcoming_deadlines"] = self._get_upcoming_deadlines()
        
        # "AI opportunities"
        if "ai" in query_lower and "opportunities" in query_lower:
            insights["ai_opportunities_count"] = len(self.semantic_index.get("ai", []))
        
        # "Fully funded"
        if "fully funded" in query_lower:
            insights["fully_funded_count"] = len(self.semantic_index.get("fully_funded", []))
        
        return insights
    
    def _count_by_category_and_country(self, category: str) -> List[Tuple[str, int]]:
        """Count opportunities by category and country."""
        opportunities = dataset_loader.opportunities
        country_counts = Counter()
        
        for opp in opportunities:
            if opp.category and category in opp.category.lower():
                if opp.country:
                    country_counts[opp.country] += 1
        
        return country_counts.most_common(10)
    
    def _get_upcoming_deadlines(self, days: int = 60) -> List[Dict[str, str]]:
        """Get opportunities with deadlines in the next N days."""
        opportunities = dataset_loader.opportunities
        upcoming = []
        cutoff = datetime.now() + timedelta(days=days)
        
        for opp in opportunities:
            if opp.deadline and opp.deadline != "Unknown":
                try:
                    dl = datetime.strptime(opp.deadline.strip(), "%Y-%m-%d")
                    if datetime.now() <= dl <= cutoff:
                        upcoming.append({
                            "title": opp.title,
                            "deadline": opp.deadline,
                            "country": opp.country or "Global",
                            "category": opp.category or "Opportunity",
                        })
                except ValueError:
                    pass
        
        return sorted(upcoming, key=lambda x: x["deadline"])[:20]
    
    def filter_by_profile(self, opportunities: List[InternalOpportunity], profile: Dict) -> List[InternalOpportunity]:
        """Filter opportunities based on user profile (degree, field, budget)."""
        filtered = []
        
        degree = (profile.get("degree") or profile.get("qualification") or "").lower()
        field = (profile.get("field") or profile.get("inferred_field") or "").lower()
        budget = profile.get("budget", {}).get("amount", float("inf"))
        
        for opp in opportunities:
            opp_text = f"{opp.title} {opp.description} {opp.eligibility}".lower()
            
            # Relevance scoring
            relevance = 0
            
            # Degree match
            if degree and degree in opp_text:
                relevance += 20
            
            # Field match
            if field and field in opp_text:
                relevance += 20
            
            # Budget compatibility (if mentioned)
            if budget < 500000 and ("fully funded" in opp_text or "no cost" in opp_text):
                relevance += 15
            
            if relevance > 10:
                filtered.append(opp)
        
        return filtered


dataset_analyzer = DatasetAnalyzer()
