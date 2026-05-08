#!/usr/bin/env python3
"""
CRITICAL TEST: Fit e+μ → predict τ (no refitting)
"""
import numpy as np
from scipy.optimize import minimize

PHI = (1 + np.sqrt(5)) / 2
MASSES = {'e': 0.510999, 'mu': 105.658375}

def get_mass(n, p, mu0, r, alpha):
    offset = n - 1
    geom = 1.0 if offset == 0 else PHI ** (offset * p)
    jump = r ** abs(offset)
    theta = 2 * np.pi * n / 3
    z3 = (1.0 + 0.618 * np.cos(theta)) ** alpha
    return mu0 * geom * jump * z3

def loss_em(params):
    """FIT ONLY electron + muon"""
    p, mu0, r, alpha = params
    pred_e = get_mass(0, p, mu0, r, alpha)
    pred_mu = get_mass(1, p, mu0, r, alpha)
    return 0.5*(abs(np.log(pred_e/MASSES['e']))**2 + abs(np.log(pred_mu/MASSES['mu']))**2)

# Optimize e+μ only
result = minimize(loss_em, [8.0, 105.0, 0.4, -1.0], bounds=[(2,15),(70,130),(0.1,2),(-2,2)])
p_opt, mu0_opt, r_opt, alpha_opt = result.x

# PREDICT tau (NO refit)
tau_pred = get_mass(2, p_opt, mu0_opt, r_opt, alpha_opt)
tau_actual = 1776.86

print(f"e+μ FIT → τ PREDICTION")
print(f"p={p_opt:.6f}, μ₀={mu0_opt:.1f}, r={r_opt:.4f}, α={alpha_opt:.4f}")
print(f"τ_pred = {tau_pred:.1f} MeV")
print(f"τ_actual= {tau_actual:.1f} MeV") 
print(f"Error = {abs(tau_pred-tau_actual)/tau_actual*100:.2f}%")
