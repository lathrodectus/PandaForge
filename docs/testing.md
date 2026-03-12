# Testing

## Framework

- **Framework:** Catch2 v2.x
- **Location:** `BambuStudio-2.5.0.66/tests/`
- **Test Data:** `tests/data/`

## Build with Tests

```bash
cd BambuStudio-2.5.0.66/build

cmake .. -DSLIC3R_BUILD_TESTS=ON \
  -DCMAKE_PREFIX_PATH="/Users/$(whoami)/Pandaforge Project/BambuStudio_dep_2.5.0.66/usr/local" \
  -DCMAKE_BUILD_TYPE=Release

make -j4
```

## Run Tests

```bash
cd tests
ctest --output-on-failure
```

## Test Categories

| Directory | Purpose |
|---|---|
| `tests/libslic3r/` | Core library unit tests |
| `tests/fff_print/` | FFF (filament) slicing tests |
| `tests/sla_print/` | SLA (resin) slicing tests |
| `tests/libnest2d/` | Nesting algorithm tests |
