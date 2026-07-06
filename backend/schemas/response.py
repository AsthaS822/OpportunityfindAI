from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .opportunity import OpportunitySchema


class VerificationMetadata(BaseModel):
    status: str
    sources_checked: int
    official_sources: int


class AlternativeSchema(BaseModel):
    type: str
    title: str
    provider: str
    country: Optional[str] = None
    reason: str
    advantage: str
    official_url: Optional[str] = None


class GroqReasoningSchema(BaseModel):
    reasoning: List[str] = []
    recommendations: List[Dict[str, Any]] = []
    comparison: Optional[str] = None
    roadmap: List[str] = []
    action_checklist: List[str] = []
    preparation_tips: Dict[str, List[str]] = {}
    ai_available: bool = False


class DiscoverResponse(BaseModel):
    query: str
    thinking_steps: List[str]
    summary: str
    roadmap: List[str]
    opportunities: List[OpportunitySchema]
    verification_summary: VerificationMetadata
    official_links: List[str]
    timings: Dict[str, int]
    generated_at: str
    intent: Optional[str] = None
    missing_information: Optional[List[str]] = None
    total_found: Optional[int] = None
    verified_count: Optional[int] = None
    decision_summary: Optional[str] = None
    follow_up_questions: Optional[List[str]] = None
    follow_up_required: bool = False
    ai_explanation_available: bool = True
    alternatives: Optional[List[AlternativeSchema]] = None
    action_checklist: Optional[List[str]] = None
    preparation_tips: Optional[Dict[str, List[str]]] = None
    career_paths: Optional[List[Dict]] = None
    recommendation_categories: Optional[Dict[str, Optional[OpportunitySchema]]] = None
    recommendation_others: Optional[List[OpportunitySchema]] = None
    groq_reasoning: Optional[GroqReasoningSchema] = None
