#!/usr/bin/env python3
"""
ESQET Lepton Mass Model v6.0 - Fixed Bounds & Multi-Objective Loss
Addresses the boundary-hitting issue from v5
"""

import numpy as np
from scipy.optimize import differential_evolution, minimize
from scipy.special import softmax

PHI = (1 + np.sqrt(5)) / 2

# Experimental masses (MeV) with higher precision
MASSES = {
    'e': 0.5109989461,
    'mu': 105.6583745,
    'tau': 1776.86
}

def z3_modulation(n, alpha, beta=0.5):
    """Z3 phase factor with symmetry-preserving form"""
    theta = 2 * np.pi * n / 3
    # Real part of ω^n plus constant to keep positive
    re_omega = np.cos(theta)
    # Shifted to [0.5, 1.5] range
    modulation = 1.0 + beta * re_omega
    return modulation ** alpha if alpha != 0 else 1.0

def get_mass(n, p, mu0, r, alpha, beta=0.5):
    """
    n = 0 (electron), 1 (muon), 2 (tau)
    p: power-law exponent for φ scaling
    mu0: mass scale (should be near muon mass)
    r: generation ratio factor
    alpha: Z3 coupling exponent
    """
    offset = n - 1
    
    # Geometric progression centered on muon
    if offset == 0:
        geom = 1.0
    else:
        geom = PHI ** (offset * p)
    
    # Generation jump factor
    jump = r ** abs(offset)
    
    # Z3 symmetry modulation
    z3 = z3_modulation(n, alpha, beta)
    
    mass = mu0 * geom * jump * z3
    
    # Small additive correction for electron (beyond multiplicative)
    # This helps with the huge dynamic range
    if n == 0 and mass < 1.0:
        mass = mass + 0.2
    
    return max(mass, 1e-6)

def loss_components(p, mu0, r, alpha):
    """Return individual mass predictions and errors"""
    preds = [get_mass(n, p, mu0, r, alpha) for n in range(3)]
    targets = [MASSES['e'], MASSES['mu'], MASSES['tau']]
    
    # Logarithmic error (better for wide range)
    log_errors = [abs(np.log(pred / target)) for pred, target in zip(preds, targets)]
    
    # Relative error
    rel_errors = [abs(pred - target) / target for pred, target in zip(preds, targets)]
    
    # Combined loss with emphasis on muon (central anchor)
    weights = [1.5, 2.0, 1.5]  # e, mu, tau
    
    loss = 0.0
    for w, log_err, rel_err in zip(weights, log_errors, rel_errors):
        loss += w * (log_err ** 2 + 0.5 * rel_err ** 2)
    
    return loss / sum(weights), preds

def objective(params):
    p, mu0, r, alpha = params
    loss, _ = loss_components(p, mu0, r, alpha)
    return loss

def koide_q(masses):
    """Koide relation: Q = (Σ m) / (Σ √m)²"""
    s1 = sum(masses)
    s2 = sum(np.sqrt(m) for m in masses)
    return s1 / (s2 ** 2)

def print_results(p, mu0, r, alpha, loss, preds):
    """Pretty print with Koide check"""
    targets = [MASSES['e'], MASSES['mu'], MASSES['tau']]
    names = ['Electron', 'Muon', 'Tau']
    
    print("\n" + "="*65)
    print("OPTIMIZED PARAMETERS")
    print("="*65)
    print(f"  p (φ exponent)     = {p:.8f}")
    print(f"  μ₀ (mass scale)    = {mu0:.6f} MeV")
    print(f"  r (generation ratio)= {r:.6f}")
    print(f"  α (Z3 coupling)    = {alpha:.6f}")
    print(f"  Loss function      = {loss:.6e}")
    
    print("\n" + "="*65)
    print("MASS PREDICTIONS")
    print("="*65)
    print(f"{'Particle':<10} {'Predicted (MeV)':<18} {'Actual (MeV)':<15} {'Error (%)':<12}")
    print("-" * 65)
    
    errors_pct = []
    for name, pred, target in zip(names, preds, targets):
        err_pct = abs(pred - target) / target * 100
        errors_pct.append(err_pct)
        print(f"{name:<10} {pred:16.4f}    {target:12.4f}    {err_pct:10.4f}%")
    
    # Koide relation
    Q = koide_q(preds)
    Q_target = 2/3
    print("\n" + "="*65)
    print("KOIDE RELATION")
    print("="*65)
    print(f"  Koide Q value      = {Q:.8f}")
    print(f"  Target (2/3)       = {Q_target:.8f}")
    print(f"  Deviation          = {abs(Q - Q_target):.2e}")
    print(f"  Relative error     = {abs(Q - Q_target) / Q_target * 100:.4f}%")
    
    # Check φ^p
    phi_p = PHI ** p
    print("\n" + "="*65)
    print("GOLDEN RATIO SCALING")
    print("="*65)
    print(f"  φ^p                = {phi_p:.6f}")
    print(f"  r / φ^p            = {r / phi_p:.6f}")
    
    # Z3 symmetry verification
    print("\n" + "="*65)
    print("Z₃ SYMMETRY MODULATION")
    print("="*65)
    for n in range(3):
        mod = z3_modulation(n, alpha)
        print(f"  n={n} ({['e','μ','τ'][n]}): modulation = {mod:.6f}")
    
    return errors_pct

if __name__ == "__main__":
    print("="*65)
    print("ESQET LEPTON MASS MODEL v6.0")
    print("Multi-objective optimization with expanded bounds")
    print("="*65)
    
    # Expanded bounds - allow parameters to find natural values
    bounds = [
        (2.0, 15.0),     # p - φ exponent
        (70.0, 130.0),   # mu0 - mass scale (around muon mass)
        (0.5, 30.0),     # r - generation ratio
        (-2.0, 3.0)      # alpha - Z3 coupling (allow negative)
    ]
    
    print("\nRunning differential evolution...")
    print("This may take a few minutes.\n")
    
    result = differential_evolution(
        objective, bounds,
        tol=1e-12,
        popsize=40,
        maxiter=300,
        seed=42,
        disp=True,
        workers=1,
        updating='deferred'
    )
    
    p_opt, mu0_opt, r_opt, alpha_opt = result.x
    loss_opt, preds_opt = loss_components(p_opt, mu0_opt, r_opt, alpha_opt)
    
    errors = print_results(p_opt, mu0_opt, r_opt, alpha_opt, loss_opt, preds_opt)
    
    # Final assessment
    print("\n" + "="*65)
    print("FINAL ASSESSMENT")
    print("="*65)
    
    # Check if parameters are realistic
    if abs(mu0_opt - MASSES['mu']) < 5:
        print("✓ Muon anchor is within 5 MeV of physical value")
    else:
        print(f"⚠ Muon anchor deviates by {abs(mu0_opt - MASSES['mu']):.1f} MeV")
    
    if r_opt > 1.0:
        print(f"✓ Generation ratio r = {r_opt:.3f} > 1 (natural hierarchy)")
    else:
        print(f"⚠ Generation ratio r = {r_opt:.3f} < 1 (inverted hierarchy)")
    
    # Koide check
    koide_ok = abs(koide_q(preds_opt) - 2/3) < 0.01
    if koide_ok:
        print("✓ Koide relation satisfied within 1%")
    else:
        print("⚠ Koide relation deviation > 1%")
    
    # Average error
    avg_err = np.mean(errors)
    if avg_err < 10:
        print(f"✓ Average mass error = {avg_err:.2f}%")
    else:
        print(f"⚠ Average mass error = {avg_err:.2f}% (further refinement needed)")
    
    # Save parameters for later use
    np.savez("esqet_mass_params.npz",
             p=p_opt, mu0=mu0_opt, r=r_opt, alpha=alpha_opt,
             loss=loss_opt, preds=preds_opt)
    print("\nParameters saved to: esqet_mass_params.npz")
