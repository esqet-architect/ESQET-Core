import numpy as np
import time

# ESQET Adaptive Parameters
BASE_LEARNING_RATE = 0.01
PHI = (1 + 5**0.5) / 2

def calculate_dynamic_eta(surprise):
    """
    Adjusts the learning rate based on environmental surprise.
    High Surprise = Faster Adaptation (High Eta)
    """
    # Scaling factor: Eta = Base * (1 + Surprise * Phi)
    eta = BASE_LEARNING_RATE * (1 + (surprise * PHI))
    return np.clip(eta, 0.01, 0.5)

def run_bridge():
    print("[*] ESQET Cognitive Bridge: Initializing Dynamic Learning Rate")
    last_tension = 4.70 # Your calibrated idle baseline
    
    try:
        while True:
            # Simulate a live tension reading from urandom
            with open("/dev/urandom", "rb") as f:
                data = f.read(512)
            
            _, counts = np.unique(list(data), return_counts=True)
            entropy = -np.sum((counts/512) * np.log2(counts/512))
            current_tension = entropy / PHI
            
            surprise = abs(current_tension - last_tension)
            eta = calculate_dynamic_eta(surprise)
            
            status = "ADAPTING" if surprise > 0.05 else "REFINING"
            
            print(f"\r[{status}] Δ: {surprise:.4f} | Learning Rate (η): {eta:.5f}", end="")
            
            last_tension = current_tension
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[!] Bridge Standby.")

if __name__ == "__main__":
    run_bridge()
