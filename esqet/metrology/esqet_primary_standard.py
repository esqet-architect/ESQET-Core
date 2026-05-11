#!/usr/bin/env python3

"""
ESQET Primary Standard — Quantum Coherence Reference (QCR)
Clean implementation.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List

PHI = (1 + np.sqrt(5)) / 2
C_ALPHA = 0.717853875325022
LAMBDA_STERILE = 6.18034e-9


@dataclass
class ESQETDeviceSpec:
    name: str
    value: float
    unit: str


class ESQETPrimaryStandard:

    def __init__(self):
        self.phi = PHI
        self.c_alpha = C_ALPHA
        self.lambda_s = LAMBDA_STERILE

        self.cavity_length = 1.0
        self.entanglement_time = 1.0
        self.phase_noise_floor = 1e-18

    # --------------------------------------------------

    def compute_theoretical_coherence_limit(self) -> float:
        return 1 / (2 * np.pi * self.lambda_s)

    # --------------------------------------------------

    def optical_lattice_clock(self) -> Dict:
        return {
            "atom": "Strontium",
            "transition_frequency": 4.29e14,
            "stability": 1e-18,
            "lattice_wavelength": 813e-9,
        }

    # --------------------------------------------------

    def entanglement_cavity(self) -> Dict:
        squeezing_db = 10 * np.log10(1 / (1 - self.c_alpha))

        return {
            "type": "Fabry-Perot",
            "length_m": self.cavity_length,
            "finesse": 1e6,
            "squeezing_db": squeezing_db,
        }

    # --------------------------------------------------

    def superconducting_loop(self) -> Dict:
        return {
            "material": "Niobium",
            "Tc_K": 9.2,
            "phase_sensitivity": 1e-18,
            "operating_temperature_K": 0.1,
        }

    # --------------------------------------------------

    def measurement_protocol(self) -> List[str]:
        return [
            "Generate entangled oscillator pair",
            "Increase coherence time >1 s",
            "Scan cavity parameters",
            "Locate entropy minimum",
            "Record invariant phase-noise floor",
        ]

    # --------------------------------------------------

    def specification_sheet(self) -> str:

        optical = self.optical_lattice_clock()
        cavity = self.entanglement_cavity()
        supercon = self.superconducting_loop()

        return f"""
ESQET PRIMARY STANDARD — QCR

Optical Clock:
  Atom: {optical['atom']}
  Stability: {optical['stability']:.0e}

Entanglement Cavity:
  Length: {cavity['length_m']} m
  Squeezing: {cavity['squeezing_db']:.2f} dB

Superconducting Loop:
  Material: {supercon['material']}
  Tc: {supercon['Tc_K']} K
"""

# --------------------------------------------------

if __name__ == "__main__":

    qcr = ESQETPrimaryStandard()

    print(qcr.specification_sheet())

    print("\nCoherence Limit:")
    print(qcr.compute_theoretical_coherence_limit())
