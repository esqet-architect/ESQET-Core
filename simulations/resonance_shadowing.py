import numpy as np
import matplotlib.pyplot as plt

def plot_shadow():
    size = 200
    x, y = np.meshgrid(np.linspace(-5, 5, size), np.linspace(-5, 5, size))
    r = np.sqrt(x**2 + y**2)
    phi = (1 + np.sqrt(5))/2
    
    # The background "Unity Resonance" of the vacuum
    vacuum = np.cos(r * phi * 2) * np.exp(-r**2 / 10)
    
    # The "Shadow" cast by a central mass (Axiom 12)
    mass_shadow = np.exp(-r**2 / 1.5)
    induced_gravity = vacuum * (1 - mass_shadow)
    
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.imshow(vacuum, cmap='viridis')
    plt.title("Vacuum Resonance (Axiom 1)")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(induced_gravity, cmap='magma')
    plt.title("Resonant Shadow (Induced Gravity)")
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig("simulations/resonance_shadowing.png")
    print("Visual generated: simulations/resonance_shadowing.png")

if __name__ == "__main__":
    plot_shadow()
