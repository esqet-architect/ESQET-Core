#!/usr/bin/env python3
"""
ESQET Motion Observer v170.3
Proper nonlinear observer + coupled oscillators + noise
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

phi = (1 + np.sqrt(5)) / 2
print(f"φ = {phi:.8f} (nonlinear gain parameter)\n")

def esqet_system(state, t, mu=1.0, k_obs=1.2, coupling=0.0, noise_level=0.0):
    """True system + observer dynamics"""
    x, v, x_hat = state
    
    # True Van der Pol dynamics (φ-scaled)
    dx = v
    dv = mu * phi * (1 - x**2) * v - x + coupling * (x_hat - x)
    
    # Proper observer dynamics (Luenberger-style)
    dx_hat = mu * phi * (1 - x_hat**2) * (x_hat) - x_hat + k_obs * (x - x_hat)
    
    # Measurement noise
    d_noise = noise_level * np.random.randn()
    
    return [dx, dv, dx_hat + d_noise]


# Simulation
t = np.linspace(0, 120, 6000)
state0 = [0.1, 0.0, 0.0]

sol = odeint(esqet_system, state0, t, args=(1.0, 1.5, 0.0, 0.015))

x, v, x_hat = sol[:,0], sol[:,1], sol[:,2]

# Plot
plt.figure(figsize=(14, 10))

plt.subplot(2, 2, 1)
plt.plot(x, v, 'gold', lw=2, label='True Phase Trajectory')
plt.plot(x_hat, sol[:,1], 'cyan', lw=1.5, alpha=0.7, label='Observer Trajectory')
plt.title('Phase Space: φ-Van der Pol Limit Cycle')
plt.xlabel('Displacement x')
plt.ylabel('Velocity v')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 2)
plt.plot(t, x, 'teal', lw=2, label='True x(t)')
plt.plot(t, x_hat, 'orange', lw=1.8, label='Observer x̂(t)')
plt.title('Time Evolution + Observer Tracking')
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(2, 2, 3)
plt.plot(t, x - x_hat, 'red', lw=1.5)
plt.title('Observer Error')
plt.xlabel('Time')
plt.ylabel('x - x̂')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/esqet_observer_phi_vdp.png', dpi=300, bbox_inches='tight')
plt.show()

print("Simulation complete.")
print("Features active: Proper observer dynamics, noise, φ-scaled nonlinearity")
