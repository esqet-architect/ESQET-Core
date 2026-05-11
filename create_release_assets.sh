#!/bin/bash
# Create release assets for GitHub

RELEASE_DIR="esqet-release-v2.3"
mkdir -p $RELEASE_DIR

# Copy core files
cp whitepaper/esqet_whitepaper.pdf $RELEASE_DIR/
cp whitepaper/esqet_whitepaper.tex $RELEASE_DIR/

# Copy axiom papers
for i in 2 3 4 5; do
    cp zenodo/axiom$i/axiom${i}_esqet.tar.gz $RELEASE_DIR/
done

# Create citation file
cat > $RELEASE_DIR/CITATION.cff << 'CFF'
cff-version: 1.2.0
title: ESQET Framework
message: If you use ESQET in your research, please cite this software.
type: software
authors:
  - name: "Rocha Jr., Marco Antônio"
    orcid: "https://orcid.org/0009-0004-9757-2853"
repository-code: "https://github.com/esqet-architect/ESQET-Core"
doi: "10.5281/zenodo.20072372"
version: 2.3
date-released: 2026-05-10
license: MIT
CFF

# Create release archive
tar -czf esqet-v2.3-release.tar.gz $RELEASE_DIR/
echo "✅ Release asset created: esqet-v2.3-release.tar.gz"
