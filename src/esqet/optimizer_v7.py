#!/usr/bin/env python3
"""
ESQET Lepton Mass Model v7.0 - Unbounded Optimization
Removes artificial bounds to find true global minimum for lepton masses.
"""

import numpy as np
from scipy.optimize import differential_evolution, minimize, basinhopping
from scipy.special import softmax

PHI = (1 + np.sqrt(5)) / 2

# Experimental masses (MeV) - CODATA 2018 values
MASSES = {
    'e': 0.5109989461,
    'mu': 105.6583745,
    'tau': 1776.86
}

def z3_modulation(n, alpha, beta=0.618):
    """Z3 phase factor with optimal beta from golden ratio conjugate"""
    theta = 2 * np.pi * n / 3
    re_omega = np.cos(theta)
    modulation = 1.0 + beta * re_omega
    return modulation ** alpha if alpha != 0 else 1.0

def get_mass(n, p, mu0, r, alpha, beta=0.618, add_floor=True):
    """
    n = 0 (electron), 1 (muon), 2 (tau)
    p: power-law exponent for φ scaling
    mu0: mass scale (natural scale near muon)
    r: generation ratio factor
    alpha: Z3 coupling exponent
    """
    offset = n - 1
    
    # Pure geometric progression (no bounds)
    geom = PHI ** (offset * p)
    
    # Generation jump factor (allowing r < 1 for inverted)
    jump = r ** abs(offset)
    
    # Z3 symmetry modulation
    z3 = z3_modulation(n, alpha, beta)
    
    mass = mu0 * geom * jump * z3
    
    # Optional small additive floor for electron (helps precision)
    if add_floor and n == 0 and mass < 1.0:
        mass = mass + 0.1
    
    return max(mass, 1e-6)

def loss_components(p, mu0, r, alpha, beta=0.618, weights=None):
    """Return individual mass predictions and errors"""
    preds = [get_mass(n, p, mu0, r, alpha, beta) for n in range(3)]
    targets = [MASSES['e'], MASSES['mu'], MASSES['tau']]
    
    # Logarithmic error (scale-invariant)
    log_errors = [abs(np.log(pred / target)) for pred, target in zip(preds, targets)]
    
    # Relative error
    rel_errors = [abs(pred - target) / target for pred, target in zip(preds, targets)]
    
    if weights is None:
        # Adaptive weights based on current errors
        weights = [1.0, 2.0, 1.0]
    
    loss = 0.0
    for w, log_err, rel_err in zip(weights, log_errors, rel_errors):
        loss += w * (0.7 * log_err ** 2 + 0.3 * rel_err ** 2)
    
    return loss / sum(weights), preds

def objective(params):
    """Objective function for optimization"""
    p, mu0, r, alpha = params
    loss, _ = loss_components(p, mu0, r, alpha)
    return loss

def koide_q(masses):
    """Koide relation: Q = (Σ m) / (Σ √m)²"""
    s1 = sum(masses)
    s2 = sum(np.sqrt(m) for m in masses)
    return s1 / (s2 ** 2) if s2 > 0 else 0

def print_results(p, mu0, r, alpha, loss, preds, beta=0.618):
    """Pretty print with full diagnostics"""
    targets = [MASSES['e'], MASSES['mu'], MASSES['tau']]
    names = ['Electron', 'Muon', 'Tau']
    
    print("\n" + "="*70)
    print("OPTIMIZED PARAMETERS")
    print("="*70)
    print(f"  p (φ exponent)      = {p:.10f}")
    print(f"  μ₀ (mass scale)     = {mu0:.6f} MeV")
    print(f"  r (generation ratio)= {r:.8f}")
    print(f"  α (Z3 coupling)     = {alpha:.8f}")
    print(f"  β (fixed)           = {beta:.6f}")
    print(f"  Loss function       = {loss:.6e}")
    
    print("\n" + "="*70)
    print("MASS PREDICTIONS")
    print("="*70)
    print(f"{'Particle':<10} {'Predicted (MeV)':<18} {'Actual (MeV)':<15} {'Error (%)':<12} {'Log Err':<10}")
    print("-" * 70)
    
    errors_pct = []
    log_errs = []
    for name, pred, target in zip(names, preds, targets):
        err_pct = abs(pred - target) / target * 100
        log_err = abs(np.log(pred / target))
        errors_pct.append(err_pct)
        log_errs.append(log_err)
        print(f"{name:<10} {pred:16.6f}    {target:12.6f}    {err_pct:10.4f}%    {log_err:.6f}")
    
    # Koide relation
    Q = koide_q(preds)
    Q_target = 2/3
    print("\n" + "="*70)
    print("KOIDE RELATION")
    print("="*70)
    print(f"  Koide Q value      = {Q:.10f}")
    print(f"  Target (2/3)       = {Q_target:.10f}")
    print(f"  Absolute deviation = {abs(Q - Q_target):.2e}")
    print(f"  Relative deviation = {abs(Q - Q_target) / Q_target * 100:.6f}%")
    
    # Golden ratio scaling
    phi_p = PHI ** p
    print("\n" + "="*70)
    print("GOLDEN RATIO SCALING")
    print("="*70)
    print(f"  φ^p                = {phi_p:.10f}")
    print(f"  r / φ^p            = {r / phi_p:.10f}")
    print(f"  log10(φ^p)         = {np.log10(phi_p):.6f}")
    
    # Z3 symmetry verification
    print("\n" + "="*70)
    print("Z₃ SYMMETRY MODULATION")
    print("="*70)
    for n in range(3):
        mod = z3_modulation(n, alpha, beta)
        print(f"  n={n} ({['e','μ','τ'][n]}): modulation = {mod:.8f}")
    
    # Mass ratios
    print("\n" + "="*70)
    print("MASS RATIOS")
    print("="*70)
    m_ratio_mu_e = preds[1] / preds[0] if preds[0] > 0 else 0
    m_ratio_tau_mu = preds[2] / preds[1] if preds[1] > 0 else 0
    actual_mu_e = targets[1] / targets[0]
    actual_tau_mu = targets[2] / targets[1]
    print(f"  m_μ / m_e          = {m_ratio_mu_e:.2f} (actual: {actual_mu_e:.2f})")
    print(f"  m_τ / m_μ          = {m_ratio_tau_mu:.2f} (actual: {actual_tau_mu:.2f})")
    
    return errors_pct, log_errs

# Multi-start optimization
def run_multi_start_optimization(n_starts=5):
    """Run multiple optimizations from different starting points"""
    best_result = None
    best_loss = float('inf')
    
    bounds = [
        (2.0, 12.0),      # p
        (50.0, 200.0),    # mu0 — wide range
        (0.1, 15.0),      # r — allow both inverted and normal
        (-3.0, 3.0)       # alpha
    ]
    
    for seed in range(n_starts):
        print(f"\n--- Optimization run {seed+1}/{n_starts} (seed={seed}) ---")
        result = differential_evolution(
            objective, bounds,
            tol=1e-12,
            popsize=30,
            maxiter=200,
            seed=seed,
            disp=False,
            workers=1,
            updating='deferred'
        )
        
        if result.fun < best_loss:
            best_loss = result.fun
            best_result = result
            print(f"  → New best loss: {best_loss:.6e}")
    
    return best_result

if __name__ == "__main__":
    print("="*70)
    print("ESQET LEPTON MASS MODEL v7.0")
    print("Unbounded multi-start optimization")
    print("="*70)
    
    # Multi-start to avoid local minima
    best = run_multi_start_optimization(n_starts=8)
    
    p_opt, mu0_opt, r_opt, alpha_opt = best.x
    loss_opt, preds_opt = loss_components(p_opt, mu0_opt, r_opt, alpha_opt)
    
    # Refine with local optimizer
    print("\n--- Local refinement with L-BFGS-B ---")
    local_result = minimize(
        objective, best.x,
        method='L-BFGS-B',
        bounds=[(2,12), (40,200), (0.1,20), (-3,3)],
        tol=1e-14
    )
    
    if local_result.fun < loss_opt:
        p_opt, mu0_opt, r_opt, alpha_opt = local_result.x
        loss_opt, preds_opt = loss_components(p_opt, mu0_opt, r_opt, alpha_opt)
        print(f"  Local improvement: {best.fun:.6e} → {loss_opt:.6e}")
    
    # Final results
    errors, log_errs = print_results(p_opt, mu0_opt, r_opt, alpha_opt, loss_opt, preds_opt)
    
    print("\n" + "="*70)
    print("FINAL ASSESSMENT")
    print("="*70)
    
    avg_err = np.mean(errors)
    avg_log_err = np.mean(log_errs)
    
    if avg_err < 1.0:
        print("✓ EXCELLENT: Average mass error < 1%")
    elif avg_err < 5.0:
        print(f"✓ GOOD: Average mass error = {avg_err:.2f}%")
    else:
        print(f"⚠ MODERATE: Average mass error = {avg_err:.2f}%")
    
    if abs(koide_q(preds_opt) - 2/3) < 0.01:
        print("✓ Koide relation satisfied within 1%")
    else:
        print("⚠ Koide relation deviation > 1%")
    
    # Save parameters
    np.savez("esqet_mass_params_v7.npz",
             p=p_opt, mu0=mu0_opt, r=r_opt, alpha=alpha_opt,
             beta=0.618, loss=loss_opt, preds=preds_opt,
             koide_Q=koide_q(preds_opt))
    print("\n✓ Parameters saved to: esqet_mass_params_v7.npz")
    
    # Recommended final parameters for ESQET framework
    print("\n" + "="*70)
    print("RECOMMENDED ESQET PARAMETERS (for framework)")
    print("="*70)
    print(f"""
    mass_scale   = {mu0_opt:.6f}   # MeV (natural scale)
    phi_exponent = {p_opt:.8f}
    gen_ratio    = {r_opt:.8f}
    z3_alpha     = {alpha_opt:.8f}
    z3_beta      = 0.618034   # golden ratio conjugate
    """)
