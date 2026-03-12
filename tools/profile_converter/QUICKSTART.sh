#!/bin/bash
# Quick Start Guide for Profile Converter
# Run this script to see usage examples

cat << 'EOF'
╔══════════════════════════════════════════════════════════════════════╗
║              PROFILE CONVERTER - QUICK START                         ║
╚══════════════════════════════════════════════════════════════════════╝

📍 You are here: tools/profile_converter/

🎯 MOST COMMON USE CASE:

   Convert Creality K1 Max profiles:

   python3 orca_to_pandaforge.py \
       ~/Pandaforge\ Project/OrcaSlicer-main/resources/profiles/Creality \
       ~/Pandaforge\ Project/BambuStudio-2.5.0.66/resources/profiles/Creality \
       --vendor "Creality"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 STEP-BY-STEP WORKFLOW:

   1️⃣  Convert profiles:
       python3 orca_to_pandaforge.py <orca_dir> <output_dir> --vendor <name>

   2️⃣  Validate conversion:
       python3 validate_profiles.py <output_dir>

   3️⃣  Test in Pandaforge:
       - Open Pandaforge
       - Select converted printer
       - Slice a test model
       - Check G-code output

   4️⃣  Tune settings:
       - Adjust pressure advance values
       - Test print calibration cube
       - Fine-tune speeds if needed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 POPULAR PRINTERS:

   Creality K1 Max:
   python3 orca_to_pandaforge.py \
       ~/Pandaforge\ Project/OrcaSlicer-main/resources/profiles/Creality \
       ~/Pandaforge\ Project/BambuStudio-2.5.0.66/resources/profiles/Creality \
       --vendor "Creality"

   Voron 2.4:
   python3 orca_to_pandaforge.py \
       ~/Pandaforge\ Project/OrcaSlicer-main/resources/profiles/Voron \
       ~/Pandaforge\ Project/BambuStudio-2.5.0.66/resources/profiles/Voron \
       --vendor "Voron"

   Prusa MK4 (Klipper):
   python3 orca_to_pandaforge.py \
       ~/Pandaforge\ Project/OrcaSlicer-main/resources/profiles/Prusa \
       ~/Pandaforge\ Project/BambuStudio-2.5.0.66/resources/profiles/Prusa \
       --vendor "Prusa"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 BATCH CONVERSION (Multiple Vendors):

   ./convert_common_printers.sh

   This will convert:
   • Creality (K1, K1 Max, K1C, Ender-3 V3 KE)
   • Voron (2.4, 0.2, Trident, Switchwire)
   • Prusa (MK4, XL with Klipper)
   • BIQU (B1, BX)
   • Qidi (X-Max 3, X-Plus 3)
   • Sovol (SV06, SV07)
   • Anycubic (Kobra series)
   • Elegoo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 DOCUMENTATION:

   Full docs:        cat README.md
   Quick reference:  cat QUICK_REFERENCE.md
   Example:          cat FLASHFORGE_EXAMPLE.md
   Help:             python3 index.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  WHAT GETS CONVERTED:

   ✓ Machine profiles (printer specs, kinematics, G-code)
   ✓ Filament profiles (materials, temps, pressure advance)
   ✓ Process profiles (quality presets, speeds)
   ✓ Assets (images, textures, 3D models)
   ✓ Vendor manifest (JSON)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 VALIDATION:

   After conversion, validate:
   python3 validate_profiles.py <output_dir>

   This checks:
   ✓ Required fields present
   ✓ Klipper settings correct (gcode_flavor, pressure advance)
   ✓ Temperature ranges valid
   ✓ Compatible printers lists accurate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ KLIPPER-SPECIFIC SETTINGS:

   The converter ensures these are set correctly:
   • gcode_flavor: "klipper"
   • enable_pressure_advance: ["1"]
   • pressure_advance: ["0.025"] (tune per filament)
   • machine_max_acceleration_x/y/z
   • machine_max_speed_x/y/z
   • use_relative_e_distances: "1"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 EXAMPLE: Flashforge Adventurer 5M Pro

   The Flashforge AD5M Pro is already converted and serves as reference:

   Location: BambuStudio-2.5.0.66/resources/profiles/Flashforge/

   Features:
   • Klipper firmware
   • Pressure advance enabled
   • High-speed (600mm/s travel, 20000mm/s² accel)
   • Multi-nozzle (0.25, 0.4, 0.6, 0.8mm)

   See FLASHFORGE_EXAMPLE.md for complete breakdown

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🆘 TROUBLESHOOTING:

   Profiles don't appear in Pandaforge:
   → Check vendor JSON is in resources/profiles/
   → Verify instantiation: "true" in profiles

   G-code errors:
   → Verify gcode_flavor: "klipper"
   → Check start/end G-code syntax

   Poor print quality:
   → Tune pressure advance (0.02-0.08 typical)
   → Adjust speeds/accelerations
   → Test with calibration cube

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📞 NEED HELP?

   • Read README.md for complete documentation
   • Check FLASHFORGE_EXAMPLE.md for real-world example
   • Review validation warnings for issues
   • Test with Flashforge profiles first (known working)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ Ready to convert your Klipper printer profiles!

EOF
