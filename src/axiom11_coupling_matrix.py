import numpy as np

def run_axiom11_matrix():
    print("="*60)
    print("ESQET Axiom 11: Inter-Generational Coupling Matrix")
    print("="*60)

    # Topological Masses (Refined from Axiom 7)
    masses = np.array([1.0, 206.76, 3477.15])
    phi = (1 + 5**0.5) / 2
    
    # Initialize a 3x3 Interaction Matrix
    # Matrix[i,j] represents the resonance ratio between generations
    matrix = np.zeros((3, 3))
    
    for i in range(3):
        for j in range(3):
            # The coupling is the ratio of their topological footprints
            # normalized by the Golden Ratio (phi)
            coupling = (masses[i] / masses[j]) / phi
            matrix[i][j] = coupling

    print(f"Coupling Resonances (Normalized to Phi):")
    print("-" * 50)
    print(f"{'':<10} | {'Gen 1':>10} | {'Gen 2':>10} | {'Gen 3':>10}")
    print("-" * 50)
    
    gens = ["Gen 1", "Gen 2", "Gen 3"]
    for i, row in enumerate(matrix):
        print(f"{gens[i]:<10} | {row[0]:>10.2f} | {row[1]:>10.2f} | {row[2]:>10.2f}")

if __name__ == "__main__":
    run_axiom11_matrix()
