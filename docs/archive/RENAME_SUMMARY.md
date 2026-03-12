# Project Rename: BambuStudio → pandaforge

## Summary of Changes

The following files were modified to rename the project from "BambuStudio" to "pandaforge":

### 1. Core Configuration Files

#### `version.inc`
- Changed `SLIC3R_APP_NAME` from "BambuStudio" to "pandaforge"
- Changed `SLIC3R_APP_KEY` from "BambuStudio" to "pandaforge"

#### `CMakeLists.txt` (root)
- Changed `project(BambuStudio)` to `project(pandaforge)`
- Updated all references to BambuStudio in comments and paths

#### `src/CMakeLists.txt`
- Changed all target names from `BambuStudio` to `pandaforge`
- Changed `project(BambuStudio-native)` to `project(pandaforge-native)`
- Updated `OUTPUT_NAME` from "bambu-studio" to "pandaforge"
- Updated `MACOSX_BUNDLE_BUNDLE_NAME` from "Bambu Studio" to "pandaforge"
- Updated all install paths and resource directories

#### `src/libslic3r/libslic3r.h`
- Changed `SLIC3R_APP_FULL_NAME` from "Bambu Studio" to "pandaforge"
- Changed `GCODEVIEWER_APP_NAME` from "BambuStudio G-code Viewer" to "pandaforge G-code Viewer"
- Changed `GCODEVIEWER_APP_KEY` from "BambuStudioGcodeViewer" to "pandaforgeGcodeViewer"
- Updated `GCODEVIEWER_BUILD_ID` accordingly

### 2. Platform-Specific Files

#### `src/platform/osx/Info.plist.in`
- Changed icon file references from `BambuStudio.icns` to `pandaforge.icns`
- Changed bundle identifier from `com.bbl.slic3r` to `com.pandaforge.slic3r`
- Changed URL scheme from `bambustudioopen` to `pandaforgeopen`

### 3. Source Code Files

#### `src/slic3r/GUI/GUI_App.cpp`
- Updated all user-facing strings from "BambuStudio" to "pandaforge"
- Updated error messages, dialog titles, and log messages

#### `src/slic3r/GUI/InstanceCheck.cpp`
- Changed "BambuLab" references to "pandaforge"

#### `src/slic3r/GUI/NetworkTestDialog.cpp`
- Changed "BambuLab" references to "pandaforge"

#### `src/slic3r/GUI/DeviceTab/CMakeLists.txt`
- Updated comment referencing BambuStudio

### 4. Documentation Files

All documentation files updated:
- `AGENTS.md`
- `BUILD_GUIDE.md`
- `CONTEXT.md`
- `PANDAFORGE_MASTER_PLAN.md`

Changed all references from "PandaForge" or "Pandaforge Project" to "pandaforge".

## What This Achieves

1. **Separate Config Directory**: The app will now use `~/.pandaforge/` instead of `~/.BambuStudio/` for configuration
2. **Separate Cache Directory**: Uses `~/Library/Application Support/pandaforge/` on macOS
3. **Independent Settings**: No longer shares settings with BambuStudio
4. **Branded UI**: All UI strings now show "pandaforge" instead of "BambuStudio"

## Post-Build Verification

After the build completes, verify:

1. Check that `install_dir/bin/pandaforge.app` exists (not `BambuStudio.app`)
2. Run: `open install_dir/bin/pandaforge.app`
3. Check that the app menu shows "pandaforge" instead of "BambuStudio"
4. Check that preferences are saved to `~/.pandaforge/` or `~/Library/Application Support/pandaforge/`

## GitHub Fork Instructions

After build verification:

1. Go to https://github.com/bambulab/BambuStudio
2. Click "Fork" button
3. Name the repository: `pandaforge`
4. Set visibility to "Private"
5. Clone your fork locally
6. Copy the modified source code to the fork
7. Push the changes

