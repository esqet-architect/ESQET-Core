"""
ESQET Operator - Clean implementation
DOI: 10.5281/zenodo.20072372
Parameter closure ready
"""
import numpy as np

class ESQETOperator:
    """Observer state update with tanh nonlinearity"""
    
    def __init__(self, gain=1.0, delta=0.01, lambd=0.001):
        self.gain = gain          # g parameter
        self.delta = delta        # δ learning rate
        self.lambd = lambd        # λ regularization
        
    def predict(self, S_prev):
        """Current prediction is just previous state"""
        return S_prev
    
    def update(self, S_prev, y_meas):
        """Update observer state using ESQET equation:
        S_t = S_{t-1} + δ * tanh(g * e_t)
        where e_t = y_t - S_{t-1}
        """
        e_t = y_meas - S_prev
        S_new = S_prev + self.delta * np.tanh(self.gain * e_t)
        return S_new
    
    def loss(self, errors):
        """Regularized loss: ℒ = 𝔼[e²] + λg²"""
        mse = np.mean(np.array(errors)**2)
        return mse + self.lambd * (self.gain**2)


def run_parameter_closure(g_values, signal, delta=0.01, lambd=0.001):
    """Sweep over gain values to find optimal g"""
    results = []
    
    print(f"\n{'='*50}")
    print(f"ESQET Parameter Closure Campaign")
    print(f"DOI: 10.5281/zenodo.20072372")
    print(f"{'='*50}\n")
    print(f"λ = {lambd}, δ = {delta}")
    print(f"Testing {len(g_values)} gain values...\n")
    
    for g in g_values:
        op = ESQETOperator(gain=g, delta=delta, lambd=lambd)
        errors = []
        S_t = 0.0
        
        for y in signal:
            S_t = op.update(S_t, y)
            e = y - S_t
            errors.append(e)
        
        loss_val = op.loss(errors)
        results.append(loss_val)
        print(f"  g = {g:.4f} → ℒ = {loss_val:.6f}")
    
    # Find optimal
    opt_idx = np.argmin(results)
    opt_g = g_values[opt_idx]
    min_loss = results[opt_idx]
    
    print(f"\n{'='*50}")
    print(f"✓ OPTIMAL PARAMETER: g* = {opt_g:.4f}")
    print(f"  Minimum loss: {min_loss:.6f}")
    print(f"{'='*50}\n")
    
    return opt_g, results


if __name__ == "__main__":
    # Generate test signal with φ-scale symmetry
    np.random.seed(42)
    t = np.linspace(0, 50, 1000)
    phi = (1 + 5**0.5) / 2  # Golden ratio
    
    # Signal: phi-frequency oscillation + noise
    signal = np.sin(2 * np.pi * t / phi) + 0.1 * np.random.randn(len(t))
    
    # Sweep over gain values
    g_range = np.linspace(0.01, 3.0, 30)
    
    opt_g, losses = run_parameter_closure(g_range, signal, delta=0.05, lambd=0.01)
    
    # Append to PARAMETERS.md
    with open("PARAMETERS.md", "a") as f:
        f.write(f"\n| g | {opt_g:.4f} | Loss minimization | φ-scaled signal | {min(losses):.6f} |")
    
    print("✓ Closure record appended to PARAMETERS.md")
