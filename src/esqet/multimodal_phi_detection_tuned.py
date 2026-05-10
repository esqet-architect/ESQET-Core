#!/usr/bin/env python3
"""
ESQET v186.1 — Tuned Multi-Modal φ Detection Pipeline
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, find_peaks
from scipy.fft import rfft, rfftfreq

# Import your modules
from multimodal_signal_sim import SignalEnvironment
# from phi_scale_detector import detect_phi_scales, detect_phi_multiscale  # if you have it

phi = (1 + np.sqrt(5)) / 2
phi_inv = (np.sqrt(5) - 1) / 2

print("="*70)
print("ESQET v186.1 — Tuned Multimodal φ Detection")
print("="*70)

# Initialize environment
env = SignalEnvironment(sample_rate=44100, duration=4.0)   # longer duration for better resolution
t = env.t

# Generate strong φ-scaled components
print("Generating φ-scaled test signal...")
composite = np.zeros_like(t)

base = 440.0  # A4 note
phi_freqs = [base * (phi ** n) for n in range(5)]
phi_inv_freqs = [base * (phi_inv ** n) for n in range(1, 4)]

for f in phi_freqs + phi_inv_freqs:
    if 20 < f < 8000:   # audible range
        sig, _, _ = env.acoustic_signal(f, amplitude=0.8, distance_m=1.0)
        composite += sig
        print(f"  Added φ-related frequency: {f:.2f} Hz")

# Add background and interference
background = env.blackbody_background(temperature_k=300)
composite += 0.3 * background

composite += env.cosmic_ray_spike(rate_per_second=8)

# Detector filtering
detected = env.detector_response(composite, bandwidth_hz=12000)

print(f"\nSignal length: {len(detected)} samples ({env.t[-1]:.1f} s)")

# ===================================================================
# φ-Scale Detection (Tuned)
# ===================================================================
def tuned_detect_phi_scales(signal, fs, tolerance=0.04, min_height=0.02):
    fft_vals = rfft(signal)
    power = np.abs(fft_vals)**2
    freqs = rfftfreq(len(signal), 1/fs)
    power /= np.max(power)
    
    peaks, props = find_peaks(power, height=min_height, distance=15, prominence=0.01)
    peak_freqs = freqs[peaks]
    peak_heights = props['peak_heights']
    
    ratios = []
    for i in range(len(peak_freqs)):
        for j in range(i+1, len(peak_freqs)):
            r = max(peak_freqs[j], peak_freqs[i]) / min(peak_freqs[j], peak_freqs[i])
            ratios.append(r)
    
    ratios = np.array(ratios)
    phi_matches = ratios[np.abs(ratios - phi) < tolerance]
    phi_inv_matches = ratios[np.abs(ratios - phi_inv) < tolerance]
    
    return peak_freqs, phi_matches, phi_inv_matches, ratios

peak_freqs, phi_matches, phi_inv_matches, all_ratios = tuned_detect_phi_scales(detected, env.fs)

print(f"\nDetected peaks: {len(peak_freqs)}")
print(f"φ matches     : {len(phi_matches)}")
print(f"φ⁻¹ matches   : {len(phi_inv_matches)}")

# ===================================================================
# Plotting
# ===================================================================
fig, axs = plt.subplots(2, 3, figsize=(15, 10))

axs[0,0].plot(t[:8000], detected[:8000], color='gold', lw=0.8)
axs[0,0].set_title('Detected Signal')
axs[0,0].set_xlabel('Time (s)')
axs[0,0].grid(True, alpha=0.3)

# Power spectrum with φ markers
freqs = rfftfreq(len(detected), 1/env.fs)
power = np.abs(rfft(detected))**2
axs[0,1].semilogy(freqs[:5000], power[:5000], color='purple', lw=0.8)
for f in list(peak_freqs)[:30]:
    if f < freqs[5000]:
        axs[0,1].axvline(f, color='red', ls='--', alpha=0.4, lw=0.8)
axs[0,1].set_title('Power Spectrum (φ peaks marked)')
axs[0,1].set_xlabel('Frequency (Hz)')
axs[0,1].grid(True, alpha=0.3)

# Ratio histogram
axs[0,2].hist(all_ratios, bins=60, color='teal', alpha=0.7, edgecolor='black')
axs[0,2].axvline(phi, color='red', ls='--', label=f'φ = {phi:.4f}')
axs[0,2].axvline(phi_inv, color='orange', ls='--', label=f'φ⁻¹ = {phi_inv:.4f}')
axs[0,2].set_title('Frequency Ratio Distribution')
axs[0,2].legend()
axs[0,2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/multimodal_phi_detection_tuned.png', dpi=300, bbox_inches='tight')
plt.show()

print("\nTuned φ detection complete.")
print(f"φ persistence in spectrum: {len(phi_matches) + len(phi_inv_matches)} matches found.")
