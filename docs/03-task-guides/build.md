# Build

This is the active build-status brief. For the longer macOS walkthrough and the older lessons that led here, also keep [../90-history/plans/build-guide-v1.md](../90-history/plans/build-guide-v1.md) open.

## Current Recommendation

- macOS: use the `install_dir` CMake flow described below.
- Linux: use `BuildLinux.sh`.
- Windows: use `build_win.bat`.
- Do not treat `BuildMac.sh` as the primary documented path for this branch.

## Verified macOS Status

Verified on March 25, 2026:

- A fresh dependency build completed into `/Users/$(whoami)/Pandaforge-deps/usr/local`.
- App configure succeeded against that prefix.
- The app build now completes successfully with `cmake --build /tmp/pandaforge-app-build-arm64 --target install --config Release -j4`.
- The installed app bundle should land at `install_dir/bin/PandaForge.app`.
- Two AppleClang compatibility fixes were required in this branch:
  - guard `-Wno-error=enum-constexpr-conversion` behind a compiler support check in `CMakeLists.txt`
  - avoid `constexpr wxMediaState` sentinels outside wx's enum range in `src/slic3r/GUI/MediaPlayCtrl.h` and `src/slic3r/GUI/wxMediaCtrl2.h`
- The earlier blocker seen in this workspace was:

```text
fatal error: cannot open file '/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/unordered_map'
```

## macOS Scratch Flow

Use a no-space source path even if the real workspace lives at `Pandaforge Project`:

```bash
ln -sfn "/Users/$(whoami)/Pandaforge Project" /tmp/pandaforge-src
```

### 1. Build dependencies

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

Verify the prefix before configuring the app:

```bash
ls -l "/Users/$(whoami)/Pandaforge-deps/usr/local/bin/wx-config"
```

### 2. Configure the app build

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

### 3. Build and install

```bash
cmake --build /tmp/pandaforge-app-build-arm64 --target install --config Release -j4
```

If the build completes, the bundle should land at:

```text
/Users/$(whoami)/Pandaforge Project/install_dir/bin/PandaForge.app
```

## Notes That Matter

- Dependency recipes live under `deps/`.
- Top-level configure entry is `CMakeLists.txt`.
- `install_dir/bin/PandaForge.app` is the expected local app output for the documented macOS flow after the PandaForge naming change.
- `docs/02-reference/naming.md` documents where the bundle name and `Application Support` path come from.
- `docs/90-history/plans/build-guide-v1.md` remains the best place for background and lessons, but this file is the current status page agents should trust first.
