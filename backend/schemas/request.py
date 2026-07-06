from pydantic import BaseModel, Field
from typing import Optional


class DiscoverRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="The search query from the user")
    language: str = Field("en", pattern="^(en|hi)$", description="Response language: en or hi")
    session_id: Optional[str] = Field("default", max_length=64, description="Session ID for context memory")
