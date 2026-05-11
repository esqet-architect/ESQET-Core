#!/bin/bash
# Lock processes to Cores 4-7
echo "[+] Optimizing for Samsung A35 (Cortex-A78)..."
taskset -c 4-7 python3 auto_investigator.py
