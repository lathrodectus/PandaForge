# Profile System

## Overview

Pandaforge uses BambuStudio's profile system: JSON files organized by vendor, with inheritance chains for machine, filament, and process profiles. Profiles live in `BambuStudio-2.5.0.66/resources/profiles/`.

## Profile Structure

```
resources/profiles/
├── Flashforge/
│   ├── Flashforge.json              # Vendor manifest
│   ├── machine/                     # Machine profiles
│   │   ├── fdm_flashforge_common.json       # Base (not user-selectable)
│   │   ├── Flashforge AD5M Pro.json         # Model definition
│   │   └── Flashforge AD5M Pro 0.4 Nozzle.json  # Nozzle variant (selectable)
│   ├── filament/                    # Filament profiles
│   │   ├── fdm_filament_pla.json            # Base
│   │   └── Generic PLA @FF AD5M Pro.json    # Printer-specific (selectable)
│   └── process/                     # Process/quality profiles
│       ├── fdm_process_common.json          # Base
│       └── 0.20mm Standard @FF AD5M Pro.json  # Quality preset (selectable)
```

## Inheritance Chain

```
fdm_machine_common          (global base)
  └── fdm_vendor_common     (vendor defaults)
      └── fdm_model_common  (model-specific)
          └── Printer 0.4 Nozzle  (user-selectable, instantiation: true)
```

Profiles with `"instantiation": "true"` appear in the UI. Base profiles (`"instantiation": "false"`) provide inherited defaults.

## Key Klipper Settings in Profiles

**Machine:** `gcode_flavor: "klipper"`, kinematics limits, start/end G-code
**Filament:** `enable_pressure_advance: ["1"]`, `pressure_advance: ["0.025"]`
**Process:** Speeds, accelerations, `compatible_printers` list

## Detailed Documentation

- **Profile rules:** [BambuStudio-2.5.0.66/resources/profiles/Profile_rules.md](../BambuStudio-2.5.0.66/resources/profiles/Profile_rules.md)
- **Inheritance chains:** [BambuStudio-2.5.0.66/resources/profiles/Profile_inheritance_chain.md](../BambuStudio-2.5.0.66/resources/profiles/Profile_inheritance_chain.md)
- **Profile converter tool:** [tools/profile_converter/README.md](../tools/profile_converter/README.md)
- **Flashforge example:** [tools/profile_converter/FLASHFORGE_EXAMPLE.md](../tools/profile_converter/FLASHFORGE_EXAMPLE.md)

## Profile Converter

The `tools/profile_converter/` tool converts OrcaSlicer Klipper profiles to Pandaforge format:

```bash
cd tools/profile_converter

# Convert a single vendor
python3 orca_to_pandaforge.py \
    ~/OrcaSlicer-main/resources/profiles/Creality \
    ~/Pandaforge\ Project/BambuStudio-2.5.0.66/resources/profiles/Creality \
    --vendor "Creality"

# Validate converted profiles
python3 validate_profiles.py \
    ~/Pandaforge\ Project/BambuStudio-2.5.0.66/resources/profiles/Creality
```

See [tools/profile_converter/README.md](../tools/profile_converter/README.md) for full usage.
