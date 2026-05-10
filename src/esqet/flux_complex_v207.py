#!/usr/bin/env python3
"""
ESQET v207 — Full Spectral Mapping: Real Attractors + Complex Voids
Correlating Stiffness to Flux Oscillations.
"""
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import polyroots

def analyze_memory_depth(n):
    # Coefficients for x^n - x^{n-1} - ... - 1 = 0
    coeffs = [-1] * n + [1]
    roots = polyroots(coeffs)
    
    # Stiffness of the dominant real root
    lambda_n = max([r.real for r in roots if abs(r.imag) < 1e-10 and r.real > 1])
    eps = 1e-8
    def beta(g): return 1.0 + sum(1.0/(g**m) for m in range(1, n)) - g
    stiffness = (beta(lambda_n + eps) - beta(lambda_n - eps)) / (2*eps)
    
    return roots, lambda_n, stiffness

print("="*70)
print("ESQET v207: COMPLEX SPECTRAL SIGNATURES")
print("="*70)

plt.figure(figsize=(10, 10))
colors = plt.cm.plasma(np.linspace(0, 1, 5))

for i, n in enumerate([2, 3, 4, 6]):
    roots, l_n, stiff = analyze_memory_depth(n)
    print(f"n={n} | Stiffness: {stiff:.4f} | Attractor: {l_n:.4f}")
    
    plt.scatter(roots.real, roots.imag, color=colors[i], label=f'n={n} (Stiff={stiff:.2f})', s=100)

# Unit circle for reference (Holographic Bound)
theta = np.linspace(0, 2*np.pi, 200)
plt.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.3, label='Unit Circle (Boundary)')

plt.axhline(0, color='k', alpha=0.5)
plt.axvline(0, color='k', alpha=0.5)
plt.title("ESQET v207: Complex Eigenvalue Map (Void Detection)")
plt.xlabel("Real (Fixed Point Attractor)")
plt.ylabel("Imaginary (Oscillatory Void Signature)")
plt.legend()
plt.grid(True, alpha=0.2)
plt.savefig('simulations/complex_spectral_map.png', dpi=300)

print("\n✓ Spectral map saved. Complex roots indicate oscillatory interference.")
print("If flux B oscillates, look for n=3 or n=4 complex modes.")
print("="*70)
