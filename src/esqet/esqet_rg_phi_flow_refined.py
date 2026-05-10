#!/usr/bin/env python3
"""
ESQET v187.1 — Refined Renormalization Flow Experiment
Tests whether φ-like scaling emerges or stabilizes under coarse-graining.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, welch

phi_target = (1 + np.sqrt(5)) / 2

class SignalEnvironment:
    def __init__(self, fs=44100, duration=8.0):
        self.fs = fs
        self.t = np.arange(0, duration, 1/fs)
    
    def generate_background(self):
        """Pink + thermal + sparse spikes"""
        pink = np.cumsum(np.random.randn(len(self.t))) * 0.015
        thermal = 0.08 * np.random.randn(len(self.t))
        spikes = np.zeros_like(self.t)
        spike_idx = np.random.randint(0, len(self.t), int(0.008*len(self.t)))
        spikes[spike_idx] = np.random.uniform(4, 15, len(spike_idx))
        return pink + thermal + spikes


def coarse_grain(signal, fs, factor=2):
    """Proper low-pass + decimation"""
    nyq = fs / 2
    cutoff = nyq / factor
    b, a = butter(6, cutoff/nyq, btype='low')
    filtered = filtfilt(b, a, signal)
    downsampled = filtered[::factor]
    return downsampled / np.std(downsampled), fs / factor


def extract_scale_ratio(signal):
    """Robust ratio extraction from dominant frequencies"""
    f, Pxx = welch(signal, fs=44100, nperseg=min(4096, len(signal)))
    peaks, _ = find_peaks(Pxx, height=np.max(Pxx)*0.1, distance=5)
    if len(peaks) < 2:
        return 1.0
    freqs = f[peaks]
    ratios = []
    for i in range(len(freqs)):
        for j in range(i+1, len(freqs)):
            ratios.append(max(freqs[j], freqs[i]) / min(freqs[j], freqs[i]))
    ratios = np.array(ratios)
    # Closest to golden ratio
    idx = np.argmin(np.abs(ratios - phi_target))
    return ratios[idx]


# ====================== RG Flow Experiment ======================
print("="*70)
print("ESQET RG Flow Experiment — φ Scale Invariance Test")
print("="*70)

env = SignalEnvironment(fs=44100, duration=8.0)
signal = env.generate_background()
signal /= np.std(signal)

scales = []
phi_flow = []
current_signal = signal
current_fs = env.fs

for level in range(9):
    ratio = extract_scale_ratio(current_signal)
    scales.append(current_fs)
    phi_flow.append(ratio)
    
    print(f"Scale {2**level:3d} (fs={current_fs:.0f} Hz) → effective ratio = {ratio:.4f}")
    
    current_signal, current_fs = coarse_grain(current_signal, current_fs)

# Plot
plt.figure(figsize=(10, 6))
plt.semilogx(scales, phi_flow, 'o-', color='gold', linewidth=2, markersize=6)
plt.axhline(phi_target, color='red', linestyle='--', label=f'Golden φ = {phi_target:.5f}')
plt.axhline(1.0, color='gray', linestyle=':', label='No scaling')
plt.title('Renormalization Flow: Effective Ratio vs Scale')
plt.xlabel('Sampling Rate (Hz) — decreasing scale →')
plt.ylabel('Dominant Frequency Ratio')
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig('simulations/esqet_rg_phi_flow_refined.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nRG Flow experiment complete.")
print("If the curve stabilizes near φ as scale decreases, you have evidence of an attractor.")
