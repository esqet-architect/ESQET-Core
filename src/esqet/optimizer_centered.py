import numpy as np
from scipy.optimize import differential_evolution
import mpmath as mp

mp.mp.dps = 60
PHI = (mp.mpf(1) + mp.sqrt(5)) / 2
OMEGA = mp.exp(2j * mp.pi / 3)

# Target Masses (MeV)
TARGETS = {'e': 0.510998, 'mu': 105.658, 'tau': 1776.86}

def f_n(n):
    # Mapping n directly to Z3 rotation
    return n * (2 * mp.pi / 3)

def esqet_centered_operator(n, p, lam, alpha):
    """
    n=0: Electron (Negative Exponent)
    n=1: Muon     (Zero Exponent - Fixed Point)
    n=2: Tau      (Positive Exponent)
    """
    # Fix B: Enforce Z3 as a phase-dependent magnitude (Complex Basis)
    phase = OMEGA ** n 
    # Geometric Shutter (Stiffness alpha)
    delta = (mp.re(phase) + 1.5) ** alpha 
    
    # Fix A: Centered Geometric progression
    # mass = scale * (basis ^ centered_index) * modulation
    exponent = (n - 1) * p
    return lam * (PHI ** exponent) * delta

def objective(params):
    p, lam, alpha = [mp.mpf(x) for x in params]
    
    preds = [esqet_centered_operator(n, p, lam, alpha) for n in range(3)]
    
    # Relative Energy Functional
    # Now all three points share equal weight in the normalized space
    error = sum(((preds[i] - TARGETS[k]) / TARGETS[k])**2 
                for i, k in enumerate(['e', 'mu', 'tau']))
            
    return float(mp.sqrt(error))

if __name__ == "__main__":
    # Bounds for Centered Spectral Search
    # lam is now the Muon-scale anchor (~100 MeV)
    bounds = [(4.0, 10.0), (50.0, 150.0), (0.1, 3.0)]
    
    result = differential_evolution(objective, bounds, tol=1e-18)
    p_opt, l_opt, a_opt = result.x
    
    print(f"\n--- CENTERED SPECTRAL MANIFOLD ---")
    print(f"Symmetry Center (λ): {l_opt:.6f} MeV")
    print(f"Spectral Slope (p):  {p_opt:.6f}")
    print(f"Phase Stiffness (α): {a_opt:.6f}\n")
    
    for i, k in enumerate(['e', 'mu', 'tau']):
        val = esqet_centered_operator(i, p_opt, l_opt, a_opt)
        err = abs(float(val) - TARGETS[k]) / TARGETS[k] * 100
        print(f"{k.upper():<3} | Pred: {float(val):10.4f} | Actual: {TARGETS[k]:10.4f} | Err: {err:7.4f}%")
