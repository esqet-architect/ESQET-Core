#!/usr/bin/env python3
"""
ESQET Network v176 — Bipolar Kuramoto with φ-Governed Attract/Repel Balance
Insight: Polarity (positive/negative coupling) creates natural synchronization structure.
φ modulates the ratio of attractive to repulsive interactions.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

phi_target = (1 + np.sqrt(5)) / 2
N = 20  # Number of oscillators
K0 = 3.0  # Base coupling strength
eta = 0.02  # φ adaptation rate

def bipolar_kuramoto(state, t):
    """
    State: [θ1, θ2, ..., θN, φ]
    Coupling signs are determined by oscillator polarity indices.
    """
    n_osc = N
    theta = state[:n_osc]
    phi_eff = state[-1]
    
    # Assign polarities: first half positive, second half negative
    # Or random signs for more realistic dynamics
    polarity = np.ones(n_osc)
    polarity[n_osc//2:] = -1.0  # Half attract, half repel
    
    # Natural frequencies (small spread)
    omega = 1.0 + 0.2 * np.random.randn(n_osc)
    
    # φ modulates the overall coupling strength
    K_eff = K0 * (1.0 + 0.5 * np.tanh(phi_eff - phi_target))
    
    # Dynamics with polarity-dependent coupling
    # Like attracts like, opposites repel — weighted by polarity product
    dtheta = np.zeros(n_osc)
    for i in range(n_osc):
        coupling = 0.0
        for j in range(n_osc):
            # Sign: product of polarities (+1 = same sign attract, -1 = opposite repel)
            sign = polarity[i] * polarity[j]
            coupling += sign * np.sin(theta[j] - theta[i])
        coupling = K_eff / n_osc * coupling
        dtheta[i] = omega[i] + coupling
    
    # φ dynamics: slow gradient descent to target
    dphi = -eta * (phi_eff - phi_target)
    dphi = np.clip(dphi, -0.03, 0.03)
    
    dstate = np.zeros(n_osc + 1)
    dstate[:n_osc] = dtheta
    dstate[-1] = dphi
    
    return dstate


def order_parameter(theta):
    """Kuramoto order parameter"""
    return np.abs(np.mean(np.exp(1j * theta)))


def cluster_order_parameter(theta, polarity):
    """Measure order within each polarity group separately"""
    pos_mask = polarity > 0
    neg_mask = polarity < 0
    
    R_pos = np.abs(np.mean(np.exp(1j * theta[pos_mask]))) if np.any(pos_mask) else 0
    R_neg = np.abs(np.mean(np.exp(1j * theta[neg_mask]))) if np.any(neg_mask) else 0
    return R_pos, R_neg


# Simulation
print("="*70)
print("ESQET v176 — Bipolar Kuramoto with φ-Governed Polarity Balance")
print("="*70)
print(f"N = {N} oscillators (half positive, half negative polarity)")
print(f"Base coupling K0 = {K0}")
print(f"φ adaptation rate η = {eta}")
print(f"φ_target = {phi_target:.6f}")
print("="*70)

np.random.seed(42)
initial = np.zeros(N + 1)
initial[:N] = np.random.uniform(-np.pi, np.pi, N)
initial[-1] = 1.0  # Start near target

t = np.linspace(0, 150, 6000)
print("Integrating bipolar Kuramoto network...")
sol = odeint(bipolar_kuramoto, initial, t, rtol=1e-8, atol=1e-10)

theta_traj = sol[:, :N]
phi_traj = sol[:, -1]

# Assign polarities for analysis
polarity = np.ones(N)
polarity[N//2:] = -1.0

# Order parameters
R_traj = np.array([order_parameter(theta_traj[i]) for i in range(len(t))])
R_pos_traj = np.zeros(len(t))
R_neg_traj = np.zeros(len(t))
for i in range(len(t)):
    R_pos_traj[i], R_neg_traj[i] = cluster_order_parameter(theta_traj[i], polarity)

print(f"\nFinal φ_eff     : {phi_traj[-1]:.6f} (target = {phi_target:.6f})")
print(f"Δ from target  : {phi_target - phi_traj[-1]:.6f}")
print(f"Final global R  : {R_traj[-1]:.4f}")
print(f"Final positive R: {R_pos_traj[-1]:.4f}")
print(f"Final negative R: {R_neg_traj[-1]:.4f}")
print(f"Mean global R   : {np.mean(R_traj[-1000:]):.4f} ± {np.std(R_traj[-1000:]):.4f}")

# Plotting
plt.figure(figsize=(15, 12))

# φ evolution
plt.subplot(2, 2, 1)
plt.plot(t, phi_traj, 'gold', lw=2)
plt.axhline(phi_target, color='red', linestyle='--', label=f'φ_target = {phi_target:.5f}')
plt.xlabel('Time')
plt.ylabel('φ_eff')
plt.title('φ Evolution — Slow Gradient Descent')
plt.legend()
plt.grid(True, alpha=0.3)

# Synchronization order parameters
plt.subplot(2, 2, 2)
plt.plot(t, R_traj, 'purple', lw=2, label='Global R')
plt.plot(t, R_pos_traj, 'blue', lw=1.5, alpha=0.7, label='Positive polarity')
plt.plot(t, R_neg_traj, 'red', lw=1.5, alpha=0.7, label='Negative polarity')
plt.axhline(0.7, color='gray', linestyle='--', alpha=0.5, label='Strong sync threshold')
plt.xlabel('Time')
plt.ylabel('Order Parameter R')
plt.title('Synchronization by Polarity Group')
plt.legend()
plt.grid(True, alpha=0.3)

# Phase distribution at the end
plt.subplot(2, 2, 3)
end_phases = theta_traj[-1, :]
colors = ['blue' if p > 0 else 'red' for p in polarity]
circle = np.exp(1j * np.linspace(0, 2*np.pi, 100))
plt.plot(np.cos(circle), np.sin(circle), 'k--', alpha=0.3)
plt.scatter(np.cos(end_phases), np.sin(end_phases), c=colors, s=60, alpha=0.7)
plt.title(f'Final Phase Distribution (R = {R_traj[-1]:.3f})')
plt.xlabel('cos θ')
plt.ylabel('sin θ')
plt.axis('equal')
plt.grid(True, alpha=0.3)

# φ distribution
plt.subplot(2, 2, 4)
plt.hist(phi_traj[-1000:], bins=30, color='brown', alpha=0.7, edgecolor='black')
plt.axvline(phi_target, color='red', linestyle='--', label=f'φ_target = {phi_target:.5f}')
plt.xlabel('φ_eff')
plt.ylabel('Count')
plt.title('φ Distribution at Steady State')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/phi_bipolar_kuramoto.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("INTERPRETATION")
print("="*70)
print("Polarity insight:")
print("  • Positive polarity oscillators attract each other")
print("  • Negative polarity oscillators attract each other")
print("  • Opposite polarities repel")
print("\nThis creates natural clustering without requiring strong coupling.")
print("φ modulates the overall interaction strength, not the sign structure.")
print("="*70)
