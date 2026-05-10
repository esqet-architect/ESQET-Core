#!/usr/bin/env python3
"""
φ-Cantor Dust: Rigorous Derivation Visualization

D_f = ln(2)/ln(φ) = 1.440420090412556

This implements the IFS with contraction ratio r = φ⁻¹
and N = 2 copies per iteration.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math

# Constants
PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
D_F_EXACT = math.log(2) / math.log(PHI)


def generate_intervals(depth: int) -> list:
    """Generate φ-Cantor intervals recursively."""
    if depth == 0:
        return [(0.0, 1.0)]
    
    parent = generate_intervals(depth - 1)
    intervals = []
    for a, b in parent:
        length = b - a
        new_len = length * PHI_INV
        intervals.append((a, a + new_len))
        intervals.append((b - new_len, b))
    return intervals


def plot_cantor():
    """Plot φ-Cantor dust at multiple depths"""
    depths = [0, 1, 2, 3, 4, 5]
    fig, axes = plt.subplots(len(depths), 1, figsize=(12, 8))
    
    for idx, d in enumerate(depths):
        intervals = generate_intervals(d)
        ax = axes[idx]
        
        for a, b in intervals:
            rect = Rectangle((a, 0.2), b - a, 0.6, 
                           facecolor='darkblue', edgecolor='navy', alpha=0.8)
            ax.add_patch(rect)
        
        measure = sum(b - a for a, b in intervals)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_ylabel(f'n={d}\nμ={measure:.4f}', rotation=0, 
                     ha='right', va='center', fontsize=9)
        ax.axvline(x=PHI_INV, color='red', linestyle='--', alpha=0.3)
        ax.axvline(x=1 - PHI_INV, color='red', linestyle='--', alpha=0.3)
    
    axes[-1].set_xlabel('Unit interval [0, 1]')
    fig.suptitle(f'φ-Cantor Dust Construction\n'
                f'D_f = ln(2)/ln(φ) = {D_F_EXACT:.10f}\n'
                f'φ = {PHI:.8f}, φ⁻¹ = {PHI_INV:.8f}', 
                fontsize=12)
    plt.tight_layout()
    plt.savefig('phi_cantor_rigorous.png', dpi=150, bbox_inches='tight')
    plt.show()
    print(f"✅ Visualization saved to phi_cantor_rigorous.png")
    print(f"   D_f = {D_F_EXACT:.12f}")
    print(f"   φ = {PHI:.15f}")
    print(f"   φ⁻¹ = {PHI_INV:.15f}")


if __name__ == "__main__":
    print("="*60)
    print("φ-CANTOR DUST - RIGOROUS DERIVATION")
    print("="*60)
    print(f"D_f = ln(2)/ln(φ) = {D_F_EXACT:.12f}")
    print("="*60)
    plot_cantor()
