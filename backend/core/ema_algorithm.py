import math
from datetime import datetime

class MomentumEngine:
    def __init__(self, alpha=0.1, decay_rate=0.05):
        """
        alpha: Compounding factor (0.1 represents the 1% target trajectory over time)
        decay_rate: The penalty severity for missed intervals
        """
        self.alpha = alpha 
        self.decay_rate = decay_rate 

    def calculate_decay(self, current_momentum: float, last_completed: datetime, current_time: datetime) -> float:
        """Applies exponential decay if the time delta exceeds 24 hours."""
        delta_days = (current_time - last_completed).days
        
        if delta_days <= 1:
            return current_momentum
            
        # Execute mathematical decay: M_t = M_{t-1} * e^(-lambda * delta_t)
        decayed_momentum = current_momentum * math.exp(-self.decay_rate * (delta_days - 1))
        return max(0.0, round(decayed_momentum, 4))

    def log_completion(self, current_momentum: float, weight: float) -> float:
        """Calculates the new compounded momentum score upon task execution."""
        new_momentum = current_momentum + self.alpha * (weight - current_momentum)
        return round(new_momentum, 4)