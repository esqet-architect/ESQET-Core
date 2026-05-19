#!/bin/bash

echo "=== Initializing Advanced Git Control Pipeline ==="

# 1. Update remote target specifically to your Core repository
git remote set-url origin "https://github.com/esqet-architect/ESQET-Core.git"
echo "✓ Remote architecture linked to ESQET-Core."

# 2. Tell Git to cache your token in memory for 3600 seconds (1 hour)
git config --global credential.helper 'cache --timeout=3600'
echo "✓ Credential caching activated (1-hour window)."

echo "=================================================="
echo "Ready to deploy! Run the push command below."
echo "When prompted for your Password, paste your 'ghp_' token."
echo "=================================================="
echo "Command: git push -u origin main"
