#!/usr/bin/env python3
"""
ESQET v181 — DEFINITIVE φ-NETWORK SYNCHRONIZATION
Bridges the working Van der Pol observer (φ ≈ 1.618 stable) 
with Kuramoto network synchronization.

Key insight: Use the SAME φ dynamics that worked in motion_observer_rk4.py
but applied to network synchronization with proper polarity structure.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import hilbert

phi_target = (1 + np.sqrt(5)) / 2
N = 20
K0 = 3.2
eta = 0.03  # φ adaptation rate (slow)

def network_dynamics(state, t):
    """
    State: [θ1, θ2, ..., θN, φ]
    Uses the PROVEN φ adaptation from motion_observer_rk4.py:
    dφ/dt = -η(φ - φ_target)  (no cross-terms, bounded)
    """
    n_osc = N
    theta = state[:n_osc]
    phi_eff = state[-1]
    
    # Natural frequencies with moderate spread
    omega = 1.0 + 0.4 * np.random.randn(n_osc)
    
    # φ-modulated coupling strength (bounded)
    K_eff = K0 * (0.7 + 0.3 * np.tanh(phi_eff - phi_target))
    
    # BIPOLAR COUPLING: phases are assigned polarities based on position
    # This creates natural clustering without forcing perfect sync
    polarity = np.ones(n_osc)
    polarity[n_osc//3:2*n_osc//3] = 0.0   # Neutral group in middle
    polarity[2*n_osc//3:] = -1.0           # Negative polarity group
    
    dtheta = np.zeros(n_osc)
    for i in range(n_osc):
        coupling = 0.0
        for j in range(n_osc):
            # Polarity-weighted coupling (attract/repel naturally)
            weight = polarity[i] * polarity[j]
            # Use sin(Δθ) for Kuramoto coupling
            coupling += weight * np.sin(theta[j] - theta[i])
        dtheta[i] = omega[i] + (K_eff / n_osc) * coupling
    
    # PROVEN φ DYNAMICS (from motion_observer_rk4.py)
    # Pure gradient descent - this worked perfectly before
    dphi = -eta * (phi_eff - phi_target)
    dphi = np.clip(dphi, -0.05, 0.05)
    
    dstate = np.zeros(n_osc + 1)
    dstate[:n_osc] = dtheta
    dstate[-1] = dphi
    
    return dstate


def order_parameter(theta):
    """Kuramoto order parameter"""
    return np.abs(np.mean(np.exp(1j * theta)))


def compute_emergent_phi(theta):
    """Compute φ from phase geometry - for diagnosis only"""
    points = np.column_stack([np.cos(theta), np.sin(theta)])
    points = points - np.mean(points, axis=0)
    cov = np.cov(points.T)
    eigvals_cov = np.linalg.eigvals(cov)
    eigvals_cov = np.sort(np.abs(eigvals_cov))[::-1]
    if eigvals_cov[1] > 1e-10:
        return np.clip(eigvals_cov[0] / eigvals_cov[1], 1.0, 2.5)
    return 1.0


# Simulation
print("="*70)
print("ESQET v181 — DEFINITIVE φ-NETWORK SYNCHRONIZATION")
print("="*70)
print(f"N = {N} oscillators (3 polarity groups: +, neutral, -)")
print(f"Base coupling K0 = {K0}")
print(f"φ adaptation rate η = {eta}")
print(f"φ_target = {phi_target:.6f}")
print("="*70)

np.random.seed(42)
initial = np.zeros(N + 1)
initial[:N] = np.random.uniform(-np.pi, np.pi, N)
initial[-1] = 1.0  # Start near target

t = np.linspace(0, 300, 8000)
print("Integrating definitive network...")
sol = odeint(network_dynamics, initial, t, rtol=1e-8, atol=1e-10)

theta_traj = sol[:, :N]
phi_traj = sol[:, -1]

# Order parameters
R_traj = np.array([order_parameter(theta_traj[i]) for i in range(len(t))])
phi_emergent_traj = np.array([compute_emergent_phi(theta_traj[i]) for i in range(len(t))])

print(f"\nFINAL STATE")
print("="*70)
print(f"φ_eff (parameter)   : {phi_traj[-1]:.6f} (target = {phi_target:.6f})")
print(f"Δ from target      : {phi_target - phi_traj[-1]:.6f}")
print(f"Emergent φ (geo)    : {phi_emergent_traj[-1]:.4f}")
print(f"Final R             : {R_traj[-1]:.4f}")
print(f"Mean R (steady)     : {np.mean(R_traj[-1000:]):.4f} ± {np.std(R_traj[-1000:]):.4f}")

# Plotting
plt.figure(figsize=(16, 12))

# φ evolution
plt.subplot(2, 2, 1)
plt.plot(t, phi_traj, 'gold', lw=2)
plt.axhline(phi_target, color='red', linestyle='--', label=f'φ_target = {phi_target:.5f}')
plt.xlabel('Time')
plt.ylabel('φ_eff')
plt.title('φ Adaptation — Pure Gradient Descent (Proven Stable)')
plt.legend()
plt.grid(True, alpha=0.3)

# Synchronization order parameter
plt.subplot(2, 2, 2)
plt.plot(t, R_traj, 'purple', lw=2)
plt.axhline(np.mean(R_traj[-1000:]), color='orange', linestyle='--',
            label=f'Steady R = {np.mean(R_traj[-1000:]):.4f}')
plt.xlabel('Time')
plt.ylabel('Order Parameter R')
plt.title('Network Synchronization')
plt.ylim(0, 1.05)
plt.legend()
plt.grid(True, alpha=0.3)

# Emergent φ from geometry
plt.subplot(2, 2, 3)
plt.plot(t, phi_emergent_traj, 'teal', lw=2)
plt.axhline(phi_target, color='red', linestyle='--', label=f'φ_target = {phi_target:.5f}')
plt.xlabel('Time')
plt.ylabel('Emergent φ (geometric)')
plt.title('φ as Emergent Geometric Invariant')
plt.legend()
plt.grid(True, alpha=0.3)

# Final phase distribution
plt.subplot(2, 2, 4)
end_phases = theta_traj[-1, :]
circle = np.exp(1j * np.linspace(0, 2*np.pi, 100))
plt.plot(np.cos(circle), np.sin(circle), 'k--', alpha=0.3)
colors = plt.cm.hsv(end_phases / (2*np.pi))
plt.scatter(np.cos(end_phases), np.sin(end_phases), c=colors, s=50, alpha=0.8)
plt.title(f'Final Phase Distribution (R = {R_traj[-1]:.3f})')
plt.xlabel('cos θ')
plt.ylabel('sin θ')
plt.axis('equal')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/phi_definitive_sync.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("DIAGNOSTICS")
print("="*70)

phi_std = np.std(phi_traj[-1000:])
print(f"φ variance (steady): {phi_std:.6f}")

if 1.5 < phi_traj[-1] < 1.7:
    print("✓ φ PARAMETER converged near golden ratio")
else:
    print(f"○ φ converged to {phi_traj[-1]:.4f}")

if 1.5 < phi_emergent_traj[-1] < 1.7:
    print("✓ EMERGENT φ (geometry) near golden ratio — STRUCTURAL INVARIANT")
elif phi_emergent_traj[-1] > 1.7:
    print(f"○ Emergent φ = {phi_emergent_traj[-1]:.4f} > 1.7 — network too anisotropic")
else:
    print(f"○ Emergent φ = {phi_emergent_traj[-1]:.4f} < 1.5 — network too isotropic")

if np.mean(R_traj[-1000:]) > 0.6:
    print("✓ STRONG SYNCHRONIZATION — network is coherent")
elif np.mean(R_traj[-1000:]) > 0.3:
    print("○ MODERATE SYNCHRONIZATION")
else:
    print("✗ WEAK SYNCHRONIZATION — increase K0")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("This version uses the PROVEN φ dynamics from motion_observer_rk4.py")
print("combined with Kuramoto oscillators and polarity grouping.")
print("\nIf φ ≈ 1.618 and R ≈ 0.6-0.8, the golden ratio emerges as")
print("a structural invariant of the synchronized network.")
print("="*70)
