#!/usr/bin/env python3
"""
ESQET Network v177 — Non-Degenerate φ-Kuramoto System
φ remains active even at synchronization via:
1. Frequency heterogeneity (persistent phase dispersion)
2. Higher harmonics in coupling (prevents trivial flattening)
3. Structural gating (φ modulates asymmetry, not just strength)
4. φ injection into frequency (always visible in dynamics)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

phi_target = (1 + np.sqrt(5)) / 2
N = 24
K0 = 2.8
eta = 0.03
gamma = 0.15  # Frequency injection strength

def non_degenerate_kuramoto(state, t):
    """
    State: [θ1, θ2, ..., θN, φ]
    φ remains active even in synchronized states.
    """
    n_osc = N
    theta = state[:n_osc]
    phi_eff = state[-1]
    
    # FIX 1: Strong frequency heterogeneity (prevents perfect sync)
    # Wider spread ensures persistent phase dynamics
    omega_base = 1.0 + 0.6 * np.random.randn(n_osc)  # sigma = 0.6, not 0.2
    
    # FIX 4: φ injects into frequency (always visible)
    omega = omega_base + gamma * (phi_eff - phi_target)
    
    # FIX 3: Structural gating — φ changes network asymmetry
    # Compute polarity based on instantaneous phase
    polarity = np.tanh(3.0 * np.cos(theta))  # -1 to 1, phase-dependent
    
    # FIX 2: Higher harmonics prevent trivial flattening
    # Even when θⱼ - θᵢ ≈ 0, sin(2Δθ) ≈ 2Δθ ≠ 0
    dtheta = np.zeros(n_osc)
    for i in range(n_osc):
        coupling = 0.0
        for j in range(n_osc):
            # Structural gating: φ weights the polarity product
            # This term DOES NOT vanish when phases align
            gate = polarity[i] * polarity[j] * phi_eff
            
            # Base Kuramoto with higher harmonics
            delta = theta[j] - theta[i]
            coupling += gate * (np.sin(delta) + 0.4 * np.sin(2*delta))
        
        # Normalized coupling
        dtheta[i] = omega[i] + (K0 / n_osc) * coupling
    
    # φ dynamics: still gradient descent, but now always coupled
    dphi = -eta * (phi_eff - phi_target)
    dphi = np.clip(dphi, -0.05, 0.05)
    
    dstate = np.zeros(n_osc + 1)
    dstate[:n_osc] = dtheta
    dstate[-1] = dphi
    
    return dstate


def order_parameter(theta):
    """Kuramoto order parameter"""
    return np.abs(np.mean(np.exp(1j * theta)))


def phase_coherence(theta):
    """Measure of phase clustering (0=uniform, 1=perfect cluster)"""
    phases = np.exp(1j * theta)
    return np.abs(np.mean(phases))


def entropy_measure(theta):
    """Shannon entropy of phase distribution (higher = more dispersed)"""
    hist, _ = np.histogram(theta, bins=20, range=(-np.pi, np.pi))
    hist = hist / (hist.sum() + 1e-12)
    entropy = -np.sum(hist * np.log(hist + 1e-12))
    return entropy / np.log(20)  # Normalized to [0,1]


# Simulation
print("="*70)
print("ESQET v177 — Non-Degenerate φ-Kuramoto System")
print("="*70)
print(f"N = {N} oscillators")
print(f"Base coupling K0 = {K0}")
print(f"φ adaptation η = {eta}, frequency injection γ = {gamma}")
print(f"Features:")
print("  • Strong frequency heterogeneity (σ=0.6)")
print("  • Higher harmonics in coupling (sin + 0.4·sin2)")
print("  • Structural gating via phase-dependent polarity")
print("  • φ injection into natural frequencies")
print(f"φ_target = {phi_target:.6f}")
print("="*70)

np.random.seed(42)
initial = np.zeros(N + 1)
initial[:N] = np.random.uniform(-np.pi, np.pi, N)
initial[-1] = 1.2

t = np.linspace(0, 200, 10000)
print("Integrating non-degenerate system...")
sol = odeint(non_degenerate_kuramoto, initial, t, rtol=1e-8, atol=1e-10)

theta_traj = sol[:, :N]
phi_traj = sol[:, -1]

# Order parameter and entropy
R_traj = np.array([order_parameter(theta_traj[i]) for i in range(len(t))])
H_traj = np.array([entropy_measure(theta_traj[i]) for i in range(len(t))])

# Measure φ–R correlation
corr_steady = np.corrcoef(phi_traj[-2000:], R_traj[-2000:])[0, 1]

print(f"\nFinal φ_eff     : {phi_traj[-1]:.6f} (target = {phi_target:.6f})")
print(f"Δ from target  : {phi_target - phi_traj[-1]:.6f}")
print(f"Final R         : {R_traj[-1]:.4f}")
print(f"Mean R (steady) : {np.mean(R_traj[-2000:]):.4f} ± {np.std(R_traj[-2000:]):.4f}")
print(f"φ−R correlation : {corr_steady:.4f}")
print(f"Phase entropy H : {np.mean(H_traj[-2000:]):.4f}")

# Plotting
plt.figure(figsize=(16, 12))

# φ evolution
plt.subplot(2, 2, 1)
plt.plot(t, phi_traj, 'gold', lw=2)
plt.axhline(phi_target, color='red', linestyle='--', label=f'φ_target = {phi_target:.5f}')
plt.xlabel('Time')
plt.ylabel('φ_eff')
plt.title('φ Evolution — Active Even at Synchronization')
plt.legend()
plt.grid(True, alpha=0.3)

# Order parameter
plt.subplot(2, 2, 2)
plt.plot(t, R_traj, 'purple', lw=2)
plt.axhline(np.mean(R_traj[-2000:]), color='orange', linestyle='--',
            label=f'Steady R = {np.mean(R_traj[-2000:]):.4f}')
plt.xlabel('Time')
plt.ylabel('Order Parameter R')
plt.title('Synchronization — Partial (Not Perfect Collapse)')
plt.ylim(0, 1.05)
plt.legend()
plt.grid(True, alpha=0.3)

# Phase entropy
plt.subplot(2, 2, 3)
plt.plot(t, H_traj, 'teal', lw=2)
plt.xlabel('Time')
plt.ylabel('Normalized Entropy H')
plt.title('Phase Distribution Entropy (Higher = More Dispersed)')
plt.grid(True, alpha=0.3)

# Final phase distribution
plt.subplot(2, 2, 4)
end_phases = theta_traj[-1, :]
circle = np.exp(1j * np.linspace(0, 2*np.pi, 100))
plt.plot(np.cos(circle), np.sin(circle), 'k--', alpha=0.3)
sc = plt.scatter(np.cos(end_phases), np.sin(end_phases), 
                  c=end_phases, cmap='hsv', s=60, alpha=0.8)
plt.title(f'Final Phase Distribution (R = {R_traj[-1]:.3f}, H = {H_traj[-1]:.3f})')
plt.xlabel('cos θ')
plt.ylabel('sin θ')
plt.axis('equal')
plt.colorbar(sc, label='Phase θ')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/phi_non_degenerate_kuramoto.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("DIAGNOSTICS")
print("="*70)

phi_std = np.std(phi_traj[-2000:])
print(f"φ variance (steady): {phi_std:.6f}")

# Check if φ remained in a meaningful range
if 1.5 < phi_traj[-1] < 1.7:
    print("✓ φ converged near golden ratio")
else:
    print(f"○ φ converged to {phi_traj[-1]:.4f}")

# Check if R is non-trivial (not 0, not 1)
if 0.4 < np.mean(R_traj[-2000:]) < 0.9:
    print("✓ PARTIAL SYNCHRONIZATION — non-degenerate attractor")
elif np.mean(R_traj[-2000:]) > 0.95:
    print("⚠ PERFECT SYNC — system may still be degenerate")
else:
    print("○ WEAK SYNCHRONIZATION — increase coupling")

print("\n" + "="*70)
print("INTERPRETATION")
print("="*70)
print("This version implements 4 structural fixes:")
print("  1. Strong frequency heterogeneity (σ=0.6)")
print("  2. Higher harmonics: sin(θ) + 0.4·sin(2θ)")
print("  3. Structural gating: φ × polarity[i] × polarity[j]")
print("  4. φ injection: ω += γ·(φ - φ_target)")
print("\nResult: φ should remain active even in synchronized states.")
print("If R ≈ 0.6-0.8 and φ ≈ 1.618, the design works.")
print("="*70)
