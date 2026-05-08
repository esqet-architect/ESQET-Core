#!/bin/bash
set -e

cd ~/ESQET-CLEAN

git stash push -u -m "temp-before-rebase"
git pull --rebase origin main
git stash pop
git push origin main
