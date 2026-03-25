# Roadmap

## Goal

Use this repository as a practical BambuStudio-derived workspace for third-party printer support, especially:

- vendor/profile work under `resources/profiles/`
- Klipper-friendly slicing behavior
- embedded printer web UI access through `print_host` / `print_host_webui`

## Current Reality

- The source tree is working directly from the repo root, not from a nested `BambuStudio-*` directory.
- The app naming sources are being normalized around `PandaForge` for build outputs and per-user data.
- Pressure advance support and third-party printer web access are present in source.
- Historical notes about bundled profile-converter tooling and custom Klipper widget modules do not match the current branch contents.

## Near-Term Priorities

### 1. Keep docs aligned with the branch

- Treat `INDEX.md` and `docs/01-start-here/current-state.md` as the routing layer.
- Keep active docs aligned with actual paths and code surfaces.
- Archive one-off investigations instead of letting them crowd the main docs surface.

### 2. Stabilize third-party printer/profile work

- Preserve complete inheritance chains in vendor manifests.
- Keep asset naming aligned with the UI lookup paths.
- Verify imported vendors through focused smoke tests before merging.

### 3. Keep build instructions reproducible

- Keep `docs/03-task-guides/build.md` as the entry point.
- Preserve `docs/90-history/plans/build-guide-v1.md` as the proven macOS method with lessons learned.
- Keep deps and app build paths current in docs.

## Medium-Term Priorities

- Finish the remaining user-facing rename work beyond bundle name and per-user data paths.
- Improve release/readme consistency if the fork identity is meant to be public-facing.
- Add stronger validation around profile manifests and asset completeness.

## De-Prioritized Or Historical Ideas

Do not assume these exist in the current branch just because older notes mention them:

- bundled `tools/profile_converter/`
- dedicated `src/slic3r/GUI/Klipper/` widget set
- native Moonraker polling/fan-control UI

They may still be worth revisiting later, but they are not current branch facts.

## Working Rule

If roadmap text and source code disagree, trust:

1. `docs/01-start-here/current-state.md`
2. the source tree
3. `docs/90-history/plans/build-guide-v1.md` for the proven macOS flow
