#!/usr/bin/env python3
"""
Profile Converter - Quick Start Menu

Provides a simple text menu to choose between GUI and CLI modes.
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


def print_menu():
    """Print the main menu"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║         Pandaforge Profile Converter                                 ║
║         OrcaSlicer → Pandaforge Profile Conversion Tool              ║
╚══════════════════════════════════════════════════════════════════════╝

Choose an option:

  [1] Launch GUI (Graphical Interface)
  [2] CLI - Convert Single Brand
  [3] CLI - Convert Multiple Brands (Batch)
  [4] Validate Converted Profiles
  [5] View Documentation
  [6] Exit

""")


def launch_gui():
    """Launch the GUI"""
    if not check_tkinter():
        print("\n❌ tkinter is not available")
        print("\nInstallation instructions:")
        print("  macOS: brew install python-tk@3.12")
        print("  Linux: sudo apt install python3-tk")
        print("\nPress Enter to return to menu...")
        input()
        return

    print("\n✓ Launching GUI...")
    try:
        import profile_converter_gui
        profile_converter_gui.main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPress Enter to return to menu...")
        input()


def cli_single_brand():
    """Run CLI for single brand conversion"""
    print("\n" + "="*70)
    print("Convert Single Brand")
    print("="*70)

    orca_dir = input("\nOrcaSlicer profile directory: ").strip()
    if not orca_dir:
        print("Cancelled.")
        return

    output_dir = input("Output directory: ").strip()
    if not output_dir:
        print("Cancelled.")
        return

    vendor = input("Vendor name (e.g., Creality, Voron): ").strip()
    if not vendor:
        print("Cancelled.")
        return

    print(f"\nConverting {vendor}...")
    cmd = [
        "python3", "orca_to_pandaforge.py",
        orca_dir, output_dir,
        "--vendor", vendor
    ]

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Conversion complete!")
    except subprocess.CalledProcessError:
        print("\n❌ Conversion failed")
    except FileNotFoundError:
        print("\n❌ orca_to_pandaforge.py not found")

    print("\nPress Enter to return to menu...")
    input()


def cli_batch():
    """Run batch conversion script"""
    print("\n" + "="*70)
    print("Batch Convert Multiple Brands")
    print("="*70)
    print("\nThis will run the batch conversion script.")
    print("Edit convert_common_printers.sh to customize brands.\n")

    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        return

    try:
        subprocess.run(["./convert_common_printers.sh"], check=True)
        print("\n✅ Batch conversion complete!")
    except subprocess.CalledProcessError:
        print("\n❌ Batch conversion failed")
    except FileNotFoundError:
        print("\n❌ convert_common_printers.sh not found")

    print("\nPress Enter to return to menu...")
    input()


def validate_profiles():
    """Run profile validation"""
    print("\n" + "="*70)
    print("Validate Converted Profiles")
    print("="*70)

    profile_dir = input("\nProfile directory to validate: ").strip()
    if not profile_dir:
        print("Cancelled.")
        return

    print(f"\nValidating {profile_dir}...")
    cmd = ["python3", "validate_profiles.py", profile_dir]

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Validation complete!")
    except subprocess.CalledProcessError:
        print("\n❌ Validation failed")
    except FileNotFoundError:
        print("\n❌ validate_profiles.py not found")

    print("\nPress Enter to return to menu...")
    input()


def view_docs():
    """View documentation"""
    print("\n" + "="*70)
    print("Documentation")
    print("="*70)
    print("""
Available documentation files:

  README.md              - Complete CLI documentation
  GUI_README.md          - GUI usage guide
  QUICK_REFERENCE.md     - Quick start guide
  FLASHFORGE_EXAMPLE.md  - Detailed profile example
  SUMMARY.md             - Tool overview

To view a file:
  cat <filename>

Or open in your editor:
  open <filename>
""")

    print("\nPress Enter to return to menu...")
    input()


def main():
    """Main menu loop"""
    while True:
        # Clear screen (works on Unix-like systems)
        print("\033[2J\033[H", end="")

        print_menu()

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            launch_gui()
        elif choice == "2":
            cli_single_brand()
        elif choice == "3":
            cli_batch()
        elif choice == "4":
            validate_profiles()
        elif choice == "5":
            view_docs()
        elif choice == "6":
            print("\nGoodbye!")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Press Enter to try again...")
            input()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")
        sys.exit(0)
