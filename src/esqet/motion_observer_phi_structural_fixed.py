#!/usr/bin/env python3
"""
ESQET Motion Observer v171.1 — Stabilized φ Adaptation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import hilbert

phi_true = (1 + np.sqrt(5)) / 2

def van_der_pol_recursive(state, t):
    """φ computed locally from state history (bounded)"""
    x, v, x_prev, x_pprev = state
    
    if abs(x_prev) > 1e-8:
        ratio = x / x_prev
        phi_local = 1.0 + 1.0 / abs(ratio)
        phi_emergent = np.clip(phi_local, 1.4, 1.85)   # Safe bracket around golden ratio
    else:
        phi_emergent = phi_true
    
    dxdt = v
    dvdt = phi_emergent * (1 - x**2) * v - x
    
    return [dxdt, dvdt, x, x_prev]


def van_der_pol_adaptive(state, t, adaptation_rate=0.012):
    """φ as a bounded reference attractor"""
    x, v, phi_eff = state
    
    # Stable adaptation law
    error = phi_true - phi_eff
    dphi = adaptation_rate * error * np.exp(-0.5 * x**2)   # damped by state magnitude
    
    dxdt = v
    dvdt = phi_eff * (1 - x**2) * v - x
    
    return [dxdt, dvdt, dphi]


# ========================== Run Simulations ==========================
print("="*70)
print("ESQET v171.1 — Stabilized φ Structural Coupling")
print("="*70)

t = np.linspace(0, 100, 6000)

# 1. Recursive φ from local state ratios
sol1 = odeint(van_der_pol_recursive, [0.5, 0.0, 0.2, 0.1], t)
x1 = sol1[:, 0]
phi_local = [1.0 + 1.0/abs(sol1[i,0]/sol1[i-1,0]) if abs(sol1[i-1,0])>1e-8 else phi_true 
             for i in range(1, len(t))]

# 2. Adaptive φ reference
sol2 = odeint(van_der_pol_adaptive, [0.5, 0.0, 1.4], t)
x2 = sol2[:, 0]
phi_evolution = sol2[:, 2]

# Amplitudes
amp1 = np.abs(hilbert(x1))
amp2 = np.abs(hilbert(x2))

print(f"Recursive φ  → Final amplitude: {np.mean(amp1[-1500:]):.4f}")
print(f"Adaptive φ   → Final amplitude: {np.mean(amp2[-1500:]):.4f}")
print(f"Final adapted φ_eff : {phi_evolution[-1]:.6f} (target = {phi_true:.6f})")

# ========================== Plotting ==========================
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(sol1[:,0], sol1[:,1], 'gold', lw=2)
plt.title('Recursive φ: Local State-Derived')
plt.xlabel('x'); plt.ylabel('v')
plt.grid(True, alpha=0.3); plt.axis('equal')

plt.subplot(2, 2, 2)
plt.plot(sol2[:,0], sol2[:,1], 'cyan', lw=2)
plt.title('Adaptive φ: Reference Attractor')
plt.xlabel('x'); plt.ylabel('v')
plt.grid(True, alpha=0.3); plt.axis('equal')

plt.subplot(2, 2, 3)
plt.plot(t[1:], phi_local[:len(t)-1], 'purple', lw=1.8, alpha=0.8, label='Local recursive φ')
plt.plot(t, phi_evolution, 'blue', lw=2, label='Adaptive φ_eff')
plt.axhline(phi_true, color='red', linestyle='--', label=f'Target φ = {phi_true:.5f}')
plt.title('φ Evolution')
plt.xlabel('Time')
plt.ylabel('φ')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 4)
plt.plot(t, amp1, 'brown', lw=1.8, alpha=0.8, label='Recursive')
plt.plot(t, amp2, 'green', lw=1.8, alpha=0.8, label='Adaptive')
plt.title('Amplitude Convergence')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/phi_structural_stable.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nStabilized version complete.")
print("φ is now bounded and numerically stable.")
