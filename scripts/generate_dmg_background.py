#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BRAND_DIR = ROOT / "assets" / "brand"
OUTPUT_PATH = BRAND_DIR / "dmg-background.png"
ICON_PATH = BRAND_DIR / "eqavo-icon-1024.png"


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def draw_gradient(image: Image.Image) -> None:
    width, height = image.size
    draw = ImageDraw.Draw(image)
    top = (15, 39, 47)
    mid = (8, 24, 31)
    bottom = (4, 12, 16)

    for y in range(height):
        if y < height * 0.55:
            ratio = y / (height * 0.55)
            color = tuple(int(top[i] * (1 - ratio) + mid[i] * ratio) for i in range(3))
        else:
            ratio = (y - height * 0.55) / (height * 0.45)
            color = tuple(int(mid[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)


def draw_glow(image: Image.Image, xy: tuple[int, int, int, int], fill: tuple[int, int, int, int], blur: int) -> None:
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.rounded_rectangle(xy, radius=48, fill=fill)
    glow = glow.filter(ImageFilter.GaussianBlur(blur))
    image.alpha_composite(glow)


def main() -> int:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    canvas = Image.new("RGBA", (1200, 780), (0, 0, 0, 255))
    draw_gradient(canvas)

    draw_glow(canvas, (70, 92, 530, 552), (120, 231, 255, 32), blur=28)
    draw_glow(canvas, (670, 168, 1130, 628), (120, 231, 255, 26), blur=36)

    card = ImageDraw.Draw(canvas)
    card.rounded_rectangle((82, 104, 518, 540), radius=52, fill=(5, 17, 22, 230), outline=(20, 57, 67, 255), width=8)
    card.rounded_rectangle((682, 180, 1118, 616), radius=52, fill=(7, 19, 25, 210), outline=(32, 87, 100, 255), width=6)

    icon = Image.open(ICON_PATH).convert("RGBA").resize((320, 320), Image.Resampling.LANCZOS)
    canvas.alpha_composite(icon, (140, 162))

    draw = ImageDraw.Draw(canvas)
    title_font = load_font(54)
    subtitle_font = load_font(28)
    label_font = load_font(24)

    draw.text((728, 244), "Install Eqavo", font=title_font, fill=(232, 247, 252, 255))
    draw.text((728, 322), "Drag Eqavo.app into Applications", font=subtitle_font, fill=(159, 205, 218, 255))
    draw.text((728, 386), "Unofficial macOS Chinese-localized build", font=label_font, fill=(117, 172, 187, 255))
    draw.text((728, 424), "based on Zed source", font=label_font, fill=(117, 172, 187, 255))

    draw.rounded_rectangle((728, 476, 1056, 538), radius=22, fill=(15, 67, 81, 255))
    draw.text((754, 492), "Apple Silicon build", font=label_font, fill=(206, 242, 252, 255))

    draw.rounded_rectangle((728, 556, 1098, 646), radius=22, fill=(7, 30, 38, 255), outline=(44, 128, 147, 255), width=2)
    draw.text((754, 574), "Sign-in, Zed AI,", font=label_font, fill=(176, 219, 231, 255))
    draw.text((754, 608), "and Pro upsells removed", font=label_font, fill=(176, 219, 231, 255))

    canvas.save(OUTPUT_PATH, format="PNG")
    print(f"Generated DMG background at: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
