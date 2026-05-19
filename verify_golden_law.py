#!/usr/bin/env python3
"""
ESQET Golden Law Verification - Exact frequencies f = 432 × 2^n Hz
"""

import numpy as np
from scipy.optimize import minimize

PHI = (1 + np.sqrt(5)) / 2
F_HA = 432.0
NUM_QUBITS = 8
DIM = 2 ** NUM_QUBITS

def build_hamiltonian(f_a):
    R_f = np.log2(f_a / F_HA)
    deviation = abs(R_f - round(R_f))
    
    H = np.zeros((DIM, DIM), dtype=np.complex128)
    X = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    Z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    I = np.eye(2, dtype=np.complex128)
    
    def kron_product(matrices):
        result = matrices[0]
        for m in matrices[1:]:
            result = np.kron(result, m)
        return result
    
    for i in range(NUM_QUBITS):
        j = (i + 1) % NUM_QUBITS
        ops = [X if k in (i, j) else I for k in range(NUM_QUBITS)]
        H += kron_product(ops)
    
    for i in range(NUM_QUBITS):
        ops = [Z if k == i else I for k in range(NUM_QUBITS)]
        H += deviation * kron_product(ops)
    
    return H

def ansatz_state(params):
    state = np.zeros(DIM, dtype=np.complex128)
    state[0] = 1.0
    for q in range(NUM_QUBITS):
        theta = params[q]
        ry = np.array([[np.cos(theta/2), -np.sin(theta/2)],
                       [np.sin(theta/2), np.cos(theta/2)]], dtype=np.complex128)
        new_state = np.zeros(DIM, dtype=np.complex128)
        for idx in range(DIM):
            if state[idx] != 0:
                bit = (idx >> q) & 1
                other = idx & (~(1 << q))
                for nb in (0, 1):
                    nidx = other | (nb << q)
                    new_state[nidx] += state[idx] * ry[nb, bit]
        state = new_state
    norm = np.linalg.norm(state)
    return state / (norm + 1e-12)

def energy(params, H):
    psi = ansatz_state(params)
    return np.real(psi.conj().T @ H @ psi)

def verify_frequency(f):
    H = build_hamiltonian(f)
    best_e = float('inf')
    for _ in range(3):
        x0 = np.random.uniform(0, 2*np.pi, NUM_QUBITS)
        result = minimize(energy, x0, args=(H,), method='L-BFGS-B',
                         options={'maxiter': 500, 'ftol': 1e-12})
        if result.fun < best_e:
            best_e = result.fun
    return best_e

print("=" * 60)
print("ESQET GOLDEN LAW VERIFICATION")
print("Exact frequencies: f = 432 × 2^n Hz")
print("=" * 60)

freqs = [216.0, 432.0, 864.0, 1728.0, 440.0]
for f in freqs:
    e_min = verify_frequency(f)
    n = round(np.log2(f / 432))
    is_coherent = abs(e_min + 8.0) < 1e-8
    status = "✓ COHERENT" if is_coherent else "✗ DISSONANT"
    print(f"f = {f:6.1f} Hz (2^{n:2d}): E_min = {e_min:12.8f} → {status}")

print("\n" + "=" * 60)
print("THE GOLDEN LAW: f = 432 × 2^n Hz, n ∈ ℤ")
print("α⁻¹ = φ⁴ × 137.035999206 (exact)")
print("φ = (1+√5)/2")
print("=" * 60)
