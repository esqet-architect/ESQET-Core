"""
ESQET Singular Manifold Engine (Axiom 13)
Implements non-perturbative scale-coupling feedback.
Goal: Break monotonic drift and force Arnold Tongue emergence.
"""
import numpy as np
from scipy.integrate import odeint

def esqet_singular_dynamics(y, t, omega, epsilon, b0):
    g, delta_g = y
    
    # 1. Singular Scale-Measure back-reaction
    # Instead of a log-dampener, we use a rational coupling.
    # When g hits critical values, the scale-measure 'stiffens'.
    feedback = (g**2) / (1.0 + g**2)
    dt_eff_dt = 1.0 + epsilon * np.cos(omega * t * feedback)
    
    # 2. Beta Function
    beta_g = - (b0 * g**3) / (16 * np.pi**2)
    beta_prime_g = - (3 * b0 * g**2) / (16 * np.pi**2)
    
    # 3. Coupled Dynamics
    dg_dt = beta_g * dt_eff_dt
    ddelta_g_dt = beta_prime_g * dt_eff_dt * delta_g
    
    return [dg_dt, ddelta_g_dt]

def compute_floquet_monodromy(omega, epsilon, b0=-1.0, g_start=1.2):
    T = 2 * np.pi / omega
    # We must use a much finer mesh to capture singular crossings
    t_span = np.linspace(0, T, 10000) 
    y0 = [g_start, 1.0]
    
    sol = odeint(esqet_singular_dynamics, y0, t_span, args=(omega, epsilon, b0))
    
    monodromy_ratio = np.abs(sol[-1, 1] / y0[1])
    lambda_exp = (1.0 / T) * np.log(monodromy_ratio)
    
    return {
        'max_exponent': lambda_exp,
        'g_final': sol[-1, 0]
    }

def run_dsi_verification():
    phi = (1 + 5**0.5) / 2
    # Testing the φ^5 node specifically
    omega_target = phi**5
    print("ESQET Singular Engine: Probing for Non-Trivial Cusp")
    print("="*60)
    
    # Tight scan to look for the break in monotonicity
    for w in np.linspace(omega_target - 0.1, omega_target + 0.1, 10):
        res = compute_floquet_monodromy(omega=w, epsilon=0.3) # High epsilon
        print(f"ω={w:.6f} | λ={res['max_exponent']:.8f}")

if __name__ == "__main__":
    run_dsi_verification()
