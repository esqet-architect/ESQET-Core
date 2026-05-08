#!/usr/bin/env python3
"""
ESQET Lepton Mass Model — Final Clean Version (v4.3)
Fixed: mpf formatting TypeError and boundary constraints.
"""
import numpy as np
from scipy.optimize import differential_evolution
import mpmath as mp

# Precision setup
mp.mp.dps = 50
PHI = (mp.mpf(1) + mp.sqrt(mp.mpf(5))) / 2
OMEGA = mp.exp(2j * mp.pi / 3)

TARGETS = {
    'e': mp.mpf('0.5109989461'),
    'mu': mp.mpf('105.6583745'),
    'tau': mp.mpf('1776.86')
}

def get_mass(n, p, mu_scale, log_ratio, alpha):
    """Centered on muon (n=1)"""
    gen_offset = mp.mpf(n) - 1
    
    # Z3 phase modulation
    phase = OMEGA ** n
    delta = mp.mpf('1.0') + mp.mpf('0.6') * mp.re(phase)

    # Core hierarchy
    # mass = mu_scale * (PHI^(offset*p)) * (log_ratio^|offset|) * (delta^alpha)
    term1 = mp.power(PHI, (gen_offset * p))
    term2 = mp.power(log_ratio, mp.absmin(gen_offset)) # Using absolute distance
    
    mass = mu_scale * term1 * term2 * mp.power(delta, alpha)

    # Floor logic
    if n == 0:
        floor = mp.mpf('0.4')
        if mass < floor: mass = floor

    return mass

def objective(params):
    p, mu_scale, log_ratio, alpha = [mp.mpf(x) for x in params]
    error = mp.mpf('0')
    
    # We use log-space error for large scale differences
    for i, k in enumerate(['e', 'mu', 'tau']):
        pred = get_mass(i, p, mu_scale, log_ratio, alpha)
        # Logarithmic error handles the 0.5 to 1776 range better than linear rel_err
        log_err = mp.log(pred / TARGETS[k])
        error += (log_err ** 2)

    return float(mp.sqrt(error))

if __name__ == "__main__":
    print("🚀 ESQET Final Centered Model v4.3\n")

    # Expanded bounds: The model was hitting the walls at 90.0 and 1.0
    bounds = [
        (2.0, 15.0),     # p
        (10.0, 500.0),   # mu_scale (Anchor can vary significantly)
        (0.1, 100.0),    # log_ratio
        (-5.0, 5.0)      # alpha (Allow phase dampening/amplification)
    ]

    result = differential_evolution(
        objective, bounds,
        strategy='best1bin',
        tol=1e-13,
        popsize=50,
        mutation=(0.5, 1.2),
        recombination=0.8,
        seed=42,
        maxiter=1500
    )

    # Extract results as mpmath types for the final display
    p_f, mu_f, log_f, alpha_f = [mp.mpf(x) for x in result.x]

    print("--- FINAL OPTIMIZATION RESULTS v4.3 ---")
    print(f"Exponent p          : {float(p_f):.8f}")
    print(f"Muon Anchor         : {float(mu_f):.6f} MeV")
    print(f"Log Ratio Factor    : {float(log_f):.6f}")
    print(f"Phase Stiffness α   : {float(alpha_f):.6f}")
    print(f"Final Loss (Log-RMS): {result.fun:.8e}\n")

    print("Particle   Predicted (MeV)   Actual (MeV)   Error %")
    print("-" * 58)
    preds = []
    for i, name in enumerate(['e', 'mu', 'tau']):
        pred = get_mass(i, p_f, mu_f, log_f, alpha_f)
        actual = TARGETS[name]
        # Calculate error using float for final print
        err_val = float(abs(pred - actual) / actual * 100)
        preds.append(float(pred))
        
        # Casting to float here solves the format string TypeError
        print(f"{name.upper():<3}     {float(pred):12.4f}    {float(actual):12.4f}    {err_val:7.6f}%")

    # Koide relation check
    sum_m = sum(preds)
    sum_s = sum(np.sqrt(m) for m in preds)
    Q = sum_m / (sum_s ** 2)
    print(f"\nKoide Q             : {Q:.8f}")
    print(f"Deviation from 2/3  : {abs(Q - 2/3):.2e}")
