import numpy as np
from src.esqet.rg_floquet import compute_floquet_monodromy

phi = (1 + 5**0.5) / 2
# Scan range covering the φ^3 to φ^5 harmonics
omega_range = np.linspace(4.0, 12.0, 100)
epsilon = 0.1  # Stronger deformation to highlight resonance

print("ESQET Resonance Scan: Searching for Scale-Locking Islands")
print("-" * 60)
print(f"{'Omega (ω)':<15} | {'Lambda (λ)':<15} | {'Stability'}")
print("-" * 60)

results = []
for w in omega_range:
    res = compute_floquet_monodromy(omega=w, epsilon=epsilon)
    lam = res['max_exponent']
    results.append((w, lam))
    # Detect local stability increases (lower lambda)
    status = "RESONANCE" if lam < 0.0275 else "DRIFT"
    print(f"{w:<15.4f} | {lam:<15.6f} | {status}")

# Find the absolute minimum in this range
best_w, best_lam = min(results, key=lambda x: x[1])
print("-" * 60)
print(f"CRITICAL RESONANCE DETECTED AT ω = {best_w:.4f}")
print(f"MINIMUM FLOQUET EXPONENT λ = {best_lam:.6f}")
