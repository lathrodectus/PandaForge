╔══════════════════════════════════════════════════════════════════════╗
║                  PROFILE CONVERTER TOOL                              ║
║           OrcaSlicer → Pandaforge (BambuStudio)                      ║
╚══════════════════════════════════════════════════════════════════════╝

📦 WHAT'S IN THIS DIRECTORY:

   TOOLS (7 files):
   • orca_to_pandaforge.py       - Main conversion script
   • validate_profiles.py        - Profile validator
   • convert_common_printers.sh  - Batch converter
   • profile_converter_gui.py    - GUI application (NEW!)
   • menu.py                     - Interactive menu (NEW!)
   • launch_gui.sh               - GUI launcher (NEW!)
   • index.py                    - Help system

   DOCUMENTATION (7 files):
   • README_FIRST.txt            - This file (start here!)
   • QUICKSTART.sh               - Quick start guide
   • GUI_README.md               - GUI documentation (NEW!)
   • README.md                   - Complete documentation
   • QUICK_REFERENCE.md          - Quick reference
   • FLASHFORGE_EXAMPLE.md       - Real-world example
   • SUMMARY.md                  - Tool overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 QUICK START (4 WAYS TO USE):

   METHOD 0: Interactive Menu (Easiest!)
   ─────────────────────────────────────
   python3 menu.py

   • Choose between GUI or CLI modes
   • Guided prompts for all options
   • Built-in documentation viewer
   • Perfect for first-time users

   ═══════════════════════════════════════════════════════════════════

   METHOD 1: Graphical Interface (GUI)
   ───────────────────────────────────
   ./launch_gui.sh

   OR

   python3 profile_converter_gui.py

   Features:
   • Visual brand selection with multi-select
   • Auto-detection of OrcaSlicer profiles
   • Real-time conversion progress
   • Search/filter printer brands
   • One-click batch conversion

   Requirements:
   • Python 3 with tkinter support
   • macOS: brew install python-tk@3.12
   • Linux: sudo apt install python3-tk

   See GUI_README.md for full documentation

   ═══════════════════════════════════════════════════════════════════

   METHOD 2: Quick Script
   ──────────────────────
   ./QUICKSTART.sh

   This interactive script will:
   • Guide you through the conversion process
   • Auto-detect OrcaSlicer installation
   • Convert common Klipper printers
   • Validate the output

   ═══════════════════════════════════════════════════════════════════

   METHOD 3: Convert Single Vendor
   ────────────────────────────────
   python3 orca_to_pandaforge.py \
       ~/OrcaSlicer-main/resources/profiles/Creality \
       ~/Pandaforge\ Project/BambuStudio-2.5.0.66/resources/profiles/Creality \
       --vendor "Creality"

   ═══════════════════════════════════════════════════════════════════

   METHOD 4: Batch Convert Multiple Vendors
   ─────────────────────────────────────────
   ./convert_common_printers.sh

   Converts common Klipper printers:
   • Creality (K1, K1 Max, K1C)
   • Voron (2.4, 0.2, Trident)
   • And more...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 DOCUMENTATION GUIDE:

   START HERE:
   1. python3 menu.py           - Interactive menu (easiest!)
   2. GUI_README.md             - GUI documentation
   3. ./QUICKSTART.sh           - Quick start script
   4. README.md                 - Full documentation
   5. FLASHFORGE_EXAMPLE.md     - Real example (Flashforge AD5M Pro)

   REFERENCE:
   6. QUICK_REFERENCE.md        - Commands and settings
   7. python3 index.py          - Interactive help

   DETAILS:
   8. SUMMARY.md                - Tool overview

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ WHAT THIS TOOL DOES:

   Converts Klipper printer profiles from OrcaSlicer to Pandaforge:
   ✓ Machine profiles (printer specs, kinematics, G-code)
   ✓ Filament profiles (materials, temps, pressure advance)
   ✓ Process profiles (quality presets, speeds)
   ✓ Assets (images, textures, 3D models)
   ✓ Vendor manifest (JSON)

   Ensures Klipper-specific settings are preserved:
   ✓ gcode_flavor: "klipper"
   ✓ Pressure advance enabled
   ✓ Kinematics (speeds, accelerations, jerk)
   ✓ Relative E distances

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 SUPPORTED PRINTERS:

   • Creality K1 / K1 Max / K1C
   • Voron 2.4 / 0.2 / Trident
   • Prusa MK4 / XL (Klipper)
   • BIQU B1 / BX
   • Qidi X-Max 3 / X-Plus 3
   • Sovol SV06 / SV07
   • Anycubic Kobra series
   • Flashforge Adventurer 5M Pro
   • And more...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆕 NEW IN THIS VERSION:

   ✨ Graphical User Interface (GUI)
      • Visual brand selection with checkboxes
      • Multi-select for batch conversion
      • Real-time progress logging
      • Auto-detection of OrcaSlicer profiles
      • Search/filter functionality

   ✨ Interactive Menu System
      • Choose between GUI and CLI modes
      • Guided prompts for all operations
      • Built-in documentation viewer

   ✨ Enhanced Launcher Scripts
      • Auto-detect Python with tkinter
      • Helpful error messages
      • Installation instructions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 STATISTICS:

   Total files:  14 (+4 new)
   Total size:   ~150 KB
   Code:         ~2,000 lines (Python + Bash)
   Docs:         ~2,000 lines (Markdown)
   Total lines:  ~4,000 lines

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ TESTED & VALIDATED:

   Flashforge Adventurer 5M Pro profiles:
   • 4 machine profiles (0.25, 0.4, 0.6, 0.8mm nozzles)
   • 18 filament profiles (PLA, PETG, ABS, ASA, TPU)
   • 30 process profiles (quality presets)
   • All Klipper settings verified ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 EXAMPLE REFERENCE:

   The Flashforge Adventurer 5M Pro serves as a complete reference:

   Location: BambuStudio-2.5.0.66/resources/profiles/Flashforge/

   See FLASHFORGE_EXAMPLE.md for detailed breakdown

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 VERSION INFO:

   Version:      1.1 (GUI Edition)
   Date:         2026-03-10
   Status:       Production Ready
   License:      AGPL-3.0 (Pandaforge Project)
   Python:       3.7+
   Dependencies: tkinter (optional, for GUI)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 NEXT STEPS:

   1. Run: python3 menu.py (interactive menu)
      OR
      Run: ./launch_gui.sh (graphical interface)

   2. Read: GUI_README.md (GUI documentation)
      OR
      Read: README.md (CLI documentation)

   3. Convert your printer profiles

   4. Validate with validate_profiles.py

   5. Test in Pandaforge

   6. Tune pressure advance values

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Ready to convert your Klipper printer profiles to Pandaforge!

   TIP: First-time users should run: python3 menu.py
