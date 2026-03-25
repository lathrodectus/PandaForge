# BambuStudio macOS Build Guide

This is the longer historical macOS guide with the lessons that led to the current local build flow.

Read [../../03-task-guides/build.md](../../03-task-guides/build.md) first for the current March 25, 2026 build status. This file keeps the detailed install-dir flow and the path lessons.

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

Create a no-space source alias if your workspace path contains spaces:

```bash
ln -sfn "/Users/$(whoami)/Pandaforge Project" /tmp/pandaforge-src
```

Create a directory for dependencies:
```bash
mkdir -p "/Users/$(whoami)/Pandaforge-deps"
```

Build the dependencies:
```bash
cmake -S /tmp/pandaforge-src/deps \
  -B /tmp/pandaforge-deps-build-arm64 \
  -G Ninja \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DDESTDIR="/Users/$(whoami)/Pandaforge-deps" \
  -DOPENSSL_ARCH="darwin64-arm64-cc" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DCMAKE_OSX_DEPLOYMENT_TARGET=10.15

cmake --build /tmp/pandaforge-deps-build-arm64 -j4
```

**Note:** This step takes 30-60 minutes and only needs to be done once.

Verify the prefix before moving on:

```bash
ls -l "/Users/$(whoami)/Pandaforge-deps/usr/local/bin/wx-config"
```

### Step 2: Build BambuStudio

Create build directory:
```bash
mkdir -p "/Users/$(whoami)/Pandaforge Project/install_dir"
```

Configure with CMake:
```bash
cmake -S /tmp/pandaforge-src \
  -B /tmp/pandaforge-app-build-arm64 \
  -G Ninja \
  -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
  -DBBL_RELEASE_TO_PUBLIC=1 \
  -DCMAKE_PREFIX_PATH="/Users/$(whoami)/Pandaforge-deps/usr/local" \
  -DwxWidgets_CONFIG_EXECUTABLE="/Users/$(whoami)/Pandaforge-deps/usr/local/bin/wx-config" \
  -DCMAKE_INSTALL_PREFIX="/Users/$(whoami)/Pandaforge Project/install_dir" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_MACOSX_RPATH=ON \
  -DCMAKE_INSTALL_RPATH="/Users/$(whoami)/Pandaforge-deps/usr/local" \
  -DCMAKE_MACOSX_BUNDLE=ON \
  -DCMAKE_OSX_ARCHITECTURES=arm64 \
  -DCMAKE_OSX_DEPLOYMENT_TARGET=10.15
```

Build and install:
```bash
cmake --build /tmp/pandaforge-app-build-arm64 --target install --config Release -j4
```

**Note:** This step takes 30-60 minutes depending on your Mac.

### Step 3: Run BambuStudio

After successful build, the app bundle is located at:
```
/Users/$(whoami)/Pandaforge Project/install_dir/bin/BambuStudio.app
```

Run it:
```bash
open "/Users/$(whoami)/Pandaforge Project/install_dir/bin/BambuStudio.app"
```

Or copy to Applications:
```bash
cp -R "/Users/$(whoami)/Pandaforge Project/install_dir/bin/BambuStudio.app" /Applications/
```

## Troubleshooting

### Space in Path Issues

If your path contains spaces, keep using the `/tmp/pandaforge-src` symlink so both configure steps run against a no-space source path:

```bash
ln -sfn "/Users/$(whoami)/Pandaforge Project" /tmp/pandaforge-src
```

### CMake Version Compatibility

If you see errors about CMake minimum version, add:
```bash
-DCMAKE_POLICY_VERSION_MINIMUM=3.5
```

### March 25, 2026 AppleClang notes

The successful scratch build still needed two local compatibility fixes:

- The top-level `CMakeLists.txt` must only add `-Wno-error=enum-constexpr-conversion` when the compiler actually supports it.
- `src/slic3r/GUI/MediaPlayCtrl.h` and `src/slic3r/GUI/wxMediaCtrl2.h` cannot declare extra `wxMediaState` sentinel values as `constexpr` on this AppleClang toolchain; runtime casts are accepted.

The earlier failure that led to this was in `src/slic3r/Utils/OctoPrint.cpp`:

```text
fatal error: cannot open file '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/unordered_map'
```

Treat that as a historical blocker after configure and dependency setup, not as a dependency-prefix failure.

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
├── Pandaforge Project/         # Source code
│   ├── install_dir/            # Install output
│   └── deps/                   # Dependencies source
├── Pandaforge-deps/            # Built dependencies
│   └── usr/local/
│       ├── bin/                # Tools including wx-config
│       ├── lib/                # Libraries
│       └── include/            # Headers
└── /tmp/pandaforge-src         # No-space source symlink used during builds
```

## References

- [Official BambuStudio Mac Compile Guide](https://github.com/bambulab/BambuStudio/wiki/Mac-Compile-Guide)
- [BambuStudio GitHub Repository](https://github.com/bambulab/BambuStudio)
