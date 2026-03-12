#!/bin/bash
# Quick launcher for Profile Converter GUI - Internal Tool

cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║         Pandaforge Profile Converter - Internal Tool                 ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "This tool converts OrcaSlicer profiles to Pandaforge format."
echo "For internal project use only - paths are automatically configured."
echo ""

# Try to find Python with tkinter support
PYTHON_CMD=""

# Check common Python installations
for cmd in python3 /usr/local/bin/python3 python3.12 python3.11 python3.10; do
    if command -v "$cmd" &> /dev/null; then
        if "$cmd" -c "import tkinter" 2>/dev/null; then
            PYTHON_CMD="$cmd"
            echo "✓ Found Python with tkinter: $cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Error: No Python installation with tkinter found"
    echo ""
    echo "Please install tkinter:"
    echo "  macOS: brew install python-tk@3.12"
    echo "         OR download Python from python.org"
    echo "  Linux: sudo apt install python3-tk"
    echo ""
    echo "Alternatively, use the CLI version:"
    echo "  python3 orca_to_pandaforge.py --help"
    exit 1
fi

echo ""
echo "Launching GUI..."
echo ""

"$PYTHON_CMD" profile_converter_gui.py

echo ""
echo "GUI closed."
