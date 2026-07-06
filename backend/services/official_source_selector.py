from typing import List, Dict, Any, Tuple, Optional
from urllib.parse import urlparse
import re


class OfficialSourceSelector:
    # Preferred TLDs with proper patterns
    PREFERRED_TLDS = [
        (".gov", ".gov.in", ".gov.uk", ".gov.au", ".gov.ca"),  # Government
        (".edu", ".edu.in", ".edu.au"),  # Education
        (".ac.uk", ".ac.in", ".ac.nz", ".ac.za"),  # Academic
        (".org",),  # Organizations
    ]
    
    AVOID_DOMAINS = ["medium.com", "quora.com", "reddit.com", "blogspot", "wordpress.com", "coaching", "blog"]

    # Whitelist of known official domains — highest priority
    OFFICIAL_WHITELIST = [
        "daad.de", "erasmus-plus.ec.europa.eu", "fulbright.org",
        "britishcouncil.org", "aicte-india.org", "ugc.gov.in",
        "myscheme.gov.in", "education.gov.in", "europa.eu",
        "ec.europa.eu", "chevening.org", "commonwealthscholarships.org",
        "topuniversities.com", "timeshighereducation.com",
        "shanghairanking.com", "usnews.com", "coursera.org",
        "edx.org", "scholars4dev.com", "opportunitydesk.org",
        "fellowshipgator.com", "researchprofessional.com",
        "nature.com", "springer.com", "elsevier.com",
        "ieee.org", "acm.org",
    ]
    
    # Keywords that indicate relevance
    RELEVANCE_KEYWORDS = [
        "scholarship", "phd", "fellowship", "funding", "grant",
        "research", "admission", "application", "deadline",
        "eligibility", "apply", "program", "opportunity"
    ]

    def _score_result(self, result: Dict[str, Any]) -> Tuple[float, str]:
        """
        Score a search result based on source reliability and relevance.
        Returns (score, confidence_level)
        """
        url = result.get("url", "")
        title = result.get("title", "").lower()
        snippet = result.get("snippet", "").lower()
        domain = urlparse(url).netloc.lower()
        
        score = 0.0
        
        # Check for avoided domains first (automatic disqualification)
        if any(avoid in domain for avoid in self.AVOID_DOMAINS):
            return 0.0, "Low"
        
        # Score 1: Official whitelist (+100 points)
        is_official = False
        for official in self.OFFICIAL_WHITELIST:
            if official in domain:
                score += 100
                is_official = True
                break
        
        # Score 2: Preferred TLDs (+50 points, use endswith for true TLD checking)
        if not is_official:
            for tld_group in self.PREFERRED_TLDS:
                if any(domain.endswith(tld) for tld in tld_group):
                    score += 50
                    break
        
        # Score 3: Content relevance (+20 points for each keyword match)
        content = f"{title} {snippet}"
        keyword_matches = sum(1 for kw in self.RELEVANCE_KEYWORDS if kw in content)
        score += keyword_matches * 20
        
        # Score 4: URL path relevance (+10 points for relevant path)
        url_lower = url.lower()
        if any(kw in url_lower for kw in ["scholarship", "phd", "fellowship", "funding"]):
            score += 10
        
        # Score 5: Recency bonus (+5 if recent)
        # Could be enhanced with actual date checking
        if "2024" in content or "2025" in content or "2026" in content:
            score += 5
        
        # Determine confidence level based on score
        if score >= 100:
            confidence = "Very High"
        elif score >= 50:
            confidence = "High"
        elif score >= 20:
            confidence = "Medium"
        else:
            confidence = "Low"
        
        return score, confidence

    def select_best_url(self, jina_search_results: List[Dict[str, Any]]) -> Tuple[Optional[str], str]:
        """
        Select the best URL from search results using a scoring system.
        Returns (url, confidence_level)
        """
        if not jina_search_results:
            return None, "Low"
        
        # Score all results
        scored_results = []
        for result in jina_search_results:
            score, confidence = self._score_result(result)
            if score > 0:  # Only include non-avoided domains
                scored_results.append({
                    "url": result.get("url"),
                    "score": score,
                    "confidence": confidence,
                    "title": result.get("title", ""),
                })
        
        # If no results passed the filter, return first result with low confidence
        if not scored_results:
            return jina_search_results[0].get("url"), "Low"
        
        # Sort by score (highest first)
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        
        # Return the best result
        best = scored_results[0]
        return best["url"], best["confidence"]


official_source_selector = OfficialSourceSelector()
