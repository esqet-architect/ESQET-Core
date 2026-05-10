#!/usr/bin/env python3
"""
ESQET Motion Observer v171 — φ as Emergent / Adaptive Property
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.signal import hilbert

phi_true = (1 + np.sqrt(5)) / 2

def van_der_pol_phi_structural(state, t):
    """φ computed recursively from local state history"""
    x, v, x_prev, x_pprev = state
    
    # Local φ approximation from consecutive states
    if abs(x_prev) > 1e-8:
        ratio = x / x_prev
        phi_local = 1.0 + 1.0 / abs(ratio)
        phi_emergent = np.clip(phi_local, 1.4, 1.8)
    else:
        phi_emergent = phi_true
    
    dxdt = v
    dvdt = phi_emergent * (1 - x**2) * v - x
    
    return [dxdt, dvdt, x, x_prev]


def phi_adaptive_reference(state, t):
    """φ as a slowly adapting reference attractor"""
    x, v, phi_eff = state
    
    # Slow adaptation toward true golden ratio
    dphi = 0.008 * (phi_true - phi_eff) * (1 - x**2)
    
    dxdt = v
    dvdt = phi_eff * (1 - x**2) * v - x
    
    return [dxdt, dvdt, dphi + phi_eff]


# ========================== Simulations ==========================
print("="*70)
print("ESQET v171 — φ as Structural / Emergent Property")
print("="*70)

t = np.linspace(0, 120, 8000)

# Simulation 1: Recursive φ from state history
initial1 = [0.6, 0.0, 0.3, 0.1]
sol1 = odeint(van_der_pol_phi_structural, initial1, t)
x1 = sol1[:, 0]

# Simulation 2: Adaptive φ reference
initial2 = [0.6, 0.0, 1.5]
sol2 = odeint(phi_adaptive_reference, initial2, t)
x2 = sol2[:, 0]
phi_evolution = sol2[:, 2]

# Amplitude envelopes
amp1 = np.abs(hilbert(x1))
amp2 = np.abs(hilbert(x2))

print(f"Recursive φ final amplitude : {np.mean(amp1[-2000:]):.4f}")
print(f"Adaptive φ final amplitude  : {np.mean(amp2[-2000:]):.4f}")
print(f"Final adapted φ_eff         : {phi_evolution[-1]:.6f} (target = {phi_true:.6f})")

# ========================== Plotting ==========================
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(sol1[:,0], sol1[:,1], 'gold', lw=2.2, label='Recursive φ')
plt.title('Phase Space — Recursive φ Emergence')
plt.xlabel('x')
plt.ylabel('v')
plt.legend()
plt.grid(True, alpha=0.3)
plt.axis('equal')

plt.subplot(2, 2, 2)
plt.plot(sol2[:,0], sol2[:,1], 'cyan', lw=2.2, label='Adaptive φ')
plt.title('Phase Space — φ as Adaptive Reference')
plt.xlabel('x')
plt.ylabel('v')
plt.legend()
plt.grid(True, alpha=0.3)
plt.axis('equal')

plt.subplot(2, 2, 3)
plt.plot(t, phi_evolution, 'purple', lw=2)
plt.axhline(phi_true, color='red', linestyle='--', label=f'Target φ = {phi_true:.6f}')
plt.title('φ Adaptation Over Time')
plt.xlabel('Time')
plt.ylabel('Effective φ')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 4)
plt.plot(t, amp1, 'brown', lw=1.8, alpha=0.8, label='Recursive')
plt.plot(t, amp2, 'green', lw=1.8, alpha=0.8, label='Adaptive')
plt.title('Limit Cycle Amplitude Convergence')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/phi_structural_emergence.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("φ is now structurally meaningful:")
print("• Recursive version: computed from local state ratios")
print("• Adaptive version: slowly converges toward golden ratio")
print("="*70)
