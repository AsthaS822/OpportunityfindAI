from fastapi import APIRouter, Request
import time
import os
import httpx
import psutil
import platform
from ..services.dataset_loader import dataset_loader
from ..config import BACKEND_VERSION
from ..cache.memory import get_cache_stats, search_cache, jina_cache, groq_cache

router = APIRouter()


async def _probe_groq() -> str:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        return "missing"
    try:
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {"model": "openai/gpt-oss-120b", "messages": [{"role": "user", "content": "ping"}]}
        async with httpx.AsyncClient() as client:
            resp = await client.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=5.0)
            if resp.status_code == 200:
                return "available"
            if resp.status_code == 429:
                return "rate_limited"
            return f"error_{resp.status_code}"
    except Exception:
        return "unavailable"


async def _probe_jina() -> str:
    key = os.getenv("JINA_API_KEY")
    if not key:
        return "missing"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://s.jina.ai/test",
                headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
                timeout=5.0,
            )
            return "available" if resp.status_code in (200, 422) else f"error_{resp.status_code}"
    except Exception:
        return "unavailable"


@router.get("/health")
async def health_check(request: Request):
    uptime_seconds = int(time.time() - request.app.state.start_time) if hasattr(request.app.state, "start_time") else 0
    process = psutil.Process(os.getpid())
    memory_mb = process.memory_info().rss / (1024 * 1024)
    cache_stats = get_cache_stats()

    groq_status = await _probe_groq()
    jina_status = await _probe_jina()

    return {
        "status": "healthy",
        "datasets_loaded": dataset_loader.stats["files_loaded"],
        "records_loaded": len(dataset_loader.opportunities),
        "memory_usage": f"{round(memory_mb, 2)} MB",
        "python_version": platform.python_version(),
        "backend_version": BACKEND_VERSION,
        "uptime": f"{uptime_seconds}s",
        "cache_status": cache_stats,
        "cache_sizes": {
            "search": len(search_cache),
            "jina": len(jina_cache),
            "groq": len(groq_cache),
        },
        "groq_status": groq_status,
        "jina_status": jina_status,
    }
