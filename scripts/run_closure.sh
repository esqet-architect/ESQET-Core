#!/bin/bash
# ESQET Closure Analysis - Master Runner

echo "=============================================="
echo "ESQET CLOSURE ANALYSIS - MASTER RUNNER"
echo "=============================================="

cd ~/ESQET-CLEAN
source venv/bin/activate

echo ""
echo "1. Running Closure Engine..."
python esqet/core/closure_engine.py

echo ""
echo "2. Generating φ-Cantor Dust visualization..."
python esqet/fractals/cantor_dust.py

echo ""
echo "3. Running RG Flow with Drag..."
python esqet/rg/flow_engine.py

echo ""
echo "4. Running Information Sweep..."
python esqet/simulations/information_sweep.py

echo ""
echo "=============================================="
echo "All analyses complete!"
echo "Output files:"
echo "  - closure_descent_curve.png"
echo "  - phi_cantor_dust.png"
echo "  - rg_flow_with_drag.png"
echo "  - information_scaling.png"
echo "=============================================="
