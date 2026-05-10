#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import h, c, e, k

# ESQET v2.3 CONSTANTS
phi = (1 + np.sqrt(5)) / 2
m_axion_eV = (2.2 / 1000) * (phi**-18)
f_axion_GHz = (m_axion_eV * e / h) / 1e9

print("="*60)
print("ESQET AXION HALOSCOPE SIMULATOR (CALIBRATED)")
print("="*60)
print(f"φ (golden ratio)      = {phi:.15f}")
print(f"m_a (predicted)       = {m_axion_eV*1e6:.4f} μeV")
print(f"f_a (predicted)       = {f_axion_GHz:.4f} GHz")
print("="*60)

# Cavity Simulation Plotting Logic
scan_freqs = np.linspace(f_axion_GHz - 0.01, f_axion_GHz + 0.01, 1000)
response = 1 / (1 + ((scan_freqs - f_axion_GHz) / (f_axion_GHz / 50000))**2)

plt.figure(figsize=(10, 6))
plt.plot(scan_freqs, response, 'b-', label='Axion Resonance')
plt.axvline(f_axion_GHz, color='r', linestyle='--', label=f'ESQET Target: {f_axion_GHz:.3f} GHz')
plt.title('ESQET v2.3: Predicted Axion Signal Profile')
plt.xlabel('Frequency (GHz)')
plt.ylabel('Normalized Response')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('esqet_haloscope_calibrated.png')
print("✓ Calibrated plot saved: esqet_haloscope_calibrated.png")
