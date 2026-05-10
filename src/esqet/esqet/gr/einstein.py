import numpy as np
from .curvature import ricci, scalar

def einstein_tensor(Riemann, metric):

    Ricci = ricci(Riemann)
    R = scalar(Ricci, metric.g_inv)

    G = Ricci - 0.5 * metric.g * R
    return G
