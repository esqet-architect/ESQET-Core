#!/usr/bin/env python3
"""
ESQET v188 — Direct β-Function Measurement
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from multimodal_signal_sim import SignalEnvironment

phi_target = (1 + np.sqrt(5)) / 2


# --------------------------------------------------
# Observable: emergent φ
# --------------------------------------------------
def compute_phi(signal):

    x = signal[:-1]
    y = signal[1:]

    cov = np.cov(x, y)
    eig = np.linalg.eigvalsh(cov)
    eig = np.sort(eig)[::-1]

    if eig[1] > 1e-12:
        return eig[0] / eig[1]
    return 1.0


# --------------------------------------------------
# RG transformation
# --------------------------------------------------
def coarse_grain(signal, fs):

    nyq = fs / 2
    cutoff = nyq / 2

    b, a = butter(4, cutoff / nyq, btype='low')
    filtered = filtfilt(b, a, signal)

    down = filtered[::2]
    down /= np.std(down)

    return down, fs // 2


# --------------------------------------------------
# Initial physical environment
# (no φ injected)
# --------------------------------------------------
print("="*70)
print("ESQET v188 — β-Function Measurement")
print("="*70)

env = SignalEnvironment(sample_rate=44100, duration=6.0)

signal = (
    env.blackbody_background(300)
    + env.cosmic_ray_spike(rate_per_second=5)
)

signal /= np.std(signal)
fs = env.fs


# --------------------------------------------------
# RG Flow Sampling
# --------------------------------------------------
scales = []
phi_vals = []

for step in range(10):

    phi_val = compute_phi(signal)

    print(f"Scale {2**step:4d} | φ = {phi_val:.5f}")

    scales.append(2**step)
    phi_vals.append(phi_val)

    signal, fs = coarse_grain(signal, fs)


scales = np.array(scales)
phi_vals = np.array(phi_vals)


# --------------------------------------------------
# β-function
# β = dφ / d ln(b)
# --------------------------------------------------
ln_scale = np.log(scales)

beta = np.gradient(phi_vals, ln_scale)


# --------------------------------------------------
# Fixed point detection
# --------------------------------------------------
fixed_points = []

for i in range(len(beta)-1):
    if beta[i] == 0 or beta[i]*beta[i+1] < 0:
        fixed_points.append(phi_vals[i])

print("\nDetected RG Fixed Points:")
if fixed_points:
    for fp in fixed_points:
        print(f"  φ* ≈ {fp:.5f}")
else:
    print("  None detected")


# --------------------------------------------------
# Plot RG Flow
# --------------------------------------------------
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(scales, phi_vals, 'o-', label='φ(scale)')
plt.axhline(phi_target, linestyle='--', label='Golden Ratio')
plt.xscale('log', base=2)
plt.xlabel('Scale')
plt.ylabel('φ')
plt.title('RG Flow')
plt.grid(True, alpha=0.3)
plt.legend()

plt.subplot(1,2,2)
plt.plot(phi_vals, beta, 'o-', label='β(φ)')
plt.axhline(0, linestyle='--')
plt.xlabel('φ')
plt.ylabel('β(φ)')
plt.title('β-Function')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("simulations/esqet_beta_function.png", dpi=300)

print("\n✓ β-function computed.")
print("Artifact: simulations/esqet_beta_function.png")
