#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


class EEP1Design:

    def generate_bill_of_materials(self):
        return """
Optical reference lasers
Squeezed light source
Fiber Mach-Zehnder interferometer
Phase modulators
FPGA digitizer system
Thermal + vibration isolation
"""


def plot_simulated_results():

    tau = np.logspace(-1, 3, 200)
    allan_dev = 1e-15 / np.sqrt(tau)

    fig, axes = plt.subplots(2, 1, figsize=(8, 8))

    axes[0].loglog(tau, 1e-15/tau)
    axes[0].set_title("Simulated Phase Noise")

    axes[1].loglog(tau, allan_dev, linewidth=2)
    axes[1].set_xlabel("Averaging Time τ (s)")
    axes[1].set_ylabel("Allan Deviation")
    axes[1].set_title("Stability Projection")
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(y=1e-18, linestyle="--",
                    label="Optical clock level")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig("eep1_simulated_output.png", dpi=150)
    plt.show()

    print("\n✅ Simulated output saved: eep1_simulated_output.png")


def run_eep1_design():

    print("="*70)
    print("ESQET EXPERIMENTAL PROTOTYPE 1 (EEP-1)")
    print("="*70)

    eep1 = EEP1Design()

    print("\n[BILL OF MATERIALS]")
    print(eep1.generate_bill_of_materials())

    print("\n[FALSIFIABLE PREDICTION]")
    print("Search for coherence minimum near φ⁻¹ ≈ 0.618 Hz")

    return eep1


if __name__ == "__main__":
    run_eep1_design()
    plot_simulated_results()
