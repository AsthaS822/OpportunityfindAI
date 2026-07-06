"""
Smart Query Parser — intent detection, entity extraction, exploratory vs personalized.
"""

import re
from typing import Dict, List, Any, Optional
from .synonyms import normalize_term, FIELD_SYNONYMS, DEGREE_SYNONYMS, COUNTRY_SYNONYMS
from ..utils.logger import get_logger

logger = get_logger(__name__)

DEGREE_FIELD_MAP = {
    "mca": "Computer Science", "bca": "Information Technology",
    "b.tech": "Engineering", "b.e": "Engineering", "m.tech": "Engineering",
    "b.sc": "Science", "m.sc": "Science",
    "bsc": "Science", "msc": "Science",
    "b.com": "Commerce", "m.com": "Commerce",
    "bcom": "Commerce", "mcom": "Commerce",
    "bba": "Business Administration", "mba": "Business Administration",
    "ba": "Arts", "ma": "Arts",
    "mbbs": "Medicine", "bds": "Dentistry",
    "llb": "Law", "llm": "Law",
    "phd": "Research", "ph.d": "Research",
}

DEGREE_CAREER_PATHS = {
    "mca": [
        "Software Engineering", "Full Stack Development", "Cloud Engineering",
        "DevOps", "Data Science", "AI/ML Engineering", "Cyber Security",
        "Database Administration", "System Architecture", "IT Consulting",
        "Government IT Officer", "Research Associate",
    ],
    "bca": [
        "MCA", "Software Development", "Web Development", "Cloud Computing",
        "Cyber Security", "Data Analytics", "IT Support", "Digital Marketing",
    ],
    "b.tech": ["Engineering Roles", "R&D", "Product Development", "Consulting", "Government Engineering"],
    "bsc": ["Research", "MSc", "PhD", "Lab Technician", "Data Analysis", "Science Communication"],
    "b.com": ["Accounting", "Finance", "Banking", "CA", "CFA", "Business Analytics", "Government Finance"],
    "mba": ["Management Consulting", "Product Management", "Finance", "Marketing", "Operations", "Strategy"],
}

DEGREE_ABROAD_FIELDS = {
    "mca": "Computer Science, Data Science, AI, Information Systems",
    "bca": "Computer Science, Information Technology, Data Science",
    "b.tech": "Engineering, Computer Science, Robotics, Renewable Energy",
    "bsc": "Physics, Chemistry, Biology, Environmental Science, Data Science",
    "b.com": "Finance, Business Analytics, International Business, Economics",
    "mba": "MBA, International Business, Finance, Marketing, Entrepreneurship",
}


class QueryParser:
    COUNTRIES = [
        "united states", "usa", "us", "uk", "united kingdom", "germany", "canada",
        "australia", "india", "japan", "france", "netherlands", "sweden",
        "switzerland", "singapore", "ireland", "austria", "belgium", "finland",
        "europe", "new zealand", "south korea", "china", "uae", "dubai",
    ]

    COUNTRY_CANONICAL = {
        "us": "United States", "usa": "United States", "united states": "United States",
        "uk": "United Kingdom", "united kingdom": "United Kingdom",
        "germany": "Germany", "deutschland": "Germany",
        "canada": "Canada", "australia": "Australia", "india": "India",
        "japan": "Japan", "france": "France", "netherlands": "Netherlands",
        "sweden": "Sweden", "switzerland": "Switzerland", "singapore": "Singapore",
        "ireland": "Ireland", "austria": "Austria", "belgium": "Belgium",
        "finland": "Finland", "europe": "Europe", "new zealand": "New Zealand",
        "south korea": "South Korea", "china": "China", "uae": "UAE", "dubai": "UAE",
    }

    DEGREES = list(DEGREE_SYNONYMS.keys()) + ["bachelor", "bachelors", "master", "masters", "phd", "mba", "mca", "diploma"]

    CATEGORIES = [
        "scholarship", "loan", "scheme", "internship", "fellowship", "grant",
        "competition", "research", "exchange program", "exchange", "volunteer", "job", "startup",
    ]

    CASTE_CATEGORIES = ["sc", "st", "obc", "ews", "general", "scheduled caste", "scheduled tribe"]

    FIELDS = list(FIELD_SYNONYMS.keys()) + [
        "artificial intelligence", "machine learning", "computer science",
        "data science", "engineering", "management", "medicine", "law",
        "economics", "psychology", "biology", "chemistry", "physics",
        "computer vision", "robotics", "business", "finance", "marketing",
    ]

    INDIAN_CITIES = [
        "mumbai", "delhi", "bangalore", "bengaluru", "hyderabad", "chennai",
        "kolkata", "pune", "ahmedabad", "jaipur", "lucknow", "noida", "gurgaon",
    ]

    # Phrases that signal the user is EXPLORING (no personal info needed)
    EXPLORATORY_PATTERNS = [
        r'opportunities?\s+in\s+\w+',
        r'scholarships?\s+in\s+\w+',
        r'phd\s+(?:opportunities?|positions?|programs?|in)\s+\w+',
        r'masters?\s+(?:in|at|programs?|opportunities?)',
        r'bachelors?\s+(?:in|at|programs?|opportunities?)',
        r'universit(?:y|ies)\s+in\s+\w+',
        r'programs?\s+in\s+\w+',
        r'courses?\s+in\s+\w+',
        r'funded\s+(?:phd|masters|positions?|programs?)',
        r'(?:study|work|research)\s+(?:in|abroad|overseas)',
        r'(?:daad|erasmus|fulbright|commonwealth|chevening)',
        r'government\s+scheme',
        r'education\s+loan',
        r'list\s+(?:of\s+)?(?:scholarships|universities|programs|courses)',
        r'top\s+(?:scholarships|universities|programs|courses)',
        r'career\s+(?:after|opportunities|options|paths?)',
        r'after\s+(?:mca|bca|b\.?tech|m\.?tech|bsc|msc|bcom|mcom|bba|mba|ba|ma|phd)',
        r'jobs?\s+(?:in|after|for)',
        r'internships?\s+(?:in|at|for|programs?)',
        r'fellowships?\s+(?:in|at|programs?)',
        r'grants?\s+(?:in|for)',
        r'competitions?\s+(?:in|for)',
        r'startup\s+(?:funding|grants?|schemes?)',
        r'visa\s+(?:requirements?|process|types?)',
        r'admission\s+(?:requirements?|process|deadlines?)',
        r'ranking[s]?\s+(?:of|for|in)',
    ]

    # Phrases that signal PERSONALIZATION NEEDED
    PERSONALIZATION_PATTERNS = [
        r'(?:best|ideal|perfect|right|suitable)\s+(?:for|scholarship|opportunity)',
        r'(?:for|to)\s+me\b',
        r'(?:my|my profile|my background|my qualifications?)',
        r'am\s+i\s+(?:eligible|qualified|fit)',
        r'can\s+i\s+(?:get|apply|qualify|avail)',
        r'recommend\s+(?:me|for me)',
        r'suggest\s+(?:me|for me)',
        r'what\s+(?:are my|should i|can i)',
        r'chances?\s+(?:of|for|to)',
        r'possible\s+for\s+me',
    ]

    def _normalize_degree(self, raw: str) -> str:
        raw = raw.lower().strip().replace(".", "")
        mapping = {
            "mca": "MCA", "bca": "BCA",
            "btech": "B.Tech", "mtech": "M.Tech",
            "be": "B.E.", "me": "M.E.",
            "bsc": "B.Sc", "msc": "M.Sc",
            "bcom": "B.Com", "mcom": "M.Com",
            "bba": "BBA", "mba": "MBA",
            "ba": "B.A.", "ma": "M.A.",
            "mbbs": "MBBS", "bds": "BDS",
            "llb": "LLB", "llm": "LLM",
            "phd": "PhD", "ph.d": "PhD",
        }
        return mapping.get(raw, raw.upper())

    def _infer_profile(self, q_lower: str, intent_obj: Dict) -> Dict:
        quals = []
        for d in [intent_obj.get("qualification"), intent_obj.get("degree")]:
            if d:
                quals.append(d.lower().replace(".", ""))
        if not quals:
            m = re.search(r'\b(mca|bca|b\.?tech|m\.?tech|bsc|msc|bcom|mcom|bba|mba|b\.?a|m\.?a|mbbs|bds|llb|llm|phd)\b', q_lower)
            if m:
                quals.append(m.group(1).replace(".", ""))

        inferred_field = None
        inferred_career_paths = []
        inferred_abroad = None
        for q in quals:
            for deg_key, field in DEGREE_FIELD_MAP.items():
                if deg_key in q:
                    inferred_field = field
                    break
            for deg_key, paths in DEGREE_CAREER_PATHS.items():
                if deg_key in q:
                    inferred_career_paths = paths
                    break
            for deg_key, abroad in DEGREE_ABROAD_FIELDS.items():
                if deg_key in q:
                    inferred_abroad = abroad
                    break

        if inferred_field and not intent_obj.get("field"):
            intent_obj["field"] = inferred_field
        if inferred_abroad and not intent_obj.get("specialization"):
            intent_obj["specialization"] = inferred_abroad
        intent_obj["inferred_career_paths"] = inferred_career_paths
        intent_obj["inferred_field"] = inferred_field
        return intent_obj

    def _is_exploratory(self, q_lower: str) -> bool:
        """True = search immediately, no follow-up needed. False = may need personalization info."""
        for pat in self.EXPLORATORY_PATTERNS:
            if re.search(pat, q_lower):
                return True
        # If it explicitly matches personalization, it's NOT exploratory
        for pat in self.PERSONALIZATION_PATTERNS:
            if re.search(pat, q_lower):
                return False
        # Short vague queries like "scholarships" are unclear — treat as exploratory
        # unless they contain personalization keywords
        return False

    def _detect_career_guidance(self, q_lower: str, primary_intent: str = "") -> bool:
        """Detect career guidance — but NOT when a specific degree/research intent is already detected."""
        # If a specific academic intent is already detected, don't override
        if primary_intent in ("PhD", "Masters", "Bachelor", "Research", "Research Grant",
                               "Research Position", "Scholarship", "Fellowship", "Grant",
                               "Exchange", "Competition", "Visa", "Admission", "Ranking"):
            return False
        # If the query name-drops a specific program/degree, don't override
        if re.search(r'\b(phd|masters?|bachelors?|m\.?(sc|tech)|b\.?(sc|tech))\b', q_lower):
            return False
        patterns = [
            r'(?:career|job|future)\s+(?:options?|opportunities?|scope|prospects?)',
            r'(?:what|what are|what is|tell me about|suggest|find)\s+(?:careers?|options?|scope|paths?)',
            r'what\s+(?:can|should)\s+(?:i|we)\s+(?:do|become|pursue)',
            r'(?:guide|counsel|advise|recommend)\s+(?:me|for|on)',
            r'career\s+(?:pathways?|roadmap|guidance|counseling)',
            r'\b(mca|bca|b\.?tech|m\.?tech|bsc|msc|bcom|mcom|bba|mba)\s+career\b',
        ]
        for pat in patterns:
            if re.search(pat, q_lower):
                return True
        # "after MCA", "after BCA" etc — specific degree career queries
        if re.search(r'\b(after|post)\s+(mca|bca|b\.?tech|m\.?tech|bsc|msc|bcom|mcom|bba|mba)', q_lower):
            return True
        return False

    def parse(self, query: str, session_profile: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        q_lower = query.lower().strip()
        session_profile = session_profile or {}

        # Primary intent detection FIRST
        primary_intent = self._detect_intent(q_lower)

        # Only override with Career Advice if no specific academic/program intent
        if primary_intent in ("Opportunity Search", "Study Abroad", "Scholarship", "Internship", "Job Search", "Government Scheme", "Startup"):
            if self._detect_career_guidance(q_lower, primary_intent):
                primary_intent = "Career Advice"

        # Determine if this is exploratory or personalized
        is_exploratory = self._is_exploratory(q_lower)
        # Override: if it's a personalization query, force not exploratory
        for pat in self.PERSONALIZATION_PATTERNS:
            if re.search(pat, q_lower):
                is_exploratory = False
                break

        intent_obj = {
            "original_query": query,
            "country": self._extract_single_country(q_lower) or session_profile.get("country"),
            "countries": self._extract_countries(q_lower) or session_profile.get("countries", []),
            "city": self._extract_city(q_lower) or session_profile.get("city"),
            "degree": self._extract_target_degree(q_lower) or session_profile.get("degree"),
            "qualification": self._extract_current_qualification(q_lower) or session_profile.get("qualification"),
            "desired_qualification": self._extract_target_degree(q_lower) or session_profile.get("desired_qualification"),
            "field": self._extract_field(q_lower) or session_profile.get("field"),
            "course": self._extract_course(q_lower) or session_profile.get("course"),
            "specialization": self._extract_specialization(q_lower) or session_profile.get("specialization"),
            "cgpa": self._extract_cgpa(q_lower) or session_profile.get("cgpa"),
            "percentage": self._extract_percentage(q_lower) or session_profile.get("percentage"),
            "marks": self._extract_marks_dict(q_lower, session_profile),
            "backlogs": self._extract_backlogs(q_lower) or session_profile.get("backlogs"),
            "work_experience": self._extract_work_experience(q_lower) or session_profile.get("work_experience"),
            "research_experience": self._extract_research_experience(q_lower) or session_profile.get("research_experience"),
            "publications": self._extract_publications(q_lower) or session_profile.get("publications"),
            "internship_experience": self._extract_internship(q_lower) or session_profile.get("internship_experience"),
            "gender": self._extract_gender(q_lower) or session_profile.get("gender"),
            "category": self._extract_caste_category(q_lower) or session_profile.get("category"),
            "income": self._extract_income(q_lower) or session_profile.get("income"),
            "budget": self._extract_budget(q_lower) or session_profile.get("budget"),
            "loan_requirement": self._detect_loan(q_lower) or session_profile.get("loan_requirement"),
            "funding": self._extract_funding(q_lower) or session_profile.get("funding"),
            "fully_funded": "fully funded" in q_lower or "full ride" in q_lower or session_profile.get("fully_funded"),
            "partially_funded": "partial" in q_lower or session_profile.get("partially_funded"),
            "ielts": self._extract_test_score(q_lower, "ielts") or session_profile.get("ielts"),
            "toefl": self._extract_test_score(q_lower, "toefl") or session_profile.get("toefl"),
            "gre": self._extract_test_score(q_lower, "gre") or session_profile.get("gre"),
            "gmat": self._extract_test_score(q_lower, "gmat") or session_profile.get("gmat"),
            "sat": self._extract_test_score(q_lower, "sat") or session_profile.get("sat"),
            "act": self._extract_test_score(q_lower, "act") or session_profile.get("act"),
            "preferred_intake": self._extract_intake(q_lower) or session_profile.get("preferred_intake"),
            "application_year": self._extract_application_year(q_lower) or session_profile.get("application_year"),
            "study_abroad": self._detect_study_abroad(q_lower, session_profile),
            "government_scheme": self._detect_government_scheme(q_lower),
            "startup": "startup" in q_lower,
            "internship": "internship" in q_lower or "intern" in q_lower,
            "grant": "grant" in q_lower,
            "competition": "competition" in q_lower or "hackathon" in q_lower,
            "research": "research" in q_lower,
            "exchange_program": "exchange" in q_lower,
            "fellowship": "fellowship" in q_lower,
            "volunteer": "volunteer" in q_lower,
            "job": any(w in q_lower for w in ["job", "employment", "career", "position"]),
            "career_goal": self._extract_career_goal(q_lower) or session_profile.get("career_goal"),
            "intent": primary_intent,
            "keywords": self._extract_keywords(q_lower),
            "inferred_career_paths": [],
            "inferred_field": None,
            "missing_information": [],
            "follow_up_required": False,
            "follow_up_questions": [],
            "is_exploratory": is_exploratory,
        }

        # Step 1: Infer profile from detected degree/qualification
        intent_obj = self._infer_profile(q_lower, intent_obj)

        # Step 2: For exploratory queries — search immediately, no follow-up
        if is_exploratory:
            intent_obj["follow_up_required"] = False
            intent_obj["follow_up_questions"] = []
            intent_obj["missing_information"] = []
            logger.info(f"Exploratory query — searching immediately. intent={primary_intent}")
        else:
            # Step 3: For personalized queries — detect what's missing minimally
            intent_obj["missing_information"] = self._detect_missing(intent_obj)
            intent_obj["follow_up_questions"] = self._build_follow_up_questions(intent_obj)
            intent_obj["follow_up_required"] = self._should_ask_follow_up(intent_obj, query)

        logger.info(f"Structured intent: intent={intent_obj['intent']}, exploratory={is_exploratory}, field={intent_obj.get('field')}, country={intent_obj['country']}")
        return intent_obj

    def _extract_countries(self, q: str) -> List[str]:
        found = []
        for c in self.COUNTRIES:
            if re.search(r'\b' + re.escape(c) + r'\b', q):
                canonical = self.COUNTRY_CANONICAL.get(c, c.title())
                if canonical not in found:
                    found.append(canonical)
        return found

    def _extract_single_country(self, q: str) -> Optional[str]:
        countries = self._extract_countries(q)
        return countries[0] if countries else None

    def _extract_city(self, q: str) -> Optional[str]:
        for city in self.INDIAN_CITIES:
            if re.search(r'\b' + city + r'\b', q):
                return city.title()
        city_match = re.search(r'(?:in|at|from)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', q)
        if city_match:
            candidate = city_match.group(1)
            if candidate.lower() not in self.COUNTRIES:
                return candidate
        return None

    def _extract_current_qualification(self, q: str) -> Optional[str]:
        patterns = [
            r'i\s+(?:have|hold|completed|done|did)\s+(?:a\s+)?([a-z\.]+(?:\s+[a-z\.]+)?)',
            r'(?:with|having)\s+([a-z\.]+(?:\s+[a-z\.]+)?)\s+(?:degree|qualification|cgpa|gpa)',
            r'\b(mca|mba|b\.?tech|m\.?tech|b\.?sc|m\.?sc|b\.?com|m\.?com|b\.?a|m\.?a|phd|bca|be|me)\b',
        ]
        for pat in patterns:
            m = re.search(pat, q)
            if m:
                qual = m.group(1).strip()
                return normalize_term(qual, DEGREE_SYNONYMS).title() if qual else None
        return None

    def _extract_target_degree(self, q: str) -> Optional[str]:
        want_patterns = [
            r'want\s+(?:a\s+)?(?:fully funded\s+)?(?:[\w\s]+\s+)?(masters?|bachelors?|phd|mba|mca|diploma|postgraduate|undergraduate)',
            r'(?:for|in|pursue|pursuing|apply(?:ing)?\s+(?:for|to))\s+(?:a\s+)?(masters?|bachelors?|phd|mba|mca|diploma)',
            r'\b(masters?|bachelors?|phd|mba|mca|m\.?sc|b\.?sc|m\.?tech|b\.?tech)\b',
        ]
        for pat in want_patterns:
            m = re.search(pat, q)
            if m:
                deg = normalize_term(m.group(1), DEGREE_SYNONYMS)
                return deg.title() if deg != "masters" else "Masters"
        return None

    def _extract_field(self, q: str) -> Optional[str]:
        field_patterns = [
            r'(?:in|for|studying|study)\s+(artificial intelligence|machine learning|computer science|data science|engineering|management|medicine|law|economics|robotics|computer vision)',
            r'\b(ai|ml|cs|it|ds|cse|ece|mechanical|civil|finance|marketing|biology|chemistry|physics)\b',
        ]
        for pat in field_patterns:
            m = re.search(pat, q)
            if m:
                term = m.group(1)
                return normalize_term(term, FIELD_SYNONYMS).title()
        return None

    def _extract_course(self, q: str) -> Optional[str]:
        m = re.search(r'(?:course|program(?:me)?)\s+(?:in|on|for)\s+([\w\s]+?)(?:\s+in|\s+at|\s+for|$)', q)
        return m.group(1).strip().title() if m else None

    def _extract_specialization(self, q: str) -> Optional[str]:
        m = re.search(r'(?:specializ(?:e|ing|ation)\s+(?:in|on))\s+([\w\s]+)', q)
        if m:
            return m.group(1).strip().title()
        return self._extract_field(q)

    def _extract_cgpa(self, q: str) -> Optional[float]:
        patterns = [
            r'(?:cgpa|gpa)[:\s]*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*(?:cgpa|gpa)',
        ]
        for pat in patterns:
            m = re.search(pat, q)
            if m:
                val = float(m.group(1))
                if 0 < val <= 10:
                    return val
        return None

    def _extract_percentage(self, q: str) -> Optional[float]:
        m = re.search(r'(\d+(?:\.\d+)?)\s*(?:%|percent|percentage)', q)
        return float(m.group(1)) if m else None

    def _extract_marks_dict(self, q: str, session: Dict) -> Optional[Dict]:
        cgpa = self._extract_cgpa(q) or session.get("cgpa")
        pct = self._extract_percentage(q) or session.get("percentage")
        if cgpa or pct:
            d = {}
            if cgpa:
                d["cgpa"] = cgpa
            if pct:
                d["percentage"] = pct
            return d
        return session.get("marks")

    def _extract_backlogs(self, q: str) -> Optional[int]:
        m = re.search(r'(\d+)\s*(?:backlogs?|kt|arrears?)', q)
        if m:
            return int(m.group(1))
        if "no backlog" in q or "zero backlog" in q:
            return 0
        return None

    def _extract_work_experience(self, q: str) -> Optional[Dict]:
        m = re.search(r'(\d+)\s*(?:\+?\s*)?(?:years?|yrs?)\s*(?:of\s+)?(?:work\s+)?(?:experience|exp)', q)
        if m:
            return {"years": int(m.group(1)), "type": "work"}
        return None

    def _extract_research_experience(self, q: str) -> Optional[Dict]:
        if "research experience" in q or "research background" in q:
            m = re.search(r'(\d+)\s*(?:years?|yrs?)', q)
            return {"years": int(m.group(1)) if m else 1, "type": "research"}
        return None

    def _extract_publications(self, q: str) -> Optional[int]:
        m = re.search(r'(\d+)\s*(?:publications?|papers?|research papers?)', q)
        return int(m.group(1)) if m else None

    def _extract_internship(self, q: str) -> Optional[Dict]:
        if "internship" in q:
            m = re.search(r'(\d+)\s*(?:months?|years?)', q)
            return {"duration": m.group(0) if m else "mentioned"}
        return None

    def _extract_gender(self, q: str) -> Optional[str]:
        if re.search(r'\b(?:female|woman|women|girl)\b', q):
            return "Female"
        if re.search(r'\b(?:male|man|men|boy)\b', q):
            return "Male"
        return None

    def _extract_caste_category(self, q: str) -> Optional[str]:
        for cat in self.CASTE_CATEGORIES:
            if re.search(r'\b' + cat + r'\b', q):
                return cat.upper() if len(cat) <= 3 else cat.title()
        return None

    def _extract_income(self, q: str) -> Optional[str]:
        m = re.search(r'(?:income|family income|annual income)[:\s]*(?:rs\.?|inr|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:lakhs?|lacs?|lpa|cr)?', q)
        if m:
            return m.group(0)
        if "low income" in q or "economically weaker" in q or "ews" in q:
            return "Low Income"
        return None

    def _extract_budget(self, q: str) -> Optional[Dict]:
        budget = {}
        m = re.search(r'(?:budget|afford|spend)[:\s]*(?:\$|usd|€|inr|₹|rs\.?)?\s*(\d+(?:,\d+)*)', q)
        if m:
            budget["amount"] = float(m.group(1).replace(",", ""))
        if "affordable" in q or "low budget" in q or "cheap" in q:
            budget["type"] = "Low"
        elif "high budget" in q or "expensive" in q:
            budget["type"] = "High"
        return budget if budget else None

    def _detect_loan(self, q: str) -> bool:
        return any(w in q for w in ["loan", "education loan", "student loan", "financing", "credit"])

    def _extract_funding(self, q: str) -> Optional[str]:
        if "fully funded" in q or "full ride" in q or "100% funded" in q:
            return "Fully Funded"
        if "partial" in q or "partially funded" in q:
            return "Partially Funded"
        if "scholarship" in q or "fellowship" in q or "grant" in q:
            return "Scholarship"
        return None

    def _extract_test_score(self, q: str, test: str) -> Optional[float]:
        m = re.search(rf'{test}[:\s]*(\d+(?:\.\d+)?)', q)
        return float(m.group(1)) if m else None

    def _extract_intake(self, q: str) -> Optional[str]:
        if "fall" in q or "september" in q or "october" in q:
            return "Fall"
        if "spring" in q or "january" in q or "february" in q:
            return "Spring"
        if "summer" in q or "may" in q:
            return "Summer"
        if "winter" in q:
            return "Winter"
        return None

    def _extract_application_year(self, q: str) -> Optional[int]:
        m = re.search(r'\b(202[4-9]|203[0-5])\b', q)
        return int(m.group(1)) if m else None

    def _detect_study_abroad(self, q: str, session: Dict) -> bool:
        if any(w in q for w in ["abroad", "overseas", "international", "foreign", "study abroad", "global"]):
            return True
        if session.get("study_abroad"):
            return True
        country = self._extract_single_country(q) or session.get("country")
        if country and country not in ("India",):
            return True
        if "india" in q and any(w in q for w in ["opportunities", "options", "scope", "career", "abroad"]):
            return True
        return False

    def _detect_government_scheme(self, q: str) -> bool:
        return any(w in q for w in ["scheme", "government", "govt", "ministry", "aicte", "ugc", "nsp"])

    def _extract_career_goal(self, q: str) -> Optional[str]:
        m = re.search(r'(?:want to become|aspire to|career in|goal is)\s+(?:a\s+)?([\w\s]+?)(?:\.|,|$)', q)
        return m.group(1).strip().title() if m else None

    def _detect_intent(self, q: str) -> str:
        """Detect the most specific intent from the query. Order matters — more specific first."""
        # Comparison
        if any(w in q for w in ["compare", "vs ", "versus", "difference between", "which is better"]):
            return "Comparison"
        # Eligibility
        if any(w in q for w in ["eligible", "can i get", "can i apply", "qualify", "chance", "possible for me", "am i eligible"]):
            return "Eligibility Check"
        # Visa
        if any(w in q for w in ["visa", "student visa", "work visa", "visa process", "visa requirement"]):
            return "Visa"
        # Admission
        if any(w in q for w in ["admission", "admissions", "application process", "how to apply", "apply to university"]):
            return "Admission"
        # Ranking
        if any(w in q for w in ["ranking", "rankings", "top university", "best university", "world ranking"]):
            return "Ranking"
        # Hackathon / Competition
        if "hackathon" in q or ("competition" in q and "scholarship" not in q):
            return "Competition"
        # Startup / Incubator / Accelerator
        if any(w in q for w in ["startup", "entrepreneur", "incubator", "accelerator", "venture capital"]):
            return "Startup"
        # Conference
        if any(w in q for w in ["conference", "conferences", "academic conference", "research conference"]):
            return "Conference"
        # Journal / Publication
        if any(w in q for w in ["journal", "publication", "research paper", "paper submission", "call for papers"]):
            return "Journal"
        # Research Grant
        if any(w in q for w in ["research grant", "research funding", "research fellowship"]):
            return "Research Grant"
        # Research Position
        if any(w in q for w in ["research position", "research assistant", "postdoc", "post-doctoral", "research scientist"]):
            return "Research Position"
        # Research (general)
        if "research" in q and "scholarship" not in q:
            return "Research"
        # PhD
        if re.search(r'\bphd\b', q) or re.search(r'\bph\.d\b', q) or re.search(r'\bdoctorate\b', q):
            if any(w in q for w in ["position", "funded", "opportunity", "program", "scholarship"]):
                return "PhD"
            if "scholarship" in q or "funding" in q:
                return "PhD"
            return "PhD"
        # Masters
        if re.search(r'\bmasters?\b', q) or re.search(r'\bm\.sc\b', q) or re.search(r'\bm\.tech\b', q) or re.search(r'\bpostgraduate\b', q):
            if any(w in q for w in ["scholarship", "funding", "funded", "program", "opportunity"]):
                return "Masters"
            return "Masters"
        # Bachelor
        if re.search(r'\bbachelors?\b', q) or re.search(r'\bb\.sc\b', q) or re.search(r'\bb\.tech\b', q) or re.search(r'\bundergraduate\b', q):
            return "Bachelor"
        # Exchange program
        if "exchange" in q:
            return "Exchange"
        # Fellowship
        if "fellowship" in q:
            return "Fellowship"
        # Education Loan
        if self._detect_loan(q):
            return "Loan"
        # Government Scheme
        if self._detect_government_scheme(q):
            return "Government Scheme"
        # Funding (general funding search)
        if any(w in q for w in ["funding", "funded", "financial support", "financial aid"]):
            return "Funding"
        # Internship
        if "internship" in q or "intern" in q:
            return "Internship"
        # Job
        if "job" in q or "employment" in q or "jobs" in q:
            return "Job Search"
        # Career Advice (with awareness of detected intent above)
        already_intent = None
        # Check if a specific intent was already matched
        if re.search(r'\bphd\b', q) or re.search(r'\bmasters?\b', q) or re.search(r'\bbachelors?\b', q):
            pass  # Let the specific intent stand
        elif self._detect_career_guidance(q):
            return "Career Advice"
        # Grant
        if "grant" in q:
            return "Grant"
        # Study Abroad
        if self._detect_study_abroad(q, {}):
            return "Study Abroad"
        # University Search
        if any(w in q for w in ["university", "universities", "college", "colleges", "institute"]):
            return "University Search"
        # Course Search
        if any(w in q for w in ["course", "courses", "program", "programs", "certificate", "diploma"]):
            return "Course Search"
        # Scholarship (fallback — must be last among specific)
        if any(w in q for w in ["scholarship", "scholarships", "sponsored", "fully funded", "full ride"]):
            return "Scholarship"
        # Explain / What is
        if any(w in q for w in ["what is", "explain", "tell me about", "what does", "how does"]):
            return "Explain"
        # Decision help
        if any(w in q for w in ["should i", "which one", "help me decide", "confused", "suggest"]):
            return "Decision"
        # Roadmap / How to
        if any(w in q for w in ["roadmap", "how to", "step by step", "process", "procedure"]):
            return "Roadmap"
        return "Opportunity Search"

    def _extract_keywords(self, q: str) -> str:
        remove_terms = set(self.COUNTRIES + self.DEGREES + self.CATEGORIES + list(FIELD_SYNONYMS.keys()))
        remaining = q
        for term in sorted(remove_terms, key=len, reverse=True):
            remaining = re.sub(r'\b' + re.escape(term) + r'\b', '', remaining)
        return " ".join(remaining.split())

    def _detect_missing(self, intent: Dict) -> List[str]:
        """Detect truly missing info — only for personalized queries, ask minimum."""
        missing = []
        intent_type = intent.get("intent", "")

        # Career Advice — only ask qualification if not present
        if intent_type == "Career Advice":
            if not intent.get("qualification") and not intent.get("degree"):
                missing.append("Current qualification or degree")
            return missing

        # Eligibility Check — ask qualification + marks
        if intent_type == "Eligibility Check":
            if not intent.get("qualification") and not intent.get("degree"):
                missing.append("Current qualification")
            if not intent.get("cgpa") and not intent.get("marks"):
                missing.append("Academic marks/CGPA")
            return missing

        # Comparison — no missing info needed
        if intent_type == "Comparison":
            return missing

        # PhD / Masters / Bachelor / Exchange / Fellowship — country + degree
        if intent_type in ("PhD", "Masters", "Bachelor", "Exchange", "Fellowship", "Study Abroad"):
            if not intent.get("country") and not intent.get("countries"):
                missing.append("Target country")
            # Only ask degree for personalized "for me" queries
            return missing

        # Scholarship / Funding / Grant — country only
        if intent_type in ("Scholarship", "Funding", "Grant", "Research Grant"):
            if not intent.get("country") and not intent.get("countries"):
                missing.append("Target country")
            return missing

        # Loan
        if intent_type == "Loan":
            if not intent.get("budget"):
                missing.append("Budget/loan amount needed")
            return missing

        # Visa / Admission — no personal info needed
        if intent_type in ("Visa", "Admission", "Ranking", "Conference", "Journal", "Competition"):
            return missing

        # Job Search / Internship
        if intent_type in ("Job Search", "Internship"):
            if not intent.get("country") and not intent.get("countries"):
                missing.append("Target country")
            return missing

        # University Search / Course Search
        if intent_type in ("University Search", "Course Search"):
            if not intent.get("country") and not intent.get("countries"):
                missing.append("Target country")
            return missing

        # Startup / Government Scheme
        if intent_type in ("Startup", "Government Scheme", "Research Position"):
            return missing

        # Fallback for Opportunity Search
        if intent_type == "Opportunity Search":
            if not intent.get("country") and not intent.get("countries"):
                pass  # Don't force country — search broadly

        return missing

    def _build_follow_up_questions(self, intent: Dict) -> List[str]:
        """Build targeted follow-up questions based on what's actually missing."""
        questions = []
        intent_type = intent.get("intent", "")

        if intent_type == "Career Advice":
            qual = intent.get("qualification") or ""
            if any(k in qual.lower() for k in ["mca", "bca", "b.tech", "m.tech", "bsc", "msc", "bcom"]):
                questions = [
                    "Which area interests you most? (Higher Studies, Jobs, Study Abroad, Startups, Research, Certifications)"
                ]
            else:
                questions = [
                    "What is your current qualification?",
                    "What are you looking for — higher studies, jobs, or scholarships?",
                ]
            return questions

        if intent_type == "Eligibility Check":
            questions = [
                "Which opportunity or program are you checking eligibility for?",
                "What is your highest qualification?",
                "What is your CGPA or percentage?",
            ]
            return questions

        if intent_type == "Comparison":
            return [
                "Which two opportunities would you like to compare?",
                "What criteria matter most to you (funding, eligibility, deadlines)?",
            ]

        mapping = {}
        for item in intent.get("missing_information", []):
            if item in mapping:
                questions.append(mapping[item])

        # Only add personalized questions if the query truly needs them
        if intent.get("is_exploratory"):
            return []  # No follow-up for exploratory queries

        # For personalized queries — minimal, targeted questions
        if intent_type in ("PhD", "Masters", "Bachelor", "Exchange", "Fellowship", "Study Abroad"):
            if not intent.get("country") and not intent.get("countries"):
                questions.append("Which country are you interested in?")
            return questions

        if intent_type in ("Scholarship", "Funding", "Grant", "Research Grant"):
            if not intent.get("country") and not intent.get("countries"):
                questions.append("Which country are you interested in?")
            return questions

        if intent_type == "Loan":
            questions.append("How much loan do you need?")
            return questions

        if intent_type in ("Job Search", "Internship"):
            if not intent.get("country") and not intent.get("countries"):
                questions.append("Which country are you interested in?")
            return questions

        return questions

    def _should_ask_follow_up(self, intent: Dict, query: str) -> bool:
        """Ask follow-up only when query is personal and truly needs info."""
        # Never ask for exploratory queries
        if intent.get("is_exploratory"):
            return False

        # Never ask for these intents
        if intent.get("intent") in ("Comparison", "Visa", "Admission", "Ranking",
                                     "Conference", "Journal", "Competition", "Startup",
                                     "Explain", "Decision", "Roadmap"):
            return False

        # Career Advice — ask only if no qualification
        if intent.get("intent") == "Career Advice":
            return not intent.get("qualification") and not intent.get("degree")

        # Eligibility Check — ask if missing qualification or marks
        if intent.get("intent") == "Eligibility Check":
            return not intent.get("qualification") or not intent.get("cgpa")

        # For personalized queries that match personalization patterns
        q_lower = query.lower()
        is_personal = any(re.search(pat, q_lower) for pat in self.PERSONALIZATION_PATTERNS)

        if is_personal:
            # Only ask if critical info is missing
            if intent.get("intent") in ("PhD", "Masters", "Bachelor", "Scholarship",
                                         "Study Abroad", "Fellowship", "Exchange",
                                         "Funding", "Grant"):
                return not intent.get("country") and not intent.get("countries")

        return False

    def to_search_params(self, intent: Dict) -> Dict[str, Any]:
        """Convert structured intent to search_engine params."""
        countries = intent.get("countries") or []
        if intent.get("country") and intent["country"] not in countries:
            countries = [intent["country"]] + countries

        degrees = []
        for d in [intent.get("degree"), intent.get("qualification"), intent.get("desired_qualification")]:
            if d:
                degrees.append(normalize_term(d, DEGREE_SYNONYMS))

        categories = []
        intent_map = {
            "Scholarship": "scholarship", "Scholarship Search": "scholarship",
            "Loan": "loan", "Loan Search": "loan",
            "Government Scheme": "scheme",
            "Internship": "internship", "Internship Search": "internship",
            "Fellowship": "fellowship", "Fellowship Search": "fellowship",
            "Grant": "grant", "Grant Search": "grant",
            "Research": "research", "Research Search": "research",
            "Research Grant": "research",
            "Research Position": "research",
            "PhD": "research", "PhD Search": "research",
            "Masters": "", "Masters Search": "",
            "Bachelor": "", "Bachelor Search": "",
            "Exchange": "exchange program", "Exchange Search": "exchange program",
            "Job Search": "job",
            "Eligibility Check": "",
            "Funding": "", "Competition": "competition", "Competition Search": "competition",
            "University Search": "", "Course Search": "",
            "Visa Search": "", "Admission Search": "",
            "Conference Search": "", "Journal Search": "",
            "Ranking Search": "", "Startup Search": "grant",
        }
        if intent.get("intent") in intent_map:
            cat = intent_map[intent["intent"]]
            if cat:
                categories.append(cat)
        elif intent.get("intent") == "Career Advice":
            categories = ["job", "internship", "fellowship", "grant"]

        field = intent.get("field") or intent.get("inferred_field")
        if field and "Computer" in field and "scholarship" not in categories:
            categories.append("scholarship")

        funding = []
        if intent.get("funding"):
            funding.append(intent["funding"].lower())
        if intent.get("fully_funded"):
            funding.append("fully funded")

        keyword_parts = [
            intent.get("field"), intent.get("course"), intent.get("specialization"),
            intent.get("keywords"), intent.get("career_goal"),
        ]
        keywords = " ".join(p for p in keyword_parts if p)

        return {
            "keywords": keywords,
            "countries": [c.lower() for c in countries],
            "degrees": degrees,
            "categories": list(set(categories)),
            "funding": funding,
            "field": intent.get("field") or intent.get("inferred_field"),
            "provider_hints": intent.get("countries", []),
            "intent": intent.get("intent"),
        }


query_parser = QueryParser()
