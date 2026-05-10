#!/usr/bin/env python3
"""
Fractal Cosmology Applications for ESQET
Connections between φ-Cantor spectral dimension and cosmology
"""

import numpy as np
import matplotlib.pyplot as plt
import math

PHI = (1 + math.sqrt(5)) / 2

class FractalCosmology:
    def __init__(self, d_s_uv=1.18, d_s_ir=4.0):
        self.d_s_uv = d_s_uv
        self.d_s_ir = d_s_ir
    
    def dimensional_flow(self, scale, crossover=0.5):
        return self.d_s_ir - (self.d_s_ir - self.d_s_uv) * np.exp(-scale / crossover)
    
    def primordial_power_spectrum(self, k, n_s=0.965):
        A_s = 2.1e-9
        k_0 = 0.05
        d_s_at_k = self.dimensional_flow(k)
        delta_n = (d_s_at_k - self.d_s_ir) / self.d_s_ir * 0.1
        n_s_eff = n_s - 1 + delta_n
        return A_s * (k / k_0) ** n_s_eff

def run_cosmology():
    print("="*70)
    print("FRACTAL COSMOLOGY APPLICATIONS")
    print("="*70)
    cosmo = FractalCosmology()
    
    # Dimensional flow
    print("\n[1] Dimensional Flow")
    for scale in [0.01, 0.1, 1.0, 10.0]:
        d_s = cosmo.dimensional_flow(scale)
        print(f"    scale={scale:.2f}: d_s = {d_s:.3f}")
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    scales = np.logspace(-2, 2, 100)
    axes[0].semilogx(scales, cosmo.dimensional_flow(scales), 'b-', linewidth=2)
    axes[0].axhline(y=1.18, color='r', linestyle='--', label='UV limit')
    axes[0].axhline(y=4.0, color='g', linestyle='--', label='IR limit')
    axes[0].set_xlabel('Scale')
    axes[0].set_ylabel('Spectral dimension d_s')
    axes[0].set_title('Dimensional Flow')
    axes[0].legend()
    
    k = np.logspace(-4, 0, 100)
    axes[1].loglog(k, cosmo.primordial_power_spectrum(k), 'b-', linewidth=2)
    axes[1].set_xlabel('k (Mpc⁻¹)')
    axes[1].set_ylabel('P(k)')
    axes[1].set_title('Primordial Power Spectrum')
    
    plt.tight_layout()
    plt.savefig('fractal_cosmology.png', dpi=150)
    plt.show()
    print("\n✅ Fractal cosmology plots saved to fractal_cosmology.png")

if __name__ == "__main__":
    run_cosmology()
