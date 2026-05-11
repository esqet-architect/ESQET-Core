import numpy as np

# Constants from your Master Equation
C_ALPHA = 0.5
LAMBDA_STERILE = 0.01

class SystemHealth:
    def __init__(self):
        self.history = []

    def compute_coherence(self, grad_energy, field_energy):
        # Your equation from REAL_APPLICATIONS.md
        return (C_ALPHA * grad_energy) - (LAMBDA_STERILE * field_energy)

    def check_recursive_loops(self, current_state):
        self.history.append(current_state)
        if len(self.history) > 10:
            # Check if current state matches the state 5 ticks ago
            if abs(self.history[-1] - self.history[-5]) < 0.001:
                return True
        return False

# Quick test of your new logic
monitor = SystemHealth()
coherence = monitor.compute_coherence(0.85, 0.12)
is_looping = monitor.check_recursive_loops(coherence)

print(f"[*] System Coherence: {coherence:.4f}")
print(f"[*] Recursive Loop detected: {is_looping}")
