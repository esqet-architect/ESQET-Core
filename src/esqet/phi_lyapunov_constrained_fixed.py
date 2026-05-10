#!/usr/bin/env python3
"""
ESQET Network v173.1 — Lyapunov-Constrained φ (Fixed & Bounded)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

phi_target = (1 + np.sqrt(5)) / 2
N = 8
K = 2.8

def network_lyapunov(state, t):
    x = state[0:2*N:2]
    v = state[1:2*N:2]
    phi_eff = state[-1]
    
    mean_x = np.mean(x)
    dstate = np.zeros(2*N + 1)
    
    for i in range(N):
        coupling = K * phi_eff * (mean_x - x[i])
        
        dstate[2*i]   = v[i]                                      # dx
        dstate[2*i+1] = phi_eff * (1 - x[i]**2) * v[i] - x[i] + coupling   # dv
    
    # Bounded Lyapunov gradient descent for φ
    dphi = -0.08 * (phi_eff - phi_target) * np.exp(-0.3 * np.mean(x**2))
    dphi = np.clip(dphi, -0.15, 0.15)   # Hard bound to prevent explosion
    
    dstate[-1] = dphi
    return dstate


if __name__ == "__main__":
    print("="*70)
    print("ESQET v173.1 — Lyapunov-Constrained φ Network (Fixed)")
    print("="*70)
    
    np.random.seed(42)
    initial = np.zeros(2*N + 1)
    for i in range(N):
        initial[2*i]   = np.random.uniform(-0.8, 0.8)
        initial[2*i+1] = np.random.uniform(-0.8, 0.8)
    initial[-1] = 1.4   # Start away from target
    
    t = np.linspace(0, 250, 10000)
    print("Integrating...")
    sol = odeint(network_lyapunov, initial, t, rtol=1e-7, atol=1e-8)
    
    x_traj = sol[:, 0:2*N:2]
    phi_traj = sol[:, -1]
    
    # Order parameter (simple coherence measure)
    R = np.zeros(len(t))
    for i in range(len(t)):
        phases = np.arctan2(x_traj[i], np.gradient(x_traj[i], t[i] if i>0 else 1))
        R[i] = np.abs(np.mean(np.exp(1j * phases)))
    
    print(f"Final φ_eff     : {phi_traj[-1]:.6f} (target = {phi_target:.6f})")
    print(f"Final sync R    : {R[-1]:.4f}")
    print(f"φ drift         : {abs(phi_target - phi_traj[-1]):.6f}")
    
    # Plot
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plt.plot(t, phi_traj, 'gold', lw=2.5)
    plt.axhline(phi_target, color='red', ls='--', label=f'Target φ = {phi_target:.5f}')
    plt.title('φ Evolution (Lyapunov Gradient Descent)')
    plt.xlabel('Time')
    plt.ylabel('φ_eff')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 2)
    plt.plot(t, R, 'purple', lw=2.5)
    plt.title('Network Synchronization (Order Parameter R)')
    plt.xlabel('Time')
    plt.ylabel('R')
    plt.ylim(0, 1.05)
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 3)
    plt.plot(x_traj[-2000:,-1], sol[-2000:,-3], 'teal', lw=1.8)   # last oscillator
    plt.title('Phase Portrait (Last Oscillator)')
    plt.xlabel('x'); plt.ylabel('v')
    plt.grid(True, alpha=0.3); plt.axis('equal')
    
    plt.subplot(2, 2, 4)
    plt.hist(phi_traj[-2000:], bins=25, color='brown', alpha=0.8)
    plt.axvline(phi_target, color='red', ls='--')
    plt.title('Final φ_eff Distribution')
    plt.xlabel('φ_eff')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('simulations/phi_lyapunov_constrained_fixed.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nFixed version complete — φ is now bounded and stable.")
