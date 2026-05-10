import numpy as np

class Tensor:
    def __init__(self, data):
        self.data = np.array(data, dtype=float)

    @property
    def rank(self):
        return self.data.ndim

    def contract(self, a1, a2):
        return Tensor(np.trace(self.data, axis1=a1, axis2=a2))

    def __repr__(self):
        return f"Tensor(rank={self.rank}, shape={self.data.shape})"
