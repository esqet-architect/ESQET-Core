#!/usr/bin/env python3
"""
ESQET v202 — Vacuum Partition Function
Calculating the Free Energy (F = -ln(lambda)) for different memory depths.
"""
import numpy as np

def calculate_free_energy(n):
    # Attractor (Dominant Eigenvalue)
    matrix = np.zeros((n, n))
    matrix[0, :] = 1
    if n > 1:
        matrix[1:, :-1] = np.eye(n-1)
    
    attractor = np.max(np.linalg.eigvals(matrix).real)
    
    # Statistical Mechanics: F = -k*T*ln(Z), here we analyze the 'Energy of Information'
    # F = -ln(attractor)
    return -np.log(attractor)

print("="*60)
print("ESQET v202: VACUUM FREE ENERGY ANALYSIS")
print("="*60)
for n in range(2, 6):
    f_energy = calculate_free_energy(n)
    print(f"Memory Depth {n}: Free Energy F = {f_energy:.8f}")
print("="*60)
print("PHYSICAL INSIGHT:")
print("Lower F (more negative) is more stable.")
print("The vacuum 'sinks' into higher memory depths unless resisted.")
print("="*60)
