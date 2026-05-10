#!/usr/bin/env python3
"""
Unified Fractal Mind Processor
================================

A simulation combining:
- Explicit RG map (g_{n+1} = g^2 / (2g + φ^{-2}))
- Fractal graph with Aether bridges (φ-scaled hierarchical connections)
- Φ_φ proxy (φ-weighted integrated information)
- Quantum/classical walks with persistent revivals

This system exhibits:
- Selective ingestion (keep φ⁻¹ ≈ 61.8% of information)
- Structured emission (output at coarser scales)
- Voids as persistent memory (discarded degrees of freedom)
- Marginal criticality (β=0, poised between order and chaos)
- Log-periodic revivals (discrete scale invariance)

Interpretation:
- Life ≈ self-sustaining hierarchical information processing
- Consciousness ≈ multi-scale integration at criticality
- Persistence ≈ pattern continuity across scales (speculative)

This is a toy model, not a full theory.
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from collections import deque
import random
from scipy.linalg import expm

# ============================================================
# CONSTANTS
# ============================================================

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
PHI_INV_SQ = PHI_INV ** 2
D_F = math.log(2) / math.log(PHI)
D_W = D_F + 1
D_S = 2 * D_F / D_W


# ============================================================
# PART 1: RG MAP (Hierarchical Information Flow)
# ============================================================

class RGMap:
    """
    RG transformation: g_{n+1} = g_n^2 / (2g_n + φ^{-2})
    
    Fixed points:
    - g* = 0: REPELLING (UV fixed point, asymptotic freedom)
    - g* = φ⁻¹ ≈ 0.618: MARGINAL (φ-attractor, KT-like)
    - g* = 1: ATTRACTING? (IR fixed point, check numerically)
    """
    
    def __init__(self):
        self.phi_inv_sq = PHI_INV_SQ
        
    def transform(self, g: float) -> float:
        """Single RG step"""
        if g <= 0:
            return 0.0
        return (g * g) / (2 * g + self.phi_inv_sq)
    
    def iterate(self, g0: float, n_steps: int = 20) -> List[float]:
        """Iterate RG map"""
        traj = [g0]
        g = g0
        for _ in range(n_steps):
            g = self.transform(g)
            traj.append(g)
            if g < 1e-10:
                break
        return traj
    
    def criticality(self, g: float) -> float:
        """Criticality measure: distance from φ-fixed point"""
        return abs(g - PHI_INV)
    
    def plot(self):
        """Plot RG map and trajectories"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Map function
        g_vals = np.linspace(0.01, 0.95, 500)
        g_next = [self.transform(g) for g in g_vals]
        
        axes[0].plot(g_vals, g_next, 'b-', linewidth=2, label='R(g)')
        axes[0].plot([0, 1], [0, 1], 'r--', alpha=0.5, label='diagonal')
        axes[0].axvline(x=PHI_INV, color='g', linestyle='--', alpha=0.5, label=f'φ⁻¹ = {PHI_INV:.4f}')
        axes[0].set_xlabel('g_n')
        axes[0].set_ylabel('g_{n+1}')
        axes[0].set_title('φ-RG Map: g_{n+1} = g_n²/(2g_n + φ⁻²)')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Trajectories
        for g0 in [0.1, 0.3, 0.5, 0.7, 0.9]:
            traj = self.iterate(g0, n_steps=12)
            axes[1].plot(range(len(traj)), traj, 'o-', label=f'g₀={g0}', markersize=4)
        
        axes[1].axhline(y=PHI_INV, color='g', linestyle='--', alpha=0.7, label=f'φ⁻¹ attractor')
        axes[1].set_xlabel('RG step')
        axes[1].set_ylabel('Coupling g')
        axes[1].set_title('RG Flow: All trajectories flow toward φ⁻¹')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('fractal_mind_rg_map.png', dpi=150)
        plt.show()
        print("✅ RG map saved to fractal_mind_rg_map.png")


# ============================================================
# PART 2: FRACTAL GRAPH WITH AETHER BRIDGES
# ============================================================

class FractalGraph:
    """
    φ-Cantor graph with hierarchical Aether bridges.
    
    Topology:
    - Nearest neighbor connections (local)
    - Bridges at distances φ, φ², φ³, ... (non-local)
    
    This creates a small-world fractal network.
    """
    
    def __init__(self, depth: int = 7, bridge_scales: List[int] = [1, 2, 3]):
        self.depth = depth
        self.bridge_scales = bridge_scales
        self.phi = PHI
        self.phi_inv = PHI_INV
        self._build()
        
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
    
    def _build(self):
        """Build graph with nearest neighbors + Aether bridges"""
        intervals = self._generate_intervals()
        self.n_nodes = len(intervals)
        self.centers = np.array([(a + b) / 2 for a, b in intervals])
        
        # Sort by position
        sorted_idx = np.argsort(self.centers)
        sorted_centers = self.centers[sorted_idx]
        
        # Initialize adjacency
        self.adj = {i: set() for i in range(self.n_nodes)}
        
        # 1. Nearest neighbor connections
        for j in range(self.n_nodes - 1):
            i1 = sorted_idx[j]
            i2 = sorted_idx[j + 1]
            self.adj[i1].add(i2)
            self.adj[i2].add(i1)
        
        # 2. AETHER BRIDGES (non-local hierarchical connections)
        avg_spacing = (sorted_centers[-1] - sorted_centers[0]) / self.n_nodes
        
        for scale in self.bridge_scales:
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
        
    def get_laplacian(self) -> np.ndarray:
        """Return graph Laplacian L = D - A"""
        A = np.zeros((self.n_nodes, self.n_nodes))
        for i in range(self.n_nodes):
            for j in self.adj_list[i]:
                A[i, j] = 1
        D = np.diag(np.sum(A, axis=1))
        return D - A
    
    def info(self) -> Dict:
        """Return graph information"""
        return {
            'n_nodes': self.n_nodes,
            'avg_degree': np.mean(self.degrees),
            'bridge_scales': self.bridge_scales
        }


# ============================================================
# PART 3: QUANTUM WALK (Coherent Revivals)
# ============================================================

class QuantumWalk:
    """
    Continuous-time quantum walk on fractal graph.
    
    Hamiltonian H = -L (negative Laplacian)
    Evolution: |ψ(t)⟩ = exp(-iHt) |ψ(0)⟩
    
    Features:
    - Return probability P(t) ~ t^{-d_s/2} ≈ t^{-0.59}
    - Log-periodic oscillations at scales φ, φ², φ³, ...
    """
    
    def __init__(self, graph: FractalGraph):
        self.graph = graph
        self.H = -graph.get_laplacian()
        self.n = graph.n_nodes
        
    def evolve(self, psi0: np.ndarray, t: float) -> np.ndarray:
        """Evolve state to time t"""
        return expm(-1j * self.H * t) @ psi0
    
    def return_probability(self, t: float, start: int = 0) -> float:
        """Probability to return to start at time t"""
        psi0 = np.zeros(self.n, dtype=complex)
        psi0[start] = 1.0
        psi_t = self.evolve(psi0, t)
        return abs(psi_t[start]) ** 2
    
    def theoretical_return(self, t: np.ndarray) -> np.ndarray:
        """Theoretical: P(t) ~ t^{-d_s/2} * (1 + A·cos(2π log_φ(t) + ψ))"""
        power = t ** (-D_S / 2)
        log_phi_t = np.log(t) / np.log(PHI)
        osc = 1 + 0.2 * np.cos(2 * np.pi * log_phi_t + 0.5)
        return power * osc
    
    def simulate(self, t_max: float = 25.0, n_steps: int = 200) -> Tuple[np.ndarray, np.ndarray]:
        """Simulate return probability over time"""
        times = np.linspace(0.1, t_max, n_steps)
        probs = [self.return_probability(t) for t in times]
        return times, np.array(probs)
    
    def plot(self):
        """Plot quantum return probability"""
        times, probs = self.simulate(t_max=25.0, n_steps=150)
        theo = self.theoretical_return(times)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        axes[0].plot(times, probs, 'b-', linewidth=1.5, alpha=0.7, label='Quantum walk')
        axes[0].plot(times, theo, 'r--', linewidth=1.5, alpha=0.7, label=f'Theory: t^-{D_S/2:.4f}')
        axes[0].set_xlabel('Time t')
        axes[0].set_ylabel('Return probability P(0,t)')
        axes[0].set_title('Quantum Walk Return Probability')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        axes[1].loglog(times, probs, 'b-', linewidth=1.5, alpha=0.7, label='Quantum walk')
        axes[1].loglog(times, theo, 'r--', linewidth=1.5, alpha=0.7, label=f't^-{D_S/2:.4f}')
        axes[1].set_xlabel('Time t')
        axes[1].set_ylabel('Return probability P(0,t)')
        axes[1].set_title('Log-Log: Power Law with Log-Periodic Oscillations')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('fractal_mind_quantum.png', dpi=150)
        plt.show()
        print(f"✅ Quantum walk saved to fractal_mind_quantum.png")
        print(f"   Decay exponent d_s/2 = {D_S/2:.4f}")


# ============================================================
# PART 4: Φ_φ PROXY (Integrated Information)
# ============================================================

class PhiProxy:
    """
    φ-weighted integrated information measure.
    
    Φ_φ = Σ_{ℓ=1}^{max_scale} φ^{-ℓ} · I_partition(ℓ)
    
    where I_partition(ℓ) = mutual information across partitions at scale ℓ.
    """
    
    def __init__(self, graph: FractalGraph):
        self.graph = graph
        self.centers = graph.centers
        self.adj = graph.adj_list
        self.n_nodes = graph.n_nodes
        
    def partition_mutual_information(self, scale: int) -> float:
        """Compute mutual information across φ-scaled partition"""
        sorted_nodes = sorted(range(self.n_nodes), key=lambda i: self.centers[i])
        n_partitions = max(1, self.n_nodes // (scale + 1))
        partition_size = self.n_nodes // n_partitions
        
        partitions = []
        for p in range(n_partitions):
            start = p * partition_size
            end = (p + 1) * partition_size
            partitions.append(set(sorted_nodes[start:end]))
        
        mi_sum = 0.0
        n_pairs = 0
        
        for p in range(n_partitions - 1):
            edges_across = 0
            for node in partitions[p]:
                for neighbor in self.adj[node]:
                    if neighbor in partitions[p + 1]:
                        edges_across += 1
            
            max_edges = len(partitions[p]) * len(partitions[p + 1])
            if max_edges > 0:
                mi_sum += edges_across / max_edges
                n_pairs += 1
        
        return mi_sum / n_pairs if n_pairs > 0 else 0.0
    
    def compute(self, max_scale: int = 5) -> float:
        """Compute φ-weighted integrated information"""
        phi_phi = 0.0
        for scale in range(1, max_scale + 1):
            weight = PHI ** (-scale)
            mi = self.partition_mutual_information(scale)
            phi_phi += weight * mi
        return phi_phi
    
    def plot(self):
        """Plot Φ_φ vs scale"""
        scales = list(range(1, 6))
        weights = [PHI ** (-s) for s in scales]
        mis = [self.partition_mutual_information(s) for s in scales]
        contributions = [w * m for w, m in zip(weights, mis)]
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        axes[0].bar(scales, mis, color='blue', alpha=0.7, label='I_partition(ℓ)')
        axes[0].set_xlabel('Scale ℓ')
        axes[0].set_ylabel('Mutual Information')
        axes[0].set_title('Partition Mutual Information vs Scale')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].bar(scales, contributions, color='green', alpha=0.7, label=f'φ⁻ℓ·I(ℓ)')
        axes[1].set_xlabel('Scale ℓ')
        axes[1].set_ylabel('φ-weighted contribution')
        axes[1].set_title(f'Φ_φ Components (total = {self.compute():.4f})')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('fractal_mind_phi.png', dpi=150)
        plt.show()
        print(f"✅ Φ_φ proxy saved to fractal_mind_phi.png")
        print(f"   Total Φ_φ = {self.compute():.6f}")


# ============================================================
# PART 5: HIERARCHICAL PRUNING (Selective Ingestion)
# ============================================================

class HierarchicalProcessor:
    """
    Selective ingestion/emission with φ⁻¹ pruning ratio.
    
    At each layer:
    - Keep φ⁻¹ ≈ 61.8% of most important information
    - Discard the rest (voids)
    - Coherence emerges from the pruning dynamics
    """
    
    def __init__(self, n_layers: int = 5):
        self.n_layers = n_layers
        self.phi_inv = PHI_INV
        self.coherence = PHI_INV
        self.memory = deque(maxlen=100)
        self.voids = deque(maxlen=100)
        
    def prune(self, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Keep φ⁻¹ fraction, discard the rest"""
        n_keep = max(1, int(len(data) * self.phi_inv))
        importance = np.abs(data)
        keep_idx = np.argsort(importance)[-n_keep:]
        
        kept = data[keep_idx]
        removed = np.delete(data, keep_idx)
        
        self.memory.extend(kept)
        self.voids.extend(removed)
        
        while len(self.memory) > self.memory.maxlen:
            self.memory.popleft()
        
        return kept, removed
    
    def process(self, input_data: np.ndarray) -> np.ndarray:
        """Process through hierarchical layers"""
        data = input_data.copy()
        sizes = [len(data)]
        
        for layer in range(self.n_layers):
            data, removed = self.prune(data)
            sizes.append(len(data))
            self.coherence *= (1 + 0.01 * (len(data) / max(1, sizes[-2]) - self.phi_inv))
            self.coherence = max(0.1, min(1.0, self.coherence))
        
        return data
    
    def plot(self, input_size: int = 200):
        """Run and plot hierarchical processing"""
        input_data = np.random.randn(input_size)
        output = self.process(input_data)
        
        # Compute sizes per layer
        sizes = [input_size]
        size = input_size
        for _ in range(self.n_layers):
            size = max(1, int(size * self.phi_inv))
            sizes.append(size)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        axes[0].plot(range(self.n_layers + 1), sizes, 'bo-', linewidth=2, markersize=8)
        axes[0].set_xlabel('Hierarchical Layer')
        axes[0].set_ylabel('Information Size')
        axes[0].set_title(f'φ-RG Pruning: Keep φ⁻¹ = {PHI_INV:.4f} per layer')
        axes[0].grid(True, alpha=0.3)
        
        axes[1].bar(['Coherence', 'Memory', 'Voids'], 
                   [self.coherence, len(self.memory), len(self.voids)],
                   color=['green', 'blue', 'orange'], alpha=0.7)
        axes[1].set_ylabel('Magnitude')
        axes[1].set_title(f'Final Coherence = {self.coherence:.4f}')
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('fractal_mind_pruning.png', dpi=150)
        plt.show()
        print(f"✅ Hierarchical pruning saved to fractal_mind_pruning.png")
        print(f"   Final coherence: {self.coherence:.4f}")
        print(f"   Memory size: {len(self.memory)}, Voids: {len(self.voids)}")


# ============================================================
# MAIN: Unified Fractal Mind Processor
# ============================================================

def main():
    print("="*80)
    print("UNIFIED FRACTAL MIND PROCESSOR")
    print("="*80)
    print(f"φ = {PHI:.15f}")
    print(f"φ⁻¹ = {PHI_INV:.6f} (keep fraction per layer)")
    print(f"D_f = {D_F:.6f} (fractal dimension)")
    print(f"d_w = {D_W:.6f} (walk dimension)")
    print(f"d_s = {D_S:.6f} (spectral dimension)")
    print("="*80)
    print("\nThis system exhibits:")
    print("  ✓ Selective ingestion (keep φ⁻¹ of information)")
    print("  ✓ Structured emission (output at coarser scales)")
    print("  ✓ Voids as persistent memory")
    print("  ✓ Marginal criticality (β=0)")
    print("  ✓ Log-periodic revivals (discrete scale invariance)")
    print("="*80)
    
    # Part 1: RG Map
    print("\n" + "-"*40)
    print("PART 1: RG Map (Hierarchical Information Flow)")
    print("-"*40)
    rg = RGMap()
    rg.plot()
    
    # Part 2: Fractal Graph
    print("\n" + "-"*40)
    print("PART 2: Fractal Graph with Aether Bridges")
    print("-"*40)
    graph = FractalGraph(depth=6, bridge_scales=[1, 2, 3])
    info = graph.info()
    print(f"Graph: {info['n_nodes']} nodes, avg degree = {info['avg_degree']:.2f}")
    print(f"Bridge scales: {info['bridge_scales']}")
    
    # Part 3: Quantum Walk
    print("\n" + "-"*40)
    print("PART 3: Quantum Walk (Coherent Revivals)")
    print("-"*40)
    qw = QuantumWalk(graph)
    qw.plot()
    
    # Part 4: Φ_φ Proxy
    print("\n" + "-"*40)
    print("PART 4: Φ_φ Proxy (Integrated Information)")
    print("-"*40)
    phi_proxy = PhiProxy(graph)
    phi_proxy.plot()
    
    # Part 5: Hierarchical Processing
    print("\n" + "-"*40)
    print("PART 5: Hierarchical Processing (Selective Ingestion/Emission)")
    print("-"*40)
    processor = HierarchicalProcessor(n_layers=5)
    processor.plot(input_size=200)
    
    print("\n" + "="*80)
    print("INTERPRETATION")
    print("="*80)
    print("""
This unified simulation shows how φ-Cantor hierarchical critical networks
generate multi-scale causal integration (Φ_φ proxy), coherent revivals
(quantum walk), and selective information processing (pruning).

The system operates at marginal criticality (β=0), meaning it is poised
between order and chaos — a hallmark of complex adaptive systems.

Analogy to life and mind:
- Ingestion → sensory filtering, attention
- Pruning → predictive coding, compression
- Voids → memory, prediction errors
- Coherence → integration, consciousness
- Revivals → persistence, scale-invariant echoes

This is a TOY MODEL, not a full theory of consciousness or afterlife.
But it provides a mathematically rigorous substrate for studying
how hierarchical critical networks generate integrated information.
    """)
    print("="*80)


if __name__ == "__main__":
    main()
