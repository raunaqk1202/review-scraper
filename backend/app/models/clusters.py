import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.db.session import Base

class Cluster(Base):
    __tablename__ = "cluster"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    label = Column(String(100))
    description = Column(Text)
    theme = Column(String(100))
    member_count = Column(Integer, default=0)
    cohesion_score = Column(Float)
    evidence_level = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    memberships = relationship("ClusterMembership", back_populates="cluster", cascade="all, delete-orphan")
    pattern_evidences = relationship("PatternEvidence", back_populates="cluster")

    __table_args__ = (
        Index("idx_cluster_theme", "theme"),
    )

class ClusterMembership(Base):
    __tablename__ = "cluster_membership"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    feedback_item_id = Column(String(36), ForeignKey("feedback_item.id"), nullable=False)
    cluster_id = Column(String(36), ForeignKey("cluster.id"), nullable=False)
    similarity_score = Column(Float)

    feedback_item = relationship("FeedbackItem", back_populates="cluster_memberships")
    cluster = relationship("Cluster", back_populates="memberships")
