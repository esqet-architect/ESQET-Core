#!/usr/bin/env python3
"""
ESQET Z₃ Mass Matrix Operator
Generations as representations of Z₃ → physical masses from eigenvalues
"""

import numpy as np
from scipy.optimize import differential_evolution
import mpmath as mp

mp.mp.dps = 50
PHI = (mp.mpf(1) + mp.sqrt(mp.mpf(5))) / 2
OMEGA = mp.exp(2j * mp.pi / 3)   # Z3 root of unity

TARGETS = {
    'e': mp.mpf('0.5109989461'),
    'mu': mp.mpf('105.6583745'),
    'tau': mp.mpf('1776.86')
}

def build_z3_mass_matrix(p, mu_scale, coupling, alpha):
    """Construct 3x3 mass matrix in Z3 basis"""
    M = mp.matrix(3)
    
    # Diagonal terms: centered scaling + representation phase
    for i in range(3):
        offset = i - 1                      # electron=-1, muon=0, tau=+1
        phase_factor = OMEGA ** i
        diag = mu_scale * (PHI ** (offset * p)) * (phase_factor ** alpha)
        M[i, i] = diag
    
    # Off-diagonal Z3-allowed soft breaking terms
    for i in range(3):
        for j in range(3):
            if i != j:
                # Symmetric breaking modulated by golden ratio
                M[i, j] = coupling * (PHI ** ((i + j - 2) * p / 2))
    
    # Get eigenvalues (physical masses)
    evals = M.eigenvals()
    masses = sorted([mp.fabs(ev) for ev in evals])
    return masses


def objective(params):
    p, mu_scale, coupling, alpha = [mp.mpf(x) for x in params]
    
    # Enforce physical constraints
    if alpha < 0 or mu_scale < 90 or mu_scale > 120:
        return 1e8
    
    try:
        masses = build_z3_mass_matrix(p, mu_scale, coupling, alpha)
        error = mp.mpf(0)
        weights = [5.0, 15.0, 6.0]   # strong muon weight
        
        for i, k in enumerate(['e', 'mu', 'tau']):
            rel = (masses[i] - TARGETS[k]) / TARGETS[k]
            error += weights[i] * rel**2
        return float(mp.sqrt(error))
    except:
        return 1e8


if __name__ == "__main__":
    print("🚀 ESQET Z₃ Mass Matrix Operator\n")
    print("Muon anchored + positive alpha constraint\n")
    
    bounds = [
        (4.5, 8.0),      # p
        (100.0, 112.0),  # mu_scale (tight around physical value)
        (0.01, 8.0),     # coupling strength (off-diagonal breaking)
        (0.0, 3.0)       # alpha ≥ 0
    ]
    
    result = differential_evolution(
        objective, bounds,
        tol=1e-14,
        popsize=60,
        mutation=0.75,
        recombination=0.85,
        seed=123,
        maxiter=500,
        workers=1
    )
    
    p, mu_scale, coupling, alpha = [float(x) for x in result.x]
    masses = build_z3_mass_matrix(p, mu_scale, coupling, alpha)
    
    print("--- Z₃ MATRIX RESULTS ---")
    print(f"Exponent p          : {p:.8f}")
    print(f"Muon Scale (anchor) : {mu_scale:.6f} MeV")
    print(f"Breaking Coupling   : {coupling:.6f}")
    print(f"Representation α    : {alpha:.6f}")
    print(f"Loss                : {result.fun:.2e}\n")
    
    print("Generation   Predicted (MeV)   Actual (MeV)   Error %")
    print("-" * 62)
    names = ['Electron', 'Muon', 'Tau']
    for name, pred, actual in zip(names, masses, [float(v) for v in TARGETS.values()]):
        err = abs(float(pred) - actual) / actual * 100
        print(f"{name:<10}   {float(pred):12.4f}    {actual:12.4f}    {err:7.4f}%")
    
    # Koide
    sum_m = sum(float(m) for m in masses)
    sum_s = sum(np.sqrt(float(m)) for m in masses)
    Q = sum_m / (sum_s ** 2)
    print(f"\nKoide Q             : {Q:.8f}")
    print(f"Deviation from 2/3  : {abs(Q - 2/3):.2e}")
