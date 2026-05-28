#!/usr/bin/env python3
"""Stitch front + back-with-qr into one side-by-side preview for visual review."""
from PIL import Image
from pathlib import Path

HERE  = Path(__file__).parent
FRONT = HERE / "mhp-doorhanger-front.png"
BACK  = HERE / "mhp-doorhanger-back.png"
OUT   = HERE / "mhp-doorhanger-preview.png"

GAP = 40
BG  = (230, 232, 238)

front = Image.open(FRONT).convert("RGB")
back  = Image.open(BACK).convert("RGB")

# Match heights — back was extended for the QR strip, so it's taller
target_h = max(front.height, back.height)
def pad_to(img, h):
    if img.height == h: return img
    new = Image.new("RGB", (img.width, h), BG)
    new.paste(img, (0, (h - img.height) // 2))
    return new
front_p = pad_to(front, target_h)
back_p  = pad_to(back,  target_h)

total_w = front_p.width + back_p.width + GAP * 3
canvas = Image.new("RGB", (total_w, target_h + GAP * 2), BG)
canvas.paste(front_p, (GAP,                              GAP))
canvas.paste(back_p,  (GAP * 2 + front_p.width,          GAP))

canvas.save(OUT, "PNG", optimize=True)
print(f"Wrote {OUT}  ({canvas.size[0]}x{canvas.size[1]}, {OUT.stat().st_size // 1024} KB)")
