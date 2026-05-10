import numpy as np

def riemann(Gamma, dGamma):

    R = np.zeros((4,4,4,4))

    for rho in range(4):
        for sigma in range(4):
            for mu in range(4):
                for nu in range(4):

                    R[rho,sigma,mu,nu] = (
                        dGamma[rho,nu,sigma,mu]
                        - dGamma[rho,mu,sigma,nu]
                    )

                    for lam in range(4):
                        R[rho,sigma,mu,nu] += (
                            Gamma[rho,mu,lam]*Gamma[lam,nu,sigma]
                            - Gamma[rho,nu,lam]*Gamma[lam,mu,sigma]
                        )

    return R

def ricci(R):
    return np.einsum("rsmr->sm", R)

def scalar(Ricci, ginv):
    return np.einsum("ab,ab", ginv, Ricci)
