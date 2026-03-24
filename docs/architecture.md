# Architecture

## Technology Stack

| Component | Version | Purpose |
|---|---|---|
| BambuStudio Base | v2.5.0.66 | Core slicer application |
| C++ Standard | C++17 | Primary language |
| CMake | 3.13+ | Build system |
| wxWidgets | 3.1.5 | GUI toolkit (BambuLab fork) |
| Boost | 1.84.0 | C++ utility libraries |
| CGAL | 5.4.5 | Computational geometry |
| libcurl | Latest | HTTP client for Moonraker API |
| nlohmann/json | Latest | JSON parsing |

**Platform:** macOS (Apple Silicon and Intel)

## Directory Structure

```
Pandaforge Project/
├── CLAUDE.md                           # Entry point for agents
├── docs/                               # Project documentation
├── tools/
│   └── profile_converter/              # OrcaSlicer -> Pandaforge converter
├── BambuStudio-2.5.0.66/               # Main source code
│   ├── src/
│   │   ├── libslic3r/                  # Core slicing engine (281 files)
│   │   │   ├── GCode.cpp/hpp           # G-code generation (layer-by-layer)
│   │   │   ├── GCodeWriter.cpp/hpp     # Low-level G-code output
│   │   │   ├── PrintConfig.cpp/hpp     # 500+ print/printer/filament settings
│   │   │   ├── AppConfig.cpp/hpp       # Application configuration
│   │   │   └── Preset.cpp/hpp          # Printer/filament/print presets
│   │   ├── slic3r/
│   │   │   ├── GUI/                    # GUI components (408 files)
│   │   │   │   ├── Klipper/            # Custom Klipper components
│   │   │   │   │   ├── BedPlateSelector.cpp/hpp
│   │   │   │   │   ├── NozzleSelector.cpp/hpp
│   │   │   │   │   └── FanControlPanel.cpp/hpp
│   │   │   │   ├── MainFrame.cpp/hpp   # Main application window
│   │   │   │   ├── Plater.cpp/hpp      # 3D workspace/plater
│   │   │   │   └── Widgets/            # Custom UI widgets
│   │   │   └── Utils/                  # Utility functions
│   │   └── BambuStudio.cpp             # Application entry point
│   ├── resources/                      # Assets, profiles, i18n
│   ├── tests/                          # Unit tests (Catch2)
│   ├── deps/                           # Dependency build scripts
│   └── install_dir/                    # Build output
│       └── BambuStudio.app             # Final macOS app bundle
└── BambuStudio_dep_2.5.0.66/           # Built dependencies
    └── usr/local/                      # wxWidgets, Boost, etc.
```

## Key Source Files

| File | Location | Purpose |
|---|---|---|
| `GCode.cpp` | `src/libslic3r/` | Main G-code generation logic |
| `GCodeWriter.cpp` | `src/libslic3r/` | Low-level G-code output and formatting |
| `PrintConfig.cpp` | `src/libslic3r/` | Configuration system (500+ settings) |
| `Preset.cpp` | `src/libslic3r/` | Manages printer/filament/print presets |
| `AppConfig.cpp` | `src/libslic3r/` | Application-level configuration |
| `MainFrame.cpp` | `src/slic3r/GUI/` | Main window, menu bar, toolbar |
| `Plater.cpp` | `src/slic3r/GUI/` | 3D view workspace, slicing controls |
| `BambuStudio.cpp` | `src/` | Application entry point |

## Configuration System

### AppConfig (Application Settings)

Persistent application settings use `Slic3r::AppConfig`:

```cpp
AppConfig* config = wxGetApp().app_config;
if (config) {
    config->set("section", "key", "value");
    std::string value = config->get("section", "key");
}
```

### PresetBundle (Printer/Filament/Print Profiles)

Printer, filament, and print presets are managed through `PresetBundle` and stored in `resources/profiles/`. Each vendor has a directory with machine, filament, and process subdirectories.

## Reference Projects

| Project | URL | Relevance |
|---|---|---|
| OrcaSlicer | https://github.com/SoftFever/OrcaSlicer | Klipper features reference (check first!) |
| BambuStudio | https://github.com/bambulab/BambuStudio | Upstream base |
| PrusaSlicer | https://github.com/prusa3d/PrusaSlicer | Original upstream |
| Klipper | https://www.klipper3d.org/ | Firmware documentation |
| Moonraker | https://moonraker.readthedocs.io/ | API documentation |
