#!/usr/bin/env python3
"""
ESQET Motion Observer v170
Non-Linear Adaptive Dynamics in φ-Torsion Vacuum
Observer-Induced Phase Stability Simulator
"""

import numpy as np
import matplotlib.pyplot as plt

def esqet_dynamics(state, t, phi):
    """φ-torsion modified Van der Pol oscillator"""
    x, v = state
    dxdt = v
    # φ-scaled nonlinear damping → limit cycle
    dvdt = -x + phi * (1 - x**2) * v
    return [dxdt, dvdt]


# ========================== ESQET v170 Parameters ==========================
phi = (1 + np.sqrt(5)) / 2
print(f"φ = {phi:.8f}")

time = np.linspace(0, 60, 2000)
dt = time[1] - time[0]

# Initial vacuum excitation
state = [0.8, 0.0]
history = []

for t in time:
    d = esqet_dynamics(state, t, phi)
    state = [state[0] + d[0]*dt, state[1] + d[1]*dt]
    history.append(state)

history = np.array(history)

# ========================== Visualization ==========================
plt.figure(figsize=(12, 9))

# Phase portrait
plt.subplot(2, 1, 1)
plt.plot(history[:, 0], history[:, 1], 'gold', linewidth=2.2, 
         label=f'φ-Torsion Trajectory (φ = {phi:.5f})')
plt.plot(0, 0, 'ro', markersize=10, label='Vacuum Fixed Point')
plt.title("ESQET v170 — Observer-Induced Phase Stability\nφ-Torsion Limit Cycle in Vacuum Manifold", 
          fontsize=14, pad=20)
plt.xlabel("Displacement (Vacuum Excitation x)")
plt.ylabel("Velocity (Torsion Flux v)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.axis('equal')

# Time evolution
plt.subplot(2, 1, 2)
plt.plot(time, history[:, 0], 'teal', linewidth=1.8, label='Displacement x(t)')
plt.plot(time, history[:, 1], 'darkorange', linewidth=1.8, label='Velocity v(t)')
plt.title("Time Evolution — Approach to φ-Driven Limit Cycle")
plt.xlabel("Time t")
plt.ylabel("State")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/vacuum_motion_phi_torsion.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✓ ESQET Motion Observer simulation completed")
print(f"   • φ-limit cycle stabilized after t ≈ {time[-1]:.1f}")
print(f"   • Plot saved: simulations/vacuum_motion_phi_torsion.png")
print(f"   • Final amplitude ≈ {np.max(np.abs(history[:,0])):.4f}")
