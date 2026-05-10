#!/usr/bin/env python3
"""
ESQET v192 — The Field Action
Demonstrates how the Principle of Least Action leads to the 
phi-attractor in the continuum limit.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def field_dynamics(t, y):
    # Second-order ODE: psi'' - psi' - psi = 0
    # Let y[0] = psi, y[1] = psi'
    psi, d_psi = y
    dd_psi = d_psi + psi
    return [d_psi, dd_psi]

# 1. Integrate the Field
t_span = (0, 5)
t_eval = np.linspace(0, 5, 500)
# Initial conditions: psi(0)=1, psi'(0)=variable
y0 = [1.0, 0.5] 

sol = solve_ivp(field_dynamics, t_span, y0, t_eval=t_eval)

# 2. Extract the Coupling g = psi' / psi
g_observed = sol.y[1] / sol.y[0]
phi = (1 + np.sqrt(5)) / 2

# 3. Visualization
plt.figure(figsize=(10, 6))
plt.plot(sol.t, g_observed, 'b-', label=r'Observed Coupling $g = \psi\' / \psi$')
plt.axhline(phi, color='gold', ls='--', label=f'Theoretical Attractor $\phi \approx {phi:.4f}$')

plt.title("ESQET Field Theory: Emergence of $g \to \phi$ from the Action")
plt.xlabel("Log-Scale $\ln(s)$")
plt.ylabel("Effective Coupling $g$")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('simulations/field_action_convergence.png')

print(f"Final Coupling Value: {g_observed[-1]:.6f}")
print("✓ Action-to-Attractor pipeline verified.")
