from fastapi import APIRouter, Request
import time
from ..limiter import limiter
from ..config import RATE_LIMIT
from ..schemas.request import DiscoverRequest
from ..schemas.response import DiscoverResponse
from ..services.master_decision_engine import master_decision_engine
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

    session_history.add(body.query, session_id)

    try:
        start_engine = time.time()
        logger.info(f"[START] Discovery: {body.query} session={session_id}")

        discovery_result = await master_decision_engine.discover(
            query=body.query.strip(),
            session_id=session_id,
        )
        timings["engine"] = int((time.time() - start_engine) * 1000)

        if discovery_result.get("status") == "error":
            return response_builder.build_response(
                query=body.query,
                opportunities=[],
                ai_analysis={"summary": discovery_result.get("message", "Unknown error"), "ai_available": False},
                thinking_steps=discovery_result.get("thinking_steps", ["Error occurred"]),
                timings=timings,
            )

        # Follow-up — no cache
        if discovery_result.get("follow_up_required"):
            timings["total"] = int((time.time() - start_total) * 1000)
            intent_type = discovery_result.get("user_intent", "")
            fq = discovery_result.get("follow_up_questions", [])
            qual = discovery_result.get("missing_information", [])
            career_paths = discovery_result.get("career_paths", [])
            if career_paths:
                summary = "I'd like to understand your goals better. Which direction interests you?"
            elif fq:
                base = f"I'll help you find the best {intent_type.lower()} opportunities. To give you personalized recommendations, I need a few details."
                summary = base + "\n\n" + "\n".join(f"• {q}" for q in fq)
            else:
                summary = f"I'll help you find the best {intent_type.lower()} opportunities."
            return response_builder.build_response(
                query=body.query,
                opportunities=[],
                ai_analysis={"summary": summary, "roadmap": []},
                thinking_steps=["Analyzing your request..."],
                timings=timings,
                additional_data={
                    "intent": intent_type,
                    "missing_info": qual,
                    "follow_up_questions": fq,
                    "follow_up_required": True,
                    "summary": summary,
                    "career_paths": career_paths,
                },
            )

        # Use Groq reasoning from engine — no second Groq call
        groq_reasoning = discovery_result.get("groq_reasoning", {})
        ai_analysis = {
            "summary": discovery_result.get("summary", ""),
            "roadmap": groq_reasoning.get("roadmap", []),
            "action_checklist": groq_reasoning.get("action_checklist", []),
            "preparation_tips": groq_reasoning.get("preparation_tips", {}),
            "ai_available": groq_reasoning.get("ai_available", True),
            "reasoning": groq_reasoning.get("reasoning", []),
            "recommendations": groq_reasoning.get("recommendations", []),
            "comparison": groq_reasoning.get("comparison"),
        }

        if not discovery_result.get("opportunities"):
            ai_analysis["summary"] = discovery_result.get("summary", "No verified opportunities found.")

        timings["total"] = int((time.time() - start_total) * 1000)

        final_response = response_builder.build_response(
            query=body.query,
            opportunities=discovery_result.get("opportunities", []),
            ai_analysis=ai_analysis,
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

        # Cache with intent-aware key
        intent_key = discovery_result.get("user_intent", "unknown")
        cache_key = f"{body.query.lower().strip()}|{intent_key}|{session_id}"
        if discovery_result.get("opportunities") and ai_analysis.get("ai_available", True):
            search_cache[cache_key] = final_response
            logger.info(f"[CACHE SET] {cache_key}")

        logger.info(f"[COMPLETE] {timings['total']}ms engine={timings.get('engine')} intent={intent_key}")
        return final_response

    except Exception as e:
        logger.error(f"[ERROR] Discovery failed: {e}", exc_info=True)
        timings["total"] = int((time.time() - start_total) * 1000)
        return response_builder.build_response(
            query=body.query,
            opportunities=[],
            ai_analysis={"summary": "Could not complete search. Please try again.", "ai_available": False},
            thinking_steps=["Searching datasets...", "Error occurred during processing"],
            timings=timings,
        )
