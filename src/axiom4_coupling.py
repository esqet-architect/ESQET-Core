import numpy as np

def run_axiom4_coupling():
    print("="*60)
    print("ESQET Axiom 4: Electromagnetic Coupling Integration")
    print("="*60)

    # Physical Constants
    alpha_inv = 137.035999  # 1/alpha
    phi = (1 + 5**0.5) / 2

    # Mass Units from Axiom 3
    # Gen I: 1.0, Gen II: 99.50, Gen III: 682.00
    mass_units = [1.0, 99.50, 682.00]
    
    print(f"Inverse Fine Structure Constant (α⁻¹): {alpha_inv}")
    print("-" * 40)

    for i, m in enumerate(mass_units):
        # Calculate the coupling resonance: (Mass / alpha_inv)
        resonance = m / alpha_inv
        # Calculate topological deviation from Phi
        deviation = resonance / phi
        
        print(f"Gen {i+1} Resonance: {resonance:.4f}")
        print(f"Gen {i+1} Phi-Deviation: {deviation:.4f}")
        print("-" * 20)

if __name__ == "__main__":
    run_axiom4_coupling()
