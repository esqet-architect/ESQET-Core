#!/bin/bash
# Lock to Performance Cores (4-7) for the Exynos 1380
echo "[+] Locking to Cortex-A78 Performance Cores..."
taskset -c 4-7 python3 test_field.py
