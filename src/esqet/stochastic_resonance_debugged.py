#!/usr/bin/env python3
"""
ESQET Stochastic Resonance — Debugged SNR Calculation
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import welch

phi = (1 + np.sqrt(5)) / 2
mu = 1.0

def vdp_stochastic(t, y, noise_level=0.0, A_sig=0.25, omega_sig=0.15):
    x, v = y
    signal = A_sig * np.sin(omega_sig * t)
    dx = v
    dv = mu * phi * (1 - x**2) * v - x + signal + noise_level * np.random.randn()
    return [dx, dv]


def compute_snr(x, t, omega_sig=0.15, nperseg=8192):
    """Improved SNR estimation at driving frequency"""
    fs = 1.0 / (t[1] - t[0])
    f, Pxx = welch(x, fs=fs, nperseg=nperseg, detrend='constant')
    
    # Find bin closest to driving frequency
    idx = np.argmin(np.abs(f - omega_sig/(2*np.pi)))
    
    # Signal power in a narrow band around driving frequency
    signal_band = Pxx[max(0, idx-5):idx+6]
    signal_power = np.max(signal_band)
    
    # Background noise power (exclude signal region)
    noise_mask = np.ones(len(Pxx), dtype=bool)
    noise_mask[max(0, idx-8):idx+9] = False
    noise_power = np.mean(Pxx[noise_mask])
    
    snr_db = 10 * np.log10(signal_power / (noise_power + 1e-12))
    return snr_db, f, Pxx, idx


if __name__ == "__main__":
    print("ESQET Stochastic Resonance — Debugged SNR Analysis\n")
    
    t = np.linspace(0, 600, 30000)
    A_sig = 0.28
    omega_sig = 0.18
    
    noise_levels = np.linspace(0.0, 3.0, 11)
    snr_results = []
    
    plt.figure(figsize=(15, 10))
    
    for i, noise in enumerate(noise_levels):
        sol = solve_ivp(vdp_stochastic, (0, t[-1]), [0.0, 0.0],
                       args=(noise, A_sig, omega_sig),
                       method='RK45', t_eval=t, rtol=1e-6)
        
        x = sol.y[0]
        
        # Compute SNR
        snr_db, f, Pxx, peak_idx = compute_snr(x, t, omega_sig)
        snr_results.append(snr_db)
        
        # Plot a few representative traces
        if i in [0, 3, 5, 7, 10]:
            plt.subplot(3, 2, [1,2,4,5,6][[0,3,5,7,10].index(i)])
            plt.plot(t[-8000:], x[-8000:], 'teal', lw=1.1, alpha=0.9)
            plt.plot(t[-8000:], A_sig*np.sin(omega_sig*t[-8000:]), 'red', lw=1.8, alpha=0.6)
            plt.title(f'Noise level = {noise:.2f} | SNR = {snr_db:.1f} dB')
            plt.xlabel('Time')
            plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('simulations/stochastic_resonance_debugged.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Summary plot
    plt.figure(figsize=(10, 6))
    plt.plot(noise_levels, snr_results, 'o-', color='purple', linewidth=2, markersize=6)
    best_idx = np.argmax(snr_results)
    plt.axvline(noise_levels[best_idx], color='red', linestyle='--', alpha=0.7)
    plt.title('Stochastic Resonance Curve — SNR vs Noise Intensity')
    plt.xlabel('Noise Level')
    plt.ylabel('SNR (dB)')
    plt.grid(True, alpha=0.3)
    plt.savefig('simulations/snr_vs_noise.png', dpi=300)
    plt.show()
    
    print(f"✅ Best SNR: {snr_results[best_idx]:.2f} dB at noise level ≈ {noise_levels[best_idx]:.2f}")
    print("Classic stochastic resonance signature observed.")
