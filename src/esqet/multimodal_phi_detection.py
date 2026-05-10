#!/usr/bin/env python3
"""
ESQET v186 — Multi-Modal Signal with φ Detection
Complete pipeline:
1. Generate realistic multi-modal signal (EM + acoustic + background)
2. Apply detector response
3. Detect φ-scale ratios in spectrum
4. Multi-scale persistence test
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, welch
from scipy.fft import rfft, rfftfreq

# Import modules
from multimodal_signal_sim import SignalEnvironment
from phi_scale_detector import detect_phi_scales, detect_phi_multiscale

phi = (1 + np.sqrt(5)) / 2
phi_inv = (np.sqrt(5) - 1) / 2

print("="*70)
print("ESQET v186 — Multi-Modal Signal with φ Detection")
print("="*70)
print("Pipeline: Signal Generation → Detection → φ-Scale Analysis")
print("="*70)

# Initialize environment
env = SignalEnvironment(sample_rate=50000, duration=2.0)  # 2 seconds for better frequency resolution
t = env.t

# Generate composite signal with multiple φ-related frequencies
print("\nGenerating composite signal...")

# φ-scaled frequency family
base_freq = 261.63  # C4 note
phi_freqs = [base_freq * (phi ** n) for n in range(4)]  # φ⁰, φ¹, φ², φ³
phi_inv_freqs = [base_freq * (phi_inv ** n) for n in range(1, 4)]

composite = np.zeros_like(t)

# Add φ-scaled acoustic signals
for f in phi_freqs + phi_inv_freqs:
    if f < 2000:  # Keep in audible range
        sig, _, _ = env.acoustic_signal(f, amplitude=0.3, distance_m=2)
        composite += sig
        print(f"  Added φ-scaled frequency: {f:.2f} Hz")

# Add EM interference (power line harmonics)
for f in [50, 60, 120, 180, 240]:
    sig, _, _ = env.electromagnetic_signal(f, amplitude=0.1, distance_m=10)
    composite += sig

# Add background radiation
background = env.blackbody_background(temperature_k=300)
composite += background * 0.5

# Add cosmic ray spikes
composite += env.cosmic_ray_spike(rate_per_second=5)

# Apply detector response (audio range)
detected = env.detector_response(composite, bandwidth_hz=5000)

print(f"\nComposite signal: {len(composite)} samples, {env.t[-1]:.2f}s duration")

# ============================================================
# φ-Scale Detection
# ============================================================
print("\n" + "="*70)
print("φ-SCALE DETECTION")
print("="*70)

# Single-scale detection
peaks, phi_matches, all_ratios = detect_phi_scales(detected, env.fs, tolerance=0.05)

print(f"\nDetected spectral peaks: {len(peaks)}")
if len(peaks) > 0:
    print(f"Peak frequencies (Hz): {[f'{p:.1f}' for p in peaks[:10]]}{'...' if len(peaks) > 10 else ''}")
print(f"φ-ratio matches found: {len(phi_matches)}")
if len(phi_matches) > 0:
    print(f"Matched ratios: {[f'{r:.4f}' for r in phi_matches[:5]]}")

# Multi-scale persistence test
print("\n" + "="*70)
print("MULTI-SCALE PERSISTENCE TEST")
print("="*70)

scales = [1, 2, 3, 5, 8, 13]
persistence, scale_ratios = detect_phi_multiscale(detected, env.fs, scales=scales, tolerance=0.08)

print(f"Scales tested: {scales}")
print(f"φ persistence: {persistence*100:.1f}%")
if persistence > 0.5:
    print("✓ φ-scale structure persists across resolutions — likely real")
else:
    print("○ φ-scale detection weak — may be noise")

# ============================================================
# Plotting
# ============================================================
fig, axs = plt.subplots(2, 3, figsize=(15, 10))

# Plot 1: Detected signal (time domain)
axs[0, 0].plot(t[:5000], detected[:5000], color='gold', linewidth=0.8, alpha=0.7)
axs[0, 0].set_title('Detected Signal (after filtering)')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Amplitude')
axs[0, 0].grid(True, alpha=0.3)

# Plot 2: Power spectrum with φ markers
freqs = rfftfreq(len(detected), 1/env.fs)
power = np.abs(rfft(detected))**2 / len(detected)
power_db = 10 * np.log10(power + 1e-10)

axs[0, 1].semilogy(freqs[:2000], power[:2000], color='purple', linewidth=0.8)
for f in phi_freqs + phi_inv_freqs:
    if f < 2000:
        axs[0, 1].axvline(f, color='red', linestyle='--', alpha=0.5, linewidth=0.8)
axs[0, 1].set_xlim(0, 2000)
axs[0, 1].set_title('Power Spectrum (φ-scaled frequencies marked)')
axs[0, 1].set_xlabel('Frequency (Hz)')
axs[0, 1].set_ylabel('Power')
axs[0, 1].grid(True, alpha=0.3)

# Plot 3: Ratio histogram with φ markers
if len(all_ratios) > 0:
    axs[0, 2].hist(all_ratios, bins=30, color='teal', alpha=0.7, edgecolor='black')
    axs[0, 2].axvline(phi, color='red', linestyle='--', label=f'φ = {phi:.4f}')
    axs[0, 2].axvline(phi_inv, color='orange', linestyle='--', label=f'φ⁻¹ = {phi_inv:.4f}')
    axs[0, 2].set_title('Frequency Ratio Distribution')
    axs[0, 2].set_xlabel('Ratio')
    axs[0, 2].set_ylabel('Count')
    axs[0, 2].legend()
    axs[0, 2].grid(True, alpha=0.3)
else:
    axs[0, 2].text(0.5, 0.5, 'Not enough peaks for ratio analysis', ha='center', va='center')
    axs[0, 2].set_title('Frequency Ratio Distribution')

# Plot 4: Detected peaks on spectrum
axs[1, 0].semilogy(freqs[:2000], power[:2000], color='gray', alpha=0.5)
if len(peaks) > 0:
    peak_powers = power[np.array([np.argmin(np.abs(freqs - p)) for p in peaks if p < 2000])]
    peak_freqs_plot = [p for p in peaks if p < 2000]
    axs[1, 0].scatter(peak_freqs_plot, peak_powers, color='red', s=30, zorder=5)
axs[1, 0].set_xlim(0, 2000)
axs[1, 0].set_title(f'Detected Peaks (N={len(peaks)})')
axs[1, 0].set_xlabel('Frequency (Hz)')
axs[1, 0].set_ylabel('Power')
axs[1, 0].grid(True, alpha=0.3)

# Plot 5: Multi-scale persistence
axs[1, 1].bar(['φ persistence', 'other'], [persistence, 1-persistence], color=['gold', 'gray'], alpha=0.7)
axs[1, 1].set_ylim(0, 1)
axs[1, 1].set_title('Multi-Scale φ Persistence')
axs[1, 1].set_ylabel('Fraction of scales')
axs[1, 1].grid(True, alpha=0.3)

# Plot 6: Golden ratio family
scales_plot = ['φ (1.618)', 'φ⁻¹ (0.618)', 'φ² (2.618)', 'φ⁻² (0.382)']
values = [phi, phi_inv, phi**2, phi_inv**2]
colors_val = ['gold', 'orange', 'lightblue', 'lightblue']
axs[1, 2].bar(scales_plot, values, color=colors_val, alpha=0.7)
axs[1, 2].set_ylabel('Scale Factor')
axs[1, 2].set_title('Golden Ratio Family')
axs[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/multimodal_phi_detection.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print(f"φ detection status: {'✓ φ detected in spectrum' if len(phi_matches) > 0 else '○ φ not detected'}")
print(f"Multi-scale persistence: {persistence*100:.1f}%")
print("\nThis framework now properly detects φ-scale ratios in realistic")
print("signals with background noise, filtering, and cosmic ray spikes.")
print("="*70)
