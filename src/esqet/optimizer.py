import numpy as np
from scipy.optimize import minimize
from calibration_map import SM_DATA

PHI = (1 + np.sqrt(5)) / 2
OMEGA = np.exp(1j * 2 * np.pi / 3)

def f_n(n):
    """Z3-derived exponent modulation."""
    return n * ((2 * np.pi / 3) / np.log(PHI))

def esqet_variational_manifold(params):
    """
    dimensionless manifold -> physical projection.
    params: [p_scale, lambda_unit, vacuum_base]
    """
    p, lam, base = params
    
    def get_mass(n):
        phase = OMEGA ** (f_n(n) % 3)
        # Fix 1: Ensure geometric stability
        geometry = (PHI ** (n * p)) * (np.real(phase) + 1.0)
        # Fix 2: Explicit separation of unit and structure
        return base + (lam * geometry)

    return {
        "electron": get_mass(0),
        "muon":     get_mass(1),
        "tau":      get_mass(2)
    }

def objective(params):
    """
    Fix 3: Relative Loss Functional (Energy Functional).
    L = sum((pred - exp) / exp)^2
    This is scale-invariant and prevents Tau-domination.
    """
    preds = esqet_variational_manifold(params)
    
    total_energy = 0
    for k, actual in SM_DATA.items():
        # Avoid zero division and enforce positivity
        pred_val = np.maximum(preds[k], 1e-9)
        relative_error = (pred_val - actual) / actual
        total_energy += relative_error**2
        
    return np.sqrt(total_energy)

# --- Constrained Optimization ---
# Constraints: p > 0, lam > 0, base >= 0
cons = ({'type': 'ineq', 'fun': lambda x: x[0]},
        {'type': 'ineq', 'fun': lambda x: x[1]},
        {'type': 'ineq', 'fun': lambda x: x[2]})

initial_guess = [5.8, 1.0, 0.5]
res = minimize(objective, initial_guess, method='SLSQP', constraints=cons)

if __name__ == "__main__":
    p_opt, l_opt, b_opt = res.x
    final_preds = esqet_variational_manifold(res.x)
    
    print(f"--- VARIATIONAL FIXED POINT LOCATED ---")
    print(f"Optimal Exponent (p): {p_opt:.6f}")
    print(f"Coupling Constant (λ): {l_opt:.6f}")
    print(f"Vacuum Energy (base): {b_opt:.6f}")
    print(f"Functional Energy (L): {res.fun:.6f}\n")

    print(f"{'Particle':<10} | {'Predicted (MeV)':<15} | {'Actual (MeV)':<15} | {'Error %'}")
    print("-" * 65)
    for k, actual in SM_DATA.items():
        pred = final_preds[k]
        err = abs(pred - actual) / actual * 100
        print(f"{k.capitalize():<10} | {pred:<15.4f} | {actual:<15.4f} | {err:.2f}%")
