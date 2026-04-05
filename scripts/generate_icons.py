#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
BRAND_DIR = ROOT / "assets" / "brand"
SVG_PATH = BRAND_DIR / "eqavo-icon.svg"
MASTER_PNG_PATH = BRAND_DIR / "eqavo-icon-1024.png"
RENDER_DIR = BRAND_DIR / "render"
ICONSET_DIR = BRAND_DIR / "Eqavo.iconset"
ICNS_PATH = BRAND_DIR / "Eqavo.icns"


def render_master_png() -> Path:
    if MASTER_PNG_PATH.exists():
        return MASTER_PNG_PATH

    RENDER_DIR.mkdir(parents=True, exist_ok=True)
    temp_output = RENDER_DIR / "eqavo-icon.svg.png"

    subprocess.run(
        [
            "qlmanage",
            "-t",
            "-s",
            "1024",
            "-o",
            str(RENDER_DIR),
            str(SVG_PATH),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    if not temp_output.exists():
        raise RuntimeError("Quick Look did not produce the expected rasterized icon output")

    shutil.move(temp_output, MASTER_PNG_PATH)
    return MASTER_PNG_PATH


def write_resized_png(source: Image.Image, size: int, output: Path) -> None:
    resized = source.resize((size, size), Image.Resampling.LANCZOS)
    resized.save(output, format="PNG")


def generate_iconset(master_png: Path) -> None:
    if ICONSET_DIR.exists():
        shutil.rmtree(ICONSET_DIR)
    ICONSET_DIR.mkdir(parents=True, exist_ok=True)

    image = Image.open(master_png).convert("RGBA")
    sizes = {
        "icon_16x16.png": 16,
        "icon_16x16@2x.png": 32,
        "icon_32x32.png": 32,
        "icon_32x32@2x.png": 64,
        "icon_128x128.png": 128,
        "icon_128x128@2x.png": 256,
        "icon_256x256.png": 256,
        "icon_256x256@2x.png": 512,
        "icon_512x512.png": 512,
        "icon_512x512@2x.png": 1024,
    }

    for name, size in sizes.items():
        write_resized_png(image, size, ICONSET_DIR / name)

    write_resized_png(image, 512, BRAND_DIR / "app-icon.png")
    write_resized_png(image, 1024, BRAND_DIR / "app-icon@2x.png")


def generate_icns(master_png: Path) -> None:
    image = Image.open(master_png).convert("RGBA")
    image.save(
        ICNS_PATH,
        format="ICNS",
        sizes=[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256), (512, 512), (1024, 1024)],
    )


def main() -> int:
    master = render_master_png()
    generate_iconset(master)
    generate_icns(master)
    print(f"Generated iconset at: {ICONSET_DIR}")
    print(f"Generated icns at: {ICNS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
