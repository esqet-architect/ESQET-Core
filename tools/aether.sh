#!/bin/bash
set -e
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

case $1 in
  "sim")
    echo "🌀 Running Axiomatic Verification..."
    python3 src/esqet/z3_test.py
    python3 src/esqet/axioms/axiom8_unity_check.py
    ;;
  "optimize")
    echo "🧠 Running Parameter Inference (Two-Space)..."
    python3 src/esqet/optimizer.py --sector leptons
    ;;
  "sync")
    git add . && git commit -m "research: state sync" && git push origin main
    ;;
  "publish")
    # Zipping logic here...
    ;;
  *)
    echo "Usage: ./tools/aether.sh {sim|optimize|sync|publish}"
    exit 1
    ;;
esac
