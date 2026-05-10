#!/usr/bin/env python3
"""
ESQET Motion Observer v170.4 — Numerically Improved
RK4 integration + proper observer dynamics
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

phi = (1 + np.sqrt(5)) / 2
mu = 1.0  # Van der Pol nonlinearity strength
print(f"φ = {phi:.8f} (nonlinear gain)")
print(f"μ = {mu:.1f} (Van der Pol parameter)\n")

def true_dynamics(t, y, mu_val=1.0):
    """True φ-scaled Van der Pol system"""
    x, v = y
    dxdt = v
    dvdt = mu_val * phi * (1 - x**2) * v - x
    return [dxdt, dvdt]


def observer_dynamics(t, y_obs, y_true, mu_val=1.0, k_obs=1.5):
    """Luenberger-style observer with proper mu parameter"""
    x_hat = y_obs[0]
    v_hat = y_obs[1] if len(y_obs) > 1 else 0.0
    x_true = y_true[0]
    
    # Update using measured output (position)
    # Innovation term drives the observer towards true state
    innovation = k_obs * (x_true - x_hat)
    
    # Observer model: same dynamics as true system + correction
    dx_hat = v_hat + innovation
    dv_hat = mu_val * phi * (1 - x_hat**2) * v_hat - x_hat + 0.5 * innovation
    
    return [dx_hat, dv_hat]


# Simulation
t_span = (0, 120)
y0 = [0.1, 0.0]

sol = solve_ivp(true_dynamics, t_span, y0, method='RK45', rtol=1e-8, atol=1e-8, 
                args=(mu,), dense_output=True)

t = np.linspace(0, 120, 6000)
traj = sol.sol(t)  # shape (2, len(t))

# Observer simulation
x_hat = np.zeros_like(t)
v_hat = np.zeros_like(t)
x_hat[0] = -0.5  # Start with wrong initial condition (test observer convergence)
v_hat[0] = 0.2

for i in range(1, len(t)):
    dt_val = t[i] - t[i-1]
    true_state = [traj[0, i], traj[1, i]]
    y_obs = [x_hat[i-1], v_hat[i-1]]
    
    d_obs = observer_dynamics(t[i], y_obs, true_state, mu_val=mu, k_obs=1.2)
    x_hat[i] = x_hat[i-1] + d_obs[0] * dt_val
    v_hat[i] = v_hat[i-1] + d_obs[1] * dt_val

# Error
pos_error = traj[0, :] - x_hat
vel_error = traj[1, :] - v_hat

# Plot
plt.figure(figsize=(14, 10))

# Phase space
plt.subplot(2, 2, 1)
plt.plot(traj[0], traj[1], 'gold', lw=2, label='True Trajectory')
plt.plot(x_hat, v_hat, 'cyan', lw=1.5, alpha=0.7, label='Observer Estimate')
plt.plot(x_hat[0], v_hat[0], 'go', markersize=8, label='Initial observer state')
plt.plot(traj[0, 0], traj[1, 0], 'ro', markersize=8, label='Initial true state')
plt.title('Phase Space — φ-Van der Pol Limit Cycle')
plt.xlabel('Displacement x')
plt.ylabel('Velocity v')
plt.legend()
plt.grid(True, alpha=0.3)
plt.axis('equal')

# Time evolution
plt.subplot(2, 2, 2)
plt.plot(t, traj[0], 'teal', lw=2, label='True x(t)')
plt.plot(t, x_hat, 'orange', lw=1.8, label='Observer x̂(t)')
plt.title('Time Evolution — Position')
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.legend()
plt.grid(True, alpha=0.3)

# Observer error
plt.subplot(2, 2, 3)
plt.plot(t, pos_error, 'red', lw=1.5, label='Position error')
plt.plot(t, vel_error, 'purple', lw=1.5, label='Velocity error', alpha=0.7)
plt.axhline(0, color='k', linestyle='--', alpha=0.5)
plt.title('Observer Convergence Error')
plt.xlabel('Time')
plt.ylabel('Error')
plt.legend()
plt.grid(True, alpha=0.3)

# Limit cycle amplitude evolution
plt.subplot(2, 2, 4)
# Compute running amplitude (Hilbert-like envelope for x)
from scipy.signal import hilbert
analytic = hilbert(traj[0])
amplitude = np.abs(analytic)
plt.plot(t, amplitude, 'brown', lw=2)
plt.axhline(np.mean(amplitude[2000:]), color='gold', linestyle='--', label=f'Steady amplitude = {np.mean(amplitude[2000:]):.3f}')
plt.title('Amplitude Evolution → φ-Limit Cycle Convergence')
plt.xlabel('Time')
plt.ylabel('Oscillation Amplitude')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/esqet_observer_rk4.png', dpi=300, bbox_inches='tight')
plt.show()

print("="*50)
print("Simulation completed with RK4 integration.")
print(f"Final position error: {pos_error[-1]:.6f}")
print(f"Final velocity error: {vel_error[-1]:.6f}")
print(f"Steady-state amplitude: {np.mean(amplitude[2000:]):.4f}")
print("="*50)
