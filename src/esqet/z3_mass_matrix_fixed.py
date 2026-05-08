#!/usr/bin/env python3
"""
ESQET Z₃ Mass Matrix Operator — Fixed
Proper eigenvalue computation + Flavon-inspired breaking
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

def build_z3_mass_matrix(p, mu_scale, coupling, alpha):
    """3x3 Mass matrix in Z3 basis"""
    M = mp.matrix(3)
    
    # Diagonal: centered scaling with representation phase
    for i in range(3):
        offset = i - 1
        phase_factor = OMEGA ** i
        diag = mu_scale * (PHI ** (offset * p)) * (phase_factor ** alpha)
        M[i, i] = diag
    
    # Off-diagonal soft breaking (Z3-allowed)
    for i in range(3):
        for j in range(i+1, 3):
            term = coupling * (PHI ** ((i + j - 2) * p / 2))
            M[i, j] = term
            M[j, i] = term   # Hermitian
    
    # Compute eigenvalues using mpmath
    evals = mp.eig(M, left=False, right=False)
    masses = sorted([mp.fabs(ev) for ev in evals])
    return masses


def objective(params):
    p, mu_scale, coupling, alpha = [mp.mpf(x) for x in params]
    
    # Physical constraints
    if alpha < 0 or mu_scale < 90 or mu_scale > 120 or coupling < 0:
        return 1e8
    
    try:
        masses = build_z3_mass_matrix(p, mu_scale, coupling, alpha)
        error = mp.mpf(0)
        weights = [5.0, 15.0, 6.0]
        
        for i, k in enumerate(['e', 'mu', 'tau']):
            rel = (masses[i] - TARGETS[k]) / TARGETS[k]
            error += weights[i] * rel**2
        return float(mp.sqrt(error))
    except:
        return 1e8


if __name__ == "__main__":
    print("🚀 ESQET Z₃ Mass Matrix Operator (Fixed)\n")
    print("Muon anchored + α ≥ 0 constraint\n")
    
    bounds = [
        (4.5, 8.5),      # p
        (100.0, 112.0),  # mu_scale
        (0.01, 12.0),    # coupling (breaking strength)
        (0.0, 3.5)       # alpha ≥ 0
    ]
    
    result = differential_evolution(
        objective, bounds,
        tol=1e-14,
        popsize=70,
        mutation=0.8,
        recombination=0.85,
        seed=42,
        maxiter=800,
        workers=1
    )
    
    p, mu_scale, coupling, alpha = [float(x) for x in result.x]
    masses = build_z3_mass_matrix(p, mu_scale, coupling, alpha)
    
    print("--- Z₃ MATRIX RESULTS (Fixed) ---")
    print(f"Exponent p          : {p:.8f}")
    print(f"Muon Scale (anchor) : {mu_scale:.6f} MeV")
    print(f"Breaking Coupling   : {coupling:.6f}")
    print(f"Representation α    : {alpha:.6f}")
    print(f"Loss                : {result.fun:.2e}\n")
    
    print("Generation   Predicted (MeV)   Actual (MeV)   Error %")
    print("-" * 62)
    names = ['Electron', 'Muon', 'Tau']
    for name, pred, actual in zip(names, masses, TARGETS.values()):
        err = abs(float(pred) - float(actual)) / float(actual) * 100
        print(f"{name:<10}   {float(pred):12.4f}    {float(actual):12.4f}    {err:7.4f}%")
    
    # Koide
    sum_m = sum(float(m) for m in masses)
    sum_s = sum(np.sqrt(float(m)) for m in masses)
    Q = sum_m / (sum_s ** 2)
    print(f"\nKoide Q             : {Q:.8f}")
    print(f"Deviation from 2/3  : {abs(Q - 2/3):.2e}")
