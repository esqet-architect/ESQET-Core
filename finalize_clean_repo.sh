#!/bin/bash
set -e

cd ~/ESQET-CLEAN
git restore --staged commit_esqet_clean.sh 2>/dev/null || true
rm -f commit_esqet_clean.sh
git status
