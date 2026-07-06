from fastapi import APIRouter, Request
import time
from ..limiter import limiter
from ..config import RATE_LIMIT
from ..schemas.request import DiscoverRequest
from ..schemas.response import DiscoverResponse
from ..services.master_decision_engine import master_decision_engine
from ..services.gemini_service import gemini_service
from ..services.response_builder import response_builder
from ..cache.memory import search_cache, session_history, cache_get
from ..utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/discover", response_model=DiscoverResponse)
@limiter.limit(RATE_LIMIT)
async def discover_opportunities(request: Request, body: DiscoverRequest):
    start_total = time.time()
    timings = {}
    session_id = body.session_id or "default"

    cache_key = f"{body.query.lower().strip()}_{body.language}_{session_id}"
    cached_response = cache_get(search_cache, cache_key, "search")
    session_history.add(body.query, session_id)

    if cached_response:
        logger.info(f"[CACHE HIT] {cache_key}")
        return cached_response

    try:
        start_engine = time.time()
        logger.info(f"[START] Discovery: {body.query} session={session_id}")

        discovery_result = await master_decision_engine.discover(
            query=body.query.strip(),
            language=body.language,
            session_id=session_id,
        )
        timings["engine"] = int((time.time() - start_engine) * 1000)

        if discovery_result.get("status") == "error":
            return response_builder.build_response(
                query=body.query,
                language=body.language,
                opportunities=[],
                gemini_analysis={"summary": discovery_result.get("message", "Unknown error"), "ai_available": False},
                thinking_steps=discovery_result.get("thinking_steps", ["Error occurred"]),
                timings=timings,
            )

        # Follow-up — no Gemini, no cache
        if discovery_result.get("follow_up_required"):
            timings["total"] = int((time.time() - start_total) * 1000)
            intent_type = discovery_result.get("user_intent", "")
            fq = discovery_result.get("follow_up_questions", [])
            qual = discovery_result.get("missing_information", [])
            summary = f"I'll help you find the best {intent_type.lower()} opportunities. To give you personalized recommendations, I need a few details."
            if fq:
                summary += f"\n\nPlease tell me:\n" + "\n".join(f"• {q}" for q in fq)
            return response_builder.build_response(
                query=body.query,
                language=body.language,
                opportunities=[],
                gemini_analysis={"summary": summary, "roadmap": []},
                thinking_steps=["Analyzing your request..."],
                timings=timings,
                additional_data={
                    "intent": intent_type,
                    "missing_info": qual,
                    "follow_up_questions": fq,
                    "follow_up_required": True,
                    "summary": summary,
                },
            )

        gemini_analysis = {"summary": discovery_result.get("summary", ""), "roadmap": [], "ai_available": True}

        if discovery_result.get("opportunities"):
            start_gemini = time.time()
            user_profile = discovery_result.get("user_profile", {})
            gemini_analysis = await gemini_service.analyze_opportunities(
                opportunities=discovery_result["opportunities"][:5],
                query=body.query,
                language=body.language,
                verified_payload=discovery_result["opportunities"][:5],
                user_profile=user_profile,
            )
            timings["gemini"] = int((time.time() - start_gemini) * 1000)
        elif not discovery_result.get("opportunities"):
            gemini_analysis = {
                "summary": discovery_result.get("summary", "No verified opportunities found."),
                "roadmap": [],
                "ai_available": True,
            }

        timings["total"] = int((time.time() - start_total) * 1000)

        final_response = response_builder.build_response(
            query=body.query,
            language=body.language,
            opportunities=discovery_result.get("opportunities", []),
            gemini_analysis=gemini_analysis,
            thinking_steps=discovery_result.get("thinking_steps", []),
            timings=timings,
            additional_data={
                "intent": discovery_result.get("user_intent"),
                "missing_info": discovery_result.get("missing_information"),
                "total_found": discovery_result.get("total_found"),
                "verified_count": discovery_result.get("verified_count"),
                "summary": discovery_result.get("summary"),
                "alternatives": discovery_result.get("alternatives", []),
                "follow_up_required": False,
            },
        )

        # Cache only successful responses with opportunities
        if discovery_result.get("opportunities") and gemini_analysis.get("ai_available", True):
            search_cache[cache_key] = final_response
            logger.info(f"[CACHE SET] {cache_key}")

        logger.info(f"[COMPLETE] {timings['total']}ms engine={timings.get('engine')} gemini={timings.get('gemini', 0)}")
        return final_response

    except Exception as e:
        logger.error(f"[ERROR] Discovery failed: {e}", exc_info=True)
        timings["total"] = int((time.time() - start_total) * 1000)
        return response_builder.build_response(
            query=body.query,
            language=body.language,
            opportunities=[],
            gemini_analysis={"summary": "Could not complete search. Please try again.", "ai_available": False},
            thinking_steps=["Searching datasets...", "Error occurred during processing"],
            timings=timings,
        )
