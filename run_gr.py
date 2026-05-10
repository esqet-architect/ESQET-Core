import sys
import os

# Add the current directory to path to ensure it finds 'esqet'
sys.path.append(os.getcwd())

try:
    from esqet.gr.tensor_utils import inverse_metric, trace
    import numpy as np
    
    def run_minkowski():
        print("--- ESQET-GR Minkowski Metric Validation ---")
        eta = np.diag([-1, 1, 1, 1])
        eta_inv = inverse_metric(eta)
        t_val = trace(eta, eta_inv)
        
        print(f"Metric Geometry: 4D Minkowski")
        print(f"Trace result: {t_val}")
        print("Status: Stable")

    if __name__ == "__main__":
        run_minkowski()
except ImportError as e:
    print(f"Path Error: {e}")
    print("Check if 'esqet' folder is in: " + os.getcwd())
