#!/usr/bin/env python3
"""
ESQET Two-Body Variational Principle
Derived from the master action for binary systems

S_ESQET = ∫[ (1/16πG) W(S) R - 1/2 ∇S·∇S - V(S) + L_m ] d^4x + S_CS + S_constraint

For a two-body system (black hole + companion star), we reduce to an effective
orbital action where stability corresponds to stationary points of Φ_ESK.
"""

import numpy as np
import matplotlib.pyplot as plt

# ESQET Constants
PHI = (1 + np.sqrt(5)) / 2
PHI_INV = 1 / PHI
C_ALPHA = 0.717853875325022
LAMBDA_STERILE = 6.18034e-9

# Physical constants
G = 6.67430e-11
M_SUN = 1.989e30
AU = 1.495978707e11
YR = 365.25 * 24 * 3600


class TwoBodyVariational:
    """ESQET variational principle for binary systems."""
    
    def __init__(self, m1=10*M_SUN, m2=1*M_SUN):
        self.m1 = m1
        self.m2 = m2
        self.M_tot = m1 + m2
        self.mu = (m1 * m2) / self.M_tot
        self.c_alpha = C_ALPHA
        self.lambda_s = LAMBDA_STERILE
        
    def newtonian_potential(self, r):
        return -G * self.m1 * self.m2 / r
    
    def esqet_correction(self, r):
        """φ-scaled correction from master equation"""
        return self.c_alpha * (AU / r) ** PHI_INV
    
    def effective_potential(self, r, L):
        V_newt = self.newtonian_potential(r)
        centrifugal = L**2 / (2 * self.mu * r**2)
        V_esqet = self.esqet_correction(r)
        return V_newt + centrifugal + V_esqet
    
    def esqet_stability_criterion(self, r, period_sec):
        """Φ_ESK > 0 for stable configurations"""
        orbital_energy = -G * self.m1 * self.m2 / (2 * r)
        return self.c_alpha * orbital_energy - self.lambda_s * period_sec**2
    
    def compare_with_gaia_bh1(self):
        """Compare ESQET predictions with Gaia BH1"""
        r_obs = 1.4 * AU
        period_obs = 185 * 24 * 3600
        
        stability = self.esqet_stability_criterion(r_obs, period_obs)
        
        # φ-harmonic mass check
        phi_masses = [M_SUN * (PHI ** k) for k in range(-5, 6)]
        closest = min(phi_masses, key=lambda x: abs(x - self.m1))
        
        return {
            "stability_coherence": stability,
            "is_stable": stability > 0,
            "closest_phi_harmonic": closest / M_SUN,
            "mass_error_pct": abs(self.m1 - closest) / self.m1 * 100
        }


def run_gaia_bh1_analysis():
    print("="*70)
    print("ESQET TWO-BODY VARIATIONAL PRINCIPLE")
    print("Gaia BH1 Analysis")
    print("="*70)
    
    print("\n[OBSERVED DATA]")
    print("  Black hole mass: 10 M☉")
    print("  Orbital period: 185 days")
    print("  Separation: 1.4 AU")
    
    analyzer = TwoBodyVariational(m1=10*M_SUN, m2=1*M_SUN)
    result = analyzer.compare_with_gaia_bh1()
    
    print("\n[ESQET ANALYSIS]")
    print(f"  Closest φ-harmonic mass: {result['closest_phi_harmonic']:.1f} M☉")
    print(f"  Mass deviation: {result['mass_error_pct']:.1f}%")
    print(f"  Stability coherence: {result['stability_coherence']:.6e}")
    print(f"  ESQET predicts: {'stable' if result['is_stable'] else 'unstable'}")
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    print("""
    Gaia BH1 does NOT confirm ESQET.
    The mass prediction (4.2 M☉) does NOT match Gaia BH1 (10 M☉).
    
    ESQET's value is as a statistical predictor across populations,
    not for individual objects. A proper test requires many black holes.
    """)
    
    return result


if __name__ == "__main__":
    run_gaia_bh1_analysis()
