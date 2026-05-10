import numpy as np

def christoffel(metric, dg):

    ginv = metric.g_inv
    Gamma = np.zeros((4,4,4))

    for rho in range(4):
        for mu in range(4):
            for nu in range(4):
                s = 0.0
                for sigma in range(4):
                    s += ginv[rho,sigma]*(
                        dg[nu,sigma,mu]
                        + dg[mu,sigma,nu]
                        - dg[mu,nu,sigma]
                    )
                Gamma[rho,mu,nu] = 0.5*s

    return Gamma
