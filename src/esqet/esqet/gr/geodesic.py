import numpy as np

def geodesic_rhs(state, Gamma):

    x = state[:4]
    v = state[4:]

    a = np.zeros(4)

    for mu in range(4):
        for a1 in range(4):
            for a2 in range(4):
                a[mu] -= Gamma[mu,a1,a2]*v[a1]*v[a2]

    return np.concatenate([v, a])
