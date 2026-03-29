# BambuStudio Profile Creation Rules

> Note: the exact branch-specific vendor loader schema now lives in `docs/02-reference/profile-system.md`. Use this file as a pattern guide, but use the reference doc for source-of-truth loader behavior.

> **Version:** 1.1  
> **Last Updated:** March 10, 2026  
> **Applies to:** pandaforge / BambuStudio v2.5.0.66
>
> **Changes in v1.1:**
> - Added intermediate layer profile documentation
> - Added value format rules (strings vs arrays)
> - Updated inheritance chain examples
> - Added troubleshooting for intermediate layer loading errors

---

## Table of Contents

1. [File Structure Rules](#file-structure-rules)
2. [Machine Profile Rules](#machine-profile-rules)
3. [Process Profile Rules](#process-profile-rules)
4. [Filament Profile Rules](#filament-profile-rules)
5. [JSON Syntax Rules](#json-syntax-rules)
6. [Inheritance & Loading Order](#inheritance--loading-order)
7. [Common Errors & Solutions](#common-errors--solutions)
8. [Nozzle Size Specifications](#nozzle-size-specifications)
9. [BBL X1C Profile Reference](#bbl-x1c-profile-reference)
10. [Quick Checklist](#quick-checklist)

---

## File Structure Rules

### Directory Layout
```
resources/profiles/
├── <Brand>.json              # Main profile registry (REQUIRED)
├── <Brand>/
│   ├── machine/              # Machine profiles
│   │   ├── fdm_*_common.json # Base machine definitions
│   │   └── <Printer> <X.X> Nozzle.json  # Instantiation profiles
│   ├── process/              # Process (print) profiles
│   │   ├── fdm_process_*.json  # Base process definitions
│   │   └── <X.XXmm> <Type> @<Brand> <Model>.json  # Instantiation profiles
│   └── filament/             # Filament profiles
│       ├── fdm_filament_*.json  # Base filament definitions
│       └── <Name> @<Brand> <Model>.json  # Instantiation profiles
```

### Naming Conventions

**Machine Files:**
- Base: `fdm_<family>_common.json`
- Instantiation: `<Brand> <Model> <X.X> Nozzle.json`
  - Example: `Flashforge Adventurer 5M Pro 0.4 Nozzle.json`

**Process Files:**
- Base: `fdm_process_<family>_common.json` or `fdm_process_<family>_0.XX.json`
- Instantiation: `<X.XXmm> <Type> @<Brand> <Model>.json`
  - Example: `0.20mm Standard @Flashforge AD5M Pro.json`
  - Multi-nozzle: `0.30mm Standard @Flashforge AD5M Pro 0.6 nozzle.json`

**Filament Files:**
- Base: `fdm_filament_<material>.json`
- Vendor base: `<Vendor> <Material> @base.json`
- Instantiation: `<Name> @<Brand> <Model>.json`
  - Example: `Generic PLA @FF AD5M Pro.json`

---

## Machine Profile Rules

### Base Machine Profile (instantiation: "false")
```json
{
    "type": "machine",
    "name": "fdm_adventurer5m_common",
    "inherits": "fdm_flashforge_common",
    "from": "system",
    "instantiation": "false",
    "gcode_flavor": "klipper",
    "printable_area": [...],
    "machine_max_acceleration_x": ["20000", "20000"],
    "machine_start_gcode": "...",
    "machine_end_gcode": "..."
}
```

### Instantiation Machine Profile (instantiation: "true")
```json
{
    "type": "machine",
    "name": "Flashforge Adventurer 5M Pro 0.4 Nozzle",
    "inherits": "fdm_adventurer5m_common",
    "from": "system",
    "setting_id": "GM_FF_AD5MP_004",
    "instantiation": "true",
    "printer_model": "Flashforge Adventurer 5M Pro",
    "default_print_profile": "0.20mm Standard @Flashforge AD5M Pro",
    "nozzle_diameter": ["0.4"],
    "printer_variant": "0.4",
    "max_layer_height": ["0.28"],
    "min_layer_height": ["0.08"],
    "retraction_length": ["0.8"],
    "nozzle_type": "stainless_steel"
}
```

### Multi-Nozzle Machine Profile Pattern
For nozzles that inherit from 0.4 Nozzle:
```json
{
    "type": "machine",
    "name": "Flashforge Adventurer 5M Pro 0.6 Nozzle",
    "inherits": "Flashforge Adventurer 5M Pro 0.4 Nozzle",
    "from": "system",
    "setting_id": "GM_FF_AD5MP_006",
    "instantiation": "true",
    "printer_model": "Flashforge Adventurer 5M Pro",
    "printer_variant": "0.6",
    "default_print_profile": "0.30mm Standard @Flashforge AD5M Pro 0.6 nozzle",
    "nozzle_diameter": ["0.6"],
    "max_layer_height": ["0.42"],
    "min_layer_height": ["0.12"],
    "retraction_length": ["1.2"],
    "upward_compatible_machine": ["Flashforge Adventurer 5M Pro 0.4 Nozzle"]
}
```

### Machine Profile Critical Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `type` | YES | string | Always `"machine"` |
| `name` | YES | string | Unique identifier |
| `inherits` | YES | string | Parent profile name |
| `from` | YES | string | Always `"system"` |
| `setting_id` | YES for instantiation | string | Unique code (e.g., `GM_FF_AD5MP_004`) |
| `instantiation` | YES | string | `"true"` or `"false"` |
| `printer_model` | YES for instantiation | string | Links to machine_model |
| `printer_variant` | YES for instantiation | string | Nozzle size (e.g., `"0.4"`) |
| `default_print_profile` | YES for instantiation | string | Default process profile name |
| `nozzle_diameter` | YES for instantiation | array | Single string element `["0.4"]` |
| `max_layer_height` | YES for instantiation | array | Single string element |
| `min_layer_height` | YES for instantiation | array | Single string element |
| `retraction_length` | YES for instantiation | array | Single string element |
| `nozzle_type` | CONDITIONAL | string | Only for base nozzle (0.4), NOT for inherited |
| `upward_compatible_machine` | NO | array | List of compatible machine names |

### Machine Model File
```json
{
    "type": "machine_model",
    "name": "Flashforge Adventurer 5M Pro",
    "model_id": "Flashforge-Adventurer-5M-Pro",
    "nozzle_diameter": "0.25;0.4;0.6;0.8",
    "machine_tech": "FFF",
    "family": "Flashforge",
    "bed_model": "...stl",
    "bed_texture": "...png",
    "default_bed_type": "Textured PEI Plate",
    "default_materials": "Generic PLA @FF AD5M Pro;Generic PETG @FF AD5M Pro"
}
```

---

## Process Profile Rules

### Base Process Profile (instantiation: "false")
```json
{
    "type": "process",
    "name": "fdm_process_flashforge_common",
    "inherits": "fdm_process_common",
    "from": "system",
    "instantiation": "false",
    "line_width": "0.42",
    "layer_height": "0.2",
    "compatible_printers": []
}
```

### Intermediate Layer Profile (instantiation: "false")
Used for layer-height or nozzle-specific defaults to reduce duplication:
```json
{
    "type": "process",
    "name": "fdm_process_flashforge_0.20",
    "inherits": "fdm_process_flashforge_common",
    "from": "system",
    "instantiation": "false",
    "layer_height": "0.20",
    "initial_layer_print_height": "0.24",
    "inner_wall_speed": "300",
    "outer_wall_speed": "180",
    "sparse_infill_speed": "350"
}
```

### Instantiation Process Profile (instantiation: "true")
```json
{
    "type": "process",
    "name": "0.20mm Standard @Flashforge AD5M Pro",
    "inherits": "fdm_process_flashforge_0.20",
    "from": "system",
    "setting_id": "GP007",
    "instantiation": "true",
    "description": "Standard printing profile...",
    "bridge_speed": "45",
    "default_acceleration": "15000",
    "compatible_printers": ["Flashforge Adventurer 5M Pro 0.4 Nozzle"]
}
```

### Multi-Nozzle Process Profile
```json
{
    "type": "process",
    "name": "0.30mm Standard @Flashforge AD5M Pro 0.6 nozzle",
    "inherits": "fdm_process_flashforge_common",
    "from": "system",
    "setting_id": "GP0306",
    "instantiation": "true",
    "description": "Default profile for 0.6mm nozzle...",
    "layer_height": "0.30",
    "line_width": "0.65",
    "compatible_printers": ["Flashforge Adventurer 5M Pro 0.6 Nozzle"]
}
```

### Process Profile Critical Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `type` | YES | string | Always `"process"` |
| `name` | YES | string | Unique identifier |
| `inherits` | YES | string | Parent profile name |
| `from` | YES | string | Always `"system"` |
| `setting_id` | YES for instantiation | string | Unique code (e.g., `GP007`) |
| `instantiation` | YES | string | `"true"` or `"false"` |
| `description` | YES for instantiation | string | User-visible description |
| `layer_height` | YES for instantiation | string | Layer height in mm |
| `line_width` | YES for instantiation | string | Line width in mm |
| `compatible_printers` | YES for instantiation | array | List of machine names |

### Speed Settings Format

**Single extruder (simpler format):**
```json
"inner_wall_speed": "200",
"outer_wall_speed": "150",
"sparse_infill_speed": "250"
```

**Multi-extruder (array format for BBL compatibility):**
```json
"inner_wall_speed": ["150", "180"],
"outer_wall_speed": ["120", "150"],
"sparse_infill_speed": ["100", "200"]
```

---

## Filament Profile Rules

### Base Filament Profile (instantiation: "false")
```json
{
    "type": "filament",
    "name": "fdm_filament_pla",
    "inherits": "fdm_filament_common",
    "from": "system",
    "instantiation": "false",
    "filament_type": ["PLA"],
    "nozzle_temperature": ["210"]
}
```

### Vendor Base Profile (instantiation: "false")
```json
{
    "type": "filament",
    "name": "SUNLU PLA+ @base",
    "inherits": "fdm_filament_pla",
    "from": "system",
    "filament_id": "SUN01",
    "instantiation": "false",
    "filament_vendor": ["SUNLU"],
    "filament_flow_ratio": ["0.98"],
    "nozzle_temperature": ["215"]
}
```

### Instantiation Filament Profile (instantiation: "true")
```json
{
    "type": "filament",
    "name": "SUNLU PLA+ @FF AD5M Pro",
    "inherits": "SUNLU PLA+ @base",
    "from": "system",
    "setting_id": "SUN01_AD5M",
    "instantiation": "true",
    "compatible_printers": [
        "Flashforge Adventurer 5M Pro 0.4 Nozzle",
        "Flashforge Adventurer 5M Pro 0.6 Nozzle",
        "Flashforge Adventurer 5M Pro 0.8 Nozzle"
    ]
}
```

### Filament Profile Critical Fields

| Field | Required | Type | Notes |
|-------|----------|------|-------|
| `type` | YES | string | Always `"filament"` |
| `name` | YES | string | Unique identifier |
| `inherits` | YES | string | Parent profile name |
| `from` | YES | string | Always `"system"` |
| `filament_id` | YES for vendor base | string | Unique material code |
| `setting_id` | YES for instantiation | string | Unique code |
| `instantiation` | YES | string | `"true"` or `"false"` |
| `filament_vendor` | YES for vendor | array | Vendor name |
| `compatible_printers` | YES for instantiation | array | List of ALL machine names |

---

## Value Format Rules

### Process Profile Value Format

**Use plain strings for ALL values in process profiles:**
```json
// CORRECT - String values:
"layer_height": "0.20",
"inner_wall_speed": "300",
"outer_wall_speed": "180",
"default_acceleration": "15000"
```

**Array format causes errors in process profiles:**
```json
// WRONG - Arrays will cause parsing errors:
"inner_wall_speed": ["300"],
"outer_wall_speed": ["180"],
"default_acceleration": ["15000"]
```

### Machine Profile Value Format

**Use arrays for machine parameters:**
```json
// CORRECT - Arrays for machine settings:
"nozzle_diameter": ["0.4"],
"retraction_length": ["0.8"],
"max_layer_height": ["0.28"],
"machine_max_acceleration_x": ["20000", "20000"]
```

### Summary Table

| Profile Type | Value Format | Example |
|--------------|--------------|---------|
| Process | String | `"inner_wall_speed": "300"` |
| Machine | Array | `"nozzle_diameter": ["0.4"]` |
| Filament | Array | `"nozzle_temperature": ["210"]` |

---

## JSON Syntax Rules

### Critical JSON Requirements

1. **No trailing commas** in arrays or objects
   ```json
   // WRONG:
   "compatible_printers": ["Machine 1", "Machine 2",]
   
   // CORRECT:
   "compatible_printers": ["Machine 1", "Machine 2"]
   ```

2. **String values must be quoted**
   ```json
   // WRONG:
   "layer_height": 0.20
   
   // CORRECT:
   "layer_height": "0.20"
   ```

3. **Arrays for machine parameters**
   ```json
   // Single value as array:
   "nozzle_diameter": ["0.4"],
   "retraction_length": ["0.8"]
   
   // Multi-extruder values:
   "nozzle_diameter": ["0.4", "0.4"],
   "retraction_length": ["0.8", "0.8"]
   ```

4. **No comments** in JSON files

---

## Inheritance & Loading Order

### Loading Order in <Brand>.json

**CRITICAL:** Files must be listed in dependency order (parents before children).

```json
{
    "process_list": [
        // 1. Base processes first
        {"name": "fdm_process_common", "sub_path": "process/fdm_process_common.json"},
        {"name": "fdm_process_flashforge_common", "sub_path": "process/fdm_process_flashforge_common.json"},
        
        // 2. Intermediate layer profiles (nozzle/layer specific)
        {"name": "fdm_process_flashforge_0.20", "sub_path": "process/fdm_process_flashforge_0.20.json"},
        {"name": "fdm_process_flashforge_0.25_nozzle", "sub_path": "process/fdm_process_flashforge_0.25_nozzle.json"},
        {"name": "fdm_process_flashforge_0.30", "sub_path": "process/fdm_process_flashforge_0.30.json"},
        {"name": "fdm_process_flashforge_0.40", "sub_path": "process/fdm_process_flashforge_0.40.json"},
        
        // 3. Then instantiation processes
        {"name": "0.20mm Standard @Flashforge AD5M Pro", "sub_path": "process/0.20mm Standard @Flashforge AD5M Pro.json"}
    ],
    "machine_list": [
        // 1. Base machines first
        {"name": "fdm_machine_common", "sub_path": "machine/fdm_machine_common.json"},
        {"name": "fdm_flashforge_common", "sub_path": "machine/fdm_flashforge_common.json"},
        {"name": "fdm_adventurer5m_common", "sub_path": "machine/fdm_adventurer5m_common.json"},
        
        // 2. Parent instantiation machine BEFORE children
        {"name": "Flashforge Adventurer 5M Pro 0.4 Nozzle", "sub_path": "machine/Flashforge Adventurer 5M Pro 0.4 Nozzle.json"},
        
        // 3. Child machines that inherit from 0.4
        {"name": "Flashforge Adventurer 5M Pro 0.25 Nozzle", "sub_path": "machine/Flashforge Adventurer 5M Pro 0.25 Nozzle.json"},
        {"name": "Flashforge Adventurer 5M Pro 0.6 Nozzle", "sub_path": "machine/Flashforge Adventurer 5M Pro 0.6 Nozzle.json"},
        {"name": "Flashforge Adventurer 5M Pro 0.8 Nozzle", "sub_path": "machine/Flashforge Adventurer 5M Pro 0.8 Nozzle.json"}
    ]
}
```

### Inheritance Chain

**Machine Profiles:**
```
fdm_machine_common
    ↳ fdm_flashforge_common
        ↳ fdm_adventurer5m_common
            ↳ Flashforge Adventurer 5M Pro 0.4 Nozzle (instantiation: true)
                ↳ Flashforge Adventurer 5M Pro 0.25 Nozzle
                ↳ Flashforge Adventurer 5M Pro 0.6 Nozzle
                ↳ Flashforge Adventurer 5M Pro 0.8 Nozzle
```

**Process Profiles (with Intermediate Layers):**
```
fdm_process_common
    ↳ fdm_process_flashforge_common
        ↳ fdm_process_flashforge_0.20
        │   ↳ 0.20mm Standard @Flashforge AD5M Pro
        │   ↳ 0.20mm Strength @Flashforge AD5M Pro
        │   ↳ 0.08mm Extra Fine @Flashforge AD5M Pro
        │   ↳ 0.08mm High Quality @Flashforge AD5M Pro
        │   ↳ 0.12mm Fine @Flashforge AD5M Pro
        │   ↳ 0.12mm High Quality @Flashforge AD5M Pro
        │   ↳ 0.16mm Optimal @Flashforge AD5M Pro
        │   ↳ 0.16mm High Quality @Flashforge AD5M Pro
        │   ↳ 0.24mm Draft @Flashforge AD5M Pro
        │   ↳ 0.28mm Extra Draft @Flashforge AD5M Pro
        │
        ↳ fdm_process_flashforge_0.25_nozzle
        │   ↳ 0.20mm Extra Draft @Flashforge AD5M Pro 0.25 nozzle
        │
        ↳ fdm_process_flashforge_0.30
        │   ↳ 0.30mm Standard @Flashforge AD5M Pro 0.6 nozzle
        │   ↳ 0.30mm Strength @Flashforge AD5M Pro 0.6 nozzle
        │
        ↳ fdm_process_flashforge_0.40
            ↳ 0.40mm Standard @Flashforge AD5M Pro 0.8 nozzle
```

---

## Common Errors & Solutions

### Error: "Failed loading configuration file"

**Causes:**
1. JSON syntax error (trailing comma, unquoted string)
2. Missing required field
3. File referenced in <Brand>.json doesn't exist
4. Inheritance parent not loaded yet
5. `compatible_printers` references non-existent machine

**Solutions:**
```bash
# Validate all JSON files:
cd resources/profiles/<Brand>
python3 -c "
import json
import os
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.endswith('.json'):
            path = os.path.join(root, f)
            try:
                with open(path) as file:
                    json.load(file)
                print(f'OK: {path}')
            except Exception as e:
                print(f'ERROR: {path}: {e}')
"
```

### Error: Process profile not showing for nozzle

**Cause:** `compatible_printers` doesn't include the machine name.

**Solution:** Update all filament and process profiles to include all machine variants.

### Error: Machine profile inheritance fails

**Cause:** Child machine listed before parent in `machine_list`.

**Solution:** Reorder `machine_list` so parent (0.4 Nozzle) is listed before children (0.25, 0.6, 0.8).

### Error: Filament profile appears as "Default Filament"

**Cause:** Missing `instantiation: "true"` or `compatible_printers` not set.

### Error: Setting values not applying

**Cause:** Array format mismatch. If parent uses arrays `["value"]`, child must also use arrays.

### Error: "Failed loading configuration file" for intermediate layers

**Cause:** Intermediate layer file not registered in `<Brand>.json` or value format inconsistency.

**Solution:** 
1. Ensure intermediate layer is listed in `process_list` BEFORE profiles that inherit from it:
```json
{
    "process_list": [
        {"name": "fdm_process_flashforge_common", "sub_path": "process/fdm_process_flashforge_common.json"},
        {"name": "fdm_process_flashforge_0.20", "sub_path": "process/fdm_process_flashforge_0.20.json"},
        {"name": "fdm_process_flashforge_0.25_nozzle", "sub_path": "process/fdm_process_flashforge_0.25_nozzle.json"},
        {"name": "0.20mm Standard @Flashforge AD5M Pro", "sub_path": "process/0.20mm Standard @Flashforge AD5M Pro.json"}
    ]
}
```

2. Use consistent value formats (strings for process profiles, NOT arrays):
```json
// WRONG - Arrays cause parsing errors in process profiles:
"initial_layer_speed": ["25"],
"outer_wall_speed": ["80"]

// CORRECT - String values for process profiles:
"initial_layer_speed": "25",
"outer_wall_speed": "80"
```

**Note:** Machine profiles use arrays for single values (`["0.4"]`), but process profiles should use plain strings.

---

## Nozzle Size Specifications

| Nozzle | Line Width | Min Layer | Max Layer | Retraction | Default Process |
|--------|------------|-----------|-----------|------------|-----------------|
| 0.25mm | 0.30mm | 0.08mm | 0.20mm | 0.6mm | 0.15mm Standard |
| 0.4mm | 0.42mm | 0.08mm | 0.28mm | 0.8mm | 0.20mm Standard |
| 0.6mm | 0.65mm | 0.12mm | 0.42mm | 1.2mm | 0.30mm Standard |
| 0.8mm | 0.85mm | 0.16mm | 0.56mm | 1.5mm | 0.40mm Standard |

---

## BBL X1C Profile Reference

When creating profiles for Flashforge/AD5M Pro, reference BBL X1C profiles:

**BBL X1C 0.2 nozzle processes:**
- 0.10mm Standard (default)
- 0.12mm Standard
- 0.14mm Standard

**BBL X1C 0.4 nozzle processes:**
- 0.08mm Extra Fine
- 0.12mm Fine
- 0.20mm Standard (default)
- 0.24mm Draft
- 0.28mm Extra Draft

**BBL X1C 0.6 nozzle processes:**
- 0.18mm Standard
- 0.24mm Standard
- 0.30mm Standard (default)
- 0.30mm Strength
- 0.36mm Standard
- 0.42mm Standard

**BBL X1C 0.8 nozzle processes:**
- 0.24mm Standard
- 0.32mm Standard
- 0.40mm Standard (default)
- 0.48mm Standard
- 0.56mm Standard

---

## Quick Checklist

When adding a new nozzle:

- [ ] Update `nozzle_diameter` in machine_model file
- [ ] Create machine profile with correct `inherits`
- [ ] Add machine to `machine_list` AFTER parent (0.4 Nozzle)
- [ ] Create or update intermediate layer profile (e.g., `fdm_process_flashforge_0.25_nozzle`)
- [ ] Register intermediate layer in `process_list` BEFORE instantiation profiles
- [ ] Create process profiles with correct `inherits` (pointing to intermediate layer)
- [ ] Add processes to `process_list` in dependency order
- [ ] Update ALL filament `compatible_printers` to include new nozzle
- [ ] Validate all JSON files
- [ ] Test loading in slicer

When adding a new intermediate layer:

- [ ] Create file with `instantiation: "false"`
- [ ] Ensure `inherits` points to correct parent
- [ ] Add to `process_list` BEFORE profiles that use it
- [ ] Use string values (NOT arrays) for settings
- [ ] Update child profiles to inherit from intermediate layer
- [ ] Remove redundant settings now inherited from intermediate layer

---

*Document maintained for pandaforge profile development.*
