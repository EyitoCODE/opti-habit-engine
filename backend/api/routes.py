"""
Opti-Habit Engine: API Route Controllers

Orchestrates REST endpoints for habit management, automated decay calculation,
computer vision verification, and persistence logging.
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.cv_verifier import HardwareVerifier
from core.ema_algorithm import MomentumEngine
from db.database import get_db
from db.models import Habit, CompletionLog

router = APIRouter(prefix="/api/habits", tags=["Habits"])

cv_system = HardwareVerifier()
math_engine = MomentumEngine(alpha=0.15, decay_rate=0.05)

# Pydantic data transfer schemas for validation
class HabitCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    weight: float = Field(default=1.0, gt=0.0, description="Task difficulty target score")

class HabitResponse(BaseModel):
    id: int
    title: str
    weight: float
    current_momentum: float
    last_completed: datetime

    class Config:
        from_attributes = True

class VerificationResponse(BaseModel):
    habit_id: int
    status: str
    previous_momentum: float
    new_momentum_score: float
    cv_verified: bool

@router.get("/", response_model=List[HabitResponse])
def get_all_habits(db: Session = Depends(get_db)):
    """
    Fetches all habit records, calculating passive exponential decay
    based on elapsed time since each habit's last completed event.
    """
    habits = db.query(Habit).all()
    now = datetime.utcnow()
    for habit in habits:
        decayed = math_engine.calculate_decay(habit.current_momentum, habit.last_completed, now)
        if decayed != habit.current_momentum:
            habit.current_momentum = decayed
            db.add(habit)
    db.commit()
    return habits

@router.post("/", response_model=HabitResponse, status_code=status.HTTP_201_CREATED)
def create_habit(payload: HabitCreate, db: Session = Depends(get_db)):
    """
    Creates and registers a new habit entity with specified target difficulty weight.
    """
    new_habit = Habit(
        title=payload.title,
        weight=payload.weight,
        current_momentum=0.0,
        last_completed=datetime.utcnow()
    )
    db.add(new_habit)
    db.commit()
    db.refresh(new_habit)
    return new_habit

@router.post("/{habit_id}/verify", response_model=VerificationResponse)
def verify_habit_hardware(habit_id: int, db: Session = Depends(get_db)):
    """
    Executes OpenCV hardware verification. If authenticated, updates the momentum
    score via the EMA formula and persists an audit log entry.
    """
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit record not found.")

    # 1. Run physical verification routine
    is_verified = cv_system.verify_physical_task(scan_duration=10)
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hardware verification failed: Object was not detected."
        )

    # 2. Factor decay into current momentum before appending positive compounding
    now = datetime.utcnow()
    active_momentum = math_engine.calculate_decay(habit.current_momentum, habit.last_completed, now)
    new_momentum = math_engine.log_completion(active_momentum, habit.weight)

    prev_momentum = habit.current_momentum
    habit.current_momentum = new_momentum
    habit.last_completed = now

    # 3. Create persistent audit log
    log = CompletionLog(
        habit_id=habit.id,
        timestamp=now,
        cv_verified=True,
        momentum_after=new_momentum
    )
    db.add(habit)
    db.add(log)
    db.commit()

    return VerificationResponse(
        habit_id=habit.id,
        status="Verification Successful",
        previous_momentum=prev_momentum,
        new_momentum_score=new_momentum,
        cv_verified=True
    )