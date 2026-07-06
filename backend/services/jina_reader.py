import httpx
import os
from ..utils.logger import get_logger

logger = get_logger(__name__)

class JinaReader:
    def __init__(self):
        self.base_url = "https://r.jina.ai/"

    async def read(self, url: str) -> str:
        api_key = os.getenv("JINA_API_KEY")
        if not api_key:
            logger.warning("JINA_API_KEY is not set. Skipping live read.")
            return ""

        from ..cache.memory import jina_cache, cache_get
        cached = cache_get(jina_cache, f"read_{url}", "jina")
        if cached is not None:
            return cached
            
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}{url}",
                    headers=headers,
                    timeout=15.0
                )
                if response.status_code == 200:
                    jina_cache[f"read_{url}"] = response.text
                    return response.text
                else:
                    logger.error(f"Jina Reader API error: {response.status_code}")
                    return ""
        except Exception as e:
            logger.error(f"Error calling Jina Reader for {url}: {str(e)}")
            return ""

jina_reader = JinaReader()
