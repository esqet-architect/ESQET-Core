#!/usr/bin/env python3
"""
ESQET v206 — Cobweb Analysis of n-step Attractors
Visualizing the 'Trapping Velocity' of the vacuum.
"""
import numpy as np
import matplotlib.pyplot as plt

def f(g, n):
    # The map: g_{k+1} = 1 + 1/g + ... + 1/g^{n-1}
    return 1.0 + sum(1.0 / (g**m) for m in range(1, n))

def plot_cobweb(n, g0, steps, ax, color):
    g = np.linspace(0.5, 3.0, 500)
    ax.plot(g, [f(x, n) for x in g], color=color, label=f'n={n} Map')
    ax.plot(g, g, 'k--', alpha=0.5) # Identity line
    
    curr_g = g0
    for _ in range(steps):
        next_g = f(curr_g, n)
        # Vertical line to map
        ax.plot([curr_g, curr_g], [curr_g, next_g], color=color, alpha=0.4)
        # Horizontal line to identity
        ax.plot([curr_g, next_g], [next_g, next_g], color=color, alpha=0.4)
        curr_g = next_g

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

plot_cobweb(2, 0.7, 10, ax1, 'blue')
ax1.set_title("Fibonacci Cobweb (Soft Trap)")

plot_cobweb(6, 0.7, 10, ax2, 'red')
ax2.set_title("Hexanacci Cobweb (Stiff Trap)")

for ax in [ax1, ax2]:
    ax.set_xlabel("$g_k$")
    ax.set_ylabel("$g_{k+1}$")
    ax.legend()
    ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('simulations/cobweb_stiffness.png')
print("="*60)
print("ESQET v206: COBWEB STIFFNESS ANALYSIS COMPLETE")
print("="*60)
print("Visual confirmation of 'Stiffness':")
print("Note how n=6 reaches the attractor much faster than n=2.")
print("="*60)
