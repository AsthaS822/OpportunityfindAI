import httpx
import os
from typing import List, Dict, Any
from ..utils.logger import get_logger

logger = get_logger(__name__)

class JinaSearch:
    def __init__(self):
        self.base_url = "https://s.jina.ai/"

    async def search(self, query: str) -> List[Dict[str, Any]]:
        api_key = os.getenv("JINA_API_KEY")
        if not api_key:
            logger.warning("JINA_API_KEY is not set. Skipping live search.")
            return []
            
        from ..cache.memory import jina_cache, cache_get
        cached = cache_get(jina_cache, f"search_{query}", "jina")
        if cached is not None:
            return cached

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{query}",
                    headers=headers,
                    timeout=10.0
                )
                if response.status_code == 200:
                    data = response.json()
                    res = data.get("data", [])
                    jina_cache[f"search_{query}"] = res
                    return res
                else:
                    logger.error(f"Jina Search API error: {response.status_code}")
                    return []  # Do not cache failures
        except Exception as e:
            logger.error(f"Error calling Jina Search: {str(e)}")
            return []  # Do not cache failures

jina_search = JinaSearch()
