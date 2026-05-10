#!/usr/bin/env python3
"""
ESQET v179 — Improved Variational φ–Kuramoto
Slower φ dynamics + explicit bounding + better coupling
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

phi_target = (1 + np.sqrt(5)) / 2
N = 16
K0 = 1.8          # Base coupling
eta = 0.008       # Very slow φ adaptation

def system(state, t):
    theta = state[:N]
    phi = state[-1]
    
    # Effective coupling modulated by φ (slow)
    K_eff = K0 * (0.5 + 0.5 * np.tanh(2*(phi - phi_target)))
    
    dtheta = np.zeros(N)
    for i in range(N):
        sum_coup = 0.0
        for j in range(N):
            sum_coup += np.sin(theta[j] - theta[i])
        dtheta[i] = (K_eff / N) * sum_coup
    
    # Slow variational dynamics for φ
    R = np.abs(np.mean(np.exp(1j * theta)))
    R_target = 0.65   # Desired partial coherence regime
    
    dphi = -eta * (phi - phi_target) + 0.12 * (R - R_target)
    dphi = np.clip(dphi, -0.04, 0.04)   # Strong bounding
    
    return np.concatenate([dtheta, [dphi]])


if __name__ == "__main__":
    print("="*70)
    print("ESQET v179 — Variational φ–Kuramoto (Improved Timescales)")
    print("="*70)
    
    np.random.seed(42)
    state0 = np.zeros(N + 1)
    state0[:N] = np.random.uniform(-np.pi, np.pi, N)
    state0[-1] = 1.3
    
    t = np.linspace(0, 400, 12000)
    print("Integrating...")
    sol = odeint(system, state0, t, rtol=1e-7, atol=1e-9)
    
    theta = sol[:, :N]
    phi_traj = sol[:, -1]
    
    # Order parameter
    R_traj = np.array([np.abs(np.mean(np.exp(1j * th))) for th in theta])
    
    print(f"Final φ_eff   : {phi_traj[-1]:.6f} (target = {phi_target:.6f})")
    print(f"Final R       : {R_traj[-1]:.4f}")
    print(f"Mean R (steady): {np.mean(R_traj[-2000:]):.4f} ± {np.std(R_traj[-2000:]):.4f}")
    
    # Plot
    plt.figure(figsize=(14, 9))
    
    plt.subplot(2, 2, 1)
    plt.plot(t, phi_traj, 'gold', lw=2.5)
    plt.axhline(phi_target, color='red', ls='--')
    plt.title('φ Evolution (Slow Variational Variable)')
    plt.ylabel('φ_eff')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 2)
    plt.plot(t, R_traj, 'purple', lw=2.5)
    plt.title('Synchronization Order Parameter R(t)')
    plt.ylim(0, 1.05)
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 3)
    plt.plot(t[-3000:], theta[-3000:, 0], 'teal', lw=1.5, label='Osc 1')
    plt.plot(t[-3000:], theta[-3000:, 1], 'cyan', lw=1.5, label='Osc 2')
    plt.title('Sample Phase Evolution')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 4)
    plt.scatter(phi_traj[-3000:], R_traj[-3000:], s=3, alpha=0.6)
    plt.xlabel('φ_eff')
    plt.ylabel('R')
    plt.title('φ–R Phase Space')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('simulations/phi_variational_v179.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\nφ is now a slow emergent coordinate responding to coherence.")
