#!/usr/bin/env python3
"""
ESQET v198 — Variational Stability Analysis
Calculates the Action Density and Potential Curvature of the Vacuum.
"""
import numpy as np

phi = (1 + np.sqrt(5)) / 2

def lagrangian_density(g, g_dot=0):
    # Potential: V(g) = 0.5*g^2 - g - ln(g)
    potential = 0.5 * g**2 - g - np.log(g)
    kinetic = 0.5 * g_dot**2
    return kinetic - potential

def vacuum_stiffness(g):
    # V''(g) = 1 + 1/g^2
    return 1 + (1 / g**2)

# Test at the Fixed Point
L_phi = lagrangian_density(phi)
stiffness = vacuum_stiffness(phi)

print("="*70)
print("ESQET v198: VARIATIONAL FIELD RECONSTRUCTION")
print("="*70)
print(f"Saddle Point (phi):    {phi:.6f}")
print(f"Lagrangian Density L:  {L_phi:.6f}")
print(f"Vacuum Stiffness V'':  {stiffness:.6f}")
print("-" * 70)
print("FIELD OBSERVATION:")
print(f"The vacuum at 81212 is trapped in a well with stiffness {stiffness:.4f}.")
print("Any observed 'magnetic drift' is a displacement from this minimum.")
print("="*70)
