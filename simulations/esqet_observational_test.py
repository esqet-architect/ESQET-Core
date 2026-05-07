import numpy as np
import matplotlib.pyplot as plt

def run_sky_test():
    """
    ESQET Sky Test: Projects Primordial Floquet Oscillations into CMB Space
    Includes Analytic Silk Damping and Fisher Information Analysis.
    """
    # 1. Configuration
    l_max = 2500
    ell = np.arange(2, l_max)
    
    # ESQET Parameters
    A_primordial = 0.01      # Primordial amplitude (1%)
    omega_phi = 12.0         # Log-frequency from Axiom 12
    delta = 0.0              # Phase
    
    # 2. Analytic Transfer Damping (Envelope Suppression)
    # sigma_l represents the width of the transfer kernel in log-k space.
    # It broadens at high l due to recombination thickness and Silk damping.
    sigma_0 = 0.01           # Baseline width at recombination
    alpha = 0.005            # Broadening rate
    sigma_l = sigma_0 + alpha * np.log(ell)
    
    # The Gaussian Damping Envelope: A_eff = A * exp(-0.5 * omega^2 * sigma_l^2)
    damping_envelope = np.exp(-0.5 * (omega_phi**2) * (sigma_l**2))
    
    # 3. Geometric Projection
    # Delta_Cl/Cl ~ A_eff * cos(omega * ln(l) + delta)
    esqet_signal = A_primordial * damping_envelope * np.cos(omega_phi * np.log(ell) + delta)
    
    # 4. Statistical Noise Model (Planck-like)
    f_sky = 0.65
    cosmic_variance = np.sqrt(2.0 / ((2 * ell + 1) * f_sky))
    # Instrument noise floor (simplified rise at high l)
    instrument_noise = 1e-4 * np.exp((ell / 1800)**2) 
    total_noise = cosmic_variance + instrument_noise

    # 5. Fisher Calculation with Damped Template
    # We evaluate if the damped signal survives the noise floor
    signal_derivative = damping_envelope * np.cos(omega_phi * np.log(ell))
    fisher_val = np.sum((signal_derivative**2) / (total_noise**2))
    sigma_a = 1.0 / np.sqrt(fisher_val)
    snr = A_primordial / sigma_a

    # 6. Visualization
    plt.figure(figsize=(12, 6))
    
    # Plot the ESQET Residuals
    plt.plot(ell, esqet_signal, label=r'Damped ESQET Residual ($\Delta C_\ell / C_\ell$)', color='gold', lw=2)
    plt.fill_between(ell, -total_noise, total_noise, color='gray', alpha=0.15, label='Planck Noise Floor (1-$\sigma$)')
    
    plt.axhline(0, color='white', linestyle='--', alpha=0.3)
    plt.title(f"ESQET Observational Test: $\omega_\phi$ = {omega_phi}, SNR = {snr:.2f}")
    plt.xlabel("Multipole Moment (l)")
    plt.ylabel(r"Relative Power Deviation")
    plt.xscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    
    plt.savefig("simulations/esqet_sky_signature.png")
    
    print("ESQET OBSERVATIONAL TEST COMPLETE")
    print("-" * 40)
    print(f"Primordial Amplitude: {A_primordial}")
    print(f"Damping at l=2000:    {damping_envelope[-1]:.4f}")
    print(f"Fisher Sensitivity:   {sigma_a:.6f}")
    print(f"Signal-to-Noise:      {snr:.2f}")
    print("-" * 40)
    
    if snr > 3:
        print("RESULT: Falsifiable. The golden-ratio signature survives damping.")
    else:
        print("RESULT: Degenerate. Signal erased by transfer damping.")

if __name__ == "__main__":
    run_sky_test()
