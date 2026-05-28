#!/usr/bin/env python3
"""
Composite the QR onto the FRONT of the MHP door hanger.

Reference: /Users/jameswalton/Downloads/mhp.doorhanger.qr.png
Source:    /Users/jameswalton/Downloads/mhp.doorhanger.front.PNG  (528 x 1537)
QR:        ./doorhanger.png  (already encodes the GH Pages URL)
Output:    ./mhp-doorhanger-front-with-qr.png

Layout: extend canvas downward with a white area, drop a navy-framed QR
badge centered in it.

Run:  python3 composite-front.py
"""
from PIL import Image, ImageDraw
from pathlib import Path
import sys

HERE     = Path(__file__).parent
SRC_FRONT = Path("/Users/jameswalton/Downloads/mhp.doorhanger.front.PNG")
SRC_QR    = HERE / "doorhanger.png"
OUT       = HERE / "mhp-doorhanger-front.png"

# --- Layout (pixels in the 528-wide source) ---
EXTEND_PX        = 290        # white area added at the bottom
QR_SIZE          = 220        # actual QR pixels
QR_WHITE_PAD     = 14         # white quiet zone outside the QR
QR_FRAME         = 4          # navy frame around the white pad
BRAND_NAVY       = (0, 81, 184)
WHITE            = (255, 255, 255)
BADGE_TOP_MARGIN = 24         # gap between top of the white extension and the badge

def main():
    if not SRC_FRONT.exists():
        print(f"ERROR: missing {SRC_FRONT}", file=sys.stderr); sys.exit(1)
    if not SRC_QR.exists():
        print(f"ERROR: missing {SRC_QR}. Run generate-qr.js first.", file=sys.stderr); sys.exit(1)

    front = Image.open(SRC_FRONT).convert("RGBA")
    qr    = Image.open(SRC_QR).convert("RGBA")
    W, H  = front.size
    print(f"Front canvas: {W}x{H}")

    # New canvas: original front + white extension
    new_h  = H + EXTEND_PX
    canvas = Image.new("RGBA", (W, new_h), WHITE + (255,))
    canvas.paste(front, (0, 0), front)

    # Build the badge: navy frame → white pad → QR
    qr_resized = qr.resize((QR_SIZE, QR_SIZE), Image.LANCZOS)
    badge_w = QR_SIZE + 2 * (QR_WHITE_PAD + QR_FRAME)
    badge_h = badge_w
    badge = Image.new("RGBA", (badge_w, badge_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(badge)
    d.rectangle([0, 0, badge_w - 1, badge_h - 1], fill=BRAND_NAVY)
    d.rectangle(
        [QR_FRAME, QR_FRAME, badge_w - 1 - QR_FRAME, badge_h - 1 - QR_FRAME],
        fill=WHITE,
    )
    badge.paste(qr_resized, (QR_FRAME + QR_WHITE_PAD, QR_FRAME + QR_WHITE_PAD), qr_resized)

    # Center horizontally; position with some margin in the new white area
    bx = (W - badge_w) // 2
    by = H + BADGE_TOP_MARGIN
    canvas.paste(badge, (bx, by), badge)

    canvas.convert("RGB").save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT}  ({canvas.size[0]}x{canvas.size[1]}, {OUT.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    main()
