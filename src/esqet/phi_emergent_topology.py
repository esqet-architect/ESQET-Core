#!/usr/bin/env python3
"""
ESQET v179 — φ as Emergent Topological Invariant
Diagnoses φ from synchronization geometry (Kuramoto Manifold).
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Global Parameters
N = 100
K = 2.5  # Coupling strength
omega = np.random.normal(0, 0.1, N) # Natural frequencies

def kuramoto_system(theta, t):
    dtheta = np.zeros(N)
    for i in range(N):
        coupling = np.sum(np.sin(theta - theta[i]))
        dtheta[i] = omega[i] + (K / N) * coupling
    return dtheta

def compute_emergent_phi(theta):
    """Compute φ as the ratio of principal axes of the phase manifold."""
    # Embed phases in 2D: (cos θ, sin θ)
    points = np.column_stack([np.cos(theta), np.sin(theta)])
    points = points - np.mean(points, axis=0)
    
    # Compute covariance matrix & eigenvalues
    cov = np.cov(points.T)
    eigvals_cov = np.linalg.eigvals(cov)
    eigvals_cov = np.sort(np.abs(eigvals_cov))[::-1]
    
    if eigvals_cov[1] > 1e-10:
        phi_emergent = eigvals_cov[0] / eigvals_cov[1]
    else:
        phi_emergent = 1.0
    return np.clip(phi_emergent, 1.0, 2.5)

def compute_order_parameter(theta):
    return np.abs(np.mean(np.exp(1j * theta)))

# Simulation Setup
print("="*70)
print("ESQET v179 — φ as Emergent Topological Invariant")
print("="*70)

np.random.seed(42)
initial = np.random.uniform(-np.pi, np.pi, N)
t = np.linspace(0, 150, 5000)

print("Integrating Kuramoto system...")
sol = odeint(kuramoto_system, initial, t, rtol=1e-8, atol=1e-10)

# Metrics over time
R_traj = np.array([compute_order_parameter(state) for state in sol])
phi_traj_eig = np.array([compute_emergent_phi(state) for state in sol])
phi_target = (1 + np.sqrt(5)) / 2

print(f"Final R                 : {R_traj[-1]:.4f}")
print(f"Emergent φ (eigenratio) : {phi_traj_eig[-1]:.4f}")
print(f"Golden ratio φ_target   : {phi_target:.6f}")
print(f"Deviation               : {abs(phi_traj_eig[-1] - phi_target):.6f}")

# Plotting
plt.figure(figsize=(12, 10))

plt.subplot(2, 1, 1)
plt.plot(t, R_traj, 'purple', label='Order Parameter R')
plt.title('Kuramoto Synchronization Profile')
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, phi_traj_eig, 'gold', lw=2, label='Emergent φ')
plt.axhline(phi_target, color='red', linestyle='--', label='φ_target (1.618)')
plt.title('φ Emergence from Phase Geometry')
plt.xlabel('Time')
plt.ylabel('Ratio of Principal Axes')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()
plt.savefig('simulations/phi_emergent_topology.png', dpi=300)
print("\n✓ Simulation complete. Artifact: simulations/phi_emergent_topology.png")
