#!/bin/bash

echo "=== Configuring Local Git Repository ==="

# 1. Configure local repository identity
git config --local user.email "marco.antonio.rocha.jr@gmail.com"
git config --local user.name "Marco Antônio Rocha Jr."
echo "✓ Local Git identity set."

# 2. Update remote origin to your actual repository
# Replace this with your specific GitHub username and repo if different
REAL_REMOTE="https://github.com/marcorochajr/Minerva-dea-mathematica.git"
git remote set-url origin "$REAL_REMOTE"
echo "✓ Remote origin updated to: $REAL_REMOTE"

# 3. Stage all active assets
git add README.md esqet_canonical_verification.py .github/workflows/verify.yml
echo "✓ Project files staged."

# 4. Execute the initial local commit
git commit -m "Optimize landscape routine and add automated verification pipeline"

echo "========================================="
echo "Local repository ready! Run this next to push:"
echo "git push -u origin main"
echo "========================================="
