#!/usr/bin/env python3
"""
φ-Parameterized Renormalization Graph Automata (φ-RGA) v2.1
============================================================

Enhanced features:
- Spectral dimension estimation (classical random walks)
- Quantum walk algorithms (continuous-time)
- Master action optimization with global optimization
- Golden mean networking (φ-weighted edges)
- Scale-dependent dimensionality flow

This is a COMPUTATIONAL PHYSICS framework.
Reproducible, testable, falsifiable.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from collections import deque
import random
import time
import json
import networkx as nx
from scipy.optimize import curve_fit, differential_evolution
from scipy.sparse.linalg import expm_multiply
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# CONSTANTS
# ============================================================

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
PHI_4 = (7 + 3 * math.sqrt(5)) / 2
M_PL = 1.220910e19  # GeV


# ============================================================
# SPECTRAL DIMENSION ANALYSIS (Classical Random Walks)
# ============================================================

def random_walk_return_prob(G: nx.Graph, max_t: int = 128, n_walks: int = 2000, 
                            seed: int = 42) -> np.ndarray:
    """
    Compute return probability p0(t) via classical random walks.
    
    Returns array of p0[t] for t = 0..max_t
    """
    np.random.seed(seed)
    returns = np.zeros(max_t + 1)
    nodes = list(G.nodes())
    
    for _ in range(n_walks):
        start = np.random.choice(nodes)
        pos = start
        returns[0] += 1
        
        for t in range(1, max_t + 1):
            neighbors = list(G.neighbors(pos))
            if neighbors:
                pos = np.random.choice(neighbors)
            if pos == start:
                returns[t] += 1
    
    return returns / n_walks


def fit_spectral_dimension(t: np.ndarray, p0: np.ndarray, 
                           windows: List[Tuple[str, int, int]] = None) -> Dict:
    """
    Multi-window spectral dimension fitting.
    
    Returns d_s for UV, short, intermediate, and long time scales.
    """
    if windows is None:
        windows = [
            ("uv_short", 4, 12),
            ("short", 6, 24),
            ("intermediate", 16, 48),
            ("long", 32, 96)
        ]
    
    def model(logt, logA, ds):
        return logA - (ds / 2.0) * logt
    
    results = {}
    for name, tmin, tmax in windows:
        mask = (t >= tmin) & (t <= tmax) & (p0 > 1e-9)
        
        if np.sum(mask) < 8:
            results[name] = {"ds": np.nan, "r2": 0.0, "std": np.nan}
            continue
        
        log_t = np.log(t[mask])
        log_p = np.log(p0[mask])
        
        try:
            popt, pcov = curve_fit(model, log_t, log_p, p0=[0, 1.2], 
                                   bounds=([-20, 0.1], [20, 5.0]))
            ds_fit = popt[1]
            perr = np.sqrt(np.diag(pcov))[1] if pcov.shape == (2, 2) else 0.05
            
            residuals = log_p - model(log_t, *popt)
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((log_p - np.mean(log_p))**2)
            r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            results[name] = {"ds": float(ds_fit), "r2": float(r2), "std": float(perr)}
        except:
            results[name] = {"ds": np.nan, "r2": 0.0, "std": np.nan}
    
    return results


# ============================================================
# QUANTUM WALK ALGORITHMS
# ============================================================

def continuous_time_quantum_walk(G: nx.Graph, time: float = 10.0, 
                                   marked: List[int] = None) -> np.ndarray:
    """
    Continuous-time quantum walk via Hamiltonian H = -γ·A.
    
    Returns final state |ψ(t)>
    """
    A = nx.adjacency_matrix(G).tocsc()
    degrees = dict(G.degree()).values()
    gamma = 1.0 / max(degrees) if max(degrees) > 0 else 1.0
    
    H = -gamma * A  # Hamiltonian
    
    n = G.number_of_nodes()
    
    # Initial state
    if marked is not None:
        psi0 = np.zeros(n, dtype=complex)
        for m in marked:
            psi0[m] = 1.0 / np.sqrt(len(marked))
    else:
        psi0 = np.ones(n, dtype=complex) / np.sqrt(n)
    
    # Evolve
    psi_t = expm_multiply(-1j * H, psi0, start=0, stop=time, num=100)
    return psi_t[-1]  # return final state


def quantum_return_prob(G: nx.Graph, times: np.ndarray, 
                        start_node: int = 0) -> np.ndarray:
    """
    Quantum return probability |⟨start|ψ(t)⟩|²
    """
    probs = []
    A = nx.adjacency_matrix(G).tocsc()
    H = -A  # simple choice
    
    n = G.number_of_nodes()
    psi0 = np.zeros(n, dtype=complex)
    psi0[start_node] = 1.0
    
    for t in times:
        psi_t = expm_multiply(-1j * H, psi0, start=0, stop=t, num=1)[-1]
        p_return = np.abs(psi_t[start_node])**2
        probs.append(p_return)
    
    return np.array(probs)


def hybrid_walk_analysis(G: nx.Graph, max_t: int = 64, 
                         n_walks: int = 1000) -> Dict:
    """
    Compare classical and quantum walk return probabilities.
    """
    times = np.linspace(0.1, max_t, min(max_t, 50))
    
    # Classical
    p_classical = random_walk_return_prob(G, max_t=int(max_t), n_walks=n_walks)
    t_classical = np.arange(len(p_classical))
    
    # Quantum
    p_quantum = quantum_return_prob(G, times, start_node=0)
    
    return {
        "classical": {"t": t_classical, "p": p_classical},
        "quantum": {"t": times, "p": p_quantum},
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges()
    }


# ============================================================
# GOLDEN MEAN NETWORKING
# ============================================================

class GoldenMeanNetwork:
    """Enhanced networking with explicit golden ratio properties"""
    
    @staticmethod
    def phi_weighted_edges(G: nx.Graph, base_weight: float = 1.0) -> nx.Graph:
        """Apply φ-scaled weights based on node layer difference"""
        for u, v in G.edges():
            layer_u = G.nodes[u].get('layer', 0)
            layer_v = G.nodes[v].get('layer', 0)
            delta = abs(layer_u - layer_v)
            weight = base_weight * (PHI ** (-delta))
            G.edges[u, v]['weight'] = weight
        return G
    
    @staticmethod
    def golden_centrality(G: nx.Graph) -> Dict:
        """φ-modulated eigenvector centrality"""
        try:
            cent = nx.eigenvector_centrality_numpy(G, weight='weight')
            phi_cent = {n: cent[n] * (PHI ** -G.nodes[n].get('layer', 0)) 
                       for n in cent}
            return phi_cent
        except:
            return nx.degree_centrality(G)
    
    @staticmethod
    def optimal_bridge_scales(max_scale: int = 4) -> List[int]:
        """Generate φ-optimal bridge scales"""
        return [int(PHI ** k) for k in range(1, max_scale + 1)]


# ============================================================
# GRAPH NODE AND GENERATOR
# ============================================================

@dataclass
class GraphNode:
    """Node in the hierarchical graph"""
    id: int
    layer: int
    value: float = 0.0
    connections: List[int] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class HierarchicalGraphGenerator:
    """φ-scaled hierarchical graph generator"""
    
    def __init__(self, depth: int = 6, bridge_scales: List[int] = None):
        self.depth = depth
        self.bridge_scales = bridge_scales or GoldenMeanNetwork.optimal_bridge_scales(3)
        self.phi = PHI
        self.phi_inv = PHI_INV
        self.nodes: Dict[int, GraphNode] = {}
        self._generate()
        
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
    
    def _generate(self):
        """Generate graph with hierarchical structure"""
        intervals = self._generate_intervals()
        n_nodes = len(intervals)
        centers = [(a + b) / 2 for a, b in intervals]
        
        # Create nodes
        for i, center in enumerate(centers):
            layer = int(math.log(i + 1, 2)) if i > 0 else 0
            self.nodes[i] = GraphNode(id=i, layer=min(layer, self.depth), value=center)
        
        # Build adjacency (nearest neighbors)
        sorted_nodes = sorted(self.nodes.values(), key=lambda n: n.value)
        for j in range(len(sorted_nodes) - 1):
            n1 = sorted_nodes[j].id
            n2 = sorted_nodes[j + 1].id
            self.nodes[n1].connections.append(n2)
            self.nodes[n2].connections.append(n1)
        
        # Add φ-scaled bridges
        if self.bridge_scales:
            positions = [n.value for n in sorted_nodes]
            avg_spacing = (positions[-1] - positions[0]) / len(positions) if positions else 1.0
            
            for scale in self.bridge_scales:
                bridge_dist = (PHI ** scale) * avg_spacing
                for i, pos_i in enumerate(positions):
                    for j in range(i + 1, min(i + 30, len(positions))):
                        actual_dist = abs(positions[j] - pos_i)
                        if actual_dist > 0 and abs(actual_dist - bridge_dist) / bridge_dist < 0.3:
                            n1 = sorted_nodes[i].id
                            n2 = sorted_nodes[j].id
                            if n2 not in self.nodes[n1].connections:
                                self.nodes[n1].connections.append(n2)
                                self.nodes[n2].connections.append(n1)
    
    def to_networkx(self) -> nx.Graph:
        """Convert to NetworkX graph with golden ratio features"""
        G = nx.Graph()
        for nid, node in self.nodes.items():
            G.add_node(nid, layer=node.layer, value=node.value)
        for nid, node in self.nodes.items():
            for conn in node.connections:
                G.add_edge(nid, conn)
        
        # Apply golden mean enhancements
        G = GoldenMeanNetwork.phi_weighted_edges(G)
        return G
    
    def get_statistics(self) -> Dict:
        """Return graph statistics"""
        degrees = [len(n.connections) for n in self.nodes.values()]
        return {
            "n_nodes": len(self.nodes),
            "avg_degree": np.mean(degrees) if degrees else 0,
            "degree_std": np.std(degrees) if degrees else 0,
            "depth": self.depth,
            "bridge_scales": self.bridge_scales
        }


# ============================================================
# MASTER ACTION SIMULATOR
# ============================================================

@dataclass
class ActionComponents:
    S_geom: float = 0.0
    S_top: float = 0.0
    S_matter: float = 0.0
    S_constraint: float = 0.0
    total: float = 0.0


class MasterActionSimulator:
    """ESQET Master Action Simulator with optimization"""
    
    def __init__(self, n_generations: int = 3, n_hierarchy: int = 80):
        self.n_generations = n_generations
        self.n_hierarchy = n_hierarchy
        self.phi = PHI
        self.phi_inv = PHI_INV
        self.m_pl = M_PL
        
        # Coupling constants (to be optimized)
        self.alpha = 1.0
        self.beta = 1.0
        self.lambda_constraint = 1.0
        
        # Optimization bounds
        self.bounds = {'alpha': (0.1, 5.0), 'beta': (0.1, 5.0), 'lambda': (0.01, 10.0)}
        
        self.history = []
    
    def compute_spectral_flow(self, d_s_uv: float = 1.18, d_s_ir: float = 4.0, 
                               scale: float = 1.0) -> float:
        return d_s_ir - (d_s_ir - d_s_uv) * math.exp(-scale)
    
    def compute_geometric_action(self, n_nodes: int = 100, avg_degree: float = 2.5) -> float:
        R_phi = (avg_degree - 2) / max(avg_degree, 1)
        D_s = self.compute_spectral_flow(scale=n_nodes / 100.0)
        return max(R_phi + self.alpha * D_s, 0.0)
    
    def compute_topological_action(self) -> float:
        cs_level = self.n_generations
        z3_penalty = 0.0 if self.n_generations == 3 else abs(self.n_generations - 3)
        return self.beta * (cs_level + z3_penalty)
    
    def compute_mass_hierarchy(self, generation: int) -> float:
        offsets = [0, 10, 20]
        n = self.n_hierarchy + (offsets[generation] if generation < len(offsets) else 0)
        return self.m_pl * (self.phi ** (-n))
    
    def compute_matter_action(self) -> float:
        total_mass = sum(self.compute_mass_hierarchy(gen) for gen in range(self.n_generations))
        return total_mass / self.m_pl
    
    def compute_gauge_anomaly(self) -> float:
        return float(self.n_generations * 0.0)  # SM anomaly-free
    
    def compute_gravitational_anomaly(self) -> float:
        return float(self.n_generations * 0.0)
    
    def compute_phi_flow_current(self) -> float:
        return 1 / self.n_hierarchy if self.n_hierarchy > 0 else 0
    
    def compute_constraint_action(self) -> float:
        A_gauge = self.compute_gauge_anomaly()
        A_grav = self.compute_gravitational_anomaly()
        div_J = self.compute_phi_flow_current()
        return self.lambda_constraint * (A_gauge**2 + A_grav**2 + div_J**2)
    
    def compute_total_action(self, verbose: bool = False) -> ActionComponents:
        S_geom = self.compute_geometric_action()
        S_top = self.compute_topological_action()
        S_matter = self.compute_matter_action()
        S_constraint = self.compute_constraint_action()
        total = S_geom + S_top + S_matter + S_constraint
        
        if verbose:
            print(f"  S_geom = {S_geom:.6f}, S_top = {S_top:.6f}")
            print(f"  S_matter = {S_matter:.6f}, S_constraint = {S_constraint:.6f}")
            print(f"  Total = {total:.6f}")
        
        return ActionComponents(S_geom, S_top, S_matter, S_constraint, total)
    
    def objective(self, params: List[float]) -> float:
        """Objective function for global optimization"""
        self.alpha, self.beta, self.lambda_constraint = params
        comp = self.compute_total_action(verbose=False)
        penalty = 0.01 * (self.alpha + self.beta + self.lambda_constraint)
        return comp.total + penalty
    
    def global_optimize(self) -> Dict:
        """Global optimization with differential evolution"""
        bounds = [self.bounds['alpha'], self.bounds['beta'], self.bounds['lambda']]
        result = differential_evolution(self.objective, bounds, workers=1, tol=1e-6)
        
        self.alpha, self.beta, self.lambda_constraint = result.x
        return {
            "optimal_params": result.x.tolist(),
            "min_action": result.fun,
            "success": result.success
        }
    
    def scan_hierarchy(self, n_range: range = None) -> Tuple[List[Dict], Dict]:
        if n_range is None:
            n_range = range(70, 91)
        results = []
        for n in n_range:
            self.n_hierarchy = n
            comp = self.compute_total_action(verbose=False)
            results.append({
                "n": n,
                "total_action": comp.total,
                "v_calc": M_PL * (PHI ** (-n))
            })
        min_result = min(results, key=lambda x: x["total_action"])
        return results, min_result


# ============================================================
# MAIN ANALYSIS
# ============================================================

def run_complete_analysis():
    """Run complete φ-RGA analysis with all features"""
    
    print("="*70)
    print("φ-RGA v2.1: Spectral Dimension + Quantum Walks + Master Action")
    print("="*70)
    
    config = {
        "depth": 5,
        "bridge_scales": [1, 2, 3],
        "n_walks_classical": 1500,
        "max_t": 64,
        "seed": 42
    }
    
    print(f"\n[CONFIG] {config}")
    
    # Set seed
    random.seed(config["seed"])
    np.random.seed(config["seed"])
    
    # Generate graph
    print("\n[STEP 1] Generating φ-Cantor graph...")
    graph = HierarchicalGraphGenerator(depth=config["depth"], 
                                       bridge_scales=config["bridge_scales"])
    stats = graph.get_statistics()
    G_nx = graph.to_networkx()
    print(f"  Nodes: {stats['n_nodes']}, Edges: {G_nx.number_of_edges()}")
    print(f"  Avg degree: {stats['avg_degree']:.2f}")
    
    # Spectral dimension (classical)
    print("\n[STEP 2] Computing spectral dimension (classical random walks)...")
    p0 = random_walk_return_prob(G_nx, max_t=config["max_t"], 
                                  n_walks=config["n_walks_classical"])
    t = np.arange(len(p0))
    ds_results = fit_spectral_dimension(t, p0)
    
    for name, res in ds_results.items():
        if not np.isnan(res["ds"]):
            print(f"  {name:15s}: d_s = {res['ds']:.4f} ± {res['std']:.4f} (R²={res['r2']:.4f})")
    
    # Quantum walk
    print("\n[STEP 3] Computing quantum walk return probability...")
    times = np.linspace(0.1, 20, 30)
    q_probs = quantum_return_prob(G_nx, times, start_node=0)
    print(f"  Quantum return at t=10: {q_probs[min(10, len(q_probs)-1)]:.6f}")
    
    # Master action
    print("\n[STEP 4] Master action optimization...")
    master = MasterActionSimulator(n_generations=3, n_hierarchy=80)
    opt_result = master.global_optimize()
    print(f"  Optimal params: α={opt_result['optimal_params'][0]:.3f}, "
          f"β={opt_result['optimal_params'][1]:.3f}, λ={opt_result['optimal_params'][2]:.3f}")
    print(f"  Min action: {opt_result['min_action']:.6f}")
    
    # Hierarchy scan
    print("\n[STEP 5] Hierarchy exponent scan...")
    results, min_h = master.scan_hierarchy(range(70, 91))
    print(f"  Minimum action at n = {min_h['n']}")
    print(f"  v = M_Pl·φ⁻{min_h['n']} = {min_h['v_calc']:.1f} GeV")
    
    # Plotting
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Return probability
    axes[0, 0].loglog(t[1:], p0[1:], 'b.', alpha=0.5, markersize=2)
    axes[0, 0].set_xlabel('Time t')
    axes[0, 0].set_ylabel('Return probability p₀(t)')
    axes[0, 0].set_title('Classical Random Walk Return Probability')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Spectral dimension by window
    names = list(ds_results.keys())
    ds_vals = [ds_results[n]["ds"] for n in names]
    ds_errs = [ds_results[n]["std"] for n in names]
    bars = axes[0, 1].bar(names, ds_vals, yerr=ds_errs, capsize=5, 
                          color=['blue', 'green', 'orange', 'red'])
    axes[0, 1].axhline(y=1.18, color='purple', linestyle='--', label='φ-Cantor proxy')
    axes[0, 1].set_ylabel('Spectral dimension d_s')
    axes[0, 1].set_title('Scale-Dependent Spectral Dimension')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Quantum return probability
    axes[1, 0].plot(times, q_probs, 'b-', linewidth=1.5)
    axes[1, 0].set_xlabel('Time t')
    axes[1, 0].set_ylabel('Return probability |⟨0|ψ(t)⟩|²')
    axes[1, 0].set_title('Quantum Walk Return Probability')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Hierarchy action scan
    n_vals = [r["n"] for r in results]
    action_vals = [r["total_action"] for r in results]
    axes[1, 1].plot(n_vals, action_vals, 'bo-', linewidth=2)
    axes[1, 1].axvline(x=80, color='r', linestyle='--', label='n=80')
    axes[1, 1].set_xlabel('Hierarchy exponent n')
    axes[1, 1].set_ylabel('Total Action S_ESQET')
    axes[1, 1].set_title('Master Action Minimization')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.suptitle('φ-RGA v2.1: Complete Analysis Suite', fontsize=14)
    plt.tight_layout()
    plt.savefig('phi_rga_v21_complete.png', dpi=150)
    plt.show()
    
    print("\n[RESULTS] Saved to phi_rga_v21_complete.png")
    
    return {
        "graph_stats": stats,
        "spectral_dimension": ds_results,
        "master_action_optimal": opt_result,
        "hierarchy_min": min_h
    }


if __name__ == "__main__":
    results = run_complete_analysis()
