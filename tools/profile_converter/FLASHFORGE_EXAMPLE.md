# Flashforge Adventurer 5M Pro - Profile Example

This document shows the complete profile structure for the Flashforge Adventurer 5M Pro, which serves as a reference example for converting other Klipper printers.

## Profile Overview

The Flashforge Adventurer 5M Pro is a Klipper-based printer with:
- **Build Volume**: 220x220x220mm
- **Nozzle Options**: 0.25mm, 0.4mm, 0.6mm, 0.8mm
- **Max Speed**: 600mm/s travel
- **Max Acceleration**: 20000mm/s²
- **Firmware**: Klipper
- **Features**: Auxiliary fan, multi-bed type support

## Directory Structure

```
Flashforge/
├── Flashforge.json                                    # Vendor manifest
├── machine/
│   ├── fdm_machine_common.json                        # Base: All FDM machines
│   ├── fdm_flashforge_common.json                     # Base: All Flashforge
│   ├── fdm_adventurer5m_common.json                   # Base: AD5M series
│   ├── Flashforge Adventurer 5M Pro.json              # Model definition
│   ├── Flashforge Adventurer 5M Pro 0.25 Nozzle.json # Instantiation
│   ├── Flashforge Adventurer 5M Pro 0.4 Nozzle.json  # Instantiation
│   ├── Flashforge Adventurer 5M Pro 0.6 Nozzle.json  # Instantiation
│   └── Flashforge Adventurer 5M Pro 0.8 Nozzle.json  # Instantiation
├── filament/
│   ├── fdm_filament_common.json                       # Base: All filaments
│   ├── fdm_filament_pla.json                          # Base: PLA materials
│   ├── fdm_filament_pet.json                          # Base: PETG materials
│   ├── fdm_filament_abs.json                          # Base: ABS materials
│   ├── Generic PLA @FF AD5M Pro.json                  # Instantiation
│   ├── Generic PETG @FF AD5M Pro.json                 # Instantiation
│   ├── Generic ABS @FF AD5M Pro.json                  # Instantiation
│   └── [Brand-specific filaments...]
├── process/
│   ├── fdm_process_common.json                        # Base: All processes
│   ├── fdm_process_flashforge_common.json             # Base: Flashforge
│   ├── fdm_process_flashforge_0.20.json               # Base: 0.20mm layer
│   ├── 0.20mm Standard @Flashforge AD5M Pro.json      # Instantiation
│   ├── 0.12mm Fine @Flashforge AD5M Pro.json          # Instantiation
│   └── [Other quality presets...]
└── [Assets: images, STL models, textures]
```

## Inheritance Chain

### Machine Profile Inheritance

```
fdm_machine_common (base for all FDM)
  ↓ inherits
fdm_flashforge_common (Flashforge defaults)
  ↓ inherits
fdm_adventurer5m_common (AD5M series specifics)
  ↓ inherits
Flashforge Adventurer 5M Pro 0.4 Nozzle (final instantiation)
```

## Complete Profile Examples

### 1. Model Definition (Flashforge Adventurer 5M Pro.json)

```json
{
    "type": "machine_model",
    "name": "Flashforge Adventurer 5M Pro",
    "model_id": "Flashforge-Adventurer-5M-Pro",
    "nozzle_diameter": "0.25;0.4;0.6;0.8",
    "machine_tech": "FFF",
    "family": "Flashforge",
    "bed_model": "flashforge_adventurer5m_series_buildplate_model.STL",
    "bed_texture": "flashforge_adventurer5mpro_buildplate_texture.png",
    "default_bed_type": "Textured PEI Plate",
    "hotend_model": "flashforge_adventurer_5m_series_hotend.STL",
    "default_materials": "Generic PLA @FF AD5M Pro;Generic PETG @FF AD5M Pro;Generic ABS @FF AD5M Pro"
}
```

**Key Points:**
- Defines the printer model and available nozzle sizes
- References 3D models and textures for UI visualization
- Lists default materials

### 2. Base Profile (fdm_adventurer5m_common.json)

```json
{
    "type": "machine",
    "name": "fdm_adventurer5m_common",
    "inherits": "fdm_flashforge_common",
    "from": "system",
    "instantiation": "false",
    "gcode_flavor": "klipper",
    "printable_area": ["-110x-110", "110x-110", "110x110", "-110x110"],
    "printable_height": "220",
    "auxiliary_fan": "1",
    "machine_max_acceleration_e": ["5000", "5000"],
    "machine_max_acceleration_extruding": ["20000", "20000"],
    "machine_max_acceleration_retracting": ["5000", "5000"],
    "machine_max_acceleration_travel": ["20000", "20000"],
    "machine_max_acceleration_x": ["20000", "20000"],
    "machine_max_acceleration_y": ["20000", "20000"],
    "machine_max_acceleration_z": ["500", "500"],
    "machine_max_speed_e": ["30", "30"],
    "machine_max_speed_x": ["600", "600"],
    "machine_max_speed_y": ["600", "600"],
    "machine_max_speed_z": ["20", "20"],
    "machine_max_jerk_e": ["2.5", "2.5"],
    "machine_max_jerk_x": ["9", "9"],
    "machine_max_jerk_y": ["9", "9"],
    "machine_max_jerk_z": ["3", "3"],
    "printer_settings_id": "Flashforge",
    "retraction_minimum_travel": ["1"],
    "retract_before_wipe": ["100%"],
    "deretraction_speed": ["35"],
    "z_hop": ["0.4"],
    "support_multi_bed_types": "1",
    "default_filament_profile": ["Generic PLA @FF AD5M Pro"],
    "machine_start_gcode": "M190 S[bed_temperature_initial_layer_single]\nM104 S[nozzle_temperature_initial_layer]\nG90\nM83\nG1 Z5 F6000\nG1 E-0.2 F800\nG1 X110 Y-110 F6000\nG1 E2 F800\nG1 Y-110 X55 Z0.25 F4800\nG1 X-55 E8 F2400\nG1 Y-109.6 F2400\nG1 X55 E5 F2400\nG1 Y-110 X55 Z0.45 F4800\nG1 X-55 E8 F2400\nG1 Y-109.6 F2400\nG1 X55 E5 F2400\nG92 E0",
    "machine_end_gcode": "G1 E-3 F3600\nG0 X50 Y50 F30000\nM104 S0 ; turn off temperature",
    "use_relative_e_distances": "1",
    "z_hop_types": "Auto Lift",
    "retraction_speed": ["35"],
    "wipe_distance": "2",
    "thumbnails": ["140x110"]
}
```

**Key Points:**
- `instantiation: "false"` - This is a base profile, not selectable by users
- `gcode_flavor: "klipper"` - Critical for Klipper printers
- Klipper kinematics: max speeds, accelerations, jerk values
- Start/end G-code with Klipper-compatible commands
- `use_relative_e_distances: "1"` - Klipper standard

### 3. Nozzle Variant (Flashforge Adventurer 5M Pro 0.4 Nozzle.json)

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

**Key Points:**
- `instantiation: "true"` - User-selectable profile
- Inherits all settings from `fdm_adventurer5m_common`
- Overrides nozzle-specific settings (diameter, layer heights, retraction)
- Links to default print profile

### 4. Filament Profile (Generic PLA @FF AD5M Pro.json)

```json
{
    "type": "filament",
    "name": "Generic PLA @FF AD5M Pro",
    "inherits": "fdm_filament_pla",
    "from": "system",
    "setting_id": "GFPLA01",
    "filament_id": "GFL01",
    "instantiation": "true",
    "filament_flow_ratio": ["0.98"],
    "filament_max_volumetric_speed": ["25"],
    "hot_plate_temp_initial_layer": ["60"],
    "hot_plate_temp": ["55"],
    "slow_down_layer_time": ["6"],
    "slow_down_min_speed": ["20"],
    "support_material_interface_fan_speed": ["100"],
    "additional_cooling_fan_speed": ["100"],
    "filament_start_gcode": ["; filament start gcode\n;right_extruder_material: PLA\n"],
    "filament_end_gcode": ["; filament end gcode\n"],
    "filament_diameter": ["1.75"],
    "enable_pressure_advance": ["1"],
    "pressure_advance": ["0.025"],
    "nozzle_temperature_initial_layer": ["215"],
    "nozzle_temperature": ["210"],
    "nozzle_temperature_range_high": ["230"],
    "nozzle_temperature_range_low": ["190"],
    "compatible_printers": [
        "Flashforge Adventurer 5M Pro 0.25 Nozzle",
        "Flashforge Adventurer 5M Pro 0.4 Nozzle",
        "Flashforge Adventurer 5M Pro 0.6 Nozzle",
        "Flashforge Adventurer 5M Pro 0.8 Nozzle"
    ]
}
```

**Key Points:**
- `enable_pressure_advance: ["1"]` - Enabled for Klipper
- `pressure_advance: ["0.025"]` - Tuned value for PLA
- Temperature ranges for UI sliders
- `compatible_printers` - Lists all compatible nozzle variants

### 5. Process Profile (0.20mm Standard @Flashforge AD5M Pro.json)

```json
{
    "type": "process",
    "name": "0.20mm Standard @Flashforge AD5M Pro",
    "inherits": "fdm_process_flashforge_0.20",
    "from": "system",
    "setting_id": "GP007",
    "instantiation": "true",
    "description": "Standard printing profile with good balance of speed and quality. Suitable for most general printing cases.",
    "bridge_speed": "45",
    "default_acceleration": "15000",
    "initial_layer_speed": "45",
    "outer_wall_acceleration": "6000",
    "overhang_totally_speed": "10",
    "support_interface_speed": "80",
    "support_speed": "180",
    "top_surface_speed": "180",
    "top_surface_acceleration": "3000",
    "travel_acceleration": "15000",
    "travel_speed": "450",
    "filename_format": "{input_filename_base}_{filament_type[0]}_{print_time}.gcode",
    "compatible_printers": ["Flashforge Adventurer 5M Pro 0.4 Nozzle"]
}
```

**Key Points:**
- Balanced speeds for quality and performance
- Klipper-appropriate accelerations (15000mm/s² default)
- High travel speed (450mm/s) leveraging Klipper capabilities
- `compatible_printers` - Specific to 0.4mm nozzle

## Vendor Manifest (Flashforge.json)

```json
{
    "name": "Flashforge",
    "version": "02.05.00.66",
    "force_update": "0",
    "description": "Flashforge configurations",
    "machine_model_list": [
        {
            "name": "Flashforge Adventurer 5M Pro",
            "sub_path": "machine/Flashforge Adventurer 5M Pro.json"
        }
    ],
    "process_list": [
        {"name": "fdm_process_common", "sub_path": "process/fdm_process_common.json"},
        {"name": "0.20mm Standard @Flashforge AD5M Pro", "sub_path": "process/0.20mm Standard @Flashforge AD5M Pro.json"},
        ...
    ],
    "filament_list": [
        {"name": "fdm_filament_common", "sub_path": "filament/fdm_filament_common.json"},
        {"name": "Generic PLA @FF AD5M Pro", "sub_path": "filament/Generic PLA @FF AD5M Pro.json"},
        ...
    ],
    "machine_list": [
        {"name": "fdm_machine_common", "sub_path": "machine/fdm_machine_common.json"},
        {"name": "Flashforge Adventurer 5M Pro 0.4 Nozzle", "sub_path": "machine/Flashforge Adventurer 5M Pro 0.4 Nozzle.json"},
        ...
    ]
}
```

## Klipper-Specific Settings Summary

### Critical Settings for Klipper Printers

1. **G-code Flavor**
   ```json
   "gcode_flavor": "klipper"
   ```

2. **Pressure Advance**
   ```json
   "enable_pressure_advance": ["1"],
   "pressure_advance": ["0.025"]
   ```

3. **Kinematics Limits**
   ```json
   "machine_max_acceleration_x": ["20000", "20000"],
   "machine_max_speed_x": ["600", "600"],
   "machine_max_jerk_x": ["9", "9"]
   ```

4. **Relative E Distances**
   ```json
   "use_relative_e_distances": "1"
   ```

5. **Start G-code Template**
   ```gcode
   M190 S[bed_temperature_initial_layer_single]  ; Wait for bed
   M104 S[nozzle_temperature_initial_layer]      ; Set nozzle temp
   G90                                            ; Absolute positioning
   M83                                            ; Relative E
   G28                                            ; Home (Klipper)
   ```

## Conversion Checklist

When converting a new Klipper printer to Pandaforge format:

- [ ] Set `gcode_flavor: "klipper"`
- [ ] Enable pressure advance in filament profiles
- [ ] Set appropriate Klipper kinematics (speeds, accelerations, jerk)
- [ ] Use `use_relative_e_distances: "1"`
- [ ] Update start/end G-code for Klipper commands
- [ ] Create base profiles with `instantiation: "false"`
- [ ] Create nozzle variants with `instantiation: "true"`
- [ ] Set `compatible_printers` lists correctly
- [ ] Include 3D models and textures for UI
- [ ] Generate vendor JSON manifest
- [ ] Validate with `validate_profiles.py`

## Testing Converted Profiles

1. **Load in Pandaforge**: Verify profiles appear in UI
2. **Slice Test Model**: Generate G-code with converted profile
3. **Inspect G-code**: Check for Klipper-specific commands
4. **Test Print**: Print calibration cube or benchy
5. **Tune Pressure Advance**: Adjust PA values per filament
6. **Verify Speeds**: Ensure speeds match printer capabilities

## Common Issues and Solutions

### Issue: Profiles don't appear in Pandaforge
- Check `instantiation: "true"` in user-selectable profiles
- Verify vendor JSON is in `resources/profiles/`
- Ensure profile names match in vendor JSON

### Issue: G-code errors
- Verify `gcode_flavor: "klipper"`
- Check start/end G-code syntax
- Test G-code commands in Klipper console

### Issue: Poor print quality
- Tune pressure advance values
- Adjust acceleration/jerk limits
- Verify speed settings are appropriate for printer

## References

- [Klipper Configuration Reference](https://www.klipper3d.org/Config_Reference.html)
- [Klipper Pressure Advance](https://www.klipper3d.org/Pressure_Advance.html)
- [BambuStudio Profile Format](https://github.com/bambulab/BambuStudio/wiki)
- [OrcaSlicer Profiles](https://github.com/SoftFever/OrcaSlicer/tree/main/resources/profiles)
