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
    __tablename__ = "opportunity_score"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    opportunity_id = Column(String(36), ForeignKey("opportunity.id"), nullable=False, unique=True)
    
    reach = Column(Float)
    frequency = Column(Float)
    severity = Column(Float)
    business_impact = Column(Float)
    evidence_strength = Column(Float)
    cross_source_consistency = Column(Float)
    cross_segment_relevance = Column(Float)
    trend_score = Column(Float)
    strategic_relevance = Column(Float)
    
    composite_score = Column(Float)
    dimension_weights = Column(SQLiteJSON)
    scored_at = Column(DateTime, default=datetime.utcnow)

    opportunity = relationship("Opportunity", back_populates="score")
    
    __table_args__ = (
        Index("idx_opp_score_composite", "composite_score"),
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
