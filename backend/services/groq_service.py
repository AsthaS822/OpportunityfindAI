import os
import json
import re
from pydantic import BaseModel
from typing import List, Dict, Any, Optional, Union
from ..utils.logger import get_logger

import httpx

logger = get_logger(__name__)

GROQ_BASE = "https://api.groq.com/openai/v1/chat/completions"
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


class GroqService:
    def _get_key(self):
        return os.getenv("GROQ_API_KEY")

    def _headers(self):
        key = self._get_key()
        if not key:
            return None
        return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    def _model(self):
        return "openai/gpt-oss-120b"

    async def _post_with_retry(self, headers: dict, payload: dict, timeout: float = 25.0) -> tuple:
        last_status = 0
        for attempt in range(2):
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.post(GROQ_BASE, json=payload, headers=headers, timeout=timeout)
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

    def _parse_content(self, resp) -> Optional[str]:
        try:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json_match.group(0)
            return content.strip()
        except Exception as e:
            logger.error(f"Groq parse error: {e}")
            return None

    async def extract_details(self, text_content: str, title: str) -> Dict[str, Any]:
        headers = self._headers()
        if not headers:
            return {}

        prompt = (
            f"Extract ONLY information explicitly stated in the text for '{title}'. "
            "Do NOT invent or guess. If a field is not found, set it to null. "
            "Fields: deadline, ranking, status (active/closed/coming soon/unknown), "
            "eligibility, required_documents, application_process, selection_process, "
            "application_fees, stipend, tuition, living_allowance, travel_support, "
            "health_insurance, visa_support, minimum_cgpa, experience, ielts, toefl, "
            "gre, gmat, seats, application_link, required_qualification.\n\n"
            "Respond in JSON format only.\n\n"
            f"Text:\n{text_content[:10000]}"
        )

        payload = {
            "model": self._model(),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
        }

        resp, err = await self._post_with_retry(headers, payload, 25.0)
        if err or not resp:
            logger.error(f"Groq extraction failed: {err}")
            return {}

        text = self._parse_content(resp)
        if not text:
            return {}

        try:
            result = json.loads(text)
            for k, v in list(result.items()):
                if v is None or v == "":
                    result[k] = "Unknown"
            return result
        except Exception as e:
            logger.error(f"Groq extraction JSON parse error: {e}")
            return {}

    async def analyze_opportunities(
        self,
        opportunities: Union[List, List[Dict]],
        query: str,
        verified_payload: Optional[List[Dict]] = None,
        user_profile: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        headers = self._headers()
        fallback = {
            "summary": "AI explanation is temporarily unavailable. Verified opportunities are still available.",
            "roadmap": [],
            "action_checklist": [],
            "preparation_tips": {},
            "ai_available": False,
        }
        if not headers:
            msg = "Groq API key not configured. Verified opportunities are still available."
            return {**fallback, "summary": msg}

        from ..cache.memory import groq_cache, cache_get

        cache_key = f"analysis_{query}"
        cached = cache_get(groq_cache, cache_key, "groq")
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

        profile_context = ""
        if user_profile:
            qual = user_profile.get("qualification") or "not specified"
            field = user_profile.get("field") or "not specified"
            country = user_profile.get("country") or "not specified"
            career_paths = user_profile.get("career_paths", [])
            profile_context = f"""
User Profile:
- Qualification: {qual}
- Field/Domain: {field}
- Country: {country}
{f"- Career paths: {', '.join(career_paths)}" if career_paths else ""}
"""

        prompt = f"""You are FutureOS — a senior career and education consultant. You help users make informed decisions by analyzing opportunities against their profile. You never search the internet — you only analyze provided data.

===========================
RULES
===========================
1. NEVER invent deadlines, rankings, university names, eligibility criteria, funding amounts, or links. Use ONLY the verified data provided.
2. If data for a field says "Unknown", simply skip it — never say "unknown", "not available", or "not verified".
3. NEVER use these words: "dataset", "dataset only", "low confidence", "unknown provider", "confidence score", "moderate match", "unverified".
4. Instead use natural labels: "Excellent fit", "Good match", "Possible match", "Recommended", "Strong option", "Worth exploring".
5. Only recommend opportunities genuinely relevant to the user's qualification and field. If irrelevant, say it may not be a strong fit.
6. Explain WHY each opportunity fits — reason from the user's qualification, field, and country.
7. Be conversational and consultant-like. End with suggested follow-up actions.
8. Never recommend unavailable programs or opportunities not in the provided data.

===========================
STRUCTURE YOUR RESPONSE
===========================
Your response must be valid JSON with these fields:

1. "summary" (string) — A detailed, consultant-style overview:
   - Start with: "Based on your profile as [qualification] in [field], here's what I found."
   - Explain the top 1-2 opportunities and WHY they fit
   - Note what's missing if applicable (e.g., CGPA, IELTS)
   - End with a clear recommendation

2. "roadmap" (list of strings) — 4-5 step action plan in order:
   - Step 1: Check eligibility requirements
   - Step 2: Prepare required documents
   - Step 3: Take required exams (IELTS, GRE, etc.)
   - Step 4: Submit application before deadline
   - Step 5: Prepare for interview/selection process

3. "action_checklist" (list of strings) — Concrete tasks:
   - "Review eligibility criteria for [opportunity name]"
   - "Prepare statement of purpose"
   - "Gather academic transcripts"
   - "Take English proficiency test"
   - etc.

4. "preparation_tips" (object) — Category→list of tips:
   - "documents": ["tip 1", "tip 2"]
   - "exams": ["tip 1", "tip 2"]
   - "application": ["tip 1", "tip 2"]
   - "interview": ["tip 1", "tip 2"]

{profile_context}
User query: {query}
Verified opportunities JSON: {json.dumps(opp_data, default=str)}

Respond in plain, simple English.

Respond ONLY with valid JSON. No other text. JSON fields: summary (string), roadmap (list of strings), action_checklist (list of strings), preparation_tips (object with category keys and list-of-strings values).
"""

        payload = {
            "model": self._model(),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }

        resp, err = await self._post_with_retry(headers, payload, 35.0)
        if err or not resp:
            logger.error(f"Groq analysis failed: {err}")
            return fallback

        text = self._parse_content(resp)
        if not text:
            return fallback

        try:
            res = json.loads(text)
            res["ai_available"] = True
            groq_cache[cache_key] = res
            return res
        except Exception as e:
            logger.error(f"Groq analysis parse error: {e}")
            return fallback


groq_service = GroqService()
