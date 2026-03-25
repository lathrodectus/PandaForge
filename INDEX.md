# Pandaforge Docs Router

Start here. This is the only router agents should open first.

## Reality Check

- The workspace is a flat source tree rooted here: `src/`, `resources/`, `deps/`, `tests/`.
- The repo/workspace is called Pandaforge, and the active app naming sources now target `PandaForge`.
- The legacy top-level `doc/` folder is intentionally gone.
- All current project docs live under `docs/`, with numeric prefixes that encode read order and trust level.
- There is no root `AGENTS.md` or `CLAUDE.md` in this branch.
- Historical notes may mention `tools/profile_converter/` and `src/slic3r/GUI/Klipper/`; those paths do not exist in this branch.
- Historical material lives under `docs/90-history/` and should be skipped by default.

## Default Read Order

1. [docs/01-start-here/current-state.md](docs/01-start-here/current-state.md)
2. [docs/01-start-here/architecture.md](docs/01-start-here/architecture.md)
3. Read one task-specific doc under `docs/02-reference/` or `docs/03-task-guides/`
4. Read [docs/04-project/roadmap.md](docs/04-project/roadmap.md) only if you need planning context
5. Only then open `docs/90-history/` if you still need archaeology

## Task Routes

| If you need to... | Read this first | Then inspect |
|---|---|---|
| Understand what is actually true in this branch | [docs/01-start-here/current-state.md](docs/01-start-here/current-state.md) | `version.inc`, `src/CMakeLists.txt`, [docs/03-task-guides/build.md](docs/03-task-guides/build.md) |
| Trace app naming, bundle naming, and user-data paths | [docs/02-reference/naming.md](docs/02-reference/naming.md) | `version.inc`, `src/CMakeLists.txt`, `src/libslic3r/libslic3r.h`, `src/libslic3r/Utils.hpp`, `src/slic3r/GUI/GUI_App.cpp` |
| Understand repo layout and key files | [docs/01-start-here/architecture.md](docs/01-start-here/architecture.md) | `src/`, `resources/`, `deps/`, `tests/`, `research/`, `worktrees/` |
| Build on macOS, Linux, or Windows | [docs/03-task-guides/build.md](docs/03-task-guides/build.md) | [docs/90-history/plans/build-guide-v1.md](docs/90-history/plans/build-guide-v1.md), `BuildLinux.sh`, `build_win.bat` |
| Work on profiles or vendor imports | [docs/02-reference/profile-system.md](docs/02-reference/profile-system.md) | [docs/02-reference/lessons-log.md](docs/02-reference/lessons-log.md), `resources/profiles/`, `src/libslic3r/PresetBundle.cpp` |
| Work on Klipper behavior | [docs/02-reference/klipper-components.md](docs/02-reference/klipper-components.md) | `src/libslic3r/GCode.cpp`, `src/libslic3r/GCodeWriter.cpp`, `src/slic3r/GUI/Tab.cpp` |
| Work on the Device tab / print host web UI | [docs/02-reference/device-tab.md](docs/02-reference/device-tab.md) | `src/slic3r/GUI/MainFrame.cpp`, `src/slic3r/GUI/PrinterWebView.cpp`, `src/slic3r/GUI/Plater.cpp`, `src/slic3r/GUI/PhysicalPrinterDialog.cpp` |
| Run automated or manual validation | [docs/03-task-guides/testing.md](docs/03-task-guides/testing.md) | `tests/`, `ctest`, focused smoke tests |
| Follow the shortest manual smoke path | [docs/03-task-guides/usage.md](docs/03-task-guides/usage.md) | `resources/profiles/`, sample `.3mf` projects, generated G-code |
| Follow repo-specific implementation patterns | [docs/03-task-guides/coding-conventions.md](docs/03-task-guides/coding-conventions.md) | `src/slic3r/GUI/`, `src/libslic3r/`, `resources/i18n/` |
| See project priorities and release direction | [docs/04-project/roadmap.md](docs/04-project/roadmap.md) | `INDEX.md`, `docs/01-start-here/current-state.md` |

## Folder Map

- [docs/01-start-here/current-state.md](docs/01-start-here/current-state.md): shortest reliable branch snapshot
- [docs/01-start-here/architecture.md](docs/01-start-here/architecture.md): repo shape and key code surfaces
- [docs/02-reference/profile-system.md](docs/02-reference/profile-system.md): vendor manifests, preset inheritance, and profile repair rules
- [docs/02-reference/naming.md](docs/02-reference/naming.md): app name, bundle name, executable name, and per-user data path sources
- [docs/02-reference/klipper-components.md](docs/02-reference/klipper-components.md): where Klipper-facing behavior actually lives
- [docs/02-reference/device-tab.md](docs/02-reference/device-tab.md): current `print_host` / `print_host_webui` flow
- [docs/02-reference/lessons-log.md](docs/02-reference/lessons-log.md): branch-earned lessons for profile and UI work
- [docs/03-task-guides/build.md](docs/03-task-guides/build.md): active build status, current macOS commands, and links to the deeper historical guide
- [docs/03-task-guides/testing.md](docs/03-task-guides/testing.md): automated and manual validation routes
- [docs/03-task-guides/usage.md](docs/03-task-guides/usage.md): shortest human smoke flow
- [docs/03-task-guides/coding-conventions.md](docs/03-task-guides/coding-conventions.md): repo-specific implementation constraints
- [docs/04-project/roadmap.md](docs/04-project/roadmap.md): priorities and direction
- [docs/90-history/README.md](docs/90-history/README.md): archived plans, reports, and stale workflow notes

## Skip By Default

Do not load `docs/90-history/**` unless you need historical context. Those files may describe older layouts, deleted tools, or plans that never landed in this branch.
