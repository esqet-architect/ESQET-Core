#!/usr/bin/env python3
"""
rauzy_fractal_visualizer.py
===========================
Generates the Rauzy Fractal Central Tile via Tribonacci substitution sequence.
Utilizes exact contracting complex conjugate roots to eliminate hardcoded
geometric approximations and rounding distortions.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

OUTPUT_DIR = "/root/ESQET-Core/analysis"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_IMG = os.path.join(OUTPUT_DIR, "rauzy_fractal_tribonacci.png")

def get_exact_projection_operators():
    """
    Computes exact projection parameters using the complex roots of 
    the characteristic polynomial: \\lambda^3 - \\lambda^2 - \\lambda - 1 = 0.
    Eliminates manual float approximations for contraction and angle metrics.
    """
    # Matrix characteristic coefficients: 1*x^3 - 1*x^2 - 1*x - 1 = 0
    coeffs = [1, -1, -1, -1]
    roots = np.roots(coeffs)
    
    # Isolate the dominant real Pisot root and the contracting complex pair
    real_root = roots[np.isreal(roots)].real[0]
    complex_roots = roots[np.iscomplex(roots)]
    
    # The contracting root governs the exact mathematical scale of the fractal tile
    contracting_root = complex_roots[0]
    
    # Construct canonical substitution incidence matrix
    # M = [[1, 1, 1], [1, 0, 0], [0, 1, 0]]
    # We find the exact eigenvector corresponding to the contracting complex eigenvalue
    # to yield the unrounded orthogonal projection plane.
    v_c = np.array([contracting_root**2, contracting_root, 1.0], dtype=complex)
    
    return contracting_root, v_c

def generate_rauzy_points(generations: int = 15):
    """
    Generates point sequences strictly adhering to the Tribonacci substitution topology:
    a -> ab, b -> ac, c -> a. 
    Projects coordinates orthogonally using the exact complex eigenplane.
    """
    contracting_root, v_c = get_exact_projection_operators()
    
    # Initialize prefix word sequence
    word = "a"
    for _ in range(generations):
        # Apply pure structural replacement rules
        next_word = []
        for char in word:
            if char == 'a':
                next_word.append("ab")
            elif char == 'b':
                next_word.append("ac")
            elif char == 'c':
                next_word.append("a")
        word = "".join(next_word)
        
    # Translate the generated substitution word into walk steps across R^3
    n = len(word)
    steps = np.zeros((n, 3))
    
    current_pos = np.zeros(3)
    for i, char in enumerate(word):
        steps[i] = current_pos
        if char == 'a':
            current_pos += [1, 0, 0]
        elif char == 'b':
            current_pos += [0, 1, 0]
        elif char == 'c':
            current_pos += [0, 0, 1]
            
    # Project 3D lattice path tracking coordinates onto the 2D complex plane slice
    projected_complex = steps @ v_c
    
    # Extract structural 2D spatial axes from complex data fields
    x_coords = projected_complex.real
    y_coords = projected_complex.imag
    
    # Center translation without metric truncation
    x_coords -= np.mean(x_coords)
    y_coords -= np.mean(y_coords)
    
    return x_coords, y_coords

def main():
    print("🚀 Computing Exact Topological Rauzy Fractal Projection...")
    
    # Generation 14 produces exactly 5,768 analytical points (T_15)
    x, y = generate_rauzy_points(generations=14)
    
    plt.figure(figsize=(11, 11), dpi=300)
    plt.style.use('dark_background')
    
    # High-density scatter mapping capturing pure mathematical boundaries
    plt.scatter(x, y, s=0.1, alpha=0.75, color='#00ffcc', edgecolors='none')
    
    plt.title('Rauzy Fractal — Tribonacci Pisot Substitution Plane', fontsize=14, color='white', pad=20)
    plt.xlabel('Canonical Projection Axis 1', fontsize=10, color='#888888')
    plt.ylabel('Canonical Projection Axis 2', fontsize=10, color='#888888')
    
    plt.axis('equal')
    plt.grid(True, which='both', linestyle=':', color='#333333', alpha=0.5)
    
    plt.savefig(OUTPUT_IMG, bbox_inches='tight', facecolor='black')
    plt.close()
    
    print(f"✅ Success. Pure unrounded fractal mapping saved to:\n  {OUTPUT_IMG} ({len(x):,} points calculated)")

if __name__ == "__main__":
    main()
