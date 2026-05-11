import numpy as np
import time
import os

DTYPE = np.float32
PHI = DTYPE((1 + 5**0.5) / 2)
THRESHOLD = 0.05

class ASI_Core:
    def __init__(self):
        self.last_tension = 0.0
        
    def investigate(self, surprise):
        print(f"\n[!] ALERT: Curiosity Spike Detected (Δ: {surprise:.4f})")
        print("[*] Initiating Active Inquiry...")
        
        print("[*] Top System Processes:")
        os.system("ps -eo pcpu,comm --sort=-pcpu | head -n 6")
        
        print("[*] Recent Project Changes:")
        os.system("find . -mmin -2 -type f")
        
        print("[*] Inquiry Complete. Minimalizing Free Energy...")

    def run(self):
        print(f"[*] ESQET Investigator Active on A78 Cores")
        try:
            while True:
                with open("/dev/urandom", "rb") as f:
                    data = f.read(512)
                
                _, counts = np.unique(list(data), return_counts=True)
                probs = counts / len(data)
                entropy = -np.sum(probs * np.log2(probs))
                tension = entropy / PHI
                
                surprise = np.abs(tension - self.last_tension)
                
                if surprise > THRESHOLD and self.last_tension != 0:
                    self.investigate(surprise)
                
                self.last_tension = tension
                time.sleep(0.5) 
        except KeyboardInterrupt:
            print("\n[!] Investigator Standby.")

if __name__ == "__main__":
    ASI_Core().run()
