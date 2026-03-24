# Building Pandaforge

## Prerequisites

```bash
# Install Xcode from App Store (required)
# Install Homebrew dependencies
brew install cmake git gettext nasm yasm x264
```

## Step 1: Build Dependencies (One-Time, 30-60 min)

```bash
cd BambuStudio-2.5.0.66/deps
mkdir -p build && cd build

# For Apple Silicon (arm64)
cmake ../ \
  -DDESTDIR="/Users/$(whoami)/Pandaforge Project/BambuStudio_dep_2.5.0.66" \
  -DOPENSSL_ARCH="darwin64-arm64-cc"

# For Intel (x86_64)
cmake ../ \
  -DDESTDIR="/Users/$(whoami)/Pandaforge Project/BambuStudio_dep_2.5.0.66" \
  -DOPENSSL_ARCH="darwin64-x86_64-cc"

make -j4  # IMPORTANT: Use -j4 not -j8 to prevent build deadlock
```

Dependencies are built once and reused across application rebuilds.

## Step 2: Build Application (30-60 min)

```bash
cd BambuStudio-2.5.0.66
mkdir -p build && cd build

cmake .. \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DBBL_RELEASE_TO_PUBLIC=1 \
  -DCMAKE_PREFIX_PATH="/Users/$(whoami)/Pandaforge Project/BambuStudio_dep_2.5.0.66/usr/local" \
  -DCMAKE_INSTALL_PREFIX="../install_dir" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_MACOSX_BUNDLE=ON

cmake --build . --target install --config Release -j4
```

## Step 3: Run

```bash
open "BambuStudio-2.5.0.66/install_dir/BambuStudio.app"
```

Or copy to Applications:
```bash
cp -R "BambuStudio-2.5.0.66/install_dir/BambuStudio.app" /Applications/
```

## CMake Options Reference

| Option | Description | Default |
|---|---|---|
| `SLIC3R_GUI` | Build with GUI components | ON |
| `SLIC3R_STATIC` | Use static libraries | ON (macOS) |
| `SLIC3R_BUILD_TESTS` | Build unit tests | OFF |
| `SLIC3R_BUILD_SANDBOXES` | Build development sandboxes | OFF |
| `SLIC3R_PCH` | Use precompiled headers | ON |
| `BBL_RELEASE_TO_PUBLIC` | Enable public release features | 0 |
| `CMAKE_BUILD_TYPE` | Release or Debug | Release |

## Troubleshooting

### Build Deadlock

**Always use `-j4` not `-j8`.** Higher parallelism causes deadlock on large translation units.

### Space-in-Path Issues

If your project path contains spaces, CMake may fail to find wxWidgets. Create a symlink:

```bash
ln -s "/Users/$(whoami)/Pandaforge Project/BambuStudio_dep_2.5.0.66/usr/local" ~/bambu_deps

# Update wx-config paths
sed -i '' "s|/Users/$(whoami)/Pandaforge Project/BambuStudio_dep_2.5.0.66/usr/local|/Users/$(whoami)/bambu_deps|g" \
  "$(brew --prefix)/bin/wx-config"

# Use symlink in CMake
cmake .. -DCMAKE_PREFIX_PATH="/Users/$(whoami)/bambu_deps" ...
```

### ICU Linking Error

```bash
export LDFLAGS="-L/opt/homebrew/opt/icu4c@78/lib"
```

### CMake Version Warnings

Add `-DCMAKE_POLICY_VERSION_MINIMUM=3.5` to the cmake configure command.

### Clean Rebuild

```bash
rm -rf build && mkdir build
```

## References

- [Official BambuStudio Mac Compile Guide](https://github.com/bambulab/BambuStudio/wiki/Mac-Compile-Guide)
