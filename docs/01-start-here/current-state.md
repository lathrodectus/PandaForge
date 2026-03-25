# Current State

This is the shortest reliable description of the current branch.

## Branch Reality

- The repository root contains the active source tree directly: `src/`, `resources/`, `deps/`, `tests/`, and `docs/`.
- The active app naming sources now target `PandaForge` for the bundle, executable, and per-user data directory.
- The workspace name and project notes use "Pandaforge" for the fork/project identity.
- There is no root `AGENTS.md` or `CLAUDE.md` in this branch.

## Verified Code Surfaces

### Klipper pressure advance

- Config definition: `src/libslic3r/PrintConfig.cpp`
- Config use in slicing: `src/libslic3r/GCode.cpp`
- G-code emission: `src/libslic3r/GCodeWriter.cpp`
- UI exposure in filament settings: `src/slic3r/GUI/Tab.cpp`

### Device tab / print host web UI

- Entry points: `src/slic3r/GUI/MainFrame.cpp`
- Embedded web view: `src/slic3r/GUI/PrinterWebView.cpp`
- Caller from plater/UI flow: `src/slic3r/GUI/Plater.cpp`
- Config keys: `print_host`, `print_host_webui`
- Settings surface: `src/slic3r/GUI/PhysicalPrinterDialog.cpp`

### Profiles and vendor data

- Data: `resources/profiles/`
- Loader and preset wiring: `src/libslic3r/PresetBundle.cpp`
- Option definitions and serialization: `src/libslic3r/Preset.cpp`, `src/libslic3r/PrintConfig.cpp`

### Build and test entry points

- active macOS build brief: `docs/03-task-guides/build.md`
- detailed macOS guide with install-path lessons: `docs/90-history/plans/build-guide-v1.md`
- `BuildMac.sh` still exists, but it is not the primary documented route for this branch
- Linux helper script: `BuildLinux.sh`
- Windows helper script: `build_win.bat`
- dependency build system: `deps/`
- main CMake entry: `CMakeLists.txt`
- automated tests: `tests/`

### Latest macOS verification

- On March 25, 2026, a fresh dependency build completed into `/Users/$(whoami)/Pandaforge-deps/usr/local`.
- App configure succeeded against that prefix and the documented install flow now completes.
- The installed app bundle should land at `install_dir/bin/PandaForge.app`.
- The bundle/executable/app-support naming sources are documented in `docs/02-reference/naming.md`.
- The working branch carries two AppleClang compatibility fixes for this flow:
  - `CMakeLists.txt` only adds `-Wno-error=enum-constexpr-conversion` when the compiler supports it
  - media-state sentinel values in the GUI are runtime casts instead of out-of-range `constexpr wxMediaState` declarations
- Treat `docs/03-task-guides/build.md` as the live status page for build work.

## Not Present In This Branch

- `tools/profile_converter/`
- `src/slic3r/GUI/Klipper/`
- root-level agent instruction files such as `AGENTS.md` or `CLAUDE.md`

Older docs may still mention those paths because they existed in planning notes or side branches. Treat those mentions as historical, not authoritative.

## Reference Repos In Workspace

- `research/OrcaSlicer-main`: embedded Git repo pinned for upstream study
- `research/QIDIStudio`: gitlink reference repo
- `worktrees/`: parallel local branches for isolated changes

Use them as reference material, not as the active source of truth for this branch.
