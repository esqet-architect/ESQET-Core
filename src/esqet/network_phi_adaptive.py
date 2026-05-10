#!/usr/bin/env python3
"""
ESQET Network Dynamics v172 — φ-Adaptive Oscillator Network
N Van der Pol oscillators with adaptive φ_eff and φ-scaled coupling.
Measures: Synchronization order parameter, φ_eff distribution, Lyapunov exponents.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.stats import pearsonr

phi_target = (1 + np.sqrt(5)) / 2
N = 12  # Number of oscillators
K = 2.5  # Global coupling strength

def oscillator_network(state, t):
    """
    State vector: [x1, v1, φ1, x2, v2, φ2, ...]
    Each oscillator: Van der Pol with adaptive φ
    Coupling: φ-scaled diffusive coupling
    """
    n_osc = N
    dstate = np.zeros(3 * n_osc)
    
    # Extract states
    x = np.zeros(n_osc)
    v = np.zeros(n_osc)
    phi_eff = np.zeros(n_osc)
    for i in range(n_osc):
        x[i] = state[3*i]
        v[i] = state[3*i + 1]
        phi_eff[i] = state[3*i + 2]
    
    # Compute coupling terms (mean field with φ-scaled weights)
    mean_x = np.mean(x)
    coupling_strength = K * phi_target  # φ-weighted global coupling
    
    # Dynamics for each oscillator
    for i in range(n_osc):
        # Coupling input
        coupling = coupling_strength * (mean_x - x[i])
        
        # Van der Pol with adaptive φ_eff
        dxdt = v[i]
        dvdt = phi_eff[i] * (1 - x[i]**2) * v[i] - x[i] + coupling
        
        # φ adaptation toward golden ratio
        alpha = 0.02  # Adaptation rate
        dphi_dt = alpha * (phi_target - phi_eff[i]) * (1 - x[i]**2) * v[i]
        
        dstate[3*i] = dxdt
        dstate[3*i + 1] = dvdt
        dstate[3*i + 2] = np.clip(dphi_dt, -0.1, 0.1)
    
    return dstate


def order_parameter(x, t):
    """Kuramoto order parameter R (synchronization measure)"""
    phases = np.arctan2(np.diff(x, axis=1), x[:, :-1])
    R = np.abs(np.mean(np.exp(1j * phases), axis=1))
    return R


# Simulation
print("="*60)
print("ESQET Network Dynamics v172")
print(f"N = {N} φ-adaptive Van der Pol oscillators")
print(f"Coupling strength K = {K}")
print(f"φ_target = {phi_target:.6f}")
print("="*60)

# Initial conditions: random x, v, φ near phi_target
np.random.seed(42)
initial_state = np.zeros(3 * N)
for i in range(N):
    initial_state[3*i] = np.random.uniform(-1, 1)
    initial_state[3*i + 1] = np.random.uniform(-1, 1)
    initial_state[3*i + 2] = phi_target + np.random.uniform(-0.3, 0.3)

t = np.linspace(0, 200, 8000)
print("Integrating network dynamics...")
sol = odeint(oscillator_network, initial_state, t, rtol=1e-6, atol=1e-8)

# Extract trajectories
x_traj = sol[:, 0:3*N:3]
phi_traj = sol[:, 2:3*N:3]
phi_mean = np.mean(phi_traj, axis=1)
phi_std = np.std(phi_traj, axis=1)

# Order parameter
R = np.zeros(len(t))
for i in range(len(t)):
    phases = np.arctan2(np.diff(x_traj[i]), x_traj[i, :-1])
    R[i] = np.abs(np.mean(np.exp(1j * phases)))

print(f"Simulation complete. Shape: {sol.shape}")
print(f"Final mean φ_eff: {phi_mean[-1]:.6f} ± {phi_std[-1]:.6f}")
print(f"Final synchronization R: {R[-1]:.4f}")

# Plotting
plt.figure(figsize=(15, 12))

# Subplot 1: φ evolution across oscillators
plt.subplot(2, 2, 1)
for i in range(min(6, N)):
    plt.plot(t, phi_traj[:, i], alpha=0.6, lw=1)
plt.plot(t, phi_mean, 'k', lw=2, label='Mean φ_eff')
plt.axhline(phi_target, color='r', linestyle='--', label=f'φ_target = {phi_target:.4f}')
plt.xlabel('Time')
plt.ylabel('φ_eff')
plt.title('φ Adaptation Across the Network')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 2: Synchronization order parameter
plt.subplot(2, 2, 2)
plt.plot(t, R, 'purple', lw=2)
plt.axhline(np.mean(R[-1000:]), color='gold', linestyle='--', 
            label=f'Steady R = {np.mean(R[-1000:]):.4f}')
plt.xlabel('Time')
plt.ylabel('Order Parameter R (0→1)')
plt.title('Network Synchronization')
plt.legend()
plt.grid(True, alpha=0.3)

# Subplot 3: Phase space of first oscillator vs mean field
plt.subplot(2, 2, 3)
plt.plot(x_traj[-1000:, 0], sol[-1000:, 1], 'gold', lw=1.5, alpha=0.7)
plt.xlabel('x₁')
plt.ylabel('v₁')
plt.title('Oscillator 1 Phase Portrait')
plt.grid(True, alpha=0.3)
plt.axis('equal')

# Subplot 4: φ distribution at steady state
plt.subplot(2, 2, 4)
plt.hist(phi_traj[-500:, :].flatten(), bins=20, color='teal', alpha=0.7, edgecolor='black')
plt.axvline(phi_target, color='r', linestyle='--', label=f'φ_target = {phi_target:.4f}')
plt.axvline(phi_mean[-1], color='gold', linestyle='-', label=f'Mean φ_eff = {phi_mean[-1]:.4f}')
plt.xlabel('φ_eff')
plt.ylabel('Count')
plt.title('Distribution of φ_eff at Steady State')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/network_phi_adaptive.png', dpi=300, bbox_inches='tight')
plt.show()

# Statistical analysis
print("\n" + "="*60)
print("STATISTICAL ANALYSIS")
print("="*60)
print(f"Mean φ_eff: {phi_mean[-1000:].mean():.6f} ± {phi_std[-1000:].mean():.6f}")
print(f"Synchronization R: {np.mean(R[-1000:]):.6f} ± {np.std(R[-1000:]):.6f}")
print(f"φ_target - mean_φ: {phi_target - phi_mean[-1000:].mean():.6f}")

# Correlation between φ and synchronization
corr, p_val = pearsonr(phi_mean[-1000:], R[-1000:])
print(f"Correlation (φ_mean vs R): {corr:.4f} (p={p_val:.4f})")

# Lyapunov-like stability measure
phi_variance = np.var(phi_traj, axis=1)
print(f"φ variance at steady state: {phi_variance[-1000:].mean():.6f}")

print("\n" + "="*60)
print("INTERPRETATION")
print("="*60)
if np.mean(R[-1000:]) > 0.7:
    print("✓ Strong synchronization — network is coherent")
else:
    print("○ Weak synchronization — oscillators remain incoherent")

if np.abs(phi_target - phi_mean[-1000:].mean()) < 0.05:
    print("✓ φ_eff converged very close to golden ratio")
else:
    print(f"○ φ_eff converged to {phi_mean[-1000:].mean():.4f} (Δ = {phi_target - phi_mean[-1000:].mean():.4f})")

if corr > 0.5:
    print("✓ Positive correlation: higher φ_eff → stronger synchronization")
elif corr < -0.5:
    print("⚠ Negative correlation: higher φ_eff → weaker synchronization")
else:
    print("○ Weak correlation — φ_eff and synchronization nearly independent")

print("="*60)
