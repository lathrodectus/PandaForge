# Lessons Log

Historical note: some lessons refer to tooling that lived in side branches or older workspaces. Keep the lesson, but verify the path before assuming the tool exists in this branch.

## March 24, 2026

- A third-party vendor manifest is not complete unless it lists the non-instantiable base presets that the visible machine, filament, and process profiles inherit from. Files merely existing on disk are not enough.
- For vendor materials, inheriting from another vendor's `@base` filament is brittle. The stable pattern in this repo is local `fdm_filament_*` bases plus vendor-visible aliases that inherit from them.
- The printer setup wizard does not build thumbnails from `bed_model` or `bed_texture`, and it does not use `model_id` for the filename. It looks for a PNG named `<machine_model_list.name>_thumbnail.png` under `resources/profiles/<Vendor>/`.
- The selected-printer image in the profile guide is a separate asset path from the setup wizard. `WebGuideDialog` publishes `<machine_model_list.name>_cover.png`, so fixing `_thumbnail.png` alone still leaves the main-window selection art blank.
- The plater/sidebar printer image is a third, separate path again. `Plater.cpp` and `SelectMachine.cpp` look for `resources/images/printer_preview_<model_id>.png`, where `<model_id>` comes from the machine-model JSON, not from the vendor manifest display name.
- Matching Bambu's selected-printer card in the main window needs both the preview asset and the Bambu-style sizer path. `Sidebar::priv::layout_printer()` was still branching on `is_bbl_vendor_preset()`, which kept converted printers in a horizontal image-plus-name row until the layout logic itself was unified.
- After unifying the selected-printer card layout, the card height also has to stay in sync with the Bambu version. The old Bambu layout effectively got extra height from the visible `Sync info` button; converted printers hid that button, so the row collapsed and clipped the printer-name line until the stacked panel min height was raised explicitly.
- Filament bed-temperature rows should be gated by supported bed types, not by vendor. `TabFilament::toggle_options()` was hiding `Cool`, `Engineering`, `Textured`, and `Supertack` temperature fields for all non-Bambu printers even when the current printer model exposed those plates, so converted printers lost editable plate temperatures despite the presets carrying the values.
- Asset-path case matters. A single mismatched filename like `X-Series_gen3_hotend.stl` versus `qidi_xseries_gen3_hotend.stl` is enough to break the model asset chain.
- Vendor JSON loading is order-sensitive. In `process_list`, `filament_list`, and `machine_list`, a preset that uses `inherits` must come after its parent, or the bundle load aborts with `Can not find inherits ...` before later presets are parsed.
- When a vendor bundle fails during process loading, missing filaments can be a downstream symptom rather than a separate material bug, because the loader never reaches `filament_list` after the earlier exception.
- For MakerWorld compatibility, a converted printer needs the Bambu-style parallel process variants at shared layer heights, not just one preset per height. Missing `High Quality` or `Strength` tiers makes project-profile preservation fall back even when the printer itself loads.
- A blanket repo-level `*.png` ignore can silently drop shipping printer assets from the PR. Converted-printer previews, wizard thumbnails, guide covers, and buildplate textures need explicit unignore rules or a forced add.
- The historical `validate_profiles.py` helper was useful for manifest wiring and reference-order checks, but it still treated inherited process values as missing because it validated raw JSON before flattening the inheritance chain.
