#!/usr/bin/env python3
"""
Profile Converter Tool - Index and Help

Quick access to all profile converter documentation and tools.
"""

import sys
from pathlib import Path


def print_help():
    """Print help information"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║         OrcaSlicer to Pandaforge Profile Converter                   ║
║                     Version 1.0 - 2026-03-10                         ║
╚══════════════════════════════════════════════════════════════════════╝

TOOLS:
  orca_to_pandaforge.py       Main conversion script
  validate_profiles.py        Profile validator
  convert_common_printers.sh  Batch conversion for common printers

DOCUMENTATION:
  README.md                   Complete documentation
  QUICK_REFERENCE.md          Quick start guide
  FLASHFORGE_EXAMPLE.md       Detailed example (AD5M Pro)
  SUMMARY.md                  Tool overview

QUICK START:
  # Convert single vendor
  python3 orca_to_pandaforge.py \\
      ~/OrcaSlicer-main/resources/profiles/Creality \\
      ~/Pandaforge/resources/profiles/Creality \\
      --vendor "Creality"

  # Validate converted profiles
  python3 validate_profiles.py \\
      ~/Pandaforge/resources/profiles/Creality

  # Convert multiple vendors
  ./convert_common_printers.sh

COMMON KLIPPER PRINTERS:
  • Creality K1 / K1 Max / K1C
  • Voron 2.4 / 0.2 / Trident
  • Prusa MK4 / XL (Klipper mod)
  • BIQU B1 / BX
  • Qidi X-Max 3 / X-Plus 3
  • Sovol SV06 / SV07
  • Anycubic Kobra series

PROFILE STRUCTURE:
  Vendor/
  ├── Vendor.json              # Manifest
  ├── machine/                 # Printer profiles
  │   ├── fdm_vendor_common.json
  │   └── Printer 0.4 Nozzle.json
  ├── filament/                # Material profiles
  │   ├── fdm_filament_pla.json
  │   └── Generic PLA.json
  └── process/                 # Quality presets
      ├── fdm_process_common.json
      └── 0.20mm Standard.json

KLIPPER-SPECIFIC SETTINGS:
  ✓ gcode_flavor: "klipper"
  ✓ enable_pressure_advance: ["1"]
  ✓ pressure_advance: ["0.025"]
  ✓ machine_max_acceleration_x/y/z
  ✓ machine_max_speed_x/y/z
  ✓ use_relative_e_distances: "1"

POST-CONVERSION STEPS:
  1. Review converted profiles
  2. Test with actual printer
  3. Tune pressure advance values
  4. Update G-code templates
  5. Verify speeds/accelerations

HELP & SUPPORT:
  • Full docs: cat README.md
  • Quick ref: cat QUICK_REFERENCE.md
  • Example: cat FLASHFORGE_EXAMPLE.md
  • Issues: Check validation warnings

REFERENCES:
  • OrcaSlicer: github.com/SoftFever/OrcaSlicer
  • Klipper: klipper3d.org
  • Pandaforge: ../../../CLAUDE.md

═══════════════════════════════════════════════════════════════════════
For detailed help on a specific tool, run:
  python3 <tool_name> --help
═══════════════════════════════════════════════════════════════════════
""")


def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        print_help()
    else:
        print_help()


if __name__ == "__main__":
    main()
