"""
Backend Decision Engine — performs all reasoning.
Gemini only explains verified results; this module decides.
"""

from typing import Dict, List, Any, Optional
from ..models.opportunity import InternalOpportunity
from ..utils.logger import get_logger

logger = get_logger(__name__)


class DecisionEngine:
    """Calculate eligibility, suitability, difficulty, confidence, recommendation, risk."""

    def analyze(
        self,
        user_profile: Dict[str, Any],
        opportunity: InternalOpportunity,
        eligibility_check: Dict[str, Any],
    ) -> Dict[str, Any]:
        checks = eligibility_check.get("checks", [])

        academic = self._match_category(
            next((c for c in checks if "Academic" in c.get("criterion", "")), None)
        )
        language = self._match_category(
            next((c for c in checks if "English" in c.get("criterion", "")), None)
        )
        experience = self._match_category(
            next((c for c in checks if "Experience" in c.get("criterion", "")), None)
        )
        funding = self._funding_match(user_profile, opportunity)
        degree = self._match_category(
            next((c for c in checks if "Degree" in c.get("criterion", "")), None)
        )

        eligible = eligibility_check.get("eligible", False)
        failed = eligibility_check.get("failed", 0)
        partial = eligibility_check.get("partial", 0)

        difficulty = self._assess_difficulty(opportunity)
        suitability = self._assess_suitability(academic, language, experience, funding, degree)
        confidence = self._assess_confidence(opportunity)
        risk = self._assess_risk(eligible, partial, failed, opportunity)
        recommendation = self._overall_recommendation(
            academic, language, experience, funding, eligible, partial, failed
        )

        verified = opportunity.verification or {}
        verified_details = getattr(opportunity, "verified_details", {}) or {}

        return {
            "eligibility": "Eligible" if eligible else ("Partially Eligible" if partial else "Not Eligible"),
            "suitability": suitability,
            "difficulty": difficulty,
            "confidence": confidence,
            "recommendation": recommendation,
            "risk": risk,
            "eligibility_analysis": {
                "academic_match": academic,
                "language_match": language,
                "experience_match": experience,
                "funding_match": funding,
                "degree_match": degree,
            },
            "overall_recommendation": recommendation,
            "why_recommended": self._why_recommended(user_profile, opportunity, recommendation),
            "why_not_fit": self._why_not_fit(checks, eligible),
            "overview": self._build_overview(opportunity, verified_details),
            "who_can_apply": verified_details.get("eligibility") or opportunity.eligibility or "Unknown",
            "required_qualification": verified_details.get("required_qualification") or opportunity.degree or "Unknown",
            "minimum_cgpa": verified_details.get("minimum_cgpa", "Unknown"),
            "required_experience": verified_details.get("experience", "Unknown"),
            "documents_required": verified_details.get("required_documents", "Unknown"),
            "funding_details": {
                "monthly_stipend": verified_details.get("stipend", "Unknown"),
                "tuition": verified_details.get("tuition", "Unknown"),
                "travel": verified_details.get("travel_support", "Unknown"),
                "accommodation": verified_details.get("living_allowance", "Unknown"),
                "health_insurance": verified_details.get("health_insurance", "Unknown"),
            },
            "application_process": verified_details.get("application_process", "Unknown"),
            "selection_process": verified_details.get("selection_process", "Unknown"),
            "application_fees": verified_details.get("application_fees", "Unknown"),
            "official_deadline": opportunity.live_deadline or opportunity.deadline or "Unknown",
            "official_source": verified.get("source") or opportunity.official_url or "Unknown",
            "verified_date": verified.get("last_checked", "Unknown"),
            "application_link": verified_details.get("application_link") or opportunity.verified_url or opportunity.official_url or "Unknown",
            "status": verified_details.get("status", "Unknown"),
            "language_requirements": {
                "ielts": verified_details.get("ielts", "Unknown"),
                "toefl": verified_details.get("toefl", "Unknown"),
                "gre": verified_details.get("gre", "Unknown"),
                "gmat": verified_details.get("gmat", "Unknown"),
            },
        }

    def _match_category(self, check: Optional[Dict]) -> str:
        if not check:
            return "Unknown"
        status = check.get("status", "UNKNOWN")
        if status == "PASS":
            diff = check.get("difference")
            if diff is not None and isinstance(diff, (int, float)) and diff >= 0.5:
                return "Excellent Match"
            return "Good Match"
        if status == "PARTIAL":
            return "Possible but Competitive"
        if status == "FAIL":
            note = check.get("note", "")
            if "missing" in note.lower() or "not provided" in note.lower():
                return "Missing — Required"
            return "Does Not Match"
        return "Unknown"

    def _funding_match(self, profile: Dict, opp: InternalOpportunity) -> str:
        user_funding = (profile.get("funding") or profile.get("funding_requirement") or "").lower()
        opp_funding = (opp.funding_type or "").lower()
        if not user_funding:
            return "Unknown"
        if not opp_funding:
            return "Unknown"
        if "fully" in user_funding and "fully" in opp_funding:
            return "Excellent Match"
        if user_funding in opp_funding or opp_funding in user_funding:
            return "Good Match"
        if "partial" in user_funding or "partial" in opp_funding:
            return "Possible but Competitive"
        return "Does Not Match"

    def _assess_difficulty(self, opp: InternalOpportunity) -> str:
        title = (opp.title or "").lower()
        provider = (opp.provider or "").lower()
        competitive = ["daad", "fulbright", "chevening", "rhodes", "gates"]
        if any(c in title or c in provider for c in competitive):
            return "High"
        if opp.match_score >= 70:
            return "Medium"
        return "Low"

    def _assess_suitability(self, academic, language, experience, funding, degree) -> str:
        matches = [academic, language, experience, funding, degree]
        excellent = sum(1 for m in matches if m == "Excellent Match")
        good = sum(1 for m in matches if m in ("Excellent Match", "Good Match"))
        missing = sum(1 for m in matches if "Missing" in m)
        fail = sum(1 for m in matches if m == "Does Not Match")

        if excellent >= 2 and fail == 0:
            return "Highly Suitable"
        if good >= 3 and fail == 0:
            return "Suitable"
        if missing >= 2:
            return "Needs More Information"
        if fail >= 2:
            return "Low Suitability"
        return "Moderately Suitable"

    def _assess_confidence(self, opp: InternalOpportunity) -> str:
        v = opp.verification or {}
        status = v.get("status", "")
        conf = v.get("confidence", "Low")
        if "Verified" in status or "Live" in status:
            return conf if conf in ("High", "Medium") else "High"
        return "Low"

    def _assess_risk(self, eligible: bool, partial: int, failed: int, opp: InternalOpportunity) -> str:
        if not eligible and failed >= 2:
            return "High"
        if partial >= 2:
            return "Medium"
        if eligible:
            return "Low"
        return "Medium"

    def _overall_recommendation(
        self, academic, language, experience, funding, eligible, partial, failed
    ) -> str:
        if eligible and academic in ("Excellent Match", "Good Match"):
            return "Strongly Recommended"
        if eligible:
            return "Recommended"
        if partial >= 1 and failed == 0:
            return "Possible but Competitive"
        if "Missing" in language:
            return "Apply After Language Test"
        if failed >= 2:
            return "Consider Alternatives"
        return "Review Carefully"

    def _why_recommended(self, profile: Dict, opp: InternalOpportunity, rec: str) -> str:
        parts = []
        if profile.get("target_country") and opp.country:
            if profile["target_country"].lower() in opp.country.lower():
                parts.append(f"Matches your target country ({opp.country})")
        if profile.get("field") and opp.title:
            field = profile["field"].lower()
            if field in opp.title.lower() or field in (opp.description or "").lower():
                parts.append(f"Aligns with your field of study ({profile['field']})")
        if rec == "Strongly Recommended":
            parts.append("Your profile meets key eligibility criteria")
        return "; ".join(parts) if parts else "Based on available verified data"

    def _why_not_fit(self, checks: List[Dict], eligible: bool) -> Optional[str]:
        if eligible:
            return None
        reasons = []
        for c in checks:
            if c.get("status") == "FAIL":
                reasons.append(f"{c.get('criterion')}: {c.get('note', 'Does not meet requirement')}")
            elif c.get("status") == "PARTIAL":
                reasons.append(f"{c.get('criterion')}: {c.get('note', 'Slightly below requirement')}")
        return "; ".join(reasons) if reasons else None

    def _build_overview(self, opp: InternalOpportunity, verified: Dict) -> str:
        desc = opp.description or ""
        if len(desc) > 200:
            desc = desc[:200] + "..."
        provider = opp.provider or "Unknown provider"
        country = opp.country or "International"
        return f"{opp.title} offered by {provider} in {country}. {desc}".strip()


decision_engine = DecisionEngine()
