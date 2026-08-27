import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class Opportunity(Base):
    __tablename__ = "opportunity"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    user_segment = Column(String(100))
    context = Column(Text)
    behavior = Column(Text)
    barrier = Column(Text)
    unmet_need = Column(Text)
    potential_solution = Column(Text)
    potential_business_impact = Column(Text)
    
    evidence_level = Column(String(50))
    supporting_conversations = Column(Integer, default=0)
    independent_sources = Column(Integer, default=0)
    source_platforms = Column(SQLiteJSON)
    time_period = Column(String(100))
    
    supporting_evidence = Column(SQLiteJSON)
    contradictory_evidence = Column(SQLiteJSON)
    
    confidence_level = Column(Float)
    generated_at = Column(DateTime, default=datetime.utcnow)

    score = relationship("OpportunityScore", back_populates="opportunity", uselist=False, cascade="all, delete-orphan")
    evidences = relationship("OpportunityEvidence", back_populates="opportunity", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_opp_evidence_confidence", "evidence_level", "confidence_level"),
    )

class OpportunityScore(Base):
    """
    Scoring model using weighted multi-factor formula:
    Score = 35% × User Pain + 30% × Business Impact + 20% × Reach + 15% × Evidence Strength

    Each dimension is rated 1.0–5.0 by the LLM.
    Composite score is 0–100: (7 × Pain) + (6 × Impact) + (4 × Reach) + (3 × Evidence)
    Max = 7×5 + 6×5 + 4×5 + 3×5 = 100
    """
    __tablename__ = "opportunity_score"

    # Scoring weights: multipliers that produce a 0–100 composite
    SCORING_WEIGHTS = {
        "user_pain": 7,        # 35% weight (7/20)
        "business_impact": 6,  # 30% weight (6/20)
        "reach": 4,            # 20% weight (4/20)
        "evidence_strength": 3 # 15% weight (3/20)
    }

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String(36), ForeignKey("opportunity.id"), nullable=False, unique=True)
    
    user_pain = Column(Float)           # 1.0–5.0: Severity of user frustration/barrier
    business_impact = Column(Float)     # 1.0–5.0: Potential effect on conversion/revenue
    reach = Column(Float)               # 1.0–5.0: How widespread the problem is
    evidence_strength = Column(Float)   # 1.0–5.0: Confidence in the finding
    
    composite_score = Column(Float)     # 0–100: Weighted composite
    dimension_weights = Column(SQLiteJSON)
    scored_at = Column(DateTime, default=datetime.utcnow)

    opportunity = relationship("Opportunity", back_populates="score")
    
    __table_args__ = (
        Index("idx_opp_score_composite", "composite_score"),
    )

    @classmethod
    def compute_composite_score(cls, user_pain: float, business_impact: float,
                                 reach: float, evidence_strength: float) -> float:
        """Compute the 0–100 composite score from four 1.0–5.0 dimension ratings."""
        w = cls.SCORING_WEIGHTS
        return (
            w["user_pain"] * user_pain +
            w["business_impact"] * business_impact +
            w["reach"] * reach +
            w["evidence_strength"] * evidence_strength
        )

class OpportunityEvidence(Base):
    __tablename__ = "opportunity_evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String(36), ForeignKey("opportunity.id"), nullable=False)
    pattern_id = Column(String(36), ForeignKey("pattern.id"))
    feedback_item_id = Column(String(36), ForeignKey("feedback_item.id"))
    
    evidence_type = Column(String(50))
    evidence_level = Column(String(50))
    evidence_text = Column(Text)
    source_reference = Column(Text)

    opportunity = relationship("Opportunity", back_populates="evidences")
    pattern = relationship("Pattern", back_populates="opportunity_evidences")
