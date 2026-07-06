"""
STEP 7: Intelligent Eligibility Checking

Never just reject. Explain why, suggest alternatives for near-misses,
and provide actionable advice.
"""

from typing import Dict, List, Any, Tuple
from ..models.opportunity import InternalOpportunity
from ..utils.logger import get_logger

logger = get_logger(__name__)

class EligibilityChecker:
    """
    Checks if user meets scholarship/opportunity requirements.
    Returns not just yes/no, but detailed explanations and alternatives.
    """
    
    def check_eligibility(self, user_profile: Dict[str, Any], opportunity: InternalOpportunity) -> Dict[str, Any]:
        """
        Check eligibility against opportunity requirements.
        
        Returns:
        {
            "eligible": bool,
            "match_score": float (0-100),
            "reasons": [list of reasons],
            "missing_docs": [list of required but missing items],
            "explanation": "Human-readable explanation",
            "alternatives": [opportunities user might qualify for]
        }
        """
        
        eligibility_checks = []
        
        # STEP 1: Academic Score Check
        academic_check = self._check_academic_score(user_profile, opportunity)
        eligibility_checks.append(academic_check)
        
        # STEP 2: Degree Level Check
        degree_check = self._check_degree_level(user_profile, opportunity)
        eligibility_checks.append(degree_check)
        
        # STEP 3: Country/Nationality Check
        nationality_check = self._check_nationality(user_profile, opportunity)
        eligibility_checks.append(nationality_check)
        
        # STEP 4: English Proficiency Check
        english_check = self._check_english_proficiency(user_profile, opportunity)
        eligibility_checks.append(english_check)
        
        # STEP 5: Work Experience Check (if required)
        experience_check = self._check_experience(user_profile, opportunity)
        eligibility_checks.append(experience_check)
        
        # STEP 6: Age Check (if applicable)
        age_check = self._check_age(user_profile, opportunity)
        eligibility_checks.append(age_check)
        
        # Calculate overall eligibility
        passed_checks = [c for c in eligibility_checks if c["status"] == "PASS"]
        partial_checks = [c for c in eligibility_checks if c["status"] == "PARTIAL"]
        failed_checks = [c for c in eligibility_checks if c["status"] == "FAIL"]
        
        # Decision logic
        is_eligible = len(failed_checks) == 0  # Eligible if no hard failures
        match_score = self._calculate_match_score(passed_checks, partial_checks, failed_checks)
        
        return {
            "opportunity_id": opportunity.id,
            "opportunity_title": opportunity.title,
            "eligible": is_eligible,
            "match_score": match_score,
            "checks": eligibility_checks,
            "passed": len(passed_checks),
            "partial": len(partial_checks),
            "failed": len(failed_checks),
            "explanation": self._generate_explanation(
                user_profile, opportunity, passed_checks, partial_checks, failed_checks
            ),
            "next_steps": self._suggest_next_steps(
                user_profile, opportunity, passed_checks, partial_checks, failed_checks
            ),
        }
    
    def _check_academic_score(self, user_profile: Dict[str, Any], opp: InternalOpportunity) -> Dict[str, Any]:
        """Check if user meets minimum academic requirements."""
        
        user_marks = user_profile.get("marks", {})
        user_cgpa = user_marks.get("cgpa")
        user_percentage = user_marks.get("percentage")
        
        # Parse opportunity requirements from eligibility text
        opp_eligibility = (opp.eligibility or "").lower()
        
        # Try to extract minimum CGPA requirement
        min_cgpa = self._extract_minimum_cgpa(opp_eligibility)
        min_percentage = self._extract_minimum_percentage(opp_eligibility)
        
        if not min_cgpa and not min_percentage:
            return {
                "criterion": "Academic Score",
                "status": "UNKNOWN",
                "details": "No academic requirement specified in opportunity",
                "user_value": f"CGPA: {user_cgpa}, Percentage: {user_percentage}",
            }
        
        # Check against CGPA if we have both
        if user_cgpa and min_cgpa:
            if user_cgpa >= min_cgpa:
                return {
                    "criterion": "Academic Score (CGPA)",
                    "status": "PASS",
                    "required": f">= {min_cgpa}",
                    "user_value": user_cgpa,
                    "difference": user_cgpa - min_cgpa,
                }
            elif user_cgpa >= min_cgpa - 0.3:  # Within 0.3 points
                return {
                    "criterion": "Academic Score (CGPA)",
                    "status": "PARTIAL",
                    "required": f">= {min_cgpa}",
                    "user_value": user_cgpa,
                    "difference": user_cgpa - min_cgpa,
                    "note": f"Short by {min_cgpa - user_cgpa:.1f} points",
                }
            else:
                return {
                    "criterion": "Academic Score (CGPA)",
                    "status": "FAIL",
                    "required": f">= {min_cgpa}",
                    "user_value": user_cgpa,
                    "difference": user_cgpa - min_cgpa,
                    "note": f"Short by {min_cgpa - user_cgpa:.1f} points",
                }
        
        # Check against percentage
        if user_percentage and min_percentage:
            if user_percentage >= min_percentage:
                return {
                    "criterion": "Academic Score (Percentage)",
                    "status": "PASS",
                    "required": f">= {min_percentage}%",
                    "user_value": f"{user_percentage}%",
                    "difference": user_percentage - min_percentage,
                }
            elif user_percentage >= min_percentage - 3:  # Within 3 percentage points
                return {
                    "criterion": "Academic Score (Percentage)",
                    "status": "PARTIAL",
                    "required": f">= {min_percentage}%",
                    "user_value": f"{user_percentage}%",
                    "difference": user_percentage - min_percentage,
                    "note": f"Short by {min_percentage - user_percentage:.0f}%",
                }
            else:
                return {
                    "criterion": "Academic Score (Percentage)",
                    "status": "FAIL",
                    "required": f">= {min_percentage}%",
                    "user_value": f"{user_percentage}%",
                    "difference": user_percentage - min_percentage,
                    "note": f"Short by {min_percentage - user_percentage:.0f}%",
                }
        
        return {
            "criterion": "Academic Score",
            "status": "UNKNOWN",
            "details": "Insufficient information to verify",
        }
    
    def _check_degree_level(self, user_profile: Dict[str, Any], opp: InternalOpportunity) -> Dict[str, Any]:
        """Check if user's education level matches opportunity."""
        
        user_degree = user_profile.get("current_education") or user_profile.get("target_degree")
        opp_degree = opp.degree
        
        if not user_degree or not opp_degree:
            return {
                "criterion": "Degree Level",
                "status": "UNKNOWN",
                "details": "Unable to verify degree requirements",
            }
        
        # Normalize for comparison
        user_deg_lower = user_degree.lower()
        opp_deg_lower = opp_degree.lower()
        
        # Check for exact or compatible match
        if any(term in opp_deg_lower for term in [user_deg_lower.split()[0]]):
            return {
                "criterion": "Degree Level",
                "status": "PASS",
                "required": opp_degree,
                "user_value": user_degree,
            }
        
        # Check if escalation is expected (e.g., Bachelor to Masters)
        escalations = [("bachelor", "master"), ("master", "phd")]
        for lower, upper in escalations:
            if lower in user_deg_lower and upper in opp_deg_lower:
                return {
                    "criterion": "Degree Level",
                    "status": "PASS",
                    "required": opp_degree,
                    "user_value": user_degree,
                    "note": "Natural progression",
                }
        
        return {
            "criterion": "Degree Level",
            "status": "FAIL",
            "required": opp_degree,
            "user_value": user_degree,
            "note": "Degree mismatch",
        }
    
    def _check_nationality(self, user_profile: Dict[str, Any], opp: InternalOpportunity) -> Dict[str, Any]:
        """Check nationality/country restrictions."""
        
        opp_eligibility = (opp.eligibility or "").lower()
        
        # If no restrictions mentioned, assume open
        if "nationality" not in opp_eligibility and "citizen" not in opp_eligibility:
            return {
                "criterion": "Nationality",
                "status": "PASS",
                "details": "No nationality restrictions specified",
            }
        
        # If restricted, check if user's country is allowed
        if "india" in opp_eligibility and user_profile.get("is_domestic"):
            return {
                "criterion": "Nationality",
                "status": "PASS",
                "required": "Indian nationals",
                "user_value": "India",
            }
        
        return {
            "criterion": "Nationality",
            "status": "UNKNOWN",
            "details": "Unable to verify nationality requirements",
        }
    
    def _check_english_proficiency(self, user_profile: Dict[str, Any], opp: InternalOpportunity) -> Dict[str, Any]:
        """Check English language requirements."""
        
        opp_eligibility = (opp.eligibility or "").lower()
        test_scores = user_profile.get("test_scores", {})
        
        # Check if IELTS/TOEFL is required
        if "ielts" not in opp_eligibility and "toefl" not in opp_eligibility:
            return {
                "criterion": "English Proficiency",
                "status": "PASS",
                "details": "No English test required",
            }
        
        # If required but user doesn't have scores
        if not test_scores:
            return {
                "criterion": "English Proficiency",
                "status": "FAIL",
                "required": "IELTS/TOEFL score needed",
                "user_value": "No test scores provided",
                "note": "IELTS or TOEFL is mandatory - take the test",
            }
        
        # Has test scores
        return {
            "criterion": "English Proficiency",
            "status": "PASS",
            "user_value": f"IELTS: {test_scores.get('ielts')} / TOEFL: {test_scores.get('toefl')}",
        }
    
    def _check_experience(self, user_profile: Dict[str, Any], opp: InternalOpportunity) -> Dict[str, Any]:
        """Check work experience requirements."""
        
        opp_eligibility = (opp.eligibility or "").lower()
        user_experience = user_profile.get("work_experience", {})
        
        # Extract minimum experience requirement (e.g., "2 years experience")
        import re
        exp_match = re.search(r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s+)?(?:experience|exp|work)', opp_eligibility)
        
        if not exp_match:
            return {
                "criterion": "Work Experience",
                "status": "UNKNOWN",
                "details": "No specific experience requirement mentioned",
            }
        
        required_years = int(exp_match.group(1))
        user_years = user_experience.get("years", 0)
        
        if user_years >= required_years:
            return {
                "criterion": "Work Experience",
                "status": "PASS",
                "required": f">= {required_years} years",
                "user_value": f"{user_years} years",
            }
        else:
            return {
                "criterion": "Work Experience",
                "status": "PARTIAL" if user_years >= required_years - 1 else "FAIL",
                "required": f">= {required_years} years",
                "user_value": f"{user_years} years",
                "difference": required_years - user_years,
            }
    
    def _check_age(self, user_profile: Dict[str, Any], opp: InternalOpportunity) -> Dict[str, Any]:
        """Check age restrictions if any."""
        
        user_age = user_profile.get("age")
        
        opp_eligibility = (opp.eligibility or "").lower()
        if "age" not in opp_eligibility:
            return {
                "criterion": "Age",
                "status": "PASS" if user_age else "UNKNOWN",
                "details": "No age restriction specified",
            }
        
        if not user_age:
            return {
                "criterion": "Age",
                "status": "UNKNOWN",
                "details": "Age not provided",
            }
        
        return {
            "criterion": "Age",
            "status": "UNKNOWN",
            "details": "Unable to parse age requirements",
        }
    
    def _extract_minimum_cgpa(self, text: str) -> float:
        """Extract minimum CGPA requirement from text."""
        import re
        match = re.search(r'(?:minimum|min)\s+(?:cgpa|gpa)[:\s]*(\d+\.\d+)', text)
        if match:
            return float(match.group(1))
        return None
    
    def _extract_minimum_percentage(self, text: str) -> float:
        """Extract minimum percentage requirement from text."""
        import re
        match = re.search(r'(?:minimum|min).*?(\d+)\s*%', text)
        if match:
            return float(match.group(1))
        return None
    
    def _calculate_match_score(self, passed: List, partial: List, failed: List) -> float:
        """Calculate overall match score (0-100)."""
        total_checks = len(passed) + len(partial) + len(failed)
        if total_checks == 0:
            return 0
        
        score = (len(passed) * 100 + len(partial) * 50) / total_checks
        return round(score, 1)
    
    def _generate_explanation(self, user_profile, opp, passed, partial, failed) -> str:
        """Generate human-readable eligibility explanation."""
        
        if not failed and not partial:
            return f"You meet all eligibility criteria for {opp.title}."
        
        if failed:
            failed_reasons = [f.get("criterion") for f in failed]
            explanation = f"Unfortunately, you don't meet the requirements for {opp.title} because:\n"
            for f in failed:
                explanation += f"  - {f.get('criterion')}: {f.get('note', 'Does not match')}\n"
            return explanation
        
        if partial:
            partial_reasons = [f.get("criterion") for f in partial]
            explanation = f"You're close to qualifying for {opp.title}. You're slightly short on:\n"
            for p in partial:
                explanation += f"  - {p.get('criterion')}: {p.get('note')}\n"
            explanation += "\nConsider strengthening these areas and reapplying."
            return explanation
        
        return "Unable to determine eligibility"
    
    def _suggest_next_steps(self, user_profile, opp, passed, partial, failed) -> List[str]:
        """Suggest actionable next steps."""
        
        steps = []
        
        # If not eligible due to academics
        if any(c.get("criterion") == "Academic Score" for c in failed):
            steps.append("Pursue additional certifications or courses to strengthen academics")
        
        # If needs English test
        if any(c.get("criterion") == "English Proficiency" for c in failed):
            steps.append("Register for IELTS or TOEFL exam")
            steps.append("Aim for IELTS 6.5+ or TOEFL 90+")
        
        # If lacking experience
        if any(c.get("criterion") == "Work Experience" for c in failed):
            steps.append("Gain relevant work experience (internships count)")
        
        # General next steps if eligible
        if not failed:
            steps.append("Gather required documents (transcripts, passport, SOP)")
            steps.append("Write a compelling Statement of Purpose")
            steps.append("Secure recommendation letters from professors")
            steps.append("Submit application before deadline")
        
        return steps

eligibility_checker = EligibilityChecker()
