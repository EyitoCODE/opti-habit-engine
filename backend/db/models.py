from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    weight = Column(Float, default=1.0)  # Represents physical/computational difficulty
    current_momentum = Column(Float, default=0.0)
    last_completed = Column(DateTime, default=datetime.utcnow)

class CompletionLog(Base):
    __tablename__ = "completion_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    cv_verified = Column(Boolean, default=False)  # True if validated by OpenCV