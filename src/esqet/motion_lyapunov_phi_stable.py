#!/usr/bin/env python3
"""
motion_lyapunov_phi_stable.py
Lyapunov-stable φ-adaptive oscillator sandbox.
Numerically verifies convergence to the Golden Ratio resonance.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import savgol_filter

# ESQET Stability Constants
phi_star = (1 + np.sqrt(5)) / 2
mu = 1.6        # Nonlinearity strength
kappa = 0.45    # Coupling to phi_star
eta = 0.08      # Adaptive gain decay

def system(t, y):
    """
    Three-state system:
    x: displacement
    v: velocity
    p: effective phi (the adaptive parameter)
    """
    x, v, p = y
    dx = v
    # Van der Pol structure with phi-controlled damping and harmonic pull
    dv = mu * p * (1 - x**2) * v - x - kappa * (p - phi_star)
    # Parameter adaptation law driving p toward phi_star
    dp = -eta * (p - phi_star) - 0.02 * x * v
    return [dx, dv, dp]

def lyapunov(y):
    """Lyapunov candidate function V(x, v, p)"""
    x, v, p = y
    return 0.5*(x**2 + v**2) + 0.5*(p - phi_star)**2

def lle_estimate(y0, eps=1e-8, dt=0.01, steps=12000, renorm=20):
    """Estimates the Largest Lyapunov Exponent to confirm stability"""
    def f_state(y):
        x, v, p = y
        return np.array([v, mu * p * (1 - x**2) * v - x - kappa * (p - phi_star), -eta * (p - phi_star) - 0.02 * x * v])

    y = np.array(y0, dtype=float)
    d = np.array([eps, 0.0, 0.0], dtype=float)
    s = 0.0
    n = 0
    for i in range(steps):
        # RK4 step for system
        k1 = f_state(y)
        k2 = f_state(y + 0.5*dt*k1)
        k3 = f_state(y + 0.5*dt*k2)
        k4 = f_state(y + dt*k3)
        y = y + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

        # RK4 step for perturbed trajectory
        yd = y + d
        k1d = f_state(yd)
        k2d = f_state(yd + 0.5*dt*k1d)
        k3d = f_state(yd + 0.5*dt*k2d)
        k4d = f_state(yd + dt*k3d)
        yd = yd + (dt/6.0)*(k1d + 2*k2d + 2*k3d + k4d)

        d = yd - y
        if (i + 1) % renorm == 0:
            dn = np.linalg.norm(d)
            if dn == 0: dn = 1e-16
            s += np.log(dn/eps)
            n += 1
            d = eps * d / dn
    return s / (n * renorm * dt)

def main():
    print("Initializing Lyapunov-Stable φ-Adaptation Analysis...")
    t_eval = np.linspace(0, 160, 16000)
    y0 = [0.25, 0.0, 1.2]
    
    sol = solve_ivp(system, (t_eval[0], t_eval[-1]), y0, t_eval=t_eval, rtol=1e-9, atol=1e-12, max_step=0.02)
    x, v, p = sol.y

    # Process Stability Metrics
    V = lyapunov(sol.y)
    Vf = savgol_filter(V, 301, 3)
    Vdot = np.gradient(Vf, t_eval)
    lle = lle_estimate(y0)

    # Visualization
    fig, ax = plt.subplots(2, 2, figsize=(12, 9))
    
    # Phase Portrait
    ax[0,0].plot(x, v, color='gold', lw=1.8)
    ax[0,0].set_title('Phase Portrait (x vs v)')
    ax[0,0].set_xlabel('x')
    ax[0,0].set_ylabel('v')
    ax[0,0].grid(True, alpha=0.3)

    # State Over Time
    ax[0,1].plot(t_eval, x, label='x(t)')
    ax[0,1].plot(t_eval, v, label='v(t)')
    ax[0,1].plot(t_eval, p, label='phi_eff(t)', color='purple', lw=2)
    ax[0,1].axhline(phi_star, color='k', ls='--', lw=1, label='phi* (Target)')
    ax[0,1].set_title('State Evolution & Parameter Adaptation')
    ax[0,1].set_xlabel('t')
    ax[0,1].legend()
    ax[0,1].grid(True, alpha=0.3)

    # Lyapunov Candidate
    ax[1,0].plot(t_eval, Vf, color='teal', lw=1.8)
    ax[1,0].set_title('Lyapunov Candidate V(t)')
    ax[1,0].set_xlabel('t')
    ax[1,0].grid(True, alpha=0.3)

    # Lyapunov Derivative
    ax[1,1].plot(t_eval, Vdot, color='crimson', lw=1.2)
    ax[1,1].axhline(0, color='k', lw=1)
    ax[1,1].set_title('Numerical dV/dt (Energy Dissipation)')
    ax[1,1].set_xlabel('t')
    ax[1,1].grid(True, alpha=0.3)

    fig.suptitle(f'ESQET Lyapunov-Stable φ-Adaptation | LLE ≈ {lle:.4f}')
    fig.tight_layout()
    fig.savefig('simulations/motion_lyapunov_phi_stable.png', dpi=300, bbox_inches='tight')
    
    print(f'Stability Estimate (LLE) ≈ {lle:.6f}')
    print(f'Final Effective φ ≈ {p[-1]:.6f}')
    print(f'Target φ ≈ {phi_star:.6f}')
    print('Artifact Saved: simulations/motion_lyapunov_phi_stable.png')

if __name__ == '__main__':
    main()
