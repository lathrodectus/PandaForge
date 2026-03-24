#!/usr/bin/env python3
"""
Profile Converter - Complete Tool Suite
Quick access to all tools and documentation
"""

import sys
import subprocess
from pathlib import Path


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║              PANDAFORGE PROFILE CONVERTER v1.1                       ║
║              OrcaSlicer → Pandaforge (BambuStudio)                   ║
║                      GUI Edition - 2026-03-10                        ║
╚══════════════════════════════════════════════════════════════════════╝
""")


def print_main_menu():
    print("""
┌──────────────────────────────────────────────────────────────────────┐
│  QUICK START                                                         │
└──────────────────────────────────────────────────────────────────────┘

  [1] 🎨 Launch GUI (Graphical Interface)
      → Visual brand selection, multi-select, real-time progress

  [2] 📋 Interactive Menu (Text-based)
      → Choose GUI/CLI modes, guided workflows

  [3] 🚀 Quick Start Script
      → Auto-detect and convert common printers

  [4] 💻 CLI - Convert Single Brand
      → Command-line conversion for one vendor

  [5] 📦 CLI - Batch Convert Multiple Brands
      → Convert multiple vendors at once

  [6] ✅ Validate Converted Profiles
      → Check converted profiles for errors

┌──────────────────────────────────────────────────────────────────────┐
│  DOCUMENTATION                                                       │
└──────────────────────────────────────────────────────────────────────┘

  [7] 📖 View GUI Documentation
  [8] 📖 View CLI Documentation
  [9] 📖 View Quick Reference
  [10] 📖 View Example (Flashforge AD5M Pro)
  [11] 🎬 View GUI Demo (Visual)

┌──────────────────────────────────────────────────────────────────────┐
│  HELP & INFO                                                         │
└──────────────────────────────────────────────────────────────────────┘

  [12] ℹ️  About This Tool
  [13] 📊 Show Statistics
  [14] 🔧 Check Requirements
  [15] ❌ Exit

""")


def launch_gui():
    """Launch the GUI"""
    print("\n🎨 Launching GUI...")
    try:
        subprocess.run(["./launch_gui.sh"], check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Trying direct launch...")
        try:
            subprocess.run(["python3", "profile_converter_gui.py"], check=True)
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\nMake sure tkinter is installed:")
            print("  macOS: brew install python-tk@3.12")
            print("  Linux: sudo apt install python3-tk")


def launch_menu():
    """Launch interactive menu"""
    print("\n📋 Launching interactive menu...")
    try:
        subprocess.run(["python3", "menu.py"], check=True)
    except Exception as e:
        print(f"❌ Error: {e}")


def launch_quickstart():
    """Launch quickstart script"""
    print("\n🚀 Launching quick start...")
    try:
        subprocess.run(["./QUICKSTART.sh"], check=True)
    except Exception as e:
        print(f"❌ Error: {e}")


def show_doc(filename):
    """Show documentation file"""
    try:
        with open(filename, 'r') as f:
            print(f.read())
        print("\nPress Enter to continue...")
        input()
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        print("Press Enter to continue...")
        input()


def show_about():
    """Show about information"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    ABOUT PROFILE CONVERTER                           ║
╚══════════════════════════════════════════════════════════════════════╝

PURPOSE:
  Convert Klipper printer profiles from OrcaSlicer to Pandaforge format,
  enabling MakerWorld project downloads with preserved print settings.

WHAT IT CONVERTS:
  ✓ Machine profiles (printer specs, kinematics, G-code templates)
  ✓ Filament profiles (materials, temperatures, pressure advance)
  ✓ Process profiles (quality presets, speeds, accelerations)
  ✓ Assets (cover images, buildplate textures, 3D models)
  ✓ Vendor manifest (JSON)

KLIPPER-SPECIFIC SETTINGS:
  ✓ gcode_flavor: "klipper"
  ✓ enable_pressure_advance: ["1"]
  ✓ pressure_advance values
  ✓ machine_max_acceleration_x/y/z
  ✓ machine_max_speed_x/y/z
  ✓ use_relative_e_distances: "1"

SUPPORTED PRINTERS:
  • Creality K1 / K1 Max / K1C
  • Voron 2.4 / 0.2 / Trident
  • Prusa MK4 / XL (Klipper)
  • BIQU B1 / BX
  • Qidi X-Max 3 / X-Plus 3
  • Sovol SV06 / SV07
  • Anycubic Kobra series
  • Flashforge Adventurer 5M Pro
  • And more...

VERSION INFO:
  Version:      1.1 (GUI Edition)
  Date:         2026-03-10
  Status:       Production Ready
  License:      AGPL-3.0 (Pandaforge Project)
  Python:       3.7+
  Dependencies: tkinter (optional, for GUI only)

PROJECT:
  Part of Pandaforge - macOS-native fork of BambuStudio v2.5.0.66
  Enhanced for Klipper 3D printer users

Press Enter to continue...
""")
    input()


def show_stats():
    """Show statistics"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                         STATISTICS                                   ║
╚══════════════════════════════════════════════════════════════════════╝

FILES:
  Total files:       18
  Python scripts:    7
  Bash scripts:      4
  Documentation:     7

CODE:
  Total lines:       ~4,500 lines
  Python code:       ~2,100 lines
  Bash scripts:      ~200 lines
  Documentation:     ~2,200 lines

SIZE:
  Total size:        ~160 KB
  Code:              ~60 KB
  Documentation:     ~100 KB

FEATURES:
  ✓ GUI with multi-select
  ✓ Interactive menu
  ✓ CLI single conversion
  ✓ CLI batch conversion
  ✓ Profile validation
  ✓ Auto-detection
  ✓ Real-time logging
  ✓ Search/filter

TESTED WITH:
  ✓ Flashforge Adventurer 5M Pro
    - 4 machine profiles
    - 18 filament profiles
    - 30 process profiles
    - All Klipper settings verified

Press Enter to continue...
""")
    input()


def check_requirements():
    """Check system requirements"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    SYSTEM REQUIREMENTS CHECK                         ║
╚══════════════════════════════════════════════════════════════════════╝
""")

    # Check Python
    print("Checking Python...")
    try:
        result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
        print(f"  ✓ {result.stdout.strip()}")
    except FileNotFoundError:
        print("  ❌ Python 3 not found")

    # Check tkinter
    print("\nChecking tkinter (for GUI)...")
    try:
        subprocess.run(["python3", "-c", "import tkinter"], check=True, capture_output=True)
        print("  ✓ tkinter available")
    except subprocess.CalledProcessError:
        print("  ❌ tkinter not available")
        print("     Install: brew install python-tk@3.12 (macOS)")
        print("              sudo apt install python3-tk (Linux)")

    # Check OrcaSlicer
    print("\nChecking for OrcaSlicer profiles...")
    orca_paths = [
        Path.home() / "OrcaSlicer-main" / "resources" / "profiles",
        Path.home() / "OrcaSlicer" / "resources" / "profiles",
        Path("/Applications/OrcaSlicer.app/Contents/Resources/profiles"),
    ]
    found = False
    for path in orca_paths:
        if path.exists():
            print(f"  ✓ Found: {path}")
            found = True
            break
    if not found:
        print("  ⚠️  OrcaSlicer profiles not found in common locations")

    # Check Pandaforge
    print("\nChecking for Pandaforge...")
    panda_path = Path.home() / "Pandaforge Project" / "BambuStudio-2.5.0.66"
    if panda_path.exists():
        print(f"  ✓ Found: {panda_path}")
    else:
        print("  ⚠️  Pandaforge not found in default location")

    print("\nPress Enter to continue...")
    input()


def main():
    """Main menu loop"""
    while True:
        print("\033[2J\033[H", end="")  # Clear screen
        print_banner()
        print_main_menu()

        choice = input("Enter choice (1-15): ").strip()

        if choice == "1":
            launch_gui()
        elif choice == "2":
            launch_menu()
        elif choice == "3":
            launch_quickstart()
        elif choice == "4":
            print("\n💻 CLI Single Brand Conversion")
            print("Run: python3 orca_to_pandaforge.py --help")
            print("\nPress Enter to continue...")
            input()
        elif choice == "5":
            print("\n📦 CLI Batch Conversion")
            print("Run: ./convert_common_printers.sh")
            print("\nPress Enter to continue...")
            input()
        elif choice == "6":
            print("\n✅ Profile Validation")
            print("Run: python3 validate_profiles.py <profile_dir>")
            print("\nPress Enter to continue...")
            input()
        elif choice == "7":
            show_doc("GUI_README.md")
        elif choice == "8":
            show_doc("README.md")
        elif choice == "9":
            show_doc("QUICK_REFERENCE.md")
        elif choice == "10":
            show_doc("FLASHFORGE_EXAMPLE.md")
        elif choice == "11":
            try:
                subprocess.run(["./GUI_DEMO.sh"], check=True)
            except:
                show_doc("GUI_DEMO.sh")
        elif choice == "12":
            show_about()
        elif choice == "13":
            show_stats()
        elif choice == "14":
            check_requirements()
        elif choice == "15":
            print("\n✨ Goodbye!\n")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Press Enter to try again...")
            input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✨ Goodbye!\n")
        sys.exit(0)
