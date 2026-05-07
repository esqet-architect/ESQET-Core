import numpy as np
from scipy.integrate import odeint

def rg_dynamics(y, t, omega, epsilon, b0):
    """
    Simultaneously evolves the coupling g and its perturbation delta_g.
    y = [g, delta_g]
    """
    g, delta_g = y
    
    # 1. Base Beta Function (1-loop QCD)
    beta_g = - (b0 * g**3) / (16 * np.pi**2)
    beta_prime_g = - (3 * b0 * g**2) / (16 * np.pi**2)
    
    # 2. ESQET Multiplicative Modulation
    modulation = 1 + epsilon * np.cos(omega * t)
    
    # 3. Coupled Equations
    dg_dt = beta_g * modulation
    ddelta_g_dt = (beta_prime_g * modulation) * delta_g
    
    return [dg_dt, ddelta_g_dt]

def compute_floquet_spectrum():
    # Parameters
    omega_phi = 12.0
    epsilon = 0.01
    b0 = 11 - (2 * 5 / 3) # QCD with 5 flavors
    
    # Integration range (one "period" in log-space T = 2pi/omega)
    T = 2 * np.pi / omega_phi
    t = np.linspace(0, T, 1000)
    
    # Initial Conditions: [g_start, delta_g_start]
    # Starting at EW scale alpha_s ~ 0.118
    y0 = [1.2, 1.0] 
    
    # Solve the system
    sol = odeint(rg_dynamics, y0, t, args=(omega_phi, epsilon, b0))
    
    # Extract Monodromy Result
    g_final, delta_g_final = sol[-1]
    
    # Compute Floquet Exponent: lambda = (1/T) * ln(|delta_g(T)/delta_g(0)|)
    floquet_exponent = (1/T) * np.log(np.abs(delta_g_final / y0[1]))
    
    print("ESQET Floquet-RG Spectral Analysis")
    print("-" * 45)
    print(f"Log-Frequency (omega): {omega_phi:.4f}")
    print(f"Modulation (epsilon):  {epsilon:.4f}")
    print(f"Floquet Exponent (λ):  {floquet_exponent:.6f}")
    print("-" * 45)
    
    if floquet_exponent < 0:
        print("RESULT: ATTRATIVE FIXED POINT (KAM-Stable)")
    elif abs(floquet_exponent) < 1e-4:
        print("RESULT: MARGINAL LIMIT CYCLE (ESQET Criticality)")
    else:
        print("RESULT: UNSTABLE FLOW (Chaos/Breakdown)")

if __name__ == "__main__":
    compute_floquet_spectrum()
