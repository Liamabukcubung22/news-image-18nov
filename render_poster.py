#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news poster (1024x1024 PNG).

Flat vector-style poster: a header naming the day, then eight story cards,
each with a short accurate headline, one factual sub-line and a small drawn
icon. No photos, no copied artwork. Rendered with PIL only.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/noto/"

NAVY = (20, 33, 61)
GOLD = (232, 181, 77)
PAPER = (247, 243, 234)
CARD = (255, 255, 255)
BORDER = (216, 210, 196)
INK = (24, 24, 24)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)

# (tag, colour, headline, sub-line, icon key)
STORIES = [
    ("GULF", (178, 34, 34), "Iran strikes Kuwait and Bahrain",
     "After U.S. jets hit a missile site on Qeshm Island", "drone"),
    ("UKRAINE", (31, 73, 125), "Kerch Bridge arch collapses",
     "Ukrainian strikes drop the road span into the strait", "bridge"),
    ("ASIA", (0, 128, 128), "Xi and Putin meet in Shenzhen",
     "APEC talks set up Thursday's summit with Trump", "flags"),
    ("USA", (43, 63, 120), "Democrats take the Senate 56-44",
     "Peltola wins Alaska, the last race decided", "capitol"),
    ("HEALTH", (122, 54, 138), "U.S. loses measles-free status",
     "5,412 cases in 2026, the most since 1991", "virus"),
    ("AFRICA", (34, 139, 92), "Ebola in Congo passes 11,000 cases",
     "Children under five hit hardest in the outbreak", "cross"),
    ("SPACE", (63, 50, 140), "Voyager 1 reaches one light-day",
     "Farthest human-made object, 16 billion miles out", "satellite"),
    ("TECH", (196, 102, 20), "Nvidia revenue doubles to $115.8B",
     "Board rules out bringing back Jensen Huang", "chip"),
]


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(draw, text, name, size, max_w, max_lines):
    """Largest font size (down to 18) letting text fit in max_lines lines."""
    while size > 18:
        fnt = font(name, size)
        if len(wrap(draw, text, fnt, max_w)) <= max_lines:
            return fnt
        size -= 1
    return font(name, 18)


def draw_icon(d, key, cx, cy, colour):
    """Simple flat icon in white on a coloured disc centred at (cx, cy)."""
    r = 38
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=colour)
    w = WHITE
    if key == "drone":  # quadcopter drone
        d.rectangle([cx - 16, cy - 7, cx + 16, cy + 7], fill=w)
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=colour)
        for sx, sy in ((-24, -16), (24, -16), (-24, 16), (24, 16)):
            d.line([cx + sx * 0.6, cy + sy * 0.6, cx + sx, cy + sy], fill=w, width=4)
            d.ellipse([cx + sx - 9, cy + sy - 4, cx + sx + 9, cy + sy + 4], fill=w)
    elif key == "bridge":  # broken bridge over water
        d.arc([cx - 28, cy - 26, cx + 28, cy + 14], 180, 360, fill=w, width=5)
        d.line([cx - 30, cy - 2, cx - 8, cy - 2], fill=w, width=5)
        d.line([cx + 8, cy - 2, cx + 30, cy - 2], fill=w, width=5)
        d.line([cx - 6, cy - 2, cx - 2, cy + 10], fill=w, width=4)
        d.line([cx + 2, cy + 10, cx + 6, cy - 2], fill=w, width=4)
        for yy in (16, 24):
            d.line([cx - 28, cy + yy, cx + 28, cy + yy], fill=w, width=3)
    elif key == "flags":  # two summit flags
        d.line([cx - 14, cy - 26, cx - 14, cy + 26], fill=w, width=4)
        d.line([cx + 14, cy - 26, cx + 14, cy + 26], fill=w, width=4)
        d.polygon([(cx - 14, cy - 26), (cx + 8, cy - 20), (cx - 14, cy - 14)], fill=(214, 48, 49))
        d.polygon([(cx + 14, cy - 26), (cx + 36, cy - 20), (cx + 14, cy - 14)], fill=(255, 255, 255))
        d.polygon([(cx - 14, cy - 26), (cx + 8, cy - 20), (cx - 14, cy - 14)],
                  outline=(255, 255, 255))
    elif key == "capitol":  # domed capitol building
        d.pieslice([cx - 14, cy - 24, cx + 14, cy + 2], 180, 360, fill=w)
        d.rectangle([cx - 20, cy + 2, cx + 20, cy + 8], fill=w)
        for x in (-16, -6, 4, 14):
            d.rectangle([cx + x, cy + 8, cx + x + 4, cy + 24], fill=w)
        d.rectangle([cx - 26, cy + 24, cx + 26, cy + 28], fill=w)
    elif key == "virus":  # virus with spikes
        for ang in range(0, 360, 45):
            import math
            a = math.radians(ang)
            x1, y1 = cx + 16 * math.cos(a), cy + 16 * math.sin(a)
            x2, y2 = cx + 26 * math.cos(a), cy + 26 * math.sin(a)
            d.line([x1, y1, x2, y2], fill=w, width=4)
            d.ellipse([x2 - 3, y2 - 3, x2 + 3, y2 + 3], fill=w)
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=w)
        d.ellipse([cx - 6, cy - 8, cx + 0, cy - 2], fill=colour)
        d.ellipse([cx + 2, cy + 2, cx + 8, cy + 8], fill=colour)
    elif key == "cross":  # medical cross
        d.rectangle([cx - 8, cy - 22, cx + 8, cy + 22], fill=w)
        d.rectangle([cx - 22, cy - 8, cx + 22, cy + 8], fill=w)
    elif key == "satellite":  # satellite with panels
        d.rectangle([cx - 26, cy - 5, cx - 8, cy + 5], fill=w)
        d.rectangle([cx + 8, cy - 5, cx + 26, cy + 5], fill=w)
        d.polygon([(cx - 8, cy - 10), (cx + 8, cy - 10), (cx + 5, cy + 10),
                   (cx - 5, cy + 10)], fill=w)
        d.line([cx + 4, cy - 14, cx + 16, cy - 26], fill=w, width=4)
        d.ellipse([cx + 12, cy - 30, cx + 20, cy - 22], fill=w)
    elif key == "chip":  # microchip
        d.rectangle([cx - 14, cy - 14, cx + 14, cy + 14], fill=w)
        d.rectangle([cx - 6, cy - 6, cx + 6, cy + 6], fill=colour)
        for x in (-10, 0, 10):
            d.line([cx + x, cy - 24, cx + x, cy - 14], fill=w, width=4)
            d.line([cx + x, cy + 14, cx + x, cy + 24], fill=w, width=4)
        for y in (-10, 0, 10):
            d.line([cx - 24, cy + y, cx - 14, cy + y], fill=w, width=4)
            d.line([cx + 14, cy + y, cx + 24, cy + y], fill=w, width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- header ----
    d.rectangle([0, 0, W, 160], fill=NAVY)
    d.rectangle([0, 160, W, 166], fill=GOLD)
    d.text((48, 18), "T H E   W O R L D   I N   O N E   D A Y",
           font=font("NotoSans-Bold.ttf", 26), fill=GOLD)
    d.text((48, 50), "Wednesday, 18 November 2026",
           font=font("NotoSans-Bold.ttf", 56), fill=WHITE)
    d.text((48, 118), "Eight stories that defined the day",
           font=font("NotoSans-Regular.ttf", 26), fill=(200, 205, 220))

    # ---- story grid: 2 columns x 4 rows ----
    margin, gap = 24, 14
    cw = (W - 2 * margin - gap) // 2
    ch = 190
    top = 182
    for i, (tag, colour, head, sub, icon) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x0 = margin + col * (cw + gap)
        y0 = top + row * (ch + gap)
        d.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], radius=14,
                            fill=CARD, outline=BORDER, width=2)
        draw_icon(d, icon, x0 + 56, y0 + 52, colour)
        tx = x0 + 108
        tw = cw - 108 - 18
        d.text((tx, y0 + 16), tag, font=font("NotoSans-Bold.ttf", 19), fill=colour)
        hf = fit_font(d, head, "NotoSans-Bold.ttf", 28, tw, 2)
        lines = wrap(d, head, hf, tw)
        y = y0 + 44
        for line in lines:
            d.text((tx, y), line, font=hf, fill=INK)
            y += hf.size + 4
        sf = fit_font(d, sub, "NotoSans-Regular.ttf", 21, cw - 36, 2)
        slines = wrap(d, sub, sf, cw - 36)
        y = y0 + 118
        for line in slines:
            d.text((x0 + 18, y), line, font=sf, fill=GREY)
            y += sf.size + 4

    # ---- footer ----
    d.text((W // 2, 990), "Sources: Reuters, AP, BBC, NASA, PAHO  |  18 November 2026",
           font=font("NotoSans-Regular.ttf", 18), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
