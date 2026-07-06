"""
STEP 15: Estimate Acceptance Chance (Rule-based, not random)
STEPS 12 & 16: Suggest Alternatives

Provides realistic acceptance probability and suggests viable alternatives.
"""

from typing import Dict, List, Any
from ..models.opportunity import InternalOpportunity
from ..utils.logger import get_logger

logger = get_logger(__name__)

class ChanceEstimator:
    """
    Estimates acceptance probability based on user profile and opportunity.
    Uses rule-based scoring, never random.
    """
    
    def estimate_chance(self, user_profile: Dict[str, Any], eligibility_check: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate probability of getting admitted/selected.
        
        Returns:
        {
            "probability": float (0-100),
            "category": "High" | "Moderate" | "Low" | "Very Low",
            "reasoning": "Human-readable explanation",
            "factors": [list of factors affecting chance]
        }
        """
        
        score = 50  # Base score
        factors = []
        
        match_score = eligibility_check.get("match_score", 0)
        checks = eligibility_check.get("checks", [])
        
        # Factor 1: Academic Match (40 points max)
        academic_check = next((c for c in checks if "Academic" in c.get("criterion", "")), None)
        if academic_check:
            if academic_check.get("status") == "PASS":
                difference = academic_check.get("difference", 0)
                if difference >= 5:
                    score += 40
                    factors.append("Strong academic profile (exceeds minimum by significant margin)")
                elif difference >= 2:
                    score += 30
                    factors.append("Solid academic profile (exceeds minimum)")
                else:
                    score += 20
                    factors.append("Meets minimum academic requirement")
            elif academic_check.get("status") == "PARTIAL":
                score += 10
                factors.append("Slightly below academic requirement (may still be considered)")
            else:
                score -= 20
                factors.append("Below minimum academic requirement (significant disadvantage)")
        
        # Factor 2: Degree Match (20 points max)
        degree_check = next((c for c in checks if "Degree" in c.get("criterion", "")), None)
        if degree_check and degree_check.get("status") == "PASS":
            score += 20
            factors.append("Degree level matches requirement perfectly")
        
        # Factor 3: English Proficiency (15 points max)
        english_check = next((c for c in checks if "English" in c.get("criterion", "")), None)
        if english_check:
            if english_check.get("status") == "PASS":
                score += 15
                factors.append("English proficiency verified")
            elif english_check.get("status") == "FAIL":
                score -= 15
                factors.append("English proficiency missing (critical requirement)")
        
        # Factor 4: Experience (15 points max) - if required
        exp_check = next((c for c in checks if "Experience" in c.get("criterion", "")), None)
        if exp_check:
            if exp_check.get("status") == "PASS":
                score += 15
                factors.append("Relevant work experience present")
            elif exp_check.get("status") == "PARTIAL":
                score += 5
                factors.append("Some relevant work experience")
        
        # Factor 5: Competitiveness Adjustment
        # Highly competitive scholarships have lower acceptance rates
        if match_score >= 90:
            score += 10
            factors.append("Strong overall match with opportunity")
        elif match_score >= 70:
            factors.append("Good match with opportunity")
        elif match_score >= 50:
            factors.append("Moderate match with opportunity")
        else:
            score -= 10
            factors.append("Weak match with opportunity")
        
        # Clamp score between 0-100
        probability = max(0, min(100, score))
        
        # Categorize
        if probability >= 80:
            category = "High"
        elif probability >= 60:
            category = "Moderate"
        elif probability >= 40:
            category = "Low"
        else:
            category = "Very Low"
        
        return {
            "probability": probability,
            "category": category,
            "reasoning": self._generate_reasoning(probability, category),
            "factors": factors,
        }
    
    def _generate_reasoning(self, probability: float, category: str) -> str:
        """Generate reasoning for the probability estimate."""
        
        if category == "High":
            return f"Based on your profile, you have a {probability:.0f}% chance of acceptance. Your qualifications are strong and competitive."
        elif category == "Moderate":
            return f"Based on your profile, you have a {probability:.0f}% chance of acceptance. Your qualifications are decent, but there's room for improvement."
        elif category == "Low":
            return f"Based on your profile, you have a {probability:.0f}% chance of acceptance. You may face stiff competition. Consider strengthening weak areas."
        else:
            return f"Based on your profile, you have a {probability:.0f}% chance of acceptance. Direct acceptance is unlikely, but don't lose hope—explore alternatives or strengthen your application."

class AlternativeSuggester:
    """
    Suggests alternative opportunities when user is not eligible for their first choice.
    STEP 12: Suggest alternatives due to low eligibility
    STEP 16: Suggest similar opportunities with better acceptance chances
    """
    
    COUNTRY_GROUPS = {
        "Germany": ["Netherlands", "Austria", "Belgium", "Switzerland"],
        "UK": ["Ireland", "Germany", "Netherlands"],
        "US": ["Canada", "Australia"],
        "Australia": ["New Zealand", "Singapore"],
        "Japan": ["South Korea", "Taiwan"],
        "India": ["Bangladesh", "Sri Lanka"],
    }
    
    def suggest_alternatives(self, 
        user_profile: Dict[str, Any],
        opportunities: List[InternalOpportunity],
        not_eligible_for: InternalOpportunity = None
    ) -> List[Dict[str, Any]]:
        """
        Suggest alternative opportunities based on user's profile.
        
        Strategies:
        1. If wanted Germany but academic score is low → suggest Netherlands, Austria
        2. If wanted Master's but score is low → suggest Bachelor's with scholarship
        3. If no result for paid internship → suggest government schemes
        4. If scholarship closed → suggest education loans
        5. Similar opportunities with higher acceptance chance
        """
        
        alternatives = []
        user_degree = user_profile.get("target_degree")
        user_country = user_profile.get("target_country")
        user_marks = user_profile.get("marks", {}) or {}
        user_percentage = user_marks.get("percentage", 0)
        
        # STRATEGY 1: Same degree, different country (STEPS 12)
        if not_eligible_for and user_country:
            similar_countries = self.COUNTRY_GROUPS.get(user_country, [])
            country_alternatives = [
                opp for opp in opportunities
                if opp.country in similar_countries and opp.degree == user_degree
            ]
            for opp in country_alternatives[:3]:  # Top 3
                alternatives.append({
                    "type": "Geographic Alternative",
                    "opportunity": opp,
                    "reason": f"Similar to {user_country} but may have easier admission requirements",
                    "advantage": "Better acceptance chances while maintaining quality education",
                })
        
        # STRATEGY 2: Lower degree level if marks are low (STEP 12)
        if user_percentage and user_percentage < 60:
            degree_progression = {
                "Master's": ["Bachelor's", "Diploma"],
                "PhD": ["Master's"],
                "MBA": ["Bachelor's", "Diploma"],
            }
            lower_degrees = degree_progression.get(user_degree, [])
            lower_degree_opps = [
                opp for opp in opportunities
                if opp.degree in lower_degrees
            ]
            for opp in lower_degree_opps[:2]:
                alternatives.append({
                    "type": "Degree Level Alternative",
                    "opportunity": opp,
                    "reason": "Lower degree level may have less stringent requirements",
                    "advantage": f"Build stronger foundation before pursuing {user_degree}",
                })
        
        # STRATEGY 3: Government schemes if no international scholarships (STEP 12)
        if user_profile.get("is_domestic"):
            govt_schemes = [
                opp for opp in opportunities
                if "scheme" in opp.category.lower() or "government" in opp.provider.lower()
            ]
            for opp in govt_schemes[:2]:
                alternatives.append({
                    "type": "Government Scheme",
                    "opportunity": opp,
                    "reason": "Government schemes often have higher success rates for domestic candidates",
                    "advantage": "Specifically designed for Indian applicants",
                })
        
        # STRATEGY 4: Education Loans if scholarships not viable
        loan_opps = [opp for opp in opportunities if "loan" in opp.category.lower()]
        if not_eligible_for and loan_opps:
            for opp in loan_opps[:1]:
                alternatives.append({
                    "type": "Education Loan Alternative",
                    "opportunity": opp,
                    "reason": "Education loans available even without perfect eligibility",
                    "advantage": "No merit-based requirements, based on institution and course",
                })
        
        # STRATEGY 5: Similar opportunities with better match (STEP 16)
        stream = user_profile.get("stream")
        if stream:
            similar_stream_opps = [
                opp for opp in opportunities
                if stream.lower() in opp.category.lower() or stream.lower() in opp.title.lower()
            ]
            for opp in similar_stream_opps[:2]:
                if opp != not_eligible_for:
                    alternatives.append({
                        "type": "Better Match in Same Field",
                        "opportunity": opp,
                        "reason": "Same field of study but potentially better fit for your profile",
                        "advantage": "May have higher acceptance chance",
                    })
        
        # Deduplicate and limit to 5 alternatives
        seen = set()
        unique_alternatives = []
        for alt in alternatives:
            opp_id = alt["opportunity"].id
            if opp_id not in seen:
                seen.add(opp_id)
                unique_alternatives.append(alt)
                if len(unique_alternatives) >= 5:
                    break
        
        logger.info(f"Suggested {len(unique_alternatives)} alternatives for user")
        return unique_alternatives

chance_estimator = ChanceEstimator()
alternative_suggester = AlternativeSuggester()
