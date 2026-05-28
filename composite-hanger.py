#!/usr/bin/env python3
"""
Composite the QR code onto the back of the MHP door hanger.

Source: /Users/jameswalton/Downloads/mhp.doorhanger.back.PNG  (524 x 1536)
QR:     ./doorhanger.png
Output: ./mhp-doorhanger-back-with-qr.png

Run from this folder:  python3 composite-hanger.py
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import sys

HERE = Path(__file__).parent
SRC_BACK = Path("/Users/jameswalton/Downloads/mhp.doorhanger.back.PNG")
SRC_QR   = HERE / "doorhanger.png"
OUT      = HERE / "mhp-doorhanger-back-with-qr.png"

# --- Layout (pixels in the 524x1536 source) ---
EXTEND_PX       = 150        # add this much navy strip at the bottom for the QR
QR_SIZE         = 110
QR_PAD          = 6
HEADLINE_TEXT   = "SCAN FOR A FREE ESTIMATE"
SUBLINE_TEXT    = "1-business-day callback"
TEXT_COLOR      = (255, 255, 255)
BAND_NAVY_SAMPLE_Y_OFFSET = 30   # sample existing band color this far up from bottom

def main():
    if not SRC_BACK.exists():
        print(f"ERROR: source missing: {SRC_BACK}", file=sys.stderr); sys.exit(1)
    if not SRC_QR.exists():
        print(f"ERROR: QR missing: {SRC_QR}. Run generate-qr.js first.", file=sys.stderr); sys.exit(1)

    back = Image.open(SRC_BACK).convert("RGBA")
    qr   = Image.open(SRC_QR).convert("RGBA")
    W, H = back.size
    print(f"Back canvas: {W}x{H}")

    # Sample the existing footer navy so the extension matches exactly
    px = back.load()
    sample = px[W // 2, H - BAND_NAVY_SAMPLE_Y_OFFSET]
    navy = sample[:3]
    print(f"Sampled footer navy: {navy}")

    # New canvas with bottom extension in matching navy
    new_h = H + EXTEND_PX
    new_canvas = Image.new("RGBA", (W, new_h), navy + (255,))
    new_canvas.paste(back, (0, 0), back)

    # Build the white-padded QR (no extra border — the navy strip is the frame)
    qr_resized = qr.resize((QR_SIZE, QR_SIZE), Image.LANCZOS)
    badge_w = QR_SIZE + 2 * QR_PAD
    badge_h = badge_w
    badge = Image.new("RGBA", (badge_w, badge_h), (255, 255, 255, 255))
    badge.paste(qr_resized, (QR_PAD, QR_PAD), qr_resized)

    # Position: QR on the left of the new strip, vertically centered
    strip_top = H
    strip_mid = strip_top + EXTEND_PX // 2
    bx = 22
    by = strip_mid - badge_h // 2
    new_canvas.paste(badge, (bx, by), badge)

    # Text on the right of the QR
    try:
        head_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
        sub_font  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 12)
    except Exception:
        head_font = ImageFont.load_default()
        sub_font  = ImageFont.load_default()

    draw = ImageDraw.Draw(new_canvas)
    text_x = bx + badge_w + 18
    # vertical block: headline + 4px gap + subline, centered in strip
    hb = head_font.getbbox(HEADLINE_TEXT)
    sb = sub_font.getbbox(SUBLINE_TEXT)
    head_h = hb[3] - hb[1]
    sub_h  = sb[3] - sb[1]
    block_h = head_h + 6 + sub_h
    text_top = strip_mid - block_h // 2 - hb[1]
    draw.text((text_x, text_top), HEADLINE_TEXT, fill=TEXT_COLOR, font=head_font)
    draw.text((text_x, text_top + head_h + 6 - sb[1] + hb[1]), SUBLINE_TEXT,
              fill=(220, 230, 245), font=sub_font)

    new_canvas.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}  ({new_canvas.size[0]}x{new_canvas.size[1]}, {OUT.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
