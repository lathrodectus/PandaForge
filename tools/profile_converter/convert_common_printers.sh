#!/bin/bash
# Quick conversion script for common Klipper printers
# Usage: ./convert_common_printers.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORCA_BASE="$HOME/Pandaforge Project/OrcaSlicer-main/resources/profiles"
PANDA_BASE="$HOME/Pandaforge Project/BambuStudio-2.5.0.66/resources/profiles"

echo "=========================================="
echo "Pandaforge Profile Converter"
echo "Converting Common Klipper Printers"
echo "=========================================="
echo ""

# Check if OrcaSlicer profiles exist
if [ ! -d "$ORCA_BASE" ]; then
    echo "❌ Error: OrcaSlicer profiles not found at: $ORCA_BASE"
    echo "Please update ORCA_BASE path in this script"
    exit 1
fi

# Create output directory
mkdir -p "$PANDA_BASE"

# List of common Klipper printer vendors to convert
declare -a vendors=(
    "Creality"
    "Voron"
    "Prusa"
    "Anycubic"
    "BIQU"
    "Qidi"
    "Sovol"
    "Elegoo"
)

echo "Vendors to convert:"
for vendor in "${vendors[@]}"; do
    echo "  - $vendor"
done
echo ""

read -p "Continue with conversion? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Conversion cancelled."
    exit 0
fi

echo ""

# Convert each vendor
for vendor in "${vendors[@]}"; do
    if [ -d "$ORCA_BASE/$vendor" ]; then
        echo "=========================================="
        echo "Converting: $vendor"
        echo "=========================================="

        python3 "$SCRIPT_DIR/orca_to_pandaforge.py" \
            "$ORCA_BASE/$vendor" \
            "$PANDA_BASE/$vendor" \
            --vendor "$vendor"

        echo ""
    else
        echo "⊘ Skipping $vendor (not found in OrcaSlicer profiles)"
        echo ""
    fi
done

echo "=========================================="
echo "✅ Conversion Complete!"
echo "=========================================="
echo ""
echo "Converted profiles are in: $PANDA_BASE"
echo ""
echo "Next steps:"
echo "1. Review converted profiles"
echo "2. Test with actual printer hardware"
echo "3. Adjust pressure advance values"
echo "4. Update G-code templates as needed"
echo ""
