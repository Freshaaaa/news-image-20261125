#!/usr/bin/env python3
"""Build the news-image-20261125 poster: THE WORLD, Wednesday 25 November 2026.

One-page newspaper poster, 1024x1024. 50 stories, 8 regions, 18 fields,
6 drawn scenes, a 5-ship timeline, a numbers strip and a footer that fits
inside the page. Rendered with Pillow only; no network, no outside files.
"""

import datetime
import textwrap

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 24
PAPER = (250, 246, 236)
INK = (17, 17, 17)
RULE = (17, 17, 17)
MUTED = (90, 86, 76)
ACCENT = (158, 27, 27)

REGIONS = {
    "EUROPE": (31, 68, 140),
    "ASIA": (158, 27, 27),
    "M. EAST": (27, 110, 68),
    "AFRICA": (176, 92, 8),
    "AMERICAS": (104, 52, 150),
    "TECH": (12, 110, 118),
    "CLIMATE": (46, 110, 46),
    "WORLD": (70, 70, 70),
}

FIELDS = [
    "War", "Diplomacy", "Energy", "Trade", "Tariffs", "Climate",
    "Health", "Tech", "Space", "Markets", "Justice", "Migration",
    "Culture", "Sport", "Science", "Aid", "Security", "Media",
]

NUMBERS = [
    ("720,000", "Russian dead"),
    ("5", "ships hit"),
    ("12", "days of attacks"),
    ("88/112", "drones downed"),
    ("168", "dead in Hong Kong blaze"),
    ("31", "dead in Cairo collapse"),
]

# (region, headline) -- 8 regions, 50 stories.
STORIES = [
    ("EUROPE", "720,000 Russian dead, Kyiv says toll climbs"),
    ("EUROPE", "88 of 112 drones downed in overnight barrage"),
    ("EUROPE", "Nuclear threat raised as plant shelling resumes"),
    ("EUROPE", "EU agrees new sanctions package on oil"),
    ("EUROPE", "NATO ministers meet on air defence gaps"),
    ("EUROPE", "Black Sea corridor reopens after strikes"),
    ("EUROPE", "Poland scrambles jets as drones near border"),
    ("EUROPE", "Grain exports delayed at Black Sea ports"),
    ("ASIA", "168 dead in Hong Kong tower blaze"),
    ("ASIA", "Hong Kong fire inquiry opens, cladding checked"),
    ("ASIA", "Taiwan watches drills across the strait"),
    ("ASIA", "Japan unveils defence budget increase"),
    ("ASIA", "India monsoon aid reaches flood districts"),
    ("ASIA", "South Korea chip exports rise again"),
    ("ASIA", "Earthquake rattles Pacific island nation"),
    ("M. EAST", "31 dead in Cairo building collapse"),
    ("M. EAST", "Gaza ceasefire talks resume in Cairo"),
    ("M. EAST", "Oil steadies as Gulf output held flat"),
    ("M. EAST", "Lebanon border calm holds for third day"),
    ("M. EAST", "Syria aid convoys cross after delay"),
    ("M. EAST", "Refugee arrivals rise on Mediterranean route"),
    ("AFRICA", "Sudan aid corridors open amid fighting"),
    ("AFRICA", "Kenya rains displace thousands"),
    ("AFRICA", "Nigeria power grid restored after outage"),
    ("AFRICA", "South Africa summit on jobs and growth"),
    ("AFRICA", "Morocco solar plant powers desert towns"),
    ("AFRICA", "Ethiopia harvest hopes rise after rains"),
    ("AMERICAS", "US imposes 25% tariffs on new goods list"),
    ("AMERICAS", "Tariff row deepens as partners retaliate"),
    ("AMERICAS", "Mexico border crossings fall sharply"),
    ("AMERICAS", "Brazil rainforest pact signed at COP31"),
    ("AMERICAS", "Canada wildfire season ends early"),
    ("AMERICAS", "Argentina inflation eases for third month"),
    ("AMERICAS", "Chile copper output climbs to record"),
    ("TECH", "AI chip demand lifts markets to record"),
    ("TECH", "Space rocket test flight ends in splashdown"),
    ("TECH", "Cyber attack hits hospitals, systems back"),
    ("TECH", "Quantum computer passes key benchmark"),
    ("TECH", "Electric car sales pass petrol in Europe"),
    ("TECH", "Undersea cable repaired after outage"),
    ("CLIMATE", "COP31 opens with finance fight unresolved"),
    ("CLIMATE", "COP31 draft urges faster coal exit"),
    ("CLIMATE", "Antarctic ice loss accelerates, study says"),
    ("CLIMATE", "Cyclone outlook raised for the Pacific"),
    ("CLIMATE", "Cold snap grips northern Europe"),
    ("WORLD", "UN warns hunger rising in conflict zones"),
    ("WORLD", "WHO tracks new flu variant closely"),
    ("WORLD", "Five ships hit in 12 days, insurers warn"),
    ("WORLD", "Shipping rates jump on Black Sea risk"),
    ("WORLD", "Nobel season ends with peace prize debate"),
]

SCENES = [
    ("BLACK SEA", "ship under escort"),
    ("KYIV NIGHT", "drones downed"),
    ("HONG KONG", "tower blaze"),
    ("CAIRO", "rescue at collapse site"),
    ("COP31 HALL", "summit in session"),
    ("PORT TARIFFS", "containers held"),
]

TIMELINE = [
    ("Day 1", "Ship 1 hit"),
    ("Day 4", "Ship 2 hit"),
    ("Day 7", "Ship 3 hit"),
    ("Day 10", "Ship 4 hit"),
    ("Day 12", "Ship 5 hit"),
]


def load_font(bold, size):
    """Best-effort DejaVu load, plain default font as fallback."""
    names = ("DejaVuSans-Bold.ttf", "DejaVuSans.ttf") if bold else ("DejaVuSans.ttf",)
    for name in names:
        path = "/usr/share/fonts/truetype/dejavu/" + name
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(draw, text, font, width):
    """Greedy word wrap measured with the real font."""
    words, lines, current = text.split(), [], ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_center(draw, y, text, font, fill=INK):
    draw_center_at(draw, W // 2, y, text, font, fill)


def draw_center_at(draw, cx, y, text, font, fill=INK):
    draw.text((cx, y), text, font=font, fill=fill, anchor="ma")


def draw_scene(draw, box, kind):
    """One small flat illustration inside box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = box
    if kind == 0:  # Black Sea: sky, sea, ship, escort dot
        draw.rectangle([x0, y0, x1, y0 + 34], fill=(178, 205, 225))
        draw.rectangle([x0, y0 + 34, x1, y1], fill=(38, 84, 128))
        draw.rectangle([x0 + 28, y0 + 44, x0 + 108, y0 + 56], fill=(20, 20, 20))
        draw.rectangle([x0 + 52, y0 + 32, x0 + 66, y0 + 44], fill=(20, 20, 20))
        draw.line([x0 + 59, y0 + 20, x0 + 59, y0 + 32], fill=(20, 20, 20), width=2)
        for wx in (14, 48, 88, 122):
            draw.arc([x0 + wx, y0 + 58, x0 + wx + 22, y0 + 70],
                     0, 180, fill=(220, 230, 238), width=2)
        draw.ellipse([x0 + 128, y0 + 40, x0 + 136, y0 + 48], fill=(158, 27, 27))
    elif kind == 1:  # Kyiv night: dark sky, stars, drone dots, burst
        draw.rectangle(box, fill=(16, 22, 44))
        for sx, sy in [(18, 12), (52, 26), (96, 10), (128, 30), (40, 44), (112, 48)]:
            draw.ellipse([x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3],
                         fill=(240, 230, 180))
        for dx, dy in [(30, 58), (70, 52), (108, 62)]:
            draw.ellipse([x0 + dx, y0 + dy, x0 + dx + 5, y0 + dy + 5],
                         fill=(220, 220, 220))
        draw.line([x0 + 70, y0 + 40, x0 + 70, y0 + 52], fill=(255, 200, 60), width=2)
        draw.line([x0 + 60, y0 + 46, x0 + 80, y0 + 46], fill=(255, 200, 60), width=2)
        draw.polygon([(x0 + 8, y1), (x0 + 40, y0 + 62), (x0 + 72, y1)],
                     fill=(30, 34, 52))
        draw.polygon([(x0 + 84, y1), (x0 + 112, y0 + 66), (x0 + 140, y1)],
                     fill=(30, 34, 52))
    elif kind == 2:  # Hong Kong: tower, flame, smoke
        draw.rectangle([x0, y0, x1, y1], fill=(214, 196, 168))
        draw.rectangle([x0 + 48, y0 + 18, x0 + 100, y1], fill=(52, 52, 58))
        for wy in range(y0 + 26, y1 - 6, 12):
            for wx in (56, 72, 88):
                draw.rectangle([x0 + wx, wy, x0 + wx + 7, wy + 6],
                               fill=(255, 196, 66))
        draw.polygon([(x0 + 74, y0 + 4), (x0 + 62, y0 + 26), (x0 + 86, y0 + 26)],
                     fill=(220, 80, 20))
        draw.ellipse([x0 + 104, y0 + 6, x0 + 122, y0 + 22], fill=(120, 120, 120))
        draw.ellipse([x0 + 116, y0 + 16, x0 + 138, y0 + 34], fill=(150, 150, 150))
    elif kind == 3:  # Cairo: standing block, tilted block, rescue cross
        draw.rectangle([x0, y0, x1, y1], fill=(226, 208, 176))
        draw.rectangle([x0 + 16, y0 + 30, x0 + 66, y1], fill=(140, 110, 78))
        draw.polygon([(x0 + 76, y0 + 52), (x0 + 128, y0 + 40),
                      (x0 + 140, y0 + 78), (x0 + 88, y0 + 88)],
                     fill=(110, 86, 60))
        draw.rectangle([x0 + 96, y0 + 66, x0 + 128, y0 + 80], fill=(255, 255, 255))
        draw.rectangle([x0 + 109, y0 + 69, x0 + 115, y0 + 77], fill=(200, 30, 30))
        draw.rectangle([x0 + 106, y0 + 72, x0 + 118, y0 + 74], fill=(200, 30, 30))
    elif kind == 4:  # COP31 hall: podium, seats, flags
        draw.rectangle([x0, y0, x1, y1], fill=(196, 214, 196))
        draw.rectangle([x0 + 52, y0 + 22, x0 + 98, y0 + 44], fill=(90, 60, 30))
        for fx, fc in [(24, (31, 68, 140)), (118, (27, 110, 68)), (132, (158, 27, 27))]:
            draw.line([x0 + fx, y0 + 10, x0 + fx, y0 + 34], fill=(40, 40, 40), width=2)
            draw.polygon([(x0 + fx, y0 + 10), (x0 + fx + 14, y0 + 15),
                          (x0 + fx, y0 + 20)], fill=fc)
        for rx in range(14, 140, 22):
            draw.rectangle([x0 + rx, y0 + 56, x0 + rx + 16, y0 + 68],
                           fill=(70, 70, 70))
    else:  # Port tariffs: stacked containers, crane
        draw.rectangle([x0, y0, x1, y1], fill=(205, 216, 226))
        draw.rectangle([x0 + 16, y0 + 52, x0 + 66, y0 + 70], fill=(158, 27, 27))
        draw.rectangle([x0 + 70, y0 + 52, x0 + 120, y0 + 70], fill=(31, 68, 140))
        draw.rectangle([x0 + 42, y0 + 32, x0 + 92, y0 + 50], fill=(176, 92, 8))
        draw.line([x0 + 20, y0 + 14, x0 + 132, y0 + 14], fill=(40, 40, 40), width=3)
        draw.line([x0 + 24, y0 + 14, x0 + 24, y0 + 52], fill=(40, 40, 40), width=2)
        draw.line([x0 + 128, y0 + 14, x0 + 128, y0 + 52], fill=(40, 40, 40), width=2)


def build():
    # Date check: the poster is dated Wednesday 25 November 2026.
    day = datetime.date(2026, 11, 25)
    assert day.strftime("%A") == "Wednesday", "date check failed"
    assert len(STORIES) == 50, "must be exactly 50 stories"
    assert len(set(region for region, _ in STORIES)) == 8, "must be 8 regions"
    assert len(FIELDS) == 18, "must be 18 fields"
    assert len(SCENES) == 6, "must be 6 scenes"
    assert len(TIMELINE) == 5, "must be 5 ships"
    assert len(NUMBERS) == 6, "must be 6 numbers"

    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    inner = W - 2 * MARGIN

    f_mast = load_font(True, 66)
    f_date = load_font(False, 16)
    f_fields = load_font(False, 13)
    f_lead = load_font(True, 29)
    f_num = load_font(True, 34)
    f_numlabel = load_font(False, 12)
    f_section = load_font(True, 15)
    f_scene = load_font(True, 12)
    f_scenecap = load_font(False, 10)
    f_tag = load_font(True, 9)
    f_head = load_font(True, 11)
    f_time = load_font(True, 12)
    f_timelabel = load_font(False, 11)
    f_foot = load_font(False, 11)

    y = MARGIN
    draw_center(draw, y, "THE WORLD", f_mast)
    y += 72
    draw_center(draw, y, "Wednesday 25 November 2026  |  50 stories  |  8 regions  |  18 fields",
                f_date)
    y += 26
    draw.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 8
    draw_center(draw, y, "  •  ".join(FIELDS[:9]), f_fields, fill=MUTED)
    y += 17
    draw_center(draw, y, "  •  ".join(FIELDS[9:]), f_fields, fill=MUTED)
    y += 21
    draw.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=1)

    # Lead headline, two lines max.
    y += 10
    lead = "720,000 Russian dead, 5 ships hit in 12 days, nuclear threat"
    lines = wrap(draw, lead, f_lead, inner)
    assert len(lines) <= 2, "lead must fit in two lines"
    for line in lines:
        draw_center(draw, y, line, f_lead)
        y += 34
    y += 4

    # Numbers strip: six boxes.
    box_w = inner // 6
    top = y
    for i, (num, label) in enumerate(NUMBERS):
        x0 = MARGIN + i * box_w
        x1 = x0 + box_w - 6
        draw.rectangle([x0, top, x1, top + 58], outline=RULE, width=1)
        cx = (x0 + x1) // 2
        draw_center_at(draw, cx, top + 5, num, f_num, fill=ACCENT)
        draw_center_at(draw, cx, top + 40, label, f_numlabel)
    y = top + 58 + 8

    # Six scenes.
    draw.text((MARGIN, y), "SIX SCENES", font=f_section, fill=INK)
    y += 22
    panel_w = (inner - 5 * 8) // 6
    panel_h = 104
    for i, (title, cap) in enumerate(SCENES):
        x0 = MARGIN + i * (panel_w + 8)
        x1 = x0 + panel_w
        draw_scene(draw, (x0, y, x1, y + panel_h - 26), i)
        draw.rectangle([x0, y, x1, y + panel_h - 26], outline=RULE, width=1)
        cx = (x0 + x1) // 2
        draw_center_at(draw, cx, y + panel_h - 22, title, f_scene)
        draw_center_at(draw, cx, y + panel_h - 10, cap, f_scenecap, fill=MUTED)
    y += panel_h + 10

    # Timeline: five ships hit in twelve days.
    draw.text((MARGIN, y), "TIMELINE — 5 SHIPS HIT IN 12 DAYS", font=f_section, fill=INK)
    y += 24
    draw.line([MARGIN + 10, y + 6, W - MARGIN - 10, y + 6], fill=RULE, width=2)
    for i, (when, what) in enumerate(TIMELINE):
        cx = MARGIN + 60 + i * ((inner - 120) // 4)
        draw.ellipse([cx - 7, y - 1, cx + 7, y + 13], fill=ACCENT)
        draw_center_at(draw, cx, y + 18, when, f_time)
        draw_center_at(draw, cx, y + 34, what, f_timelabel, fill=MUTED)
    y += 58

    # Stories grid: five columns, ten rows.
    draw.text((MARGIN, y), "50 STORIES", font=f_section, fill=INK)
    y += 22
    cols, rows = 5, 10
    cell_w = inner // cols
    cell_h = 39
    for idx, (region, headline) in enumerate(STORIES):
        col, row = idx % cols, idx // cols
        x0 = MARGIN + col * cell_w
        y0 = y + row * cell_h
        tag_color = REGIONS[region]
        draw.text((x0 + 2, y0), region, font=f_tag, fill=tag_color)
        head_lines = wrap(draw, headline, f_head, cell_w - 8)
        assert len(head_lines) <= 2, "headline must fit in two lines: " + headline
        for j, line in enumerate(head_lines):
            draw.text((x0 + 2, y0 + 12 + j * 13), line, font=f_head, fill=INK)
        if col < cols - 1:
            draw.line([x0 + cell_w - 4, y0 + 2, x0 + cell_w - 4, y0 + cell_h - 4],
                      fill=(200, 194, 182), width=1)
    y += rows * cell_h + 8

    # Footer: must end inside the page (bottom margin kept).
    draw.line([MARGIN, y, W - MARGIN, y], fill=RULE, width=2)
    y += 8
    footer = ("THE WORLD  •  Wednesday 25 November 2026  •  50 stories, 8 regions, "
              "18 fields  •  Sources: wires and official statements  •  "
              "The lead toll is Kyiv's figure; ship attacks are counted over 12 days.")
    foot_lines = wrap(draw, footer, f_foot, inner)
    assert len(foot_lines) <= 2, "footer must fit in two lines"
    for line in foot_lines:
        draw_center(draw, y, line, f_foot, fill=MUTED)
        y += 15
    assert y <= H - MARGIN, "footer runs past the bottom edge"
    print("footer bottom y =", y, "page =", H, "margin =", MARGIN)

    img.save("entry.png")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    build()
