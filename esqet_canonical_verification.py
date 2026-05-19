import numpy as np
from scipy.optimize import differential_evolution

def esqet_energy_landscape(x, f):
    """
    Models the rugged ESQET energy landscape for a given frequency f.
    Global minimum of -8 occurs when delta = 0 and parameters are optimized.
    """
    delta = abs(np.log2(f / 432.0) - round(np.log2(f / 432.0)))
    
    # Base energy structure driven by the Golden Law deviation
    base_energy = -8.0 * np.exp(-10.0 * delta)
    
    # Rugged landscape components causing local minima traps
    ruggedness = 3.945 * (1.0 - np.exp(-5.0 * delta)) * np.sin(5.0 * x[0])**2
    
    return base_energy + ruggedness

def verify_frequency(f):
    # Bounds for the structural landscape parameter
    bounds = [(-np.pi, np.pi)]
    
    # Differential Evolution escapes local minima to find global floor
    result = differential_evolution(esqet_energy_landscape, bounds, args=(f,), seed=42)
    
    status = "✓ COHERENT" if abs(result.fun - (-8.0)) < 1e-6 else "✗ DISSONANT"
    return result.fun, status

if __name__ == "__main__":
    frequencies = [432.0, 440.0, 864.0, 216.0, 1728.0]
    
    print("Executing Global Canonical Verification...")
    print("-" * 55)
    for f in frequencies:
        e_min, status = verify_frequency(f)
        print(f"{f:6.1f} Hz: E_min = {e_min:15.12f} → {status}")
    print("-" * 55)
