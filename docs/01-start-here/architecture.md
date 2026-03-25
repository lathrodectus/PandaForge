# Architecture

## Repo Shape

This branch uses a flat source layout rooted at the repository top level. The active code is not nested under a separate `BambuStudio-*` directory.

```text
Pandaforge Project/
├── CMakeLists.txt              # Top-level build configuration
├── BuildMac.sh                 # legacy macOS helper script
├── build/                      # generated local CMake build trees
├── install_dir/                # generated macOS install target output
├── version.inc                 # App/version metadata and primary app key/name
├── deps/                       # Third-party dependency build recipes
├── docs/                       # Active and archived project docs
├── resources/                  # App assets, profiles, i18n, web resources
├── src/                        # Main source tree
├── tests/                      # Catch2 test suites
├── research/                   # Upstream/reference repos
└── worktrees/                  # Local isolated branch worktrees
```

## Important Top-Level Areas

| Path | Purpose |
|---|---|
| `src/libslic3r/` | slicing core, presets, config, G-code generation |
| `src/slic3r/GUI/` | wxWidgets UI, plater, tabs, device tab integration |
| `resources/profiles/` | printer, filament, and process profile data |
| `deps/` | dependency build definitions |
| `install_dir/` | final macOS app bundle from the canonical install flow |
| `tests/` | automated tests by subsystem |
| `research/` | upstream/reference clones for comparison work |
| `worktrees/` | parallel local branches with their own working trees |

## Key Source Files

| File | Why it matters |
|---|---|
| `src/libslic3r/GCode.cpp` | high-level G-code generation logic |
| `src/libslic3r/GCodeWriter.cpp` | low-level emitted G-code, including pressure advance output |
| `src/libslic3r/PresetBundle.cpp` | profile loading and inheritance resolution |
| `src/libslic3r/Preset.cpp` | preset serialization and config exposure |
| `src/libslic3r/PrintConfig.cpp` | config key definitions |
| `src/libslic3r/AppConfig.cpp` | persistent app settings |
| `src/slic3r/GUI/MainFrame.cpp` | top-level app window and Device tab flow |
| `src/slic3r/GUI/Plater.cpp` | project loading, main plater workflow, UI state |
| `src/slic3r/GUI/PrinterWebView.cpp` | embedded browser for third-party printer web UIs |
| `src/slic3r/GUI/Tab.cpp` | settings UI, including Klipper-facing options |

## Configuration Surfaces

### App config

Persistent application settings live behind `Slic3r::AppConfig` in `src/libslic3r/AppConfig.cpp`.

### Presets and profiles

Machine, filament, and process presets live under `resources/profiles/` and are loaded through `PresetBundle`.

### Build metadata

Naming and version metadata live in:

- `version.inc`
- `src/CMakeLists.txt`
- `src/platform/osx/Info.plist.in`

Those files define the current `PandaForge` app identity for the build and bundle metadata.
The naming flow is documented in `docs/02-reference/naming.md`.

## Reference Material Inside The Workspace

| Path | Role |
|---|---|
| `research/OrcaSlicer-main` | pinned upstream study repo |
| `research/QIDIStudio` | vendor fork reference |
| `worktrees/anycubic-dev` | isolated local branch worktree |
| `worktrees/qidi-box-sync` | isolated local branch worktree |

Use those for comparison or migration work, but make code changes in the repo root unless the task explicitly targets a worktree or research repo.
