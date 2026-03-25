# Testing

## Automated Tests

This file is mainly about the CMake/Catch2 test surface under:

```text
tests/
```

Main groups:

| Path | Purpose |
|---|---|
| `tests/libslic3r/` | core library behavior |
| `tests/fff_print/` | FFF slicing flows |
| `tests/sla_print/` | SLA flows |
| `tests/libnest2d/` | nesting behavior |

Other test trees also exist in this repo:

- `t/`
- `xs/t/`

## Build Tests

Build deps first for your target architecture, then configure a test build from the repo root:

```bash
mkdir -p build/tests-arm64
cd build/tests-arm64

cmake ../.. \
  -DSLIC3R_BUILD_TESTS=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="/Users/$(whoami)/Pandaforge-deps/usr/local"

cmake --build . --config Release -j4
```

Adjust `arm64` to `x86_64` if needed.

## Run Tests

From the test build directory:

```bash
ctest --output-on-failure
```

## High-Value Manual Smoke Checks

When changing third-party/Klipper behavior, also do targeted manual checks:

1. Open a printer profile from `resources/profiles/`.
2. Slice a small model and inspect the generated G-code for `SET_PRESSURE_ADVANCE` when enabled.
3. Verify the Device tab can load the configured `print_host` or `print_host_webui` for a non-BBL printer.
4. If profile data changed, verify the preset actually appears in the UI and resolves its inheritance chain.

## When To Prefer Smoke Tests

Prefer focused manual validation when you touch:

- profile manifests
- profile asset paths
- Device tab / embedded web UI
- UI-only settings exposure

Those flows are only partially covered by automated tests.
