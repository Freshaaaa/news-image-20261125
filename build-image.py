#!/usr/bin/env python3
"""Wednesday 25 November 2026 — one-page news poster (news-image-20261125).

Drawn from scratch with Pillow. All story facts are embedded below, verified
against Reuters / CNN / Mediazona / Meduza / Kyiv Independent / NY Post /
FXStreet reporting for 25 November 2026. No network access at build time.
Deterministic: same input always renders byte-identical output.
"""
import hashlib
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette -----------------------------------------------------------------
PAPER = (245, 238, 218)      # cream newsprint
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
SKY_RED = (143, 29, 34)

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

# stories illustrated as full scenes in the pictures strip (number -> caption)
PICTURES = [
    (28, "Houthis hit Ras Tanura + Riyadh"),
    (29, "Sahel drones vs Russians"),
    (30, "Tankers hit near Hormuz"),
    (15, "12 corals revived on reef"),
    (12, "England chase 185, win"),
    (42, "Cairo tanker fire"),
    (43, "Shenzhou-24 lifts off"),
    (40, "Solomons pact signed"),
    (39, "Brazil recalls envoy"),
    (48, "Cartagena siege ends"),
    (50, "Olkaria steam returns"),
    (44, "Organoids in orbit"),
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
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# --- full-scene illustrations ----------------------------------------------------
def scene_cemetery(d, x, y, w, h):
    """Lead 1: a war memorial field at night — rows of crosses under a moon."""
    d.rectangle([x, y, x + w, y + h], fill=SKY_NIGHT)
    d.ellipse([x + w - 52, y + 8, x + w - 18, y + 42], fill=(232, 228, 210))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(18, 24, 46))
    # rows of small white crosses, nearer rows bigger
    for row, (cy, cw, ch) in enumerate([(0.68, 6, 14), (0.78, 8, 18), (0.90, 10, 22)]):
        n = 9 - row
        for i in range(n):
            cx = x + (i + 0.5) * (w / n)
            cyv = y + h * cy
            d.rectangle([cx - cw / 2, cyv - ch / 2, cx + cw / 2, cyv + ch / 2], fill=WHITE)
            d.rectangle([cx - cw, cyv - ch / 4, cx + cw, cyv + ch / 4], fill=WHITE)
    # red poppies
    for px, py in [(0.12, 0.86), (0.55, 0.80), (0.86, 0.92)]:
        d.ellipse([x + w * px - 4, y + h * py - 4, x + w * px + 4, y + h * py + 4], fill=RED)


def scene_ships(d, x, y, w, h):
    """Lead 2: two warships on a night sea, explosions over the water."""
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    d.ellipse([x + w - 46, y + 6, x + w - 16, y + 36], fill=(232, 228, 210))
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=(14, 38, 58))
    for wy in (0.72, 0.82, 0.92):
        d.line([x + 8, y + h * wy, x + w - 8, y + h * wy], fill=(90, 140, 170), width=2)
    # ship one (left, larger)
    hx, hy = x + w * 0.10, y + h * 0.60
    d.polygon([(hx, hy + 14), (hx + w * 0.42, hy + 14), (hx + w * 0.38, hy), (hx + w * 0.06, hy)], fill=(30, 34, 40))
    d.rectangle([hx + w * 0.14, hy - 12, hx + w * 0.26, hy], fill=(30, 34, 40))
    d.rectangle([hx + w * 0.18, hy - 22, hx + w * 0.21, hy - 12], fill=(30, 34, 40))
    # ship two (right, smaller, listing)
    hx2, hy2 = x + w * 0.62, y + h * 0.66
    d.polygon([(hx2, hy2 + 10), (hx2 + w * 0.30, hy2 + 10), (hx2 + w * 0.27, hy2), (hx2 + w * 0.04, hy2)], fill=(44, 48, 56))
    # explosions
    burst(d, x + w * 0.48, y + h * 0.42, 13, (255, 170, 40))
    burst(d, x + w * 0.48, y + h * 0.42, 7, (255, 220, 120))
    burst(d, x + w * 0.82, y + h * 0.52, 9, (255, 140, 30))


def scene_missile(d, x, y, w, h):
    """Lead 3: a missile climbing under a red warning sky."""
    d.rectangle([x, y, x + w, y + h], fill=SKY_RED)
    for sx in (0.08, 0.30, 0.55, 0.78, 0.94):
        d.ellipse([x + w * sx, y + 8, x + w * sx + 3, y + 11], fill=(255, 220, 180))
    # smoke trail
    d.polygon([(x + w * 0.42, y + h), (x + w * 0.52, y + h), (x + w * 0.47, y + h * 0.45)], fill=(200, 190, 180))
    # missile body, angled up
    mx, my = x + w * 0.44, y + h * 0.30
    d.polygon([(mx, my - 26), (mx + 7, my - 12), (mx + 7, my + 22), (mx, my + 28), (mx - 7, my + 22), (mx - 7, my - 12)], fill=WHITE)
    d.polygon([(mx - 7, my + 18), (mx - 15, my + 30), (mx - 7, my + 24)], fill=(200, 200, 200))
    d.polygon([(mx + 7, my + 18), (mx + 15, my + 30), (mx + 7, my + 24)], fill=(200, 200, 200))
    burst(d, mx, my + 34, 12, (255, 170, 40))
    burst(d, mx, my + 34, 6, (255, 230, 140))
    # warning triangle
    tx, ty = x + w * 0.74, y + h * 0.30
    d.polygon([(tx, ty - 24), (tx + 24, ty + 16), (tx - 24, ty + 16)], fill=(255, 205, 0), outline=INK)
    f = SANS_B(24)
    d.text((tx - 3, ty - 8), "!", font=f, fill=INK)


def scene_refinery(d, x, y, w, h):
    """Picture 28: a refinery and a Riyadh tower struck at dusk."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 44, 62))
    d.ellipse([x + w * 0.72, y + 6, x + w * 0.72 + 26, y + 32], fill=(240, 200, 140))
    # refinery blocks
    d.rectangle([x + w * 0.06, y + h * 0.55, x + w * 0.42, y + h], fill=(28, 26, 32))
    d.rectangle([x + w * 0.10, y + h * 0.42, x + w * 0.14, y + h * 0.55], fill=(28, 26, 32))
    d.rectangle([x + w * 0.18, y + h * 0.36, x + w * 0.22, y + h * 0.55], fill=(28, 26, 32))
    d.rectangle([x + w * 0.28, y + h * 0.46, x + w * 0.36, y + h * 0.55], fill=(28, 26, 32))
    # flare stack flame
    burst(d, x + w * 0.20, y + h * 0.32, 10, (255, 170, 40))
    burst(d, x + w * 0.20, y + h * 0.32, 5, (255, 220, 120))
    # Riyadh tower (right)
    d.rectangle([x + w * 0.60, y + h * 0.30, x + w * 0.86, y + h], fill=(40, 38, 48))
    for wy in (0.38, 0.50, 0.62, 0.74, 0.86):
        d.rectangle([x + w * 0.64, y + h * wy, x + w * 0.82, y + h * wy + 4], fill=(255, 210, 110))
    burst(d, x + w * 0.73, y + h * 0.22, 11, (255, 150, 30))
    # smoke
    d.ellipse([x + w * 0.44, y + h * 0.18, x + w * 0.58, y + h * 0.30], fill=(120, 110, 120))
    d.ellipse([x + w * 0.52, y + h * 0.12, x + w * 0.64, y + h * 0.22], fill=(140, 130, 130))


def scene_drone(d, x, y, w, h):
    """Picture 29: an FPV quadcopter over desert, a military vehicle below."""
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(238, 214, 170))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(217, 179, 128))
    d.ellipse([x + w * 0.80, y + 8, x + w * 0.80 + 24, y + 32], fill=(250, 200, 90))
    # dunes
    d.polygon([(x, y + h * 0.72), (x + w * 0.35, y + h * 0.58), (x + w * 0.7, y + h * 0.72), (x + w, y + h * 0.62), (x + w, y + h), (x, y + h)], fill=(198, 158, 104))
    # military vehicle
    vx, vy = x + w * 0.12, y + h * 0.78
    d.rectangle([vx, vy, vx + w * 0.34, vy + 12], fill=(64, 70, 52))
    d.rectangle([vx + w * 0.06, vy - 8, vx + w * 0.22, vy], fill=(64, 70, 52))
    d.ellipse([vx + 4, vy + 10, vx + 14, vy + 20], fill=INK)
    d.ellipse([vx + w * 0.34 - 14, vy + 10, vx + w * 0.34 - 4, vy + 20], fill=INK)
    # quadcopter
    cx, cy = x + w * 0.62, y + h * 0.38
    d.line([cx - 26, cy - 14, cx + 26, cy + 14], fill=(40, 40, 44), width=3)
    d.line([cx - 26, cy + 14, cx + 26, cy - 14], fill=(40, 40, 44), width=3)
    d.ellipse([cx - 10, cy - 7, cx + 10, cy + 7], fill=(40, 40, 44))
    for rx, ry in [(-26, -14), (26, 14), (-26, 14), (26, -14)]:
        d.ellipse([cx + rx - 9, cy + ry - 3, cx + rx + 9, cy + ry + 3], fill=(120, 120, 130))
    d.line([cx, cy + 7, cx - 8, vy - 4], fill=(200, 60, 40), width=2)


def scene_tanker(d, x, y, w, h):
    """Picture 30: an oil tanker burning on a grey sea."""
    d.rectangle([x, y, x + w, y + h], fill=(70, 88, 96))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(30, 52, 64))
    for wy in (0.70, 0.80, 0.90):
        d.line([x + 6, y + h * wy, x + w - 6, y + h * wy], fill=(110, 140, 150), width=2)
    # tanker hull
    hx, hy = x + w * 0.08, y + h * 0.56
    d.polygon([(hx, hy + 16), (hx + w * 0.78, hy + 16), (hx + w * 0.72, hy), (hx + w * 0.06, hy)], fill=(24, 26, 30))
    d.rectangle([hx + w * 0.58, hy - 16, hx + w * 0.70, hy], fill=(220, 220, 220))
    d.rectangle([hx + w * 0.60, hy - 24, hx + w * 0.66, hy - 16], fill=(220, 220, 220))
    # fire + smoke over the deck
    burst(d, x + w * 0.34, y + h * 0.44, 14, (255, 160, 30))
    burst(d, x + w * 0.34, y + h * 0.44, 8, (255, 215, 110))
    d.ellipse([x + w * 0.26, y + h * 0.16, x + w * 0.40, y + h * 0.30], fill=(60, 58, 60))
    d.ellipse([x + w * 0.34, y + h * 0.08, x + w * 0.48, y + h * 0.22], fill=(80, 78, 80))
    # small second vessel
    d.polygon([(x + w * 0.82, y + h * 0.66), (x + w * 0.96, y + h * 0.66), (x + w * 0.93, y + h * 0.58), (x + w * 0.85, y + h * 0.58)], fill=(44, 48, 54))


def scene_reef(d, x, y, w, h):
    """Picture 15: Acropora corals revived on the reef."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 90, 120))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(10, 60, 84))
    # light rays
    for rx in (0.15, 0.45, 0.75):
        d.polygon([(x + w * rx, y), (x + w * rx + 14, y), (x + w * rx - 10, y + h * 0.7), (x + w * rx - 24, y + h * 0.7)], fill=(40, 130, 160))
    # coral branches
    def coral(cx, base, col, scale=1.0):
        for dx, dy, ln in [(-14, -26, 3), (-6, -34, 3), (0, -40, 4), (8, -30, 3), (16, -22, 3)]:
            d.line([cx, base, cx + dx * scale, base + dy * scale], fill=col, width=4)
            d.ellipse([cx + dx * scale - 3, base + dy * scale - 3, cx + dx * scale + 3, base + dy * scale + 3], fill=col)
    coral(x + w * 0.22, y + h * 0.92, (255, 140, 150))
    coral(x + w * 0.55, y + h * 0.95, (255, 180, 90), 1.2)
    coral(x + w * 0.82, y + h * 0.90, (255, 110, 130), 0.9)
    # fish
    for fx, fy, fc in [(0.30, 0.30, (255, 210, 80)), (0.68, 0.42, (255, 255, 255)), (0.48, 0.22, (255, 160, 60))]:
        px, py = x + w * fx, y + h * fy
        d.ellipse([px - 9, py - 5, px + 9, py + 5], fill=fc)
        d.polygon([(px + 8, py), (px + 15, py - 5), (px + 15, py + 5)], fill=fc)
    # bubbles
    for bx, by, br in [(0.12, 0.55, 3), (0.20, 0.40, 2), (0.88, 0.30, 3), (0.78, 0.55, 2)]:
        d.ellipse([x + w * bx - br, y + h * by - br, x + w * bx + br, y + h * by + br], outline=(200, 230, 240), width=1)


def scene_cricket(d, x, y, w, h):
    """Picture 12: a batsman mid-swing on a green outfield."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 140, 70))
    d.ellipse([x - w * 0.2, y + h * 0.55, x + w * 1.2, y + h * 1.25], fill=(84, 168, 92))
    d.rectangle([x + w * 0.42, y + h * 0.42, x + w * 0.58, y + h], fill=(214, 192, 150))
    # stumps
    for sx in (0.60, 0.635, 0.67):
        d.rectangle([x + w * sx, y + h * 0.52, x + w * sx + 3, y + h * 0.66], fill=(240, 220, 140))
    d.rectangle([x + w * 0.60, y + h * 0.50, x + w * 0.673, y + h * 0.53], fill=(240, 220, 140))
    # batsman: legs, shirt, head, bat
    bx, by = x + w * 0.30, y + h * 0.62
    d.line([bx, by, bx - 8, y + h * 0.92], fill=INK, width=5)
    d.line([bx, by, bx + 10, y + h * 0.92], fill=INK, width=5)
    d.polygon([(bx - 10, by), (bx + 10, by), (bx + 8, by - 26), (bx - 8, by - 26)], fill=WHITE)
    d.ellipse([bx - 7, by - 38, bx + 7, by - 24], fill=(210, 170, 130))
    d.line([bx + 8, by - 20, bx + 30, by - 48], fill=(120, 80, 40), width=5)
    d.rectangle([bx + 28, by - 52, bx + 36, by - 34], fill=(150, 105, 50))
    # red ball flying
    d.ellipse([x + w * 0.80 - 5, y + h * 0.24 - 5, x + w * 0.80 + 5, y + h * 0.24 + 5], fill=RED)
    d.arc([x + w * 0.68, y + h * 0.16, x + w * 0.92, y + h * 0.40], 200, 340, fill=WHITE, width=2)


def scene_fire(d, x, y, w, h):
    """Picture 42: a fuel tanker burning on a ring road at night."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 22, 34))
    d.ellipse([x + w * 0.78, y + 6, x + w * 0.78 + 22, y + 28], fill=(220, 210, 190))
    # road
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=(40, 40, 48))
    d.line([x + 6, y + h * 0.82, x + w - 6, y + h * 0.82], fill=(220, 200, 90), width=2)
    # tanker truck, tipped
    hx, hy = x + w * 0.14, y + h * 0.56
    d.polygon([(hx, hy + 14), (hx + w * 0.52, hy + 14), (hx + w * 0.48, hy), (hx + w * 0.06, hy)], fill=(180, 60, 40))
    d.ellipse([hx + w * 0.10, hy + 10, hx + w * 0.10 + 12, hy + 22], fill=INK)
    d.ellipse([hx + w * 0.40, hy + 10, hx + w * 0.40 + 12, hy + 22], fill=INK)
    # big fire + smoke
    burst(d, x + w * 0.44, y + h * 0.44, 16, (255, 150, 20))
    burst(d, x + w * 0.44, y + h * 0.44, 9, (255, 220, 110))
    d.ellipse([x + w * 0.30, y + h * 0.10, x + w * 0.48, y + h * 0.28], fill=(70, 66, 70))
    d.ellipse([x + w * 0.42, y + h * 0.04, x + w * 0.58, y + h * 0.20], fill=(90, 86, 90))
    # distant cars
    for cx in (0.70, 0.84):
        d.rectangle([x + w * cx, y + h * 0.70, x + w * cx + 16, y + h * 0.78], fill=(200, 200, 210))


def scene_rocket(d, x, y, w, h):
    """Picture 43: Shenzhou-24 lifts off on a Long March-2F."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 44, 88))
    for sx in (0.10, 0.34, 0.62, 0.86):
        d.ellipse([x + w * sx, y + 8, x + w * sx + 3, y + 11], fill=WHITE)
    # launch tower
    d.rectangle([x + w * 0.12, y + h * 0.30, x + w * 0.20, y + h], fill=(60, 66, 80))
    for ty in (0.38, 0.52, 0.66, 0.80):
        d.rectangle([x + w * 0.12, y + h * ty, x + w * 0.20, y + h * ty + 3], fill=(120, 130, 150))
    # rocket body
    rx = x + w * 0.52
    d.polygon([(rx, y + h * 0.10), (rx + 9, y + h * 0.18), (rx + 9, y + h * 0.58), (rx, y + h * 0.64), (rx - 9, y + h * 0.58), (rx - 9, y + h * 0.18)], fill=WHITE)
    d.rectangle([rx - 9, y + h * 0.30, rx + 9, y + h * 0.36], fill=RED)
    d.polygon([(rx - 9, y + h * 0.58), (rx - 17, y + h * 0.70), (rx - 9, y + h * 0.66)], fill=(200, 200, 200))
    d.polygon([(rx + 9, y + h * 0.58), (rx + 17, y + h * 0.70), (rx + 9, y + h * 0.66)], fill=(200, 200, 200))
    # flame + smoke
    burst(d, rx, y + h * 0.78, 13, (255, 170, 40))
    burst(d, rx, y + h * 0.78, 7, (255, 230, 140))
    d.ellipse([x + w * 0.30, y + h * 0.82, x + w * 0.52, y + h * 0.98], fill=(200, 200, 210))
    d.ellipse([x + w * 0.48, y + h * 0.86, x + w * 0.72, y + h], fill=(180, 180, 190))


def scene_pact(d, x, y, w, h):
    """Picture 40: two flags and a signed pact document."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 228, 214))
    # flag poles
    d.line([x + w * 0.22, y + h * 0.14, x + w * 0.22, y + h * 0.72], fill=INK, width=3)
    d.line([x + w * 0.78, y + h * 0.14, x + w * 0.78, y + h * 0.72], fill=INK, width=3)
    # Australia flag (blue, stars)
    d.rectangle([x + w * 0.22, y + h * 0.14, x + w * 0.46, y + h * 0.40], fill=(0, 40, 120))
    d.ellipse([x + w * 0.30, y + h * 0.22, x + w * 0.30 + 8, y + h * 0.22 + 8], fill=WHITE)
    d.ellipse([x + w * 0.38, y + h * 0.30, x + w * 0.38 + 6, y + h * 0.30 + 6], fill=WHITE)
    # Solomons flag (blue/green, yellow diagonal, stars)
    d.polygon([(x + w * 0.54, y + h * 0.14), (x + w * 0.78, y + h * 0.14), (x + w * 0.78, y + h * 0.40), (x + w * 0.54, y + h * 0.40)], fill=(0, 90, 160))
    d.polygon([(x + w * 0.54, y + h * 0.40), (x + w * 0.78, y + h * 0.14), (x + w * 0.78, y + h * 0.40)], fill=(0, 130, 60))
    d.line([x + w * 0.54, y + h * 0.40, x + w * 0.78, y + h * 0.14], fill=(255, 210, 0), width=3)
    # document
    d.rectangle([x + w * 0.30, y + h * 0.62, x + w * 0.70, y + h * 0.94], fill=WHITE, outline=INK)
    for ly in (0.68, 0.76, 0.84):
        d.line([x + w * 0.34, y + h * ly, x + w * 0.66, y + h * ly], fill=(150, 150, 150), width=1)
    d.ellipse([x + w * 0.60, y + h * 0.88, x + w * 0.60 + 7, y + h * 0.88 + 7], fill=RED)


def scene_flags(d, x, y, w, h):
    """Picture 39: Brazil and Argentina flags, a diplomatic break."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 232, 216))
    # Brazil flag (green, yellow diamond, blue globe)
    d.rectangle([x + w * 0.08, y + h * 0.18, x + w * 0.46, y + h * 0.52], fill=(0, 140, 60))
    d.polygon([(x + w * 0.27, y + h * 0.22), (x + w * 0.42, y + h * 0.35), (x + w * 0.27, y + h * 0.48), (x + w * 0.12, y + h * 0.35)], fill=(255, 210, 0))
    d.ellipse([x + w * 0.22, y + h * 0.28, x + w * 0.32, y + h * 0.42], fill=(0, 50, 160))
    # Argentina flag (light blue / white / light blue, sun)
    d.rectangle([x + w * 0.54, y + h * 0.18, x + w * 0.92, y + h * 0.52], fill=(120, 200, 235))
    d.rectangle([x + w * 0.54, y + h * 0.29, x + w * 0.92, y + h * 0.41], fill=WHITE)
    d.ellipse([x + w * 0.69, y + h * 0.30, x + w * 0.77, y + h * 0.40], fill=(255, 200, 60))
    # a crack between them
    d.line([x + w * 0.50, y + h * 0.12, x + w * 0.50, y + h * 0.58], fill=RED, width=3)
    d.line([x + w * 0.48, y + h * 0.30, x + w * 0.52, y + h * 0.34], fill=RED, width=2)
    # embassy door, closed
    d.rectangle([x + w * 0.38, y + h * 0.66, x + w * 0.62, y + h * 0.94], fill=(120, 90, 60), outline=INK)
    d.ellipse([x + w * 0.56, y + h * 0.78, x + w * 0.56 + 5, y + h * 0.78 + 5], fill=GOLD)


def scene_market(d, x, y, w, h):
    """Picture 48: a Cartagena supermarket, police lights outside."""
    d.rectangle([x, y, x + w, y + h], fill=(70, 90, 130))
    d.ellipse([x + w * 0.80, y + 6, x + w * 0.80 + 22, y + 28], fill=(240, 220, 170))
    # supermarket block
    d.rectangle([x + w * 0.08, y + h * 0.34, x + w * 0.92, y + h * 0.88], fill=(245, 240, 225))
    # awning stripes
    for i in range(6):
        col = RED if i % 2 == 0 else WHITE
        d.rectangle([x + w * (0.08 + i * 0.14), y + h * 0.34, x + w * (0.08 + (i + 1) * 0.14), y + h * 0.46], fill=col)
    # glass doors
    d.rectangle([x + w * 0.38, y + h * 0.52, x + w * 0.62, y + h * 0.88], fill=(170, 205, 225), outline=INK)
    d.line([x + w * 0.50, y + h * 0.52, x + w * 0.50, y + h * 0.88], fill=INK, width=2)
    # police car + lights
    d.rectangle([x + w * 0.68, y + h * 0.78, x + w * 0.92, y + h * 0.90], fill=(30, 40, 60))
    d.ellipse([x + w * 0.72, y + h * 0.88, x + w * 0.72 + 8, y + h * 0.88 + 8], fill=INK)
    d.ellipse([x + w * 0.86, y + h * 0.88, x + w * 0.86 + 8, y + h * 0.88 + 8], fill=INK)
    burst(d, x + w * 0.80, y + h * 0.72, 8, (255, 60, 60))
    burst(d, x + w * 0.80, y + h * 0.72, 4, (80, 140, 255))


def scene_geothermal(d, x, y, w, h):
    """Picture 50: steam vents over the Rift Valley at Olkaria."""
    d.rectangle([x, y, x + w, y + h * 0.55], fill=(150, 190, 220))
    d.rectangle([x, y + h * 0.55, x + w, y + h], fill=(90, 140, 70))
    d.ellipse([x + w * 0.78, y + 8, x + w * 0.78 + 24, y + 32], fill=(255, 220, 110))
    # hills
    d.polygon([(x, y + h * 0.72), (x + w * 0.30, y + h * 0.50), (x + w * 0.62, y + h * 0.70), (x + w, y + h * 0.56), (x + w, y + h), (x, y + h)], fill=(70, 120, 60))
    # power plant blocks
    d.rectangle([x + w * 0.10, y + h * 0.66, x + w * 0.30, y + h * 0.86], fill=(220, 220, 225))
    d.rectangle([x + w * 0.16, y + h * 0.58, x + w * 0.20, y + h * 0.66], fill=(200, 200, 205))
    # steam columns
    for sx in (0.42, 0.60, 0.76):
        d.ellipse([x + w * sx, y + h * 0.22, x + w * sx + 16, y + h * 0.42], fill=(240, 244, 248))
        d.ellipse([x + w * sx + 4, y + h * 0.12, x + w * sx + 20, y + h * 0.30], fill=(250, 252, 255))
    # pipes
    d.line([x + w * 0.30, y + h * 0.76, x + w * 0.42, y + h * 0.76], fill=(90, 90, 100), width=3)
    d.line([x + w * 0.30, y + h * 0.82, x + w * 0.60, y + h * 0.82], fill=(90, 90, 100), width=3)


def scene_lab(d, x, y, w, h):
    """Picture 44: brain organoids in a dish, under stars."""
    d.rectangle([x, y, x + w, y + h], fill=(20, 28, 52))
    for sx in (0.08, 0.26, 0.48, 0.70, 0.88):
        d.ellipse([x + w * sx, y + 8, x + w * sx + 3, y + 11], fill=WHITE)
    # space station arc
    d.arc([x - w * 0.2, y - h * 0.3, x + w * 1.1, y + h * 0.5], 20, 160, fill=(180, 190, 210), width=4)
    # petri dish
    cx, cy = x + w * 0.50, y + h * 0.58
    d.ellipse([cx - 34, cy - 20, cx + 34, cy + 20], fill=(220, 230, 240), outline=(150, 160, 180))
    d.ellipse([cx - 30, cy - 16, cx + 30, cy + 16], fill=(180, 200, 230))
    # organoids (small pink spheres)
    for ox, oy, r in [(-16, -6, 7), (6, -10, 8), (16, 4, 6), (-4, 8, 7)]:
        d.ellipse([cx + ox - r, cy + oy - r, cx + ox + r, cy + oy + r], fill=(255, 150, 180), outline=(200, 90, 130))
    # flask
    d.polygon([(x + w * 0.12, y + h * 0.78), (x + w * 0.20, y + h * 0.78), (x + w * 0.16, y + h * 0.62), (x + w * 0.12, y + h * 0.62)], fill=(200, 220, 240), outline=INK)
    d.ellipse([x + w * 0.12, y + h * 0.78, x + w * 0.20, y + h * 0.86], fill=(120, 180, 220))


SCENES = {1: scene_cemetery, 2: scene_ships, 3: scene_missile,
          28: scene_refinery, 29: scene_drone, 30: scene_tanker,
          15: scene_reef, 12: scene_cricket,
          42: scene_fire, 43: scene_rocket, 40: scene_pact,
          39: scene_flags, 48: scene_market, 50: scene_geothermal,
          44: scene_lab}


# --- dotted world map ------------------------------------------------------------
def dotted_map(d, x, y, w, h, pins):
    """A dot-matrix world map. Land blobs are ellipses in map-local coords."""
    blobs = [  # (cx, cy, rx, ry) in a 600x90 local frame
        (90, 24, 72, 22), (150, 66, 34, 19),      # Americas
        (308, 16, 46, 14), (318, 54, 40, 27),     # Europe, Africa
        (452, 20, 92, 19), (520, 66, 46, 14),     # Asia, SE Asia/Australia
    ]
    step = 9
    for gy in range(0, h, step):
        for gx in range(0, w, step):
            lx = gx / w * 600
            ly = gy / h * 90
            land = any(((lx - cx) / rx) ** 2 + ((ly - cy) / ry) ** 2 <= 1
                       for cx, cy, rx, ry in blobs)
            if land:
                d.ellipse([x + gx, y + gy, x + gx + 3, y + gy + 3], fill=(52, 68, 96))
    for num, px, py in pins:
        ax, ay = x + px / 600 * w, y + py / 90 * h
        badge(d, ax, ay, 9, num)


# --- layout ----------------------------------------------------------------------
MARGIN = 20
CW = W - 2 * MARGIN  # 984 usable


def rule(d, x, y, w, color=RED, h=2):
    d.rectangle([x, y, x + w, y + h], fill=color)


def section_head(d, x, y, text, color=RED):
    d.text((x, y), text, font=SANS_B(13), fill=color)
    return y + 15


def draw_poster():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0

    # top bar
    d.rectangle([0, 0, W, 26], fill=NAVY)
    d.text((MARGIN, 5), "THE WORLD IN ONE DAY", font=SANS_B(15), fill=GOLD)
    right = "50 STORIES  ·  8 REGIONS  ·  18 FIELDS"
    d.text((W - MARGIN - d.textlength(right, font=SANS_B(13)), 6), right,
           font=SANS_B(13), fill=WHITE)
    y = 26

    # masthead
    d.text((MARGIN, y + 5), "Wednesday 25 November 2026", font=SERIF_B(40), fill=INK)
    y += 58
    rule(d, MARGIN, y, CW, RED, 4)
    y += 7
    sub = ("720,000 Russian dead, one every 4 minutes  ·  Zelensky confirms the Gulf "
           "strike  ·  Medvedev threatens nuclear attack")
    d.text((MARGIN, y), sub, font=SANS(16), fill=(60, 60, 60))
    y += 19

    # the war at sea — ships strip
    d.rectangle([0, y, W, y + 40], fill=NAVY)
    d.text((MARGIN, y + 4), "THE WAR AT SEA", font=SANS_B(13), fill=GOLD)
    d.text((MARGIN, y + 20), "5 SHIPS IN 12 DAYS", font=SANS_B(13), fill=WHITE)
    col_w = (W - 190) // 5
    for i, (dt, name, status, loc) in enumerate(SHIPS):
        cx = 190 + i * col_w
        d.text((cx, y + 3), dt, font=SANS_B(11), fill=GOLD)
        d.text((cx, y + 16), name, font=SANS_B(12), fill=WHITE)
        d.text((cx, y + 29), f"{status}, {loc}", font=SANS(11), fill=GRAY_LT)
    y += 40

    # the day in numbers
    y += 4
    y = section_head(d, MARGIN, y, "THE DAY IN NUMBERS")
    cell = CW // 6
    for i, (big, label) in enumerate(NUMBERS):
        cx = MARGIN + i * cell
        d.text((cx, y), big, font=SERIF_B(26), fill=RED)
        d.text((cx, y + 32), label, font=SANS(12), fill=GRAY)
        if i:
            d.line([cx - 8, y + 2, cx - 8, y + 38], fill=(200, 190, 170), width=1)
    y += 44

    # three lead cards
    y += 4
    gap = 12
    card_w = (CW - 2 * gap) // 3
    lead_titles = [(1, "1 RUSSIA · THE HUMAN COST"), (2, "2 GULF OF FINLAND · WAR AT SEA"),
                   (3, "3 MOSCOW · ESCALATION")]
    lead_y = y
    for i, st in enumerate(STORIES[:3]):
        num, region, head, cap = st
        cx = MARGIN + i * (card_w + gap)
        d.rectangle([cx, lead_y, cx + card_w, lead_y + 26], fill=RED)
        badge(d, cx + 14, lead_y + 13, 10, num)
        d.text((cx + 30, lead_y + 6), lead_titles[i][1], font=SANS_B(12), fill=WHITE)
        SCENES[num](d, cx, lead_y + 26, card_w, 72)
        hy = lead_y + 26 + 72 + 4
        hy = text_block(d, cx, hy, head, SERIF_B(26), INK, card_w, 25, max_lines=2)
        text_block(d, cx, hy + 2, cap, SANS(12), (60, 60, 60), card_w, 12, max_lines=2)
    y = lead_y + 26 + 72 + 4 + 50 + 24

    # the rest of the day
    y += 3
    y = section_head(d, MARGIN, y, "THE REST OF THE DAY")
    rule(d, MARGIN, y, CW, RED, 1)
    y += 4
    rest = STORIES[3:13]
    for col in (0, 1):
        col_x = MARGIN + col * (CW // 2 + 10)
        cy = y
        for st in rest[col * 5:(col + 1) * 5]:
            num, region, head, cap = st
            badge(d, col_x + 9, cy + 8, 9, num)
            d.text((col_x + 24, cy), head, font=SANS_B(15), fill=INK)
            rw = region
            d.text((col_x + CW // 2 - 10 - d.textlength(rw, font=SANS(11)), cy + 2),
                   rw, font=SANS(11), fill=GRAY)
            d.text((col_x + 24, cy + 16), cap, font=SANS(12), fill=GRAY)
            cy += 29
    y += 5 * 29 + 4

    # the day in pictures — twelve new full scenes, two rows of six
    y = section_head(d, MARGIN, y, "THE DAY IN PICTURES — 12 SCENES DRAWN IN CODE")
    rule(d, MARGIN, y, CW, RED, 1)
    y += 4
    pic_w = (CW - 5 * 10) // 6
    for row in (0, 1):
        for i, (num, cap) in enumerate(PICTURES[row * 6:(row + 1) * 6]):
            px = MARGIN + i * (pic_w + 10)
            SCENES[num](d, px, y, pic_w, 44)
            badge(d, px + 9, y + 44 + 10, 7, num)
            text_block(d, px + 20, y + 44 + 3, cap, SANS(11), INK, pic_w - 20, 12, max_lines=2)
        y += 44 + 20
    y += 1

    # the day on a clock — UTC timeline of the biggest moments
    y = section_head(d, MARGIN, y, "THE DAY ON A CLOCK — UTC")
    tl_y = y + 2
    d.line([MARGIN, tl_y + 6, W - MARGIN, tl_y + 6], fill=(52, 68, 96), width=2)
    TIMELINE = [
        ("00:00", "Cairo tanker fire"),
        ("04:00", "Gaza toll 74,746"),
        ("08:00", "Shenzhou-24 lifts off"),
        ("12:00", "Solomons pact signed"),
        ("16:00", "Brazil recalls envoy"),
        ("20:00", "Medvedev threat"),
    ]
    for i, (hh, label) in enumerate(TIMELINE):
        tx = MARGIN + i * (CW // 5)
        d.ellipse([tx - 4, tl_y + 2, tx + 4, tl_y + 10], fill=RED, outline=WHITE)
        # time label: left-aligned, except the last one which is right-aligned
        if i == len(TIMELINE) - 1:
            d.text((W - MARGIN - d.textlength(hh, font=SANS_B(10)), tl_y + 12), hh, font=SANS_B(10), fill=INK)
            d.text((W - MARGIN - d.textlength(label, font=SANS(10)), tl_y + 22), label, font=SANS(10), fill=GRAY)
        else:
            d.text((tx - 2, tl_y + 12), hh, font=SANS_B(10), fill=INK)
            d.text((tx - 2, tl_y + 22), label, font=SANS(10), fill=GRAY)
    y = tl_y + 32

    # stories by region — compact horizontal band (8 regions)
    y += 1
    y = section_head(d, MARGIN, y, "STORIES BY REGION")
    counts = {}
    for _, region, _, _ in STORIES:
        counts[region] = counts.get(region, 0) + 1
    maxc = max(counts.values())
    cell_w = CW // 8
    for i, rk in enumerate(REGION_KEYS):
        c = counts.get(rk, 0)
        bx = MARGIN + i * cell_w
        label = {"N. AMERICA": "N. America", "S. AMERICA": "S. America"}.get(rk, rk.title())
        d.text((bx, y), label, font=SANS_B(11), fill=INK)
        bar_w = int((cell_w - 28) * c / maxc)
        d.rectangle([bx, y + 14, bx + bar_w, y + 23], fill=REGION_COLORS[rk])
        d.text((bx + bar_w + 4, y + 13), str(c), font=SANS_B(12), fill=INK)
    y += 26

    # also on — the remaining stories, three columns
    y = section_head(d, MARGIN, y, "ALSO ON WEDNESDAY 25 NOVEMBER — 37 MORE STORIES")
    rule(d, MARGIN, y, CW, RED, 1)
    y += 4
    rest2 = STORIES[13:]
    per_col = (len(rest2) + 2) // 3
    col_w = CW // 3
    for col in (0, 1, 2):
        col_x = MARGIN + col * col_w
        cy = y
        for st in rest2[col * per_col:(col + 1) * per_col]:
            num, region, head, cap = st
            line = f"{num}. {head}"
            d.text((col_x, cy), line, font=SANS(11), fill=INK)
            cy += 11
    y += per_col * 11 + 4

    # date check
    d.rectangle([MARGIN, y, W - MARGIN, y + 14], outline=RED, width=1)
    d.text((MARGIN + 6, y + 2), "DATE CHECK — Today's news is the fallout, not the rally: COP31 (Sun) · Nvidia +31.5% (Mon) · Huang reinstated (Mon).", font=SANS_B(12), fill=INK)
    y += 14

    # markets bar
    d.rectangle([0, y, W, y + 22], fill=NAVY)
    d.text((MARGIN, y + 4), "MARKETS · MORNING SNAPSHOT", font=SANS_B(12), fill=GOLD)
    mk = "Gold ~$3,620     NVDA down >3% premarket"
    d.text((W - MARGIN - d.textlength(mk, font=SANS_B(12)), y + 4), mk,
           font=SANS_B(12), fill=WHITE)
    y += 22

    # footer
    d.text((MARGIN, y + 2), "FIELDS — " + FIELDS, font=SANS(10), fill=GRAY)
    d.text((MARGIN, y + 12), SOURCES, font=SANS(10), fill=GRAY)
    pt = "PRESS TIME 09:00 UTC"
    d.text((W - MARGIN - d.textlength(pt, font=SANS_B(10)), y + 12), pt,
           font=SANS_B(10), fill=INK)
    y += 19
    return img, y


def main():
    img, final_y = draw_poster()
    if final_y > H:
        print(f"WARNING: layout overflow, final y={final_y} > {H}", file=sys.stderr)
    img.save(OUT, format="PNG", optimize=True)
    data = open(OUT, "rb").read()
    print(f"wrote {OUT}  {len(data)} bytes  sha256={hashlib.sha256(data).hexdigest()[:16]}  final_y={final_y}")


if __name__ == "__main__":
    main()
