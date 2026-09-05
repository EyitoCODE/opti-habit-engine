"""
Opti-Habit Engine: SQLAlchemy Data Models

Defines relational database schemas for habit entities, momentum metrics,
and computer vision proof-of-work completion logs.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.database import Base

class Habit(Base):
    """
    Represents an ongoing habit, tracking difficulty weighting,
    current compounded momentum, and last completion timestamp.
    """
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    # Weight acts as the asymptotic target score representing task difficulty (W > 0).
    weight = Column(Float, default=1.0, nullable=False)
    current_momentum = Column(Float, default=0.0, nullable=False)
    last_completed = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Establish one-to-many relationship with execution audit records.
    logs = relationship("CompletionLog", back_populates="habit", cascade="all, delete-orphan")

class CompletionLog(Base):
    """
    Audit log recording each habit verification event,
    recording whether hardware computer vision verification was completed.
    """
    __tablename__ = "completion_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    cv_verified = Column(Boolean, default=False, nullable=False)
    momentum_after = Column(Float, default=0.0, nullable=False)

    habit = relationship("Habit", back_populates="logs")