#!/usr/bin/env python3
"""
PixelMood — Emotion image generator for SmallTV Ultra
Generates 10 emotion images (240x240 JPG) for Claude Code status display.
"""
import os
import math
import argparse
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = "/System/Library/Fonts/HelveticaNeue.ttc"

EMOTIONS = [
    ("thinking",  (15, 25, 60),   (80, 140, 255),  "dots",     "THINKING", "..."),
    ("working",   (50, 25, 0),    (255, 140, 0),   "gear",     "WORKING",  "..."),
    ("done",      (0, 50, 20),    (0, 220, 80),    "check",    "DONE",     "!"),
    ("nice",      (50, 40, 0),    (255, 210, 0),   "star",     "NICE",     "!"),
    ("error",     (60, 10, 10),   (255, 60, 60),   "cross",    "ERROR",    "!"),
    ("question",  (35, 10, 60),   (180, 80, 255),  "qmark",    "YES OR",   "NO?"),
    ("searching", (0, 40, 50),    (0, 200, 200),   "lens",     "ANALYZING","..."),
    ("idea",      (50, 35, 0),    (255, 180, 0),   "bulb",     "IDEA",     "!"),
    ("careful",   (55, 20, 0),    (255, 100, 0),   "triangle", "CAREFUL",  "!"),
    ("chat",      (15, 30, 40),   (80, 200, 180),  "bubble",   "CHAT",     "MODE"),
]


def get_font(size, bold=False):
    idx = 1 if bold else 0
    return ImageFont.truetype(FONT_PATH, size, index=idx)


def make_base(bg, accent):
    img = Image.new("RGB", (240, 240), bg)
    draw = ImageDraw.Draw(img)
    for x, y in [(0, 0), (220, 0), (0, 220), (220, 220)]:
        draw.rectangle([x, y, x + 20, y + 20], fill=accent)
    draw.rectangle([2, 2, 237, 237], outline=accent, width=2)
    return img, draw


def center_text(draw, y, text, size, color, bold=True):
    f = get_font(size, bold)
    bbox = f.getbbox(text)
    w = bbox[2] - bbox[0]
    draw.text((120 - w // 2, y), text, font=f, fill=color)


def draw_dots(draw, cx, cy, accent):
    for dx in [-36, 0, 36]:
        r = 14
        draw.ellipse([cx + dx - r, cy - r, cx + dx + r, cy + r], fill=accent)


def draw_gear(draw, cx, cy, accent):
    draw.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], outline=accent, width=6)
    draw.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=accent)
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        x1, y1 = cx + 38 * math.cos(rad), cy + 38 * math.sin(rad)
        x2, y2 = cx + 52 * math.cos(rad), cy + 52 * math.sin(rad)
        draw.line([x1, y1, x2, y2], fill=accent, width=10)


def draw_check(draw, cx, cy, accent):
    pts = [(cx - 45, cy), (cx - 15, cy + 35), (cx + 45, cy - 35)]
    draw.line([pts[0], pts[1]], fill=accent, width=12)
    draw.line([pts[1], pts[2]], fill=accent, width=12)


def draw_star(draw, cx, cy, accent):
    pts = []
    for i in range(10):
        r = 50 if i % 2 == 0 else 22
        ang = math.radians(i * 36 - 90)
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    draw.polygon(pts, fill=accent)


def draw_cross(draw, cx, cy, accent):
    draw.line([cx - 40, cy - 40, cx + 40, cy + 40], fill=accent, width=14)
    draw.line([cx + 40, cy - 40, cx - 40, cy + 40], fill=accent, width=14)


def draw_qmark(draw, cx, cy, accent):
    f = ImageFont.truetype(FONT_PATH, 110, index=1)
    bbox = f.getbbox("?")
    w = bbox[2] - bbox[0]
    draw.text((cx - w // 2, cy - 65), "?", font=f, fill=accent)


def draw_lens(draw, cx, cy, accent):
    draw.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], outline=accent, width=8)
    draw.line([cx + 28, cy + 28, cx + 50, cy + 50], fill=accent, width=12)


def draw_bulb(draw, cx, cy, accent):
    draw.ellipse([cx - 35, cy - 50, cx + 35, cy + 20], outline=accent, width=7)
    draw.rectangle([cx - 20, cy + 18, cx + 20, cy + 38], outline=accent, width=5)
    draw.line([cx - 20, cy + 28, cx + 20, cy + 28], fill=accent, width=4)
    draw.line([cx - 20, cy + 35, cx + 20, cy + 35], fill=accent, width=4)


def draw_triangle(draw, cx, cy, accent):
    pts = [(cx, cy - 48), (cx - 48, cy + 35), (cx + 48, cy + 35)]
    draw.polygon(pts, outline=accent, width=8)
    f = ImageFont.truetype(FONT_PATH, 50, index=1)
    draw.text((cx - 8, cy - 15), "!", font=f, fill=accent)


def draw_bubble(draw, cx, cy, accent):
    draw.rounded_rectangle([cx - 50, cy - 40, cx + 50, cy + 30], radius=20, outline=accent, width=7)
    draw.polygon([(cx - 20, cy + 28), (cx - 40, cy + 52), (cx + 5, cy + 28)], fill=accent)


SYMBOL_FNS = {
    "dots": draw_dots, "gear": draw_gear, "check": draw_check,
    "star": draw_star, "cross": draw_cross, "qmark": draw_qmark,
    "lens": draw_lens, "bulb": draw_bulb, "triangle": draw_triangle,
    "bubble": draw_bubble,
}


def generate_all(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for name, bg, accent, sym, label, sub in EMOTIONS:
        img, draw = make_base(bg, accent)
        SYMBOL_FNS[sym](draw, 120, 95, accent)
        center_text(draw, 165, label, 32, accent, bold=True)
        center_text(draw, 200, sub, 24, (200, 200, 200), bold=False)
        path = os.path.join(output_dir, f"{name}.jpg")
        img.save(path, "JPEG", quality=90)
        print(f"  ✓ {name}.jpg")
    print(f"\nGenerated {len(EMOTIONS)} images in {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PixelMood emotion images")
    parser.add_argument("--output", default="/tmp/pixelmood", help="Output directory")
    args = parser.parse_args()
    generate_all(args.output)
