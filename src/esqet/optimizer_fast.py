#!/usr/bin/env python3
"""
ESQET Lepton Mass Model — Fast & Stable Version
Uses numpy only, no mpmath type issues
"""

import numpy as np
from scipy.optimize import differential_evolution, minimize

# Constants
PHI = (1 + np.sqrt(5)) / 2
OMEGA_REAL = np.cos(2 * np.pi / 3)  # Re(ω) = -1/2
OMEGA_IMAG = np.sin(2 * np.pi / 3)   # Im(ω) = √3/2

# Known masses in MeV
TARGETS = {
    'e': 0.5109989461,
    'mu': 105.6583745,
    'tau': 1776.86
}

def z3_phase_modulation(n, alpha, strength=0.6):
    """Z3 phase modulation based on cube roots of unity"""
    # ω = e^(2πi/3)
    phase_angle = 2 * np.pi * n / 3
    # Real part modulation
    modulation = 1.0 + strength * np.cos(phase_angle)
    return modulation ** alpha

def get_mass(n, p, mu_scale, gamma, alpha):
    """
    Centered mass formula (n=0: e, n=1: mu, n=2: tau)
    
    Parameters:
    - p: exponent for PHI scaling
    - mu_scale: muon mass anchor
    - gamma: generation ratio factor
    - alpha: phase stiffness
    """
    gen_offset = n - 1
    
    # PHI scaling (centered on muon)
    if gen_offset == 0:
        phi_term = 1.0
    else:
        phi_term = PHI ** (gen_offset * p)
    
    # Generation ratio term
    ratio_term = gamma ** abs(gen_offset)
    
    # Z3 phase modulation
    phase_term = z3_phase_modulation(n, alpha)
    
    mass = mu_scale * phi_term * ratio_term * phase_term
    
    # Floor for electron
    if n == 0 and mass < 0.4:
        mass = 0.4
    
    return mass

def objective(params):
    """Logarithmic error for scale invariance"""
    p, mu_scale, gamma, alpha = params
    
    # Parameter bounds protection
    if mu_scale < 10 or mu_scale > 500:
        return 1e10
    if gamma < 0.1 or gamma > 50:
        return 1e10
    
    errors = []
    for i, key in enumerate(['e', 'mu', 'tau']):
        pred = get_mass(i, p, mu_scale, gamma, alpha)
        target = TARGETS[key]
        
        # Combined absolute and relative error
        abs_err = abs(pred - target) / target
        log_err = abs(np.log(pred / target))
        
        errors.append(abs_err + 0.5 * log_err)
    
    return np.mean(errors)

def koide_quality(masses):
    """Check Koide relation Q = (sum m) / (sum sqrt(m))^2"""
    sum_m = sum(masses)
    sum_sqrt = sum(np.sqrt(max(0, m)) for m in masses)
    if sum_sqrt == 0:
        return 0
    return sum_m / (sum_sqrt ** 2)


if __name__ == "__main__":
    print("="*60)
    print("ESQET Lepton Mass Model — Fast Optimizer")
    print("="*60)
    
    # Bounds for parameters
    bounds = [
        (4.0, 12.0),    # p — PHI exponent
        (90.0, 120.0),  # mu_scale — muon anchor (MeV)
        (1.0, 30.0),    # gamma — generation ratio
        (0.0, 3.0)      # alpha — phase stiffness
    ]
    
    print("\nRunning differential evolution...")
    result = differential_evolution(
        objective, bounds,
        tol=1e-10,
        popsize=30,
        maxiter=200,
        seed=42,
        disp=True,
        workers=1
    )
    
    p_opt, mu_opt, gamma_opt, alpha_opt = result.x
    
    print("\n" + "="*60)
    print("OPTIMIZATION RESULTS")
    print("="*60)
    print(f"Exponent p          : {p_opt:.8f}")
    print(f"Muon Anchor μ₀      : {mu_opt:.6f} MeV")
    print(f"Generation ratio γ  : {gamma_opt:.6f}")
    print(f"Phase stiffness α   : {alpha_opt:.6f}")
    print(f"Final loss          : {result.fun:.8e}")
    
    print("\n" + "="*60)
    print("PREDICTED MASSES")
    print("="*60)
    print(f"{'Particle':<10} {'Predicted':<12} {'Actual':<12} {'Error %':<10}")
    print("-" * 50)
    
    predictions = []
    for i, name in enumerate(['e', 'mu', 'tau']):
        pred = get_mass(i, p_opt, mu_opt, gamma_opt, alpha_opt)
        actual = TARGETS[name]
        err_pct = abs(pred - actual) / actual * 100
        predictions.append(pred)
        print(f"{name.upper():<10} {pred:12.4f} {actual:12.4f} {err_pct:9.4f}%")
    
    print("\n" + "="*60)
    print("KOIDE RELATION VERIFICATION")
    print("="*60)
    koide_q = koide_quality(predictions)
    print(f"Koide Q value       : {koide_q:.8f}")
    print(f"Target (2/3)        : {0.66666667:.8f}")
    print(f"Deviation           : {abs(koide_q - 2/3):.2e}")
    print(f"Relative deviation  : {abs(koide_q - 2/3) / (2/3) * 100:.4f}%")
    
    # Golden ratio analysis
    print("\n" + "="*60)
    print("GOLDEN RATIO ANALYSIS")
    print("="*60)
    phi_p = PHI ** p_opt
    print(f"φ^p                : {phi_p:.6f}")
    print(f"Generation ratio γ : {gamma_opt:.6f}")
    print(f"γ / φ^p            : {gamma_opt / phi_p:.6f}")
    
    # Z3 symmetry test
    print("\n" + "="*60)
    print("Z3 SYMMETRY TEST")
    print("="*60)
    for n in [0, 1, 2]:
        mod = z3_phase_modulation(n, alpha_opt)
        print(f"n={n} (mass {['e','μ','τ'][n]}): modulation = {mod:.6f}")
    
    # Recommended final parameters
    print("\n" + "="*60)
    print("RECOMMENDED ESQET PARAMETERS")
    print("="*60)
    print(f"""
    p           = {p_opt:.6f}
    mu_scale    = {mu_opt:.6f} MeV
    gamma       = {gamma_opt:.6f}
    alpha       = {alpha_opt:.6f}
    """)
