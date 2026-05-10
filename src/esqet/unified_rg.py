#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from numpy.polynomial.polynomial import polyroots

# ====================== CONSTANTS ======================
phi = (1 + np.sqrt(5)) / 2
roots = polyroots([-1, -1, -1, 1])
tau = [r.real for r in roots if abs(r.imag) < 1e-10 and r.real > 1][0]

# ====================== BETA FUNCTIONS ======================
def beta_fib(t, g):
    return 1 + 1/g - g

def beta_trib(t, g):
    return 1 + 1/g + 1/g**2 - g

# ====================== ANALYSIS ======================
def run_unified_analysis():
    t_span = (0, 10)
    t_eval = np.linspace(0, 10, 500)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Fibonacci Flow
    for g0 in [0.5, 3.0]:
        sol = solve_ivp(beta_fib, t_span, [g0], t_eval=t_eval)
        ax1.plot(sol.t, sol.y[0], label=f'g0={g0}')
    ax1.axhline(phi, color='gold', ls='--', label=f'φ ≈ {phi:.4f}')
    ax1.set_title("Fibonacci RG Flow (2-Step Memory)")
    ax1.legend()

    # Tribonacci Flow
    for g0 in [0.5, 3.0]:
        sol = solve_ivp(beta_trib, t_span, [g0], t_eval=t_eval)
        ax2.plot(sol.t, sol.y[0], label=f'g0={g0}')
    ax2.axhline(tau, color='gold', ls='--', label=f'τ ≈ {tau:.4f}')
    ax2.set_title("Tribonacci RG Flow (3-Step Memory)")
    ax2.legend()

    plt.tight_layout()
    plt.savefig('simulations/unified_rg_v200.png')
    
    print("="*50)
    print("ESQET v200: UNIFIED RG COMPLETE")
    print("="*50)
    print(f"Golden Ratio φ: {phi:.6f}")
    print(f"Tribonacci τ:   {tau:.6f}")
    print("Check 'simulations/unified_rg_v200.png' for visual confirmation.")

if __name__ == "__main__":
    run_unified_analysis()
