import numpy as np
import matplotlib.pyplot as plt

def run_sky_test():
    """
    ESQET Sky Test: Projects Primordial Floquet Oscillations into CMB Space
    Includes Silk Damping and Fisher Information Analysis.
    """
    # 1. Configuration
    l_max = 2500
    ell = np.arange(2, l_max)
    phi = (1 + np.sqrt(5)) / 2
    
    # ESQET Parameters
    A_primordial = 0.01      # Primordial amplitude
    omega_phi = 12.0         # Axiom 12 frequency
    delta = 0.0              # Phase
    
    # 2. Analytic Transfer Damping (Silk Damping Approximation)
    # Oscillations are suppressed at high l as the photon-baryon plasma 
    # diffuses. theta_d is the damping scale.
    theta_d = 0.0016 
    damping_filter = np.exp(-(ell * theta_d)**2)
    
    # 3. Geometric Projection
    # Projecting log-k onto angular l-space
    # Delta_Cl/Cl ~ A * damping * cos(omega * ln(l) + delta)
    esqet_signal = A_primordial * damping_filter * np.cos(omega_phi * np.log(ell) + delta)
    
    # 4. Statistical Noise Model (Planck-like)
    f_sky = 0.65
    cosmic_variance = np.sqrt(2.0 / ((2 * ell + 1) * f_sky))
    instrument_noise = 1e-4 * np.exp((ell / 1500)**2) # High-l noise rise
    total_error = cosmic_variance + instrument_noise

    # 5. Fisher Calculation for Detectability
    # F = sum [ (dSignal/dA)^2 / Error^2 ]
    signal_derivative = damping_filter * np.cos(omega_phi * np.log(ell))
    fisher_a = np.sum((signal_derivative**2) / (total_error**2))
    sigma_a = 1.0 / np.sqrt(fisher_a)
    snr = A_primordial / sigma_a

    # 6. Visualization
    plt.figure(figsize=(12, 6))
    
    # Plot the residuals (The "Sky" vs Lambda-CDM)
    plt.plot(ell, esqet_signal, label=r'ESQET Residual ($\Delta C_\ell / C_\ell$)', color='gold', lw=2)
    plt.fill_between(ell, -total_error, total_error, color='gray', alpha=0.2, label='1-$\sigma$ Detection Threshold')
    
    plt.axhline(0, color='white', linestyle='--', alpha=0.5)
    plt.title(f"ESQET Observational Signature: SNR = {snr:.2f}")
    plt.xlabel("Multipole Moment (l)")
    plt.ylabel(r"Relative Anisotropy Difference")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.3)
    
    plt.savefig("simulations/esqet_sky_signature.png")
    
    print("ESQET SKY TEST COMPLETE")
    print("-" * 30)
    print(f"Primordial Amplitude: {A_primordial}")
    print(f"Damped Max Amplitude: {np.max(esqet_signal):.6f}")
    print(f"Fisher Uncertainty (σ_A): {sigma_a:.6f}")
    print(f"Detectability (SNR): {snr:.2f}")
    print("-" * 30)
    if snr > 3:
        print("RESULT: Falsifiable. ESQET is within current mission sensitivity.")
    else:
        print("RESULT: Degenerate. ESQET is indistinguishable from standard vacuum.")

if __name__ == "__main__":
    run_sky_test()
