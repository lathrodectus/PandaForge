# Changelog

Living document tracking recent changes to the Pandaforge project.

## Recent Changes

### March 24, 2026 -- Converted Printer Cards Match Bambu Layout In Main Window
- Removed the plater/sidebar special-case layout that rendered non-Bambu printers horizontally, so converted printers now use the same stacked thumbnail-over-name card layout as Bambu printers in the selected-printer panel
- Standardized the selected-printer card sizing in `Plater.cpp` so converted printers use the same panel dimensions as the built-in Bambu profiles instead of the wider third-party card variant
- Fixed the follow-up clipping bug where converted-printer names disappeared in the main window because the stacked card height still depended on the visible Bambu sync button; the selected-printer panels now keep Bambu-height spacing even when that button is hidden
- Fixed the filament-settings plate-temperature UI for converted printers by showing bed-temperature rows according to the active printer model's supported bed types instead of hiding them for every non-Bambu vendor preset

### March 24, 2026 -- AD5X Process Ladder Aligned For MakerWorld Matching
- Expanded the Flashforge AD5X process ladder so the 0.4, 0.6, and 0.8 nozzle variants expose the same major layer-height tiers Pandaforge users are likely to encounter from Bambu X1 and A1 MakerWorld projects
- Reworked AD5X process inheritance so each preset now inherits from the matching AD5M Pro parent instead of faking missing tiers from a smaller subset
- Added missing AD5X 0.4 nozzle quality tiers (`0.08`, `0.12`, `0.16`, `0.20 Strength`, `0.28 Extra Draft`)
- Added missing AD5X 0.6 nozzle tiers (`0.18 Standard`, `0.24 Standard`, `0.30 Strength`, `0.36 Standard`, `0.42 Standard`)
- Added missing AD5X 0.8 nozzle tiers (`0.24 Standard`, `0.32 Standard`, `0.48 Standard`, `0.56 Standard`)
- Cleaned up AD5X 0.25 nozzle inheritance to use the exact imported parent profiles for `0.10`, `0.12`, and `0.14`
- Updated `Flashforge.json` so Pandaforge loads the expanded AD5X ladder in manifest order

### March 24, 2026 -- Qidi Q2 / X-Plus 4 / X-Max 4 Imported For MakerWorld
- Added a reduced `Qidi.json` vendor manifest for Qidi Q2, Qidi X-Plus 4, and Qidi X-Max 4 only, with the machine, process, and filament files needed for those families
- Switched the Qidi machine models to generic PLA/PETG/ABS/ASA defaults instead of carrying over a large vendor filament tree
- Imported the shared Qidi base machine and process layers required for inheritance, then filled in the missing 0.2, 0.6, and 0.8 nozzle process tiers so each supported nozzle has a complete usable ladder
- Normalized the X-Max 4 process ladder to X1-style tier names (`High Quality`, `Optimal`, `Standard`, `Strength`, `Draft`) while keeping `renamed_from` aliases for the old Qidi `Balanced` names
- Expanded the Qidi Q2 0.4 nozzle ladder with MakerWorld-facing parallel tiers: `0.08mm High Quality`, `0.12mm High Quality`, `0.16mm High Quality`, and `0.20mm Strength`
- Verified the AD5X and Qidi printer/process/filament graphs with focused local QA checks for manifest wiring, inheritance resolution, and expected layer-height coverage
- Restored the Qidi-local `fdm_filament_*` base presets and repointed the user-facing generic Qidi materials to those local parents so default filaments appear in the UI again
- Added explicit wizard thumbnail assets for Qidi Q2, Qidi X-Plus 4, and Qidi X-Max 4, and fixed the Q2 hotend asset path typo
- Fixed the real Qidi bundle load failure by reordering `Qidi.json` so child presets no longer appear before their parents:
  `0.08mm Extra Fine @Qidi Q2` now follows `0.12mm Fine @Qidi Q2`,
  `0.08mm Extra Fine @Qidi XPlus4` now follows `0.12mm Fine @Qidi XPlus4`,
  and each `0.2 nozzle` machine now appears after its `0.4 nozzle` parent
- Added the wizard thumbnails under the filenames the UI actually resolves from `machine_model_list` names:
  `Qidi Q2_thumbnail.png`,
  `Qidi X-Plus 4_thumbnail.png`,
  and `Qidi X-Max 4_thumbnail.png`
- Filled the second asset gap for converted printers by matching both UI lookup paths:
  the setup wizard now has `_thumbnail.png` files for the Flashforge converted models,
  and the profile guide now has `_cover.png` files for the Qidi converted models
- Filled the plater/sidebar preview path as well by adding `resources/images/printer_preview_<model_id>.png` assets for the converted Qidi and Flashforge printers, so the selected-printer thumbnail no longer falls back to the placeholder in the main window

### March 21, 2026 -- Flashforge AD5X Profiles Added
- Added Flashforge AD5X machine model and nozzle variants (0.25, 0.4, 0.6, 0.8)
- Preserved OrcaSlicer-style multi-material behavior for AD5X:
  - `single_extruder_multi_material = 1`
  - toolchange retraction and cut-distance settings
  - prime tower enabled in AD5X process presets
- Made AD5X `change_filament_gcode` explicit with `T[next_extruder]` so Pandaforge uses the custom toolchange path instead of an empty-field fallback
- Added AD5X-specific generic filament presets, including 0.25 nozzle variants
- Added AD5X process presets for 0.25, 0.4, 0.6, and 0.8 nozzle workflows
- Updated `Flashforge.json` vendor manifest to expose the new profiles in Pandaforge
- Added Orca-compatible AD5M/AD5M Pro process aliases so the AD5X process chain resolves through the same parent names Orca uses

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
