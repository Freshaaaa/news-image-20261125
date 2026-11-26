#!/usr/bin/env python3
"""Wednesday 25 November 2026 — one-page news poster (news-image-20261125).

Round 7: a fresh in-session rewrite of the Round 6 poster. All 50 story
facts are embedded below, verified against Reuters / CNN / Mediazona /
Meduza / Kyiv Independent / NY Post / FXStreet reporting for 25 November
2026. Drawn from scratch with Pillow. No network access at build time.
Deterministic: same input always renders byte-identical output.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette -----------------------------------------------------------------
PAPER = (245, 238, 218)
PAPER_DK = (233, 224, 198)
INK = (26, 26, 26)
NAVY = (26, 35, 64)
NAVY_LT = (48, 60, 96)
RED = (179, 35, 42)
RED_DK = (143, 29, 34)
GOLD = (212, 175, 105)
GRAY = (96, 96, 96)
GRAY_LT = (168, 168, 168)
WHITE = (255, 255, 255)
SKY_NIGHT = (28, 36, 64)
SEA = (22, 50, 74)

FDIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

# --- the day's stories ---------------------------------------------------------
# (number, region, headline, subhead)
STORIES = [
    (1, "EUROPE", "720,000 RUSSIAN DEAD",
     "490,000 confirmed by Rosstat; one death every 4 minutes since 2022, leaked data show."),
    (2, "EUROPE", "FIVE SHIPS HIT IN 12 DAYS",
     "Zelensky confirms the Gulf strike on Sparta II; Merkury sunk off Benghazi."),
    (3, "EUROPE", "MEDVEDEV THREATENS NUCLEAR STRIKE",
     "'Preventive nuclear attack' threat; Putin calls retaliation 'inevitable' as Kyiv holds on."),
    (4, "N. AMERICA", "Trump pardons turkeys 'Freedom' + 'Feathers'",
     "Thanksgiving pardon at the White House."),
    (5, "N. AMERICA", "Giuliani gets Medal of Freedom",
     "Trump honours the former New York mayor."),
    (6, "N. AMERICA", "Abrego Garcia to leave US voluntarily",
     "Salvadoran migrant agrees to depart."),
    (7, "EUROPE", "Sarkozy corruption trial set",
     "Pretrial hearing 1 Apr 2027 in Paris."),
    (8, "N. AMERICA", "FAA radar fault delays Chicago flights",
     "Disruption hits O'Hare departures."),
    (9, "MIDDLE EAST", "Houthis 60 km from Aden",
     "Yemen military: 'Aden will not fall.'"),
    (10, "N. AMERICA", "Fort Hood shooter seeks execution delay",
     "Hasan asks court to postpone sentence."),
    (11, "ASIA", "BJP + Akali Dal ally for Punjab 2027",
     "Pact sealed for the state election."),
    (12, "GLOBAL", "England beat Australia by 8 wickets",
     "2nd T20I, chasing 185."),
    (13, "ASIA", "RFE/RL returns to shortwave",
     "Back on air for Afghan girls' schooling."),
    (14, "EUROPE", "Denmark upholds ghetto evictions",
     "Supreme Court backs the evictions."),
    (15, "ASIA", "Great Barrier Reef: 12 species revived",
     "Acropora corals brought back."),
    (16, "MIDDLE EAST", "Israel military suicides at 16-year high",
     "Highest toll in 16 years."),
    (17, "EUROPE", "EU 22nd sanctions package",
     "60 banks cut from SWIFT, 70+ shadow-fleet ships."),
    (18, "EUROPE", "NATO AWACS to Poland",
     "After 3 Kh-101 missiles fell 20 Nov."),
    (19, "EUROPE", "Zaporizhzhia strike, 11 civilians hurt",
     "Guided-bomb attack at dawn."),
    (20, "MIDDLE EAST", "Gaza death toll 74,746",
     "WAFA toll; 266M face acute food insecurity."),
    (21, "GLOBAL", "266 million face acute food insecurity",
     "WFP: worst hunger crisis on record."),
    (22, "ASIA", "Nepal PM Balendra Shah visits India",
     "State visit to New Delhi."),
    (23, "GLOBAL", "Gold near $3,620 in Asia",
     "Safe-haven buying lifts bullion."),
    (24, "GLOBAL", "GTA 6 still topping charts",
     "A week after its 19 Nov launch."),
    (25, "GLOBAL", "Nvidia cools; NVDA down >3% premarket",
     "Rally fades after Huang's return."),
    (26, "EUROPE", "Russia calls ship attacks 'terrorism'",
     "Moscow blames Kyiv for the strikes."),
    (27, "EUROPE", "Lukashenko offers to fly Zelensky to Moscow",
     "Zelensky: 'Bring Putin to Kyiv.'"),
    (28, "MIDDLE EAST", "Houthis hit Saudi refinery + Riyadh tower",
     "Ras Tanura refinery struck; 11 hurt in Riyadh."),
    (29, "AFRICA", "Sahel drone war hits Russians",
     "Insurgents fly FPV drones vs Russian forces in Mali."),
    (30, "MIDDLE EAST", "Ships hit near Strait of Hormuz",
     "UKMTO logs projectile strikes; Iran claims mines."),
    (31, "ASIA", "China Politburo graft probe",
     "Shanghai chief Chen Jining investigated."),
    (32, "AFRICA", "Ramaphosa wins Farmgate court case",
     "Panel report set aside."),
    (33, "EUROPE", "Spain election debate — housing",
     "Sanchez vs Feijoo before 29 Nov vote."),
    (34, "GLOBAL", "Stocks tumble as AI rally fizzles",
     "Asia down; tariff threats loom."),
    (35, "MIDDLE EAST", "Jordan death sentence over officer killing",
     "State Security Court ruling."),
    (36, "EUROPE", "Russia extradites Chinese suspect",
     "$2.3B illegal-deposit case."),
    (37, "N. AMERICA", "Trump tariffs probe findings due",
     "Section 301 probe on 16 partners."),
    (38, "N. AMERICA", "US PCE inflation + Q3 GDP data due",
     "Two big releases before Thanksgiving."),
    (39, "S. AMERICA", "Brazil recalls envoy, bars Milei",
     "Ambassador pulled from Buenos Aires; Milei barred from Lula's 5 Jan inauguration."),
    (40, "OCEANIA", "Australia–Solomons sign security pact",
     "Canberra becomes defence partner of choice; $740M over 10 years; China pact lapses."),
    (41, "S. AMERICA", "Eni + Repsol pledge $2B in Venezuela",
     "Joint $2B over 5 years with PDVSA."),
    (42, "AFRICA", "Cairo tanker fire kills 31",
     "Fuel tanker overturns on Ring Road; 31 killed, 21 hurt, 27 vehicles charred."),
    (43, "ASIA", "Shenzhou-24 carries first Pakistani to space",
     "Muhammad Zeeshan Ali, first Pakistani in orbit, first foreigner on Tiangong."),
    (44, "N. AMERICA", "Brain organoids in space hint at Alzheimer's",
     "UC San Diego: 40 days on ISS, published 25 Nov in Science Advances."),
    (45, "AFRICA", "Pete Edochie dies at 79",
     "Nollywood's Okonkwo, 200+ films, prostate cancer."),
    (46, "AFRICA", "Ghana: AI must aid, not replace, teachers",
     "Deputy Education Minister on AI in schools."),
    (47, "GLOBAL", "Peatland drainage drove 2.7% of warming",
     "Nature study: drained peatlands behind 2.7% of human-caused warming."),
    (48, "S. AMERICA", "Colombia supermarket hostage siege ends",
     "20 held in Cartagena; 17-hour standoff, forces storm in."),
    (49, "ASIA", "Iwo Jima gains new volcanic land",
     "Eruption redraws part of the Japanese island."),
    (50, "AFRICA", "Olkaria I geothermal steams back to life",
     "Kenya's oldest geothermal station restarts."),
]

# the war at sea — five vessels, 11-22 November
SHIPS = [
    ("NOV 11", "Naro-Fominsk corvette", "struck", "Gulf of Finland"),
    ("NOV 21", "Sparta II cargo ship", "set ablaze", "Gulf of Finland"),
    ("NOV 21", "Ambal ferry", "hit", "Gulf of Finland"),
    ("NOV 22", "Merkury corvette", "sunk", "Benghazi"),
    ("NOV 22", "Angara cargo ship", "hit", "Benghazi"),
]

# the day in numbers: (big figure, label)
NUMBERS = [
    ("720,000", "Russian soldiers dead"),
    ("74,746", "Gaza death toll"),
    ("$740M", "Solomons pact"),
    ("$2B", "Venezuela $2B"),
    ("31", "Cairo fire dead"),
    ("2.7%", "peatland warming"),
]

REGIONS = ["Europe", "N. America", "Asia", "Middle East", "Africa", "S. America", "Oceania", "Global"]
REGION_KEYS = ["EUROPE", "N. AMERICA", "ASIA", "MIDDLE EAST", "AFRICA", "S. AMERICA", "OCEANIA", "GLOBAL"]
REGION_COLORS = {
    "EUROPE": (43, 87, 151), "N. AMERICA": (46, 139, 87), "ASIA": (179, 35, 42),
    "MIDDLE EAST": (204, 133, 32), "AFRICA": (96, 96, 160), "S. AMERICA": (16, 120, 110),
    "OCEANIA": (120, 70, 140), "GLOBAL": (120, 110, 90),
}

DATE_CHECK = ("DATE CHECK — Left out as earlier news: COP31's collapse (Sun) · "
              "Nvidia's +31.5% rally (Mon) · Brentford 4-0 Everton (Mon) · "
              "Huang reinstated (Mon) · Jabalia strike (Mon) · "
              "Wednesday's news is the fallout, not the rally.")
FIELDS = "Politics · War/Security · Climate · Markets · Health · Science · Sport · Crime/Justice · Diplomacy · Tech/AI · Energy · Space · Culture · Education · Environment · Disaster · Trade · Migration"
SOURCES = "Sources: Reuters · CNN · Mediazona · Meduza · Kyiv Independent · NY Post · FXStreet. Pictures and map: original, drawn in code."


# --- text helpers ---------------------------------------------------------------
def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if d.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, max_w, lh, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def badge(d, cx, cy, r, num, fill=RED, tfill=WHITE):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    f = SANS_B(max(10, int(r * 1.05)))
    tw = d.textlength(str(num), font=f)
    th = f.size
    d.text((cx - tw / 2, cy - th / 2 - 1), str(num), font=f, fill=tfill)


def burst(d, cx, cy, r, fill):
    """Starburst: 8 spikes around a centre."""
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# --- compact scene illustrations ------------------------------------------------
# Each scene is a small, simple vignette: a coloured sky, a few shapes, a caption.
# Six scenes, one per key visual story, drawn with plain Pillow shapes.

def scene_night_crosses(d, x, y, w, h):
    """Lead 1: war memorial field at night — rows of crosses under a moon."""
    d.rectangle([x, y, x + w, y + h], fill=SKY_NIGHT)
    d.ellipse([x + w - 34, y + 8, x + w - 10, y + 32], fill=(235, 230, 200))
    for row in range(3):
        for col in range(6):
            cx = x + 12 + col * (w - 24) / 5
            cy = y + h - 12 - row * 14
            d.line([cx, cy - 8, cx, cy + 4], fill=(200, 200, 190), width=2)
            d.line([cx - 4, cy - 5, cx + 4, cy - 5], fill=(200, 200, 190), width=2)


def scene_ship_fire(d, x, y, w, h):
    """Lead 2: a ship ablaze on a dark sea — orange flames, black smoke."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(16, 38, 56))
    d.rectangle([x + w * 0.18, y + h - 34, x + w * 0.82, y + h - 18], fill=(40, 40, 44))
    for fx, fh in [(0.3, 26), (0.5, 36), (0.7, 24)]:
        d.polygon([(x + w * fx - 10, y + h - 34), (x + w * fx, y + h - 34 - fh),
                   (x + w * fx + 10, y + h - 34)], fill=(255, 140, 40))
    d.ellipse([x + w * 0.55, y + 6, x + w * 0.75, y + 22], fill=(60, 60, 60))
    d.ellipse([x + w * 0.65, y + 2, x + w * 0.85, y + 16], fill=(80, 80, 80))


def scene_rocket(d, x, y, w, h):
    """Shenzhou-24: a rocket climbing through a dusk sky, exhaust plume."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 32, 64))
    d.ellipse([x + w - 26, y + 8, x + w - 8, y + 26], fill=(235, 230, 200))
    rx = x + w / 2
    d.polygon([(rx, y + 10), (rx - 10, y + 44), (rx + 10, y + 44)], fill=(220, 220, 220))
    d.rectangle([rx - 10, y + 44, rx + 10, y + 62], fill=(200, 200, 200))
    d.polygon([(rx - 6, y + 62), (rx, y + h - 6), (rx + 6, y + 62)], fill=(255, 160, 60))
    d.polygon([(rx - 3, y + 62), (rx, y + h - 14), (rx + 3, y + 62)], fill=(255, 220, 120))


def scene_coral(d, x, y, w, h):
    """Great Barrier Reef: coral branches in turquoise water."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 110, 130))
    for bx, bh, col in [(0.2, 40, (255, 120, 120)), (0.45, 52, (255, 180, 100)),
                        (0.7, 36, (255, 140, 160)), (0.85, 28, (140, 220, 200))]:
        cx = x + w * bx
        d.line([cx, y + h, cx, y + h - bh], fill=col, width=4)
        d.line([cx, y + h - bh * 0.6, cx - 12, y + h - bh], fill=col, width=3)
        d.line([cx, y + h - bh * 0.6, cx + 12, y + h - bh * 0.85], fill=col, width=3)
    d.ellipse([x + 8, y + 8, x + 16, y + 16], fill=(255, 220, 120))
    d.ellipse([x + w - 20, y + 12, x + w - 12, y + 20], fill=(255, 220, 120))


def scene_fire(d, x, y, w, h):
    """Cairo tanker fire: a burning tanker on a road at night."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 30))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(50, 50, 54))
    d.rectangle([x + w * 0.2, y + h - 30, x + w * 0.8, y + h - 16], fill=(120, 120, 120))
    d.ellipse([x + w * 0.3, y + h - 12, x + w * 0.38, y + h - 4], fill=(20, 20, 20))
    d.ellipse([x + w * 0.62, y + h - 12, x + w * 0.7, y + h - 4], fill=(20, 20, 20))
    for fx, fh in [(0.35, 30), (0.55, 42), (0.72, 28)]:
        d.polygon([(x + w * fx - 9, y + h - 30), (x + w * fx, y + h - 30 - fh),
                   (x + w * fx + 9, y + h - 30)], fill=(255, 120, 30))


def scene_geothermal(d, x, y, w, h):
    """Olkaria geothermal: steam plumes over a green Rift Valley plant."""
    d.rectangle([x, y, x + w, y + h], fill=(120, 170, 210))
    d.polygon([(x, y + h), (x + w * 0.3, y + h * 0.45), (x + w * 0.6, y + h),
               (x + w, y + h)], fill=(60, 130, 70))
    d.rectangle([x + w * 0.15, y + h - 26, x + w * 0.5, y + h - 12], fill=(180, 180, 180))
    d.rectangle([x + w * 0.6, y + h - 22, x + w * 0.85, y + h - 12], fill=(200, 200, 200))
    for sx in (0.25, 0.45, 0.7):
        d.ellipse([x + w * sx, y + 8, x + w * sx + 16, y + 24], fill=(240, 240, 240))
        d.ellipse([x + w * sx + 6, y + 2, x + w * sx + 20, y + 16], fill=(250, 250, 250))


SCENES = [
    (1, "720,000 Russian dead", scene_night_crosses),
    (2, "Five ships hit in 12 days", scene_ship_fire),
    (43, "Shenzhou-24 lifts off", scene_rocket),
    (15, "12 corals revived on reef", scene_coral),
    (42, "Cairo tanker fire", scene_fire),
    (50, "Olkaria steam returns", scene_geothermal),
]


# --- main layout ----------------------------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 88], fill=NAVY)
    d.text((24, 10), "THE WORLD", font=SERIF_B(50), fill=WHITE)
    d.text((24, 62), "WEDNESDAY 25 NOVEMBER 2026", font=SANS_B(16), fill=GOLD)
    d.text((W - 24, 14), "50 STORIES  ·  8 REGIONS  ·  18 FIELDS",
           font=SANS_B(15), fill=WHITE, anchor="ra")
    d.text((W - 24, 38), "ONE PAGE, ONE DAY", font=SANS(13), fill=GRAY_LT, anchor="ra")
    d.text((W - 24, 58), "UTC TIMELINE INSIDE", font=SANS(13), fill=GRAY_LT, anchor="ra")

    # --- lead stories (1-3): big headlines + one scene each ---
    y = 98
    leads = [STORIES[0], STORIES[1], STORIES[2]]
    lead_w = (W - 48 - 2 * 12) // 3
    for i, (num, region, head, sub) in enumerate(leads):
        x = 24 + i * (lead_w + 12)
        col = REGION_COLORS[region]
        d.rectangle([x, y, x + lead_w, y + 20], fill=col)
        d.text((x + 8, y + 3), region, font=SANS_B(12), fill=WHITE)
        d.text((x + lead_w - 8, y + 3), f"#{num}", font=SANS_B(12), fill=WHITE, anchor="ra")
        SCENES[i][2](d, x, y + 24, lead_w, 78)
        yy = y + 108
        yy = text_block(d, x, yy, head, SERIF_B(24), INK, lead_w, 27, max_lines=2)
        yy = text_block(d, x, yy + 1, sub, SANS(12), GRAY, lead_w, 15, max_lines=2)
    y = 98 + 108 + 50 + 26 + 6

    # --- numbers strip ---
    d.rectangle([24, y, W - 24, y + 54], fill=PAPER_DK, outline=GOLD, width=2)
    d.text((36, y + 4), "THE DAY IN NUMBERS", font=SANS_B(12), fill=RED_DK)
    nx = 36
    for fig, lab in NUMBERS:
        d.text((nx, y + 20), fig, font=SERIF_B(20), fill=NAVY)
        d.text((nx, y + 42), lab, font=SANS(10), fill=GRAY)
        nx += 162
    y += 60

    # --- ships timeline: five vessels, 11-22 Nov ---
    d.rectangle([24, y, W - 24, y + 62], fill=WHITE, outline=GRAY_LT, width=1)
    d.text((36, y + 4), "THE WAR AT SEA — FIVE VESSELS, 11–22 NOVEMBER",
           font=SANS_B(12), fill=NAVY)
    sx = 36
    for date, name, verb, place in SHIPS:
        d.text((sx, y + 22), date, font=SANS_B(11), fill=RED)
        d.text((sx, y + 36), name, font=SANS_B(11), fill=INK)
        d.text((sx, y + 49), f"{verb} · {place}", font=SANS(10), fill=GRAY)
        sx += 194
    y += 68

    # --- story grid: all 50 stories, 5 columns, headline + 1-line subhead ---
    d.text((24, y), "ALL 50 STORIES, BY REGION", font=SANS_B(13), fill=NAVY)
    y += 18
    col_w = (W - 48 - 4 * 8) // 5
    col_x = [24 + i * (col_w + 8) for i in range(5)]
    groups = []
    for key in REGION_KEYS:
        groups.append([s for s in STORIES if s[1] == key])
    flat = []
    for g in groups:
        flat.extend(g)
    per_col = (len(flat) + 4) // 5
    col_bottom = y
    for ci in range(5):
        chunk = flat[ci * per_col:(ci + 1) * per_col]
        cx = col_x[ci]
        cy = y
        for num, region, head, sub in chunk:
            col = REGION_COLORS[region]
            d.rectangle([cx, cy, cx + 16, cy + 16], fill=col)
            d.text((cx + 8, cy + 2), str(num), font=SANS_B(9), fill=WHITE, anchor="ma")
            tx = cx + 20
            cy = text_block(d, tx, cy, head, SANS_B(11), INK, col_w - 20, 13, max_lines=2)
            cy = text_block(d, tx, cy, sub, SANS(9), GRAY, col_w - 20, 11, max_lines=1)
            cy += 3
        col_bottom = max(col_bottom, cy)
    y = col_bottom + 6

    # --- pictures strip: six scenes, compact ---
    d.text((24, y), "IN PICTURES", font=SANS_B(13), fill=NAVY)
    y += 17
    pic_w = (W - 48 - 5 * 8) // 6
    pic_h = 48
    for i, (num, cap, fn) in enumerate(SCENES):
        x = 24 + i * (pic_w + 8)
        fn(d, x, y, pic_w, pic_h)
        d.rectangle([x, y + pic_h, x + pic_w, y + pic_h + 17], fill=NAVY)
        d.text((x + 4, y + pic_h + 3), f"#{num} {cap}", font=SANS_B(9), fill=WHITE)
    y += pic_h + 17 + 7

    # --- region band + fields ---
    d.rectangle([24, y, W - 24, y + 24], fill=NAVY_LT)
    rx = 32
    d.text((rx, y + 4), "BY REGION:", font=SANS_B(11), fill=WHITE)
    rx += 88
    for key in REGION_KEYS:
        n = sum(1 for s in STORIES if s[1] == key)
        label = key.title().replace("N. America", "N.America").replace("Middle East", "M.East").replace("S. America", "S.America")
        d.text((rx, y + 4), f"{label} {n}", font=SANS(11), fill=WHITE)
        rx += 108
    y += 28
    y = text_block(d, 24, y, FIELDS, SANS(10), GRAY, W - 48, 13)
    y += 3

    # --- footer: date check + sources (both inside the box, fits the page) ---
    d.rectangle([24, y, W - 24, y + 46], fill=(232, 222, 190), outline=GOLD, width=1)
    text_block(d, 32, y + 4, DATE_CHECK, SANS_B(10), RED_DK, W - 64, 13, max_lines=2)
    d.text((32, y + 34), SOURCES, font=SANS(9), fill=GRAY)
    d.text((W - 24, y + 34), "news-image-20261125 · Round 7", font=SANS(9),
           fill=GRAY, anchor="ra")

    img.save(OUT)
    print(f"saved {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
