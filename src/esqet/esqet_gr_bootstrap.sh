#!/usr/bin/env bash
set -e

echo "=================================="
echo " ESQET GR ENGINE BOOTSTRAP"
echo "=================================="

########################################
# SAFE PYTHON ENV (PEP 668 FIX)
########################################

if [ ! -d ".venv" ]; then
    echo "[+] Creating virtual environment"
    python3 -m venv .venv
fi

source .venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install numpy scipy

########################################
# DIRECTORY STRUCTURE
########################################

mkdir -p esqet/gr
mkdir -p esqet/apps/cli

########################################
# TENSOR CORE
########################################

cat > esqet/gr/tensor.py <<'PY'
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
PY

########################################
# METRIC
########################################

cat > esqet/gr/metric.py <<'PY'
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
PY

########################################
# CHRISTOFFEL SYMBOLS
########################################

cat > esqet/gr/connections.py <<'PY'
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
PY

########################################
# CURVATURE ENGINE
########################################

cat > esqet/gr/curvature.py <<'PY'
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
PY

########################################
# EINSTEIN TENSOR
########################################

cat > esqet/gr/einstein.py <<'PY'
import numpy as np
from .curvature import ricci, scalar

def einstein_tensor(Riemann, metric):

    Ricci = ricci(Riemann)
    R = scalar(Ricci, metric.g_inv)

    G = Ricci - 0.5 * metric.g * R
    return G
PY

########################################
# GEODESIC ENGINE
########################################

cat > esqet/gr/geodesic.py <<'PY'
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
PY

########################################
# EINSTEIN SOLVER
########################################

cat > esqet/gr/solver.py <<'PY'
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
PY

########################################
# CLI TOOL
########################################

cat > esqet/apps/cli/gr_cli.py <<'PY'
import argparse
from esqet.gr.metric import minkowski

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--metric", default="minkowski")
    args = parser.parse_args()

    if args.metric == "minkowski":
        g = minkowski()

    print("Metric tensor:")
    print(g.g)
PY

########################################
# REGISTER ENTRYPOINT
########################################

if ! grep -q "esqet-gr" pyproject.toml; then
cat >> pyproject.toml <<'TOML'

[project.scripts]
esqet-gr = "esqet.apps.cli.gr_cli:main"
TOML
fi

########################################
# INSTALL PACKAGE
########################################

pip install -e .

echo ""
echo "=================================="
echo " ESQET GR ENGINE INSTALLED ✓"
echo "=================================="
echo "Activate with:"
echo "   source .venv/bin/activate"
echo ""
echo "Run:"
echo "   esqet-gr --metric minkowski"
echo ""
