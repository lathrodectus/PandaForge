# BambuStudio macOS Build Guide

This document describes how to build BambuStudio on macOS using the official method from [BambuLab's Mac Compile Guide](https://github.com/bambulab/BambuStudio/wiki/Mac-Compile-Guide).

## Prerequisites

Install the following tools:
- **Xcode** from App Store
- **CMake**, **git**, **gettext** via Homebrew:
  ```bash
  brew install cmake git gettext
  ```

Install FFmpeg build dependencies:
```bash
brew install nasm yasm x264
```

## Build Steps

### Step 1: Build Dependencies (First Time Only)

Create a directory for dependencies:
```bash
mkdir -p "/Users/$(whoami)/pandaforge/BambuStudio_dep"
```

Build the dependencies:
```bash
cd "/Users/$(whoami)/pandaforge/BambuStudio-2.5.0.66/deps"
mkdir -p build && cd build

# For Apple Silicon (arm64)
cmake ../ \
  -DDESTDIR="/Users/$(whoami)/pandaforge/BambuStudio_dep" \
  -DOPENSSL_ARCH="darwin64-arm64-cc"

# For Intel (x86_64)
cmake ../ \
  -DDESTDIR="/Users/$(whoami)/pandaforge/BambuStudio_dep" \
  -DOPENSSL_ARCH="darwin64-x86_64-cc"

# Build (replace N with number of CPU cores)
make -j8
```

**Note:** This step takes 30-60 minutes and only needs to be done once.

### Step 2: Build BambuStudio

Create build directory:
```bash
cd "/Users/$(whoami)/pandaforge/BambuStudio-2.5.0.66"
mkdir -p install_dir
mkdir -p build && cd build
```

Configure with CMake:
```bash
cmake .. \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DBBL_RELEASE_TO_PUBLIC=1 \
  -DCMAKE_PREFIX_PATH="/Users/$(whoami)/pandaforge/BambuStudio_dep/usr/local" \
  -DCMAKE_INSTALL_PREFIX="../install_dir" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_MACOSX_RPATH=ON \
  -DCMAKE_INSTALL_RPATH="/Users/$(whoami)/pandaforge/BambuStudio_dep/usr/local" \
  -DCMAKE_MACOSX_BUNDLE=ON
```

Build and install:
```bash
cmake --build . --target install --config Release -j8
```

**Note:** This step takes 30-60 minutes depending on your Mac.

### Step 3: Run BambuStudio

After successful build, the app bundle is located at:
```
/Users/$(whoami)/pandaforge/BambuStudio-2.5.0.66/install_dir/BambuStudio.app
```

Run it:
```bash
open "/Users/$(whoami)/pandaforge/BambuStudio-2.5.0.66/install_dir/BambuStudio.app"
```

Or copy to Applications:
```bash
cp -R "/Users/$(whoami)/pandaforge/BambuStudio-2.5.0.66/install_dir/BambuStudio.app" /Applications/
```

## Troubleshooting

### Space in Path Issues

If your path contains spaces (like "pandaforge"), CMake may have issues with wxWidgets detection. Fix the wx-config symlink:

```bash
# Create symlink without spaces
ln -s "/Users/$(whoami)/pandaforge/BambuStudio_dep/usr/local" ~/bambu_deps

# Update wx-config script paths
sed -i '' "s|/Users/$(whoami)/pandaforge/BambuStudio_dep/usr/local|/Users/$(whoami)/bambu_deps|g" \
  "/Users/$(whoami)/bambu_deps/lib/wx/config/osx_cocoa-unicode-static-3.1"

# Use symlink in CMake configuration
cmake .. \
  -DCMAKE_PREFIX_PATH="/Users/$(whoami)/bambu_deps" \
  -DwxWidgets_CONFIG_EXECUTABLE="/Users/$(whoami)/bambu_deps/bin/wx-config" \
  ...
```

### CMake Version Compatibility

If you see errors about CMake minimum version, add:
```bash
-DCMAKE_POLICY_VERSION_MINIMUM=3.5
```

### Missing Libraries

If linking fails with missing ICU libraries:
```bash
export LDFLAGS="-L/opt/homebrew/opt/icu4c@78/lib"
```

## Build Configuration Options

| Option | Description |
|--------|-------------|
| `-DCMAKE_BUILD_TYPE=Release` | Release build (optimized) |
| `-DCMAKE_BUILD_TYPE=Debug` | Debug build |
| `-DBBL_RELEASE_TO_PUBLIC=1` | Enable public release features |
| `-j8` | Use 8 parallel jobs (adjust to your CPU cores) |

## Directory Structure

```
pandaforge/
├── BambuStudio-2.5.0.66/      # Source code
│   ├── build/                  # Build directory
│   ├── install_dir/            # Install output
│   └── deps/                   # Dependencies source
├── BambuStudio_dep/            # Built dependencies
│   └── usr/local/
│       ├── bin/                # Tools including wx-config
│       ├── lib/                # Libraries
│       └── include/            # Headers
└── BUILD_GUIDE.md              # This file
```

## References

- [Official BambuStudio Mac Compile Guide](https://github.com/bambulab/BambuStudio/wiki/Mac-Compile-Guide)
- [BambuStudio GitHub Repository](https://github.com/bambulab/BambuStudio)
