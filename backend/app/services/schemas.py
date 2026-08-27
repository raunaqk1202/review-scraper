from pydantic import BaseModel, Field
from typing import List
from app.models.enums import JourneyStage

class SignalExtracted(BaseModel):
    summary: str = Field(..., description="A concise 1-2 sentence summary of the specific behavior, barrier, or unmet need.")
    journey_stage: JourneyStage = Field(..., description="The stage of the shopping journey this signal belongs to (e.g. WISHLIST, PURCHASE_POSTPONEMENT, COMPARISON).")
    signal_type: str = Field(..., description="The type of signal (e.g., 'BARRIER', 'UNMET_NEED', 'COMPARISON_BEHAVIOR', 'SOCIAL_VALIDATION').")
    evidence_quote: str = Field(..., description="The exact verbatim quote from the text that proves this signal.")

class NoiseReductionResult(BaseModel):
    is_relevant: bool = Field(..., description="True if the text contains genuine discussion about shopping psychology, wishlist behavior, sizing, fit, comparison, or purchase postponement. False if it is spam, a generic bug report, or irrelevant.")
    reason: str = Field(..., description="Reasoning for why it is relevant or irrelevant.")

class SignalExtractionResult(BaseModel):
    signals: List[SignalExtracted] = Field(..., description="List of deeply analyzed behavioral signals extracted from the text. Can be empty if no specific insights are found.")

class OpportunityScoringResult(BaseModel):
    """LLM-generated scores for an opportunity, each rated 1.0–5.0."""
    user_pain: float = Field(
        ..., ge=1.0, le=5.0,
        description="How severe is this problem for users? 1=minor inconvenience, 5=critical blocker preventing purchase."
    )
    business_impact: float = Field(
        ..., ge=1.0, le=5.0,
        description="How much could solving this affect conversion, revenue, or retention? 1=negligible, 5=major revenue driver."
    )
    reach: float = Field(
        ..., ge=1.0, le=5.0,
        description="How widespread is this problem across the user base? 1=very niche, 5=affects most users."
    )
    evidence_strength: float = Field(
        ..., ge=1.0, le=5.0,
        description="How confident are we in this finding? 1=single anecdotal mention, 5=consistent pattern across multiple sources."
    )
