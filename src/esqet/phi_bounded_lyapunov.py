#!/usr/bin/env python3
"""
ESQET Network v174 — Provably Bounded φ Dynamics
Fixes:
1. φ only perturbs baseline dynamics, doesn't scale them
2. φ update uses only bounded functions (tanh)
3. Explicit Lyapunov descent: dp = -η * (p - φ_target)
4. No chaotic energy injection into φ
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

phi_target = (1 + np.sqrt(5)) / 2
N = 8
K = 2.5
alpha = 0.3  # Coupling modulation strength
eta = 0.05   # φ adaptation rate

def network_bounded(state, t):
    """
    State: [x1, v1, x2, v2, ..., φ]
    φ is now provably bounded via gradient descent on (φ - φ_target)²
    """
    n_osc = N
    x = np.zeros(n_osc)
    v = np.zeros(n_osc)
    for i in range(n_osc):
        x[i] = state[2*i]
        v[i] = state[2*i + 1]
    phi_eff = state[-1]
    
    # Mean field
    mean_x = np.mean(x)
    
    # FIX 1: φ only perturbs coupling, doesn't scale entire dynamics
    # Baseline Van der Pol (φ=1 gives standard VdP)
    baseline_nl = 1.0
    phi_modulation = 1.0 + alpha * np.tanh(phi_eff - phi_target)  # Bounded between 0.7 and 1.3
    
    dxdt = np.zeros(n_osc)
    dvdt = np.zeros(n_osc)
    for i in range(n_osc):
        dxdt[i] = v[i]
        # FIX: φ modulates nonlinearity, doesn't multiply it directly
        dvdt[i] = baseline_nl * (1 - x[i]**2) * v[i] - x[i] + K * phi_modulation * (mean_x - x[i])
    
    # FIX 2 & 3: φ update uses pure gradient descent on quadratic penalty
    # No x*v cross-terms — they cause unbounded energy injection
    dphi_dt = -eta * (phi_eff - phi_target)  # Pure Lyapunov: V = 0.5*(φ - φ_target)²
    dphi_dt = np.clip(dphi_dt, -0.1, 0.1)   # Safety bound
    
    dstate = np.zeros(2*n_osc + 1)
    dstate[0:2*n_osc:2] = dxdt
    dstate[1:2*n_osc:2] = dvdt
    dstate[-1] = dphi_dt
    
    return dstate


def compute_order_parameter(x):
    """Kuramoto order parameter via Hilbert phase"""
    from scipy.signal import hilbert
    analytic = hilbert(x)
    phase = np.angle(analytic)
    return np.abs(np.mean(np.exp(1j * phase)))


def lyapunov_function(state):
    """Candidate Lyapunov function: V = oscillator energy + φ penalty"""
    n_osc = N
    x = state[0:2*n_osc:2]
    v = state[1:2*n_osc:2]
    phi_eff = state[-1]
    
    V_osc = 0.5 * np.mean(x**2 + v**2)
    V_phi = 0.5 * (phi_eff - phi_target)**2
    return V_osc + V_phi


# Simulation
print("="*70)
print("ESQET v174 — Provably Bounded φ Dynamics")
print("="*70)
print(f"N = {N} oscillators, K = {K}, α = {alpha}, η = {eta}")
print(f"φ_target = {phi_target:.6f}")
print("Fixes: φ only perturbs coupling, pure gradient descent, no x·v injection")
print("="*70)

# Initial conditions
np.random.seed(42)
initial = np.zeros(2*N + 1)
for i in range(N):
    initial[2*i] = np.random.uniform(-0.8, 0.8)
    initial[2*i + 1] = np.random.uniform(-0.8, 0.8)
initial[-1] = 0.8  # Start away from target

t = np.linspace(0, 400, 10000)
print("Integrating bounded dynamics...")
sol = odeint(network_bounded, initial, t, rtol=1e-8, atol=1e-10)

x_traj = sol[:, 0:2*N:2]
phi_traj = sol[:, -1]

# Order parameter
R_traj = np.zeros(len(t))
for i in range(len(t)):
    R_traj[i] = compute_order_parameter(x_traj[i])

# Lyapunov function
V_traj = np.zeros(len(t))
for i in range(0, len(t), 500):
    V_traj[i] = lyapunov_function(sol[i])
V_traj = np.interp(t, t[::500], V_traj[::500])

print(f"\nFinal φ_eff     : {phi_traj[-1]:.6f} (target = {phi_target:.6f})")
print(f"Δ from target  : {phi_target - phi_traj[-1]:.6f}")
print(f"Final sync R    : {R_traj[-1]:.4f}")
print(f"Mean sync R     : {np.mean(R_traj[-2000:]):.4f} ± {np.std(R_traj[-2000:]):.4f}")

# Estimate Lyapunov-like stability from φ variance
phi_std = np.std(phi_traj[-2000:])
print(f"φ variance (steady): {phi_std:.6f}")

# Plotting
plt.figure(figsize=(15, 12))

# φ evolution
plt.subplot(2, 2, 1)
plt.plot(t, phi_traj, 'gold', lw=2)
plt.axhline(phi_target, color='red', linestyle='--', label=f'φ_target = {phi_target:.5f}')
plt.ylim(phi_target - 0.5, phi_target + 0.5)
plt.xlabel('Time')
plt.ylabel('φ_eff')
plt.title('φ Evolution — Pure Lyapunov Descent (No x·v Injection)')
plt.legend()
plt.grid(True, alpha=0.3)

# Synchronization
plt.subplot(2, 2, 2)
plt.plot(t, R_traj, 'purple', lw=2)
plt.axhline(np.mean(R_traj[-2000:]), color='orange', linestyle='--',
            label=f'Steady R = {np.mean(R_traj[-2000:]):.4f}')
plt.xlabel('Time')
plt.ylabel('Order Parameter R')
plt.title('Network Synchronization')
plt.legend()
plt.grid(True, alpha=0.3)

# Lyapunov function
plt.subplot(2, 2, 3)
plt.plot(t, V_traj, 'teal', lw=2)
plt.xlabel('Time')
plt.ylabel('V(t)')
plt.title('Lyapunov Function — Should Decrease or Remain Bounded')
plt.grid(True, alpha=0.3)

# Phase portrait
plt.subplot(2, 2, 4)
plt.plot(x_traj[-2000:, -1], sol[-2000:, -3], 'brown', lw=1.5, alpha=0.7)
plt.xlabel('x_N')
plt.ylabel('v_N')
plt.title('Phase Portrait (Last Oscillator)')
plt.grid(True, alpha=0.3)
plt.axis('equal')

plt.tight_layout()
plt.savefig('simulations/phi_bounded_lyapunov.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("DIAGNOSTICS")
print("="*70)
print(f"Lyapunov function change: ΔV = {V_traj[-1] - V_traj[0]:.2e}")
if V_traj[-1] < V_traj[0]:
    print("✓ V(t) decreased — Lyapunov function is working")
else:
    print("⚠ V(t) increased — check for energy injection")

if phi_std < 0.05:
    print("✓ φ converged to narrow distribution")
else:
    print(f"○ φ variance = {phi_std:.4f} — some drift remains")

if np.mean(R_traj[-2000:]) > 0.5:
    print("✓ STRONG SYNCHRONIZATION")
elif np.mean(R_traj[-2000:]) > 0.2:
    print("○ MODERATE SYNCHRONIZATION")
else:
    print("✗ WEAK SYNCHRONIZATION")

print("\n" + "="*70)
print("INTERPRETATION")
print("="*70)
print("This version uses:")
print("  1. φ only perturbs coupling (not scaled dynamics)")
print("  2. Pure gradient descent: dφ/dt = -η(φ - φ_target)")
print("  3. No x·v energy injection into φ")
print("  4. Bounded modulation via tanh")
print("\nResult: φ should remain near target, not blow up to 61.")
print("If φ still drifts, the issue is in coupling structure.")
print("="*70)
