# Pandaforge Documentation Index

Agent routing table. Find the right doc for any task.

| I need to... | Read this |
|---|---|
| Build the project | [docs/building.md](building.md) |
| Understand codebase structure | [docs/architecture.md](architecture.md) |
| Write C++ code / know style rules | [docs/coding-conventions.md](coding-conventions.md) |
| Work on Klipper UI components | [docs/klipper-components.md](klipper-components.md) |
| Work on Moonraker / fan control | [docs/moonraker-api.md](moonraker-api.md) |
| Work on profiles / profile converter | [docs/profile-system.md](profile-system.md) |
| Use the profile converter tool | [tools/profile_converter/README.md](../tools/profile_converter/README.md) |
| See project roadmap / status | [docs/roadmap.md](roadmap.md) |
| See recent changes | [docs/changelog.md](changelog.md) |
| Run or write tests | [docs/testing.md](testing.md) |
| Understand profile inheritance rules | [BambuStudio-2.5.0.66/resources/profiles/Profile_rules.md](../BambuStudio-2.5.0.66/resources/profiles/Profile_rules.md) |
| Understand profile inheritance chains | [BambuStudio-2.5.0.66/resources/profiles/Profile_inheritance_chain.md](../BambuStudio-2.5.0.66/resources/profiles/Profile_inheritance_chain.md) |

## File Map

```
CLAUDE.md                    <- Entry point (read first)
docs/
  INDEX.md                   <- This file
  architecture.md            <- Directory structure, tech stack, key source files
  building.md                <- Prerequisites -> build -> run -> troubleshooting
  coding-conventions.md      <- Code style, wxWidgets 3.1.5, AppConfig, i18n
  klipper-components.md      <- BedPlateSelector, NozzleSelector, FanControlPanel
  moonraker-api.md           <- HTTP endpoints, libcurl, Phase 2 plans
  roadmap.md                 <- Vision, Phase 0-4 status, next steps
  changelog.md               <- Recent changes, rename history
  testing.md                 <- Catch2 setup, running tests
  profile-system.md          <- Profile overview + pointers to detailed docs
  archive/                   <- Historical docs (not for daily use)
tools/profile_converter/
  README.md                  <- Consolidated converter docs (CLI + GUI + interactive)
  FLASHFORGE_EXAMPLE.md      <- Reference profile example
```
