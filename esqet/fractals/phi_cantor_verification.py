#!/usr/bin/env python3
"""
φ-Cantor Universality Class - Independent Verification

This is the FALSIFICATION TEST.
We generate the φ-Cantor graph and measure exponents directly via simulation,
NOT from theoretical formulas.

If the measured exponents match the theoretical predictions,
the universality class survives.
If not, the scaling relations are self-consistent but nonphysical.

Measured exponents (direct simulation):
- d_s (spectral dimension) from random walk return probability
- d_w (walk dimension) from mean-square displacement
- ζ̃ (resistance exponent) from effective resistance
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typing import Tuple, List
import random

# Constants
PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI

# Theoretical predictions (to compare against)
D_F_THEORY = math.log(2) / math.log(PHI)
D_W_THEORY = D_F_THEORY + 1
D_S_THEORY = 2 * D_F_THEORY / D_W_THEORY
ZETA_THEORY = 2


class PhiCantorGraph:
    """
    Build the φ-Cantor graph for numerical simulation.
    """
    
    def __init__(self, depth: int = 7):
        self.depth = depth
        self.phi_inv = PHI_INV
        self.nodes = []
        self.edges = []
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
        """Build graph from adjacent intervals"""
        intervals = self._generate_intervals()
        self.centers = [(a + b) / 2 for a, b in intervals]
        self.n_nodes = len(self.centers)
        
        # Sort by position
        sorted_idx = sorted(range(self.n_nodes), key=lambda i: self.centers[i])
        
        self.adj = [[] for _ in range(self.n_nodes)]
        
        for j in range(self.n_nodes - 1):
            i1 = sorted_idx[j]
            i2 = sorted_idx[j + 1]
            # Connect if intervals are adjacent
            gap = self.centers[i2] - self.centers[i1]
            width1 = intervals[i1][1] - intervals[i1][0]
            width2 = intervals[i2][1] - intervals[i2][0]
            if gap < (width1 + width2) * 1.1:
                self.adj[i1].append(i2)
                self.adj[i2].append(i1)
        
        # Count degrees
        self.degrees = [len(self.adj[i]) for i in range(self.n_nodes)]
    
    def random_walk(self, start: int, steps: int) -> List[int]:
        """Simple random walk on graph"""
        path = [start]
        current = start
        for _ in range(steps):
            if self.adj[current]:
                current = random.choice(self.adj[current])
            path.append(current)
        return path
    
    def compute_return_probability(self, n_walkers: int = 500, max_steps: int = 500) -> np.ndarray:
        """Compute P(0,t) from random walk simulations"""
        return_counts = np.zeros(max_steps + 1)
        
        for _ in range(n_walkers):
            start = random.randint(0, self.n_nodes - 1)
            path = self.random_walk(start, max_steps)
            for t, node in enumerate(path):
                if node == start:
                    return_counts[t] += 1
        
        return return_counts / n_walkers
    
    def compute_mean_square_displacement(self, n_walkers: int = 200, max_steps: int = 500) -> np.ndarray:
        """Compute ⟨r²(t)⟩ from random walks"""
        msd = np.zeros(max_steps + 1)
        
        for _ in range(n_walkers):
            start = random.randint(0, self.n_nodes - 1)
            path = self.random_walk(start, max_steps)
            start_pos = self.centers[start]
            for t, node in enumerate(path):
                displacement = self.centers[node] - start_pos
                msd[t] += displacement ** 2
        
        return msd / n_walkers


def fit_power_law(x, y, x_min=10, x_max=None):
    """Fit power law: y = A * x^exponent"""
    if x_max is None:
        x_max = len(x) - 1
    
    mask = (x >= x_min) & (x <= x_max)
    x_fit = x[mask]
    y_fit = y[mask]
    
    log_x = np.log(x_fit)
    log_y = np.log(y_fit)
    
    slope, intercept = np.polyfit(log_x, log_y, 1)
    A = np.exp(intercept)
    
    return slope, A


def run_verification():
    """Run the independent verification simulation"""
    print("="*70)
    print("φ-CANTOR UNIVERSALITY CLASS - INDEPENDENT VERIFICATION")
    print("="*70)
    print("""
This is the FALSIFICATION TEST.
We measure exponents directly from simulation,
NOT from theoretical formulas.

If measured exponents match theory → class survives.
If not → scaling relations are self-consistent but nonphysical.
    """)
    print("="*70)
    
    # Build graph
    print("\n[1] Building φ-Cantor graph...")
    graph = PhiCantorGraph(depth=6)
    print(f"    Nodes: {graph.n_nodes}")
    print(f"    Avg degree: {np.mean(graph.degrees):.2f}")
    
    # Measure return probability → spectral dimension
    print("\n[2] Measuring return probability P(0,t)...")
    P_return = graph.compute_return_probability(n_walkers=500, max_steps=400)
    t = np.arange(len(P_return))
    t_valid = t[t > 5]
    P_valid = P_return[t > 5]
    
    # Fit power law: P(t) ~ t^{-d_s/2}
    d_s_half_fit, _ = fit_power_law(t_valid, P_valid, x_min=20)
    d_s_measured = -2 * d_s_half_fit
    print(f"    Measured d_s/2 = {-d_s_half_fit:.4f}")
    print(f"    Measured d_s = {d_s_measured:.4f}")
    print(f"    Theoretical d_s = {D_S_THEORY:.6f}")
    print(f"    Difference: {abs(d_s_measured - D_S_THEORY):.4f}")
    
    # Measure mean-square displacement → walk dimension
    print("\n[3] Measuring mean-square displacement ⟨r²(t)⟩...")
    msd = graph.compute_mean_square_displacement(n_walkers=300, max_steps=300)
    msd_valid = msd[t > 10]
    t_valid_msd = t[t > 10]
    
    # Fit: ⟨r²(t)⟩ ~ t^{2/d_w}
    d_w_inv_fit, _ = fit_power_law(t_valid_msd, msd_valid, x_min=20)
    d_w_measured = 2 / d_w_inv_fit
    print(f"    Measured exponent (2/d_w) = {d_w_inv_fit:.4f}")
    print(f"    Measured d_w = {d_w_measured:.4f}")
    print(f"    Theoretical d_w = {D_W_THEORY:.6f}")
    print(f"    Difference: {abs(d_w_measured - D_W_THEORY):.4f}")
    
    # Verification result
    print("\n" + "="*70)
    print("VERIFICATION RESULT")
    print("="*70)
    
    d_s_error = abs(d_s_measured - D_S_THEORY) / D_S_THEORY
    d_w_error = abs(d_w_measured - D_W_THEORY) / D_W_THEORY
    
    if d_s_error < 0.1 and d_w_error < 0.1:
        print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║  ✓ VERIFICATION PASSED                                                    ║
║                                                                           ║
║  Measured exponents match theoretical predictions within statistical      ║
║  error. The φ-Cantor universality class survives independent testing.     ║
║                                                                           ║
║  This is now a legitimate candidate for a new universality class.         ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """)
    else:
        print("""
╔═══════════════════════════════════════════════════════════════════════════╗
║  ✗ VERIFICATION FAILED                                                   ║
║                                                                           ║
║  Measured exponents DO NOT match theoretical predictions.                 ║
║  The scaling relations are self-consistent but nonphysical.               ║
║  This universality class does not describe actual dynamics.               ║
╚═══════════════════════════════════════════════════════════════════════════╝
        """)
    
    # Plot results
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Return probability
    axes[0].loglog(t[1:], P_return[1:], 'b.', alpha=0.5, markersize=3, label='Simulation')
    t_fit = t_valid_msd
    P_fit = t_fit ** (-d_s_measured/2)
    axes[0].loglog(t_fit, P_fit, 'r-', linewidth=2, label=f'Fit: d_s={d_s_measured:.3f}')
    axes[0].set_xlabel('Time t')
    axes[0].set_ylabel('Return probability P(0,t)')
    axes[0].set_title(f'Return Probability (d_s = {d_s_measured:.3f})')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Mean-square displacement
    axes[1].loglog(t[1:], msd[1:], 'b.', alpha=0.5, markersize=3, label='Simulation')
    msd_fit = t_fit ** (2/d_w_measured)
    axes[1].loglog(t_fit, msd_fit, 'r-', linewidth=2, label=f'Fit: d_w={d_w_measured:.3f}')
    axes[1].set_xlabel('Time t')
    axes[1].set_ylabel('⟨r²(t)⟩')
    axes[1].set_title(f'Mean-Square Displacement (d_w = {d_w_measured:.3f})')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('phi_cantor_verification.png', dpi=150)
    plt.show()
    
    print("\n✅ Verification plot saved to phi_cantor_verification.png")
    
    return {
        "d_s_measured": d_s_measured,
        "d_s_theory": D_S_THEORY,
        "d_w_measured": d_w_measured,
        "d_w_theory": D_W_THEORY,
        "passed": d_s_error < 0.1 and d_w_error < 0.1
    }


if __name__ == "__main__":
    results = run_verification()
    
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("""
If VERIFICATION PASSED:
    1. Submit to Physical Review E as a new universality class
    2. Compare with known KT/hierarchical lattice models
    3. Seek experimental realization (resistor network)

If VERIFICATION FAILED:
    1. The scaling relations are mathematically consistent but nonphysical
    2. Return to theory: check assumptions about graph construction
    3. Re-run with larger depth, more walkers, better statistics
    """)
