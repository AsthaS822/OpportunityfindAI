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


class GeminiService:
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
        language: str = "en",
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
            return {**fallback, "summary": "Groq API key not configured. Verified opportunities are still available."}

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

        prompt = f"""You are the OpportunityOS AI Opportunity Advisor — an experienced career counselor, education consultant, scholarship advisor, visa advisor, research mentor, and government scheme expert combined.

===========================
PRIMARY OBJECTIVE
===========================
Help users make the best decision, not simply retrieve information. Every response should help the user understand what opportunities exist, whether they qualify, why they qualify, what to do next, and what alternatives exist. NEVER dump raw search results — synthesize them.

===========================
RULES
===========================
1. Do NOT invent deadlines, rankings, universities, eligibility, stipend, funding, or links. Use ONLY the verified data provided.
2. ONLY recommend opportunities genuinely relevant to the user's qualification and field. If an opportunity is clearly irrelevant, say it may not be a strong fit and move on.
3. Explain why each opportunity fits the user's profile (qualification, field, country). Reason from the user's background.
4. If CGPA or IELTS is mentioned, give specific advice. If the user has an MCA, infer Computer Science background. If BCom, recommend commerce-appropriate paths.
5. Include a personalized preparation roadmap with timeline.
6. Include an application checklist (documents, exams, steps).
7. Compare multiple opportunities if available (pros/cons). Use a comparison format.
8. Suggest alternative paths if the user might not qualify.
9. If data has Unknown values, simply skip them — never say "not verified yet" or "unknown".
10. Never use the words "dataset", "dataset only", "low confidence", "unknown provider", "moderate match", "confidence score".
11. Use natural labels: "Good match", "Excellent fit", "Recommended", "Possible match".
12. Be conversational. End every answer with suggested follow-up questions like "Compare opportunities", "Show deadlines", "Explain eligibility", "Estimate my chances", "Application checklist".
13. If the user asks about opportunities after a degree, first outline career paths, study abroad options, then scholarships — not the reverse.

{profile_context}
User query: {query}
Verified opportunities JSON: {json.dumps(opp_data, default=str)}

{lang_instruction}

Respond ONLY with valid JSON. Do not include any other text. JSON fields: summary (string — detailed personalized assessment), roadmap (list of strings — step by step application plan), action_checklist (list of strings — documents and tasks), preparation_tips (object with category as key and list of tips as value).
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
            gemini_cache[cache_key] = res
            return res
        except Exception as e:
            logger.error(f"Groq analysis parse error: {e}")
            return fallback


gemini_service = GeminiService()
