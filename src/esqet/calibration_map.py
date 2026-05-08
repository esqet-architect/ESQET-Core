import numpy as np

def axiom_to_observable(dimensionless_ratios, lambda_scale=0.51099895):
    """
    Projects Axiomatic Space (Ratios) into Observable Space (MeV).
    Lambda_scale is the physical anchor (Electron Mass).
    """
    return {k: v * lambda_scale for k, v in dimensionless_ratios.items()}

# Core SM Data for Reference
SM_DATA = {
    "electron": 0.51099895,
    "muon": 105.658375,
    "tau": 1776.86
}
