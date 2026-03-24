# pandaforge Project - Master Plan & Roadmap

**Document Version:** 1.0  
**Date:** March 5, 2026  
**Status:** Post-M1 Review - Restarting from Clean Baseline

---

## Executive Summary

pandaforge is a BambuStudio v2.5.0.66 fork with Klipper-specific enhancements for macOS. This document consolidates all project goals, plans, roadmaps, and lessons learned.

### What Was Accomplished (March 4-5, 2026)
- ✅ Built clean BambuStudio v2.5.0.66 using official Mac Compile Guide
- ✅ Created build documentation (BUILD_GUIDE.md)
- ✅ Compiled Klipper UI components (BedPlateSelector, NozzleSelector, FanControlPanel)
- ⚠️ pandaforge build deadlocked due to parallel build issues (-j8)
- ⚠️ Klipper components compiled but not integrated into Main UI

### Decision: Clean Slate Restart
Nuke everything except working baseline: `BambuStudio-2.5.0.66` + `BambuStudio_dep_2.5.0.66`

---

## Project Vision

### Mission
Create a macOS-native BambuStudio fork optimized for Klipper printers with:
1. **Klipper-specific UI controls** (bed plates, nozzle selectors, fan control)
2. **Moonraker integration** for real-time printer control
3. **Profile converter** for OrcaSlicer → BambuStudio migration
4. **Better Klipper defaults** and G-code templates

### Target Users
- Klipper printer owners on macOS
- Users wanting BambuStudio's UI with Klipper's flexibility
- Users migrating from OrcaSlicer to BambuStudio

---

## Technical Architecture

### Base Platform
| Component | Version | Source |
|-----------|---------|--------|
| BambuStudio | v2.5.0.66 | Official BambuLab |
| wxWidgets | 3.1.5 | BambuLab fork |
| Boost | 1.84.0 | Built from deps |
| CGAL | 5.4.5 | Manual download |
| Build Method | Official Mac Compile Guide | GitHub Wiki |

### Klipper Components (Developed)

#### 1. BedPlateSelector (121 lines)
```cpp
// Dropdown for bed plate selection
// Types: Cool, Engineering, High Temp, Textured PEI, Custom
// Features: Temperature recommendations, G-code variable export
```

#### 2. NozzleSelector (187 lines)
```cpp
// Nozzle diameter selector with auto-scaling
// Sizes: 0.2mm - 0.8mm
// Auto-scales: line width, speed, retraction, layer height
```

#### 3. FanControlPanel (558 lines)
```cpp
// Moonraker HTTP API integration
// Controls: Part, Chamber, Aux, Exhaust fans
// Features: Manual control, auto-polling, printer profiles
// Profiles: Creality K1, Qidi Q2, Flashforge 5M, Centauri Carbon
```

### File Locations (Pre-Cleanup)
```
pandaforge/
├── BambuStudio-2.5.0.66/          # ✅ KEEP - Working baseline
│   ├── src/slic3r/GUI/Klipper/     # Klipper components (compiled)
│   ├── build/                      # Build artifacts
│   └── install_dir/BambuStudio.app # ✅ Working binary (108MB)
├── BambuStudio_dep_2.5.0.66/       # ✅ KEEP - Dependencies
│   └── usr/local/                  # wxWidgets, Boost, etc.
├── pandaforge/                     # ❌ DELETE - Deadlocked fork
├── wx-install/                     # ❌ DELETE - Duplicate
├── wxWidgets/                      # ❌ DELETE - Source (not needed)
├── CGAL-5.3.2/                     # ❌ DELETE - Old version
├── CGAL-5.4.5/                     # ❌ DELETE - Not needed with deps
├── CGAL-5.6.1/                     # ❌ DELETE - Not needed
└── BUILD_GUIDE.md                  # ✅ KEEP - Documentation
```

---

## Development Phases

### Phase 0: Foundation ✅ COMPLETE
**Goal:** Working BambuStudio binary

| Task | Status | Notes |
|------|--------|-------|
| Install Xcode CLI tools | ✅ | `xcode-select --install` |
| Install Homebrew deps | ✅ | cmake, ninja, boost, etc. |
| Build dependencies | ✅ | `BambuStudio_dep_2.5.0.66` |
| Build BambuStudio | ✅ | Binary at `install_dir/BambuStudio.app` |
| Document build process | ✅ | BUILD_GUIDE.md created |

**Exit Criteria:** Clean build from fresh checkout succeeds

---

### Phase 1: Klipper Integration (CURRENT FOCUS)
**Goal:** Add Klipper UI components to main interface

#### 1.1 Fix API Compatibility Issues ✅ DONE
| Issue | Solution |
|-------|----------|
| `wxArrayString` initializer | Move to constructor |
| `wxFont::SetBold()` | Remove (not in wx 3.1) |
| `wxSpinCtrl::SetSuffix()` | Comment out |
| `wxConfigBase` | Use `Slic3r::AppConfig` |
| Include paths | Use relative `../I18N.hpp` |

#### 1.2 Integrate into MainFrame (PENDING)
```cpp
// File: src/slic3r/GUI/MainFrame.cpp

// 1. Add includes near top
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

// 3. Create UI in constructor or init method
void MainFrame::CreateKlipperUI() {
    // Option A: Add to toolbar
    m_bed_plate_selector = new BedPlateSelector(m_toolbar);
    m_toolbar->AddControl(m_bed_plate_selector);
    
    m_nozzle_selector = new NozzleSelector(m_toolbar);
    m_toolbar->AddControl(m_nozzle_selector);
    
    // Option B: Add to side panel (better for FanControlPanel)
    m_fan_control = new FanControlPanel(side_panel);
}
```

**Decision needed:** Toolbar vs Side panel placement

---

### Phase 2: Moonraker Integration
**Goal:** Real-time printer communication

| Feature | Priority | Technical Approach |
|---------|----------|-------------------|
| Fan speed control | High | HTTP POST to Moonraker API |
| Temperature monitoring | High | Poll `/api/printer` endpoint |
| Print status | Medium | WebSocket connection |
| Camera feed | Low | Embed MJPEG stream |

#### Moonraker API Endpoints
```
GET  /api/printer          # Get printer status
POST /api/printer/command  # Send G-code
GET  /api/server/info      # Server info
```

---

### Phase 3: Profile Converter
**Goal:** OrcaSlicer → BambuStudio profile migration

**Tool:** `tools/profile_converter/converter.py`

| Feature | Status |
|---------|--------|
| Basic JSON conversion | ✅ Exists |
| Nozzle scaling | ✅ Exists |
| Printer adaptation | ✅ Exists |
| UI integration | ❌ Not done |

**Usage:**
```bash
python3 tools/profile_converter/converter.py \
  input_orca_profile.json \
  output_dir/ \
  --nozzle 0.6 \
  --printer "Creality K1"
```

---

### Phase 4: Klipper G-code Templates
**Goal:** Better default G-code for Klipper printers

**Features:**
- Bed plate variable substitution (`{bed_plate_type}`)
- Klipper-optimized start/end G-code
- Pressure advance integration
- Input shaping hints

---

## Build System

### Official Method (PROVEN WORKING)
Based on [BambuLab Mac Compile Guide](https://github.com/bambulab/BambuStudio/wiki/Mac-Compile-Guide)

```bash
# Step 1: Build deps (one-time, 30-60 min)
cd BambuStudio-2.5.0.66/deps && mkdir build && cd build
cmake ../ -DDESTDIR=".../BambuStudio_dep" -DOPENSSL_ARCH="darwin64-arm64-cc"
make -j8

# Step 2: Build app (30-60 min)
cd ../.. && mkdir build && cd build
cmake .. \
  -DCMAKE_PREFIX_PATH=".../BambuStudio_dep/usr/local" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_MACOSX_BUNDLE=ON
cmake --build . --target install --config Release -j8
```

### Key Lessons Learned
1. **Use `-j4` not `-j8`** - Prevents deadlock on large files
2. **Use symlink for deps** - Avoids space-in-path issues
3. **Fix wx-config paths** - Must point to actual dep location
4. **Boost 1.84 works** - No need for Boost 1.90 patches

---

## Cleanup Plan (Execute Now)

### KEEP These Items
```
pandaforge/
├── BambuStudio-2.5.0.66/              # Working source + binary
│   ├── src/slic3r/GUI/Klipper/         # Klipper components
│   ├── build/                          # Current build
│   ├── install_dir/BambuStudio.app     # ✅ Working binary
│   └── deps/                           # Dependency source
├── BambuStudio_dep_2.5.0.66/           # ✅ Built dependencies
│   └── usr/local/
├── BUILD_GUIDE.md                      # ✅ Build instructions
└── PANDAFORGE_MASTER_PLAN.md           # ✅ This document
```

### DELETE These Items
```
pandaforge/
├── pandaforge/                         # Deadlocked fork attempt
├── wx-install/                         # Duplicate wxWidgets
├── wxWidgets/                          # Source (use deps instead)
├── CGAL-5.3.2/                         # Old version
├── CGAL-5.4.5/                         # Not needed with deps
├── CGAL-5.6.1/                         # Not needed
├── CGAL-*.tar.xz                       # Source archives
├── BambuStudio-official/               # Duplicate
├── BambuStudio_dep/                    # Old deps
├── build/                              # Old build artifacts
└── .PROJECT_DEVELOPMENT_CYCLE.md.swp   # Vim swap file
```

---

## Next Steps (Post-Cleanup)

### Immediate (Today)
1. ✅ Nuke everything except working baseline
2. Verify BambuStudio.app still runs
3. Decide: Integrate Klipper UI now or test baseline first?

### Short-term (This Week)
1. Integrate Klipper components into MainFrame
2. Test UI functionality
3. Add Moonraker connection dialog

### Medium-term (This Month)
1. Complete Moonraker integration
2. Polish profile converter
3. Add Klipper G-code templates

### Long-term
1. CI/CD pipeline for automated builds
2. Create GitHub releases
3. Documentation website

---

## Appendix A: Klipper Components Reference

### BedPlateSelector API
```cpp
BedPlateSelector(wxWindow* parent);
BedPlateType GetSelectedBedPlate();  // Returns enum
void SetBedPlate(BedPlateType type);
int GetBedTemp(bool first_layer);    // Get recommended temp
wxString GetGCodeVariable();          // For template substitution
```

### NozzleSelector API
```cpp
NozzleSelector(wxWindow* parent);
float GetNozzleDiameter();
void SetNozzleDiameter(float d);
void ApplyScalingToConfig(DynamicPrintConfig& config);
const NozzlePreset* GetCurrentPreset();
```

### FanControlPanel API
```cpp
FanControlPanel(wxWindow* parent);
void SetPrinterProfile(const PrinterProfile& profile);
void SetPrinterURL(const wxString& url);
bool SendGCode(const wxString& gcode);
void StartPolling(int interval_ms = 2000);
void StopPolling();
```

---

## Appendix B: Known Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Build deadlock | `-j8` too parallel | Use `-j4` |
| wxWidgets not found | Space in path | Use symlink `~/bambu_deps` |
| wx-config errors | Wrong prefix path | Fix path in `wx-config` script |
| ICU not found | Keg-only install | Add `-L/opt/homebrew/opt/icu4c@78/lib` |
| CMake version warnings | Old policies | Add `-DCMAKE_POLICY_VERSION_MINIMUM=3.5` |
| wxArrayString init fails | wx 3.1 limitation | Initialize in constructor |

---

## Appendix C: Git Strategy

### Recommended Branch Structure
```
main                    # Stable releases
├── develop             # Integration branch
├── feature/klipper-ui  # Klipper UI components
├── feature/moonraker   # Moonraker integration
└── hotfix/build-fixes  # Build system fixes
```

### Current State
- Fork exists at: `https://github.com/lathrodectus/pandaforge`
- Local repo `pandaforge/` will be deleted
- Need to re-clone or re-initialize after cleanup

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-03-05 | Kimi | Initial master plan consolidation |

---

**END OF DOCUMENT**
