import numpy as np
import matplotlib.pyplot as plt

def esqet_fisher_analysis():
    # Experimental specs (approximate Planck-like)
    l_max = 2500
    ell = np.arange(2, l_max)
    
    # ESQET Signal: Delta Cl / Cl = A * cos(omega * ln(l) + delta)
    # We test the sensitivity to the frequency 'omega'
    omega = 10.0  # Log-frequency
    A = 0.01      # Amplitude of the resonance ripple
    
    # Noise model (Cosmic Variance + Instrumental)
    # f_sky = fraction of sky observed
    f_sky = 0.65
    C_l_noise = (2 / ((2 * ell + 1) * f_sky))
    
    # Derivatives for Fisher Matrix
    # d(Cl)/d(omega) = -A * ln(ell) * sin(omega * ln(ell) + delta)
    deriv_omega = -A * np.log(ell) * np.sin(omega * np.log(ell))
    
    # Fisher Element F_omega_omega
    # F = sum [ (1/Var) * (dCl/d_param)^2 ]
    F_omega_omega = np.sum((1 / C_l_noise) * (deriv_omega**2))
    
    # Predicted 1-sigma error on the frequency
    sigma_omega = 1 / np.sqrt(F_omega_omega)
    
    print("ESQET Fisher Forecast (CMB-S4 Level)")
    print("-" * 50)
    print(f"Log-Frequency (omega): {omega}")
    print(f"Modulation Amp (A):    {A}")
    print(f"Predicted Error (sigma_omega): {sigma_omega:.6f}")
    print(f"Signal-to-Noise (omega/sigma): {omega/sigma_omega:.2f}")
    
    if omega/sigma_omega > 5:
        print("Status: HIGHLY DETECTABLE (Should be visible in residuals)")
    else:
        print("Status: HIDDEN (Below current sensitivity limits)")

if __name__ == "__main__":
    esqet_fisher_analysis()
