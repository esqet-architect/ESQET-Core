#!/usr/bin/env python3
"""
ESQET φ-Scale Detector Module
Detects golden ratio ratios in spectral peaks of any signal.
"""

import numpy as np
from scipy.signal import find_peaks, welch
from scipy.fft import rfft, rfftfreq

phi = (1 + np.sqrt(5)) / 2
phi_inv = (np.sqrt(5) - 1) / 2

def detect_phi_scales(signal, fs, tolerance=0.05, min_peak_height=0.05):
    """
    Detect φ-scale ratios in signal spectrum.
    
    Parameters:
    - signal: input time series
    - fs: sampling frequency (Hz)
    - tolerance: allowed deviation from φ (e.g., 0.05 means 1.618 ± 5%)
    - min_peak_height: minimum relative peak height
    
    Returns:
    - peak_freqs: list of detected peak frequencies
    - phi_matches: list of frequency ratios that match φ
    - phi_ratios: all measured ratios
    """
    
    # Compute power spectrum
    fft_vals = rfft(signal)
    power = np.abs(fft_vals)**2
    freqs = rfftfreq(len(signal), 1/fs)
    
    # Normalize
    power /= np.max(power)
    
    # Find dominant peaks
    peaks, properties = find_peaks(power, height=min_peak_height, distance=10)
    peak_freqs = freqs[peaks]
    peak_heights = properties['peak_heights']
    
    if len(peak_freqs) < 2:
        return peak_freqs, [], []
    
    # Compute all pairwise ratios
    phi_ratios = []
    ratio_pairs = []
    
    for i in range(len(peak_freqs)):
        for j in range(i+1, len(peak_freqs)):
            # Ensure ratio > 1
            if peak_freqs[j] > peak_freqs[i]:
                r = peak_freqs[j] / peak_freqs[i]
            else:
                r = peak_freqs[i] / peak_freqs[j]
            
            phi_ratios.append(r)
            ratio_pairs.append((i, j, r))
    
    phi_ratios = np.array(phi_ratios)
    
    # Find matches to φ
    phi_error = np.abs(phi_ratios - phi)
    phi_inv_error = np.abs(phi_ratios - phi_inv)
    
    matches = []
    match_ratios = []
    
    for idx, (r, err, err_inv) in enumerate(zip(phi_ratios, phi_error, phi_inv_error)):
        if err < tolerance:
            matches.append((r, 'φ', err))
            match_ratios.append(r)
        elif err_inv < tolerance:
            matches.append((r, 'φ⁻¹', err_inv))
            match_ratios.append(r)
    
    return peak_freqs, match_ratios, phi_ratios


def detect_phi_multiscale(signal, fs, scales=[1, 2, 3, 5, 8, 13], tolerance=0.05):
    """
    Multi-scale φ detection: downsample signal and check persistence.
    
    Returns:
    - persistence: fraction of scales where φ appears
    - scale_peaks: list of peaks at each scale
    """
    scale_ratios = []
    original_len = len(signal)
    
    for scale in scales:
        if scale > 1:
            # Downsample
            downsampled = signal[::scale]
            fs_down = fs / scale
        else:
            downsampled = signal
            fs_down = fs
        
        _, ratios, _ = detect_phi_scales(downsampled, fs_down, tolerance=tolerance)
        scale_ratios.extend(ratios)
    
    # Count unique ratio detections
    unique_ratios = np.unique(np.round(scale_ratios, 3))
    phi_count = sum(1 for r in unique_ratios if abs(r - phi) < tolerance or abs(r - phi_inv) < tolerance)
    
    persistence = phi_count / (len(unique_ratios) + 1e-6)
    
    return persistence, scale_ratios


if __name__ == "__main__":
    print("φ-scale detector module loaded.")
    print(f"Target φ = {phi:.6f}")
    print(f"Target φ⁻¹ = {phi_inv:.6f}")
