#!/usr/bin/env python3
"""
ESQET Centered Spectral Model v2
Muon as true fixed point + stronger constraints
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

def get_mass(n, p, mu_scale, ratio_factor, alpha):
    """
    Cleaner parameterization:
      - mu_scale = mass at center (n=1)
      - ratio_factor controls generational jump strength
    """
    # Centered exponent
    exp = (n - 1) * p
    
    # Z3 phase as modulation (bounded)
    phase = OMEGA ** n
    delta = (mp.re(phase) + mp.mpf('1.2')) ** alpha   # shifted for better range
    
    # Multiplicative hierarchy centered on muon
    return mu_scale * (PHI ** exp) * delta ** ratio_factor


def objective(params):
    p, mu_scale, ratio_factor, alpha = [mp.mpf(x) for x in params]
    
    error = mp.mpf('0')
    weights = [1.0, 8.0, 2.0]   # strong muon emphasis
    
    for i, k in enumerate(['e', 'mu', 'tau']):
        pred = get_mass(i, p, mu_scale, ratio_factor, alpha)
        rel_err = (pred - TARGETS[k]) / TARGETS[k]
        error += weights[i] * rel_err**2
    
    return float(mp.sqrt(error))


if __name__ == "__main__":
    print("🚀 ESQET Centered Spectral Model v2")
    print("Muon anchored as central scale\n")
    
    bounds = [
        (5.2, 6.8),      # p — focused on golden-like region
        (80.0, 130.0),   # mu_scale — around real muon mass
        (0.5, 3.0),      # ratio_factor
        (0.3, 2.5)       # alpha
    ]
    
    result = differential_evolution(
        objective, bounds, 
        tol=1e-14, 
        popsize=40, 
        mutation=0.65, 
        recombination=0.7,
        seed=42,
        workers=1
    )
    
    p, mu_scale, ratio_factor, alpha = result.x
    
    print("--- OPTIMIZATION RESULTS ---")
    print(f"Exponent p          : {p:.8f}")
    print(f"Muon Scale (central): {mu_scale:.6f} MeV")
    print(f"Ratio Factor        : {ratio_factor:.6f}")
    print(f"Phase Stiffness α   : {alpha:.6f}")
    print(f"Final Loss          : {result.fun:.8f}\n")
    
    print("Particle   Predicted      Actual       Error %")
    print("-" * 55)
    for i, name in enumerate(['e', 'mu', 'tau']):
        pred = get_mass(i, p, mu_scale, ratio_factor, alpha)
        err = float(abs(pred - TARGETS[name]) / TARGETS[name] * 100)
        print(f"{name.upper():<3}     {float(pred):10.4f}    {float(TARGETS[name]):10.4f}    {err:7.3f}%")
    
    # Koide relation
    preds = [get_mass(i, p, mu_scale, ratio_factor, alpha) for i in range(3)]
    sum_m = sum(preds)
    sum_s = sum(mp.sqrt(m) for m in preds)
    Q = sum_m / (sum_s ** 2)
    print(f"\nKoide Q             : {float(Q):.8f}")
    print(f"Deviation from 2/3  : {float(abs(Q - mp.mpf('2')/3)):.2e}")
