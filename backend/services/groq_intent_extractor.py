"""
GROQ INTENT EXTRACTOR — First Groq call.
Takes raw query → returns structured JSON: intent, entities, search targets, missing info.
"""

import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
import httpx
from ..utils.logger import get_logger

logger = get_logger(__name__)

GROQ_BASE = "https://api.groq.com/openai/v1/chat/completions"
FALLBACK_INTENT = {
    "primary_intent": "Opportunity Search",
    "secondary_intents": [],
    "entities": {},
    "search_targets": ["scholarships", "fellowships"],
    "needs_personalization": False,
    "missing_fields": [],
    "suggested_follow_up": [],
    "query_type": "exploratory",
}


class GroqIntentExtractor:
    def _get_key(self):
        return os.getenv("GROQ_API_KEY")

    def _headers(self):
        key = self._get_key()
        if not key:
            return None
        return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

    def _model(self):
        return "openai/gpt-oss-120b"

    async def extract(self, query: str) -> Dict[str, Any]:
        headers = self._headers()
        if not headers:
            logger.warning("No Groq key — using fallback intent extraction")
            return self._rule_based_fallback(query)

        prompt = f"""You are FutureOS, an AI decision engine that understands educational and career queries.

Extract structured intent from the user's query. Be precise — don't collapse different intents.

VALID PRIMARY INTENTS (pick exactly one):
- PhD Search: Query about PhD positions, funded PhDs, doctoral programs, doctorate
- Masters Search: Query about Masters programs, MS, M.Sc, M.Tech, postgraduate
- Bachelor Search: Query about Bachelors, undergraduate programs
- Scholarship Search: Query about scholarships, financial aid, funding for study
- Fellowship Search: Query about fellowships, research fellowships
- Grant Search: Query about grants, research funding
- Loan Search: Query about education loans, student loans, financing
- Internship Search: Query about internships, training programs
- Job Search: Query about jobs, employment, career opportunities after a degree
- Career Advice: Query about career paths, what to do after a degree, guidance
- Research Search: Query about research positions, research opportunities, postdoc
- Exchange Search: Query about exchange programs, student exchange
- Competition Search: Query about competitions, hackathons, contests
- Conference Search: Query about conferences, academic conferences, calls for papers
- Journal Search: Query about journals, publications
- Startup Search: Query about startups, entrepreneurship, incubators
- Government Scheme: Query about government schemes, central/state schemes
- Visa Search: Query about student visas, work visas, visa process
- Admission Search: Query about admissions, application process, how to apply
- Ranking Search: Query about university rankings, rankings comparison
- University Search: Query about universities, colleges, institutes
- Course Search: Query about courses, programs, certificates
- Eligibility Check: Query about eligibility, "can I get", "am I eligible", chances
- Comparison: Query comparing options, "vs", "which is better"
- Explain: Query asking "what is", "explain", "tell me about"
- Decision Help: Query asking "should I", "help me decide", confused
- Roadmap: Query asking "how to", "roadmap", "step by step"
- General Search: Anything else about opportunities

Output JSON with:
{{
  "primary_intent": "<ONE valid intent>",
  "secondary_intents": ["<related intents if any>"],
  "entities": {{
    "degree": "<detected degree or null>",
    "country": "<detected country or null>",
    "field": "<detected field of study or null>",
    "funding": "<Fully Funded | Partial | Not specified>",
    "provider": "<specific program name like DAAD, Erasmus or null>",
    "career_stage": "<student | graduate | professional | not specified>",
    "budget": "<budget mention or null>",
    "qualification": "<current qualification or null>",
    "cgpa": "<CGPA or null>",
    "target_degree": "<target degree or null>"
  }},
  "search_targets": ["<target1>", "<target2>", ...],
  "needs_personalization": true/false,
  "missing_fields": ["<field1>", "<field2>"],
  "suggested_follow_up": ["<question1>", "<question2>"],
  "query_type": "exploratory" or "personalized"
}}

CRITICAL RULES:
- exploratory = user just exploring options: "PhD in Europe", "Scholarships in Germany", "Jobs after MCA"
- personalized = user asking about themselves: "Can I get", "Best for me", "Am I eligible", "Suggest for me"
- For exploratory queries: search_targets should be broad and relevant
- For personalized queries: missing_fields should be minimal but critical
- search_targets MUST be specific searchable terms: ["phd positions europe", "funded phd programs", "doctoral scholarships europe"]
- For "PhD opportunities in Europe", search_targets should be: ["phd positions in europe", "funded phd programs", "doctoral scholarships", "phd fellowships"]
- For "education loans after BSc", search_targets should be: ["education loans", "student loans", "study loans"]
- NEVER include "scholarship" in search_targets if user asked for loans
- NEVER include "jobs" if user asked for PhD
- ALWAYS align search_targets with the user's actual intent

User query: {query}

Respond ONLY with valid JSON. No other text.
"""

        payload = {
            "model": self._model(),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
        }

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(GROQ_BASE, json=payload, headers=headers, timeout=20.0)
                if resp.status_code != 200:
                    logger.error(f"Groq intent extract failed: HTTP {resp.status_code}")
                    return self._rule_based_fallback(query)

                text = resp.json()["choices"][0]["message"]["content"]
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if not json_match:
                    logger.error("No JSON in Groq intent response")
                    return self._rule_based_fallback(query)

                result = json.loads(json_match.group(0))
                result["raw_query"] = query
                self._validate_and_fix(result)
                logger.info(f"Groq intent: {result.get('primary_intent')} | targets: {result.get('search_targets', [])} | type: {result.get('query_type')}")
                return result

        except Exception as e:
            logger.error(f"Groq intent extract error: {e}")
            return self._rule_based_fallback(query)

    def _validate_and_fix(self, result: Dict):
        if not result.get("primary_intent"):
            result["primary_intent"] = "Opportunity Search"
        if not result.get("search_targets"):
            result["search_targets"] = ["scholarships", "fellowships"]
        if not result.get("query_type"):
            result["query_type"] = "exploratory"
        if not result.get("entities"):
            result["entities"] = {}
        if result.get("needs_personalization") is None:
            result["needs_personalization"] = result.get("query_type") == "personalized"

    def _rule_based_fallback(self, query: str) -> Dict:
        q = query.lower()
        result = {**FALLBACK_INTENT, "raw_query": query, "entities": {}}

        has_phd = bool(re.search(r'\bphd\b', q)) or bool(re.search(r'\bph\.d\b', q)) or 'doctorate' in q
        has_masters = bool(re.search(r'\bmasters?\b', q)) or bool(re.search(r'\bpostgraduate\b', q))
        has_bachelor = bool(re.search(r'\bbachelors?\b', q)) or bool(re.search(r'\bundergraduate\b', q))
        has_scholarship = 'scholarship' in q
        has_loan = any(w in q for w in ['loan', 'education loan', 'student loan'])
        has_job = 'job' in q or 'jobs' in q or 'employment' in q
        has_internship = 'internship' in q or 'intern' in q
        has_fellowship = 'fellowship' in q
        has_grant = 'grant' in q
        has_research = 'research' in q
        has_visa = 'visa' in q
        has_admission = 'admission' in q
        has_ranking = 'ranking' in q
        has_university = any(w in q for w in ['university', 'universities', 'college'])
        has_career = any(w in q for w in ['career', 'scope', 'future']) and not has_scholarship and not has_loan and not has_fellowship and not has_phd and not has_research
        has_after_degree = bool(re.search(r'\b(after|pursuing|completed)\s+(mca|bca|b\.tech|m\.tech|bsc|msc|mba|ba|ma|bcom|mcom|bba|mbbs)\b', q)) and not has_scholarship and not has_loan and not has_fellowship and not has_phd and not has_research and not has_job
        has_competition = 'competition' in q or 'hackathon' in q
        has_startup = 'startup' in q or 'entrepreneur' in q
        has_exchange = 'exchange' in q
        has_conference = 'conference' in q
        has_compare = any(w in q for w in ['compare', 'vs ', 'versus', 'which is better'])
        has_eligibility = any(w in q for w in ['eligible', 'can i get', 'am i eligible', 'qualify', 'chance'])
        has_explain = any(w in q for w in ['what is', 'explain', 'tell me about'])
        has_decision = any(w in q for w in ['should i', 'help me decide', 'confused between'])
        has_roadmap = any(w in q for w in ['roadmap', 'how to', 'step by step'])

        def extract_country():
            countries = ["usa", "us", "uk", "germany", "canada", "australia", "france", "netherlands", "sweden", "switzerland", "singapore", "india", "japan", "china", "europe", "new zealand", "ireland", "dubai"]
            for c in sorted(countries, key=len, reverse=True):
                if re.search(r'\b' + re.escape(c) + r'\b', q):
                    return c.title()
            return None

        def extract_degree():
            degs = [("phd", "PhD"), ("ph.d", "PhD"), ("mca", "MCA"), ("bca", "BCA"), ("mba", "MBA"), ("b.tech", "B.Tech"), ("m.tech", "M.Tech"), ("bsc", "B.Sc"), ("msc", "M.Sc"), ("bcom", "B.Com"), ("mcom", "M.Com"), ("bba", "BBA"), ("ba", "B.A"), ("ma", "M.A"), ("mbbs", "MBBS"), ("bachelor", "Bachelor"), ("master", "Master")]
            for pattern, label in degs:
                if re.search(r'\b' + re.escape(pattern) + r'\b', q):
                    return label
            return None

        country = extract_country()
        degree = extract_degree()
        is_exploratory = not has_eligibility and not has_decision and not has_compare
        for pat in [r'\b(for|to)\s+me\b', r'\bmy\s+(profile|background|qualification)', r'\brecommend\s+(me|for me)']:
            if re.search(pat, q):
                is_exploratory = False
                break

        result["entities"] = {
            "degree": degree,
            "country": country,
            "field": None,
            "funding": "Not specified",
            "provider": None,
            "career_stage": "not specified",
        }

        # CONTENT INTENTS (checked first — specific what-user-wants)
        if has_phd:
            result["primary_intent"] = "PhD Search"
            region = f" in {country}" if country else ""
            result["search_targets"] = [f"phd positions{region}", f"funded phd programs{region}", f"doctoral scholarships{region}", f"phd fellowships{region}"]
        elif has_scholarship:
            result["primary_intent"] = "Scholarship Search"
            region = f" in {country}" if country else ""
            deg_tag = f" for {degree} graduates" if degree else ""
            result["search_targets"] = [f"scholarships{region}{deg_tag}", f"funded programs{region}", f"financial aid{region}", f"scholarships{region}"]
        elif has_loan:
            result["primary_intent"] = "Loan Search"
            result["search_targets"] = ["education loans", "student loans", "study loans", "education financing"]
        elif has_fellowship:
            result["primary_intent"] = "Fellowship Search"
            result["search_targets"] = ["fellowships", "research fellowships", "academic fellowships"]
        elif has_grant:
            result["primary_intent"] = "Grant Search"
            result["search_targets"] = ["grants", "research grants", "funding grants"]
        elif has_job:
            result["primary_intent"] = "Job Search"
            result["search_targets"] = [f"jobs after {degree}" if degree else "jobs", "career opportunities", "job listings"]
        elif has_internship:
            result["primary_intent"] = "Internship Search"
            result["search_targets"] = ["internships", "internship programs", "training programs"]
        elif has_research:
            result["primary_intent"] = "Research Search"
            result["search_targets"] = ["research positions", "research opportunities", "research programs"]
        elif has_masters:
            result["primary_intent"] = "Masters Search"
            region = f" in {country}" if country else ""
            result["search_targets"] = [f"masters programs{region}", f"masters scholarships{region}", f"postgraduate programs{region}"]
        elif has_bachelor:
            result["primary_intent"] = "Bachelor Search"
            result["search_targets"] = [f"bachelor programs", f"undergraduate scholarships", f"bachelor degrees"]
        # SCHEME / VISA / UNIVERSITY / ADMISSION / RANKING
        elif has_visa:
            result["primary_intent"] = "Visa Search"
            result["search_targets"] = ["student visa", "study visa", "visa requirements"]
        elif has_admission:
            result["primary_intent"] = "Admission Search"
            result["search_targets"] = ["admissions", "admission process", "how to apply"]
        elif has_ranking:
            result["primary_intent"] = "Ranking Search"
            result["search_targets"] = ["university rankings", "world rankings", "top universities"]
        elif has_university:
            result["primary_intent"] = "University Search"
            region = f" in {country}" if country else ""
            result["search_targets"] = [f"universities{region}", f"colleges{region}", f"institutes{region}"]
        # CAREER / AFTER-DEGREE
        elif has_career or has_after_degree:
            result["primary_intent"] = "Career Advice"
            deg_tag = degree.lower() if degree else "graduation"
            result["search_targets"] = [f"career after {deg_tag}", f"career opportunities after {deg_tag}", f"higher education after {deg_tag}"]
        # COMPETITION / STARTUP / EXCHANGE / CONFERENCE
        elif has_competition:
            result["primary_intent"] = "Competition Search"
            result["search_targets"] = ["competitions", "hackathons", "student competitions"]
        elif has_startup:
            result["primary_intent"] = "Startup Search"
            result["search_targets"] = ["startup funding", "entrepreneurship programs", "business grants"]
        elif has_exchange:
            result["primary_intent"] = "Exchange Search"
            result["search_targets"] = ["exchange programs", "student exchange", "study abroad exchange"]
        elif has_conference:
            result["primary_intent"] = "Conference Search"
            result["search_targets"] = ["academic conferences", "research conferences", "call for papers"]
        # META INTENTS (checked last — how-to, explain, compare, eligibility, decision)
        elif has_roadmap:
            result["primary_intent"] = "Roadmap"
            result["search_targets"] = []
        elif has_explain:
            result["primary_intent"] = "Explain"
            result["search_targets"] = []
        elif has_compare:
            result["primary_intent"] = "Comparison"
            result["search_targets"] = ["programs comparison", "opportunities comparison"]
        elif has_eligibility:
            result["primary_intent"] = "Eligibility Check"
            result["search_targets"] = ["scholarships", "fellowships", "programs"]
        elif has_decision:
            result["primary_intent"] = "Decision Help"
            result["search_targets"] = ["opportunities", "programs"]
        else:
            result["primary_intent"] = "General Search"
            aft_tag = f" after {degree}" if degree else ""
            result["search_targets"] = [f"opportunities{aft_tag}", "scholarships", "fellowships", "educational opportunities"]

        if country:
            result["entities"]["country"] = country
        if degree:
            result["entities"]["degree"] = degree

        result["query_type"] = "personalized" if not is_exploratory else "exploratory"
        result["needs_personalization"] = not is_exploratory
        if is_exploratory:
            result["missing_fields"] = []
            result["suggested_follow_up"] = []
        else:
            if not result["entities"].get("country"):
                result["missing_fields"] = ["country"]
                result["suggested_follow_up"] = ["Which country are you interested in?"]

        return result


groq_intent_extractor = GroqIntentExtractor()
