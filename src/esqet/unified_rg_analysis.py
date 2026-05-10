#!/usr/bin/env python3
"""
ESQET v190 — Unified RG Analysis
Integrates Discrete Lattice, Continuous Flow, and Stability Phase Portrait.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Physical Constants
phi = (1 + np.sqrt(5)) / 2

def beta(t, g):
    # Continuous flow: dg/d(ln s) = 1 + 1/g - g
    return 1 + (1/g) - g

def run_analysis():
    print("="*70)
    print("ESQET v190: SCALE INVARIANCE & RG STABILITY")
    print("="*70)

    # 1. Discrete Convergence (Binet Decay)
    print("\n1. DISCRETE CONVERGENCE (Ratio Error Decay)")
    F = [1, 1]
    for _ in range(12): F.append(F[-1] + F[-2])
    
    print(f"{'k':>2} | {'Ratio':>12} | {'Error vs φ':>12} | {'Theoretical Decay'}")
    for k in range(1, len(F)-1):
        ratio = F[k+1] / F[k]
        error = abs(ratio - phi)
        decay = (1/phi**2)**k
        print(f"{k+1:2d} | {ratio:12.8f} | {error:12.4e} | {decay:12.4e}")

    # 2. Phase Portrait Visualization
    g_range = np.linspace(0.4, 3.0, 300)
    beta_vals = beta(0, g_range)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot 1: The Beta Function Landscape
    ax1.plot(g_range, beta_vals, 'b-', lw=2)
    ax1.axhline(0, color='black', alpha=0.5)
    ax1.axvline(phi, color='gold', ls='--', label=f'Fixed Point φ={phi:.4f}')
    
    # Add flow arrows
    x_arrows = np.linspace(0.5, 2.8, 15)
    y_arrows = beta(0, x_arrows)
    for x, y in zip(x_arrows, y_arrows):
        direction = 0.2 if y > 0 else -0.2
        ax1.arrow(x, 0, direction, 0, head_width=0.05, head_length=0.05, fc='k', ec='k', alpha=0.4)

    ax1.set_title("The Vacuum Potential: Beta Function Phase Portrait")
    ax1.set_xlabel("Scaling Ratio (g)")
    ax1.set_ylabel("dg/dln(s)")
    ax1.legend()

    # Plot 2: Continuous Trajectories (Log-Scale Flow)
    t_span = (0, 7)
    t_eval = np.linspace(0, 7, 500)
    for g0 in [0.5, 1.0, 2.5, 3.0]:
        sol = solve_ivp(beta, t_span, [g0], t_eval=t_eval)
        ax2.plot(sol.t, sol.y[0], label=f'Start g0={g0}')

    ax2.axhline(phi, color='gold', ls='--')
    ax2.set_title("Continuous Scale Flow Toward Infrared Fixed Point")
    ax2.set_xlabel("ln(s) [Log-Scale]")
    ax2.set_ylabel("Effective Ratio g(s)")
    ax2.legend()

    plt.tight_layout()
    plt.savefig('simulations/unified_rg_analysis.png')
    print("\n✓ Analysis complete. Phase portrait saved to simulations/unified_rg_analysis.png")

if __name__ == "__main__":
    run_analysis()
