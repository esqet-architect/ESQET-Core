#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import math

PHI = (1 + math.sqrt(5)) / 2
L = math.log(PHI)
PHI_INV = 1 / PHI

class PhiRGFlow:
    def __init__(self, alpha=0.618, gamma=PHI_INV):
        self.alpha = alpha
        self.gamma = gamma
        self.L = L

    def beta_function(self, O):
        if O <= 0: return 0.0
        return self.alpha * (O - O**2) * (1 - self.gamma / O)

    def beta_derivative(self, O):
        if O <= 0: return self.alpha * self.gamma
        u, v = (O - O**2), (1 - self.gamma / O)
        up, vp = (1 - 2 * O), (self.gamma / (O**2))
        return self.alpha * (up * v + u * vp)

    def rg_map(self, O):
        return O - self.beta_function(O) * self.L

    def analyze_stability(self):
        print("="*60)
        print("phi-RG FLOW ANALYSIS")
        print("="*60)
        fp_candidates = [0.0, 1.0, self.gamma]
        results = []
        for fp in fp_candidates:
            b_val = self.beta_function(fp)
            b_prime = self.beta_derivative(fp)
            f_prime = 1 - self.L * b_prime
            stability = "attracting" if abs(f_prime) < 1 else "repelling"
            
            print(f"\nFixed Point O* = {fp:.6f}")
            print(f"  f'(O*) = {f_prime:.6f} ({stability})")
            
            if stability == "attracting":
                nu = -math.log(abs(f_prime)) / self.L
                print(f"  Critical exponent nu = {nu:.4f}")
            results.append({"O*": fp, "nu": nu if stability=="attracting" else None})
        return results

if __name__ == "__main__":
    rg = PhiRGFlow()
    rg.analyze_stability()
