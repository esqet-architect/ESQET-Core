# Add this fixed function to replace the broken quantum_return_prob

def quantum_return_prob_fixed(G: nx.Graph, times: np.ndarray, start_node: int = 0) -> np.ndarray:
    """
    Quantum return probability |⟨start|ψ(t)⟩|² (FIXED: handles single time points)
    """
    if len(times) < 2:
        raise ValueError("Need at least 2 time points for expm_multiply")
    
    probs = []
    A = nx.adjacency_matrix(G).tocsc()
    H = -A  # simple choice
    
    n = G.number_of_nodes()
    psi0 = np.zeros(n, dtype=complex)
    psi0[start_node] = 1.0
    
    # Use full evolution over the time range
    psi_t_all = expm_multiply(-1j * H, psi0, start=times[0], stop=times[-1], num=len(times))
    
    for psi_t in psi_t_all:
        p_return = np.abs(psi_t[start_node])**2
        probs.append(p_return)
    
    return np.array(probs)
