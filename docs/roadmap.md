# Project Roadmap

## Vision

Pandaforge is a macOS-native BambuStudio fork optimized for Klipper printers. Create BambuStudio's excellent UI with Klipper's flexibility.

### Target Users
- Klipper printer owners on macOS
- Users wanting BambuStudio's UI with Klipper's flexibility
- Users migrating from OrcaSlicer to BambuStudio

## Phase Status

### Phase 0: Foundation -- COMPLETE

**Goal:** Working BambuStudio binary

| Task | Status |
|---|---|
| Install Xcode CLI tools | Done |
| Install Homebrew deps | Done |
| Build dependencies (`BambuStudio_dep_2.5.0.66`) | Done |
| Build BambuStudio binary | Done |
| Document build process | Done |

### Phase 1: Klipper Integration -- IN PROGRESS

**Goal:** Add Klipper UI components to main interface

| Task | Status |
|---|---|
| Fix API compatibility issues (wxWidgets 3.1.5) | Done |
| Compile Klipper components (BedPlateSelector, NozzleSelector, FanControlPanel) | Done |
| Pressure advance fix (GCodeWriter multi-extruder support) | Done |
| UI panel size fix for 3rd-party printers | Done |
| Integrate components into MainFrame | Pending |
| Test UI functionality | Pending |
| Add Moonraker connection dialog | Pending |

**Decision needed:** Toolbar vs Side panel placement for Klipper UI components.

### Phase 2: Moonraker Integration -- NOT STARTED

**Goal:** Real-time printer communication

- Temperature monitoring (poll `/api/printer`)
- WebSocket connection for print status
- Camera feed (MJPEG stream)

### Phase 3: Profile Converter -- NOT STARTED

**Goal:** OrcaSlicer -> BambuStudio profile migration with UI integration

- Basic JSON conversion exists (`tools/profile_converter/`)
- UI integration into Pandaforge not done

### Phase 4: Klipper G-code Templates -- NOT STARTED

**Goal:** Better default G-code for Klipper printers

- Bed plate variable substitution (`{bed_plate_type}`)
- Klipper-optimized start/end G-code
- Pressure advance integration
- Input shaping hints

## Lessons Learned

1. **Use `-j4` not `-j8`** -- Higher parallelism causes build deadlock on large translation units
2. **Use symlink for deps** -- Avoids space-in-path issues with CMake/wxWidgets
3. **Fix wx-config paths** -- Must point to actual dependency location
4. **Boost 1.84 works** -- No need for Boost 1.90 patches
5. **wxWidgets 3.1.5 API** -- Many 3.2+ features not available (SetBold, SetSuffix, initializer lists)

## Decision Log

| Decision | Choice | Rationale |
|---|---|---|
| Base version | BambuStudio v2.5.0.66 | Latest stable at project start |
| wxWidgets version | 3.1.5 (BambuLab fork) | Matches upstream, proven stable |
| Config storage | AppConfig (not wxConfigBase) | Matches BambuStudio patterns |
| Build parallelism | -j4 | Prevents deadlock |
| Profile converter | Python (not C++) | Faster development, no compilation |

## Git Strategy

```
main                    # Stable releases
├── develop             # Integration branch
├── feature/klipper-ui  # Klipper UI components
├── feature/moonraker   # Moonraker integration
└── hotfix/build-fixes  # Build system fixes
```

GitHub: `https://github.com/lathrodectus/pandaforge`

## Next Steps

### Immediate
1. Integrate Klipper components into MainFrame
2. Test UI functionality
3. Add Moonraker connection dialog

### Short-term
1. Complete Moonraker integration
2. Polish profile converter
3. Add Klipper G-code templates

### Long-term
1. CI/CD pipeline for automated builds
2. GitHub releases
3. Documentation website
