#!/bin/bash
# Quick launcher for interactive CLI converter

cd "$(dirname "$0")"

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║    Pandaforge Profile Converter - Interactive CLI                   ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Internal tool with automatic path configuration"
echo ""

python3 convert_interactive.py
