# pandaforge Project - AI Agent Guide

**Last Updated:** March 5, 2026  
**Version:** 1.0

> **Note**: See also [`CONTEXT.md`](CONTEXT.md) for detailed project context, recent changes, and development notes.

---

## Project Overview

pandaforge is a macOS-native fork of BambuStudio v2.5.0.66, specifically enhanced for Klipper 3D printer users. The project aims to combine BambuStudio's excellent UI with Klipper's flexibility, providing specialized controls for Klipper-based printers.

### Primary Goal

Enable users of **Klipper-based printers** to download **MakerWorld projects** and print seamlessly **without losing print settings** of the project.

### Key Objectives

1. **Klipper-specific UI Controls**: Custom widgets for bed plate selection, nozzle diameter switching, and fan control
2. **Moonraker Integration**: Real-time printer communication via HTTP API
3. **Profile Converter**: Migration tool for OrcaSlicer → BambuStudio profiles
4. **Better Klipper Defaults**: Optimized G-code templates and configurations
5. **MakerWorld Compatibility**: Preserve print settings when importing MakerWorld projects on Klipper printers

### Project Status

- **Phase 0 (Foundation)**: ✅ Complete - Working BambuStudio binary built
- **Phase 1 (Klipper Integration)**: 🔄 In Progress - Components compiled, UI integration pending
- **Phase 2+**: Not started

---

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

---

## Project Structure

```
pandaforge/
├── AGENTS.md                       # This file
├── BUILD_GUIDE.md                  # Build instructions
├── PANDAFORGE_MASTER_PLAN.md       # Project roadmap and planning
├── BambuStudio-2.5.0.66/           # Main source code
│   ├── src/                        # Source code
│   │   ├── libslic3r/              # Core slicing engine (281 files)
│   │   │   ├── AppConfig.cpp/hpp   # Application configuration
│   │   │   ├── PrintConfig.cpp/hpp # Print settings
│   │   │   └── ...                 # Slicing algorithms
│   │   ├── slic3r/                 # Application layer
│   │   │   ├── GUI/                # GUI components (408 files)
│   │   │   │   ├── Klipper/        # 🎯 CUSTOM KLIPPER COMPONENTS
│   │   │   │   │   ├── BedPlateSelector.cpp/hpp
│   │   │   │   │   ├── NozzleSelector.cpp/hpp
│   │   │   │   │   └── FanControlPanel.cpp/hpp
│   │   │   │   ├── MainFrame.cpp/hpp      # Main application window
│   │   │   │   ├── Plater.cpp/hpp         # 3D plater/workspace
│   │   │   │   ├── Widgets/               # Custom UI widgets
│   │   │   │   └── ...
│   │   │   └── Utils/              # Utility functions
│   │   └── BambuStudio.cpp         # Application entry point
│   ├── deps/                       # Dependency build scripts
│   │   ├── Boost/                  # Boost libraries
│   │   ├── wxWidgets/              # wxWidgets build
│   │   ├── CGAL/                   # CGAL build
│   │   └── ...                     # Other dependencies
│   ├── tests/                      # Unit tests (Catch2)
│   ├── resources/                  # Assets and profiles
│   ├── build/                      # Build output (generated)
│   └── install_dir/                # Installation output
│       └── BambuStudio.app         # 🎯 Final macOS app bundle
└── BambuStudio_dep_2.5.0.66/       # Built dependencies
    └── usr/local/                  # wxWidgets, Boost, etc.
```

---

## Important References

### OrcaSlicer

**OrcaSlicer is a critical reference for this project.**

- **Why**: OrcaSlicer supports almost all Klipper printers and has great features
- **Usage**: Port features and improvements from OrcaSlicer to pandaforge
- **Repository**: https://github.com/SoftFever/OrcaSlicer
- **Key Features to Reference**:
  - Comprehensive Klipper printer profiles
  - Advanced calibration tools (PA tower, flow rate, etc.)
  - Support for Voron and other popular Klipper printers
  - Multi-material support for Klipper setups
  - Optimized print settings for non-Bambu printers

**When implementing new features for Klipper support, always check how OrcaSlicer handles the same feature first.**

---

## Custom Klipper Components

Three custom UI components have been developed in `src/slic3r/GUI/Klipper/`:

### 1. BedPlateSelector

**Files:** `BedPlateSelector.cpp`, `BedPlateSelector.hpp`

Dropdown selector for bed plate types with temperature recommendations.

**Features:**
- Bed plate types: Cool, Engineering, High Temp, Textured PEI, Custom
- Temperature recommendations per plate type
- G-code variable export for template substitution
- Stores settings in `AppConfig`

**API:**
```cpp
BedPlateSelector(wxWindow* parent);
BedPlateType GetSelectedBedPlate() const;
int GetBedTemp(bool is_first_layer) const;
wxString GetGCodeVariable() const;
```

### 2. NozzleSelector

**Files:** `NozzleSelector.cpp`, `NozzleSelector.hpp`

Nozzle diameter selector with automatic print setting scaling.

**Features:**
- Sizes: 0.2mm - 0.8mm with presets
- Auto-scales: line width, speed, retraction, layer height
- Applies changes to `DynamicPrintConfig`

**API:**
```cpp
NozzleSelector(wxWindow* parent);
float GetNozzleDiameter() const;
void ApplyScalingToConfig(DynamicPrintConfig& config);
const NozzlePreset* GetCurrentPreset() const;
```

### 3. FanControlPanel

**Files:** `FanControlPanel.cpp`, `FanControlPanel.hpp`

Moonraker HTTP API integration for real-time fan control.

**Features:**
- Controls: Part cooling, Chamber, Aux, Exhaust fans
- Auto-polling from printer (2-second interval)
- Predefined printer profiles (Creality K1, Qidi Q2, Flashforge 5M, Centauri Carbon)
- libcurl for HTTP communication

**API:**
```cpp
FanControlPanel(wxWindow* parent);
void SetPrinterProfile(const PrinterProfile& profile);
void SetPrinterURL(const wxString& url);
bool SendGCode(const wxString& gcode);
void StartPolling(int interval_ms = 2000);
```

---

## Build System

### Prerequisites

```bash
# Install Xcode from App Store
# Install Homebrew dependencies
brew install cmake git gettext nasm yasm x264
```

### Build Commands

#### Step 1: Build Dependencies (One-time, 30-60 min)

```bash
cd BambuStudio-2.5.0.66/deps
mkdir -p build && cd build

# For Apple Silicon (arm64)
cmake ../ \
  -DDESTDIR="/Users/$(whoami)/pandaforge/BambuStudio_dep_2.5.0.66" \
  -DOPENSSL_ARCH="darwin64-arm64-cc"

make -j4  # ⚠️ Use -j4 not -j8 to prevent deadlock
```

#### Step 2: Build Application (30-60 min)

```bash
cd BambuStudio-2.5.0.66
mkdir -p build && cd build

cmake .. \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DBBL_RELEASE_TO_PUBLIC=1 \
  -DCMAKE_PREFIX_PATH="/Users/$(whoami)/pandaforge/BambuStudio_dep_2.5.0.66/usr/local" \
  -DCMAKE_INSTALL_PREFIX="../install_dir" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_MACOSX_BUNDLE=ON

cmake --build . --target install --config Release -j4
```

#### Space-in-Path Workaround

If the path contains spaces (like "pandaforge"), create a symlink:

```bash
ln -s "/Users/$(whoami)/pandaforge/BambuStudio_dep_2.5.0.66/usr/local" ~/bambu_deps

# Update wx-config paths
sed -i '' "s|/Users/$(whoami)/pandaforge/BambuStudio_dep_2.5.0.66/usr/local|/Users/$(whoami)/bambu_deps|g" \
  "$(brew --prefix)/bin/wx-config"

# Use symlink in CMake
-DCMAKE_PREFIX_PATH="/Users/$(whoami)/bambu_deps"
```

### CMake Options

| Option | Description | Default |
|--------|-------------|---------|
| `SLIC3R_GUI` | Build with GUI components | ON |
| `SLIC3R_STATIC` | Use static libraries | ON (macOS) |
| `SLIC3R_BUILD_TESTS` | Build unit tests | OFF |
| `SLIC3R_BUILD_SANDBOXES` | Build development sandboxes | OFF |
| `SLIC3R_PCH` | Use precompiled headers | ON |
| `BBL_RELEASE_TO_PUBLIC` | Enable public release features | 0 |

---

## Code Style Guidelines

### General Conventions

1. **Namespaces**: All code is in `Slic3r::GUI` namespace
2. **Includes**: Use relative paths for internal headers, e.g., `#include "../I18N.hpp"`
3. **Internationalization**: Wrap user-facing strings with `_L("...")` macro
4. **wxWidgets**: Use wxWidgets 3.1.5 API (not 3.2+)

### wxWidgets 3.1 Compatibility

The project uses wxWidgets 3.1.5. Some features from newer versions are NOT available:

```cpp
// ❌ Not available in wx 3.1:
m_spinCtrl->SetSuffix("%");           // Use plain SpinCtrl instead
wxFont bold = font.SetBold();          // Use SetWeight(wxFONTWEIGHT_BOLD)
wxArrayString choices = { "a", "b" };  // Initialize in constructor instead

// ✅ Correct approach:
wxArrayString choices;
choices.Add("a");
choices.Add("b");
```

### Configuration Storage

Use `Slic3r::AppConfig` instead of `wxConfigBase`:

```cpp
// ✅ Correct
AppConfig* config = wxGetApp().app_config;
if (config) {
    config->set("section", "key", "value");
}
```

---

## Testing

### Test Framework

- **Framework**: Catch2 v2.x
- **Location**: `tests/` directory
- **Test Data**: `tests/data/`

### Running Tests

```bash
# Build with tests enabled
cmake .. -DSLIC3R_BUILD_TESTS=ON
make -j4

# Run tests
cd tests
ctest --output-on-failure
```

### Test Categories

| Directory | Purpose |
|-----------|---------|
| `tests/libslic3r/` | Core library unit tests |
| `tests/fff_print/` | FFF slicing tests |
| `tests/sla_print/` | SLA slicing tests |
| `tests/libnest2d/` | Nesting algorithm tests |

---

## Integration Points

### Adding Klipper Components to MainFrame

To integrate the custom components into the main UI, modify `src/slic3r/GUI/MainFrame.cpp`:

```cpp
// 1. Add includes
#include "Klipper/BedPlateSelector.hpp"
#include "Klipper/NozzleSelector.hpp"
#include "Klipper/FanControlPanel.hpp"

// 2. Add member variables to MainFrame class
class MainFrame : public DPIFrame {
    // ... existing members ...
    BedPlateSelector* m_bed_plate_selector = nullptr;
    NozzleSelector* m_nozzle_selector = nullptr;
    FanControlPanel* m_fan_control = nullptr;
};

// 3. Create UI in initialization method
void MainFrame::CreateKlipperUI() {
    // Add to appropriate panel/sizer
    m_bed_plate_selector = new BedPlateSelector(parent_panel);
    m_nozzle_selector = new NozzleSelector(parent_panel);
    m_fan_control = new FanControlPanel(parent_panel);
}
```

### Moonraker API Endpoints

The FanControlPanel communicates with Moonraker using these endpoints:

```
GET  /api/printer                    # Get printer status
POST /api/printer/command            # Send G-code
GET  /api/server/info                # Server info
POST /printer/gcode/script           # Execute G-code script
```

---

## Common Issues & Solutions

### Build Issues

| Issue | Solution |
|-------|----------|
| Build deadlock | Use `-j4` instead of `-j8` |
| wxWidgets not found | Create symlink for path with spaces |
| ICU linking error | `export LDFLAGS="-L/opt/homebrew/opt/icu4c@78/lib"` |
| CMake version warnings | Add `-DCMAKE_POLICY_VERSION_MINIMUM=3.5` |

### API Compatibility

| Issue | Solution |
|-------|----------|
| `wxArrayString` init fails | Initialize in constructor |
| `wxFont::SetBold()` missing | Use `SetWeight(wxFONTWEIGHT_BOLD)` |
| `wxSpinCtrl::SetSuffix()` missing | Remove suffix or subclass |

---

## Security Considerations

1. **HTTP Communication**: FanControlPanel uses HTTP (not HTTPS) for Moonraker. Ensure printers are on trusted networks.
2. **G-code Injection**: User-provided G-code is sent directly to printers. Validate inputs before sending.
3. **Network Access**: The application requires network access for Moonraker integration and BambuLab cloud features.

---

## Localization

The project uses Localazy for internationalization:

- **Config**: `localazy.json`
- **Source Language**: English (en)
- **Supported Languages**: fr, de, sv, es, nl, hu, it, ja, ko
- **Format**: GNU gettext (.po files)

Location: `resources/i18n/`

---

## License

BambuStudio is licensed under the **GNU Affero General Public License, version 3** (AGPL-3.0).

- Based on PrusaSlicer by Prusa Research
- Originally from Slic3r by Alessandro Ranellucci
- The Bambu networking plugin uses non-free libraries (optional)

---

## References

- [BambuStudio GitHub](https://github.com/bambulab/BambuStudio)
- [Mac Compile Guide](https://github.com/bambulab/BambuStudio/wiki/Mac-Compile-Guide)
- [wxWidgets 3.1 Documentation](https://docs.wxwidgets.org/3.1/)
- [Moonraker API Documentation](https://moonraker.readthedocs.io/)

---

*This document is maintained for AI coding agents. For human-readable documentation, see BUILD_GUIDE.md and PANDAFORGE_MASTER_PLAN.md.*
