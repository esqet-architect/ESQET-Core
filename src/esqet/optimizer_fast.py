#!/usr/bin/env python3
import numpy as np
from scipy.optimize import differential_evolution, minimize

# Constants
PHI = (1.0 + np.sqrt(5.0)) / 2.0
TARGETS = np.array([0.5109989461, 105.6583745, 1776.86])

def get_masses(p, mu_scale, gamma, alpha):
    n = np.array([0, 1, 2])
    gen_offset = n - 1
    
    # Z3 modulation
    phases = np.exp(2j * np.pi * n / 3.0)
    modulation = 1.0 + 0.6 * np.real(phases)
    delta = modulation ** alpha
    
    # Hierarchy: Muon centered
    # mass = mu_scale * (PHI^(offset*p)) * (gamma^|offset|) * delta
    # We use power for the hierarchy jumps
    masses = mu_scale * (PHI ** (gen_offset * p)) * (gamma ** np.abs(gen_offset)) * delta
    return masses

def objective(params):
    p, mu_scale, gamma, alpha = params
    preds = get_masses(p, mu_scale, gamma, alpha)
    
    # Logarithmic RMS error is much more robust for values across 4 orders of magnitude
    log_errors = np.log(preds / TARGETS)
    rmse = np.sqrt(np.mean(log_errors**2))
    
    # Add a small penalty for being too close to the bounds to push the optimizer back
    return rmse

if __name__ == "__main__":
    print("============================================================")
    print("      ESQET Lepton Mass Model — Fast Optimizer v4.4")
    print("============================================================\n")

    # Expanded bounds to stop "hugging" the 90.0 and 1.0 limits
    bounds = [
        (2.0, 12.0),      # p (Exponent)
        (50.0, 150.0),    # mu_scale (Anchor - wider range)
        (0.5, 20.0),      # gamma (Generation ratio)
        (-2.0, 2.0)       # alpha (Phase stiffness)
    ]

    result = differential_evolution(
        objective, bounds,
        strategy='best1bin',
        maxiter=1000,
        popsize=30,
        tol=1e-12,
        mutation=(0.5, 1.0),
        recombination=0.7,
        disp=True
    )

    # Polishing
    final_res = minimize(objective, result.x, method='L-BFGS-B', bounds=bounds)
    p_opt, mu_opt, gamma_opt, alpha_opt = final_res.x

    preds = get_masses(p_opt, mu_opt, gamma_opt, alpha_opt)
    
    print("\n" + "="*60)
    print("OPTIMIZATION RESULTS")
    print("="*60)
    print(f"Exponent p          : {p_opt:.8f}")
    print(f"Muon Anchor μ₀      : {mu_opt:.6f} MeV")
    print(f"Generation ratio γ  : {gamma_opt:.6f}")
    print(f"Phase stiffness α   : {alpha_opt:.6f}")
    print(f"Final loss          : {final_res.fun:.8e}")

    print("\n" + "="*60)
    print("PREDICTED MASSES")
    print("="*60)
    names = ['E', 'MU', 'TAU']
    for i in range(3):
        err = abs(preds[i] - TARGETS[i]) / TARGETS[i] * 100
        print(f"{names[i]:<3}     {preds[i]:12.4f}    {TARGETS[i]:12.4f}    {err:7.4f}%")

    # Koide Relation
    sum_m = np.sum(preds)
    sum_sqrt_m = np.sum(np.sqrt(preds))
    koide_q = sum_m / (sum_sqrt_m**2)
    
    print("\n" + "="*60)
    print("KOIDE RELATION VERIFICATION")
    print("="*60)
    print(f"Koide Q value       : {koide_q:.8f}")
    print(f"Target (2/3)        : 0.66666667")
    print(f"Deviation           : {abs(koide_q - 2/3):.2e}")

    print("\n" + "="*60)
    print("RECOMMENDED ESQET PARAMETERS")
    print("="*60)
    print(f"p={p_opt:.6f}, mu={mu_opt:.6f}, gamma={gamma_opt:.6f}, alpha={alpha_opt:.6f}")
