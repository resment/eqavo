#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TARGET_TRIPLE="${1:-aarch64-apple-darwin}"

source .venv/bin/activate

python3 scripts/generate_icons.py
python3 scripts/sync_zed.py
python3 scripts/apply_translations.py
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

script/generate-licenses
cargo build --release --package zed --package cli --target "$TARGET_TRIPLE"

APP_PATH="$(cargo bundle --release --target "$TARGET_TRIPLE" --package zed --select-workspace-root | xargs)"
cp "target/$TARGET_TRIPLE/release/cli" "$APP_PATH/Contents/MacOS/cli"
cp "crates/zed/resources/Document.icns" "$APP_PATH/Contents/Resources/Document.icns"

ARCH_SUFFIX="aarch64"
if [[ "$TARGET_TRIPLE" == "x86_64-apple-darwin" ]]; then
  ARCH_SUFFIX="x86_64"
fi

DMG_TARGET_DIR="target/$TARGET_TRIPLE/release"
DMG_SOURCE_DIR="$DMG_TARGET_DIR/dmg"
DMG_PATH="$DMG_TARGET_DIR/Eqavo-$ARCH_SUFFIX.dmg"

rm -rf "$DMG_SOURCE_DIR"
mkdir -p "$DMG_SOURCE_DIR"
mv "$APP_PATH" "$DMG_SOURCE_DIR"
ln -s /Applications "$DMG_SOURCE_DIR/Applications"

hdiutil create -volname Eqavo -srcfolder "$DMG_SOURCE_DIR" -ov -format UDZO "$DMG_PATH"
rm "$DMG_SOURCE_DIR/Applications"

echo ""
echo "Created DMG:"
echo "$DMG_PATH"
