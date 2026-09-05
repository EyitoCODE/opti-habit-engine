"""
Opti-Habit Engine: Exponential Moving Average (EMA) & Decay Engine

Implements compounding habit momentum calculation alongside continuous 
time-based degradation models to penalize missed execution intervals.
"""
import math
from datetime import datetime

class MomentumEngine:
    """
    State-free mathematical engine computing compounding returns and time decay.
    
    Formula 1 (Compounding Task Execution):
        M_t = M_{t-1} + alpha * (Weight - M_{t-1})
        
    Formula 2 (Continuous Time-Based Decay):
        M_t = M_{t-1} * e^(-lambda * delta_t)
    """
    def __init__(self, alpha: float = 0.15, decay_rate: float = 0.05):
        """
        alpha: Smoothing coefficient balancing past performance against new execution.
        decay_rate: Lambda parameter determining the steepness of the exponential decay curve.
        """
        self.alpha = alpha 
        self.decay_rate = decay_rate 

    def calculate_decay(self, current_momentum: float, last_completed: datetime, current_time: datetime) -> float:
        """
        Applies exponential decay if the duration since last completion exceeds 24 hours.
        """
        delta_days = (current_time - last_completed).total_seconds() / 86400.0
        
        # Grace period: No degradation penalty within the initial 24 hours.
        if delta_days <= 1.0:
            return current_momentum
            
        # Penalize overdue duration (elapsed time beyond the 24-hour mark).
        overdue_days = delta_days - 1.0
        decayed_momentum = current_momentum * math.exp(-self.decay_rate * overdue_days)
        return max(0.0, round(decayed_momentum, 4))

    def log_completion(self, current_momentum: float, weight: float) -> float:
        """
        Updates the momentum score following a successful task execution,
        progressively moving momentum toward the target weight value.
        """
        new_momentum = current_momentum + self.alpha * (weight - current_momentum)
        return round(new_momentum, 4)