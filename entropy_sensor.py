import numpy as np
import time

# ESQET Mobile Constants
DTYPE = np.float32
PHI = DTYPE((1 + 5**0.5) / 2)

def calculate_shannon_entropy(data):
    if not data: return 0
    _, counts = np.unique(list(data), return_counts=True)
    probs = counts / len(data)
    return -np.sum(probs * np.log2(probs))

def run_sensor():
    print(f"[*] ESQET Entropy Sensor Active (Locked to Cores 4-7)")
    print(f"[*] Integration Constant: {PHI:.4f}")
    
    try:
        while True:
            # Simulated data stream (Replace with real logs/traffic later)
            sample_data = np.random.bytes(1024) 
            entropy = calculate_shannon_entropy(sample_data)
            
            # Map entropy to the Master Equation tension
            # F_qc = Entropy / Phi
            tension = entropy / PHI
            
            print(f"\r[S-FIELD] Entropy: {entropy:.4f} | Tension: {tension:.4f}", end="")
            time.sleep(0.1) # 10Hz sampling is easy for the A35
    except KeyboardInterrupt:
        print("\n[!] Sensor Standby.")

if __name__ == "__main__":
    run_sensor()
