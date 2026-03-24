# Klipper UI Components

Three custom components in `src/slic3r/GUI/Klipper/`.

## BedPlateSelector

**Files:** `BedPlateSelector.cpp`, `BedPlateSelector.hpp`

Dropdown selector for bed plate types with temperature recommendations.

**Features:**
- Bed plate types: Cool, Engineering, High Temp, Textured PEI, Custom
- Temperature recommendations per plate type
- G-code variable export for template substitution (`{bed_plate_type}`)
- Stores settings in AppConfig under `"klipper"` section

**API:**
```cpp
BedPlateSelector(wxWindow* parent);
BedPlateType GetSelectedBedPlate() const;
void SetBedPlate(BedPlateType type);
int GetBedTemp(bool is_first_layer) const;
wxString GetGCodeVariable() const;
```

## NozzleSelector

**Files:** `NozzleSelector.cpp`, `NozzleSelector.hpp`

Nozzle diameter selector with automatic print setting scaling.

**Features:**
- Sizes: 0.2mm, 0.4mm, 0.6mm, 0.8mm (with presets)
- Auto-scales: line width, speed, retraction, layer height
- Applies changes to `DynamicPrintConfig`

**API:**
```cpp
NozzleSelector(wxWindow* parent);
float GetNozzleDiameter() const;
void SetNozzleDiameter(float d);
void ApplyScalingToConfig(DynamicPrintConfig& config);
const NozzlePreset* GetCurrentPreset() const;
```

**Line counts:** 187 lines

## FanControlPanel

**Files:** `FanControlPanel.cpp`, `FanControlPanel.hpp`

Moonraker HTTP API integration for real-time fan control.

**Features:**
- Controls: Part cooling, Chamber, Aux, Exhaust fans
- Auto-polling from printer (2-second interval)
- Predefined printer profiles: Creality K1, Qidi Q2, Flashforge 5M, Centauri Carbon
- Uses libcurl for HTTP communication

**API:**
```cpp
FanControlPanel(wxWindow* parent);
void SetPrinterProfile(const PrinterProfile& profile);
void SetPrinterURL(const wxString& url);
bool SendGCode(const wxString& gcode);
void StartPolling(int interval_ms = 2000);
void StopPolling();
```

**Line counts:** 558 lines

## Pressure Advance

Pressure advance settings are applied in `GCodeWriter::set_pressure_advance()`.

**Implementation in GCode.cpp (at print start):**
```cpp
if (config.enable_pressure_advance.get_at(extruder_id)) {
    double pa_value = config.pressure_advance.get_at(extruder_id);
    gcode += m_writer.set_pressure_advance(pa_value, extruder_id);
}
```

**G-code output format:**
```gcode
SET_PRESSURE_ADVANCE EXTRUDER=extruder ADVANCE=0.0585
```

**Testing pressure advance:**
- Enable in filament settings: `enable_pressure_advance = 1`
- Set value: `pressure_advance = 0.0585` (example)
- Check G-code output for `SET_PRESSURE_ADVANCE` line

## MainFrame Integration

To add these components to the main UI, modify `src/slic3r/GUI/MainFrame.cpp`:

```cpp
// 1. Add includes
#include "Klipper/BedPlateSelector.hpp"
#include "Klipper/NozzleSelector.hpp"
#include "Klipper/FanControlPanel.hpp"

// 2. Add member variables to MainFrame class
class MainFrame : public DPIFrame {
    // ... existing members ...
    BedPlateSelector* m_bed_plate_selector = nullptr;
    NozzleSelector* m_nozzle_selector = nullptr;
    FanControlPanel* m_fan_control = nullptr;
};

// 3. Create UI in initialization method
void MainFrame::CreateKlipperUI() {
    m_bed_plate_selector = new BedPlateSelector(parent_panel);
    m_nozzle_selector = new NozzleSelector(parent_panel);
    m_fan_control = new FanControlPanel(parent_panel);
}
```

**Placement decision pending:** Toolbar vs Side panel (side panel preferred for FanControlPanel).
