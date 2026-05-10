"""ESQET Core Operator - Unity Resonance"""
import numpy as np

class ESQETOperator:
    """Unity Resonance Observer (g=1, δ=1 after parameter closure)"""
    
    def __init__(self, gain=1.0, delta=1.0, lambd=0.001):
        self.gain = gain
        self.delta = delta
        self.lambd = lambd
        self.S = 0.0
        self.errors = []
    
    def update(self, y_meas):
        """S_t = S_{t-1} + δ * tanh(g * (y_t - S_{t-1}))"""
        e = y_meas - self.S
        self.S = self.S + self.delta * np.tanh(self.gain * e)
        self.errors.append(e)
        return self.S
    
    def loss(self):
        mse = np.mean(np.array(self.errors)**2)
        return mse + self.lambd * (self.gain**2)
    
    def reset(self):
        self.S = 0.0
        self.errors = []

def unity_observer(S_prev, y_meas):
    """Simplified Unity Resonance (g=1, δ=1) - zero free parameters"""
    return S_prev + np.tanh(y_meas - S_prev)
