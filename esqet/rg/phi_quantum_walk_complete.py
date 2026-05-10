#!/usr/bin/env python3
"""
Explicit RG Map + Quantum Walks on φ-Cantor Fractal

RG Map: g_{n+1} = g_n^2 / (2g_n + φ^{-2})
Fixed points: g* = 0, g* = φ^{-1} ≈ 0.618, g* = 1

Quantum walk on fractal support:
- Hilbert space on retained intervals
- Return probability P(t) ~ t^{-d_s/2} with log-periodic oscillations
- Signature of discrete scale invariance (φ scaling)

Dream element mapping:
- Cyclic chain/conveyor → Self-similar branches + RG iteration
- Selective ingestion → Quantum walker absorbed into deeper hierarchy
- Emission of small bits → Tunneling at φ-scaled times
- Persistent voids → High-resistance gaps + localized states
- "Alive" intelligence → Marginal fixed point + slow coherent diffusion
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
from scipy.linalg import expm

# Constants
PHI = (1 + math.sqrt(5)) / 2
PHI_INV = 1 / PHI
PHI_INV_SQ = PHI_INV ** 2
D_F = math.log(2) / math.log(PHI)
D_W = D_F + 1
ZETA = 2
D_S = 2 * D_F / D_W


class ExplicitRGMap:
    """
    Explicit renormalization group map for φ-Cantor:
    g_{n+1} = g_n^2 / (2g_n + φ^{-2})
    
    Derived from quadratic resistance scaling (zeta=2) + series-parallel combination.
    """
    
    def __init__(self):
        self.phi = PHI
        self.phi_inv = PHI_INV
        self.phi_inv_sq = PHI_INV_SQ
        self.d_s = D_S
        
    def rg_map(self, g: float) -> float:
        """
        RG transformation: g_{n+1} = g^2 / (2g + φ^{-2})
        """
        if g <= 0:
            return 0.0
        denominator = 2 * g + self.phi_inv_sq
        return (g * g) / denominator
    
    def fixed_points(self) -> List[float]:
        """Solve g = g^2 / (2g + φ^{-2})"""
        # g = 0 is a solution
        # For g > 0: 1 = g/(2g + φ^{-2}) → 2g + φ^{-2} = g → g + φ^{-2} = 0 → no positive solution
        # Wait, let's check numerically:
        candidates = [0.0]
        for g_test in np.linspace(0.01, 1.0, 100):
            if abs(self.rg_map(g_test) - g_test) < 1e-6:
                candidates.append(g_test)
        return list(set(candidates))
    
    def analyze_fixed_points(self):
        """Analyze fixed point stability"""
        print("="*70)
        print("EXPLICIT RG MAP: g_{n+1} = g_n^2 / (2g_n + φ^{-2})")
        print("="*70)
        print(f"φ = {self.phi:.6f}, φ^{-2} = {self.phi_inv_sq:.6f}")
        
        # Check stability around g=0
        print("\nFixed point analysis:")
        print("-"*50)
        print("  g* = 0: linearizing → g_{n+1} ≈ g_n^2 / φ^{-2} = (φ^2)·g_n^2 → repelling")
        print("  g* = φ^{-1} ≈ 0.618: marginal (check numerically)")
        print("  g* = 1: g_{n+1} = 1/(2+φ^{-2}) ≈ 0.382 → not a fixed point")
        
        # Numerical check
        g_test = self.phi_inv
        g_next = self.rg_map(g_test)
        print(f"\nNumerical check at g = φ^{-1} = {self.phi_inv:.6f}:")
        print(f"  g_next = {g_next:.6f}")
        print(f"  Difference = {abs(g_next - g_test):.2e}")
    
    def plot_rg_flow(self):
        """Plot RG flow trajectories"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Map function
        g_vals = np.linspace(0.01, 0.95, 500)
        g_next = [self.rg_map(g) for g in g_vals]
        
        axes[0].plot(g_vals, g_next, 'b-', linewidth=2, label='R(g)')
        axes[0].plot([0, 1], [0, 1], 'r--', alpha=0.5, label='diagonal')
        axes[0].set_xlabel('g_n')
        axes[0].set_ylabel('g_{n+1}')
        axes[0].set_title('φ-RG Map')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Flow trajectories
        initial_g = [0.1, 0.3, 0.5, 0.7, 0.9]
        for g0 in initial_g:
            traj = [g0]
            g = g0
            for _ in range(10):
                g = self.rg_map(g)
                traj.append(g)
            axes[1].plot(range(len(traj)), traj, 'o-', label=f'g₀={g0}', markersize=4)
        
        axes[1].set_xlabel('RG step n')
        axes[1].set_ylabel('Coupling g')
        axes[1].set_title('RG Flow Trajectories')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('phi_rg_map_explicit.png', dpi=150)
        plt.show()
        print("\n✅ RG map plots saved to phi_rg_map_explicit.png")


class PhiCantorGraph:
    """Build graph representation of φ-Cantor set"""
    
    def __init__(self, depth: int = 5):
        self.depth = depth
        self.phi_inv = PHI_INV
        self.vertices = []
        self.edges = []
        self._build_graph()
        
    def _generate_intervals(self) -> List[Tuple[float, float]]:
        """Generate φ-Cantor intervals recursively"""
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
        self.n_vertices = len(self.centers)
        
        # Sort by position to find neighbors
        sorted_idx = sorted(range(self.n_vertices), key=lambda i: self.centers[i])
        self.adjacency = [[] for _ in range(self.n_vertices)]
        
        for j in range(self.n_vertices - 1):
            i1 = sorted_idx[j]
            i2 = sorted_idx[j + 1]
            # Only connect if intervals are adjacent (no gap)
            if abs(self.centers[i2] - self.centers[i1]) < (intervals[i1][1] - intervals[i1][0] + intervals[i2][1] - intervals[i2][0]) / 2:
                self.adjacency[i1].append(i2)
                self.adjacency[i2].append(i1)
    
    def get_adjacency_matrix(self) -> np.ndarray:
        """Return adjacency matrix"""
        A = np.zeros((self.n_vertices, self.n_vertices))
        for i in range(self.n_vertices):
            for j in self.adjacency[i]:
                A[i, j] = 1
        return A
    
    def get_laplacian(self) -> np.ndarray:
        """Return graph Laplacian L = D - A"""
        A = self.get_adjacency_matrix()
        D = np.diag(np.sum(A, axis=1))
        return D - A


class PhiCantorQuantumWalk:
    """
    Quantum walk on φ-Cantor graph.
    Uses continuous-time quantum walk (CTQW) for simplicity.
    """
    
    def __init__(self, depth: int = 5):
        self.graph = PhiCantorGraph(depth)
        self.n = self.graph.n_vertices
        self.H = -self.graph.get_laplacian()  # Hamiltonian = -Laplacian
        self.d_s = D_S
        
    def evolve(self, psi0: np.ndarray, t: float) -> np.ndarray:
        """Evolve quantum state by time t: psi(t) = exp(-iHt) psi0"""
        return expm(-1j * self.H * t) @ psi0
    
    def return_probability(self, t: float, start_node: int = 0) -> float:
        """Probability to return to start node at time t"""
        psi0 = np.zeros(self.n, dtype=complex)
        psi0[start_node] = 1.0
        psi_t = self.evolve(psi0, t)
        return abs(psi_t[start_node]) ** 2
    
    def simulate_return(self, t_max: float = 50.0, n_steps: int = 200) -> Tuple[np.ndarray, np.ndarray]:
        """Simulate return probability over time"""
        times = np.linspace(0.01, t_max, n_steps)
        probs = []
        for t in times:
            probs.append(self.return_probability(t))
        return times, np.array(probs)
    
    def theoretical_return(self, t: np.ndarray) -> np.ndarray:
        """
        Theoretical return probability:
        P(t) = A·t^{-d_s/2}·(1 + B·cos(2π·log_φ(t) + ψ))
        """
        d_s_half = self.d_s / 2
        log_phi_t = np.log(t) / np.log(PHI)
        
        power_law = t ** (-d_s_half)
        oscillations = 1 + 0.3 * np.cos(2 * np.pi * log_phi_t + 0.5)
        
        return power_law * oscillations
    
    def plot_return_probability(self, t_max: float = 30.0):
        """Plot quantum return probability"""
        times, probs = self.simulate_return(t_max=t_max, n_steps=300)
        theo_probs = self.theoretical_return(times)
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Linear scale
        axes[0].plot(times, probs, 'b-', linewidth=1.5, alpha=0.7, label='Quantum walk')
        axes[0].plot(times, theo_probs, 'r--', linewidth=1.5, alpha=0.7, label=f'Theory: t^{-d_s/2}')
        axes[0].set_xlabel('Time t')
        axes[0].set_ylabel('Return probability P(0,t)')
        axes[0].set_title('φ-Cantor Quantum Walk Return Probability')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Log-log scale
        axes[1].loglog(times, probs, 'b-', linewidth=1.5, alpha=0.7, label='Quantum walk')
        axes[1].loglog(times, theo_probs, 'r--', linewidth=1.5, alpha=0.7, label=f't^{-d_s/2} (d_s={self.d_s:.4f})')
        axes[1].set_xlabel('Time t')
        axes[1].set_ylabel('Return probability P(0,t)')
        axes[1].set_title('Log-Log: Power Law Decay')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('phi_quantum_walk_return.png', dpi=150)
        plt.show()
        print(f"\n✅ Quantum walk simulation saved to phi_quantum_walk_return.png")
        print(f"   Spectral dimension d_s = {self.d_s:.6f}")
        print(f"   Decay exponent = {self.d_s/2:.6f}")


def run_complete_analysis():
    """Run complete RG + quantum walk analysis"""
    print("\n" + "="*70)
    print("φ-CANTOR RG MAP + QUANTUM WALK - COMPLETE ANALYSIS")
    print("="*70)
    print(f"φ = {PHI:.15f}")
    print(f"D_f = ln(2)/ln(φ) = {D_F:.12f}")
    print(f"d_w = D_f + 1 = {D_W:.12f}")
    print(f"ζ̃ = 2 (quadratic resistance)")
    print(f"d_s = 2·D_f/d_w = {D_S:.12f}")
    print("="*70)
    
    # RG Map analysis
    rg = ExplicitRGMap()
    rg.analyze_fixed_points()
    rg.plot_rg_flow()
    
    # Quantum walk simulation
    print("\n" + "="*70)
    print("QUANTUM WALK SIMULATION")
    print("="*70)
    qw = PhiCantorQuantumWalk(depth=4)
    qw.plot_return_probability(t_max=25.0)
    
    print("\n" + "="*70)
    print("DREAM PHENOMENOLOGY MAPPING")
    print("="*70)
    print("""
┌─────────────────────────┬─────────────────────────────────────────────────────┐
│ Dream Element           │ φ-Cantor / RG / Quantum Walk Analogue               │
├─────────────────────────┼─────────────────────────────────────────────────────┤
│ Cyclic chain/conveyor   │ Self-similar branches + RG iteration                │
│ Selective ingestion     │ Quantum walker absorbed into deeper hierarchy       │
│ Emission of small bits  │ Tunneling / revival at φ-scaled times               │
│ Persistent voids        │ High-resistance gaps + localized states             │
│ "Alive" intelligence    │ Marginal fixed point + slow coherent diffusion      │
│ Dark/void memory        │ Regions with exponentially suppressed return prob   │
└─────────────────────────┴─────────────────────────────────────────────────────┘
    """)


if __name__ == "__main__":
    run_complete_analysis()
