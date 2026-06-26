from fastapi import FastAPI, HTTPException
from core.cv_verifier import HardwareVerifier
from core.ema_algorithm import MomentumEngine

app = FastAPI(title="Opti-Habit Engine API")

# Initialize core systems
cv_system = HardwareVerifier()
math_engine = MomentumEngine(alpha=0.1, decay_rate=0.05)

# Temporary in-memory state (Database integration follows verification testing)
current_user_state = {
    "momentum": 0.0,
    "last_task_weight": 1.5
}

@app.get("/")
def health_check():
    return {"status": "Algorithmic Engine & API Online"}

@app.post("/verify-and-log")
def verify_and_log_task():
    """
    Triggers the CV hardware verification. If successful, updates the EMA algorithm.
    """
    # 1. Trigger Hardware Verification
    is_verified = cv_system.verify_physical_task(scan_duration=10)
    
    if not is_verified:
        raise HTTPException(status_code=400, detail="Hardware verification failed. Task not completed.")
    
    # 2. Trigger Mathematical Engine
    new_momentum = math_engine.log_completion(
        current_momentum=current_user_state["momentum"],
        weight=current_user_state["last_task_weight"]
    )
    
    # Update state
    current_user_state["momentum"] = new_momentum
    
    return {
        "status": "Task Verified Successfully",
        "new_momentum_score": new_momentum,
        "verification_method": "OpenCV Canny Edge Detection"
    }