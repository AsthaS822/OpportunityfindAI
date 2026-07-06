import os
import json
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
from ..utils.logger import get_logger

import httpx

logger = get_logger(__name__)

RETRYABLE_STATUS = {429, 500, 502, 503, 504}


class VerifiedExtractionSchema(BaseModel):
    deadline: Optional[str] = None
    ranking: Optional[str] = None
    status: Optional[str] = None
    eligibility: Optional[str] = None
    required_documents: Optional[str] = None
    application_process: Optional[str] = None
    selection_process: Optional[str] = None
    application_fees: Optional[str] = None
    stipend: Optional[str] = None
    tuition: Optional[str] = None
    living_allowance: Optional[str] = None
    travel_support: Optional[str] = None
    health_insurance: Optional[str] = None
    visa_support: Optional[str] = None
    minimum_cgpa: Optional[str] = None
    experience: Optional[str] = None
    ielts: Optional[str] = None
    toefl: Optional[str] = None
    gre: Optional[str] = None
    gmat: Optional[str] = None
    seats: Optional[str] = None
    application_link: Optional[str] = None
    required_qualification: Optional[str] = None


class RoadmapSchema(BaseModel):
    summary: str
    roadmap: List[str]
    action_checklist: Optional[List[str]] = None
    preparation_tips: Optional[Dict[str, List[str]]] = None


class GeminiService:
    def _get_url(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return None
        return f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    async def _post_with_retry(self, url: str, payload: dict, timeout: float = 25.0) -> tuple:
        last_status = 0
        for attempt in range(2):
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(url, json=payload, timeout=timeout)
                    last_status = resp.status_code
                    if resp.status_code == 200:
                        return resp, None
                    if resp.status_code not in RETRYABLE_STATUS:
                        return resp, f"HTTP {resp.status_code}"
            except httpx.TimeoutException:
                if attempt == 1:
                    return None, "timeout"
            except Exception as e:
                return None, str(e)
        return None, f"HTTP {last_status}" if last_status else "timeout"

    async def extract_details(self, text_content: str, title: str) -> Dict[str, Any]:
        """Extract verified fields from official page text only. Use Unknown/null if not found."""
        url = self._get_url()
        if not url:
            return {}

        prompt = (
            f"Extract ONLY information explicitly stated in the text for '{title}'. "
            "Do NOT invent or guess. If a field is not found, set it to null. "
            "Fields: deadline, ranking, status (active/closed/coming soon/unknown), "
            "eligibility, required_documents, application_process, selection_process, "
            "application_fees, stipend, tuition, living_allowance, travel_support, "
            "health_insurance, visa_support, minimum_cgpa, experience, ielts, toefl, "
            "gre, gmat, seats, application_link, required_qualification.\n\n"
            f"Text:\n{text_content[:10000]}"
        )

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": VerifiedExtractionSchema.model_json_schema(),
            },
        }

        resp, err = await self._post_with_retry(url, payload, 25.0)
        if err or not resp:
            logger.error(f"Gemini extraction failed: {err}")
            return {}

        try:
            data = resp.json()
            text_resp = data["candidates"][0]["content"]["parts"][0]["text"]
            result = json.loads(text_resp)
            for k, v in list(result.items()):
                if v is None or v == "":
                    result[k] = "Unknown"
            return result
        except Exception as e:
            logger.error(f"Gemini extraction parse error: {e}")
            return {}

    async def analyze_opportunities(
        self,
        opportunities: Union[List, List[Dict]],
        query: str,
        language: str = "en",
        verified_payload: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        url = self._get_url()
        fallback = {
            "summary": "AI explanation is temporarily unavailable. Verified opportunities are still available.",
            "roadmap": [],
            "action_checklist": [],
            "preparation_tips": {},
            "ai_available": False,
        }
        if not url:
            return {**fallback, "summary": "Gemini API key not configured. Verified opportunities are still available."}

        from ..cache.memory import gemini_cache, cache_get

        cache_key = f"analysis_{query}_{language}"
        cached = cache_get(gemini_cache, cache_key, "gemini")
        if cached:
            cached["ai_available"] = True
            return cached

        opp_data = verified_payload or []
        if not opp_data:
            for opp in opportunities:
                if isinstance(opp, dict):
                    opp_data.append({
                        "title": opp.get("title"),
                        "provider": opp.get("provider"),
                        "country": opp.get("country"),
                        "decision_analysis": opp.get("decision_analysis"),
                        "verification": opp.get("verification"),
                        "deadline": opp.get("deadline"),
                        "eligibility": opp.get("eligibility"),
                    })
                else:
                    opp_data.append({
                        "title": getattr(opp, "title", None),
                        "provider": getattr(opp, "provider", None),
                        "decision_analysis": getattr(opp, "decision_analysis", None),
                    })

        lang_instruction = (
            "Respond in plain, simple English."
            if language == "en"
            else "Respond in simple Hindi. NEVER translate University Names, Scholarship Names, Government Scheme Names, or Program Names — keep those in English."
        )

        prompt = f"""You are a career counselor explaining VERIFIED opportunities only.

STRICT RULES:
- Do NOT invent deadlines, rankings, universities, eligibility, stipend, funding, or links.
- Use ONLY the verified JSON data provided below.
- Explain why each opportunity fits or may not fit the user.
- Include preparation roadmap, timeline, application checklist, mistakes to avoid.
- Include tips for SOP, resume, LOR, visa, and interview IF relevant.
- If data says Unknown, say it is not verified yet.

User query: {query}
Verified opportunities JSON: {json.dumps(opp_data, default=str)}

{lang_instruction}
"""

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "responseSchema": RoadmapSchema.model_json_schema(),
            },
        }

        resp, err = await self._post_with_retry(url, payload, 35.0)
        if err or not resp:
            logger.error(f"Gemini analysis failed: {err}")
            return fallback

        try:
            data = resp.json()
            text_resp = data["candidates"][0]["content"]["parts"][0]["text"]
            res = json.loads(text_resp)
            res["ai_available"] = True
            gemini_cache[cache_key] = res
            return res
        except Exception as e:
            logger.error(f"Gemini analysis parse error: {e}")
            return fallback


gemini_service = GeminiService()
