# pandaforge Project Context

## Project Overview
**pandaforge** is a macOS-native fork of BambuStudio v2.5.0.66, specifically enhanced for Klipper 3D printer users.

### Primary Goal
Enable users of Klipper-based printers to download MakerWorld projects and print seamlessly without losing print settings of the project.

### Key Objectives
1. **Klipper-specific UI Controls**: Custom widgets for bed plate selection, nozzle diameter switching, and fan control
2. **Moonraker Integration**: Real-time printer communication via HTTP API
3. **Profile Converter**: Migration tool for OrcaSlicer → BambuStudio profiles
4. **Better Klipper Defaults**: Optimized G-code templates and configurations
5. **MakerWorld Compatibility**: Preserve print settings when importing MakerWorld projects

## Important References

### OrcaSlicer
- **Critical Reference**: OrcaSlicer is a very important source for improvements
- **Why**: It supports almost all Klipper printers and has great features
- **Usage**: Port features and improvements from OrcaSlicer to pandaforge
- **GitHub**: https://github.com/SoftFever/OrcaSlicer

### Upstream Sources
- **BambuStudio Base**: v2.5.0.66 - Core slicer application
- **Original**: PrusaSlicer by Prusa Research
- **Root**: Slic3r by Alessandro Ranellucci

## Recent Changes & Fixes

### Pressure Advance Fix (March 5, 2026)
- **Issue**: Pressure advance settings not being applied to Klipper G-code output
- **Solution**: 
  - Added initial pressure advance setup at print start
  - Enhanced Klipper multi-extruder support with EXTRUDER parameter
  - Updated `GCodeWriter::set_pressure_advance()` to accept extruder_id
- **Files Modified**:
  - `src/libslic3r/GCode.cpp`
  - `src/libslic3r/GCodeWriter.cpp`
  - `src/libslic3r/GCodeWriter.hpp`

### UI Panel Size Fix (March 5, 2026)
- **Issue**: Printer and bed plate selector panels too small for 3rd party printers
- **Solution**: Increased panel size for non-BBL printers (96x68 → 140x90 pixels)
- **Note**: Layout differences are intentional (BBL=vertical, 3rd party=horizontal)

## Custom Klipper Components

### 1. BedPlateSelector
- **Location**: `src/slic3r/GUI/Klipper/BedPlateSelector.cpp/hpp`
- **Features**:
  - Bed plate types: Cool, Engineering, High Temp, Textured PEI, Custom
  - Temperature recommendations per plate type
  - G-code variable export for template substitution

### 2. NozzleSelector
- **Location**: `src/slic3r/GUI/Klipper/NozzleSelector.cpp/hpp`
- **Features**:
  - Sizes: 0.2mm - 0.8mm with presets
  - Auto-scales: line width, speed, retraction, layer height
  - Applies changes to DynamicPrintConfig

### 3. FanControlPanel (planned/in-progress)
- **Location**: `src/slic3r/GUI/Klipper/FanControlPanel.cpp/hpp`
- **Features**:
  - Controls: Part cooling, Chamber, Aux, Exhaust fans
  - Auto-polling from printer (2-second interval)
  - Predefined printer profiles

## Technology Stack

| Component | Version | Purpose |
|-----------|---------|---------|
| BambuStudio Base | v2.5.0.66 | Core slicer application |
| C++ Standard | C++17 | Primary language |
| CMake | 3.13+ | Build system |
| wxWidgets | 3.1.5 | Cross-platform GUI toolkit |
| Boost | 1.84.0 | C++ utility libraries |
| CGAL | 5.4.5 | Computational geometry |
| libcurl | Latest | HTTP client for Moonraker API |
| nlohmann/json | Latest | JSON parsing for API responses |

## Build Information

### macOS Build Location
```
/Users/emredoner/pandaforge/BambuStudio-2.5.0.66/install_dir/bin/BambuStudio.app
```

### Key Build Notes
- Use `-j4` not `-j8` to prevent build deadlock
- Use symlink for path with spaces: `~/bambu_deps`
- Dependencies built in: `BambuStudio_dep_2.5.0.66/`

## Development Guidelines

### Code Style
1. All code in `Slic3r::GUI` namespace
2. Use relative paths for internal headers
3. Wrap user-facing strings with `_L("...")` macro
4. Use wxWidgets 3.1.5 API (not 3.2+)

### Configuration Storage
Use `Slic3r::AppConfig` instead of `wxConfigBase`:
```cpp
AppConfig* config = wxGetApp().app_config;
if (config) {
    config->set("section", "key", "value");
}
```

### Testing Pressure Advance
Enable in filament settings:
- `enable_pressure_advance = 1`
- `pressure_advance = 0.0585` (example value)

Check G-code output for:
```gcode
SET_PRESSURE_ADVANCE EXTRUDER=extruder ADVANCE=0.0585 ; Override pressure advance value
```

## Future Work

### Planned Features
1. Profile converter from OrcaSlicer formats
2. Enhanced Moonraker integration
3. More Klipper-optimized default profiles
4. Improved MakerWorld project import

### Reference Features from OrcaSlicer to Port
- Advanced calibration tools
- More comprehensive Klipper printer profiles
- Improved support for Voron and other Klipper printers
- Better multi-material support for Klipper

## Contact & Resources
- Main Repo: Based on BambuStudio v2.5.0.66
- OrcaSlicer Reference: https://github.com/SoftFever/OrcaSlicer
- Moonraker API: https://moonraker.readthedocs.io/
- Klipper: https://www.klipper3d.org/
