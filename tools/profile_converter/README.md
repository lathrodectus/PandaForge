# OrcaSlicer to Pandaforge Profile Converter

Converts Klipper printer profiles from OrcaSlicer format to Pandaforge (BambuStudio fork) format. Preserves inheritance chains, Klipper-specific settings (pressure advance, kinematics), and generates proper vendor manifests.

## Requirements

- Python 3.7+ (standard library only)
- tkinter (optional, for GUI only): `brew install python-tk@3.12`

## Quick Start

```bash
cd tools/profile_converter

# Option 1: One-command launcher
./run.sh

# Option 2: GUI
./launch_gui.sh

# Option 3: Interactive CLI menu
python3 menu.py

# Option 4: Direct CLI
python3 orca_to_pandaforge.py <orca_dir> <output_dir> --vendor "Brand"
```

## CLI Usage

### Convert a Single Vendor

```bash
python3 orca_to_pandaforge.py \
    ~/OrcaSlicer-main/resources/profiles/Creality \
    ~/Pandaforge\ Project/BambuStudio-2.5.0.66/resources/profiles/Creality \
    --vendor "Creality"
```

### Convert Multiple Vendors

```bash
./convert_common_printers.sh
```

### Validate Converted Profiles

```bash
python3 validate_profiles.py \
    ~/Pandaforge\ Project/BambuStudio-2.5.0.66/resources/profiles/Creality
```

Validates: required fields, profile types, Klipper settings, temperature ranges, compatible printers, vendor JSON structure.

## GUI Usage

```bash
./launch_gui.sh
# Or: python3 profile_converter_gui.py
```

**Features:**
- Automatic path detection (uses project directories)
- Hierarchical brand/model tree view with multi-select
- Klipper filtering (select only Klipper-compatible printers)
- Search/filter by brand name
- Real-time conversion log
- Background processing (UI stays responsive)

**Workflow:** Launch → Select brands/printers → Click "Convert Selected" → Done

## Interactive CLI

```bash
python3 convert_interactive.py
# Or: ./convert.sh
```

**Selection options:**
- Enter numbers: `1,3,5` (specific brands)
- Enter range: `1-5`
- Enter `A` (all brands)
- Enter `K` (all Klipper brands)
- Per brand: `A` (all), `S` (select specific), `K` (Klipper only)

## Supported Printers

| Brand | Models |
|---|---|
| Creality | K1, K1 Max, K1C, Ender-3 V3 KE, CR-M4 |
| Voron | 2.4, 0.2, Trident, Switchwire |
| Prusa | MK4, XL (Klipper mods) |
| Qidi | X-Max 3, X-Plus 3 |
| Sovol | SV06, SV07 |
| BIQU | B1, BX |
| Flashforge | Adventurer 5M Pro |
| Anycubic | Kobra series (Klipper) |
| Others | Elegoo, Kingroon, Artillery, Ratrig, and more |

## What Gets Converted

- **Machine profiles** -- Printer specs, kinematics, G-code templates
- **Filament profiles** -- Materials, temperatures, pressure advance settings
- **Process profiles** -- Quality presets, speeds, accelerations
- **Assets** -- Cover images, buildplate textures, 3D models
- **Vendor manifest** -- JSON manifest for BambuStudio profile system

## Output Structure

```
output_dir/
├── Vendor.json              # Vendor manifest
├── machine/
│   ├── Printer Model.json
│   ├── Printer 0.4 Nozzle.json
│   └── fdm_vendor_common.json
├── filament/
│   ├── Generic PLA.json
│   ├── Generic PETG.json
│   └── fdm_filament_pla.json
├── process/
│   ├── 0.20mm Standard.json
│   ├── 0.12mm Fine.json
│   └── fdm_process_common.json
├── *_cover.png
├── *_buildplate_texture.png
└── *_buildplate_model.STL
```

## Field Mappings

| OrcaSlicer Field | Pandaforge Field |
|---|---|
| `bed_temperature` | `hot_plate_temp` |
| `bed_temperature_initial_layer` | `hot_plate_temp_initial_layer` |
| `first_layer_height` | `initial_layer_height` |
| `perimeters` | `wall_loops` |
| `top_solid_layers` | `top_shell_layers` |
| `bottom_solid_layers` | `bottom_shell_layers` |

## Klipper-Specific Handling

The converter ensures these critical settings are preserved:

1. **G-code flavor:** Sets `gcode_flavor: "klipper"`
2. **Pressure advance:** Enables `enable_pressure_advance: ["1"]`, preserves PA values (default 0.025)
3. **Kinematics:** Preserves max speeds, accelerations, and jerk values
4. **Relative E:** Sets `use_relative_e_distances: "1"`
5. **G-code templates:** Maintains Klipper-specific start/end G-code

## Profile Templates

### Machine Profile (Minimal)
```json
{
    "type": "machine",
    "name": "Printer Name 0.4 Nozzle",
    "inherits": "fdm_vendor_common",
    "from": "system",
    "instantiation": "true",
    "gcode_flavor": "klipper",
    "nozzle_diameter": ["0.4"],
    "printable_area": ["0x0", "220x0", "220x220", "0x220"],
    "printable_height": "250"
}
```

### Filament Profile (Minimal)
```json
{
    "type": "filament",
    "name": "Generic PLA @Printer",
    "inherits": "fdm_filament_pla",
    "from": "system",
    "instantiation": "true",
    "nozzle_temperature": ["210"],
    "hot_plate_temp": ["55"],
    "enable_pressure_advance": ["1"],
    "pressure_advance": ["0.025"],
    "compatible_printers": ["Printer Name 0.4 Nozzle"]
}
```

### Process Profile (Minimal)
```json
{
    "type": "process",
    "name": "0.20mm Standard @Printer",
    "inherits": "fdm_process_common",
    "from": "system",
    "instantiation": "true",
    "layer_height": "0.2",
    "compatible_printers": ["Printer Name 0.4 Nozzle"]
}
```

## Inheritance Chains

```
Machine:  fdm_machine_common -> fdm_vendor_common -> fdm_model_common -> Printer 0.4 Nozzle
Filament: fdm_filament_common -> fdm_filament_pla -> Generic PLA @Printer
Process:  fdm_process_common -> fdm_process_vendor -> 0.20mm Standard @Printer
```

## Post-Conversion Steps

1. **Review** -- Check converted JSON files for accuracy
2. **Test print** -- Run test prints with actual hardware
3. **Tune pressure advance** -- Typical values: PLA 0.025-0.040, PETG 0.055-0.080, ABS 0.035-0.055, TPU 0.000-0.020
4. **Customize G-code** -- Update start/end G-code for your printer
5. **Verify compatibility** -- Ensure `compatible_printers` lists are correct

## Troubleshooting

| Issue | Solution |
|---|---|
| "OrcaSlicer directory not found" | Verify path to OrcaSlicer profiles directory exists |
| No profiles converted | Check source has `machine/`, `filament/`, `process/` subdirs |
| Missing assets | Ensure cover images and buildplate files exist in source |
| Inheritance errors | Base profiles (`instantiation: false`) are auto-skipped |
| Profiles not appearing in Pandaforge | Check vendor JSON in `resources/profiles/`, verify `instantiation: "true"` |
| GUI won't launch | Install tkinter: `brew install python-tk@3.12` |
| G-code errors | Verify `gcode_flavor: "klipper"` and start/end G-code syntax |

## Contributing

To add field mappings or vendor-specific conversions:
1. Edit `FIELD_MAPPINGS` in `orca_to_pandaforge.py`
2. Add vendor-specific logic in `convert_inherits()` method
3. Test with actual profiles from that vendor

## See Also

- [FLASHFORGE_EXAMPLE.md](FLASHFORGE_EXAMPLE.md) -- Detailed real-world profile example (Adventurer 5M Pro)
- [Profile system overview](../../docs/profile-system.md)

## License

AGPL-3.0 (same as Pandaforge project)
