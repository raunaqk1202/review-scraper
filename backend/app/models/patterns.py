import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class Pattern(Base):
    __tablename__ = "pattern"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    pattern_type = Column(String(50))
    evidence_level = Column(String(50))
    
    occurrence_count = Column(Integer, default=0)
    source_count = Column(Integer, default=0)
    user_count = Column(Integer, default=0)
    
    segment_distribution = Column(SQLiteJSON)
    category_distribution = Column(SQLiteJSON)
    time_distribution = Column(SQLiteJSON)
    
    trend_direction = Column(String(50))
    strength_score = Column(Float)
    
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)

    evidences = relationship("PatternEvidence", back_populates="pattern", cascade="all, delete-orphan")
    opportunity_evidences = relationship("OpportunityEvidence", back_populates="pattern")

    __table_args__ = (
        Index("idx_pattern_trend_strength", "trend_direction", "strength_score"),
    )

class PatternEvidence(Base):
    __tablename__ = "pattern_evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pattern_id = Column(String(36), ForeignKey("pattern.id"), nullable=False)
    cluster_id = Column(String(36), ForeignKey("cluster.id"))
    feedback_item_id = Column(String(36), ForeignKey("feedback_item.id"))
    
    evidence_type = Column(String(50))
    evidence_text = Column(Text)

    pattern = relationship("Pattern", back_populates="evidences")
    cluster = relationship("Cluster", back_populates="pattern_evidences")
