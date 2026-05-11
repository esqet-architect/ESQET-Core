import numpy as np
import time
import os

# Define 32-bit precision for Exynos 1380 efficiency
DTYPE = np.float32
size = 256 

# Initialize field with phi-based normalization
phi = DTYPE((1 + 5**0.5) / 2)
field = (np.random.normal(0, 1, (size, size)) / phi).astype(DTYPE)

print(f"[*] Starting 32-bit S-Field Stress Test...")
start = time.time()

# 500 iterations of Laplacian tension
for i in range(500):
    # Quick 2D Laplacian approximation
    laplacian = (np.roll(field, 1, axis=0) + np.roll(field, -1, axis=0) +
                 np.roll(field, 1, axis=1) + np.roll(field, -1, axis=1) - 4*field)
    field += 0.1 * laplacian

end = time.time()
print(f"[*] Results for Samsung A35:")
print(f"[*] 500 iterations on {size}x{size} lattice: {end-start:.4f}s")
print(f"[*] Field Mean: {np.mean(field):.6e}")
