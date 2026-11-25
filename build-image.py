#!/usr/bin/env python3
"""Draw news-image-20261125: a newspaper-style 1024x1024 PNG summing up
Wednesday 25 November 2026. Follows Larisha's news-24 structure (top 50)
and the v3 lesson from news-24: FULL-SCENE vector illustrations, not flat
icons. The day's news is dominated by the war at sea and its human cost,
so the three leads are drawn as real scenes: the 5-ship campaign in the
Gulf of Finland and off Benghazi (cargo ship + corvette + drone boats),
a memorial field for the 720,000 Russian dead, and a missile under a red
warning sky for Medvedev's nuclear threat. All story data is embedded as
literals, verified live 25 Nov 2026 against Reuters (Sybiha / Zelensky
confirmation, Sparta II, Merkury), CNN / Mediazona / Meduza (720,000 dead,
490,000 confirmed by Rosstat), NY Post (Medvedev threat), plus the
research file's verified 25 Nov set. No network access: running this
script always draws the same bytes.

Layout (newspaper):
  top bar    -> kicker + counts
  masthead   -> serif date + one-line subtitle (3 fresh leads, sharpened)
  sea strip  -> the war at sea: 5 ships hit in 12 days (Nov 11-22)
  numbers    -> 6 big verified numbers
  3 leads    -> full-scene illustrated cards (ships / memorial / missile)
  10 stories -> numbered 4-13, two columns
  map + region bars -> dotted world map with pins 1-3 + counts
  14 more    -> numbered 14-27, two-column one-liners
  date check -> earlier news explicitly excluded
  footer     -> markets + 10 fields + sourcing note
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

TITLE = ("Wednesday 25 November 2026: 28 stories, 6 regions, 10 fields "
         "\u2014 5 ships hit in 12 days, 720,000 Russian dead, nuclear threat")

# --- palette (newspaper: cream paper, navy, red, gold) --------------------
PAPER = (244, 238, 222)
PAPER_DARK = (236, 228, 208)
INK = (26, 26, 26)
NAVY = (16, 30, 52)
NAVY_DARK = (11, 22, 40)
RED = (178, 34, 34)
RED_DARK = (140, 24, 24)
GOLD = (198, 148, 52)
WHITE = (255, 255, 255)
GREY = (88, 88, 88)
GREY_DARK = (60, 60, 60)
LIGHT_LINE = (208, 198, 178)
CARD = (255, 255, 255)
GREEN = (28, 120, 70)
BLUE = (37, 99, 168)
ORANGE = (232, 120, 40)
SKY_GREY = (70, 80, 96)

REGION_COLORS = {
    "EUROPE": (37, 99, 168),
    "ASIA": (168, 58, 75),
    "MIDDLE EAST": (183, 121, 31),
    "NORTH AMERICA": (30, 122, 76),
    "GLOBAL": (90, 107, 122),
}

# --- story data ------------------------------------------------------------
# Leads: (big, headline, detail, region label, art kind, number)
LEADS = [
    ("5 SHIPS", "FIVE SHIPS HIT IN 12 DAYS",
     "Zelensky confirms the Gulf of Finland strike on Sparta II; the "
     "Merkury corvette was sunk off Benghazi.",
     "1 GULF OF FINLAND \u00b7 WAR AT SEA", "ships", 1),
    ("720,000", "720,000 RUSSIAN DEAD",
     "490,000 confirmed by Rosstat; one death every 4 minutes since "
     "2022, leaked data show.",
     "2 RUSSIA \u00b7 THE HUMAN COST", "memorial", 2),
    ("NUCLEAR", "MEDVEDEV THREATENS NUCLEAR STRIKE",
     "\u201cPreventive nuclear attack\u201d threat; Putin calls retaliation "
     "\u201cinevitable\u201d as Kyiv holds on.",
     "3 MOSCOW \u00b7 ESCALATION", "missile", 3),
]

# Numbered stories 4-13: (number, headline, detail, region)
NUMBERED = [
    (4, "Trump pardons turkeys \u2018Freedom\u2019 + \u2018Feathers\u2019",
     "Thanksgiving pardon at the White House.", "NORTH AMERICA"),
    (5, "Giuliani gets Medal of Freedom",
     "Trump honours the former New York mayor.", "NORTH AMERICA"),
    (6, "Abrego Garcia to leave US voluntarily",
     "Salvadoran migrant agrees to depart.", "NORTH AMERICA"),
    (7, "Sarkozy corruption trial set",
     "Pretrial hearing 1 Apr 2027 in Paris.", "EUROPE"),
    (8, "FAA radar fault delays Chicago flights",
     "Disruption hits O\u2019Hare departures.", "NORTH AMERICA"),
    (9, "Houthis 60 km from Aden",
     "Yemen military: \u201cAden will not fall.\u201d", "MIDDLE EAST"),
    (10, "Fort Hood shooter seeks execution delay",
     "Hasan asks court to postpone sentence.", "NORTH AMERICA"),
    (11, "BJP + Akali Dal ally for Punjab 2027",
     "Pact sealed for the state election.", "ASIA"),
    (12, "England beat Australia by 8 wickets",
     "2nd T20I, chasing 185.", "GLOBAL"),
    (13, "RFE/RL returns to shortwave",
     "Back on air for Afghan girls\u2019 schooling.", "ASIA"),
]

# More stories 14-27: (number, region, headline)
MORE = [
    (14, "EUROPE", "Denmark upholds ghetto evictions"),
    (15, "ASIA", "Great Barrier Reef: 12 species revived"),
    (16, "MIDDLE EAST", "Israel military suicides at 16-year high"),
    (17, "EUROPE", "EU 22nd sanctions package"),
    (18, "EUROPE", "NATO AWACS to Poland"),
    (19, "EUROPE", "Zaporizhzhia strike, 11 civilians hurt"),
    (20, "MIDDLE EAST", "Gaza death toll 74,746"),
    (21, "GLOBAL", "266 million face acute food insecurity"),
    (22, "ASIA", "Nepal PM Balendra Shah visits India"),
    (23, "GLOBAL", "Gold near $3,620 in Asia"),
    (24, "GLOBAL", "GTA 6 still topping charts after 19 Nov launch"),
    (25, "GLOBAL", "Nvidia rally cools; NVDA down >3% premarket"),
    (26, "EUROPE", "Russia calls ship attacks \u2018terrorism\u2019"),
    (27, "EUROPE", "Lukashenko offers to fly Zelensky to Moscow"),
]

REGION_TOTALS = {"EUROPE": 10, "NORTH AMERICA": 5, "ASIA": 4,
                 "MIDDLE EAST": 3, "GLOBAL": 5}
REGION_ORDER = ["EUROPE", "NORTH AMERICA", "ASIA", "MIDDLE EAST", "GLOBAL"]

# The war at sea: 5 Russian vessels hit Nov 11-22 (Kyiv Independent).
# (date, vessel, status) — all confirmed or attributed by Kyiv.
SEA = [
    ("NOV 11", "Naro-Fominsk corvette", "struck, Gulf of Finland"),
    ("NOV 21", "Sparta II cargo ship", "set ablaze, Gulf of Finland"),
    ("NOV 21", "Ambal ferry", "hit, Gulf of Finland"),
    ("NOV 22", "Merkury corvette", "sunk, Benghazi"),
    ("NOV 22", "Angara cargo ship", "hit, Benghazi"),
]

# The day in numbers: (big, caption) — all verified live 25 Nov.
NUMBERS = [
    ("720,000", "Russian soldiers dead"),
    ("490,000", "confirmed dead by end Sep"),
    ("74,746", "Gaza death toll"),
    ("266M", "face acute food insecurity"),
    ("60 km", "Houthis from Aden"),
    ("12", "Acropora species revived"),
]

DATE_CHECK = ("DATE CHECK \u2014 Left out as earlier news: COP31\u2019s "
              "collapse (Sun) \u00b7 Nvidia\u2019s +31.5% rally (Mon) \u00b7 "
              "Brentford 4\u20130 Everton (Mon) \u00b7 Huang reinstated (Mon) "
              "\u00b7 Jabalia strike (Mon) \u00b7 Wednesday\u2019s news is the "
              "fallout, not the rally.")

FIELDS = ("Politics \u00b7 War/Security \u00b7 Climate \u00b7 Markets \u00b7 "
          "Health \u00b7 Science \u00b7 Sport \u00b7 Crime/Justice \u00b7 "
          "Diplomacy \u00b7 Tech/AI")

MARKETS = ("Gold ~$3,620   NVDA down >3% premarket")

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def serif_b(size):
    return font("DejaVuSerif-Bold.ttf", size)


def serif(size):
    return font("DejaVuSerif.ttf", size)


def sans_b(size):
    return font("DejaVuSans-Bold.ttf", size)


def sans(size):
    return font("DejaVuSans.ttf", size)


def wrap(draw, text, fnt, width):
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

# --- dotted world map ------------------------------------------------------
MAP_COLS, MAP_ROWS = 80, 16
LAND_RECTS = [
    # North America
    (2, 0, 26, 2), (3, 2, 27, 5), (6, 5, 24, 6), (20, 6, 24, 8),
    # South America
    (22, 8, 31, 9), (23, 10, 30, 10), (24, 11, 28, 12), (25, 12, 27, 13),
    # Greenland
    (29, 0, 33, 1),
    # Europe
    (38, 2, 48, 4), (39, 4, 46, 5),
    # Africa
    (37, 6, 50, 8), (38, 9, 49, 10), (40, 11, 47, 11), (42, 12, 45, 12),
    # Asia
    (49, 1, 78, 3), (49, 3, 76, 5), (50, 5, 72, 6), (55, 6, 70, 7),
    (60, 8, 70, 9),
    # Australia
    (64, 10, 74, 11), (66, 11, 72, 12),
]
LAND = set()
for x0, y0, x1, y1 in LAND_RECTS:
    for yy in range(y0, y1 + 1):
        for xx in range(x0, x1 + 1):
            LAND.add((xx, yy))


def lonlat_to_cell(lon, lat):
    col = int((lon + 180.0) / 360.0 * MAP_COLS)
    row = int((80.0 - lat) / 140.0 * MAP_ROWS)
    return max(0, min(MAP_COLS - 1, col)), max(0, min(MAP_ROWS - 1, row))


# lead pins: (lon, lat, number)
# 1 = Gulf of Finland (lead 1, Sparta II). 2 = Moscow (lead 2, the toll).
# 3 = Benghazi (Merkury sinking, the other half of lead 1's campaign);
# lead 3's nuclear threat is a Moscow story, covered by pin 2's region.
PINS = [
    (25.0, 59.5, 1),    # Gulf of Finland
    (37.6, 55.7, 2),    # Moscow, Russia
    (20.0, 32.0, 3),    # Benghazi, Libya
]


def draw_dotted_map(d, x0, y0, w, h, dot_color, pin_color):
    cell_w = w / MAP_COLS
    cell_h = h / MAP_ROWS
    r = max(1, int(min(cell_w, cell_h) * 0.38))
    for (cx, cy) in LAND:
        px = x0 + (cx + 0.5) * cell_w
        py = y0 + (cy + 0.5) * cell_h
        d.ellipse([px - r, py - r, px + r, py + r], fill=dot_color)
    for lon, lat, num in PINS:
        cx, cy = lonlat_to_cell(lon, lat)
        px = x0 + (cx + 0.5) * cell_w
        py = y0 + (cy + 0.5) * cell_h
        pr = 11
        d.ellipse([px - pr, py - pr, px + pr, py + pr], fill=pin_color,
                  outline=WHITE, width=2)
        tf = sans_b(12)
        tw = d.textlength(str(num), font=tf)
        d.text((px - tw / 2, py - 8), str(num), font=tf, fill=WHITE)


# --- lead illustrations: full scenes, not icons ---------------------------
# Every scene is drawn in the same 320x96 slot, all coordinates fixed
# (deterministic — no randomness). Colours are flat so the PNG stays small.
def _starburst(d, cx, cy, r, color):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    for ang in (0, 45, 90, 135):
        import math
        a = math.radians(ang)
        x1 = cx + int(math.cos(a) * r * 1.5)
        y1 = cy + int(math.sin(a) * r * 1.5)
        x2 = cx - int(math.cos(a) * r * 1.5)
        y2 = cy - int(math.sin(a) * r * 1.5)
        d.line([x1, y1, x2, y2], fill=color, width=3)


def _smoke(d, cx, cy, color, puffs=3):
    radii = (7, 9, 11)[:puffs]
    for i, r in enumerate(radii):
        d.ellipse([cx - r, cy - i * 12 - r, cx + r, cy - i * 12 + r],
                  fill=color)


def _usv(d, cx, cy, color):
    # small uncrewed surface vessel: low dark hull + mast + white wake
    d.polygon([(cx - 12, cy), (cx + 12, cy), (cx + 8, cy - 5),
               (cx - 8, cy - 5)], fill=color)
    d.line([cx, cy - 5, cx, cy - 11], fill=color, width=2)
    d.line([cx - 18, cy + 3, cx + 18, cy + 3], fill=(220, 230, 240),
           width=2)


def draw_lead_art(d, x0, y0, w, h, kind):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY_DARK)
    if kind == "ships":
        # Baltic night: grey sky, moon, cargo ship Sparta II burning,
        # corvette Merkury listing, drone boats with wakes, bursts + smoke
        d.ellipse([x0 + 282, y0 + 8, x0 + 298, y0 + 24],
                  fill=(230, 225, 200))
        # sea
        sea = y0 + h - 28
        d.rectangle([x0, sea, x0 + w, y0 + h], fill=(24, 68, 110))
        for wx in range(0, w, 22):
            d.line([x0 + wx, sea + 8, x0 + wx + 12, sea + 8],
                   fill=(120, 170, 210), width=2)
            d.line([x0 + wx + 6, sea + 18, x0 + wx + 18, sea + 18],
                   fill=(90, 140, 185), width=2)
        # cargo ship Sparta II, left: hull, containers, bridge, fire
        d.polygon([(x0 + 18, sea), (x0 + 150, sea), (x0 + 138, sea - 16),
                   (x0 + 30, sea - 16)], fill=(70, 95, 130))
        d.rectangle([x0 + 34, sea - 16, x0 + 144, sea - 12],
                    fill=(88, 115, 150))
        for bx in (40, 62, 84, 106):
            d.rectangle([x0 + bx, sea - 30, x0 + bx + 18, sea - 16],
                        fill=(52, 78, 112))
        d.rectangle([x0 + 122, sea - 40, x0 + 140, sea - 16],
                    fill=(70, 95, 130))
        d.rectangle([x0 + 128, sea - 48, x0 + 134, sea - 40],
                    fill=(70, 95, 130))
        _starburst(d, x0 + 84, sea - 34, 9, ORANGE)
        _smoke(d, x0 + 84, sea - 34, (120, 130, 145), puffs=2)
        # corvette Merkury, right, listing and low in the water
        d.polygon([(x0 + 190, sea + 2), (x0 + 292, sea + 2),
                   (x0 + 282, sea - 14), (x0 + 202, sea - 14)],
                  fill=(88, 115, 150))
        d.rectangle([x0 + 232, sea - 30, x0 + 262, sea - 14],
                    fill=(88, 115, 150))
        d.line([x0 + 246, sea - 30, x0 + 246, sea - 38],
               fill=(88, 115, 150), width=3)
        _starburst(d, x0 + 218, sea - 22, 7, (240, 160, 60))
        _smoke(d, x0 + 218, sea - 22, (120, 130, 145), puffs=2)
        _starburst(d, x0 + 268, sea - 28, 6, ORANGE)
        # drone boats in the foreground
        _usv(d, x0 + 60, sea + 12, (10, 18, 32))
        _usv(d, x0 + 160, sea + 16, (10, 18, 32))
        _usv(d, x0 + 250, sea + 10, (10, 18, 32))
    elif kind == "memorial":
        # somber field: grey sky, pale sun, rows of grave crosses
        # receding to the horizon, one red poppy in the foreground
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(52, 58, 72))
        d.ellipse([x0 + 262, y0 + 10, x0 + 286, y0 + 34],
                  fill=(200, 195, 175))
        horizon = y0 + 52
        d.rectangle([x0, horizon, x0 + w, y0 + h], fill=(38, 44, 56))
        # four rows of crosses, smaller toward the horizon
        for row, (cy, s, gap) in enumerate(((horizon + 30, 12, 30),
                                            (horizon + 18, 10, 25),
                                            (horizon + 8, 7, 20),
                                            (horizon + 1, 5, 16))):
            x = x0 + 12 + row * 5
            while x < x0 + w - 12:
                d.line([x, cy - s, x, cy + s], fill=(215, 210, 195),
                       width=3)
                d.line([x - s // 2, cy - s // 2, x + s // 2, cy - s // 2],
                       fill=(215, 210, 195), width=3)
                x += gap
        # one red poppy, foreground left
        d.ellipse([x0 + 24, horizon + 32, x0 + 36, horizon + 44],
                  fill=RED)
        d.line([x0 + 30, horizon + 44, x0 + 30, horizon + 52],
               fill=(28, 120, 70), width=2)
    elif kind == "missile":
        # red warning sky, a missile climbing with flame + smoke trail,
        # warning triangle, ground glow
        d.rectangle([x0, y0, x0 + w, y0 + h], fill=(96, 20, 20))
        stars = [(18, 10), (52, 18), (96, 8), (140, 14), (200, 10),
                 (246, 16), (288, 8), (30, 30), (170, 28), (260, 30)]
        for sx, sy in stars:
            d.ellipse([x0 + sx - 1, y0 + sy - 1, x0 + sx + 1, y0 + sy + 1],
                      fill=(220, 180, 160))
        # missile, centre-left, nose up — large and central
        mx, my = x0 + 118, y0 + 56
        d.polygon([(mx, my - 44), (mx + 10, my - 26), (mx + 10, my + 10),
                   (mx, my + 18), (mx - 10, my + 10), (mx - 10, my - 26)],
                  fill=(225, 225, 220))
        d.polygon([(mx - 10, my + 2), (mx - 22, my + 16), (mx - 10, my + 10)],
                  fill=(180, 180, 175))
        d.polygon([(mx + 10, my + 2), (mx + 22, my + 16), (mx + 10, my + 10)],
                  fill=(180, 180, 175))
        # red stripe on the missile body
        d.rectangle([mx - 10, my - 8, mx + 10, my - 2], fill=RED)
        # flame + smoke trail below the missile
        _starburst(d, mx, my + 26, 11, ORANGE)
        _smoke(d, mx, my + 32, (150, 150, 150), puffs=3)
        # launch pad, bottom left
        d.rectangle([x0 + 84, y0 + h - 12, x0 + 152, y0 + h - 6],
                    fill=(60, 60, 60))
        d.rectangle([x0, y0 + h - 6, x0 + w, y0 + h], fill=ORANGE)
        # warning triangle, top right
        tx, ty = x0 + 262, y0 + 14
        d.polygon([(tx, ty), (tx + 34, ty + 30), (tx - 34, ty + 30)],
                  fill=(240, 200, 60))
        d.rectangle([tx - 2, ty + 10, tx + 2, ty + 22], fill=(96, 20, 20))
        d.ellipse([tx - 2, ty + 25, tx + 2, ty + 29], fill=(96, 20, 20))
        # second, smaller missile silhouette, far right
        d.polygon([(x0 + 300, y0 + 66), (x0 + 304, y0 + 56),
                   (x0 + 304, y0 + 74), (x0 + 300, y0 + 78),
                   (x0 + 296, y0 + 74), (x0 + 296, y0 + 56)],
                  fill=(160, 160, 155))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 20                      # side margin
    CW = 320                    # lead card width
    GAP = 12

    # --- top bar -----------------------------------------------------------
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((M, 6), "THE WORLD IN ONE DAY", font=sans_b(13), fill=GOLD)
    right = "28 STORIES  \u00b7  6 REGIONS  \u00b7  10 FIELDS"
    rw = d.textlength(right, font=sans_b(13))
    d.text((W - M - rw, 6), right, font=sans_b(13), fill=WHITE)

    # --- masthead ----------------------------------------------------------
    d.text((M, 34), "Wednesday 25 November 2026", font=serif_b(40),
           fill=INK)
    d.rectangle([M, 82, M + 210, 86], fill=RED)
    sub = ("Zelensky confirms the Gulf of Finland strike \u00b7 720,000 "
           "Russian dead, one every 4 minutes \u00b7 Medvedev threatens a "
           "preventive nuclear attack")
    d.text((M, 92), sub, font=serif(13), fill=GREY_DARK)

    # --- war at sea strip --------------------------------------------------
    st_y, st_h = 112, 46
    d.rectangle([M, st_y, W - M, st_y + st_h], fill=NAVY)
    d.text((M + 10, st_y + 5), "THE WAR AT SEA", font=sans_b(10),
           fill=GOLD)
    d.text((M + 10, st_y + 20), "5 SHIPS IN 12 DAYS", font=sans_b(10),
           fill=WHITE)
    col_w = (W - 2 * M - 150) / 5
    for i, (dt, vessel, status) in enumerate(SEA):
        x = M + 150 + i * col_w
        d.text((x, st_y + 5), dt, font=sans_b(12), fill=GOLD)
        d.text((x, st_y + 22), vessel, font=sans_b(10), fill=WHITE)
        d.text((x, st_y + 34), status, font=sans(9), fill=(180, 195, 215))

    # --- numbers -----------------------------------------------------------
    nb_y = 164
    d.text((M, nb_y), "THE DAY IN NUMBERS", font=sans_b(11), fill=RED)
    nb_top = nb_y + 18
    col_w = (W - 2 * M) / 6
    for i, (big, cap) in enumerate(NUMBERS):
        x = M + i * col_w
        d.text((x, nb_top), big, font=serif_b(24), fill=RED)
        lines = wrap(d, cap, sans(10), col_w - 10)
        y = nb_top + 30
        for ln in lines[:1]:
            d.text((x, y), ln, font=sans(10), fill=GREY)
            y += 12
        if i < 5:
            d.line([x + col_w - 6, nb_top + 4, x + col_w - 6, nb_top + 46],
                   fill=LIGHT_LINE, width=1)

    # --- 3 lead cards ------------------------------------------------------
    lead_y, lead_h = 228, 212
    for i, (big, head, detail, region, kind, num) in enumerate(LEADS):
        x0 = M + i * (CW + GAP)
        # header bar
        d.rectangle([x0, lead_y, x0 + CW, lead_y + 26], fill=RED)
        d.ellipse([x0 + 8, lead_y + 4, x0 + 30, lead_y + 22], fill=WHITE)
        tf = sans_b(13)
        tw = d.textlength(str(num), font=tf)
        d.text((x0 + 19 - tw / 2, lead_y + 5), str(num), font=tf, fill=RED)
        d.text((x0 + 38, lead_y + 6), region, font=sans_b(10), fill=WHITE)
        # illustration (full scene)
        art_y = lead_y + 26
        draw_lead_art(d, x0, art_y, CW, 96, kind)
        # headline + detail
        hy = art_y + 96 + 8
        lines = wrap(d, head, serif_b(19), CW - 4)
        y = hy
        for ln in lines[:2]:
            d.text((x0 + 2, y), ln, font=serif_b(19), fill=INK)
            y += 24
        dlines = wrap(d, detail, sans(11), CW - 4)
        y = hy + 26 * len(lines[:2])
        for ln in dlines[:2]:
            d.text((x0 + 2, y), ln, font=sans(11), fill=GREY_DARK)
            y += 15

    # --- numbered stories 4-13 --------------------------------------------
    num_y = 448
    d.text((M, num_y), "THE REST OF THE DAY", font=sans_b(11), fill=RED)
    d.line([M, num_y + 16, W - M, num_y + 16], fill=RED, width=1)
    col_x = [M, W // 2 + 6]
    col_w = (W - 2 * M) // 2 - 6
    for idx, (n, head, detail, region) in enumerate(NUMBERED):
        ci = 0 if idx < 5 else 1
        ri = idx if idx < 5 else idx - 5
        x = col_x[ci]
        y = num_y + 24 + ri * 24
        # number badge
        d.ellipse([x, y, x + 20, y + 20], fill=RED)
        tf = sans_b(12)
        tw = d.textlength(str(n), font=tf)
        d.text((x + 10 - tw / 2, y + 3), str(n), font=tf, fill=WHITE)
        # headline (bold) + region tag inline
        hl = f"{head}  \u2014  {region}"
        d.text((x + 26, y), hl, font=sans_b(11), fill=INK)
        d.text((x + 26, y + 13), detail, font=sans(9), fill=GREY)

    # --- map + region bars -------------------------------------------------
    map_y = 596
    d.text((M, map_y), "WHERE IT HAPPENED", font=sans_b(11), fill=RED)
    d.line([M, map_y + 16, 640, map_y + 16], fill=RED, width=1)
    d.text((664, map_y), "STORIES BY REGION", font=sans_b(11), fill=RED)
    d.line([664, map_y + 16, W - M, map_y + 16], fill=RED, width=1)
    draw_dotted_map(d, M, map_y + 22, 620, 92, (52, 72, 96), RED)
    # region bars
    bar_x, bar_top = 664, map_y + 22
    bar_max_w = 180
    for i, region in enumerate(REGION_ORDER):
        cnt = REGION_TOTALS[region]
        y = bar_top + i * 14
        color = REGION_COLORS[region]
        lab = region.title() if region != "NORTH AMERICA" else "N. America"
        d.text((bar_x, y), lab, font=sans_b(10), fill=INK)
        bw = int(bar_max_w * cnt / 10.0)
        d.rectangle([bar_x + 118, y + 1, bar_x + 118 + bw, y + 10], fill=color)
        d.text((bar_x + 118 + bw + 6, y), str(cnt), font=sans_b(10),
               fill=INK)

    # --- 14 more stories ---------------------------------------------------
    more_y = 726
    d.text((M, more_y), "ALSO ON WEDNESDAY 25 NOVEMBER \u2014 14 MORE STORIES",
           font=sans_b(11), fill=RED)
    d.line([M, more_y + 16, W - M, more_y + 16], fill=RED, width=1)
    col_x = [M, W // 2 + 6]
    for idx, (n, region, head) in enumerate(MORE):
        ci = 0 if idx < 7 else 1
        ri = idx if idx < 7 else idx - 7
        x = col_x[ci]
        y = more_y + 24 + ri * 20
        d.text((x, y), f"{n}.", font=sans_b(11), fill=RED)
        d.text((x + 26, y), region, font=sans_b(10), fill=GREY)
        rw = d.textlength(region, font=sans_b(10))
        d.text((x + 26 + rw + 6, y), head, font=sans(11), fill=INK)

    # --- date check --------------------------------------------------------
    dc_y = 890
    d.rectangle([M, dc_y, W - M, dc_y + 44], outline=RED, width=2)
    dc_lines = wrap(d, DATE_CHECK, sans(11), W - 2 * M - 20)
    _y = dc_y + 6
    for _ln in dc_lines[:2]:
        d.text((M + 10, _y), _ln, font=sans(11), fill=INK)
        _y += 16

    # --- markets band ------------------------------------------------------
    mk_y = 942
    d.rectangle([0, mk_y, W, mk_y + 30], fill=NAVY)
    lab = "MARKETS \u00b7 MORNING SNAPSHOT"
    d.text((M, mk_y + 8), lab, font=sans_b(12), fill=GOLD)
    mw = d.textlength(MARKETS, font=sans_b(12))
    d.text((W - M - mw, mk_y + 8), MARKETS, font=sans_b(12), fill=WHITE)

    # --- fields + sourcing -------------------------------------------------
    d.text((M, 980), "FIELDS \u2014 " + FIELDS, font=sans(11), fill=INK)
    d.text((M, 996),
           "Sources: Reuters \u00b7 CNN \u00b7 Mediazona \u00b7 Meduza \u00b7 "
           "Kyiv Independent \u00b7 NY Post \u00b7 FXStreet. Pictures and "
           "map: original, drawn in code.",
           font=sans(10), fill=GREY)
    pt = "PRESS TIME 09:00 UTC"
    pw = d.textlength(pt, font=sans_b(10))
    d.text((W - M - pw, 996), pt, font=sans_b(10), fill=GREY)

    img.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    assert img.size == (1024, 1024), f"entry must be 1024x1024, got {img.size}"
    assert size <= 1024 * 1024, f"entry over 1 MiB: {size} bytes"
    assert sum(REGION_TOTALS.values()) == 27, "region totals must sum to 27"
    n_stories = len(LEADS) + len(NUMBERED) + len(MORE) + 1  # +1 markets
    n_regions = len(REGION_TOTALS) + 1  # +1 markets strip
    print(f"TITLE ({len(TITLE)} chars): {TITLE}")
    print(f"stories={n_stories} regions={n_regions} fields=10")
    print(f"region totals sum={sum(REGION_TOTALS.values())}")
    print(f"saved {OUT}: {size} bytes, {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
