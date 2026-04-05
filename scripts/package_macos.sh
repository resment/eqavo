#!/bin/zsh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

TARGET_TRIPLE="${1:-aarch64-apple-darwin}"

source .venv/bin/activate

python3 scripts/generate_icons.py
if [[ "${EQAVO_SKIP_SYNC:-0}" != "1" ]]; then
  python3 scripts/sync_zed.py
fi
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
python3 "$ROOT/scripts/verify_release_safety.py" "$APP_PATH"

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
