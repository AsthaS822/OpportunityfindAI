from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class EligibilityAnalysisSchema(BaseModel):
    academic_match: Optional[str] = None
    language_match: Optional[str] = None
    experience_match: Optional[str] = None
    funding_match: Optional[str] = None
    degree_match: Optional[str] = None


class DecisionAnalysisSchema(BaseModel):
    eligibility: Optional[str] = None
    suitability: Optional[str] = None
    difficulty: Optional[str] = None
    confidence: Optional[str] = None
    recommendation: Optional[str] = None
    risk: Optional[str] = None
    overall_recommendation: Optional[str] = None
    why_recommended: Optional[str] = None
    why_not_fit: Optional[str] = None
    overview: Optional[str] = None
    who_can_apply: Optional[str] = None
    required_qualification: Optional[str] = None
    minimum_cgpa: Optional[str] = None
    required_experience: Optional[str] = None
    documents_required: Optional[str] = None
    funding_details: Optional[Dict[str, Any]] = None
    application_process: Optional[str] = None
    selection_process: Optional[str] = None
    application_fees: Optional[str] = None
    official_deadline: Optional[str] = None
    official_source: Optional[str] = None
    verified_date: Optional[str] = None
    application_link: Optional[str] = None
    status: Optional[str] = None
    eligibility_analysis: Optional[EligibilityAnalysisSchema] = None


class OpportunitySchema(BaseModel):
    id: Optional[str] = None
    title: str
    provider: str
    country: Optional[str] = None
    category: str
    degree: Optional[str] = None
    funding_type: Optional[str] = None
    deadline: Optional[str] = None
    eligibility: Optional[str] = None
    description: Optional[str] = None
    official_url: Optional[str] = None
    verification: Dict[str, Any] = Field(default_factory=dict)
    source_type: str = "Dataset Only"
    dataset_deadline: Optional[str] = None
    live_deadline: Optional[str] = None
    using_deadline: Optional[str] = None
    dataset_ranking: Optional[str] = None
    live_ranking: Optional[str] = None
    match_score: Optional[float] = None
    decision_analysis: Optional[DecisionAnalysisSchema] = None
    eligibility_checks: Optional[Dict[str, Any]] = None
    next_steps: Optional[List[str]] = None
