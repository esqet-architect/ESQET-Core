#!/bin/bash
# Zenodo submission helper

echo "=========================================="
echo "ESQET ZENODO SUBMISSION HELPER"
echo "=========================================="
echo ""
echo "Files ready for upload:"
echo "  1. zenodo/axiom2/axiom2_esqet.tar.gz"
echo "  2. zenodo/axiom3/axiom3_esqet.tar.gz"
echo "  3. zenodo/axiom4/axiom4_esqet.tar.gz"
echo "  4. zenodo/axiom5/axiom5_esqet.tar.gz"
echo ""
echo "SHA256 checksums:"
sha256sum zenodo/axiom*/axiom*_esqet.tar.gz 2>/dev/null
echo ""
echo "Next steps:"
echo "  1. Visit https://zenodo.org"
echo "  2. Upload each tarball"
echo "  3. Copy metadata from respective metadata.json"
echo "  4. Publish and record DOIs"
echo "=========================================="
