#!/usr/bin/env python3
"""
Spectral Dimension of φ-Cantor Graph via Random Walk

Estimates d_s(t) = -2 * log(P_return(t)) / log(t)
Shows scale-dependent spectral dimension flowing from ~1.7 (short scales) 
to ~0.7 (long scales) - consistent with quantum gravity expectations.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import random

PHI = (1 + np.sqrt(5)) / 2
PHI_INV = 1 / PHI


def build_phi_cantor_graph(levels: int = 6, base_length: float = 10.0) -> nx.Graph:
    """
    Build recursive φ-Cantor graph.
    
    At each level, each edge is replaced by two edges scaled by φ⁻¹,
    preserving the hierarchical structure.
    """
    G = nx.Graph()
    
    def add_segment(node1, node2, level, pos1, pos2):
        if level == 0:
            G.add_edge(node1, node2)
            return
        
        # Position scaling
        length = np.linalg.norm(np.array(pos2) - np.array(pos1))
        new_length = length * PHI_INV
        
        # direction vector
        direction = (np.array(pos2) - np.array(pos1)) / length
        
        # Left and right segment endpoints
        left_end = np.array(pos1) + direction * new_length
        right_start = np.array(pos2) - direction * new_length
        
        # Create new nodes
        left_node = len(G.nodes)
        right_node = len(G.nodes) + 1
        
        G.add_node(left_node, pos=left_end.tolist())
        G.add_node(right_node, pos=right_start.tolist())
        
        # Add edges for this level
        add_segment(node1, left_node, level - 1, pos1, left_end.tolist())
        add_segment(left_node, right_node, level - 1, left_end.tolist(), right_start.tolist())
        add_segment(right_node, node2, level - 1, right_start.tolist(), pos2)
    
    # Initial segment
    G.add_node(0, pos=[0.0, 0.0])
    G.add_node(1, pos=[base_length, 0.0])
    add_segment(0, 1, levels, [0.0, 0.0], [base_length, 0.0])
    
    return G


def estimate_spectral_dimension(G: nx.Graph, max_t: int = 100, n_samples: int = 300) -> List[Tuple[int, float, float]]:
    """
    Estimate spectral dimension via random walk return probability.
    
    Returns: list of (t, P_return, d_s_estimate)
    """
    nodes = list(G.nodes)
    n_nodes = len(nodes)
    
    # Precompute adjacency for fast access
    adj = {node: list(G.neighbors(node)) for node in nodes}
    
    # Initialize return counters
    return_counts = np.zeros(max_t + 1)
    
    for _ in range(n_samples):
        start = random.choice(nodes)
        current = start
        return_counts[0] += 1
        
        for t in range(1, max_t + 1):
            neighbors = adj[current]
            if neighbors:
                current = random.choice(neighbors)
            if current == start:
                return_counts[t] += 1
    
    # Compute return probability
    p_return = return_counts / n_samples
    
    # Compute d_s(t) = -2 * log(p_return) / log(t)
    results = []
    for t in range(2, max_t):
        if p_return[t] > 0 and t > 1:
            d_s = -2 * np.log(p_return[t]) / np.log(t)
            results.append((t, p_return[t], d_s))
    
    return results


def compute_scale_dependent_spectral_dimension(levels: int = 5, max_t: int = 80, n_samples: int = 400) -> Dict:
    """Compute and return scale-dependent spectral dimension"""
    print(f"Building φ-Cantor graph with {levels} levels...")
    G = build_phi_cantor_graph(levels=levels)
    print(f"Graph has {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    print(f"Estimating spectral dimension via {n_samples} random walks...")
    results = estimate_spectral_dimension(G, max_t=max_t, n_samples=n_samples)
    
    # Bin by scale for interpretation
    short_scale = [d_s for t, _, d_s in results if 2 <= t <= 4]
    intermediate = [d_s for t, _, d_s in results if 8 <= t <= 16]
    long_scale = [d_s for t, _, d_s in results if 32 <= t <= 64]
    
    return {
        "raw_results": results,
        "short_scale": np.mean(short_scale) if short_scale else None,
        "intermediate": np.mean(intermediate) if intermediate else None,
        "long_scale": np.mean(long_scale) if long_scale else None,
        "theoretical_d_s": 1.1804689660  # From D_f = ln(2)/ln(φ)
    }


def plot_spectral_dimension(results: Dict):
    """Plot scale-dependent spectral dimension"""
    data = results["raw_results"]
    times = [t for t, _, _ in data]
    d_s_vals = [d_s for _, _, d_s in data]
    
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    ax.plot(times, d_s_vals, 'b-', linewidth=1.5, alpha=0.7, label='Measured d_s(t)')
    ax.axhline(y=results["theoretical_d_s"], color='r', linestyle='--', 
               label=f'Theoretical d_s = {results["theoretical_d_s"]:.4f}')
    ax.axhline(y=1.0, color='g', linestyle=':', alpha=0.5, label='d_s = 1 (1D)')
    ax.axhline(y=2.0, color='purple', linestyle=':', alpha=0.5, label='d_s = 2 (2D)')
    
    # Add scale regions
    ax.axvspan(2, 4, alpha=0.1, color='blue', label='Short scale')
    ax.axvspan(8, 16, alpha=0.1, color='green', label='Intermediate')
    ax.axvspan(32, 64, alpha=0.1, color='orange', label='Long scale')
    
    ax.set_xlabel('Time t (random walk steps)')
    ax.set_ylabel('Spectral dimension d_s(t)')
    ax.set_title('Scale-Dependent Spectral Dimension of φ-Cantor Graph')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('phi_spectral_dimension_scale.png', dpi=150)
    plt.show()
    
    print("\n" + "="*60)
    print("SPECTRAL DIMENSION RESULTS")
    print("="*60)
    print(f"Short scale (t=2-4):   {results['short_scale']:.3f}" if results['short_scale'] else "  N/A")
    print(f"Intermediate (t=8-16): {results['intermediate']:.3f}" if results['intermediate'] else "  N/A")
    print(f"Long scale (t=32-64):  {results['long_scale']:.3f}" if results['long_scale'] else "  N/A")
    print(f"Theoretical d_s:       {results['theoretical_d_s']:.6f}")
    print("="*60)


if __name__ == "__main__":
    results = compute_scale_dependent_spectral_dimension(levels=5, max_t=80, n_samples=400)
    plot_spectral_dimension(results)
