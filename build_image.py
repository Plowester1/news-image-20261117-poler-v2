#!/usr/bin/env python3
"""Build entry.png for news-image-20261117 (poler v2): a light, airy
sky-blue front page summing up Tuesday 17 November 2026 in eight stories.

Lead story: Japan scrambles jets — so the hero is aviation-themed, with a
big side-view jet drawn over a pale sky. All headlines/subheads are taken
verbatim from the verified story pool; only layout, colours and icons are
this variant's own. Pure PIL, no network, deterministic output.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SKY = (214, 233, 248)        # pale sky-blue page
SKY_DEEP = (183, 214, 240)   # slightly deeper sky for bands
MAST = (13, 52, 110)         # deep blue masthead
MAST_LINE = (255, 255, 255)
CARD = (255, 255, 255)       # white cards
CARD_EDGE = (163, 196, 224)  # card outline
INK = (18, 38, 66)           # headline ink
SUBINK = (74, 96, 124)       # subhead slate blue
ACCENT = (255, 176, 32)      # warm amber accent (date + hero stripe)
FOOTINK = (96, 122, 152)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

# (tag, tag colour, headline, subhead, icon key)
HERO = ("ASIA", (13, 52, 110),
        "Japan scrambles jets over Russian airspace",
        "Tokyo protests after two suspected Russian aircraft cross its skies.",
        "jet")

GRID = [
    ("ECONOMY", (8, 120, 96),
     "Japan's economy unexpectedly contracts",
     "Q3 shrinks an annualized 0.1%, surprising markets.",
     "chart"),
    ("MIDDLE EAST", (196, 58, 32),
     "US strikes Iran as tankers burn in Hormuz",
     "US jets hit missile sites after a fourth tanker struck a mine; Tehran warns of a \u2018huge price\u2019.",
     "flame"),
    ("EUROPE", (36, 96, 180),
     "Ukraine hits Crimean Bridge, Russia replies",
     "Kerch link closed after overnight strike; Moscow hits Kyiv bridges in reply.",
     "bridge"),
    ("TECH", (104, 52, 168),
     "US tightens AI chip export ban on China",
     "Commerce Dept closes a loophole on AI chips bought abroad; Nvidia rules out rehiring Huang.",
     "chip"),
]

BOTTOM = [
    ("DIPLOMACY", (16, 138, 90),
     "Trump meets Quad leaders in Manila",
     "US, Japan, India and Australia announce AI initiative and minerals pacts.",
     "quad"),
    ("FINANCE", (158, 110, 8),
     "Chase glitch delays bank transfers",
     "JPMorgan software bug slows transfers and Zelle; restored Monday evening.",
     "bank"),
    ("YEMEN", (148, 44, 96),
     "Houthi advance forces Yemen government retreat",
     "Government troops pull back from the Red Sea coast to defend Aden.",
     "flag"),
]


def fit_lines(draw, text, font, max_w):
    """Greedy word wrap to a pixel width."""
    out, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if draw.textlength(cand, font=font) <= max_w:
            cur = cand
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def pill(draw, x, y, label, colour, font):
    """Small rounded tag pill; returns its width."""
    w = int(draw.textlength(label, font=font)) + 20
    draw.rounded_rectangle([x, y, x + w, y + 26], radius=13, fill=colour)
    draw.text((x + 10, y + 4), label, font=font, fill=(255, 255, 255))
    return w


# ---- icons: simple flat PIL shapes, drawn fresh for this variant ----
def icon_jet_side(draw, cx, cy, s, colour):
    """Side-view jet flying right, with a dotted contrail."""
    for i, r in enumerate((3, 2, 2)):
        x = cx - s - 10 - i * 15
        draw.ellipse([x - r, cy - r, x + r, cy + r], fill=(140, 180, 215))
    # fuselage: pointed nose right, flat tail left
    draw.polygon([(cx + 0.95 * s, cy), (cx + 0.10 * s, cy - 0.20 * s),
                  (cx - 0.85 * s, cy - 0.14 * s), (cx - 0.85 * s, cy + 0.14 * s),
                  (cx + 0.10 * s, cy + 0.20 * s)], fill=colour)
    # main wing, swept down-back
    draw.polygon([(cx + 0.20 * s, cy + 0.10 * s), (cx - 0.30 * s, cy + 0.80 * s),
                  (cx - 0.05 * s, cy + 0.10 * s)], fill=colour)
    # tail fin on top, rear
    draw.polygon([(cx - 0.80 * s, cy - 0.10 * s), (cx - 0.62 * s, cy - 0.62 * s),
                  (cx - 0.45 * s, cy - 0.10 * s)], fill=colour)
    # cockpit window near the nose
    draw.ellipse([cx + 0.55 * s, cy - 0.14 * s, cx + 0.78 * s, cy - 0.02 * s],
                 fill=(255, 255, 255))


def icon_chart(draw, cx, cy, s, colour):
    bars = [0.45, 0.75, 0.55, 1.0]
    bw = 0.22 * s
    step = 0.5 * s
    for i, h in enumerate(bars):
        x0 = cx - s + i * step
        draw.rectangle([x0, cy + s - h * s, x0 + bw, cy + s], fill=colour)
    draw.line([cx - s, cy + s, cx + s, cy + s], fill=colour, width=3)


def icon_flame(draw, cx, cy, s, colour):
    pts = [(cx, cy - s), (cx + 0.55 * s, cy - 0.35 * s), (cx + 0.75 * s, cy + 0.30 * s),
           (cx + 0.40 * s, cy + 0.85 * s), (cx - 0.40 * s, cy + 0.85 * s),
           (cx - 0.75 * s, cy + 0.30 * s), (cx - 0.55 * s, cy - 0.35 * s)]
    draw.polygon(pts, fill=colour)
    draw.ellipse([cx - 0.22 * s, cy + 0.15 * s, cx + 0.22 * s, cy + 0.62 * s],
                 fill=(255, 214, 90))


def icon_bridge(draw, cx, cy, s, colour):
    draw.arc([cx - s, cy - 0.6 * s, cx + s, cy + 0.8 * s], 180, 360,
             fill=colour, width=5)
    draw.line([cx - s, cy + 0.55 * s, cx + s, cy + 0.55 * s], fill=colour, width=5)
    for fx in (-0.5, 0.0, 0.5):
        draw.line([cx + fx * s, cy + 0.05 * s, cx + fx * s, cy + 0.55 * s],
                  fill=colour, width=3)


def icon_chip(draw, cx, cy, s, colour):
    draw.rounded_rectangle([cx - 0.62 * s, cy - 0.62 * s, cx + 0.62 * s, cy + 0.62 * s],
                           radius=8, fill=colour)
    draw.rectangle([cx - 0.30 * s, cy - 0.30 * s, cx + 0.30 * s, cy + 0.30 * s],
                   outline=(255, 255, 255), width=3)
    for fx in (-0.35, 0.0, 0.35):
        draw.line([cx + fx * s, cy - 0.62 * s, cx + fx * s, cy - 0.95 * s],
                  fill=colour, width=4)
        draw.line([cx + fx * s, cy + 0.62 * s, cx + fx * s, cy + 0.95 * s],
                  fill=colour, width=4)
        draw.line([cx - 0.62 * s, cy + fx * s, cx - 0.95 * s, cy + fx * s],
                  fill=colour, width=4)
        draw.line([cx + 0.62 * s, cy + fx * s, cx + 0.95 * s, cy + fx * s],
                  fill=colour, width=4)


def icon_quad(draw, cx, cy, s, colour):
    cols = [(13, 52, 110), (16, 138, 90), (196, 58, 32), (255, 176, 32)]
    offs = [(-0.42, -0.42), (0.42, -0.42), (-0.42, 0.42), (0.42, 0.42)]
    r = 0.40 * s
    for (ox, oy), c in zip(offs, cols):
        draw.ellipse([cx + ox * s - r, cy + oy * s - r,
                      cx + ox * s + r, cy + oy * s + r], fill=c)


def icon_bank(draw, cx, cy, s, colour):
    draw.polygon([(cx - s, cy - 0.35 * s), (cx, cy - 0.85 * s),
                  (cx + s, cy - 0.35 * s)], fill=colour)
    draw.rectangle([cx - s, cy - 0.30 * s, cx + s, cy - 0.12 * s], fill=colour)
    for fx in (-0.62, -0.21, 0.21, 0.62):
        draw.rectangle([cx + fx * s - 0.10 * s, cy - 0.05 * s,
                        cx + fx * s + 0.10 * s, cy + 0.65 * s], fill=colour)
    draw.rectangle([cx - s, cy + 0.72 * s, cx + s, cy + 0.90 * s], fill=colour)


def icon_flag(draw, cx, cy, s, colour):
    draw.line([cx - 0.55 * s, cy - s, cx - 0.55 * s, cy + s], fill=(90, 70, 60),
              width=5)
    draw.polygon([(cx - 0.55 * s, cy - s), (cx + 0.75 * s, cy - 0.72 * s),
                  (cx - 0.55 * s, cy - 0.38 * s)], fill=colour)
    draw.line([cx - 0.55 * s, cy + s, cx + 0.55 * s, cy + s], fill=(90, 70, 60),
              width=5)


ICONS = {"jet": icon_jet_side, "chart": icon_chart, "flame": icon_flame,
         "bridge": icon_bridge, "chip": icon_chip, "quad": icon_quad,
         "bank": icon_bank, "flag": icon_flag}


def card(draw, x0, y0, x1, y1, accent):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=CARD,
                           outline=CARD_EDGE, width=2)
    draw.rounded_rectangle([x0, y0, x0 + 8, y1], radius=4, fill=accent)


def main():
    img = Image.new("RGB", (W, H), SKY)
    d = ImageDraw.Draw(img)

    # ---- masthead: deep blue band, white serif title, amber date ----
    d.rectangle([0, 0, W, 128], fill=MAST)
    d.rectangle([0, 128, W, 132], fill=ACCENT)
    f_mast = ImageFont.truetype(SERIF, 58)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_mast)) / 2, 20), title,
           font=f_mast, fill=MAST_LINE)
    f_date = ImageFont.truetype(BOLD, 22)
    date = "TUESDAY, 17 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 92), date,
           font=f_date, fill=ACCENT)

    f_tag = ImageFont.truetype(BOLD, 17)
    m = 32
    full = W - 2 * m  # 960

    # ---- hero: Japan jets, aviation accent, big side-view jet ----
    hx0, hy0, hh = m, 146, 204
    card(d, hx0, hy0, hx0 + full, hy0 + hh, HERO[1])
    # pale sky panel behind the jet on the right
    d.rounded_rectangle([hx0 + full - 300, hy0 + 8, hx0 + full - 8, hy0 + hh - 8],
                        radius=10, fill=SKY)
    icon_jet_side(d, hx0 + full - 158, hy0 + hh // 2 - 6, 80, (13, 52, 110))
    d.line([hx0 + full - 292, hy0 + hh - 34, hx0 + full - 40, hy0 + hh - 34],
           fill=(255, 255, 255), width=3)
    px, py = hx0 + 26, hy0 + 20
    pill(d, px, py, HERO[0], HERO[1], f_tag)
    py += 40
    f_hero = ImageFont.truetype(BOLD, 37)
    f_hero_sub = ImageFont.truetype(REG, 21)
    tw = full - 52 - 300
    for line in fit_lines(d, HERO[2], f_hero, tw)[:2]:
        d.text((px, py), line, font=f_hero, fill=INK)
        py += 45
    py += 6
    for line in fit_lines(d, HERO[3], f_hero_sub, tw)[:2]:
        d.text((px, py), line, font=f_hero_sub, fill=SUBINK)
        py += 28

    # ---- 2x2 grid: economy, Iran, Ukraine, chip ban ----
    cw = (full - 16) // 2  # 472
    ch = 188
    f_head = ImageFont.truetype(BOLD, 26)
    f_sub = ImageFont.truetype(REG, 18)
    for i, (tag, colour, head, sub, icon) in enumerate(GRID):
        col, row = i % 2, i // 2
        x0 = m + col * (cw + 16)
        y0 = 360 + row * (ch + 14)
        card(d, x0, y0, x0 + cw, y0 + ch, colour)
        ICONS[icon](d, x0 + cw - 48, y0 + 48, 30, colour)
        px, py = x0 + 24, y0 + 14
        pill(d, px, py, tag, colour, f_tag)
        py += 38
        tw = cw - 48 - 62
        for line in fit_lines(d, head, f_head, tw)[:2]:
            d.text((px, py), line, font=f_head, fill=INK)
            py += 30
        py += 4
        for line in fit_lines(d, sub, f_sub, tw)[:3]:
            d.text((px, py), line, font=f_sub, fill=SUBINK)
            py += 22

    # ---- bottom row: Quad, Chase, Houthis (three cards) ----
    bw = 309
    f_bhead = ImageFont.truetype(BOLD, 21)
    f_bsub = ImageFont.truetype(REG, 15)
    for i, (tag, colour, head, sub, icon) in enumerate(BOTTOM):
        x0 = m + i * (bw + 16)
        y0 = 764
        bh = 190
        card(d, x0, y0, x0 + bw, y0 + bh, colour)
        ICONS[icon](d, x0 + bw - 40, y0 + 44, 22, colour)
        px, py = x0 + 22, y0 + 14
        pill(d, px, py, tag, colour, f_tag)
        py += 36
        tw = bw - 44 - 52
        for line in fit_lines(d, head, f_bhead, tw)[:3]:
            d.text((px, py), line, font=f_bhead, fill=INK)
            py += 25
        py += 3
        for line in fit_lines(d, sub, f_bsub, tw)[:3]:
            d.text((px, py), line, font=f_bsub, fill=SUBINK)
            py += 19

    # ---- footer ----
    f_foot = ImageFont.truetype(REG, 16)
    foot = "17 November 2026  \u2022  World news at a glance  \u2022  Japan  \u2022  Iran  \u2022  Ukraine  \u2022  China chips  \u2022  Quad  \u2022  Chase  \u2022  Yemen"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 972), foot,
           font=f_foot, fill=FOOTINK)

    img.save("entry.png", "PNG", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
