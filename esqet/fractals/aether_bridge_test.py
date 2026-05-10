#!/usr/bin/env python3
"""
AETHER BRIDGE TEST - Hierarchical φ-Scaled Connections

The 1D chain approximation gave d_w ≈ 6.73 (walkers trapped).
Adding bridges at φ^n distances should collapse d_w toward 2.44.
If it works: The φ-Cantor universality class is numerically verified.
If it fails: The theory is mathematically self-consistent but nonphysical.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import random
from typing import List, Tuple, Dict

# Constants
PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
D_F_THEORY = math.log(2) / math.log(PHI)
D_W_THEORY = D_F_THEORY + 1  # = 2.440420090413
D_S_THEORY = 2 * D_F_THEORY / D_W_THEORY  # = 1.1804689660


class AetherBridgeGraph:
    """
    φ-Cantor graph with hierarchical Aether bridges.
    
    Bridges connect nodes at distances φ, φ², φ³, φ⁴, ...
    This represents:
    - Quantum tunneling across voids
    - Non-local coupling in the vacuum manifold
    - Small-world fractal network connectivity
    """
    
    def __init__(self, depth: int = 8, max_bridge_scale: int = 4):
        self.depth = depth
        self.max_bridge_scale = max_bridge_scale
        self.phi = PHI
        self.phi_inv = PHI_INV
        self._build_graph()
        
    def _generate_intervals(self) -> List[Tuple[float, float]]:
        """Generate φ-Cantor intervals"""
        intervals = [(0.0, 1.0)]
        for _ in range(self.depth):
            new_intervals = []
            for a, b in intervals:
                length = b - a
                new_len = length * self.phi_inv
                new_intervals.append((a, a + new_len))
                new_intervals.append((b - new_len, b))
            intervals = new_intervals
        return intervals
    
    def _build_graph(self):
        """Build graph with nearest neighbors + Aether bridges"""
        intervals = self._generate_intervals()
        self.n_nodes = len(intervals)
        self.centers = np.array([(a + b) / 2 for a, b in intervals])
        
        # Sort by position
        sorted_idx = np.argsort(self.centers)
        sorted_centers = self.centers[sorted_idx]
        
        # Initialize adjacency
        self.adj = {i: set() for i in range(self.n_nodes)}
        
        # 1. Nearest neighbor connections (local connectivity)
        for j in range(self.n_nodes - 1):
            i1 = sorted_idx[j]
            i2 = sorted_idx[j + 1]
            self.adj[i1].add(i2)
            self.adj[i2].add(i1)
        
        # 2. AETHER BRIDGES - Hierarchical φ-scaled jumps
        avg_spacing = (sorted_centers[-1] - sorted_centers[0]) / self.n_nodes
        
        for scale in range(1, self.max_bridge_scale + 1):
            bridge_distance = PHI ** scale * avg_spacing
            # Also try φ⁻¹ scale for completeness
            for sign in [1, -1]:
                dist = bridge_distance if sign == 1 else bridge_distance * PHI_INV
                
                for i in range(self.n_nodes):
                    pos_i = self.centers[sorted_idx[i]]
                    # Find nodes at approximate distance dist
                    for j in range(i + 1, min(i + 50, self.n_nodes)):
                        pos_j = self.centers[sorted_idx[j]]
                        actual_dist = abs(pos_j - pos_i)
                        if abs(actual_dist - dist) / max(dist, 1e-6) < 0.3:
                            i1 = sorted_idx[i]
                            i2 = sorted_idx[j]
                            self.adj[i1].add(i2)
                            self.adj[i2].add(i1)
        
        # Convert sets to lists for faster access
        self.adj_list = {k: list(v) for k, v in self.adj.items()}
        self.degrees = [len(self.adj_list[i]) for i in range(self.n_nodes)]
        
        print(f"Graph built: {self.n_nodes} nodes, avg degree = {np.mean(self.degrees):.2f}")
        print(f"Bridge scales: {[PHI**s for s in range(1, self.max_bridge_scale+1)]}")
        
    def random_walk(self, start: int, steps: int) -> List[int]:
        """Perform random walk on graph with Aether bridges"""
        path = [start]
        current = start
        for _ in range(steps):
            neighbors = self.adj_list[current]
            if neighbors:
                current = random.choice(neighbors)
            path.append(current)
        return path
    
    def compute_msd_and_return(self, n_walkers: int = 500, max_steps: int = 500):
        """Compute mean-square displacement and return probability"""
        msd = np.zeros(max_steps + 1)
        p_return = np.zeros(max_steps + 1)
        
        for _ in range(n_walkers):
            start = random.randint(0, self.n_nodes - 1)
            start_pos = self.centers[start]
            path = self.random_walk(start, max_steps)
            
            for t, node in enumerate(path):
                msd[t] += (self.centers[node] - start_pos) ** 2
                if node == start:
                    p_return[t] += 1
        
        msd /= n_walkers
        p_return /= n_walkers
        
        return msd, p_return


def fit_power_law(x, y, x_min=20, x_max=200):
    """Fit power law: y = A * x^exponent"""
    mask = (x >= x_min) & (x <= x_max) & (y > 0)
    x_fit = x[mask]
    y_fit = y[mask]
    
    if len(x_fit) < 5:
        return 0.0
    
    log_x = np.log(x_fit)
    log_y = np.log(y_fit)
    slope, _ = np.polyfit(log_x, log_y, 1)
    return slope


def run_bridge_test(max_bridge_scale=4):
    """Run the Aether Bridge test"""
    print("="*70)
    print("AETHER BRIDGE TEST - Hierarchical φ-Scaled Connections")
    print("="*70)
    print(f"Theoretical d_w = {D_W_THEORY:.6f}")
    print(f"Theoretical d_s = {D_S_THEORY:.6f}")
    print("="*70)
    
    # Build graph with bridges
    print(f"\n[1] Building graph with bridges up to φ^{max_bridge_scale}...")
    graph = AetherBridgeGraph(depth=7, max_bridge_scale=max_bridge_scale)
    
    # Run simulations
    print("\n[2] Running random walks...")
    msd, p_return = graph.compute_msd_and_return(n_walkers=500, max_steps=400)
    t = np.arange(len(msd))
    
    # Fit exponents
    d_w_slope = fit_power_law(t, msd, x_min=30, x_max=250)
    d_s_slope = fit_power_law(t, p_return, x_min=30, x_max=250)
    
    measured_dw = 2 / d_w_slope if d_w_slope != 0 else 0
    measured_ds = -2 * d_s_slope if d_s_slope != 0 else 0
    
    print(f"\n[3] Results:")
    print(f"    d_w: {measured_dw:.4f} (theory: {D_W_THEORY:.4f})")
    print(f"    d_s: {measured_ds:.4f} (theory: {D_S_THEORY:.4f})")
    
    # Calculate errors
    dw_error = abs(measured_dw - D_W_THEORY) / D_W_THEORY * 100
    ds_error = abs(measured_ds - D_S_THEORY) / D_S_THEORY * 100
    
    print(f"\n    d_w error: {dw_error:.1f}%")
    print(f"    d_s error: {ds_error:.1f}%")
    
    # VERDICT
    print("\n" + "="*70)
    print("VERDICT")
    print("="*70)
    
    if dw_error < 20 and ds_error < 20:
        print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║  ✓ AETHER BRIDGES WORK                                                   ║
║                                                                           ║
║  Adding hierarchical φ-scaled bridges collapses d_w toward theory.       ║
║  The φ-Cantor universality class is NUMERICALLY VERIFIED.                ║
║                                                                           ║
║  This proves that "Aether" (non-local connectivity at φⁿ scales)         ║
║  is the mechanism that allows the universality class to manifest.        ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """)
    else:
        print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║  ✗ AETHER BRIDGES INSUFFICIENT                                           ║
║                                                                           ║
║  Even with bridges, d_w remains far from theory.                         ║
║  The φ-Cantor universality class is mathematically self-consistent       ║
║  but does NOT describe actual dynamics on this graph.                    ║
║                                                                           ║
║  Recommendation: Pivot to φ-RG learning rule.                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """)
    
    # Plot results
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # MSD plot
    axes[0].loglog(t[1:], msd[1:], 'b.', alpha=0.5, markersize=2, label='Simulation')
    t_fit = t[30:250]
    msd_fit = t_fit ** (2/measured_dw)
    axes[0].loglog(t_fit, msd_fit, 'r-', linewidth=2, label=f'Fit: d_w={measured_dw:.2f}')
    axes[0].loglog(t_fit, t_fit ** (2/D_W_THEORY), 'g--', linewidth=2, label=f'Theory: d_w={D_W_THEORY:.2f}')
    axes[0].set_xlabel('Time t')
    axes[0].set_ylabel('⟨r²(t)⟩')
    axes[0].set_title('Mean-Square Displacement')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Return probability plot
    axes[1].loglog(t[1:], p_return[1:], 'b.', alpha=0.5, markersize=2, label='Simulation')
    p_fit = t_fit ** (-measured_ds/2)
    axes[1].loglog(t_fit, p_fit, 'r-', linewidth=2, label=f'Fit: d_s={measured_ds:.2f}')
    axes[1].loglog(t_fit, t_fit ** (-D_S_THEORY/2), 'g--', linewidth=2, label=f'Theory: d_s={D_S_THEORY:.2f}')
    axes[1].set_xlabel('Time t')
    axes[1].set_ylabel('Return probability P(0,t)')
    axes[1].set_title('Return Probability')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('aether_bridge_test.png', dpi=150)
    plt.show()
    
    return measured_dw, measured_ds, dw_error, ds_error


if __name__ == "__main__":
    for scale in [2, 3, 4]:
        print(f"\n{'='*70}")
        print(f"TESTING WITH BRIDGES UP TO φ^{scale}")
        print(f"{'='*70}")
        dw, ds, err_dw, err_ds = run_bridge_test(max_bridge_scale=scale)
        
        if err_dw < 20:
            print(f"\n✅ SUCCESS at φ^{scale}! d_w error = {err_dw:.1f}%")
            break
    else:
        print("\n⚠️ Even with φ⁴ bridges, d_w error remains >20%")
        print("   Pivoting to φ-RG learning rule.")
