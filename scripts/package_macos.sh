#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TARGET_TRIPLE="${1:-aarch64-apple-darwin}"
DMG_BACKGROUND_PATH="$ROOT/assets/brand/dmg-background.png"

sign_app_bundle() {
  local path="$1"

  if [[ -n "${APPLE_DEVELOPER_IDENTITY:-}" ]]; then
    codesign --force --deep --sign "$APPLE_DEVELOPER_IDENTITY" "$path"
  else
    codesign --force --deep --sign - "$path"
  fi
}

sign_file() {
  local path="$1"

  if [[ -n "${APPLE_DEVELOPER_IDENTITY:-}" ]]; then
    codesign --force --sign "$APPLE_DEVELOPER_IDENTITY" "$path"
  else
    codesign --force --sign - "$path"
  fi
}

notarize_if_configured() {
  local path="$1"

  if [[ -z "${APPLE_IDENTITY_TEAM_ID:-}" || -z "${APPLE_ID:-}" || -z "${APPLE_APP_SPECIFIC_PASSWORD:-}" ]]; then
    return 0
  fi

  xcrun notarytool submit \
    "$path" \
    --apple-id "$APPLE_ID" \
    --password "$APPLE_APP_SPECIFIC_PASSWORD" \
    --team-id "$APPLE_IDENTITY_TEAM_ID" \
    --wait
}

customize_dmg_layout() {
  local volume_name="$1"

  osascript <<EOF >/dev/null
tell application "Finder"
  tell disk "${volume_name}"
    open
    tell container window
      set current view to icon view
      set toolbar visible to false
      set statusbar visible to false
      set bounds to {120, 120, 980, 660}
      set theViewOptions to the icon view options
      set icon size of theViewOptions to 144
      set text size of theViewOptions to 16
      try
        set background picture of theViewOptions to file ".background:dmg-background.png"
      end try
    end tell
    try
      set position of item "Eqavo.app" of container window to {220, 270}
      set position of item "Applications" of container window to {620, 270}
    end try
    update without registering applications
    delay 2
    close
  end tell
end tell
EOF
}

source .venv/bin/activate

python3 scripts/generate_icons.py
python3 scripts/generate_dmg_background.py
if [[ "${EQAVO_SKIP_SYNC:-0}" != "1" ]]; then
  python3 scripts/sync_zed.py
fi
python3 scripts/apply_translations.py
python3 scripts/patch_agent_env.py
python3 scripts/disable_services.py
python3 scripts/apply_branding.py

cd "$ROOT/.workdir/zed-src"
source "$HOME/.cargo/env"

rustup target add "$TARGET_TRIPLE"
export CXXFLAGS="-stdlib=libc++"
export BINDGEN_EXTRA_CLANG_ARGS="--sysroot=$(xcrun --show-sdk-path)"
export ZED_RELEASE_CHANNEL="stable"
export ZED_BUNDLE=true

if ! cargo -q bundle --help 2>&1 | head -n 1 | grep -q "cargo-bundle v0.6.1-zed"; then
  cargo install cargo-bundle --git https://github.com/zed-industries/cargo-bundle.git --branch zed-deploy
fi

zsh script/generate-licenses
cargo build --release --package zed --package cli --target "$TARGET_TRIPLE"

pushd crates/zed >/dev/null
cp Cargo.toml Cargo.toml.backup
sed -i.backup "s/package.metadata.bundle-stable/package.metadata.bundle/" Cargo.toml
APP_PATH="$(cargo bundle --release --target "$TARGET_TRIPLE" | xargs)"
mv Cargo.toml.backup Cargo.toml
rm -f Cargo.toml.backup
popd >/dev/null

cp "target/$TARGET_TRIPLE/release/cli" "$APP_PATH/Contents/MacOS/cli"
cp "crates/zed/resources/Document.icns" "$APP_PATH/Contents/Resources/Document.icns"
sign_app_bundle "$APP_PATH"
codesign --verify --deep --strict --verbose=2 "$APP_PATH"
python3 "$ROOT/scripts/verify_release_safety.py" "$APP_PATH"

ARCH_SUFFIX="aarch64"
if [[ "$TARGET_TRIPLE" == "x86_64-apple-darwin" ]]; then
  ARCH_SUFFIX="x86_64"
fi

DMG_TARGET_DIR="target/$TARGET_TRIPLE/release"
DMG_SOURCE_DIR="$DMG_TARGET_DIR/dmg"
DMG_PATH="$DMG_TARGET_DIR/Eqavo-$ARCH_SUFFIX.dmg"
DMG_RW_PATH="$DMG_TARGET_DIR/Eqavo-$ARCH_SUFFIX.rw.dmg"
DMG_MOUNT_OUTPUT="$DMG_TARGET_DIR/Eqavo-$ARCH_SUFFIX.mount.txt"

rm -rf "$DMG_SOURCE_DIR" "$DMG_RW_PATH" "$DMG_MOUNT_OUTPUT"
rm -f "$DMG_PATH"
mkdir -p "$DMG_SOURCE_DIR"
mkdir -p "$DMG_SOURCE_DIR/.background"
cp -R "$APP_PATH" "$DMG_SOURCE_DIR/"
ln -s /Applications "$DMG_SOURCE_DIR/Applications"
cp "$DMG_BACKGROUND_PATH" "$DMG_SOURCE_DIR/.background/dmg-background.png"

hdiutil create -volname Eqavo -srcfolder "$DMG_SOURCE_DIR" -ov -format UDRW "$DMG_RW_PATH"
hdiutil attach -readwrite -noverify -noautoopen "$DMG_RW_PATH" > "$DMG_MOUNT_OUTPUT"

DMG_DEVICE="$(awk '/Apple_HFS/ {print $1; exit}' "$DMG_MOUNT_OUTPUT")"
if [[ -z "$DMG_DEVICE" ]]; then
  DMG_DEVICE="$(awk 'NR==1 {print $1}' "$DMG_MOUNT_OUTPUT")"
fi

if command -v osascript >/dev/null 2>&1; then
  customize_dmg_layout "Eqavo" || true
fi

sync
for attempt in 1 2 3; do
  if hdiutil detach "$DMG_DEVICE"; then
    break
  fi
  sleep 2
done

if diskutil info "$DMG_DEVICE" >/dev/null 2>&1; then
  hdiutil detach -force "$DMG_DEVICE"
fi

hdiutil convert "$DMG_RW_PATH" -ov -format UDZO -imagekey zlib-level=9 -o "$DMG_PATH"
sign_file "$DMG_PATH"
notarize_if_configured "$DMG_PATH"
if [[ -n "${APPLE_IDENTITY_TEAM_ID:-}" && -n "${APPLE_ID:-}" && -n "${APPLE_APP_SPECIFIC_PASSWORD:-}" ]]; then
  xcrun stapler staple "$APP_PATH" || true
  xcrun stapler staple "$DMG_PATH" || true
fi

rm "$DMG_SOURCE_DIR/Applications"
rm -rf "$DMG_SOURCE_DIR"
rm -f "$DMG_RW_PATH" "$DMG_MOUNT_OUTPUT"

echo ""
echo "Created DMG:"
echo "$DMG_PATH"
