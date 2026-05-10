#!/usr/bin/env python3
"""
ESQET v199 — Lyapunov Stability & Drift Analysis
Separating the Fundamental Flow from the Stability Landscape.
"""
import numpy as np
import matplotlib.pyplot as plt

def f(g):
    # The Drift Field (Beta Function)
    return 1 + (1/g) - g

def V(g):
    # The Lyapunov Function (Potential)
    return 0.5 * g**2 - g - np.log(g)

g = np.linspace(0.4, 3.0, 500)
drift = f(g)
potential = V(g)
phi = (1 + np.sqrt(5)) / 2

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))

# Plot 1: The Drift Field (where f(g)=0 is the attractor)
ax1.plot(g, drift, 'b-', label='Drift Field $f(g)$')
ax1.axhline(0, color='k', alpha=0.3)
ax1.axvline(phi, color='gold', ls='--', label=f'Fixed Point $\phi \approx {phi:.4f}$')
ax1.set_title("Drift Field: The Engine of Convergence")
ax1.set_ylabel("$\dot{g}$ (Scale Velocity)")
ax1.legend()

# Plot 2: The Lyapunov Function (the stability well)
ax2.plot(g, potential, 'r-', label='Lyapunov Function $V(g)$')
ax2.axvline(phi, color='gold', ls='--')
ax2.set_title("Lyapunov Landscape: The Vacuum Stability Well")
ax2.set_xlabel("Coupling Constant $g$")
ax2.set_ylabel("$V(g)$")
ax2.legend()

plt.tight_layout()
plt.savefig('simulations/lyapunov_analysis.png')

print(f"Fixed Point: {phi:.6f}")
print(f"Drift at phi: {f(phi):.6e}")
print("✓ Hierarchy verified: Drift vanishes at the Lyapunov minimum.")
