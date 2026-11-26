#!/usr/bin/env python3
"""Wednesday 25 November 2026 — one-page newspaper, drawn from scratch.
Render: python3 build-image.py  ->  entry.png (1024 x 1024, no network).
All pictures are drawn in code; all text is set in code below.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 244, 228)
INK = (18, 22, 32)
NAVY = (16, 38, 74)
NAVY2 = (24, 58, 108)
RED = (178, 34, 28)
GOLD = (196, 148, 44)
GREY = (90, 92, 98)
LINE = (178, 168, 142)
CREAM2 = (242, 233, 210)

def font(sz, bold=False, serif=False):
    base = "/usr/share/fonts/truetype/dejavu/"
    name = "DejaVuSerif-Bold.ttf" if serif else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    try:
        return ImageFont.truetype(base + name, sz)
    except Exception:
        return ImageFont.load_default()

def wrap(draw, txt, fnt, maxw, maxlines=3):
    words = txt.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
            if len(lines) >= maxlines:
                break
    if cur and len(lines) < maxlines:
        lines.append(cur)
    if len(lines) == maxlines and words:
        joined = " ".join(lines)
        if len(joined) < len(txt):
            lines[-1] = lines[-1].rstrip() + "…"
    return lines

def para(draw, x, y, txt, fnt, maxw, maxlines=3, fill=INK, lh=None):
    lines = wrap(draw, txt, fnt, maxw, maxlines)
    step = lh or int(fnt.size * 1.18)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y

def centred(draw, cx, y, txt, fnt, fill):
    draw.text((cx - draw.textlength(txt, font=fnt) / 2, y), txt, font=fnt, fill=fill)

# ---------------------------------------------------------------- data
ITEMS = [
    (1, "EUROPE", "720,000 RUSSIAN DEAD", "490,000 confirmed by Rosstat; one death every 4 minutes since 2022, leaked data show."),
    (2, "EUROPE", "FIVE SHIPS HIT IN 12 DAYS", "Zelensky confirms the Gulf strike on Sparta II; Merkury sunk off Benghazi."),
    (3, "EUROPE", "MEDVEDEV THREATENS NUCLEAR STRIKE", "'Preventive nuclear attack' threat; Putin calls retaliation 'inevitable' as Kyiv holds on."),
    (4, "N. AMERICA", "Trump pardons turkeys 'Freedom' + 'Feathers'", "Thanksgiving pardon at the White House."),
    (5, "N. AMERICA", "Giuliani gets Medal of Freedom", "Trump honours the former New York mayor."),
    (6, "N. AMERICA", "Abrego Garcia to leave US voluntarily", "Salvadoran migrant agrees to depart."),
    (7, "EUROPE", "Sarkozy corruption trial set", "Pretrial hearing 1 Apr 2027 in Paris."),
    (8, "N. AMERICA", "FAA radar fault delays Chicago flights", "Disruption hits O'Hare departures."),
    (9, "MIDDLE EAST", "Houthis 60 km from Aden", "Yemen military: 'Aden will not fall.'"),
    (10, "N. AMERICA", "Fort Hood shooter seeks execution delay", "Hasan asks court to postpone sentence."),
    (11, "ASIA", "BJP + Akali Dal ally for Punjab 2027", "Pact sealed for the state election."),
    (12, "GLOBAL", "England beat Australia by 8 wickets", "2nd T20I, chasing 185."),
    (13, "ASIA", "RFE/RL returns to shortwave", "Back on air for Afghan girls' schooling."),
    (14, "EUROPE", "Denmark upholds ghetto evictions", "Supreme Court backs the evictions."),
    (15, "ASIA", "Great Barrier Reef: 12 species revived", "Acropora corals brought back."),
    (16, "MIDDLE EAST", "Israel military suicides at 16-year high", "Highest toll in 16 years."),
    (17, "EUROPE", "EU 22nd sanctions package", "60 banks cut from SWIFT, 70+ shadow-fleet ships."),
    (18, "EUROPE", "NATO AWACS to Poland", "After 3 Kh-101 missiles fell 20 Nov."),
    (19, "EUROPE", "Zaporizhzhia strike, 11 civilians hurt", "Guided-bomb attack at dawn."),
    (20, "MIDDLE EAST", "Gaza death toll 74,746", "WAFA toll; 266M face acute food insecurity."),
    (21, "GLOBAL", "266 million face acute food insecurity", "WFP: worst hunger crisis on record."),
    (22, "ASIA", "Nepal PM Balendra Shah visits India", "State visit to New Delhi."),
    (23, "GLOBAL", "Gold near $3,620 in Asia", "Safe-haven buying lifts bullion."),
    (24, "GLOBAL", "GTA 6 still topping charts", "A week after its 19 Nov launch."),
    (25, "GLOBAL", "Nvidia cools; NVDA down >3% premarket", "Rally fades after Huang's return."),
    (26, "EUROPE", "Russia calls ship attacks 'terrorism'", "Moscow blames Kyiv for the strikes."),
    (27, "EUROPE", "Lukashenko offers to fly Zelensky to Moscow", "Zelensky: 'Bring Putin to Kyiv.'"),
    (28, "MIDDLE EAST", "Houthis hit Saudi refinery + Riyadh tower", "Ras Tanura refinery struck; 11 hurt in Riyadh."),
    (29, "AFRICA", "Sahel drone war hits Russians", "Insurgents fly FPV drones vs Russian forces in Mali."),
    (30, "MIDDLE EAST", "Ships hit near Strait of Hormuz", "UKMTO logs projectile strikes; Iran claims mines."),
    (31, "ASIA", "China Politburo graft probe", "Shanghai chief Chen Jining investigated."),
    (32, "AFRICA", "Ramaphosa wins Farmgate court case", "Panel report set aside."),
    (33, "EUROPE", "Spain election debate — housing", "Sanchez vs Feijoo before 29 Nov vote."),
    (34, "GLOBAL", "Stocks tumble as AI rally fizzles", "Asia down; tariff threats loom."),
    (35, "MIDDLE EAST", "Jordan death sentence over officer killing", "State Security Court ruling."),
    (36, "EUROPE", "Russia extradites Chinese suspect", "$2.3B illegal-deposit case."),
    (37, "N. AMERICA", "Trump tariffs probe findings due", "Section 301 probe on 16 partners."),
    (38, "N. AMERICA", "US PCE inflation + Q3 GDP data due", "Two big releases before Thanksgiving."),
    (39, "S. AMERICA", "Brazil recalls envoy, bars Milei", "Ambassador pulled from Buenos Aires; Milei barred from Lula's 5 Jan inauguration."),
    (40, "OCEANIA", "Australia–Solomons sign security pact", "Canberra becomes defence partner of choice; $740M over 10 years; China pact lapses."),
    (41, "S. AMERICA", "Eni + Repsol pledge $2B in Venezuela", "Joint $2B over 5 years with PDVSA."),
    (42, "AFRICA", "Cairo tanker fire kills 31", "Fuel tanker overturns on Ring Road; 31 killed, 21 hurt, 27 vehicles charred."),
    (43, "ASIA", "Shenzhou-24 carries first Pakistani to space", "Muhammad Zeeshan Ali, first Pakistani in orbit, first foreigner on Tiangong."),
    (44, "N. AMERICA", "Brain organoids in space hint at Alzheimer's", "UC San Diego: 40 days on ISS, published 25 Nov in Science Advances."),
    (45, "AFRICA", "Pete Edochie dies at 79", "Nollywood's Okonkwo, 200+ films, prostate cancer."),
    (46, "AFRICA", "Ghana: AI must aid, not replace, teachers", "Deputy Education Minister on AI in schools."),
    (47, "GLOBAL", "Peatland drainage drove 2.7% of warming", "Nature study: drained peatlands behind 2.7% of human-caused warming."),
    (48, "S. AMERICA", "Colombia supermarket hostage siege ends", "20 held in Cartagena; 17-hour standoff, forces storm in."),
    (49, "ASIA", "Iwo Jima gains new volcanic land", "Eruption redraws part of the Japanese island."),
    (50, "AFRICA", "Olkaria I geothermal steams back to life", "Kenya's oldest geothermal station restarts."),
]
REGION_ORDER = ["EUROPE", "N. AMERICA", "ASIA", "MIDDLE EAST", "AFRICA", "S. AMERICA", "OCEANIA", "GLOBAL"]
REGION_COUNT = {"EUROPE": 12, "N. AMERICA": 8, "ASIA": 7, "MIDDLE EAST": 6, "AFRICA": 6, "S. AMERICA": 3, "OCEANIA": 1, "GLOBAL": 7}
FIELDS = ["Politics", "War/Security", "Climate", "Markets", "Health", "Science", "Sport", "Crime/Justice", "Diplomacy", "Tech/AI", "Energy", "Space", "Culture", "Education", "Environment", "Disaster", "Trade", "Migration"]
NUMBERS = [
    ("720,000", "Russian soldiers dead"),
    ("74,746", "Gaza death toll"),
    ("$740M", "Solomons pact"),
    ("$2B", "Venezuela pledge"),
    ("31", "Cairo fire dead"),
    ("2.7%", "peatland warming"),
]
SHIPS = [
    ("NOV 11", "Naro-Fominsk", "corvette, struck", "Gulf of Finland"),
    ("NOV 21", "Sparta II", "cargo ship, set ablaze", "Gulf of Finland"),
    ("NOV 21", "Ambal", "ferry, hit", "Gulf of Finland"),
    ("NOV 22", "Merkury", "corvette, sunk", "Benghazi"),
    ("NOV 22", "Angara", "cargo ship, hit", "Benghazi"),
]

# ------------------------------------------------------------- pictures
def scene_crosses(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 22, 48))
    d.ellipse([x + w - 34, y + 5, x + w - 12, y + 27], fill=(240, 238, 220))
    d.ellipse([x + w - 30, y + 8, x + w - 16, y + 22], fill=(14, 22, 48))
    for i in range(9):
        cx = x + 10 + (i % 3) * 22
        cy = y + h - 22 - (i // 3) * 12
        d.line([cx, cy - 8, cx, cy + 8], fill=(210, 205, 190), width=2)
        d.line([cx - 5, cy - 3, cx + 5, cy - 3], fill=(210, 205, 190), width=2)
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(40, 48, 70))

def scene_shipfire(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 18, 36))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(18, 48, 78))
    d.rectangle([x + 18, y + h - 32, x + w - 18, y + h - 16], fill=(30, 32, 38))
    d.rectangle([x + 34, y + h - 42, x + w - 44, y + h - 32], fill=(52, 54, 60))
    for j, (fx, fw, fh) in enumerate([(44, 14, 22), (62, 18, 28), (84, 12, 18)]):
        d.polygon([(x + fx, y + h - 32), (x + fx + fw // 2, y + h - 32 - fh), (x + fx + fw, y + h - 32)], fill=(242, 120, 30) if j != 1 else (255, 190, 40))
    d.ellipse([x + 8, y + 6, x + 26, y + 20], fill=(220, 220, 210))

def scene_rocket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 52, 96))
    for sx, sy in [(12, 10), (40, 22), (88, 8), (70, 30)]:
        d.ellipse([x + sx, y + sy, x + sx + 3, y + sy + 3], fill=(255, 255, 255))
    d.polygon([(x + w // 2, y + 6), (x + w // 2 - 7, y + 34), (x + w // 2 + 7, y + 34)], fill=(240, 240, 235))
    d.rectangle([x + w // 2 - 7, y + 34, x + w // 2 + 7, y + 48], fill=(220, 220, 215))
    d.polygon([(x + w // 2, y + 48), (x + w // 2 - 6, y + h - 8), (x + w // 2 + 6, y + h - 8)], fill=(255, 150, 30))
    d.ellipse([x + 10, y + h - 14, x + w - 10, y + h - 2], fill=(210, 210, 205))

def scene_reef(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 110, 130))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(210, 190, 140))
    for bx, col in [(16, (255, 120, 140)), (48, (255, 170, 80)), (80, (255, 110, 120))]:
        for k in range(3):
            d.line([x + bx + k * 6, y + h - 10, x + bx + k * 6 - 4, y + h - 34], fill=col, width=3)
    for fx, fy in [(20, 14), (70, 10), (95, 22)]:
        d.ellipse([x + fx, y + fy, x + fx + 10, y + fy + 5], fill=(255, 220, 60))

def scene_tanker(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 24, 16))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(60, 60, 60))
    d.rounded_rectangle([x + 20, y + h - 26, x + w - 20, y + h - 12], radius=5, fill=(150, 150, 150))
    for j, (fx, fw, fh) in enumerate([(30, 16, 26), (52, 20, 34), (76, 14, 22)]):
        d.polygon([(x + fx, y + h - 24), (x + fx + fw // 2, y + h - 24 - fh), (x + fx + fw, y + h - 24)], fill=(255, 90, 20) if j % 2 == 0 else (255, 180, 30))
    d.ellipse([x + 60, y + 4, x + 92, y + 22], fill=(90, 90, 90))

def scene_geo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 200))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(90, 140, 80))
    d.rectangle([x + 12, y + h - 30, x + w - 12, y + h - 14], fill=(120, 120, 120))
    for px in [26, 58, 90]:
        d.rectangle([x + px, y + 18, x + px + 8, y + h - 28], fill=(90, 90, 95))
    for cx, cy, r in [(30, 16, 10), (48, 10, 12), (80, 14, 11)]:
        d.ellipse([x + cx - r, y + cy - r // 2, x + cx + r, y + cy + r // 2], fill=(255, 255, 255))

SCENES = [
    (scene_crosses, "1 · Memorial crosses"),
    (scene_shipfire, "2 · Burning ship"),
    (scene_rocket, "43 · Shenzhou-24"),
    (scene_reef, "15 · Great Barrier Reef"),
    (scene_tanker, "42 · Cairo tanker fire"),
    (scene_geo, "50 · Olkaria steam"),
]

# ---------------------------------------------------------------- page
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 14
CW = W - 2 * MX

# masthead
d.rectangle([0, 0, W, 76], fill=NAVY)
d.text((MX, 6), "THE WORLD", font=font(44, bold=True, serif=True), fill=(250, 244, 228))
d.text((MX, 54), "WEDNESDAY 25 NOVEMBER 2026", font=font(13, bold=True), fill=(210, 190, 120))
centred(d, W - MX - 150, 14, "50 STORIES · 8 REGIONS · 18 FIELDS", font(12, bold=True), (240, 235, 220))
centred(d, W - MX - 150, 34, "One day, the whole planet", font(10), (190, 200, 220))
d.rectangle([0, 76, W, 79], fill=GOLD)

# numbers strip
ny, nh = 84, 27
seg = CW // 6
for i, (num, lab) in enumerate(NUMBERS):
    x0 = MX + i * seg
    d.text((x0 + 4, ny), num, font=font(14, bold=True), fill=RED)
    d.text((x0 + 4, ny + 15), lab, font=font(8), fill=GREY)
    if i:
        d.line([x0, ny + 2, x0, ny + nh - 2], fill=LINE, width=1)
d.line([MX, ny + nh + 2, MX + CW, ny + nh + 2], fill=INK, width=1)

# three leads
ly, lh = 118, 144
lw = (CW - 20) // 3
lead_pics = [scene_crosses, scene_shipfire, scene_rocket]
for i, num in enumerate([1, 2, 3]):
    x0 = MX + i * (lw + 10)
    item = ITEMS[num - 1]
    lead_pics[i](d, x0, ly, lw, 68)
    para(d, x0, ly + 72, f"{num} {item[2]}", font(15, bold=True), lw, maxlines=2, fill=INK, lh=17)
    para(d, x0, ly + 108, item[3], font(9), lw, maxlines=2, fill=(50, 50, 55), lh=11)
    d.line([x0, ly + lh - 4, x0 + lw, ly + lh - 4], fill=LINE, width=1)

# timeline: five ships, 11–22 Nov
ty = 270
d.text((MX, ty), "WAR AT SEA — FIVE SHIPS, 11–22 NOVEMBER", font=font(11, bold=True), fill=NAVY)
d.line([MX, ty + 16, MX + CW, ty + 16], fill=NAVY, width=2)
tw = CW // 5
for i, (dt, ship, what, place) in enumerate(SHIPS):
    x0 = MX + i * tw
    d.ellipse([x0 + 2, ty + 20, x0 + 10, ty + 28], fill=RED)
    d.text((x0 + 14, ty + 19), dt, font=font(9, bold=True), fill=RED)
    d.text((x0 + 2, ty + 31), ship, font=font(10, bold=True), fill=INK)
    d.text((x0 + 2, ty + 43), what, font=font(8), fill=GREY)
    d.text((x0 + 2, ty + 53), place, font=font(8), fill=GREY)

# pictures strip
py = 336
d.text((MX, py), "PICTURES — DRAWN IN CODE", font=font(10, bold=True), fill=NAVY)
pw = (CW - 25) // 6
for i, (fn, cap) in enumerate(SCENES):
    x0 = MX + i * (pw + 5)
    fn(d, x0, py + 16, pw, 46)
    d.text((x0, py + 64), cap, font=font(7), fill=GREY)

# grid: grouped by region, 5 columns x 10 rows
ordered = []
for reg in REGION_ORDER:
    ordered.extend([it for it in ITEMS if it[1] == reg])
assert len(ordered) == 50, len(ordered)
gy = 416
gh = 44
gw = (CW - 24) // 5
for idx, (num, reg, head, sub) in enumerate(ordered):
    r, c = divmod(idx, 5)
    x0 = MX + c * (gw + 6)
    y0 = gy + r * gh
    d.rectangle([x0, y0, x0 + gw, y0 + gh - 3], fill=CREAM2 if r % 2 == 0 else PAPER)
    d.text((x0 + 3, y0 + 2), f"{num:02d}", font=font(9, bold=True), fill=RED)
    d.text((x0 + 26, y0 + 3), reg, font=font(7, bold=True), fill=NAVY2)
    para(d, x0 + 3, y0 + 14, head, font(9, bold=True), gw - 6, maxlines=2, lh=10)
    # subhead: one line, clipped by width
    sub1 = wrap(d, sub, font(8), gw - 6, maxlines=1)
    if sub1:
        d.text((x0 + 3, y0 + 33), sub1[0], font=font(8), fill=GREY)

# region band + fields
by = gy + 10 * gh + 6
d.rectangle([MX, by, MX + CW, by + 26], fill=NAVY)
d.text((MX + 6, by + 6), "8 REGIONS", font=font(11, bold=True), fill=(250, 244, 228))
band = "  ·  ".join(f"{r} {REGION_COUNT[r]}" for r in REGION_ORDER)
d.text((MX + 110, by + 7), band, font=font(9), fill=(220, 225, 235))
d.text((MX, by + 32), "18 FIELDS:  " + " · ".join(FIELDS), font=font(9), fill=INK)

# footer: date-check box, must end <= 1019
fy = by + 58
d.rectangle([MX, fy, MX + CW, fy + 72], outline=RED, width=2)
d.text((MX + 8, fy + 6), "DATE CHECK", font=font(10, bold=True), fill=RED)
para(d, MX + 8, fy + 20, "Left out as earlier news: COP31's collapse (Sun) · Nvidia's +31.5% rally (Mon) · Brentford 4-0 Everton (Mon) · Huang reinstated (Mon) · Jabalia strike (Mon) · Wednesday's news is the fallout, not the rally.", font(9), CW - 16, maxlines=3, lh=12)
sy = fy + 78
d.text((MX, sy), "Sources: Reuters · CNN · Mediazona · Meduza · Kyiv Independent · NY Post · FXStreet. Pictures and map: original, drawn in code.", font=font(8), fill=GREY)
assert sy + 12 <= 1019, sy
print(f"footer box {fy}-{fy+72}, sources {sy}, bottom {sy+12}")
img.save("entry.png", "PNG")
print("saved entry.png", img.size)
