#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def beta(t, g):
    return 1 + (1/g) - g

phi = (1 + np.sqrt(5)) / 2
t_span = (0, 10)
t_eval = np.linspace(0, 10, 1000)
initial_conditions = [0.5, 1.0, 2.0, 3.0]

plt.figure(figsize=(10, 6))
for g0 in initial_conditions:
    sol = solve_ivp(beta, t_span, [g0], t_eval=t_eval)
    plt.plot(sol.t, sol.y[0], label=f'g0={g0}')

plt.axhline(phi, color='red', ls='--', label='Fixed Point (phi)')
plt.title("Continuous RG Flow of the ESQET Vacuum")
plt.xlabel("ln(s) [Scale]")
plt.ylabel("g(s) [Ratio]")
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('simulations/continuous_rg_flow.png')
print(f"Successfully converged to phi: {sol.y[0][-1]:.6f}")
