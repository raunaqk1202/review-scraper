import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.dialects.sqlite import JSON as SQLiteJSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class DataSource(Base):
    __tablename__ = "data_source"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    platform = Column(String(50), nullable=False)
    source_type = Column(String(50), nullable=False)
    description = Column(String(255))
    config = Column(SQLiteJSON)
    last_fetched = Column(DateTime)
    
    feedback_items = relationship("FeedbackItem", back_populates="source", cascade="all, delete-orphan")

class FeedbackItem(Base):
    __tablename__ = "feedback_item"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("data_source.id"), nullable=False)
    original_text = Column(Text, nullable=False)
    cleaned_text = Column(Text)
    content_hash = Column(String(64), nullable=False, unique=True)
    source_platform = Column(String(50), nullable=False)
    source_url = Column(String(512))
    source_date = Column(DateTime)
    thread_id = Column(String(128))
    author_id_anonymized = Column(String(128))
    language = Column(String(10), default="en")
    is_spam = Column(Boolean, default=False)
    is_duplicate = Column(Boolean, default=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)

    source = relationship("DataSource", back_populates="feedback_items")
    signals = relationship("AISignal", back_populates="feedback_item", cascade="all, delete-orphan")
    cluster_memberships = relationship("ClusterMembership", back_populates="feedback_item", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_feedback_platform_date", "source_platform", "source_date"),
    )
