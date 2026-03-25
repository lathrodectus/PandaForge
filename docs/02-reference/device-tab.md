# Device Tab And Print Host Web UI

This branch does not currently ship a native Moonraker API layer. The active third-party printer integration path is the Device tab loading the printer's web UI through `print_host_webui`, or `print_host` when no dedicated web UI URL is configured.

## Current Flow

| Step | File |
|---|---|
| trigger from UI/plater | `src/slic3r/GUI/Plater.cpp` |
| resolve and load printer URL | `src/slic3r/GUI/MainFrame.cpp` |
| render embedded browser | `src/slic3r/GUI/PrinterWebView.cpp` |
| configure host/web UI values | `src/slic3r/GUI/PhysicalPrinterDialog.cpp` |

## What This Means

- For non-BBL printers, the important settings are `print_host` and optionally `print_host_webui`.
- The app embeds Fluidd, Mainsail, or another printer web UI through `wxWebView`.
- If you need native Moonraker HTTP polling, fan control panels, or websocket state sync, that is future work, not current branch reality.

## Practical Debugging

Check these first:

1. The selected physical printer configuration exposes a valid `print_host` or `print_host_webui`.
2. Configure `print_host` and optionally `print_host_webui` in the Physical Printer dialog.
3. The URL includes the protocol, or the app can normalize a bare host by adding `http://`.
4. The target web UI is reachable outside the app.

## Historical Note

Older docs may describe a `FanControlPanel` and direct Moonraker REST polling. Those notes are archived history, not the current implementation.
