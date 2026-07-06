"""
STEP 1 & 2: Understand the User and Detect Missing Information

Extracts detailed user profile from the query using NLP patterns
and detects what information is missing for better recommendations.
"""

import re
from typing import Dict, List, Any, Tuple
from ..utils.logger import get_logger

logger = get_logger(__name__)

class UserProfileExtractor:
    """
    Extracts user profile information from query.
    Understands: Education, marks, country, degree, stream, budget, funding needs, etc.
    """
    
    DEGREES_MAP = {
        "bachelor": "Bachelor's",
        "bachelors": "Bachelor's",
        "b.tech": "Bachelor's",
        "b.sc": "Bachelor's",
        "b.a": "Bachelor's",
        "b.com": "Bachelor's",
        "undergrad": "Bachelor's",
        "master": "Master's",
        "masters": "Master's",
        "m.tech": "Master's",
        "m.sc": "Master's",
        "mba": "MBA",
        "m.a": "Master's",
        "m.com": "Master's",
        "mca": "Master's",
        "phd": "PhD",
        "doctorate": "PhD",
        "postdoc": "Postdoctoral",
        "diploma": "Diploma",
        "pg": "Postgraduate",
        "ug": "Undergraduate",
    }
    
    STREAMS = ["engineering", "management", "science", "arts", "commerce", "law", "medicine", "nursing", "architecture", "design", "it", "cse", "ece", "mechanical", "civil", "ai", "ml", "data science", "business", "psychology", "sociology"]
    
    TEST_SCORES = ["ielts", "toefl", "gre", "gmat", "gate", "sat", "act", "jee"]
    
    FUNDING_KEYWORDS = ["fully funded", "full ride", "partial funding", "half funded", "100% funded", "sponsored", "scholarship", "fellowship", "grant", "loan", "free"]
    
    COUNTRIES = ["us", "usa", "uk", "germany", "canada", "australia", "india", "japan", "france", "netherlands", "sweden", "switzerland", "singapore", "ireland", "austria", "belgium", "finland", "europe"]
    
    def extract(self, query: str) -> Dict[str, Any]:
        """Extract comprehensive user profile from query."""
        q_lower = query.lower()
        
        profile = {
            "query": query,
            "intent": self._detect_intent(q_lower),
            "current_education": self._extract_current_education(q_lower),
            "marks": self._extract_marks(q_lower),
            "target_country": self._extract_country(q_lower),
            "target_degree": self._extract_degree(q_lower),
            "stream": self._extract_stream(q_lower),
            "funding_requirement": self._extract_funding(q_lower),
            "work_experience": self._extract_experience(q_lower),
            "test_scores": self._extract_test_scores(q_lower),
            "age": self._extract_age(q_lower),
            "budget": self._extract_budget(q_lower),
            "is_domestic": self._is_domestic_search(q_lower),
            "intake_preference": self._extract_intake(q_lower),
            "language_preference": self._extract_language_pref(q_lower),
            "missing_information": [],
        }
        
        # Detect missing information
        profile["missing_information"] = self._detect_missing(profile)
        
        logger.info(f"User Profile Extracted: {profile}")
        return profile
    
    def _detect_intent(self, q_lower: str) -> str:
        """Detect what user is looking for."""
        if any(word in q_lower for word in ["scholarship", "grant", "fund", "sponsored"]):
            return "scholarship_search"
        elif any(word in q_lower for word in ["internship", "intern"]):
            return "internship_search"
        elif any(word in q_lower for word in ["job", "position", "employment", "career"]):
            return "job_search"
        elif any(word in q_lower for word in ["loan", "financing", "credit"]):
            return "education_loan"
        elif any(word in q_lower for word in ["scheme", "government", "benefit"]):
            return "government_scheme"
        elif any(word in q_lower for word in ["exchange", "abroad", "study"]):
            return "study_abroad"
        return "opportunity_search"
    
    def _extract_current_education(self, q_lower: str) -> str:
        """Extract user's current/completed education."""
        for degree, canonical in self.DEGREES_MAP.items():
            if degree in q_lower:
                return canonical
        return None
    
    def _extract_marks(self, q_lower: str) -> Dict[str, float]:
        """Extract academic marks/percentage/CGPA."""
        marks_info = {}
        
        # CGPA pattern: "3.8 CGPA", "CGPA 3.8", "GPA 3.5"
        cgpa_match = re.search(r'(?:cgpa|gpa)[:\s]*(\d+\.\d+)', q_lower)
        if cgpa_match:
            marks_info["cgpa"] = float(cgpa_match.group(1))
        
        # Percentage pattern: "72%", "72 percent", "score 72"
        percent_match = re.search(r'(\d+)\s*(?:%|percent)', q_lower)
        if percent_match:
            marks_info["percentage"] = float(percent_match.group(1))
        
        return marks_info if marks_info else None
    
    def _extract_country(self, q_lower: str) -> str:
        """Extract target country."""
        for country in self.COUNTRIES:
            if country in q_lower:
                return country.title()
        return None
    
    def _extract_degree(self, q_lower: str) -> str:
        """Extract target degree level."""
        for degree, canonical in self.DEGREES_MAP.items():
            if degree in q_lower:
                return canonical
        return None
    
    def _extract_stream(self, q_lower: str) -> str:
        """Extract field of study."""
        for stream in self.STREAMS:
            if stream in q_lower:
                return stream.title()
        return None
    
    def _extract_funding(self, q_lower: str) -> str:
        """Extract funding requirement."""
        if "fully funded" in q_lower or "full ride" in q_lower:
            return "Fully Funded"
        elif "partial" in q_lower:
            return "Partial Funding"
        elif "free" in q_lower:
            return "Fully Funded"
        elif "paid" in q_lower or "sponsorship" in q_lower:
            return "Sponsored"
        return None
    
    def _extract_experience(self, q_lower: str) -> Dict[str, Any]:
        """Extract work experience."""
        exp = {}
        
        # Years of experience: "2 years experience", "5 yrs"
        years_match = re.search(r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|work|exp)', q_lower)
        if years_match:
            exp["years"] = int(years_match.group(1))
        
        # Experience type
        if "tech" in q_lower or "software" in q_lower:
            exp["field"] = "Technology"
        elif "finance" in q_lower:
            exp["field"] = "Finance"
        elif "marketing" in q_lower:
            exp["field"] = "Marketing"
        
        return exp if exp else None
    
    def _extract_test_scores(self, q_lower: str) -> Dict[str, float]:
        """Extract English test scores."""
        scores = {}
        
        # IELTS: "IELTS 7", "IELTS 7.5"
        ielts_match = re.search(r'ielts[:\s]*(\d+(?:\.\d+)?)', q_lower)
        if ielts_match:
            scores["ielts"] = float(ielts_match.group(1))
        
        # TOEFL: "TOEFL 100"
        toefl_match = re.search(r'toefl[:\s]*(\d+)', q_lower)
        if toefl_match:
            scores["toefl"] = int(toefl_match.group(1))
        
        return scores if scores else None
    
    def _extract_age(self, q_lower: str) -> int:
        """Extract age if mentioned."""
        age_match = re.search(r'(?:age|aged)\s*(\d+)', q_lower)
        if age_match:
            return int(age_match.group(1))
        return None
    
    def _extract_budget(self, q_lower: str) -> Dict[str, Any]:
        """Extract budget information."""
        budget = {}
        
        # Currency amounts: "$50000", "50000 USD", "INR 20 lakhs"
        amount_match = re.search(r'\$?(\d+(?:,?\d+)*)\s*(?:usd|inr|euro|gbp)?', q_lower)
        if amount_match:
            amount_str = amount_match.group(1).replace(',', '')
            try:
                budget["max_amount"] = float(amount_str)
            except:
                pass
        
        # Budget requirement
        if "expensive" in q_lower or "high cost" in q_lower:
            budget["type"] = "High Budget"
        elif "affordable" in q_lower or "cheap" in q_lower or "low cost" in q_lower:
            budget["type"] = "Low Budget"
        
        return budget if budget else None
    
    def _extract_intake(self, q_lower: str) -> str:
        """Extract preferred intake (fall, spring, etc.)."""
        if "fall" in q_lower or "september" in q_lower:
            return "Fall"
        elif "spring" in q_lower or "january" in q_lower:
            return "Spring"
        elif "summer" in q_lower:
            return "Summer"
        return None
    
    def _is_domestic_search(self, q_lower: str) -> bool:
        """Check if looking for domestic or international."""
        if any(word in q_lower for word in ["india", "domestic", "home", "local"]):
            return True
        elif any(word in q_lower for word in ["abroad", "international", "overseas", "foreign"]):
            return False
        return None
    
    def _extract_language_pref(self, q_lower: str) -> str:
        """Extract language preference."""
        if "hindi" in q_lower or "hinglish" in q_lower:
            return "hi"
        return "en"
    
    def _detect_missing(self, profile: Dict[str, Any]) -> List[str]:
        """Detect what critical information is missing."""
        missing = []
        
        if not profile.get("marks"):
            missing.append("Academic marks/CGPA/Percentage")
        
        if profile.get("intent") in ["scholarship_search", "study_abroad"]:
            if not profile.get("target_country"):
                missing.append("Target country/destination")
            if not profile.get("target_degree"):
                missing.append("Target degree level")
        
        if not profile.get("test_scores"):
            missing.append("English test scores (IELTS/TOEFL)")
        
        if profile.get("intent") in ["internship_search", "job_search"]:
            if not profile.get("work_experience"):
                missing.append("Work experience")
        
        if not profile.get("funding_requirement"):
            missing.append("Funding requirement (fully funded/partial)")
        
        return missing

user_profile_extractor = UserProfileExtractor()
