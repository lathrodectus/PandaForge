# Changelog

Living document tracking recent changes to the Pandaforge project.

## Recent Changes

### March 12, 2026 -- GitHub Setup Complete
- Pushed repository to https://github.com/lathrodectus/PandaForge
- Configured git remotes: `origin` (fork) and `upstream` (BambuStudio)
- Cleaned up temporary worktree branches (9 branches removed)
- Created GitHub workflow documentation (`docs/github-workflow.md`)
- Updated documentation index with GitHub workflow guide
- Repository ready for Phase 1 development

### March 12, 2026 -- Documentation Reorganization
- Consolidated ~30 markdown files into structured `docs/` directory
- Created single-source-of-truth documentation (eliminated ~57% duplication)
- Slimmed CLAUDE.md from ~370 lines to ~120 lines (routing index + critical rules)
- Consolidated 15 profile converter docs into 2 (README.md + FLASHFORGE_EXAMPLE.md)
- Archived historical docs to `docs/archive/`

### March 10, 2026 -- Profile Converter Enhancements
- Added GUI for profile converter (`profile_converter_gui.py`)
- Added interactive CLI (`convert_interactive.py`)
- Added profile validation tool (`validate_profiles.py`)
- Added batch conversion script (`convert_common_printers.sh`)
- Converted Flashforge Adventurer 5M Pro profiles (reference example)

### March 5, 2026 -- Pressure Advance Fix
- **Issue:** Pressure advance settings not being applied to Klipper G-code output
- **Solution:**
  - Added initial pressure advance setup at print start
  - Enhanced Klipper multi-extruder support with EXTRUDER parameter
  - Updated `GCodeWriter::set_pressure_advance()` to accept extruder_id
- **Files Modified:**
  - `src/libslic3r/GCode.cpp`
  - `src/libslic3r/GCodeWriter.cpp`
  - `src/libslic3r/GCodeWriter.hpp`

### March 5, 2026 -- UI Panel Size Fix
- **Issue:** Printer and bed plate selector panels too small for 3rd party printers
- **Solution:** Increased panel size for non-BBL printers (96x68 -> 140x90 pixels)
- **Note:** Layout differences are intentional (BBL=vertical, 3rd party=horizontal)

### March 4-5, 2026 -- Project Foundation
- Built clean BambuStudio v2.5.0.66 using official Mac Compile Guide
- Created build documentation
- Compiled Klipper UI components (BedPlateSelector, NozzleSelector, FanControlPanel)
- Discovered and documented `-j4` deadlock fix

## Project Rename History

The project was renamed from "BambuStudio" to "pandaforge". Files modified:

### Core Configuration
- `version.inc` -- Changed `SLIC3R_APP_NAME` and `SLIC3R_APP_KEY`
- `CMakeLists.txt` (root) -- Changed `project()` name
- `src/CMakeLists.txt` -- Changed target names, `OUTPUT_NAME`, `MACOSX_BUNDLE_BUNDLE_NAME`
- `src/libslic3r/libslic3r.h` -- Changed `SLIC3R_APP_FULL_NAME`, `GCODEVIEWER_APP_NAME`

### Platform-Specific
- `src/platform/osx/Info.plist.in` -- Changed icon refs, bundle identifier (`com.pandaforge.slic3r`), URL scheme

### Source Code
- `src/slic3r/GUI/GUI_App.cpp` -- Updated user-facing strings
- `src/slic3r/GUI/InstanceCheck.cpp` -- Changed "BambuLab" references
- `src/slic3r/GUI/NetworkTestDialog.cpp` -- Changed "BambuLab" references

### What the Rename Achieves
- Separate config directory: `~/.pandaforge/` (not `~/.BambuStudio/`)
- Separate cache: `~/Library/Application Support/pandaforge/`
- Independent settings from BambuStudio
- Branded UI showing "pandaforge"
