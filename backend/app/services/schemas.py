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
