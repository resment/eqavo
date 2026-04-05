#!/bin/zsh
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

source .venv/bin/activate

python3 scripts/sync_zed.py
python3 scripts/apply_translations.py
python3 scripts/patch_agent_env.py
python3 scripts/disable_services.py
python3 scripts/apply_branding.py

cd "$ROOT/.workdir/zed-src"
source "$HOME/.cargo/env"
export BINDGEN_EXTRA_CLANG_ARGS="--sysroot=$(xcrun --show-sdk-path)"

cargo build --release --package zed

echo ""
echo "Build complete:"
echo "$ROOT/.workdir/zed-src/target/release/zed"
