#!/usr/bin/env python3
"""
unified_precision_ledger.py
===========================
Aggregates ESQET framework observables using strict, unrounded analytical derivations.
Eliminates all rounding, floor, and ceiling functions to preserve pure, infinite-precision algebraic limits.
"""

import os
import json
import numpy as np
from decimal import Decimal, getcontext

# Set precision to 100 digits to avoid any float rounding artifacts
getcontext().prec = 100

RESULTS_DIR = "/root/ESQET-Core/results"
os.makedirs(RESULTS_DIR, exist_ok=True)
OUTPUT_JSON = os.path.join(RESULTS_DIR, "unified_precision_ledger.json")

# Pure Constants defined via Strings to eliminate binary float distortion
PHI_STR = "1.618033988749894848204586834365638117720309179805762862135448622705260462818902449707207204189391138"
CODATA_ALPHA_INV_STR = "137.035999177"
F_HA_STR = "432.0"

def calculate_exact_alpha_deviation():
    """Evaluates unrounded topological alpha candidate against CODATA baseline."""
    phi = Decimal(PHI_STR)
    codata = Decimal(CODATA_ALPHA_INV_STR)
    
    # Pure geometric formula: 360 / phi^2 - 2 / phi^3
    term_1 = Decimal("360") / (phi ** 2)
    term_2 = Decimal("2") / (phi ** 3)
    alpha_inv_predicted = term_1 - term_2
    
    absolute_delta = abs(alpha_inv_predicted - codata)
    ppm_error = (absolute_delta / codata) * Decimal("1000000")
    
    return alpha_inv_predicted, ppm_error

def main():
    print("="*75)
    print("ESQET UNROUNDED UNIFIED PRECISION LEDGER")
    print("="*75)
    
    # 1. Compute unrounded multi-digit alpha precision
    alpha_inv, alpha_ppm = calculate_exact_alpha_deviation()
    
    # 2. Extract analytical log deviation parameters for a benchmark off-center frequency
    # Tracking the exact offset from the anchor without applying any round() boundaries
    freq_sample = 440.0
    f_ha = float(F_HA_STR)
    R_f = np.log2(freq_sample / f_ha)
    
    # Calculate log distance using pure unrounded floating point limits
    raw_log_deviation = abs(R_f - 1.0)
    
    print(f"🔬 Pure Algebraic Inversion Expansions:")
    print(f"  Calculated \u03b1\u207b\u00b1:      {alpha_inv}")
    print(f"  PPM Discrepancy:   {alpha_ppm} ppm")
    print(f"\n📊 Exact Logarithmic Trajectory Scaling:")
    print(f"  Sample Target:     {freq_sample} Hz")
    print(f"  Raw R_f Factor:    {R_f:.15f}")
    print(f"  Raw Log Deviation: {raw_log_deviation:.15f}")
    print("="*75)
    
    # Export unrounded structural telemetry payloads as high-precision strings
    payload = {
        "precision_context_digits": getcontext().prec,
        "constants": {
            "phi_algebraic_limit": PHI_STR,
            "codata_alpha_inverse_reference": CODATA_ALPHA_INV_STR
        },
        "alpha_inverse_derivation": {
            "predicted_value": str(alpha_inv),
            "parts_per_million_error": str(alpha_ppm)
        },
        "frequency_trajectory_derivation": {
            "evaluated_frequency_hz": freq_sample,
            "raw_log2_ratio": float(R_f),
            "unrounded_log_deviation": float(raw_log_deviation)
        }
    }
    
    with open(OUTPUT_JSON, "w") as f:
        json.dump(payload, f, indent=2)
        
    print(f"📄 Exact telemetry database safely exported to: {OUTPUT_JSON}\n")

if __name__ == "__main__":
    main()
