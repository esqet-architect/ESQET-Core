import numpy as np
import matplotlib.pyplot as plt

def plot_kam_rg_flow():
    """
    Visualizes KAM-style stability in the deformed RG space.
    """
    omega = 12.0
    epsilon = 0.01
    mu = np.logspace(0, 4, 1000)
    
    # Generate multiple trajectories
    plt.figure(figsize=(10, 6))
    for g0 in np.linspace(0.5, 1.5, 5):
        # Simulated log-periodic coupling
        g_mu = g0 * (1 - 0.1 * np.log(mu/mu[0])) * (1 + epsilon * np.cos(omega * np.log(mu)))
        plt.semilogx(mu, g_mu, label=f'g_start={g0}')

    plt.title("KAM-Stable RG Trajectories (ESQET Modulation)")
    plt.xlabel("Energy Scale $\mu$ (GeV)")
    plt.ylabel("Effective Coupling $g(\mu)$")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.savefig("simulations/rg_stability_kam.png")
    print("Stability plot generated: simulations/rg_stability_kam.png")

if __name__ == "__main__":
    plot_kam_rg_flow()
