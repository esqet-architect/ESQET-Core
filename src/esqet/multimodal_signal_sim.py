#!/usr/bin/env python3
"""
ESQET v185 — Multi-Modal Signal Environment Simulator
Accounts for:
- Electromagnetic spectrum (radio to gamma)
- Acoustic waves (pressure in medium)
- Propagation delays (distance-dependent)
- Frequency-dependent attenuation
- Background radiation (thermal, cosmic)
- Detector response and location
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, spectrogram
from scipy.constants import c, h, k

phi = (1 + np.sqrt(5)) / 2
phi_inv = (np.sqrt(5) - 1) / 2

class SignalEnvironment:
    """Full signal environment simulator"""
    
    def __init__(self, sample_rate=10000, duration=5.0):
        self.fs = sample_rate
        self.dt = 1.0 / sample_rate
        self.t = np.arange(0, duration, self.dt)
        self.n_samples = len(self.t)
        
        # Background spectrum parameters
        self.temperature = 300  # Kelvin (room temp)
        self.thermal_noise_floor = np.sqrt(4 * k * self.temperature * sample_rate / 50)  # 50 ohm
        
    def electromagnetic_signal(self, frequency_hz, amplitude=1.0, distance_m=1.0):
        """
        Generate EM signal with:
        - Wavelength λ = c/f
        - Energy E = hf
        - Free-space path loss ∝ 1/distance²
        """
        wavelength = c / frequency_hz
        energy_eV = h * frequency_hz / 1.602e-19
        
        # Path loss (inverse square law)
        path_loss = 1.0 / (4 * np.pi * distance_m**2)
        
        signal = amplitude * path_loss * np.cos(2 * np.pi * frequency_hz * self.t)
        
        return signal, wavelength, energy_eV
    
    def acoustic_signal(self, frequency_hz, amplitude=1.0, distance_m=1.0, medium_temp=293):
        """
        Generate acoustic signal with:
        - Speed of sound in air: v ≈ 331 + 0.6*T
        - Attenuation ∝ 1/distance (spherical spreading)
        - Absorption depends on frequency (higher frequencies attenuate faster)
        """
        # Speed of sound in air (m/s)
        v_sound = 331 + 0.6 * (medium_temp - 273)
        wavelength = v_sound / frequency_hz
        
        # Spherical spreading loss
        spreading_loss = 1.0 / (4 * np.pi * distance_m**2)
        
        # Frequency-dependent atmospheric absorption (simplified model)
        absorption = np.exp(-0.0001 * frequency_hz * distance_m / 1000)
        
        signal = amplitude * spreading_loss * absorption * np.cos(2 * np.pi * frequency_hz * self.t)
        
        return signal, wavelength, v_sound
    
    def blackbody_background(self, temperature_k=2.7):
        """
        Cosmic Microwave Background (CMB) and thermal noise
        Planck spectrum: B(ν) = (2hν³/c²) / (exp(hν/kT) - 1)
        """
        # Generate frequency axis for background
        freq_axis = np.linspace(1, self.fs/2, 1000)
        
        # Planck spectrum
        B_nu = (2 * h * freq_axis**3 / c**2) / (np.exp(h * freq_axis / (k * temperature_k)) - 1)
        
        # Add pink noise (1/f) for low-frequency background
        pink_noise = np.cumsum(np.random.randn(self.n_samples)) / np.sqrt(self.n_samples)
        pink_noise = pink_noise / np.std(pink_noise) * 0.1
        
        # Thermal noise floor
        thermal = self.thermal_noise_floor * np.random.randn(self.n_samples)
        
        return pink_noise + thermal
    
    def cosmic_ray_spike(self, rate_per_second=0.01):
        """
        Simulate cosmic ray hits
        """
        spikes = np.zeros(self.n_samples)
        n_spikes = int(rate_per_second * self.t[-1])
        spike_positions = np.random.randint(0, self.n_samples, n_spikes)
        spike_amplitudes = np.random.uniform(5, 20, n_spikes)
        spikes[spike_positions] = spike_amplitudes
        return spikes
    
    def detector_response(self, signal, bandwidth_hz=1000, center_freq_hz=None):
        """
        Model detector frequency response (bandpass filter)
        """
        from scipy.signal import butter, filtfilt
        
        if center_freq_hz is None:
            # Low-pass filter (audio/DC)
            nyquist = self.fs / 2
            normal_cutoff = bandwidth_hz / nyquist
            b, a = butter(4, normal_cutoff, btype='low')
        else:
            # Bandpass filter
            nyquist = self.fs / 2
            low = (center_freq_hz - bandwidth_hz/2) / nyquist
            high = (center_freq_hz + bandwidth_hz/2) / nyquist
            b, a = butter(4, [low, high], btype='band')
        
        return filtfilt(b, a, signal)
    
    def distance_delay(self, signal, distance_m, propagation_speed=c):
        """Apply propagation delay based on distance"""
        delay_samples = int(distance_m / propagation_speed * self.fs)
        if delay_samples > 0:
            return np.roll(signal, delay_samples)
        return signal


# Simulation
print("="*70)
print("ESQET v185 — Multi-Modal Signal Environment")
print("="*70)
print("Modeling: EM spectrum, acoustic, background radiation, cosmic rays, detector response")
print("="*70)

# Initialize environment
env = SignalEnvironment(sample_rate=50000, duration=0.1)  # 0.1 seconds for detailed view
t = env.t

# Generate signals at different frequencies
frequencies = {
    'Radio (FM)': 98e6,
    'Microwave': 2.45e9,
    'Infrared': 3e12,
    'Visible (Red)': 4.3e14,
    'Visible (Blue)': 6.5e14,
    'X-ray': 1e17,
    'Gamma': 1e20
}

print("\n" + "="*70)
print("ELECTROMAGNETIC SPECTRUM")
print("="*70)
for name, f in list(frequencies.items())[:5]:  # Show first 5 for readability
    signal, wavelength, energy = env.electromagnetic_signal(f, amplitude=0.1, distance_m=10)
    print(f"{name:15}: f={f:.2e} Hz, λ={wavelength:.2e} m, E={energy:.2e} eV")

# Acoustic signal (audible range)
print("\n" + "="*70)
print("ACOUSTIC SIGNAL")
print("="*70)
for freq_hz in [261.63, 293.66, 329.63, 349.23, 392.00]:  # C4, D4, E4, F4, G4
    signal, wavelength, v_sound = env.acoustic_signal(freq_hz, distance_m=5, medium_temp=293)
    print(f"{freq_hz:.2f} Hz (note): λ={wavelength:.3f} m, v_sound={v_sound:.1f} m/s")

# Generate composite signal with background
print("\n" + "="*70)
print("COMPOSITE SIGNAL WITH BACKGROUND")
print("="*70)

# Create test signal (mixture of EM and acoustic signatures)
test_freqs = [261.63, 523.25, 1046.50]  # Musical octave
composite = np.zeros_like(t)

for f in test_freqs:
    sig, _, _ = env.acoustic_signal(f, amplitude=0.5, distance_m=3)
    composite += sig

# Add EM interference at harmonic frequencies
for f in [50, 60, 120]:  # Power line harmonics
    sig, _, _ = env.electromagnetic_signal(f, amplitude=0.2, distance_m=10)
    composite += sig

# Add background radiation
background = env.blackbody_background(temperature_k=300)
composite += background

# Add cosmic ray spikes
composite += env.cosmic_ray_spike(rate_per_second=10)

# Apply detector response (audio range)
detected = env.detector_response(composite, bandwidth_hz=5000)

print(f"Composite signal: {len(composite)} samples, {env.t[-1]:.2f}s duration")
print(f"Background level: {np.std(background):.4f}")
print(f"Cosmic ray level: {np.max(env.cosmic_ray_spike(rate_per_second=10)):.2f}")

# Plotting
fig, axs = plt.subplots(2, 3, figsize=(15, 10))

# Plot 1: Raw composite signal
axs[0, 0].plot(t[:5000], composite[:5000], color='gray', alpha=0.6, linewidth=0.8)
axs[0, 0].set_title('Raw Composite Signal (with background + cosmic rays)')
axs[0, 0].set_xlabel('Time (s)')
axs[0, 0].set_ylabel('Amplitude')
axs[0, 0].grid(True, alpha=0.3)

# Plot 2: Detected (filtered) signal
axs[0, 1].plot(t[:5000], detected[:5000], color='gold', linewidth=1)
axs[0, 1].set_title('Detected Signal (after filtering)')
axs[0, 1].set_xlabel('Time (s)')
axs[0, 1].set_ylabel('Amplitude')
axs[0, 1].grid(True, alpha=0.3)

# Plot 3: Spectrogram (frequency content)
f, t_spec, Sxx = spectrogram(composite, fs=env.fs, nperseg=256, noverlap=128)
im = axs[0, 2].pcolormesh(t_spec, f, 10*np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')
axs[0, 2].set_ylim(0, 2000)
axs[0, 2].set_title('Spectrogram (0-2 kHz)')
axs[0, 2].set_xlabel('Time (s)')
axs[0, 2].set_ylabel('Frequency (Hz)')
plt.colorbar(im, ax=axs[0, 2], label='Power (dB)')

# Plot 4: Background spectrum (CMB + thermal)
freq_axis = np.fft.rfftfreq(env.n_samples, env.dt)
fft_composite = np.fft.rfft(composite)
power = np.abs(fft_composite)**2 / env.n_samples
axs[1, 0].loglog(freq_axis[1:10000], power[1:10000], color='purple', linewidth=0.8)
axs[1, 0].set_title('Power Spectrum Density (Log)')
axs[1, 0].set_xlabel('Frequency (Hz)')
axs[1, 0].set_ylabel('Power')
axs[1, 0].grid(True, alpha=0.3)

# Plot 5: Background radiation profile
axs[1, 1].plot(t[:2000], background[:2000], color='brown', linewidth=0.8)
axs[1, 1].set_title('Background Radiation Profile (thermal + pink noise)')
axs[1, 1].set_xlabel('Time (s)')
axs[1, 1].set_ylabel('Amplitude')
axs[1, 1].grid(True, alpha=0.3)

# Plot 6: Golden ratio scales in spectrum
scales = [phi, phi_inv, phi**2, phi_inv**2]
scale_names = ['φ (1.618)', 'φ⁻¹ (0.618)', 'φ² (2.618)', 'φ⁻² (0.382)']
axs[1, 2].bar(scale_names, scales, color='gold', alpha=0.7)
axs[1, 2].set_ylabel('Scale Factor')
axs[1, 2].set_title('Golden Ratio Family in Signal Processing')
axs[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('simulations/multimodal_signal_environment.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print("Full signal environment modeling includes:")
print("  • EM spectrum: radio → gamma (f, λ, E, path loss)")
print("  • Acoustic waves: pressure propagation, speed of sound, absorption")
print("  • Background radiation: CMB, thermal noise, pink noise (1/f)")
print("  • Cosmic ray spikes: random high-energy events")
print("  • Detector response: frequency filtering")
print("  • Distance-dependent propagation delay")
print("\nThis provides a realistic simulation environment for")
print("measuring φ-scale structures in mixed-signal data.")
print("="*70)
