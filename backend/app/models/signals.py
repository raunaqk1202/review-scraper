import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Index, Text
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class AISignal(Base):
    __tablename__ = "ai_signal"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_item_id = Column(String(36), ForeignKey("feedback_item.id"), nullable=False)
    
    journey_stage = Column(String(50))
    signal_type = Column(String(50))
    summary = Column(String(255))
    evidence_quote = Column(Text)
    opportunity_theme = Column(String(255))
    confidence_score = Column(Float)
    
    extracted_at = Column(DateTime, default=datetime.utcnow)

    feedback_item = relationship("FeedbackItem", back_populates="signals")

    __table_args__ = (
        Index("idx_ai_signal_journey_type", "journey_stage", "signal_type"),
    )
