#!/bin/bash
# One-command setup and launch script

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║              PANDAFORGE PROFILE CONVERTER v1.1                       ║
║                     One-Command Setup                                ║
╚══════════════════════════════════════════════════════════════════════╝

Checking system...
EOF

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7+"
    exit 1
fi
echo "✓ Python 3 found"

# Check tkinter
if python3 -c "import tkinter" 2>/dev/null; then
    echo "✓ tkinter available (GUI enabled)"
    HAS_GUI=true
else
    echo "⚠️  tkinter not available (GUI disabled)"
    echo "   Install: brew install python-tk@3.12 (macOS)"
    echo "            sudo apt install python3-tk (Linux)"
    HAS_GUI=false
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$HAS_GUI" = true ]; then
    echo "Launching master interface..."
    echo ""
    python3 start.py
else
    echo "Launching text menu (GUI not available)..."
    echo ""
    python3 menu.py
fi
