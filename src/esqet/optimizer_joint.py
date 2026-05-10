import numpy as np
from scipy.optimize import differential_evolution
import mpmath as mp

mp.mp.dps = 50
PHI = (mp.mpf(1) + mp.sqrt(5)) / 2
OMEGA = mp.exp(2j * mp.pi / 3)

# Target Masses (MeV)
TARGETS = {'e': 0.51099, 'mu': 105.658, 'tau': 1776.86}

def get_mass(n, p, lam, base, alpha):
    # Z3 Phase Modulation
    phase = OMEGA ** (n * (2 * mp.pi / 3) / mp.log(PHI) % 3)
    # The 'Stiffness' alpha adjusts the depth of the generation shutter
    delta = (mp.re(phase) + 1.0) ** alpha
    return base + lam * (PHI ** (n * p)) * delta

def objective(params):
    p, lam, base, alpha = [mp.mpf(x) for x in params]
    
    m_e = get_mass(0, p, lam, base, alpha)
    m_mu = get_mass(1, p, lam, base, alpha)
    m_tau = get_mass(2, p, lam, base, alpha)
    
    # Relative Energy Functional
    # We weight the Muon heavily to force the optimizer out of the p=9 trap
    error = ((m_e - TARGETS['e'])/TARGETS['e'])**2 + \
            ((m_mu - TARGETS['mu'])/TARGETS['mu'])**2 * 5 + \
            ((m_tau - TARGETS['tau'])/TARGETS['tau'])**2
            
    return float(mp.sqrt(error))

if __name__ == "__main__":
    # Bounds designed to find the p~6 'Golden' region
    bounds = [(5.5, 6.5), (1.0, 15.0), (0, 1), (0.1, 2.0)]
    result = differential_evolution(objective, bounds, tol=1e-15)
    
    p, lam, base, alpha = result.x
    print(f"\n--- SPECTRAL INTERVENTION COMPLETE ---")
    print(f"Optimal p    : {p:.6f}")
    print(f"Stiffness α  : {alpha:.6f}")
    print(f"Base (MeV)   : {base:.6f}\n")
    
    for i, k in enumerate(['e', 'mu', 'tau']):
        pred = get_mass(i, p, lam, base, alpha)
        err = abs(float(pred) - TARGETS[k]) / TARGETS[k] * 100
        print(f"{k.upper():<3} | Pred: {float(pred):10.4f} | Actual: {TARGETS[k]:10.4f} | Err: {err:7.4f}%")
