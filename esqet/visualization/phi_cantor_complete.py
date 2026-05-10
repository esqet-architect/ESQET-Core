#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
D_F_EXACT = math.log(2) / math.log(PHI)

class PhiCantorDust:
    def __init__(self):
        self.intervals_by_depth = {}

    def generate_intervals(self, depth):
        if depth == 0: return [(0.0, 1.0)]
        if depth in self.intervals_by_depth: return self.intervals_by_depth[depth]
        
        parent_intervals = self.generate_intervals(depth - 1)
        intervals = []
        for a, b in parent_intervals:
            length = b - a
            new_length = length * PHI_INV
            intervals.append((a, a + new_length))
            intervals.append((b - new_length, b))
        self.intervals_by_depth[depth] = intervals
        return intervals

def run_viz():
    dust = PhiCantorDust()
    depths = [0, 1, 2, 3, 4, 5]
    fig, axes = plt.subplots(len(depths), 1, figsize=(10, 8))
    
    for idx, d in enumerate(depths):
        intervals = dust.generate_intervals(d)
        for a, b in intervals:
            axes[idx].add_patch(Rectangle((a, 0.2), b - a, 0.6, color='navy', alpha=0.8))
        axes[idx].set_xlim(0, 1)
        axes[idx].set_ylim(0, 1)
        axes[idx].set_yticks([])
        axes[idx].set_ylabel(f'n={d}', rotation=0, labelpad=20)

    plt.suptitle(f'phi-Cantor Dust (Df ≈ {D_F_EXACT:.4f})')
    plt.tight_layout()
    plt.savefig('phi_cantor_dust_fixed.png')
    print("✅ Visualization saved to phi_cantor_dust_fixed.png")

if __name__ == "__main__":
    run_viz()
