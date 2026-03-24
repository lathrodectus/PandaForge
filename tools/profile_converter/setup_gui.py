#!/usr/bin/env python3
"""
Profile Converter GUI - Installation Check and Setup

Checks for tkinter availability and provides installation instructions if needed.
"""

import sys
import subprocess
from pathlib import Path


def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter
        return True
    except ImportError:
        return False


def print_installation_instructions():
    """Print installation instructions for tkinter"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║         Pandaforge Profile Converter GUI - Setup Required            ║
╚══════════════════════════════════════════════════════════════════════╝

❌ tkinter is not available with your current Python installation.

INSTALLATION OPTIONS:

macOS:
------
Option 1 (Recommended): Install Python from python.org
  1. Download from: https://www.python.org/downloads/
  2. Install the .pkg file
  3. Run: /usr/local/bin/python3 profile_converter_gui.py

Option 2: Install python-tk via Homebrew
  brew install python-tk@3.12
  python3.12 profile_converter_gui.py

Linux (Ubuntu/Debian):
----------------------
  sudo apt update
  sudo apt install python3-tk

Linux (Fedora):
---------------
  sudo dnf install python3-tkinter

ALTERNATIVE: Use Command-Line Interface
----------------------------------------
If you prefer not to install tkinter, use the CLI version:

  # Convert single brand
  python3 orca_to_pandaforge.py \\
      ~/OrcaSlicer-main/resources/profiles/Creality \\
      ~/Pandaforge/resources/profiles/Creality \\
      --vendor "Creality"

  # Convert multiple brands
  ./convert_common_printers.sh

See README.md for full CLI documentation.

═══════════════════════════════════════════════════════════════════════
""")


def main():
    """Main entry point"""
    if not check_tkinter():
        print_installation_instructions()
        sys.exit(1)

    # tkinter is available, launch GUI
    print("✓ tkinter available, launching GUI...")

    # Import and run GUI
    try:
        from profile_converter_gui import main as gui_main
        gui_main()
    except Exception as e:
        print(f"\n❌ Error launching GUI: {e}")
        print("\nTry running directly: python3 profile_converter_gui.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
