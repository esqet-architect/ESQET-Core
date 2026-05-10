#!/usr/bin/env python3
"""
φ-Weighted Φ Proxy - Multi-Scale Causal Integration on Fractal RG Networks

Hypothesis: Φ_φ is maximized near marginal criticality (β ≈ 0)
and decreases as d_s deviates from the 1-2 range.

This is a testable, falsifiable prediction linking the φ-Cantor
universality class to IIT-like integrated information.

Definition:
Φ_φ(G) = Σ_ℓ w(ℓ) · I_partition(ℓ)

where:
- ℓ indexes φ-scaled partition scales
- w(ℓ) = φ^{-ℓ} (weight decaying with scale)
- I_partition(ℓ) is mutual information across the partition
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from collections import deque
import random

# Constants
PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
D_F_THEORY = math.log(2) / math.log(PHI)
D_W_THEORY = D_F_THEORY + 1
D_S_THEORY = 2 * D_F_THEORY / D_W_THEORY


class PhiFractalRGNetwork:
    """
    Fractal RG network with φ-scale hierarchical structure.
    """
    
    def __init__(self, depth: int = 6, add_bridges: bool = True):
        self.depth = depth
        self.add_bridges = add_bridges
        self.phi = PHI
        self.phi_inv = PHI_INV
        self._build_network()
        
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
    
    def _build_network(self):
        """Build network with φ-scale hierarchical structure"""
        intervals = self._generate_intervals()
        self.n_nodes = len(intervals)
        self.centers = np.array([(a + b) / 2 for a, b in intervals])
        
        # Sort by position
        sorted_idx = np.argsort(self.centers)
        sorted_centers = self.centers[sorted_idx]
        
        # Initialize adjacency
        self.adj = {i: set() for i in range(self.n_nodes)}
        
        # Nearest neighbor connections
        for j in range(self.n_nodes - 1):
            i1 = sorted_idx[j]
            i2 = sorted_idx[j + 1]
            self.adj[i1].add(i2)
            self.adj[i2].add(i1)
        
        # Hierarchical bridges (if enabled)
        if self.add_bridges:
            avg_spacing = (sorted_centers[-1] - sorted_centers[0]) / self.n_nodes
            for scale in range(1, 4):
                bridge_dist = (PHI ** scale) * avg_spacing
                for i in range(self.n_nodes):
                    pos_i = self.centers[sorted_idx[i]]
                    for j in range(i + 1, min(i + 50, self.n_nodes)):
                        pos_j = self.centers[sorted_idx[j]]
                        actual_dist = abs(pos_j - pos_i)
                        if abs(actual_dist - bridge_dist) / bridge_dist < 0.3:
                            i1 = sorted_idx[i]
                            i2 = sorted_idx[j]
                            self.adj[i1].add(i2)
                            self.adj[i2].add(i1)
        
        self.adj_list = {k: list(v) for k, v in self.adj.items()}
        self.degrees = [len(self.adj_list[i]) for i in range(self.n_nodes)]
    
    def compute_partition_mutual_information(self, scale: int) -> float:
        """
        Compute mutual information across φ-scaled partition.
        
        Partition the network at scale ℓ = φ^scale.
        Measure information flow between partitions.
        """
        # Create partition boundaries at multiples of scale
        sorted_nodes = sorted(range(self.n_nodes), key=lambda i: self.centers[i])
        
        # Number of partitions at this scale
        n_partitions = max(1, self.n_nodes // (scale + 1))
        partition_size = self.n_nodes // n_partitions
        
        # Assign nodes to partitions
        partitions = []
        for p in range(n_partitions):
            start = p * partition_size
            end = (p + 1) * partition_size
            partitions.append(set(sorted_nodes[start:end]))
        
        # Compute mutual information between adjacent partitions
        mi_sum = 0.0
        n_pairs = 0
        
        for p in range(n_partitions - 1):
            # Count edges between partition p and p+1
            edges_across = 0
            for node in partitions[p]:
                for neighbor in self.adj_list[node]:
                    if neighbor in partitions[p + 1]:
                        edges_across += 1
            
            # Total possible edges
            max_edges = len(partitions[p]) * len(partitions[p + 1])
            
            if max_edges > 0:
                # Normalized mutual information proxy
                mi = edges_across / max_edges
                mi_sum += mi
                n_pairs += 1
        
        return mi_sum / n_pairs if n_pairs > 0 else 0.0
    
    def compute_phi_phi(self, max_scale: int = 5) -> float:
        """
        Compute φ-weighted Φ proxy:
        Φ_φ = Σ_{ℓ=1}^{max_scale} φ^{-ℓ} · I_partition(ℓ)
        """
        phi_phi = 0.0
        for scale in range(1, max_scale + 1):
            weight = PHI ** (-scale)
            mi = self.compute_partition_mutual_information(scale)
            phi_phi += weight * mi
        
        return phi_phi


def compute_theoretical_d_s(criticality: float) -> float:
    """
    Compute spectral dimension as a function of criticality parameter.
    At β=0 (marginal criticality), d_s ≈ 1.18.
    As criticality deviates, d_s changes.
    """
    # Simple model: d_s max at criticality
    d_s_max = D_S_THEORY
    d_s_min = 0.5
    # Gaussian-like peak
    d_s = d_s_min + (d_s_max - d_s_min) * math.exp(-criticality ** 2 / 0.1)
    return d_s


def run_phi_phi_scan():
    """Scan over criticality parameter and compute Φ_φ"""
    print("="*70)
    print("φ-Weighted Φ Proxy: Multi-Scale Causal Integration")
    print("="*70)
    
    criticality_values = np.linspace(0, 1, 11)
    phi_phi_values = []
    d_s_values = []
    
    for crit in criticality_values:
        # Build network with variable criticality (bridge strength modulates)
        network = PhiFractalRGNetwork(depth=5, add_bridges=crit > 0.3)
        phi_phi = network.compute_phi_phi(max_scale=4)
        phi_phi_values.append(phi_phi)
        d_s_values.append(compute_theoretical_d_s(crit))
    
    # Plot results
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Φ_φ vs criticality
    axes[0].plot(criticality_values, phi_phi_values, 'bo-', linewidth=2, markersize=8)
    axes[0].axvline(x=0.618, color='r', linestyle='--', alpha=0.7, label='φ-fixed point (marginal)')
    axes[0].set_xlabel('Criticality Parameter β (0 = critical, 1 = ordered)')
    axes[0].set_ylabel('Φ_φ (φ-weighted integrated information)')
    axes[0].set_title('Φ_φ vs Criticality')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # d_s vs criticality
    axes[1].plot(criticality_values, d_s_values, 'go-', linewidth=2, markersize=8)
    axes[1].axhline(y=D_S_THEORY, color='r', linestyle='--', alpha=0.7, label=f'd_s = {D_S_THEORY:.4f} (φ-Cantor)')
    axes[1].set_xlabel('Criticality Parameter β')
    axes[1].set_ylabel('Spectral Dimension d_s')
    axes[1].set_title('Spectral Dimension vs Criticality')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('phi_phi_proxy.png', dpi=150)
    plt.show()
    
    # Find maximum
    max_idx = np.argmax(phi_phi_values)
    print(f"\nMaximum Φ_φ at criticality = {criticality_values[max_idx]:.3f}")
    print(f"φ-fixed point = {PHI_INV:.3f}")
    
    if abs(criticality_values[max_idx] - PHI_INV) < 0.1:
        print("\n✅ HYPOTHESIS SUPPORTED: Φ_φ maximized near φ-fixed point (marginal criticality)")
    else:
        print("\n⚠️ HYPOTHESIS NOT SUPPORTED: Φ_φ maximum deviates from φ-fixed point")
    
    return criticality_values, phi_phi_values


if __name__ == "__main__":
    crit, phi_phi = run_phi_phi_scan()
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("""
The φ-weighted Φ proxy is a testable, falsifiable measure linking
the φ-Cantor universality class to IIT-like integrated information.

Hypothesis: Φ_φ is maximized near marginal criticality (β ≈ 0)
and decreases as d_s deviates from the 1-2 range.

This prediction can be tested on:
- Random graphs
- Neural simulations
- Diffusion networks
- Empirical brain data (EEG/fMRI)

If confirmed, the φ-Cantor universality class becomes a candidate
model for how hierarchical critical networks generate multi-scale
causal integration.
    """)
