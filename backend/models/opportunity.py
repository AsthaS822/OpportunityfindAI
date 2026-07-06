from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class InternalOpportunity:
    id: str
    title: str
    provider: str
    country: Optional[str]
    category: str
    degree: Optional[str]
    funding_type: Optional[str]
    deadline: Optional[str]
    eligibility: Optional[str]
    description: Optional[str]
    official_url: Optional[str]
    source_dataset: str

    match_score: float = 0.0
    dataset_deadline: Optional[str] = None
    live_deadline: Optional[str] = None
    dataset_ranking: Optional[str] = None
    live_ranking: Optional[str] = None
    verification: Dict[str, Any] = field(default_factory=dict)
    source_type: str = "Dataset Only"
    verified_url: Optional[str] = None
    verified_details: Dict[str, Any] = field(default_factory=dict)
    eligibility_analysis: Optional[Dict[str, Any]] = None
    decision_analysis: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not self.verification:
            self.verification = {
                "status": "Dataset Only",
                "confidence": "Low",
                "source": "Local Dataset",
                "last_checked": None,
            }
