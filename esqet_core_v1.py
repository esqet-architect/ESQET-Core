import numpy as np
import time
import json
import os

# Configuration
PHI = (1 + 5**0.5) / 2
THRESHOLD = 0.05
LOG_FILE = "cognitive_events.json"

class ESQETCore:
    def __init__(self):
        self.last_tension = 4.70
        self.events = []

    def log_event(self, surprise, eta):
        event = {
            "timestamp": time.time(),
            "surprise": float(surprise),
            "eta": float(eta),
            "top_proc": subprocess.getoutput("ps -eo comm --sort=-pcpu | head -n 2 | tail -n 1")
        }
        print(f"\n[EVENT] Surprise Detected! Logging to {LOG_FILE}...")
        self.events.append(event)
        with open(LOG_FILE, "w") as f:
            json.dump(self.events, f, indent=4)

    def run(self):
        import subprocess
        print("[*] ESQET Core V1: Online. Monitoring A78 Cluster...")
        try:
            while True:
                with open("/dev/urandom", "rb") as f:
                    data = f.read(512)
                
                # Math
                _, counts = np.unique(list(data), return_counts=True)
                entropy = -np.sum((counts/len(data)) * np.log2(counts/len(data)))
                tension = entropy / PHI
                surprise = abs(tension - self.last_tension)
                
                # Adaptive Eta
                eta = 0.01 * (1 + (surprise * PHI))
                
                if surprise > THRESHOLD:
                    self.log_event(surprise, eta)
                
                print(f"\r[CORE] Tension: {tension:.4f} | η: {eta:.5f} | Events: {len(self.events)}", end="")
                
                self.last_tension = tension
                time.sleep(0.4)
        except KeyboardInterrupt:
            print("\n[!] Core Standby.")

if __name__ == "__main__":
    ESQETCore().run()
