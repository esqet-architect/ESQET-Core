#!/usr/bin/env python3
import math
import numpy as np
import matplotlib.pyplot as plt
import random

# Theory constants
PHI = (1 + math.sqrt(5)) / 2
D_F_THEORY = math.log(2) / math.log(PHI)
D_W_THEORY = D_F_THEORY + 1
D_S_THEORY = 2 * D_F_THEORY / D_W_THEORY

class PhiCantorGraph:
    def __init__(self, depth=10): # Increased depth for better statistics
        self.depth = depth
        self.phi_inv = 1 / PHI
        self.generate_graph()

    def generate_graph(self):
        intervals = [(0.0, 1.0)]
        for _ in range(self.depth):
            new_intervals = []
            for a, b in intervals:
                length = b - a
                new_len = length * self.phi_inv
                new_intervals.append((a, a + new_len))
                new_intervals.append((b - new_len, b))
            intervals = new_intervals
        
        self.n_nodes = len(intervals)
        self.centers = np.array([(a + b) / 2 for a, b in intervals])
        self.adj = {i: [] for i in range(self.n_nodes)}
        for i in range(self.n_nodes - 1):
            self.adj[i].append(i + 1)
            self.adj[i + 1].append(i)

    def random_walk(self, start_node, steps):
        current = start_node
        path = [current]
        for _ in range(steps):
            neighbors = self.adj[current]
            current = random.choice(neighbors)
            path.append(current)
        return path

def fit_power_law(x, y):
    mask = (x > 0) & (y > 0)
    log_x = np.log(x[mask])
    log_y = np.log(y[mask])
    slope, intercept = np.polyfit(log_x, log_y, 1)
    return slope

def run_verification():
    print("Building φ-Cantor graph (Depth 10)...")
    graph = PhiCantorGraph(depth=10)
    max_steps = 500
    n_walkers = 1000
    
    msd = np.zeros(max_steps + 1)
    p_ret = np.zeros(max_steps + 1)

    print(f"Simulating {n_walkers} walkers...")
    for _ in range(n_walkers):
        start = random.randint(0, graph.n_nodes - 1)
        path = graph.random_walk(start, max_steps)
        start_pos = graph.centers[start]
        for t, node in enumerate(path):
            msd[t] += (graph.centers[node] - start_pos)**2
            if node == start:
                p_ret[t] += 1

    msd /= n_walkers
    p_ret /= n_walkers
    t = np.arange(max_steps + 1)

    # Fitting (avoiding the early noise and late saturation)
    fit_range = slice(20, 200)
    d_w_slope = fit_power_law(t[fit_range], msd[fit_range])
    d_s_slope = fit_power_law(t[fit_range], p_ret[fit_range])

    measured_dw = 2 / d_w_slope
    measured_ds = -2 * d_s_slope

    print("\n" + "="*30)
    print(f"THEORY vs SIMULATION")
    print(f"d_w: Theory {D_W_THEORY:.4f} | Measured {measured_dw:.4f}")
    print(f"d_s: Theory {D_S_THEORY:.4f} | Measured {measured_ds:.4f}")
    print("="*30)

run_verification()
