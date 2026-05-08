#!/bin/bash
set -e

cd ~/ESQET-CLEAN

git fetch origin
git rebase origin/main
git push origin main
