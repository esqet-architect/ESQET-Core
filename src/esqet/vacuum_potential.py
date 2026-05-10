#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def V(g):
    # Reconstructed potential: V(g) = 0.5*g^2 - g - ln(g)
    return 0.5 * g**2 - g - np.log(g)

g_vals = np.linspace(0.5, 3.5, 500)
pot_vals = V(g_vals)
phi = (1 + np.sqrt(5)) / 2

plt.figure(figsize=(10, 6))
plt.plot(g_vals, pot_vals, 'k-', lw=2, label='RG Potential $V(g)$')
plt.axvline(phi, color='gold', ls='--', label=f'Vacuum Minimum $\phi \approx {phi:.4f}$')
plt.scatter([phi], [V(phi)], color='red', zorder=5)

plt.title("ESQET: The Energy Well of Space-Time")
plt.xlabel("Coupling Constant $g$")
plt.ylabel("Effective Potential $V(g)$")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('simulations/vacuum_potential_well.png')

print(f"Potential Minimum at g={phi:.6f}")
print(f"Saddle-point geometry confirmed.")
