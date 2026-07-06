"""
REASONING ENGINE — eligibility reasoning, multi-factor ranking, estimated fit, categories.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from ..models.opportunity import InternalOpportunity
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ReasoningEngine:
    """Richer reasoning: estimated fit, competition, difficulty, categorization."""

    def categorize_recommendations(self, opportunities: List[InternalOpportunity], user_profile: Dict) -> Dict:
        if not opportunities:
            return {"best_choice": None, "safe_option": None, "dream_option": None, "backup_option": None, "others": []}

        ranked = sorted(opportunities, key=lambda x: x.match_score or 0, reverse=True)
        result = {"best_choice": None, "safe_option": None, "dream_option": None, "backup_option": None, "others": []}

        for opp in ranked:
            score = opp.match_score or 0
            funding = (opp.funding_type or "").lower()
            deadline_ok = self._deadline_active(opp.deadline)

            if score >= 75 and deadline_ok and ("fully" in funding or "full" in funding):
                if not result["dream_option"]:
                    result["dream_option"] = opp
                    continue
            if score >= 60 and deadline_ok:
                if not result["best_choice"]:
                    result["best_choice"] = opp
                    continue
            if score >= 40 and deadline_ok:
                if not result["safe_option"]:
                    result["safe_option"] = opp
                    continue
            if score >= 20:
                if not result["backup_option"]:
                    result["backup_option"] = opp
                    continue
            result["others"].append(opp)

        return result

    def estimate_chance(self, user_profile: Dict, opportunity: InternalOpportunity) -> Dict:
        """Estimated Fit — Excellent / Good / Moderate / Weak. Never predict acceptance."""
        score = opportunity.match_score or 0
        reasons = []
        gaps = []
        fit_level = "weak"

        if score >= 75:
            fit_level = "excellent"
            reasons.append("Strong alignment with your academic background")
        elif score >= 50:
            fit_level = "good"
            reasons.append("Good overall match with your profile")
        elif score >= 30:
            fit_level = "moderate"
            reasons.append("Partial alignment — review specific requirements")
        else:
            fit_level = "weak"
            gaps.append("Limited alignment with your profile")

        if user_profile.get("target_country") and opportunity.country:
            if user_profile["target_country"].lower() in opportunity.country.lower():
                reasons.append("Country preference matches")
            else:
                gaps.append(f"Target country {user_profile['target_country']} differs from {opportunity.country}")

        funding = (opportunity.funding_type or "").lower()
        if "fully" in funding:
            reasons.append("Fully funded — covers all expenses")
        elif "partial" in funding:
            reasons.append("Partially funded — may need additional arrangements")

        if "Live Verified" in (opportunity.verification or {}).get("status", ""):
            reasons.append("Officially verified — up-to-date information")

        deadline_str = opportunity.deadline
        if deadline_str and deadline_str != "Unknown":
            try:
                dl = datetime.strptime(deadline_str.strip(), "%Y-%m-%d")
                days_left = (dl - datetime.now()).days
                if 0 < days_left <= 30:
                    reasons.append(f"Deadline approaching — {days_left} days left")
                elif days_left > 30:
                    reasons.append(f"Sufficient time until deadline ({days_left} days)")
            except ValueError:
                pass

        return {
            "fit": fit_level,
            "score": score,
            "reasons": reasons[:3],
            "gaps": gaps[:3],
            "recommendation": self._fit_label(fit_level),
        }

    def estimate_competition(self, opportunity: InternalOpportunity) -> Dict:
        """Estimate competition level based on available data."""
        title = (opportunity.title or "").lower()
        desc = (opportunity.description or "").lower()
        combined = f"{title} {desc}"

        acceptance_rate = None
        if "acceptance" in combined:
            import re
            m = re.search(r'(\d+)[–\-]\d+%', combined) or re.search(r'(\d+)%\s*(?:acceptance|selectivity)', combined)
            if m:
                acceptance_rate = f"{m.group(1)}%"

        competition = "moderate"
        if acceptance_rate:
            rate = int(acceptance_rate.replace("%", ""))
            if rate < 10:
                competition = "very high"
            elif rate < 25:
                competition = "high"
            elif rate < 50:
                competition = "moderate"
            else:
                competition = "low"

        prestigious_keywords = ["prestigious", "competitive", "highly selective", "top", "world-renowned"]
        if any(kw in combined for kw in prestigious_keywords) and competition == "moderate":
            competition = "high"

        difficulty = self._estimate_difficulty(opportunity)

        return {
            "competition": competition,
            "acceptance_rate": acceptance_rate or "Not specified",
            "difficulty": difficulty,
            "preparation_time": self._preparation_time(difficulty),
        }

    def compare_opportunities(self, opp_a: InternalOpportunity, opp_b: InternalOpportunity) -> Dict:
        def safe(o: InternalOpportunity, attr: str) -> str:
            return str(getattr(o, attr, "") or "")

        return {
            "title": f"{opp_a.title} vs {opp_b.title}",
            "comparisons": [
                {"aspect": "Funding", "a": safe(opp_a, "funding_type"), "b": safe(opp_b, "funding_type")},
                {"aspect": "Country", "a": safe(opp_a, "country"), "b": safe(opp_b, "country")},
                {"aspect": "Provider", "a": safe(opp_a, "provider"), "b": safe(opp_b, "provider")},
                {"aspect": "Degree Level", "a": safe(opp_a, "degree"), "b": safe(opp_b, "degree")},
                {"aspect": "Deadline", "a": safe(opp_a, "deadline"), "b": safe(opp_b, "deadline")},
                {"aspect": "Eligibility", "a": safe(opp_a, "eligibility")[:100], "b": safe(opp_b, "eligibility")[:100]},
                {"aspect": "Match Score", "a": f"{opp_a.match_score or 0}%", "b": f"{opp_b.match_score or 0}%"},
            ],
            "recommendation": self._pick_best(opp_a, opp_b),
        }

    def multi_factor_score(self, opportunity: InternalOpportunity, user_profile: Dict) -> float:
        """Richer scoring: similarity + eligibility + funding + freshness + verification + popularity."""
        base = opportunity.match_score or 0

        if "Live Verified" in (opportunity.verification or {}).get("status", ""):
            base += 8

        funding = (opportunity.funding_type or "").lower()
        if "fully" in funding:
            base += 10
        elif "partial" in funding:
            base += 5

        if self._deadline_active(opportunity.deadline):
            base += 5

        if user_profile.get("target_country") and opportunity.country:
            if user_profile["target_country"].lower() in opportunity.country.lower():
                base += 8

        if user_profile.get("target_degree") and opportunity.degree:
            if user_profile["target_degree"].lower() in (opportunity.degree or "").lower():
                base += 8

        return min(base, 100)

    def suggest_alternatives_by_criteria(self, opportunity: InternalOpportunity,
                                          all_opportunities: List[InternalOpportunity],
                                          criteria: str = "provider") -> List[Dict]:
        """Suggest alternatives by same provider, country, funding, or degree."""
        if not opportunity:
            return []
        alternatives = []
        seen_titles = set()

        for opp in all_opportunities:
            if opp.id == opportunity.id:
                continue
            if opp.title in seen_titles:
                continue

            reason = None
            if criteria == "provider" and opp.provider and opportunity.provider:
                if opp.provider.lower() == opportunity.provider.lower():
                    reason = "Same provider offers more options"
            elif criteria == "country" and opp.country and opportunity.country:
                if opp.country.lower() == opportunity.country.lower():
                    reason = "Same country — related opportunity"
            elif criteria == "funding" and opp.funding_type and opportunity.funding_type:
                if opp.funding_type.lower() == opportunity.funding_type.lower():
                    reason = "Similar funding arrangement"
            elif criteria == "degree" and opp.degree and opportunity.degree:
                if opp.degree.lower() == opportunity.degree.lower():
                    reason = "Same degree level — consider both"

            if reason and opp.title not in seen_titles:
                seen_titles.add(opp.title)
                alternatives.append({
                    "opportunity": opp,
                    "reason": reason,
                    "type": criteria,
                    "advantage": f"Alternative {criteria}-based option",
                })

            if len(alternatives) >= 3:
                break

        return alternatives

    def _deadline_active(self, deadline: Optional[str]) -> bool:
        if not deadline or deadline == "Unknown":
            return True
        try:
            dl = datetime.strptime(deadline.strip(), "%Y-%m-%d")
            return dl > datetime.now()
        except ValueError:
            return True

    def _fit_label(self, fit: str) -> str:
        labels = {
            "excellent": "Excellent fit — highly recommended",
            "good": "Good match — review requirements to confirm",
            "moderate": "Possible match — some requirements may need verification",
            "weak": "Limited fit — consider other options",
        }
        return labels.get(fit, "Review eligibility requirements")

    def _estimate_difficulty(self, opp: InternalOpportunity) -> str:
        """Estimate application difficulty based on available data."""
        combined = ((opp.title or "") + " " + (opp.description or "")).lower()
        complex_indicators = ["research proposal", "statement of purpose", "essay", "interview",
                              "recommendation letter", "portfolio", "audition"]
        simple_indicators = ["online application", "simple", "easy", "no application fee",
                             "automatic consideration"]

        complexity_score = 0
        for kw in complex_indicators:
            if kw in combined:
                complexity_score += 2
        for kw in simple_indicators:
            if kw in combined:
                complexity_score -= 1

        if complexity_score >= 4:
            return "high"
        elif complexity_score >= 2:
            return "moderate"
        return "low"

    def _preparation_time(self, difficulty: str) -> str:
        mapping = {
            "high": "2-4 months recommended",
            "moderate": "1-2 months recommended",
            "low": "2-4 weeks sufficient",
        }
        return mapping.get(difficulty, "Varies by program")

    def _pick_best(self, a: InternalOpportunity, b: InternalOpportunity) -> str:
        sa = a.match_score or 0
        sb = b.match_score or 0
        if sa > sb + 10:
            return f"{a.title} is the stronger option based on match score"
        elif sb > sa + 10:
            return f"{b.title} is the stronger option based on match score"
        return "Both are comparable — choose based on your preferences"


reasoning_engine = ReasoningEngine()
