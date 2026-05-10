import numpy as np

def inverse_metric(g):
    """Calculates the inverse metric tensor g^{ab}."""
    return np.linalg.inv(g)

def raise_index(v, g_inv):
    """Raises the index of a vector using the inverse metric."""
    return g_inv @ v

def lower_index(v, g):
    """Lowers the index of a vector using the metric."""
    return g @ v

def trace(T, g_inv):
    """Calculates the trace of a (0,2) tensor T_ab."""
    return np.einsum("ab,ab->", g_inv, T)

if __name__ == "__main__":
    # Quick validation with Minkowski metric
    eta = np.diag([-1, 1, 1, 1])
    eta_inv = inverse_metric(eta)
    print("Minkowski Inverse Metric:")
    print(eta_inv)
    
    t_val = trace(eta, eta_inv)
    print(f"Trace of Minkowski (should be 4): {t_val}")
