# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Project Summary

**Pandaforge** is a macOS-native fork of BambuStudio v2.5.0.66 for Klipper 3D printer users. It combines BambuStudio's UI with Klipper's flexibility: custom UI controls, Moonraker API integration, profile converter, optimized G-code, and MakerWorld compatibility.

## Quick Reference

| Component | Details |
|---|---|
| Base | BambuStudio v2.5.0.66 (C++17) |
| GUI | wxWidgets 3.1.5 (BambuLab fork) |
| Build | CMake 3.13+, always use `-j4` |
| Libraries | Boost 1.84.0, CGAL 5.4.5, libcurl, nlohmann/json |
| Platform | macOS (Apple Silicon and Intel) |

## Documentation Index

| I need to... | Read this |
|---|---|
| Build the project | `docs/building.md` |
| Understand codebase structure | `docs/architecture.md` |
| Write C++ code / know style rules | `docs/coding-conventions.md` |
| Work on Klipper UI components | `docs/klipper-components.md` |
| Work on Moonraker / fan control | `docs/moonraker-api.md` |
| Work on profiles / profile converter | `docs/profile-system.md` |
| Use the profile converter tool | `tools/profile_converter/README.md` |
| See project roadmap / status | `docs/roadmap.md` |
| See recent changes | `docs/changelog.md` |
| Run or write tests | `docs/testing.md` |
| Use GitHub / gh CLI / agents | `docs/github-workflow.md` |
| Full documentation index | `docs/INDEX.md` |

## Critical Rules

1. **Always use `-j4` not `-j8`** -- prevents build deadlock on large translation units
2. **wxWidgets 3.1.5 only** -- no `SetBold()`, no `SetSuffix()`, no `wxArrayString` initializer lists
3. **Use `AppConfig`** for settings, never `wxConfigBase`
4. **Wrap UI strings** with `_L("...")` for internationalization
5. **Check OrcaSlicer first** when implementing Klipper features
6. **Namespace**: all code in `Slic3r::GUI`

## Build Quick Start

```bash
# Prerequisites
brew install cmake git gettext nasm yasm x264

# Build deps (one-time, 30-60 min)
cd BambuStudio-2.5.0.66/deps && mkdir -p build && cd build
cmake ../ -DDESTDIR="/Users/$(whoami)/Pandaforge Project/BambuStudio_dep_2.5.0.66" -DOPENSSL_ARCH="darwin64-arm64-cc"
make -j4

# Build app (30-60 min)
cd ../../.. && cd BambuStudio-2.5.0.66 && mkdir -p build && cd build
cmake .. -DCMAKE_POLICY_VERSION_MINIMUM=3.5 -DBBL_RELEASE_TO_PUBLIC=1 -DCMAKE_PREFIX_PATH="/Users/$(whoami)/Pandaforge Project/BambuStudio_dep_2.5.0.66/usr/local" -DCMAKE_INSTALL_PREFIX="../install_dir" -DCMAKE_BUILD_TYPE=Release -DCMAKE_MACOSX_BUNDLE=ON
cmake --build . --target install --config Release -j4

# Run
open "BambuStudio-2.5.0.66/install_dir/BambuStudio.app"
```

Full build guide with troubleshooting: `docs/building.md`

## wxWidgets 3.1.5 Quick Reference

```cpp
// WRONG (wx 3.2+)               // CORRECT (wx 3.1.5)
wxArrayString c = {"a","b"};     wxArrayString c; c.Add("a"); c.Add("b");
font.SetBold();                  font.SetWeight(wxFONTWEIGHT_BOLD);
spin->SetSuffix("%");            // Not available -- remove or subclass
wxConfigBase::Get();             wxGetApp().app_config->set("s","k","v");
```

## Project Status

- **Phase 0 (Foundation):** Done -- working binary built
- **Phase 1 (Klipper Integration):** In progress -- components compiled, UI integration pending
- **Phase 2-4:** Not started

Full roadmap: `docs/roadmap.md`
