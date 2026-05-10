#!/usr/bin/env python3
"""
ESQET v201 — Spectral Signature Analysis
Computing the dominant eigenvalues (Attractors) for n-step memory vacua.
"""
import numpy as np

def get_dominant_eig(n):
    # Construct the companion matrix for n-step recursion
    # Top row is all 1s, sub-diagonal is 1s, rest 0s.
    matrix = np.zeros((n, n))
    matrix[0, :] = 1
    if n > 1:
        matrix[1:, :-1] = np.eye(n-1)
    
    eigenvalues = np.linalg.eigvals(matrix)
    # The attractor is the largest real eigenvalue
    return np.max(eigenvalues.real)

print("="*60)
print("ESQET v201: VACUUM SPECTRAL SIGNATURES")
print("="*60)
for i in range(2, 6):
    attractor = get_dominant_eig(i)
    name = {2: "Fibonacci (φ)", 3: "Tribonacci (τ)", 4: "Tetranacci", 5: "Pentanacci"}[i]
    print(f"{name} Memory Depth {i}: Attractor = {attractor:.8f}")
print("="*60)
print("PHYSICAL HYPOTHESIS:")
print("Magnetic flux stabilization at these values indicates")
print("the 'depth' of local quantum entanglement memory.")
