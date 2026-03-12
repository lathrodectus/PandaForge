# Moonraker API Integration

## HTTP Endpoints

The FanControlPanel communicates with Moonraker using these endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/printer` | Get printer status (temperatures, fans, position) |
| `POST` | `/api/printer/command` | Send G-code command |
| `GET` | `/api/server/info` | Get Moonraker server info |
| `POST` | `/printer/gcode/script` | Execute G-code script |

## HTTP Communication

FanControlPanel uses **libcurl** for HTTP requests to the Moonraker API.

```cpp
void SetPrinterURL(const wxString& url);  // e.g., "http://192.168.1.100:7125"
bool SendGCode(const wxString& gcode);     // Sends via POST /api/printer/command
void StartPolling(int interval_ms = 2000); // Polls GET /api/printer every 2s
```

Communication is **HTTP only** (not HTTPS). Ensure printers are on trusted networks.

## Current Implementation (Phase 1)

- FanControlPanel polls printer status every 2 seconds
- Supports Part cooling, Chamber, Aux, and Exhaust fan control
- Predefined profiles for common Klipper printers:
  - Creality K1
  - Qidi Q2
  - Flashforge 5M
  - Centauri Carbon

## Phase 2 Roadmap

| Feature | Priority | Technical Approach |
|---|---|---|
| Fan speed control | High | HTTP POST to Moonraker API |
| Temperature monitoring | High | Poll `/api/printer` endpoint |
| Print status | Medium | WebSocket connection |
| Camera feed | Low | Embed MJPEG stream |

## References

- [Moonraker API Documentation](https://moonraker.readthedocs.io/)
- [Klipper Documentation](https://www.klipper3d.org/)
