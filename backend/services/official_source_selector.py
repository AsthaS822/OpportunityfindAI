from typing import List, Dict, Any, Tuple, Optional
from urllib.parse import urlparse

class OfficialSourceSelector:
    PREFERRED_TLDS = [".gov", ".edu", ".ac.", ".org"]
    AVOID_DOMAINS = ["medium.com", "quora.com", "reddit.com", "blogspot", "wordpress.com", "coaching", "blog"]

    def select_best_url(self, jina_search_results: List[Dict[str, Any]]) -> Tuple[Optional[str], str]:
        if not jina_search_results:
            return None, "Low"
            
        # Try to find a highly preferred domain first (High Confidence)
        for result in jina_search_results:
            url = result.get("url", "")
            domain = urlparse(url).netloc.lower()
            
            if any(tld in domain for tld in self.PREFERRED_TLDS) and not any(avoid in domain for avoid in self.AVOID_DOMAINS):
                return url, "High"

        # Try to find medium confidence (not preferred, but not strictly avoided)
        for result in jina_search_results:
            url = result.get("url", "")
            domain = urlparse(url).netloc.lower()
            if not any(avoid in domain for avoid in self.AVOID_DOMAINS):
                return url, "Medium"
                
        # If all else fails, return the top result as Low confidence
        return jina_search_results[0].get("url"), "Low"

official_source_selector = OfficialSourceSelector()
