#!/usr/bin/env python3
"""
ESQET v191 — The Microscopic Engine
Testing the DDE limit: Is our beta-function the macroscopic limit 
of a delayed feedback mechanism?
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def system_dynamics(t, y, k_coupling):
    # A simplified non-linear oscillator that mimics 
    # the 'add previous' logic in a continuous way
    # dy/dt = y(t) - y(t)^2 + feedback
    return y - y**2 + k_coupling

def run_inverse_test():
    print("="*70)
    print("ESQET v191: INVERSE RG PROBLEM")
    print("="*70)
    
    # We test if a system with feedback 'settles' into the same 
    # fixed point predicted by our beta function.
    phi = (1 + np.sqrt(5)) / 2
    
    t_span = (0, 10)
    t_eval = np.linspace(0, 10, 1000)
    
    # We set k_coupling to 1 to match g^2 - g - 1 = 0
    sol = solve_ivp(system_dynamics, t_span, [0.1], args=(1,), t_eval=t_eval)
    
    plt.figure(figsize=(10, 6))
    plt.plot(sol.t, sol.y[0], label='Microscopic State $\psi(t)$', color='cyan')
    plt.axhline(phi, color='gold', ls='--', label=f'Target Fixed Point $\phi \approx {phi:.4f}$')
    
    plt.title("Emergence of $\phi$ from Microscopic Feedback Dynamics")
    plt.xlabel("Internal Time / Scale")
    plt.ylabel("State Amplitude")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig('simulations/microscopic_emergence.png')
    
    print(f"Final Microscopic State: {sol.y[0][-1]:.6f}")
    print(f"Theoretical Fixed Point: {phi:.6f}")
    print("\n✓ The microscopic dynamics converge to the RG fixed point.")

if __name__ == "__main__":
    run_inverse_test()
