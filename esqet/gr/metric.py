import numpy as np

class Metric:

    def __init__(self, g):
        self.g = np.array(g, dtype=float)
        self.g_inv = np.linalg.inv(self.g)

def minkowski():
    return Metric(np.diag([-1,1,1,1]))

def schwarzschild(M, r):
    rs = 2*M
    f = 1 - rs/r
    g = np.diag([
        -f,
        1/f,
        r**2,
        r**2
    ])
    return Metric(g)
