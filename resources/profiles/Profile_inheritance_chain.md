# Profile Inheritance Chain Analysis

> **Version:** 1.1  
> **Last Updated:** March 10, 2026  
> **Applies to:** pandaforge vs OrcaSlicer Profile Comparison
>
> **Changes in v1.1:**
> - Added complete BBL OrcaSlicer inheritance chain
> - Added full Flashforge OrcaSlicer inheritance chain
> - Added detailed side-by-side comparison tables
> - Added machine profile inheritance comparison

---

## Table of Contents

1. [Overview](#overview)
2. [BBL (Bambu Lab) Inheritance Chain](#bbl-bambu-lab-inheritance-chain)
   - [Pandaforge BBL Structure](#pandaforge-bbl-structure)
   - [OrcaSlicer BBL Structure](#orcaslicer-bbl-structure)
   - [BBL Side-by-Side Comparison](#bbl-side-by-side-comparison)
3. [Flashforge Inheritance Chain](#flashforge-inheritance-chain)
   - [Pandaforge Flashforge Structure](#pandaforge-flashforge-structure)
   - [OrcaSlicer Flashforge Structure](#orcaslicer-flashforge-structure)
   - [Flashforge Side-by-Side Comparison](#flashforge-side-by-side-comparison)
4. [Key Differences Summary](#key-differences-summary)
5. [Value Format Comparison](#value-format-comparison)
6. [Porting Guide](#porting-guide)

---

## Overview

This document provides comprehensive inheritance chain maps for **BBL (Bambu Lab)** and **Flashforge** profiles in both **pandaforge** and **OrcaSlicer**. Understanding these inheritance patterns is crucial for:

- Porting profiles between slicers
- Maintaining consistent settings
- Debugging profile loading issues
- Creating new vendor profiles

---

## BBL (Bambu Lab) Inheritance Chain

### Pandaforge BBL Structure

```
fdm_process_common (ROOT)
│
├── fdm_process_single_common (instantiation: "false")
│   │
│   ├── fdm_process_single_0.06_nozzle_0.2
│   │   └── 0.06mm Fine @BBL A1 0.2 nozzle (instantiation: "true")
│   │   └── 0.06mm Fine @BBL A1M 0.2 nozzle
│   │   └── 0.06mm Fine @BBL P1P 0.2 nozzle
│   │   └── 0.06mm High Quality @BBL A1 0.2 nozzle
│   │   └── 0.06mm High Quality @BBL A1M 0.2 nozzle
│   │   └── 0.06mm High Quality @BBL P1P 0.2 nozzle
│   │   └── 0.06mm High Quality @BBL X1C 0.2 nozzle
│   │   └── 0.06mm Standard @BBL X1C 0.2 nozzle
│   │
│   ├── fdm_process_single_0.08
│   │   └── 0.08mm Extra Fine @BBL A1
│   │   └── 0.08mm Extra Fine @BBL A1M
│   │   └── 0.08mm Extra Fine @BBL H2S
│   │   └── 0.08mm Extra Fine @BBL P1P
│   │   └── 0.08mm Extra Fine @BBL P2S
│   │   └── 0.08mm Extra Fine @BBL X1C
│   │   └── 0.08mm High Quality @BBL A1
│   │   └── 0.08mm High Quality @BBL A1M
│   │   └── 0.08mm High Quality @BBL H2S
│   │   └── 0.08mm High Quality @BBL P1P
│   │   └── 0.08mm High Quality @BBL P2S
│   │   └── 0.08mm High Quality @BBL X1C
│   │
│   ├── fdm_process_single_0.08_nozzle_0.2
│   │   └── 0.08mm High Quality @BBL A1 0.2 nozzle
│   │   └── 0.08mm High Quality @BBL A1M 0.2 nozzle
│   │   └── 0.08mm High Quality @BBL H2S 0.2 nozzle
│   │   └── 0.08mm High Quality @BBL P1P 0.2 nozzle
│   │   └── 0.08mm High Quality @BBL P2S 0.2 nozzle
│   │   └── 0.08mm High Quality @BBL X1C 0.2 nozzle
│   │   └── 0.08mm Optimal @BBL A1 0.2 nozzle
│   │   └── 0.08mm Optimal @BBL A1M 0.2 nozzle
│   │   └── 0.08mm Optimal @BBL P1P 0.2 nozzle
│   │   └── 0.08mm Standard @BBL X1C 0.2 nozzle
│   │
│   ├── fdm_process_single_0.10_nozzle_0.2
│   │   └── 0.10mm High Quality @BBL A1 0.2 nozzle
│   │   └── 0.10mm High Quality @BBL A1M 0.2 nozzle
│   │   └── 0.10mm High Quality @BBL P1P 0.2 nozzle
│   │   └── 0.10mm High Quality @BBL X1C 0.2 nozzle
│   │   └── 0.10mm Standard @BBL A1 0.2 nozzle
│   │   └── 0.10mm Standard @BBL A1M 0.2 nozzle
│   │   └── 0.10mm Standard @BBL H2S 0.2 nozzle
│   │   └── 0.10mm Standard @BBL H2DP 0.2 nozzle
│   │   └── 0.10mm Standard @BBL P1P 0.2 nozzle
│   │   └── 0.10mm Standard @BBL P2S 0.2 nozzle
│   │   └── 0.10mm Standard @BBL X1C 0.2 nozzle
│   │
│   ├── fdm_process_single_0.12
│   │   └── 0.12mm Draft @BBL A1M 0.2 nozzle
│   │   └── 0.12mm Fine @BBL A1
│   │   └── 0.12mm Fine @BBL A1M
│   │   └── 0.12mm Fine @BBL A1M 0.2 nozzle
│   │   └── 0.12mm Fine @BBL H2DP
│   │   └── 0.12mm Fine @BBL P1P
│   │   └── 0.12mm Fine @BBL P2S
│   │   └── 0.12mm Fine @BBL X1C
│   │   └── 0.12mm High Quality @BBL A1
│   │   └── 0.12mm High Quality @BBL A1M
│   │   └── 0.12mm High Quality @BBL H2S
│   │   └── 0.12mm High Quality @BBL P1P
│   │   └── 0.12mm High Quality @BBL P2S
│   │   └── 0.12mm High Quality @BBL X1C
│   │   └── 0.12mm Standard @BBL X1C 0.2 nozzle
│   │
│   ├── fdm_process_single_0.12_nozzle_0.2
│   │   └── 0.12mm Balanced Quality @BBL H2S 0.2 nozzle
│   │   └── 0.12mm Balanced Quality @BBL P2S 0.2 nozzle
│   │   └── 0.12mm Draft @BBL A1 0.2 nozzle
│   │   └── 0.12mm Draft @BBL P1P 0.2 nozzle
│   │
│   ├── fdm_process_single_0.14_nozzle_0.2
│   │   └── 0.14mm Extra Draft @BBL A1 0.2 nozzle
│   │   └── 0.14mm Extra Draft @BBL A1M 0.2 nozzle
│   │   └── 0.14mm Extra Draft @BBL P1P 0.2 nozzle
│   │   └── 0.14mm Standard @BBL X1C 0.2 nozzle
│   │
│   ├── fdm_process_single_0.16
│   │   └── 0.16mm High Quality @BBL A1M
│   │   └── 0.16mm High Quality @BBL H2S
│   │   └── 0.16mm High Quality @BBL P1P
│   │   └── 0.16mm High Quality @BBL P2S
│   │   └── 0.16mm High Quality @BBL X1C
│   │   └── 0.16mm Optimal @BBL A1
│   │   └── 0.16mm Optimal @BBL A1M
│   │   └── 0.16mm Optimal @BBL P1P
│   │   └── 0.16mm Optimal @BBL X1C
│   │   └── 0.16mm Standard @BBL H2S
│   │   └── 0.16mm Standard @BBL P2S
│   │
│   ├── fdm_process_single_0.18_nozzle_0.6
│   │   └── 0.18mm Fine @BBL A1 0.6 nozzle
│   │   └── 0.18mm Fine @BBL A1M 0.6 nozzle
│   │   └── 0.18mm Fine @BBL P1P 0.6 nozzle
│   │   └── 0.18mm Standard @BBL X1C 0.6 nozzle
│   │
│   ├── fdm_process_single_0.20
│   │   └── 0.20mm High Quality @BBL H2S
│   │   └── 0.20mm High Quality @BBL P2S
│   │   └── 0.20mm Standard @BBL A1
│   │   └── 0.20mm Standard @BBL A1M
│   │   └── 0.20mm Standard @BBL H2S
│   │   └── 0.20mm Standard @BBL P1P
│   │   └── 0.20mm Standard @BBL P2S
│   │   └── 0.20mm Standard @BBL X1C
│   │   └── 0.20mm Strength @BBL A1
│   │   └── 0.20mm Strength @BBL A1M
│   │   └── 0.20mm Strength @BBL P1P
│   │   └── 0.20mm Strength @BBL X1C
│   │
│   ├── fdm_process_single_0.24
│   │   └── 0.24mm Draft @BBL A1
│   │   └── 0.24mm Draft @BBL A1M
│   │   └── 0.24mm Draft @BBL P1P
│   │   └── 0.24mm Draft @BBL X1C
│   │   └── 0.24mm Standard @BBL H2S
│   │   └── 0.24mm Standard @BBL P2S
│   │   └── 0.24mm Standard @BBL X1C 0.6 nozzle
│   │
│   ├── fdm_process_single_0.24_nozzle_0.6
│   │   └── 0.24mm Balanced Quality @BBL H2S 0.6 nozzle
│   │   └── 0.24mm Balanced Quality @BBL P2S 0.6 nozzle
│   │   └── 0.24mm Fine @BBL A1 0.8 nozzle
│   │   └── 0.24mm Fine @BBL A1M 0.8 nozzle
│   │   └── 0.24mm Fine @BBL P1P 0.8 nozzle
│   │   └── 0.24mm Optimal @BBL A1 0.6 nozzle
│   │   └── 0.24mm Optimal @BBL A1M 0.6 nozzle
│   │   └── 0.24mm Optimal @BBL P1P 0.6 nozzle
│   │   └── 0.24mm Standard @BBL H2S 0.6 nozzle
│   │   └── 0.24mm Standard @BBL X1C 0.6 nozzle
│   │
│   ├── fdm_process_single_0.24_nozzle_0.8
│   │   └── 0.24mm Balanced Quality @BBL H2S 0.8 nozzle
│   │   └── 0.24mm Balanced Quality @BBL P2S 0.8 nozzle
│   │   └── 0.24mm Standard @BBL X1C 0.8 nozzle
│   │
│   ├── fdm_process_single_0.28
│   │   └── 0.28mm Extra Draft @BBL A1
│   │   └── 0.28mm Extra Draft @BBL A1M
│   │   └── 0.28mm Extra Draft @BBL P1P
│   │   └── 0.28mm Extra Draft @BBL X1C
│   │
│   ├── fdm_process_single_0.30_nozzle_0.6
│   │   └── 0.30mm Standard @BBL A1 0.6 nozzle
│   │   └── 0.30mm Standard @BBL A1M 0.6 nozzle
│   │   └── 0.30mm Standard @BBL H2S 0.6 nozzle
│   │   └── 0.30mm Standard @BBL P1P 0.6 nozzle
│   │   └── 0.30mm Standard @BBL P2S 0.6 nozzle
│   │   └── 0.30mm Standard @BBL X1C 0.6 nozzle
│   │   └── 0.30mm Strength @BBL A1 0.6 nozzle
│   │   └── 0.30mm Strength @BBL A1M 0.6 nozzle
│   │   └── 0.30mm Strength @BBL X1C 0.6 nozzle
│   │
│   ├── fdm_process_single_0.32_nozzle_0.8
│   │   └── 0.32mm Balanced Quality @BBL H2S 0.8 nozzle
│   │   └── 0.32mm Balanced Quality @BBL P2S 0.8 nozzle
│   │   └── 0.32mm Optimal @BBL A1 0.8 nozzle
│   │   └── 0.32mm Optimal @BBL A1M 0.8 nozzle
│   │   └── 0.32mm Optimal @BBL P1P 0.8 nozzle
│   │   └── 0.32mm Standard @BBL X1C 0.8 nozzle
│   │
│   ├── fdm_process_single_0.36_nozzle_0.6
│   │   └── 0.36mm Draft @BBL A1 0.6 nozzle
│   │   └── 0.36mm Draft @BBL A1M 0.6 nozzle
│   │   └── 0.36mm Draft @BBL P1P 0.6 nozzle
│   │   └── 0.36mm Standard @BBL X1C 0.6 nozzle
│   │
│   ├── fdm_process_single_0.40_nozzle_0.8
│   │   └── 0.40mm Standard @BBL A1 0.8 nozzle
│   │   └── 0.40mm Standard @BBL A1M 0.8 nozzle
│   │   └── 0.40mm Standard @BBL H2S 0.8 nozzle
│   │   └── 0.40mm Standard @BBL P1P 0.8 nozzle
│   │   └── 0.40mm Standard @BBL P2S 0.8 nozzle
│   │   └── 0.40mm Standard @BBL X1 0.8 nozzle
│   │   └── 0.40mm Standard @BBL X1C 0.8 nozzle
│   │
│   ├── fdm_process_single_0.42_nozzle_0.6
│   │   └── 0.42mm Extra Draft @BBL A1 0.6 nozzle
│   │   └── 0.42mm Extra Draft @BBL A1M 0.6 nozzle
│   │   └── 0.42mm Standard @BBL X1C 0.6 nozzle
│   │
│   ├── fdm_process_single_0.48_nozzle_0.8
│   │   └── 0.48mm Draft @BBL A1 0.8 nozzle
│   │   └── 0.48mm Draft @BBL A1M 0.8 nozzle
│   │   └── 0.48mm Draft @BBL P1P 0.8 nozzle
│   │   └── 0.48mm Standard @BBL X1C 0.8 nozzle
│   │
│   └── fdm_process_single_0.56_nozzle_0.8
│       └── 0.56mm Extra Draft @BBL A1 0.8 nozzle
│       └── 0.56mm Extra Draft @BBL A1M 0.8 nozzle
│       └── 0.56mm Extra Draft @BBL P1P 0.8 nozzle
│       └── 0.56mm Standard @BBL X1C 0.8 nozzle
│
└── fdm_process_dual_common (instantiation: "false")
    ├── fdm_process_dual_0.06_nozzle_0.2
    ├── fdm_process_dual_0.08_nozzle_0.2
    ├── fdm_process_dual_0.08_nozzle_0.4
    │   └── 0.08mm Extra Fine @BBL H2D
    │   └── 0.08mm Extra Fine @BBL H2DP
    │   └── 0.12mm Fine @BBL H2D
    │   └── 0.12mm Fine @BBL H2DP
    │   └── 0.16mm Balanced Quality @BBL H2D
    │   └── 0.16mm Balanced Quality @BBL H2DP
    │   └── 0.16mm Standard @BBL H2D
    │   └── 0.16mm Standard @BBL H2DP
    │
    ├── fdm_process_dual_0.10_nozzle_0.2
    │   └── 0.10mm Standard @BBL H2D 0.2 nozzle
    │   └── 0.10mm Standard @BBL H2DP 0.2 nozzle
    │
    ├── fdm_process_dual_0.12_nozzle_0.2
    │   └── 0.12mm Balanced Quality @BBL H2D 0.2 nozzle
    │   └── 0.12mm Balanced Quality @BBL H2DP 0.2 nozzle
    │
    ├── fdm_process_dual_0.12_nozzle_0.4
    ├── fdm_process_dual_0.14_nozzle_0.2
    ├── fdm_process_dual_0.16_nozzle_0.4
    │   └── 0.16mm Balanced Quality @BBL H2D
    │   └── 0.16mm Balanced Quality @BBL H2DP
    │
    ├── fdm_process_dual_0.18_nozzle_0.6
    │   └── 0.18mm Balanced Quality @BBL H2D 0.6 nozzle
    │   └── 0.18mm Balanced Quality @BBL H2DP 0.6 nozzle
    │
    ├── fdm_process_dual_0.20_nozzle_0.4
    │   └── 0.20mm Balanced Strength @BBL H2D
    │   └── 0.20mm Balanced Strength @BBL H2DP
    │   └── 0.20mm Standard @BBL H2D
    │   └── 0.20mm Standard @BBL H2DP
    │
    ├── fdm_process_dual_0.24_nozzle_0.4
    │   └── 0.24mm Standard @BBL H2D
    │   └── 0.24mm Standard @BBL H2DP
    │
    ├── fdm_process_dual_0.24_nozzle_0.6
    │   └── 0.24mm Balanced Quality @BBL H2D 0.6 nozzle
    │   └── 0.24mm Balanced Quality @BBL H2DP 0.6 nozzle
    │   └── 0.24mm Balanced Strength @BBL H2D 0.6 nozzle
    │
    ├── fdm_process_dual_0.24_nozzle_0.8
    │   └── 0.24mm Balanced Quality @BBL H2D 0.8 nozzle
    │   └── 0.24mm Balanced Quality @BBL H2DP 0.8 nozzle
    │
    ├── fdm_process_dual_0.28_nozzle_0.4
    ├── fdm_process_dual_0.30_nozzle_0.6
    │   └── 0.30mm Standard @BBL H2D 0.6 nozzle
    │   └── 0.30mm Standard @BBL H2DP 0.6 nozzle
    │
    ├── fdm_process_dual_0.32_nozzle_0.8
    │   └── 0.32mm Balanced Quality @BBL H2D 0.8 nozzle
    │   └── 0.32mm Balanced Quality @BBL H2DP 0.8 nozzle
    │   └── 0.32mm Balanced Strength @BBL H2D 0.8 nozzle
    │   └── 0.32mm Balanced Strength @BBL H2DP 0.8 nozzle
    │
    ├── fdm_process_dual_0.36_nozzle_0.6
    ├── fdm_process_dual_0.40_nozzle_0.8
    │   └── 0.40mm Standard @BBL H2D 0.8 nozzle
    │   └── 0.40mm Standard @BBL H2DP 0.8 nozzle
    │
    ├── fdm_process_dual_0.42_nozzle_0.6
    ├── fdm_process_dual_0.48_nozzle_0.8
    └── fdm_process_dual_0.56_nozzle_0.8
```

### OrcaSlicer BBL Structure

OrcaSlicer BBL has the **same inheritance structure** as pandaforge but with key differences:

```
fdm_process_common (ROOT)
│
├── fdm_process_single_common
│   │
│   ├── fdm_process_single_0.06_nozzle_0.2
│   ├── fdm_process_single_0.08
│   ├── fdm_process_single_0.08_nozzle_0.2
│   ├── fdm_process_single_0.10_nozzle_0.2
│   ├── fdm_process_single_0.12
│   ├── fdm_process_single_0.12_nozzle_0.2
│   ├── fdm_process_single_0.14_nozzle_0.2
│   ├── fdm_process_single_0.16
│   ├── fdm_process_single_0.18_nozzle_0.6
│   ├── fdm_process_single_0.20
│   ├── fdm_process_single_0.24
│   ├── fdm_process_single_0.24_nozzle_0.6
│   ├── fdm_process_single_0.24_nozzle_0.8
│   ├── fdm_process_single_0.28
│   ├── fdm_process_single_0.30_nozzle_0.6
│   ├── fdm_process_single_0.32_nozzle_0.8
│   ├── fdm_process_single_0.36_nozzle_0.6
│   ├── fdm_process_single_0.40_nozzle_0.8
│   ├── fdm_process_single_0.42_nozzle_0.6
│   ├── fdm_process_single_0.48_nozzle_0.8
│   └── fdm_process_single_0.56_nozzle_0.8
│
└── fdm_process_dual_common
    ├── fdm_process_dual_0.06_nozzle_0.2
    ├── fdm_process_dual_0.08_nozzle_0.2
    ├── fdm_process_dual_0.08_nozzle_0.4
    ├── fdm_process_dual_0.10_nozzle_0.2
    ├── fdm_process_dual_0.12_nozzle_0.2
    ├── fdm_process_dual_0.12_nozzle_0.4
    ├── fdm_process_dual_0.14_nozzle_0.2
    ├── fdm_process_dual_0.16_nozzle_0.4
    ├── fdm_process_dual_0.18_nozzle_0.6
    ├── fdm_process_dual_0.20_nozzle_0.4
    ├── fdm_process_dual_0.24_nozzle_0.4
    ├── fdm_process_dual_0.24_nozzle_0.6
    ├── fdm_process_dual_0.24_nozzle_0.8
    ├── fdm_process_dual_0.28_nozzle_0.4
    ├── fdm_process_dual_0.30_nozzle_0.6
    ├── fdm_process_dual_0.32_nozzle_0.8
    ├── fdm_process_dual_0.36_nozzle_0.6
    ├── fdm_process_dual_0.40_nozzle_0.8
    ├── fdm_process_dual_0.42_nozzle_0.6
    ├── fdm_process_dual_0.48_nozzle_0.8
    └── fdm_process_dual_0.56_nozzle_0.8
```

### BBL Side-by-Side Comparison

| Aspect | Pandaforge BBL | OrcaSlicer BBL | Notes |
|--------|---------------|----------------|-------|
| **Version** | 02.05.00.05 | 02.01.00.00 | Pandaforge newer |
| **Machines** | 12 models | 11 models | Pandaforge adds H2C, H2S, P2S |
| **Inheritance Depth** | 4 levels | 4 levels | Same structure |
| **Base Files** | 45 | 45 | Same count |
| **Single Common** | ✅ | ✅ | Same |
| **Dual Common** | ✅ | ✅ | Same |
| **Intermediate Layers** | 23 single, 22 dual | 23 single, 22 dual | Same |

**Key Differences:**

| Setting | Pandaforge | OrcaSlicer | Impact |
|---------|------------|------------|--------|
| `inner_wall_speed` | `["300", "400"]` | `["300", "300"]` | Pandaforge enables High Flow |
| `outer_wall_speed` | `["200", "350"]` | `["200", "200"]` | Pandaforge enables High Flow |
| `sparse_infill_speed` | `["270", "370"]` | `["270", "270"]` | Pandaforge enables High Flow |
| `default_acceleration` | `["10000", "10000"]` | `["10000", "10000"]` | Same |

**Note:** Array values are `[Standard Nozzle, High Flow Nozzle]`. Pandaforge enables High Flow speeds in second position.

---

## Flashforge Inheritance Chain

### Pandaforge Flashforge Structure

```
fdm_process_common (ROOT)
│
└── fdm_process_flashforge_common (instantiation: "false")
    │
    ├── fdm_process_flashforge_0.20 (instantiation: "false")
    │   │
    │   ├── 0.08mm Extra Fine @Flashforge AD5M Pro (instantiation: "true")
    │   ├── 0.08mm High Quality @Flashforge AD5M Pro
    │   ├── 0.12mm Fine @Flashforge AD5M Pro
    │   ├── 0.12mm High Quality @Flashforge AD5M Pro
    │   ├── 0.16mm Optimal @Flashforge AD5M Pro
    │   ├── 0.16mm High Quality @Flashforge AD5M Pro
    │   ├── 0.20mm Standard @Flashforge AD5M Pro
    │   ├── 0.20mm Strength @Flashforge AD5M Pro
    │   ├── 0.24mm Draft @Flashforge AD5M Pro
    │   └── 0.28mm Extra Draft @Flashforge AD5M Pro
    │
    ├── fdm_process_flashforge_0.25_nozzle (instantiation: "false")
    │   │
    │   ├── 0.10mm High Quality @Flashforge AD5M Pro 0.25 nozzle
    │   ├── 0.12mm Fine @Flashforge AD5M Pro 0.25 nozzle
    │   ├── 0.15mm Standard @Flashforge AD5M Pro 0.25 nozzle
    │   ├── 0.18mm Draft @Flashforge AD5M Pro 0.25 nozzle
    │   └── 0.20mm Extra Draft @Flashforge AD5M Pro 0.25 nozzle
    │
    ├── fdm_process_flashforge_0.30 (instantiation: "false")
    │   │
    │   ├── 0.30mm Standard @Flashforge AD5M Pro 0.6 nozzle
    │   └── 0.30mm Strength @Flashforge AD5M Pro 0.6 nozzle
    │
    └── fdm_process_flashforge_0.40 (instantiation: "false")
        │
        ├── 0.40mm Standard @Flashforge AD5M Pro 0.8 nozzle
        └── (other 0.8mm profiles)
```

### OrcaSlicer Flashforge Structure

```
fdm_process_common (ROOT)
│
└── fdm_process_flashforge_common (instantiation: "false")
    │
    ├── fdm_process_flashforge_0.20 (instantiation: "false")
    │   │
    │   ├── 0.12mm Fine @Flashforge AD5M 0.4 Nozzle
    │   ├── 0.12mm Fine @Flashforge AD5M Pro 0.4 Nozzle
    │   ├── 0.20mm Standard @Flashforge AD5M 0.4 Nozzle
    │   ├── 0.20mm Standard @Flashforge AD5M Pro 0.4 Nozzle
    │   ├── 0.24mm Draft @Flashforge AD5M 0.4 Nozzle
    │   ├── 0.24mm Draft @Flashforge AD5M Pro 0.4 Nozzle
    │   └── (other 0.4mm profiles for AD5M, AD5M Pro)
    │
    ├── fdm_process_flashforge_0.30 (instantiation: "false")
    │   │
    │   ├── 0.30mm Standard @Flashforge AD5M 0.6 Nozzle
    │   ├── 0.30mm Standard @Flashforge AD5M Pro 0.6 Nozzle
    │   └── (0.6mm profiles for AD5M, AD5M Pro, G3U, G4, G4P, AD5X)
    │
    └── fdm_process_flashforge_0.40 (instantiation: "false")
        │
        ├── 0.40mm Standard @Flashforge AD5M 0.8 Nozzle
        ├── 0.40mm Standard @Flashforge AD5M Pro 0.8 Nozzle
        └── (0.8mm profiles for AD5M, AD5M Pro, AD5X, G3U, G4, G4P)

Note: 0.25mm nozzle profiles in OrcaSlicer directly inherit from fdm_process_flashforge_common
or from other profiles (e.g., 0.12mm Standard @Flashforge AD5M Pro 0.25 Nozzle inherits 
from 0.20mm Standard @Flashforge AD5M Pro 0.4 Nozzle)
```

### Flashforge Side-by-Side Comparison

| Aspect | Pandaforge Flashforge | OrcaSlicer Flashforge | Notes |
|--------|----------------------|----------------------|-------|
| **Machines** | 1 (AD5M Pro) | 9 (AD3, AD4, AD5M, AD5M Pro, AD5X, G2S, G3U, G4, G4P) | OrcaSlicer much broader |
| **Intermediate Layers** | 4 | 3 | Pandaforge adds 0.25_nozzle |
| **Inheritance Depth** | 3-4 levels | 3 levels | Similar |
| **0.25 Nozzle Layer** | ✅ `fdm_process_flashforge_0.25_nozzle` | ❌ Direct inheritance | Key difference |
| **Value Format** | Strings | Strings | Same format |

**Intermediate Layer Comparison:**

| Layer | Pandaforge | OrcaSlicer |
|-------|------------|------------|
| `fdm_process_flashforge_0.20` | ✅ | ✅ |
| `fdm_process_flashforge_0.25_nozzle` | ✅ | ❌ Missing |
| `fdm_process_flashforge_0.30` | ✅ | ✅ |
| `fdm_process_flashforge_0.40` | ✅ | ✅ |

**Profile Count Comparison:**

| Nozzle Size | Pandaforge | OrcaSlicer |
|-------------|------------|------------|
| 0.25mm | 5 profiles | Multiple (AD5M, AD5M Pro, G4, G4P, AD5X) |
| 0.4mm | 10 profiles | Many across all 9 machines |
| 0.6mm | 2 profiles | Many across all machines |
| 0.8mm | 1 profile | Many across all machines |

---

## Key Differences Summary

### Inheritance Depth Comparison

| Vendor | Pandaforge Max Depth | OrcaSlicer Max Depth |
|--------|---------------------|---------------------|
| BBL | 4 levels | 4 levels |
| Flashforge | 4 levels | 3-4 levels |

### Value Format Summary

| Vendor | Pandaforge | OrcaSlicer |
|--------|------------|------------|
| **BBL Process** | Arrays `["300", "400"]` | Arrays `["300", "300"]` |
| **Flashforge Process** | Strings `"300"` | Strings `"300"` |
| **Machine (both)** | Arrays `["0.4"]` | Arrays `["0.4"]` |
| **Filament (both)** | Arrays `["210"]` | Arrays `["210"]` |

### Intermediate Layer Patterns

| Vendor | Pattern | Example |
|--------|---------|---------|
| BBL | `fdm_process_{type}_{layer}_nozzle_{nozzle}` | `fdm_process_single_0.20` |
| Flashforge PF | `fdm_process_flashforge_{layer}` or `{nozzle}_nozzle` | `fdm_process_flashforge_0.25_nozzle` |
| Flashforge OS | `fdm_process_flashforge_{layer}` only | `fdm_process_flashforge_0.20` |

---

## Value Format Comparison

### Format by Profile Type

| Profile Type | BBL Format | Flashforge Format |
|--------------|------------|-------------------|
| Process | Arrays | Strings |
| Machine | Arrays | Arrays |
| Filament | Arrays | Arrays |

### Why Different Formats?

**BBL uses Arrays** because Bambu Lab printers support dual extruders with different nozzle types (Standard and High Flow). The array format allows specifying different speeds for each extruder:

```json
// BBL: Different speeds for Standard [0] and High Flow [1] nozzles
"inner_wall_speed": ["300", "400"],
"outer_wall_speed": ["200", "350"]
```

**Flashforge uses Strings** because Flashforge printers (AD5M, AD5M Pro) are single extruder machines:

```json
// Flashforge: Single extruder, single value
"inner_wall_speed": "300",
"outer_wall_speed": "180"
```

---

## Porting Guide

### From OrcaSlicer to Pandaforge

#### BBL Profiles

1. **Keep array format** - BBL uses arrays in both slicers
2. **Update High Flow values** - Change second array value to enable High Flow:
   ```json
   // OrcaSlicer
   "inner_wall_speed": ["300", "300"]
   
   // Pandaforge (enable High Flow)
   "inner_wall_speed": ["300", "400"]
   ```
3. **Add new machine models** if needed (H2C, H2S, P2S)

#### Flashforge Profiles

1. **Add intermediate layer** for 0.25mm nozzle if missing:
   ```json
   // Create fdm_process_flashforge_0.25_nozzle.json
   {
       "type": "process",
       "name": "fdm_process_flashforge_0.25_nozzle",
       "inherits": "fdm_process_flashforge_common",
       "instantiation": "false",
       "line_width": "0.28",
       "inner_wall_speed": "100",
       ...
   }
   ```
2. **Use string values** (not arrays) for process profiles
3. **Register in Flashforge.json** in correct order
4. **Update inheritance** in 0.25mm profiles to point to intermediate layer

### From Pandaforge to OrcaSlicer

#### BBL Profiles

1. **Keep array format**
2. **Disable High Flow** - Set both array values equal:
   ```json
   // Pandaforge
   "inner_wall_speed": ["300", "400"]
   
   // OrcaSlicer (disable High Flow)
   "inner_wall_speed": ["300", "300"]
   ```

#### Flashforge Profiles

1. **Use string values** (same in both)
2. **Remove 0.25_nozzle intermediate layer** if not needed
3. **Update inheritance** to point directly to `fdm_process_flashforge_common`

---

## Loading Order Requirements

### Critical: Register Intermediate Layers

Intermediate layers MUST be listed in `<Brand>.json` BEFORE profiles that inherit from them:

```json
{
    "process_list": [
        // 1. Root base
        {"name": "fdm_process_common", ...},
        
        // 2. Vendor base
        {"name": "fdm_process_flashforge_common", ...},
        
        // 3. Intermediate layers (in order of dependency)
        {"name": "fdm_process_flashforge_0.20", ...},
        {"name": "fdm_process_flashforge_0.25_nozzle", ...},
        {"name": "fdm_process_flashforge_0.30", ...},
        {"name": "fdm_process_flashforge_0.40", ...},
        
        // 4. Instantiation profiles
        {"name": "0.20mm Standard @Flashforge AD5M Pro", ...}
    ]
}
```

**Failure to register intermediate layers will cause "Failed loading configuration file" errors.**

---

*Document maintained for pandaforge profile development.*
