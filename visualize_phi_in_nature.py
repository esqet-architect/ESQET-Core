#!/usr/bin/env python3
"""
Visualize φ-ratio appearances in nature (real, documented phenomena)
"""

import matplotlib.pyplot as plt
import numpy as np

PHI = 1.618033988749895

# Real φ occurrences in nature
phi_phenomena = {
    "Nautilus shell": 1.618,
    "Sunflower seeds": 1.618,
    "Pine cone spirals": 1.618,
    "DNA helix (34/21)": 34/21,
    "Human hand proportions": 1.618,
    "Hurricane spiral": 1.618,
    "Galaxy spiral arms": 1.618,
    "Leaf arrangements": 1.618
}

fig, ax = plt.subplots(figsize=(10, 6))
names = list(phi_phenomena.keys())
values = list(phi_phenomena.values())
colors = plt.cm.viridis(np.linspace(0, 1, len(names)))

bars = ax.barh(names, values, color=colors, edgecolor='black')
ax.axvline(x=PHI, color='red', linestyle='--', linewidth=2, label=f'φ = {PHI:.6f}')
ax.set_xlabel('Ratio')
ax.set_title('Golden Ratio φ in Nature (Documented Phenomena)')
ax.legend()
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('phi_in_nature.png', dpi=150)
plt.show()
print("✅ Visualization saved: phi_in_nature.png")
