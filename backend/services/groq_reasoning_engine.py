"""
Groq Reasoning Engine: Analyzes top opportunities and provides detailed explanations.
Generates personalized recommendations with eligibility, funding, and next steps.
"""

import os
import json
import re
from typing import Dict, List, Any, Optional
import httpx
from ..utils.logger import get_logger

logger = get_logger(__name__)

GROQ_BASE = "https://api.groq.com/openai/v1/chat/completions"


class GroqReasoningEngine:
    def _get_key(self):
        return os.getenv("GROQ_API_KEY")

    def _headers(self):
        key = self._get_key()
        if not key:
            return None
        return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    def _model(self):
        return "openai/gpt-oss-120b"

    def _format_candidates(self, opportunities, verified_map: Dict[str, Any]) -> str:
        lines = []
        for i, opp in enumerate(opportunities[:30], 1):
            title = opp.title or "Untitled"
            provider = opp.provider or "Unknown Provider"
            country = opp.country or "Unknown"
            category = opp.category or ""
            funding = opp.funding_type or ""
            deadline = opp.deadline or ""
            eligibility = (opp.eligibility or "")[:200]
            desc = (opp.description or "")[:200]
            score = round(opp.match_score or 0, 1)
            source = opp.source_type or "Dataset"

            verified = verified_map.get(opp.id, {})
            live_info = ""
            if verified:
                live_info = f" | Verified: {verified.get('status', '')} | Live deadline: {verified.get('deadline', 'N/A')} | Live eligibility: {(verified.get('eligibility') or '')[:100]}"

            lines.append(
                f"[{i}] {title} | {provider} | {country} | {category} | {funding} | "
                f"Deadline: {deadline} | Score: {score}/100 | Source: {source}{live_info}"
            )
            if eligibility:
                lines.append(f"    Eligibility: {eligibility}")
            if desc:
                lines.append(f"    Description: {desc}")
            lines.append("")
        return "\n".join(lines)

    async def reason(
        self,
        query: str,
        opportunities: List,
        verified_data: Optional[Dict[str, Any]] = None,
        user_profile: Optional[Dict] = None,
        intent_data: Optional[Dict] = None,
        route_plan: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        headers = self._headers()
        fallback = {
            "summary": "Analysis is temporarily unavailable. Verified opportunities are still available above.",
            "reasoning": [],
            "recommendations": [],
            "comparison": None,
            "roadmap": [],
            "action_checklist": [],
            "preparation_tips": {},
            "ai_available": False,
        }
        if not headers:
            return fallback

        from ..cache.memory import groq_cache, cache_get
        cache_key = f"reason_{query}"
        cached = cache_get(groq_cache, cache_key, "groq")
        if cached:
            cached["ai_available"] = True
            return cached

        verified_map = verified_data or {}
        candidates_str = self._format_candidates(opportunities, verified_map)

        profile_context = ""
        if user_profile:
            qual = user_profile.get("qualification") or user_profile.get("current_education") or "not specified"
            field = user_profile.get("field") or user_profile.get("stream") or "not specified"
            country = user_profile.get("country") or user_profile.get("target_country") or "not specified"
            profile_context = f"""
User Profile:
- Qualification: {qual}
- Field: {field}
- Country/Interest: {country}
"""

        # Structured intent context
        intent_context = ""
        if intent_data:
            pi = intent_data.get("primary_intent", "Unknown")
            ents = intent_data.get("entities", {})
            missing = intent_data.get("missing_fields", [])
            search_targets = intent_data.get("search_targets", [])
            intent_context = f"""
Detected Intent:
- Primary: {pi}
- Degree: {ents.get('degree', 'N/A')}
- Country: {ents.get('country', 'N/A')}
- Field: {ents.get('field', 'N/A')}
- Funding: {ents.get('funding', 'Not specified')}
- Search Targets: {', '.join(search_targets) if search_targets else 'N/A'}
- Missing info: {', '.join(missing) if missing else 'None'}
"""

        route_context = ""
        if route_plan:
            cats = route_plan.get("categories", [])
            route_context = f"""
Search Strategy:
- Searched categories: {', '.join(cats) if cats else 'All (no restriction)'}
- Query type: {intent_data.get('query_type', 'exploratory') if intent_data else 'Unknown'}
"""

        prompt = f"""You are FutureOS. You are NOT a chatbot. You are an AI decision engine that provides detailed, actionable guidance.

The user asked: "{query}"

Here are the opportunities with full details including eligibility, deadlines, and funding:
{candidates_str}

{intent_context}
{route_context}
{profile_context}

Your task — PROVIDE DETAILED EXPLANATIONS:

1. UNDERSTAND what the user wants:
   - PhD → funded PhD positions, research fellowships, doctoral programs
   - Loans → education loans, NOT scholarships
   - Career → jobs, higher studies, skill development paths
   - Internship → paid/unpaid internships, training programs

2. EXPLAIN EACH OPPORTUNITY IN DETAIL:
   - What it is (program type, level, field)
   - Who can apply (eligibility criteria, age limits if mentioned, qualifications required)
   - Funding details (fully funded / partial / self-funded, coverage details)
   - Application requirements (documents, tests, language requirements)
   - Deadlines (exact dates when available)
   - Fees (if mentioned in eligibility or description)
   - Next steps (how to apply, what to prepare)

3. BE SPECIFIC about requirements:
   - Don't say "eligible applicants" — say "BSc graduates with 60%+ marks"
   - Don't say "check eligibility" — explain the actual criteria
   - If age limit exists, mention it clearly
   - If fees are mentioned, state them
   - If documents are listed, name them

4. PRIORITIZE relevance:
   - Match the user's intent (PhD ≠ Bachelor's scholarship)
   - Exclude opportunities that don't fit
   - Rank by how well they match the query

5. TRUST official web pages when available:
   - If verified data shows different deadline/eligibility, use that
   - Mark opportunities as "Recently verified from official source"

6. If information is missing, say "Not specified" — never invent details.

Output valid JSON:
{{
  "summary": "A 3-4 sentence consultant-style answer that directly addresses the user's question. Start with the answer, then explain key opportunities with specific details about eligibility and funding.",
  "reasoning": [
    "Step 1: What the user asked for and why",
    "Step 2: What categories I searched",
    "Step 3: What I found and filtered",
    "Step 4: How I ranked them"
  ],
  "recommendations": [
    {{
      "title": "Full opportunity name",
      "provider": "Provider/University name",
      "country": "Country",
      "why": "2-3 sentence explanation of why this matches the user's profile and query",
      "fit": "Excellent fit | Good match | Possible option | Worth exploring",
      "match_score": <0-100>,
      "eligibility_details": "Specific requirements: degree type, marks/CGPA, age limit (if any), nationality, experience (if needed)",
      "funding_details": "Fully funded (tuition + stipend) | Partial funding (details) | Self-funded | Tuition waiver | Not specified",
      "application_requirements": "Documents needed, tests required (IELTS/TOEFL/GRE scores if mentioned), language requirements",
      "deadline": "Exact date or rolling or not specified",
      "fees": "Application fees or program fees if mentioned, otherwise 'Not specified'",
      "next_steps": "What to do next: prepare documents, check official site, apply by date, contact provider"
    }}
  ],
  "comparison": "If multiple strong options exist, compare them: funding differences, eligibility differences, application difficulty, deadlines. If only 1 option or not relevant, use null.",
  "roadmap": [
    "Step 1: Prepare required documents (list specific docs if known)",
    "Step 2: Check detailed eligibility on official website",
    "Step 3: Prepare for required tests (if applicable)",
    "Step 4: Submit application before deadline",
    "Step 5: Follow up and prepare for next stages"
  ],
  "action_checklist": [
    "Specific action 1 (e.g., 'Get transcripts certified')",
    "Specific action 2 (e.g., 'Book IELTS exam for target score 6.5+')",
    "Specific action 3 (e.g., 'Draft Statement of Purpose')"
  ],
  "preparation_tips": {{
    "Documents": ["tip 1", "tip 2"],
    "Application": ["tip 1", "tip 2"],
    "Tests": ["tip 1", "tip 2"]
  }}
}}

CRITICAL RULES:
- summary must answer the question directly with specific details
- recommendations must include detailed eligibility and funding information
- Never say "check official website" without providing what's known
- Be specific: "BSc with 60%+" not "qualified graduates"
- If age limit exists, mention it clearly
- Respond ONLY with valid JSON, no extra text.
"""

        payload = {
            "model": self._model(),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(GROQ_BASE, json=payload, headers=headers, timeout=45.0)
                if resp.status_code != 200:
                    logger.error(f"Groq reasoning failed: HTTP {resp.status_code}")
                    return fallback

                text = resp.json()["choices"][0]["message"]["content"]
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if not json_match:
                    logger.error("No JSON in Groq reasoning response")
                    return fallback

                result = json.loads(json_match.group(0))
                result["ai_available"] = True
                groq_cache[cache_key] = result
                return result

        except Exception as e:
            logger.error(f"Groq reasoning error: {e}")
            return fallback


groq_reasoning_engine = GroqReasoningEngine()
