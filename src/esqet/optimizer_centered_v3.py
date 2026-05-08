#!/usr/bin/env python3
"""
ESQET Centered Spectral Model v3
Better scaling separation + adaptive bounds
"""

import numpy as np
from scipy.optimize import differential_evolution
import mpmath as mp

mp.mp.dps = 40
PHI = (mp.mpf(1) + mp.sqrt(mp.mpf(5))) / 2
OMEGA = mp.exp(2j * mp.pi / 3)

TARGETS = {
    'e': mp.mpf('0.5109989461'),
    'mu': mp.mpf('105.6583745'),
    'tau': mp.mpf('1776.86')
}

def get_mass(n, p, mu_scale, gen_ratio, alpha):
    """
    n = 0 (e), 1 (mu), 2 (tau)
    mu_scale = central anchor
    gen_ratio = effective generational multiplication factor
    """
    # Centered exponent
    exp = (n - 1) * p
    
    # Z3 phase modulation (bounded)
    phase = OMEGA ** n
    delta = mp.mpf('1.0') + 0.8 * mp.re(phase)   # milder modulation
    
    # Core multiplicative form
    mass = mu_scale * (PHI ** exp) * (gen_ratio ** abs(n-1)) * (delta ** alpha)
    
    # Small additive floor for electron stability
    if n == 0:
        mass += mp.mpf('0.4')
    
    return mass


def objective(params):
    p, mu_scale, gen_ratio, alpha = [mp.mpf(x) for x in params]
    
    error = mp.mpf('0')
    weights = [3.0, 12.0, 4.0]   # muon priority
    
    for i, k in enumerate(['e', 'mu', 'tau']):
        pred = get_mass(i, p, mu_scale, gen_ratio, alpha)
        rel = (pred - TARGETS[k]) / TARGETS[k]
        error += weights[i] * rel**2
    
    return float(mp.sqrt(error))


if __name__ == "__main__":
    print("🚀 ESQET Centered Spectral Model v3 - Improved Separation\n")
    
    bounds = [
        (4.5, 7.5),      # p
        (90.0, 125.0),   # mu_scale
        (10.0, 30.0),    # gen_ratio (controls electron <-> muon jump)
        (0.2, 2.8)       # alpha
    ]
    
    result = differential_evolution(
        objective, bounds,
        tol=1e-15,
        popsize=50,
        mutation=0.7,
        recombination=0.8,
        seed=123,
        workers=1,
        maxiter=200
    )
    
    p, mu_scale, gen_ratio, alpha = [float(x) for x in result.x]
    
    print("--- OPTIMIZATION RESULTS v3 ---")
    print(f"Exponent p          : {p:.8f}")
    print(f"Muon Anchor         : {mu_scale:.6f} MeV")
    print(f"Generation Ratio    : {gen_ratio:.6f}")
    print(f"Phase Stiffness α   : {alpha:.6f}")
    print(f"Loss                : {result.fun:.8f}\n")
    
    print("Particle   Predicted (MeV)   Actual (MeV)   Error %")
    print("-" * 58)
    preds = []
    for i, name in enumerate(['e', 'mu', 'tau']):
        pred = float(get_mass(i, p, mu_scale, gen_ratio, alpha))
        actual = float(TARGETS[name])
        err = abs(pred - actual) / actual * 100
        preds.append(pred)
        print(f"{name.upper():<3}     {pred:12.4f}    {actual:12.4f}    {err:7.3f}%")
    
    # Koide
    sum_m = sum(preds)
    sum_s = sum(np.sqrt(m) for m in preds)
    Q = sum_m / (sum_s ** 2)
    print(f"\nKoide Q             : {Q:.8f}")
    print(f"Deviation from 2/3  : {abs(Q - 2/3):.2e}")
