#!/usr/bin/env python3
"""
ESQET Dynamics Explorer v170.4
→ Bifurcation analysis w.r.t. φ parameter
→ Kuramoto synchronization in networks of φ-coupled oscillators
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

phi_base = (1 + np.sqrt(5)) / 2

def van_der_pol_bifurcation_demo():
    """Bifurcation study: amplitude vs φ"""
    print("Running bifurcation analysis on φ parameter...")
    
    phi_values = np.linspace(0.5, 5.0, 60)
    amplitudes = []
    
    for phi in phi_values:
        def vdp(state, t):
            x, v = state
            dx = v
            dv = phi * (1 - x**2) * v - x
            return [dx, dv]
        
        sol = odeint(vdp, [0.1, 0.0], np.linspace(0, 200, 4000))
        # Measure stable amplitude after transient
        amp = np.max(np.abs(sol[-1000:, 0]))
        amplitudes.append(amp)
    
    plt.figure(figsize=(10, 6))
    plt.plot(phi_values, amplitudes, 'o-', color='gold', linewidth=2)
    plt.axvline(x=phi_base, color='red', linestyle='--', label=f'Golden φ ≈ {phi_base:.5f}')
    plt.title('Bifurcation Diagram: Limit Cycle Amplitude vs φ')
    plt.xlabel('φ (nonlinear gain parameter)')
    plt.ylabel('Stable Oscillation Amplitude')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('simulations/bifurcation_phi_amplitude.png', dpi=300)
    plt.show()
    
    print(f"Golden φ = {phi_base:.5f} produces amplitude ≈ {amplitudes[np.argmin(np.abs(phi_values-phi_base))]:.4f}")


def kuramoto_network(n_osc=8, K=1.5, phi_influence=1.0):
    """Kuramoto model with φ-weighted natural frequencies"""
    print(f"\nSimulating Kuramoto network ({n_osc} oscillators) with φ influence...")
    
    # Natural frequencies influenced by φ
    omega = phi_influence * np.random.normal(0, 0.8, n_osc)
    theta = np.random.uniform(0, 2*np.pi, n_osc)
    
    def kuramoto_dynamics(theta, t, K):
        dtheta = omega.copy()
        for i in range(n_osc):
            for j in range(n_osc):
                dtheta[i] += (K / n_osc) * np.sin(theta[j] - theta[i])
        return dtheta
    
    t = np.linspace(0, 80, 4000)
    sol = odeint(kuramoto_dynamics, theta, t, args=(K,))
    
    # Order parameter (synchronization measure)
    R = np.abs(np.mean(np.exp(1j * sol), axis=1))
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    for i in range(min(6, n_osc)):
        plt.plot(t, sol[:, i] % (2*np.pi), alpha=0.8, label=f'Osc {i+1}')
    plt.title(f'Kuramoto Synchronization Network (K={K}, φ-influence={phi_influence})')
    plt.ylabel('Phase θ_i (mod 2π)')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 1, 2)
    plt.plot(t, R, 'red', linewidth=2.5)
    plt.title('Global Order Parameter R(t) — Synchronization Level')
    plt.xlabel('Time')
    plt.ylabel('R (0 = incoherent, 1 = fully synchronized)')
    plt.ylim(0, 1.05)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('simulations/kuramoto_phi_synchronization.png', dpi=300)
    plt.show()
    
    print(f"Final synchronization level R = {R[-1]:.4f}")


if __name__ == "__main__":
    print("ESQET Dynamics Explorer — Bifurcation + Synchronization\n")
    
    # 1. Bifurcation analysis
    van_der_pol_bifurcation_demo()
    
    # 2. Kuramoto network
    kuramoto_network(n_osc=12, K=2.0, phi_influence=phi_base)
    
    print("\nExploration complete.")
    print("Key insight: φ acts as a tunable parameter affecting both individual oscillator amplitude and network synchronization strength.")
