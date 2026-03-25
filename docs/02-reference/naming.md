# Naming

Use this file when a task touches the app name, bundle name, executable name, config filename, or per-user data path.

## Current Rule

- The fork/project label in docs is `Pandaforge`.
- The built app identity should be `PandaForge`.
- On macOS, the user-data root should be `~/Library/Application Support/PandaForge`.

## Sources Of Truth

| Concern | File | What it controls |
|---|---|---|
| App key and app name macros | `version.inc` | `SLIC3R_APP_NAME` and `SLIC3R_APP_KEY` used across build metadata and runtime config |
| Human-facing app full name | `src/libslic3r/libslic3r.h` | `SLIC3R_APP_FULL_NAME`, G-code viewer name, and related build-id strings |
| macOS bundle and executable output name | `src/CMakeLists.txt` | target `OUTPUT_NAME`, `MACOSX_BUNDLE_BUNDLE_NAME`, and bundle resource path |
| macOS plist metadata | `src/platform/osx/Info.plist.in` | `CFBundleExecutable`, `CFBundleName`, version strings, and URL scheme metadata |
| Runtime user-data root | `src/slic3r/GUI/GUI_App.cpp` | `SetAppName(SLIC3R_APP_KEY)` feeding `wxStandardPaths::Get().GetUserDataDir()` |
| Sanitized path redaction lengths | `src/libslic3r/Utils.hpp` | the platform path patterns used when logs redact usernames |
| App config filenames | `src/libslic3r/AppConfig.cpp` | `${SLIC3R_APP_KEY}.conf` and `${GCODEVIEWER_APP_KEY}.conf` under the data dir |
| Relaunching a sibling app on macOS | `src/slic3r/Utils/Process.cpp` | expected executable name inside the app bundle |

## What This Means On macOS

- Bundle path: `install_dir/bin/PandaForge.app`
- Main executable: `install_dir/bin/PandaForge.app/Contents/MacOS/PandaForge`
- User data root: `~/Library/Application Support/PandaForge`
- Main config file: `~/Library/Application Support/PandaForge/PandaForge.conf`

## Scope Note

This naming guide covers the build artifact identity and runtime data location first. It does not guarantee that every user-facing string, icon asset name, desktop entry, or updater endpoint has been fully rebranded.
