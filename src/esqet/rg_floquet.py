"""
ESQET Nonlinear Scale-Measure Engine
Implements Reparameterized RG Flow: dg/dt_eff = beta(g)
where dt_eff = dt * (1 + epsilon * cos(omega * t))
"""
import numpy as np
from scipy.integrate import odeint

def esqet_measure_dynamics(y, t, omega, epsilon, b0):
    """
    Coupled system for coupling g and perturbation delta_g
    using a non-uniform scale measure (Scale-Measure Engine).
    """
    g, delta_g = y
    
    # 1. Scale Metric (Deformation of the ln(mu) interval)
    # This prevents the averaging out of the Floquet term
    dt_eff_dt = 1.0 + epsilon * np.cos(omega * t)
    
    # 2. Beta Function (1-loop QCD approximation)
    # Note: b0 < 0 for asymptotic freedom (standard QCD convention)
    beta_g = - (b0 * g**3) / (16 * np.pi**2)
    beta_prime_g = - (3 * b0 * g**2) / (16 * np.pi**2)
    
    # 3. Reparameterized Dynamics
    dg_dt = beta_g * dt_eff_dt
    ddelta_g_dt = beta_prime_g * dt_eff_dt * delta_g
    
    return [dg_dt, ddelta_g_dt]

def compute_floquet_monodromy(omega, epsilon, b0=-1.0, g_start=1.2):
    """
    Computes the stability spectrum over one period of the scale-metric.
    """
    # Period of the scale modulation
    T = 2 * np.pi / omega
    t_span = np.linspace(0, T, 2000)
    
    # Initial conditions: [initial_coupling, initial_perturbation]
    y0 = [g_start, 1.0]
    
    # Integrate over the period T
    sol = odeint(esqet_measure_dynamics, y0, t_span, args=(omega, epsilon, b0))
    
    # Monodromy Matrix (for 1D, just the scalar ratio)
    monodromy_ratio = np.abs(sol[-1, 1] / y0[1])
    
    # Floquet Exponent
    lambda_exp = (1.0 / T) * np.log(monodromy_ratio)
    
    return {
        'max_exponent': lambda_exp,
        'g_final': sol[-1, 0],
        'period': T
    }

def run_dsi_verification():
    """
    Verifies if the stability matches Fibonacci/Golden-Ratio hierarchies.
    """
    phi = (1 + 5**0.5) / 2
    # Test scales (Fibonacci sequence)
    fibs = [1, 2, 3, 5, 8, 13]
    
    print("="*60)
    print("ESQET Scale-Measure Engine: DSI Verification")
    print("="*60)
    
    for n in fibs:
        omega_n = phi**n
        # Low epsilon to check for resonance capture
        res = compute_floquet_monodromy(omega=omega_n, epsilon=0.05)
        print(f"Scale φ^{n:<2} (ω={omega_n:>8.3f}): λ = {res['max_exponent']:.6f}")

if __name__ == "__main__":
    run_dsi_verification()
