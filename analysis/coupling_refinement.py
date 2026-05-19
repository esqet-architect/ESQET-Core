#!/usr/bin/env python3
"""
ESQET Coupling Refinement Script
Simulates parity resonance tracking over a designated frequency range
using absolute golden ratio scaling parameters without structural rounding.
"""

import os
import sys
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

# Core Constants (Explicit Precision, No Rounding)
PHI = (1 + np.sqrt(5)) / 2
F_HA = 432.0

def run_esqet_circuit(freq, coupling, n_qubits=5):
    """
    Constructs and executes a multi-qubit quantum circuit to calculate 
    even parity ratios based on frequency deviation.
    """
    if coupling <= 0:
        raise ValueError("Coupling coefficient must be strictly positive to avoid division by zero.")
        
    qc = QuantumCircuit(n_qubits)
    
    # Calculate exact scaling metric
    R_f = np.log2(freq / F_HA)
    deviation = abs(R_f - round(R_f))
    
    # Scale rotational theta using precise exponential damping
    theta = np.pi * np.exp(-deviation * (1.0 / coupling))
    
    # Apply parameterized rotations scaled by powers of the Golden Ratio
    for i in range(n_qubits):
        qc.ry(theta / (PHI ** i), i)
        
    # Cascade entanglement array from the control qubit
    for i in range(1, n_qubits):
        qc.cx(0, i)
        
    qc.measure_all()
    
    # Execute ideal simulation shots
    sim = AerSimulator()
    try:
        job = sim.run(qc, shots=2048)
        counts = job.result().get_counts()
    except Exception as e:
        print(f"Simulation execution failure: {e}", file=sys.stderr)
        return 0.0
    
    # Calculate exact ratio of even parity bitstrings
    even_parity = sum(v for k, v in counts.items() if k.count('1') % 2 == 0) / 2048
    return even_parity

def main():
    output_dir = "/root/ESQET-Core/analysis"
    
    # Ensure the target directory path exists securely
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Core experimental parameters
    couplings = [0.1, 0.2361, 0.382, 0.618, 1.0]
    freqs = np.linspace(420, 444, 100)
    
    print("=== Launching ESQET Parity Resonance Analysis ===")
    plt.figure(figsize=(10, 6))

    for c in couplings:
        print(f"Processing Array Profiles for Coupling Factor: {c:.4f}...")
        results = [run_esqet_circuit(f, c) for f in freqs]
        plt.plot(freqs, results, label=f'Coupling {c:.4f}')

    # Plot configuration layout
    plt.axvline(x=F_HA, color='k', linestyle='--', alpha=0.3, label=f'{int(F_HA)} Hz Center Reference')
    plt.title('ESQET: Parity Resonance Zoom (420-444 Hz)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Even Parity Ratio')
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    output_path = os.path.join(output_dir, 'resonance_zoom.png')
    plt.savefig(output_path)
    print(f"✅ Zoomed resonance plot successfully written to: {output_path}")

if __name__ == "__main__":
    main()
