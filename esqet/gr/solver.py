import numpy as np

class EinsteinSolver:

    def __init__(self, Lambda=0.0):
        self.Lambda = Lambda

    def residual(self, G, metric, T):
        lhs = G + self.Lambda * metric.g
        rhs = 8*np.pi*T
        return lhs - rhs

    def vacuum_error(self, G):
        return np.max(np.abs(G))
