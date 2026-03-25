# Klipper Support Surface

Despite the filename, this branch does not contain a dedicated `src/slic3r/GUI/Klipper/` module. Klipper-related support is spread across profiles, settings UI, G-code generation, and the Device tab flow.

## Where Klipper Support Actually Lives

| Area | Files | Notes |
|---|---|---|
| Profile data | `resources/profiles/` | machine/process/filament presets and vendor manifests |
| Config keys | `src/libslic3r/PrintConfig.cpp` | definitions for `print_host`, `print_host_webui`, pressure advance, and other options |
| Preset loading | `src/libslic3r/PresetBundle.cpp`, `src/libslic3r/Preset.cpp` | profile wiring and compatibility |
| Settings UI | `src/slic3r/GUI/Tab.cpp` | exposes Klipper-related options |
| G-code generation | `src/libslic3r/GCode.cpp`, `src/libslic3r/GCodeWriter.cpp` | pressure advance output and slicer behavior |
| Device tab web access | `src/slic3r/GUI/MainFrame.cpp`, `src/slic3r/GUI/PrinterWebView.cpp`, `src/slic3r/GUI/Plater.cpp`, `src/slic3r/GUI/PhysicalPrinterDialog.cpp` | loads `print_host_webui` or falls back to `print_host` |

## Pressure Advance

Current support is real and implemented in the active source tree:

- config definition: `src/libslic3r/PrintConfig.cpp`
- settings UI: `src/slic3r/GUI/Tab.cpp`
- emitted G-code: `src/libslic3r/GCodeWriter.cpp`
- slicer integration points: `src/libslic3r/GCode.cpp`

Example emitted command:

```gcode
SET_PRESSURE_ADVANCE ADVANCE=0.025
```

## Device Tab

For third-party printers, the practical integration point is the embedded web UI path driven by `print_host_webui` or `print_host`, not a native Klipper widget set.

See [device-tab.md](device-tab.md) for that flow.

## Historical Note

Archived docs may mention custom widgets such as `BedPlateSelector`, `NozzleSelector`, or `FanControlPanel`. Those references are historical and do not match the current branch contents.
