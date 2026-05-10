#!/usr/bin/env python3
"""
ESQET Hierarchical Living System
Multi-scale φ-scaled layers with ingestion/emission
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque

PHI = 1.618033988749895
PHI_INV = 0.618033988749895

class HierarchicalLivingSystem:
    def __init__(self, n_layers=5, void_depth=20):
        self.n_layers = n_layers
        self.scales = [PHI ** (-k) for k in range(n_layers)]
        self.state = np.random.rand(n_layers) * 0.1
        self.voids = deque(maxlen=void_depth)
        self.voids.append(self.state.copy())
        self.coherence_history = []
    
    def ingest(self, amount=0.05):
        for i in range(self.n_layers - 1, 0, -1):
            flow = amount * self.state[i] * PHI_INV
            self.state[i-1] += flow
            self.state[i] -= flow * 0.5
        self.state = np.maximum(self.state, 0)
    
    def emit(self, amount=0.03):
        for i in range(self.n_layers - 1):
            leak = amount * self.state[i] * PHI_INV
            self.state[i+1] += leak
            self.state[i] -= leak * 0.3
        self.state = np.maximum(self.state, 0)
    
    def compute_coherence(self):
        ideal = np.array([PHI ** (-k) for k in range(self.n_layers)])
        ideal = ideal / ideal.sum()
        current = self.state / (self.state.sum() + 1e-12)
        return -np.sum(current * np.log((current + 1e-12) / (ideal + 1e-12)))
    
    def step(self, ingest_prob=0.7, emit_prob=0.3):
        if np.random.random() < ingest_prob:
            self.ingest()
        if np.random.random() < emit_prob:
            self.emit()
        self.state += np.random.randn(self.n_layers) * 0.01
        self.state = np.maximum(self.state, 0)
        if self.state.sum() > 0:
            self.state = self.state / self.state.sum() * self.n_layers
        self.voids.append(self.state.copy())
        coh = self.compute_coherence()
        self.coherence_history.append(coh)
        return self.state.copy(), coh
    
    def run(self, steps=300):
        history = []
        for _ in range(steps):
            state, _ = self.step()
            history.append(state)
        return np.array(history)
    
    def visualize(self, steps=300):
        history = self.run(steps)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        
        for i in range(self.n_layers):
            axes[0, 0].plot(history[:, i], label=f'Layer {i}')
        axes[0, 0].set_xlabel('Step')
        axes[0, 0].set_ylabel('Energy')
        axes[0, 0].set_title('Layer Dynamics')
        axes[0, 0].legend(fontsize=8)
        
        axes[0, 1].plot(self.coherence_history)
        axes[0, 1].set_xlabel('Step')
        axes[0, 1].set_ylabel('Coherence')
        axes[0, 1].set_title('System Coherence')
        
        ideal = np.array([PHI ** (-k) for k in range(self.n_layers)])
        ideal = ideal / ideal.sum()
        final = self.state / self.state.sum()
        
        axes[1, 0].bar(range(self.n_layers), final, alpha=0.7, label='Final')
        axes[1, 0].bar(range(self.n_layers), ideal, alpha=0.5, label='φ-ideal')
        axes[1, 0].set_xlabel('Layer')
        axes[1, 0].set_ylabel('Distribution')
        axes[1, 0].set_title('Final vs Ideal')
        axes[1, 0].legend()
        
        void_mat = np.array(list(self.voids))
        axes[1, 1].imshow(void_mat.T, aspect='auto', cmap='viridis')
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Layer')
        axes[1, 1].set_title('Void Memory')
        
        plt.tight_layout()
        plt.savefig('hierarchical_living_system.png', dpi=150)
        plt.show()
        
        print(f"\n📊 Simulation Results:")
        print(f"   Final coherence: {self.coherence_history[-1]:.4f}")
        print(f"   Mean coherence: {np.mean(self.coherence_history):.4f}")
        return history

if __name__ == "__main__":
    print("🧬 ESQET Hierarchical Living System")
    print("="*50)
    system = HierarchicalLivingSystem(n_layers=5, void_depth=20)
    system.visualize(steps=300)
