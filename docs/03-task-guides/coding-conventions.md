# Coding Conventions

## General Rules

- **Namespaces**: GUI code commonly lives in `Slic3r::GUI`, but the repo also contains substantial non-GUI code under `src/libslic3r/` and other namespaces
- **Includes**: Use relative paths for internal headers: `#include "../I18N.hpp"`
- **Internationalization**: Wrap user-facing strings with `_L("...")` macro
- **C++ Standard**: C++17 features are available

## wxWidgets 3.1.5 Compatibility

The project uses wxWidgets 3.1.5 (BambuLab fork). Some features from newer versions are **NOT available**:

```cpp
// ---- NOT AVAILABLE in wx 3.1 ----

m_spinCtrl->SetSuffix("%");            // No suffix support
wxFont bold = font.SetBold();          // SetBold() doesn't exist
wxArrayString choices = { "a", "b" };  // Initializer list not supported

// ---- CORRECT APPROACH ----

// wxArrayString: initialize in constructor
wxArrayString choices;
choices.Add("a");
choices.Add("b");

// wxFont: use SetWeight
wxFont font = GetFont();
font.SetWeight(wxFONTWEIGHT_BOLD);

// wxSpinCtrl: no suffix - remove or subclass
```

## Configuration Storage

**Always use `AppConfig`**, never `wxConfigBase`:

```cpp
// CORRECT
AppConfig* config = wxGetApp().app_config;
if (config) {
    config->set("klipper", "bed_plate", "textured_pei");
    std::string value = config->get("klipper", "bed_plate");
}

// WRONG - do not use
wxConfigBase* config = wxConfigBase::Get();
```

## Adding New Klipper Features

1. **Check OrcaSlicer first** — see how they handle the same feature
2. Implement in the current branch's real surface area:
   `src/slic3r/GUI/` for UI,
   `src/libslic3r/` for slicing/config logic,
   or `resources/profiles/` for data-only changes
3. Follow wxWidgets 3.1.5 API constraints (see above)
4. Use `AppConfig` for persistent settings
5. Wrap UI strings with `_L()` for internationalization
6. Test with actual Klipper printer if possible

## Modifying G-code Generation

1. Core logic: `src/libslic3r/GCode.cpp`
2. Low-level output: `src/libslic3r/GCodeWriter.cpp`
3. Settings definitions: `src/libslic3r/PrintConfig.cpp`
4. Test with multiple printer profiles
5. Verify G-code output manually

## Localization

- Config: `localazy.json`
- Source language: English (en)
- Supported: fr, de, sv, es, nl, hu, it, ja, ko
- Format: GNU gettext (.po files) in `resources/i18n/`

## Security Notes

1. **Embedded printer web UIs**: `print_host` / `print_host_webui` content may be loaded in the Device tab. Treat printer web access as trusted-network functionality.
2. **G-code Injection**: User-provided G-code is sent directly to printers. Validate inputs.
3. **Network Access**: Required for embedded printer web UIs and BambuLab cloud features.

## License

BambuStudio is licensed under **AGPL-3.0**. Based on PrusaSlicer by Prusa Research, originally from Slic3r by Alessandro Ranellucci.
