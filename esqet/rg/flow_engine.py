#!/usr/bin/env python3
"""
φ-RG Flow Engine with Topological Drag Term

The drag term represents the slowing of RG flow near φ-fixed points,
modeling the "symmetry saturation" phase of the vacuum manifold.
"""

import numpy as np
import matplotlib.pyplot as plt
import math
from typing import Dict, List

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
L = math.log(PHI)
D_F = math.log(2) / math.log(PHI)


class PhiRGFlowWithDrag:
    """
    RG flow with topological drag near φ-fixed points.
    Drag coefficient κ controls the slowing of flow.
    """
    
    def __init__(self, alpha=1.2, gamma=PHI_INV, drag_coeff=1.0):
        self.alpha = alpha
        self.gamma = gamma
        self.drag_coeff = drag_coeff
        self.L = L
        
    def beta_function(self, O):
        """
        β(O) = α · (O - O²) · (1 - γ/O) · (O - 0.3) · drag_factor
        """
        if O <= 0:
            return 0.0
        term1 = O - O**2
        term2 = 1 - self.gamma / O
        term3 = O - 0.3
        
        # Drag term: slows flow near O = γ (φ-fixed point)
        drag = 1 / (1 + self.drag_coeff * abs(O - self.gamma))
        
        return self.alpha * term1 * term2 * term3 * drag
    
    def rg_map(self, O):
        return O - self.beta_function(O) * self.L
    
    def flow_trajectory(self, O0, n_steps=50):
        traj = [O0]
        O = O0
        for _ in range(n_steps):
            O = self.rg_map(O)
            traj.append(O)
            if O <= 0 or O > 2:
                break
        return np.array(traj)
    
    def plot_flow_comparison(self, O0=0.8, drag_values=[0, 0.5, 1.0, 2.0]):
        """Compare flows with different drag coefficients"""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        for drag in drag_values:
            self.drag_coeff = drag
            traj = self.flow_trajectory(O0, n_steps=40)
            ax.plot(range(len(traj)), traj, 'o-', label=f'κ={drag}', markersize=4)
        
        ax.axhline(y=1, color='r', linestyle='--', alpha=0.5, label='IR fixed point O=1')
        ax.axhline(y=PHI_INV, color='g', linestyle='--', alpha=0.5, label=f'φ-fixed point γ={PHI_INV:.4f}')
        ax.set_xlabel('RG step')
        ax.set_ylabel('Operator O')
        ax.set_title('RG Flow with Topological Drag\nEffect of drag coefficient κ')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('rg_flow_with_drag.png', dpi=150)
        plt.show()
        print("✅ RG flow with drag saved to rg_flow_with_drag.png")
        return fig


if __name__ == "__main__":
    rg = PhiRGFlowWithDrag(alpha=1.2, drag_coeff=1.0)
    rg.plot_flow_comparison()
