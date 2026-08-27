from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class OpportunityScoreResponse(BaseModel):
    user_pain: Optional[float] = None
    business_impact: Optional[float] = None
    reach: Optional[float] = None
    evidence_strength: Optional[float] = None
    composite_score: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)

class OpportunityResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    barrier: Optional[str] = None
    unmet_need: Optional[str] = None
    supporting_conversations: int
    score: Optional[OpportunityScoreResponse] = None
    
    model_config = ConfigDict(from_attributes=True)

class AISignalResponse(BaseModel):
    id: str
    journey_stage: Optional[str] = None
    signal_type: Optional[str] = None
    summary: Optional[str] = None
    evidence_quote: Optional[str] = None
    confidence_score: Optional[float] = None
    
    model_config = ConfigDict(from_attributes=True)
