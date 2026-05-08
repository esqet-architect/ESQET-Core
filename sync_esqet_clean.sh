#!/bin/bash
set -e

cd ~/ESQET-CLEAN

git pull --rebase origin main
git push origin main
