#!/usr/bin/env python3
"""
ESQET Z₃ Triplet with Aligned Flavon VEV
Improved breaking + better numerical stability
"""

import numpy as np
from scipy.optimize import differential_evolution
import mpmath as mp

mp.mp.dps = 50
PHI = (mp.mpf(1) + mp.sqrt(mp.mpf(5))) / 2
OMEGA = mp.exp(2j * mp.pi / 3)

TARGETS = {
    'e': mp.mpf('0.5109989461'),
    'mu': mp.mpf('105.6583745'),
    'tau': mp.mpf('1776.86')
}

def build_mass_matrix(p, v_flavon, yukawa, alpha):
    """Triplet with flavon VEV aligned toward tau generation"""
    M = mp.matrix(3)
    
    # Flavon VEV vector (strongest toward tau)
    vev = [v_flavon * PHI**(-1.5), v_flavon * PHI**(-0.5), v_flavon]
    
    for i in range(3):
        for j in range(3):
            # Invariant bilinear + flavon insertion
            base_scale = PHI ** ((i + j - 2) * p / 2.0)
            flavon_contrib = (vev[i] * vev[j]) ** alpha
            M[i,j] = yukawa * base_scale * flavon_contrib
    
    # Small explicit breaking for electron
    M[0,0] += mp.mpf('0.35')
    
    # Get physical masses
    evals = mp.eig(M, left=False, right=False)
    masses = sorted([mp.fabs(ev) for ev in evals])
    return masses


def objective(params):
    p, v_flavon, yukawa, alpha = [mp.mpf(x) for x in params]
    
    if alpha < 0 or v_flavon < 80 or v_flavon > 140 or yukawa < 0:
        return 1e9
    
    try:
        masses = build_mass_matrix(p, v_flavon, yukawa, alpha)
        error = mp.mpf(0)
        weights = [8.0, 12.0, 5.0]
        
        for i, k in enumerate(['e','mu','tau']):
            rel = (masses[i] - TARGETS[k]) / TARGETS[k]
            error += weights[i] * rel**2
        return float(mp.sqrt(error))
    except:
        return 1e9


if __name__ == "__main__":
    print("🚀 ESQET Z₃ Triplet + Aligned Flavon VEV (Refined)\n")
    
    bounds = [
        (4.8, 7.5),      # p
        (95.0, 125.0),   # v_flavon (near muon scale)
        (0.05, 3.0),     # yukawa coupling
        (0.1, 2.8)       # alpha
    ]
    
    result = differential_evolution(
        objective, bounds,
        tol=1e-15,
        popsize=80,
        mutation=0.82,
        recombination=0.88,
        seed=777,
        maxiter=1000,
        workers=1
    )
    
    p, v_flavon, yukawa, alpha = [float(x) for x in result.x]
    masses = build_mass_matrix(p, v_flavon, yukawa, alpha)
    
    print("--- REFINED TRIPLET + FLAVON RESULTS ---")
    print(f"Exponent p          : {p:.8f}")
    print(f"Flavon VEV scale    : {v_flavon:.6f} MeV")
    print(f"Yukawa coupling     : {yukawa:.6f}")
    print(f"Flavon power α      : {alpha:.6f}")
    print(f"Loss                : {result.fun:.2e}\n")
    
    print("Generation   Predicted (MeV)   Actual (MeV)   Error %")
    print("-" * 62)
    names = ['Electron', 'Muon', 'Tau']
    for name, pred, actual in zip(names, masses, TARGETS.values()):
        err = abs(float(pred) - float(actual)) / float(actual) * 100
        print(f"{name:<10}   {float(pred):12.4f}    {float(actual):12.4f}    {err:7.4f}%")
    
    sum_m = sum(float(m) for m in masses)
    sum_s = sum(np.sqrt(float(m)) for m in masses)
    Q = sum_m / (sum_s ** 2)
    print(f"\nKoide Q             : {Q:.8f}")
    print(f"Deviation from 2/3  : {abs(Q - 2/3):.2e}")
