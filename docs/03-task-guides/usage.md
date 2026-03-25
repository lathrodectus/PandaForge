# Usage

This is the shortest human-facing smoke path for the current branch.

## Basic Workflow

1. Open the app.
2. Select a printer profile that already exists under `resources/profiles/`.
3. In filament settings, enable pressure advance if your printer uses it.
4. If you want in-app printer access, configure `print_host` and optionally `print_host_webui` in the Physical Printer dialog.
5. Open a model or a MakerWorld `.3mf` project.
6. Slice and inspect the generated G-code.

## Things To Verify

### Pressure advance

When enabled, exported G-code should contain:

```gcode
SET_PRESSURE_ADVANCE
```

### Device tab

For a non-BBL printer with a valid `print_host` or `print_host_webui`, the Device tab should load the printer's web UI.

### Profiles

If a profile does not appear in the UI, check:

- manifest ordering
- inheritance targets
- `instantiation`
- missing assets or companion presets

See [profile-system.md](../02-reference/profile-system.md) and [lessons-log.md](../02-reference/lessons-log.md).

## What This Branch Does Not Bundle

This branch does not currently include the historical `tools/profile_converter/` helper referenced in older notes. If you are importing vendor data, expect manual profile work or use a separate reference branch/repo.
