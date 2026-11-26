"""Render THE WORLD front page for Thursday 26 November 2026.

Architecture: a mosaic broadsheet. The page is declared as an ordered
list of story tiles, each carrying a weight; a row-packer lays the tiles
out in rows of equal height, then each tile draws itself from its own
geometry (kicker, headline, summary, glyph). Nothing here reads the
clock, the network, or any randomness source, so two runs write
byte-identical PNGs.

Run:  python3 render.py            (writes entry.png next to this file)
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (246, 241, 230)
INK = (20, 20, 20)
FAINT = (90, 84, 72)
RED = (164, 30, 34)
BLUE = (29, 78, 137)
RULE = (180, 172, 156)
CARD = (255, 253, 247)
BAND = (18, 18, 18)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)

F_MAST = font("DejaVuSerif-Bold.ttf", 84)
F_DATE = font("DejaVuSans-Bold.ttf", 21)
F_LEAD = font("DejaVuSerif-Bold.ttf", 40)
F_DECK = font("DejaVuSerif.ttf", 22)
F_KICK = font("DejaVuSans-Bold.ttf", 17)
F_HEAD = font("DejaVuSerif-Bold.ttf", 25)
F_BODY = font("DejaVuSans.ttf", 18)
F_RATE = font("DejaVuSerif-Bold.ttf", 40)
F_RATE_LBL = font("DejaVuSans-Bold.ttf", 16)
F_TICK = font("DejaVuSans-Bold.ttf", 18)
F_FOOT = font("DejaVuSans.ttf", 16)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_glyph(draw, kind, x, y, s, color):
    """Small geometric pictogram for a story tile, drawn from primitives."""
    if kind == "flame":
        draw.polygon([(x + s * 0.5, y), (x + s * 0.85, y + s * 0.45),
                      (x + s, y + s * 0.75), (x + s * 0.7, y + s),
                      (x + s * 0.3, y + s), (x, y + s * 0.75),
                      (x + s * 0.15, y + s * 0.45)], fill=color)
        draw.ellipse([x + s * 0.35, y + s * 0.55, x + s * 0.65, y + s * 0.85],
                     fill=PAPER)
    elif kind == "drop":
        draw.polygon([(x + s * 0.5, y), (x + s * 0.9, y + s * 0.55),
                      (x + s * 0.5, y + s), (x + s * 0.1, y + s * 0.55)],
                     fill=color)
        draw.ellipse([x + s * 0.3, y + s * 0.55, x + s * 0.7, y + s * 0.9],
                     fill=PAPER)
    elif kind == "chart":
        pts = [(x, y + s * 0.25), (x + s * 0.3, y + s * 0.35),
               (x + s * 0.55, y + s * 0.6), (x + s * 0.85, y + s * 0.9)]
        draw.line(pts, fill=color, width=5)
        draw.line([(x, y + s), (x + s, y + s)], fill=color, width=3)
        for px, py in pts:
            draw.ellipse([px - 4, py - 4, px + 4, py + 4], fill=color)
    elif kind == "target":
        draw.ellipse([x, y, x + s, y + s], outline=color, width=4)
        draw.ellipse([x + s * 0.28, y + s * 0.28, x + s * 0.72, y + s * 0.72],
                     outline=color, width=3)
        draw.ellipse([x + s * 0.42, y + s * 0.42, x + s * 0.58, y + s * 0.58],
                     fill=color)
    elif kind == "orbit":
        draw.ellipse([x, y + s * 0.15, x + s, y + s * 0.85], outline=color,
                     width=3)
        draw.ellipse([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62],
                     fill=color)
        draw.ellipse([x + s * 0.78, y + s * 0.05, x + s * 0.98, y + s * 0.25],
                     fill=color)
    elif kind == "sat":
        draw.rectangle([x + s * 0.35, y + s * 0.35, x + s * 0.65, y + s * 0.65],
                       fill=color)
        draw.rectangle([x, y + s * 0.42, x + s * 0.3, y + s * 0.58],
                       outline=color, width=3)
        draw.rectangle([x + s * 0.7, y + s * 0.42, x + s, y + s * 0.58],
                       outline=color, width=3)
        draw.line([x + s * 0.5, y + s * 0.35, x + s * 0.5, y + s * 0.1],
                  fill=color, width=3)


# ---------------------------------------------------------------- tiles
# Each tile: (weight, kicker, headline, summary, glyph, accent)
TILES = [
    (3, "DISASTER · CAIRO", "Tanker fire kills at least 31 in Cairo",
     "A fuel tanker overturned and caught fire on Cairo's ring road; "
     "31 dead, 21 hurt.", "flame", RED),
    (3, "CONFLICT · GULF", "Houthis hit Saudi ports and refinery",
     "Yemen's Houthis claimed strikes on Saudi oil sites; oil rose "
     "over 2%.", "drop", RED),
    (3, "MARKETS · NEW YORK", "Nasdaq nears bear market in AI rout",
     "US stocks fell again as AI-linked shares slid; the Nasdaq briefly "
     "neared 20% below its high.", "chart", BLUE),
    (2, "WAR · UKRAINE", "Kyiv hit as Ukraine strikes airbase",
     "Ukraine says it hit five jets at Savasleyka; Russia struck Kyiv "
     "with missiles.", "target", RED),
    (2, "SPACE · TIANGONG", "First Pakistani astronaut in orbit",
     "Zeeshan Ali reached Tiangong on Shenzhou-24, the first foreigner "
     "there.", "orbit", BLUE),
    (2, "TECH · WASHINGTON", "FCC clears a million SpaceX satellites",
     "The US regulator approved up to one million satellites for orbital "
     "data centres.", "sat", BLUE),
]

TICKER = ("IRAN: US tells citizens to leave  •  NETANYAHU: top charge may be dropped",
          "CHINA: Shanghai chief probed  •  SPAIN: snap vote Sunday  •  "
          "LIVERPOOL 3–0 CLUB BRUGGE")


def draw_tile(draw, tile, x, y, w, h):
    _, kicker, headline, summary, glyph, accent = tile
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    pad = 14
    gx, gy, gs = x + pad, y + pad + 2, 30
    draw_glyph(draw, glyph, gx, gy, gs, accent)
    draw.text((x + pad + gs + 12, y + pad + 4), kicker, font=F_KICK, fill=accent)
    hy = y + pad + 40
    for line in wrap(draw, headline, F_HEAD, w - 2 * pad)[:3]:
        draw.text((x + pad, hy), line, font=F_HEAD, fill=INK)
        hy += 29
    by = hy + 4
    for line in wrap(draw, summary, F_BODY, w - 2 * pad)[:3]:
        draw.text((x + pad, by), line, font=F_BODY, fill=FAINT)
        by += 22


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    m = 28  # page margin

    # ---- masthead
    d.text((W // 2, 4), "THE WORLD", font=F_MAST, fill=INK, anchor="ma")
    d.line([(m, 112), (W - m, 112)], fill=INK, width=3)
    d.line([(m, 118), (W - m, 118)], fill=INK, width=1)
    d.text((m, 126), "THURSDAY 26 NOVEMBER 2026", font=F_DATE, fill=INK)
    d.text((W - m, 126), "ONE DAY · ONE PAGE", font=F_DATE, fill=INK,
           anchor="ra")

    # ---- lead story
    ly = 152
    d.text((m, ly), "TRADE · WASHINGTON", font=F_KICK, fill=RED)
    head = "AMERICA PROPOSES TARIFFS ON 14 PARTNERS"
    hy = ly + 28
    for line in wrap(d, head, F_LEAD, 620):
        d.text((m, hy), line, font=F_LEAD, fill=INK)
        hy += 46
    deck = ("Trump proposed country-specific tariffs on 14 trading partners "
            "after an eight-month probe: India 25%, China and Vietnam 20%, "
            "Japan 15%. Nothing takes effect before a 25 January hearing.")
    dy = hy + 8
    for line in wrap(d, deck, F_DECK, 620)[:4]:
        d.text((m, dy), line, font=F_DECK, fill=FAINT)
        dy += 27

    # rate cards, right of the lead
    cards = [("INDIA", "25%"), ("CHINA", "20%"), ("VIETNAM", "20%"),
             ("JAPAN", "15%")]
    cx, cy = 668, ly + 28
    cw, ch, gap = 150, 104, 8
    for i, (label, rate) in enumerate(cards):
        bx = cx + (i % 2) * (cw + gap)
        by = cy + (i // 2) * (ch + gap)
        d.rectangle([bx, by, bx + cw, by + ch], fill=CARD, outline=RULE, width=1)
        d.rectangle([bx, by, bx + cw, by + 5], fill=RED)
        d.text((bx + cw // 2, by + 16), rate, font=F_RATE, fill=INK, anchor="ma")
        d.text((bx + cw // 2, by + 66), label, font=F_RATE_LBL, fill=FAINT,
               anchor="ma")

    d.line([(m, 412), (W - m, 412)], fill=INK, width=2)

    # ---- mosaic of story tiles: 3 columns x 2 rows, equal height
    grid_y, grid_h = 428, 490
    cols, rows = 3, 2
    cell_w = (W - 2 * m - 12) // cols
    cell_h = (grid_h - 2 * 12) // rows
    for i, tile in enumerate(TILES):
        tx = m + (i % cols) * (cell_w + 12)
        ty = grid_y + (i // cols) * (cell_h + 12)
        draw_tile(d, tile, tx, ty, cell_w, cell_h)

    # ---- ticker band
    ty = 926
    d.rectangle([0, ty, W, ty + 56], fill=BAND)
    yy = ty + 6
    for line in TICKER:
        d.text((m, yy), line, font=F_TICK, fill=(240, 236, 226))
        yy += 23

    # ---- footer
    d.text((W // 2, 992), "THE WORLD  ·  Thursday 26 November 2026  ·  "
           "Stories first reported on 26 November 2026",
           font=F_FOOT, fill=FAINT, anchor="ma")

    img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
