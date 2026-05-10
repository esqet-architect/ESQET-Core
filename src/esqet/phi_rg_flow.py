#!/usr/bin/env python3
"""
ESQET v181 — The RG Flow Machine
Derives phi as a fixed point attractor of the scaling beta-function.
Fixed: Matplotlib math parsing for labels.
"""

import numpy as np
import matplotlib.pyplot as plt

def beta(g):
    """The beta-function for additive scale recursion."""
    return 1 + (1/g) - g

def simulate_flow(g_start, steps=50, dt=0.1):
    g = g_start
    path = [g]
    for _ in range(steps):
        dg = beta(g) * dt
        g += dg
        path.append(g)
    return np.array(path)

# Attractor Analysis
phi = (1 + np.sqrt(5)) / 2
g_values = np.linspace(0.5, 3.0, 500)
beta_values = beta(g_values)

# Trajectories
t_low = simulate_flow(0.8)
t_high = simulate_flow(2.8)

plt.figure(figsize=(10, 6))

# Use raw strings for LaTeX and handle $ signs carefully
plt.plot(g_values, beta_values, 'k-', label=r'Beta Function $\beta(g)$')
plt.axhline(0, color='red', lw=1)
plt.axvline(phi, color='gold', ls='--', label=rf'Fixed Point $\phi \approx {phi:.3f}$')

# Flow visualization
plt.plot(t_low, beta(t_low), 'bo', markersize=3, alpha=0.5, label='Flow from small scale')
plt.plot(t_high, beta(t_high), 'ro', markersize=3, alpha=0.5, label='Flow from large scale')

plt.title("ESQET v181: The RG Flow Attractor")
plt.xlabel("Scaling Ratio (g)")
plt.ylabel("Rate of Change (Beta)")
plt.legend()
plt.grid(True, alpha=0.2)

# Save and Show
plt.savefig('simulations/phi_rg_flow_attractor.png')
print(f"Fixed point discovered at g = {t_low[-1]:.6f}")
print("✓ ESQET v181: Execution successful. Artifact saved.")
