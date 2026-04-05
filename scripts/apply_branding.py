#!/usr/bin/env python3
from __future__ import annotations

import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from zed_cn_macos.config import load_paths


def replace_all(text: str, replacements: list[tuple[str, str]]) -> str:
    for old, new in replacements:
        if new in text:
            continue
        if old not in text:
            raise RuntimeError(f"Expected snippet not found: {old}")
        text = text.replace(old, new)
    return text


def main() -> int:
    paths = load_paths(ROOT)
    cargo_toml = paths.source_dir / "crates" / "zed" / "Cargo.toml"
    resources_dir = paths.source_dir / "crates" / "zed" / "resources"
    branding_dir = ROOT / "assets" / "brand"

    content = cargo_toml.read_text()
    content = replace_all(
        content,
        [
            ('identifier = "dev.zed.Zed"', 'identifier = "dev.eqavo.Eqavo"'),
            ('name = "Zed"', 'name = "Eqavo"'),
            (
                'icon = ["resources/app-icon@2x.png", "resources/app-icon.png"]',
                'icon = ["resources/app-icon@2x.png", "resources/app-icon.png"]',
            ),
            ('osx_url_schemes = ["zed"]', 'osx_url_schemes = ["eqavo"]'),
        ],
    )
    cargo_toml.write_text(content)

    shutil.copy2(branding_dir / "app-icon.png", resources_dir / "app-icon.png")
    shutil.copy2(branding_dir / "app-icon@2x.png", resources_dir / "app-icon@2x.png")
    shutil.copy2(branding_dir / "Eqavo.icns", resources_dir / "Document.icns")

    print("Applied Eqavo branding to synced Zed source.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
