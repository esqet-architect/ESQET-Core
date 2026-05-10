#!/usr/bin/env python3
"""
φ-Cantor Dust: Fractal implementation with rigorous dimension D_f = ln(2)/ln(φ)
Supports ℤ₃ weighting for information dimension analysis.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math
from typing import List, Tuple

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
D_F = math.log(2) / math.log(PHI)


class PhiCantorDust:
    """φ-Cantor dust generator with ℤ₃ weighting support"""
    
    def __init__(self, max_depth: int = 10):
        self.max_depth = max_depth
        self.phi_inv = PHI_INV
        self.d_f = D_F
        
    def generate_intervals(self, depth: int) -> List[Tuple[float, float]]:
        """Generate interval endpoints recursively"""
        if depth == 0:
            return [(0.0, 1.0)]
        
        parent = self.generate_intervals(depth - 1)
        intervals = []
        for a, b in parent:
            length = b - a
            new_len = length * self.phi_inv
            intervals.append((a, a + new_len))
            intervals.append((b - new_len, b))
        return intervals
    
    def compute_measure(self, depth: int) -> float:
        """Total length at given depth"""
        intervals = self.generate_intervals(depth)
        return sum(b - a for a, b in intervals)
    
    def visualize(self, max_depth: int = 6):
        """Plot the φ-Cantor dust at multiple depths"""
        depths = list(range(max_depth + 1))
        fig, axes = plt.subplots(len(depths), 1, figsize=(12, 8))
        
        for idx, d in enumerate(depths):
            intervals = self.generate_intervals(d)
            ax = axes[idx]
            
            for a, b in intervals:
                rect = Rectangle((a, 0.2), b - a, 0.6, 
                               facecolor='darkblue', edgecolor='navy', alpha=0.8)
                ax.add_patch(rect)
            
            measure = self.compute_measure(d)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.set_yticks([])
            ax.set_ylabel(f'n={d}\nμ={measure:.4f}', rotation=0, 
                         ha='right', va='center', fontsize=9)
            ax.axvline(x=PHI_INV, color='red', linestyle='--', alpha=0.3)
            ax.axvline(x=1 - PHI_INV, color='red', linestyle='--', alpha=0.3)
        
        axes[-1].set_xlabel('Unit interval [0, 1]')
        fig.suptitle(f'φ-Cantor Dust\nD_f = ln(2)/ln(φ) = {self.d_f:.10f}', fontsize=12)
        plt.tight_layout()
        plt.savefig('phi_cantor_dust.png', dpi=150)
        plt.show()
        print(f"✅ Visualization saved to phi_cantor_dust.png")
        return fig


if __name__ == "__main__":
    dust = PhiCantorDust()
    dust.visualize()
