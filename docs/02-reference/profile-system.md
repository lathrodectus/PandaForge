# Profile System

## Where Profiles Live

Profiles live in:

```text
resources/profiles/
```

In this branch, vendor manifests are usually sibling JSON files at the top level, while machine, filament, and process presets live under vendor subdirectories.

Typical layout:

- `resources/profiles/<Vendor>.json` for the vendor manifest
- `resources/profiles/<Vendor>/machine/` for printer definitions
- `resources/profiles/<Vendor>/filament/` for material presets
- `resources/profiles/<Vendor>/process/` for quality/process presets

## Code Touchpoints

| File | Role |
|---|---|
| `src/libslic3r/PresetBundle.cpp` | loads manifests and preset graphs |
| `src/libslic3r/Preset.cpp` | preset serialization and compatibility logic |
| `src/libslic3r/PrintConfig.cpp` | config key definitions |
| `src/slic3r/GUI/Tab.cpp` | settings UI exposure |

## Structure Pattern

```text
resources/profiles/
├── Qidi.json
└── Qidi/
    ├── machine/
    ├── filament/
    └── process/
```

Within each area, base presets usually appear first and user-selectable variants later.

## Critical Rules

### Load order matters

Manifest lists are order-sensitive. If preset `B` inherits from preset `A`, `A` must appear earlier in the manifest list.

### `instantiation` controls UI visibility

- `true`: selectable in the UI
- `false`: base preset used only for inheritance

### Vendor bundles need complete base layers

A vendor import is not complete unless the manifest includes the non-instantiable machine, filament, and process bases that visible presets inherit from.

### Assets resolve through multiple paths

For printer/profile UX, be aware that different UI surfaces look for different assets:

- setup wizard thumbnails
- profile guide cover images
- plater/sidebar preview images

See [lessons-log.md](lessons-log.md) for the detailed filename conventions that were learned the hard way.

## Klipper-Relevant Fields

Common fields that matter for third-party/Klipper workflows:

- `gcode_flavor`
- `enable_pressure_advance`
- `pressure_advance`
- machine kinematics and limits
- `compatible_printers`

Definitions live in `src/libslic3r/PrintConfig.cpp`.

Related physical-printer host settings used by the Device tab:

- `print_host`
- `print_host_webui`

Those are configured through the Physical Printer flow, not as vendor profile JSON content.

## Adding Or Repairing A Vendor

Use this checklist:

1. Confirm the vendor manifest lists every required base preset before derived presets.
2. Confirm machine, filament, and process inheritance graphs all resolve locally.
3. Confirm user-visible presets have `instantiation = true`.
4. Confirm wizard, guide, and preview assets exist under the filenames the UI actually resolves.
5. Confirm at least one valid nozzle/process ladder exists for every exposed machine.

## Notes About Historical Tooling

Older docs and archived investigations mention a bundled `tools/profile_converter/` workflow. That tool does not exist in this branch. Treat those references as historical unless you are reviving that tooling from another branch or reference repo.
