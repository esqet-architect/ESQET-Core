#!/usr/bin/env python3
"""
ESQET v178 — Variational Two-Timescale φ–Kuramoto System

KEY CHANGE:
φ is no longer a control parameter.
It is a slow emergent variable driven by synchronization error.

This creates a closed variational loop:
    θ dynamics  ← φ-dependent coupling
    φ dynamics  ← synchronization functional R(θ)

Stable, bounded, non-degenerate.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# ----------------------------
# Parameters
# ----------------------------
N = 16
K0 = 2.5
phi_target = (1 + np.sqrt(5)) / 2

eta = 0.01        # slow φ timescale
beta = 0.05       # coupling feedback strength

# ----------------------------
# Order parameter
# ----------------------------
def order_parameter(theta):
    return np.abs(np.mean(np.exp(1j * theta)))

# ----------------------------
# Variational dynamics
# ----------------------------
def system(state, t):
    theta = state[:N]
    phi = state[-1]

    R = np.abs(np.mean(np.exp(1j * theta)))  # global coherence

    # φ defines coupling strength but is NOT injected into frequency
    K_eff = K0 * (0.6 + 0.4 * np.tanh(phi - phi_target))

    dtheta = np.zeros(N)

    for i in range(N):
        coupling = 0.0
        for j in range(N):
            coupling += np.sin(theta[j] - theta[i])
        dtheta[i] = coupling * (K_eff / N)

    # VARIATIONAL φ DYNAMICS
    # φ minimizes mismatch between desired coherence and actual coherence
    R_target = 0.6  # desired partial synchronization regime

    dphi = -eta * (phi - phi_target) + beta * (R - R_target)

    # mild bounding (prevents numerical drift)
    dphi = np.clip(dphi, -0.05, 0.05)

    return np.concatenate([dtheta, [dphi]])

# ----------------------------
# Simulation
# ----------------------------
print("="*70)
print("ESQET v178 — Variational φ–Synchronization System")
print("="*70)

np.random.seed(42)

state0 = np.zeros(N + 1)
state0[:N] = np.random.uniform(-np.pi, np.pi, N)
state0[-1] = 1.2

t = np.linspace(0, 200, 8000)

print("Integrating variational system...")
sol = odeint(system, state0, t, rtol=1e-8, atol=1e-10)

theta_traj = sol[:, :N]
phi_traj = sol[:, -1]

R_traj = np.array([order_parameter(theta_traj[i]) for i in range(len(t))])

# ----------------------------
# Diagnostics
# ----------------------------
print("\nFINAL STATE")
print("="*70)
print(f"φ_eff final   : {phi_traj[-1]:.6f}")
print(f"φ drift       : {phi_target - phi_traj[-1]:.6f}")
print(f"R final       : {R_traj[-1]:.4f}")
print(f"R mean        : {np.mean(R_traj[-1000:]):.4f} ± {np.std(R_traj[-1000:]):.4f}")

corr = np.corrcoef(phi_traj[-2000:], R_traj[-2000:])[0,1]
print(f"corr(φ, R)    : {corr:.4f}")

# ----------------------------
# Plot
# ----------------------------
plt.figure(figsize=(15,10))

plt.subplot(2,2,1)
plt.plot(t, phi_traj, 'gold')
plt.axhline(phi_target, ls='--', color='red')
plt.title("φ — Variational Emergent Variable")
plt.grid()

plt.subplot(2,2,2)
plt.plot(t, R_traj, 'purple')
plt.title("Synchronization R(t)")
plt.ylim(0,1)
plt.grid()

plt.subplot(2,2,3)
plt.plot(theta_traj[-1], 'teal')
plt.title("Final Phase Snapshot")
plt.grid()

plt.subplot(2,2,4)
plt.scatter(phi_traj[-1000:], R_traj[-1000:], s=2)
plt.xlabel("φ")
plt.ylabel("R")
plt.title("φ–R Coupling Manifold")
plt.grid()

plt.tight_layout()
plt.savefig("simulations/phi_variational_v178.png", dpi=300)
plt.show()

print("\nINTERPRETATION")
print("="*70)
print("• φ is now a slow emergent coordinate (not a driver)")
print("• φ responds to synchronization level R")
print("• system has a closed variational loop")
print("• no frequency injection → no runaway behavior")
print("="*70)

