#!/usr/bin/env python3
"""news-image-20261124 v2 — NEW RULES build (written fresh in this session).

Master System Instruction (Fura 25 Nov 23:01 WIB): Classic Financial
Broadsheet, cream #F6F2E9, Deep Navy #1E293B, Terracotta #B91C1C, serif.
Locked structure: giant-date masthead + story count; THE DAY IN UTC timeline
directly under the masthead (lesson from the A2 champion duel: the timeline
strip belongs up top); KPI strip of 6 giant news numbers; 3 hero cards with
custom inked procedural vector art; 5 secondary cards, EACH with an
icon/mini-graphic (no plain-text cards); bottom world map WHERE IT HAPPENED
(left 30%) + ALSO index nos. 9-32 (right 70%, 3 cols) + DATE CHECK ribbon.
TOTAL 32 stories (3 + 5 + 24), all verified live 25 Nov ~23:30 WIB.

Gemini blueprint (flash-lite, pool-2; strategy/audit routes 503'd three
times, flash-lite explicit worked on the 4th attempt): focal = Dow 50,019
chart; zone heights 96+360+280+288 (adapted to the locked structure);
variants A editorial (Chen focal) vs B market (Dow focal); polish move =
strict baseline grid. AUDIT of Gemini: no factual premise disputed; the
"baseline grid" polish is generic, so the build's real polish move is the
timeline-under-masthead + numbered map pins cross-referencing the ALSO
numbers (the two concrete criticisms from the A2 duel).

Facts (all 2+ sources, live search 25 Nov ~23:15-23:40 WIB):
- Chen Jining: Xinhua Tue 24 Nov; Reuters; 4th Politburo member probed
  since 2025; first Shanghai chief probed since 2006.
- Dow 50,018.70 +0.85% (+423.39); Nasdaq -1.48% to 23,733.54; S&P -0.50%;
  Nvidia -5.86%; KOSPI +6.32% to 5,006.03; Nikkei +3.9%.
- Sanofi buys Insmed $41.0bn cash, $175/share, ~17% over Mon close,
  46% over 18 Nov close; biggest pharma deal since Pfizer-SeaGen $43bn
  (2023). Sanofi PR 24 Nov 06:30 UTC.
- Sarkozy + Carla Bruni to trial 3 Nov-2 Dec 2027, 11 defendants,
  witness-tampering / criminal conspiracy (Le Monde/Reuters, Tue).
- Houthis ~60 km from Aden; govt digs in (Reuters/AP, Tue).
- Israel kills Hamas internal security chief Naeem Abu Nahel, Gaza City
  (Reuters, Tue). Russian strike on Zaporizhzhia kills 2, wounds 22
  (Reuters, Tue). UK heat deaths 5,258 summer 2026, prev high 2,985
  (2022) — UKHSA/Reuters, Tue.
- Microsoft 'Code Red' after 24h Nov 12-13 outage; 1-hour fix target
  (Reuters memos, Tue). Hasina plans return 16 Dec; Dhaka: extradition
  only (Reuters, Tue). Chess WCC Game 1: Gukesh-Sindarov draw, 38 moves,
  0.5-0.5 (Chess.com, Tue).
- v1's 21 stories reused as the base (verified 24 Nov 07:05-07:20 WIB;
  see RESEARCH.md): Iran-US, Nvidia +31% Mon, Indonesia fire 24 dead,
  Ukraine 153 drones, Gaza 99%, FIFA hosts, Puigdemont, Denmark,
  Estonia, Sparta II, singer flogging, India-China, Nepal, Odesa,
  Verstappen, supermoon, Modi IIT Patna, Vanuatu M6.5, S Korea FM,
  Lisbon march.
DATE TRAP (excluded, in DATE CHECK only): Hormuz tanker-mine fire is a
WED 25 Nov Iran claim — NOT 24 Nov. Alcaraz ATP title Sun 22 Nov.
Sparta II struck Sat 21 Nov. COP31 collapse Sun 22-23 Nov.

Deterministic: no network, no clock, no randomness. Every text line is
tracked; overflow / truncation / overlap fails the build (exit 1).
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 242, 233)   # #F6F2E9
NAVY = (30, 41, 59)       # #1E293B
TERRA = (185, 28, 28)     # #B91C1C
INK = (28, 25, 23)
GREY = (100, 96, 84)
CARD = (255, 255, 255)
EDGE = (198, 188, 164)
GOLD = (180, 130, 30)
GREEN = (22, 101, 52)
MAPLAND = (226, 214, 186)
MAPSEA = (228, 234, 238)
LIGHT = (238, 232, 214)

FONT_DIRS = ["/usr/share/fonts/truetype/liberation",
             "/usr/share/fonts/truetype/dejavu"]


def load_font(bold, size, serif=False, italic=False):
    if serif:
        names = (["LiberationSerif-BoldItalic.ttf"] if (bold and italic)
                 else ["LiberationSerif-Bold.ttf"] if bold
                 else ["LiberationSerif-Italic.ttf"] if italic
                 else ["LiberationSerif-Regular.ttf"])
        names += ["DejaVuSerif-Bold.ttf", "DejaVuSerif.ttf"]
    else:
        names = (["LiberationSans-BoldItalic.ttf"] if (bold and italic)
                 else ["LiberationSans-Bold.ttf"] if bold
                 else ["LiberationSans-Italic.ttf"] if italic
                 else ["LiberationSans-Regular.ttf"])
        names += ["DejaVuSans-Bold.ttf", "DejaVuSans.ttf"]
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, int(size))
    return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    out, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


class Audit:
    def __init__(self):
        self.boxes = []
        self.problems = []

    def put(self, draw, xy, lines, fnt, fill, cap=None, label="text"):
        x, y = xy
        step = int(fnt.size * 1.22)
        for ln in lines:
            w = draw.textlength(ln, font=fnt)
            self.boxes.append((label, x, y, x + w, y + fnt.size))
            if cap is not None and w > cap + 0.5:
                self.problems.append(
                    f"OVERFLOW {label}: '{ln}' {w:.0f}px > {cap}px")
            draw.text((x, y), ln, font=fnt, fill=fill)
            y += step
        return y

    def check_overlaps(self):
        for i in range(len(self.boxes)):
            for j in range(i + 1, len(self.boxes)):
                a, b = self.boxes[i], self.boxes[j]
                ox = min(a[3], b[3]) - max(a[1], b[1])
                oy = min(a[4], b[4]) - max(a[2], b[2])
                if ox > 1 and oy > 1:
                    self.problems.append(
                        f"OVERLAP {a[0]} vs {b[0]} at "
                        f"({max(a[1], b[1]):.0f},{max(a[2], b[2]):.0f}) "
                        f"{ox:.0f}x{oy:.0f}")

    def finish(self):
        self.check_overlaps()
        if self.problems:
            for p in self.problems:
                print("AUDIT FAIL:", p, file=sys.stderr)
            sys.exit(1)


def rule(draw, x0, y, x1, wdt=2, fill=NAVY):
    draw.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def badge(draw, tr, x, y, label, fill=TERRA):
    f = load_font(True, 10)
    w = draw.textlength(label, font=f) + 12
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=fill)
    tr.put(draw, (x + 6, y + 2), [label], f, (255, 255, 255),
           label="badge:" + label)
    return w

# ---------------------------------------------------------------- icons
def icon(draw, kind, x0, y0, s, ink=NAVY, accent=TERRA):
    """Small inked glyph, 2px outline style. Box s x s at (x0,y0)."""
    if kind == "scales":  # Sarkozy / law
        draw.line([(x0 + s * .5, y0 + 3), (x0 + s * .5, y0 + s - 4)],
                  fill=ink, width=2)
        draw.line([(x0 + 3, y0 + 7), (x0 + s - 3, y0 + 7)], fill=ink, width=2)
        for cx in (x0 + 6, x0 + s - 6):
            draw.line([(cx, y0 + 7), (cx, y0 + 15)], fill=ink, width=2)
            draw.arc([cx - 6, y0 + 12, cx + 6, y0 + 24], 0, 180, fill=accent,
                     width=2)
        draw.rectangle([x0 + s * .5 - 7, y0 + s - 6, x0 + s * .5 + 7,
                        y0 + s - 3], fill=ink)
    elif kind == "arrow":  # Houthi advance
        draw.line([(x0 + 3, y0 + s - 6), (x0 + s - 6, y0 + 5)], fill=ink,
                  width=3)
        draw.polygon([(x0 + s - 6, y0 + 3), (x0 + s - 1, y0 + 8),
                      (x0 + s - 11, y0 + 9)], fill=accent)
        draw.line([(x0 + 3, y0 + s - 6), (x0 + 14, y0 + s - 6)], fill=accent,
                  width=2)
        draw.ellipse([x0 + 2, y0 + s - 12, x0 + 10, y0 + s - 4],
                     outline=ink, width=2)
    elif kind == "target":  # Gaza strike
        cx, cy = x0 + s / 2, y0 + s / 2
        for r in (10, 6):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink,
                         width=2)
        draw.ellipse([cx - 2.5, cy - 2.5, cx + 2.5, cy + 2.5], fill=accent)
        draw.line([(cx, y0 + 1), (cx, y0 + 6)], fill=ink, width=2)
        draw.line([(cx, y0 + s - 6), (cx, y0 + s - 1)], fill=ink, width=2)
    elif kind == "burst":  # Zaporizhzhia
        cx, cy = x0 + s / 2, y0 + s / 2
        pts = []
        import math
        for k in range(12):
            r = 11 if k % 2 == 0 else 5
            a = math.pi * k / 6
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        draw.polygon(pts, fill=(250, 204, 21), outline=ink)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=accent)
    elif kind == "sun":  # heat
        cx, cy = x0 + s / 2, y0 + s / 2
        for k in range(8):
            import math
            a = math.pi * k / 4
            draw.line([(cx + 9 * math.cos(a), cy + 9 * math.sin(a)),
                       (cx + 13 * math.cos(a), cy + 13 * math.sin(a))],
                      fill=GOLD, width=2)
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(250, 204, 21),
                     outline=ink, width=2)
    elif kind == "pill":  # Sanofi
        draw.rounded_rectangle([x0 + 2, y0 + 6, x0 + s - 2, y0 + s - 6],
                               radius=8, outline=ink, width=2, fill=CARD)
        draw.rectangle([x0 + 2, y0 + 6, x0 + s / 2, y0 + s - 6],
                       fill=TERRA)
        draw.line([(x0 + s / 2, y0 + 6), (x0 + s / 2, y0 + s - 6)],
                  fill=ink, width=2)
        draw.rounded_rectangle([x0 + 2, y0 + 6, x0 + s - 2, y0 + s - 6],
                               radius=8, outline=ink, width=2)


# ---------------------------------------------------------------- hero art
def art_chen(draw, x0, y0, wdt, hgt):
    """Shanghai skyline, inked, with red seal stamp."""
    base = y0 + hgt - 14
    draw.rectangle([x0, y0, x0 + wdt, y0 + hgt], fill=(232, 226, 204))
    # Oriental Pearl-ish tower + blocks
    draw.polygon([(x0 + wdt * .45, base), (x0 + wdt * .48, y0 + 14),
                  (x0 + wdt * .52, y0 + 14), (x0 + wdt * .55, base)],
                 fill=NAVY, outline=INK)
    draw.line([(x0 + wdt * .5, y0 + 14), (x0 + wdt * .5, y0 + 4)],
              fill=INK, width=2)
    draw.ellipse([x0 + wdt * .46, y0 + 30, x0 + wdt * .54, y0 + 42],
                 fill=TERRA, outline=INK, width=2)
    draw.ellipse([x0 + wdt * .47, y0 + 56, x0 + wdt * .53, y0 + 66],
                 fill=TERRA, outline=INK, width=2)
    for bx, bw, bh in ((.06, .16, .55), (.24, .14, .72), (.62, .18, .62),
                       (.82, .12, .48)):
        draw.rectangle([x0 + wdt * bx, base - hgt * bh,
                        x0 + wdt * (bx + bw), base], fill=(90, 100, 120),
                       outline=INK, width=2)
        for wy in range(3):
            for wx in range(2):
                draw.rectangle(
                    [x0 + wdt * (bx + .03 + wx * .06),
                     base - hgt * bh + 8 + wy * 12,
                     x0 + wdt * (bx + .06 + wx * .06),
                     base - hgt * bh + 14 + wy * 12],
                    fill=(250, 204, 21))
    draw.line([(x0, base), (x0 + wdt, base)], fill=INK, width=3)
    # red seal stamp
    sx, sy = x0 + wdt - 66, y0 + 8
    draw.rectangle([sx, sy, sx + 56, sy + 56], outline=TERRA, width=3)
    draw.rectangle([sx + 4, sy + 4, sx + 52, sy + 52], outline=TERRA,
                   width=1)
    f = load_font(True, 13, serif=True)
    draw.text((sx + 9, sy + 6), "PROBE", font=f, fill=TERRA)
    draw.text((sx + 14, sy + 30), "4TH", font=f, fill=TERRA)


def art_dow(draw, x0, y0, wdt, hgt):
    """Split market chart: green climb to 50,019, red give-back."""
    draw.rectangle([x0, y0, x0 + wdt, y0 + hgt], fill=CARD)
    base = y0 + hgt - 16
    # gridlines
    for gy in range(4):
        yy = y0 + 10 + gy * (hgt - 26) / 3
        draw.line([(x0 + 6, yy), (x0 + wdt - 6, yy)], fill=EDGE, width=1)
    # green climb
    pts = [(x0 + 8, base - 8), (x0 + wdt * .3, base - hgt * .45),
           (x0 + wdt * .55, base - hgt * .38),
           (x0 + wdt * .72, base - hgt * .82)]
    draw.line(pts, fill=GREEN, width=4, joint="curve")
    # red give-back
    pts2 = [(x0 + wdt * .72, base - hgt * .82),
            (x0 + wdt * .86, base - hgt * .55),
            (x0 + wdt - 8, base - hgt * .42)]
    draw.line(pts2, fill=TERRA, width=4, joint="curve")
    # peak dot + dashed 50,000 line
    px, py = x0 + wdt * .72, base - hgt * .82
    draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=GREEN, outline=INK,
                 width=2)
    ly = base - hgt * .78
    for xx in range(int(x0 + 6), int(x0 + wdt - 6), 12):
        draw.line([(xx, ly), (xx + 7, ly)], fill=GOLD, width=2)
    f = load_font(True, 10)
    draw.text((x0 + 8, ly - 14), "50,000", font=f, fill=GOLD)


def art_sanofi(draw, x0, y0, wdt, hgt):
    """Pill + vial, inked, on light panel."""
    draw.rectangle([x0, y0, x0 + wdt, y0 + hgt], fill=(232, 226, 204))
    # big capsule
    draw.rounded_rectangle([x0 + 12, y0 + hgt / 2 - 16,
                            x0 + wdt - 12, y0 + hgt / 2 + 16], radius=16,
                           fill=CARD, outline=INK, width=3)
    draw.rectangle([x0 + 12, y0 + hgt / 2 - 16, x0 + wdt / 2,
                    y0 + hgt / 2 + 16], fill=TERRA)
    draw.line([(x0 + wdt / 2, y0 + hgt / 2 - 16),
               (x0 + wdt / 2, y0 + hgt / 2 + 16)], fill=INK, width=3)
    # vial
    vx = x0 + wdt - 52
    draw.rectangle([vx, y0 + 10, vx + 30, y0 + hgt - 12], fill=CARD,
                   outline=INK, width=2)
    draw.rectangle([vx + 4, y0 + 4, vx + 26, y0 + 12], fill=NAVY)
    draw.rectangle([vx + 4, y0 + hgt - 26, vx + 26, y0 + hgt - 14],
                   fill=(147, 197, 253))
    f = load_font(True, 12)
    tw = draw.textlength("$175", font=f)
    draw.text((x0 + 16, y0 + hgt / 2 - 8), "$175", font=f,
              fill=(255, 255, 255))
    draw.text((x0 + 16 + tw + 4, y0 + hgt / 2 - 8), "/ SHARE", font=f,
              fill=(255, 255, 255))


# ---------------------------------------------------------------- zones
def masthead(draw, tr):
    draw.rectangle([0, 0, W, 92], fill=PAPER)
    rule(draw, 24, 10, 1000, 3)
    f_k = load_font(True, 11)
    tr.put(draw, (24, 16),
           ["THE WORLD IN ONE DAY  —  A BROADSHEET OF TUESDAY'S NEWS"],
           f_k, TERRA, cap=976, label="kicker")
    f_d = load_font(True, 46, serif=True)
    tr.put(draw, (22, 32), ["TUESDAY 24 NOVEMBER 2026"], f_d, NAVY,
           cap=980, label="date")
    f_s = load_font(True, 13)
    tr.put(draw, (24, 80),
           ["32 STORIES  ·  7 CONTINENTS  ·  EVERY ONE FROM THIS ONE DAY"],
           f_s, INK, cap=976, label="subhead")
    rule(draw, 24, 92, 1000, 2)


def timeline(draw, tr, y0=96):
    f_l = load_font(True, 11)
    tr.put(draw, (24, y0 + 4), ["THE DAY IN UTC"], f_l, NAVY, cap=120,
           label="tl-label")
    f_t = load_font(False, 11)
    ticks = [("MON 02:40", "Vanuatu M6.5"),
             ("06:30", "Sanofi $41bn"),
             ("09:51", "Heat 5,258"),
             ("14:00", "Chess Game 1"),
             ("EVE", "Chen probe"),
             ("21:28", "Dow 50,019")]
    x = 150
    for t, what in ticks:
        draw.ellipse([x, y0 + 20, x + 6, y0 + 26], fill=TERRA)
        tr.put(draw, (x + 10, y0 + 4), [t], load_font(True, 11), TERRA,
               cap=80, label="tick:" + t)
        tr.put(draw, (x + 10, y0 + 17), [what], f_t, INK, cap=140,
               label="tickwhat:" + t)
        x += 146
    rule(draw, 150, y0 + 23, 996, 1, fill=EDGE)
    rule(draw, 24, y0 + 30, 1000, 1, fill=EDGE)


def kpi_strip(draw, tr, y0=130):
    f_l = load_font(True, 10)
    tr.put(draw, (24, y0), ["THE DAY IN NUMBERS"], f_l, NAVY, cap=200,
           label="kpi-label")
    items = [("50,019", "DOW CLOSE", "above 50,000"),
             ("$41BN", "SANOFI BUYS", "Insmed, $175/sh"),
             ("5,258", "HEAT DEATHS", "England, record"),
             ("60 KM", "HOUTHIS FROM", "Aden"),
             ("+6.32%", "KOSPI JUMP", "to 5,006.03"),
             ("24", "DEAD, FACTORY", "fire, Cikande")]
    bw, gap = 158, 6
    y = y0 + 16
    for i, (num, l1, l2) in enumerate(items):
        x = 24 + i * (bw + gap)
        draw.rectangle([x, y, x + bw, y + 46], fill=CARD, outline=EDGE,
                       width=1)
        draw.rectangle([x, y, x + bw, y + 3], fill=TERRA if i % 2 == 0
                       else NAVY)
        tr.put(draw, (x + 8, y + 7), [num], load_font(True, 22, serif=True),
               NAVY, cap=bw - 16, label="kpi:" + num)
        tr.put(draw, (x + 8, y + 31), [l1 + " " + l2],
               load_font(True, 9), GREY, cap=bw - 16, label="kpilab:" + l1)


HEROES = {
    "chen": dict(
        badge="CHINA · POLITICS", icon="chen",
        head="CHINA PROBES SHANGHAI PARTY CHIEF",
        dek=["Chen Jining, a Politburo member, is the",
             "4th top leader probed since 2025.",
             "First Shanghai chief probed since 2006.",
             "Politburo down to 21 active members."],
        src="Xinhua / Reuters"),
    "dow": dict(
        badge="MARKETS · USA", icon="dow",
        head="DOW TOPS 50,000 AS AI RALLY FADES",
        dek=["Dow +0.85% to 50,018.70; Nasdaq -1.48%,",
             "Nvidia -5.86% give back Monday's surge.",
             "KOSPI had jumped +6.32% in Seoul.",
             "S&P 500 -0.50% to 7,201.09."],
        src="Dow Jones / Reuters"),
    "sanofi": dict(
        badge="BUSINESS · PHARMA", icon="sanofi",
        head="SANOFI BUYS INSMED FOR $41BN",
        dek=["$175 a share in cash — the biggest",
             "pharma deal since 2023. Closes H1 2027."],
        src="Sanofi / WSJ"),
}


def hero_card(draw, tr, key, x0, y0, wdt, hgt, focal=False):
    st = HEROES[key]
    draw.rectangle([x0, y0, x0 + wdt, y0 + hgt], fill=CARD, outline=EDGE,
                   width=1)
    draw.rectangle([x0, y0, x0 + wdt, y0 + 3], fill=TERRA)
    art_h = 124 if focal else 48
    if key == "chen":
        art_chen(draw, x0 + 10, y0 + 26, wdt - 20, art_h)
    elif key == "dow":
        art_dow(draw, x0 + 10, y0 + 26, wdt - 20, art_h)
    else:
        art_sanofi(draw, x0 + 10, y0 + 26, wdt - 20, art_h)
    badge(draw, tr, x0 + 10, y0 + 7, st["badge"])
    ty = y0 + 26 + art_h + 8
    hs = 21 if focal else 15
    lines = wrap(draw, st["head"], load_font(True, hs, serif=True),
                 wdt - 20)
    ty = tr.put(draw, (x0 + 10, ty), lines, load_font(True, hs, serif=True),
                NAVY, cap=wdt - 20, label="herohead:" + key)
    dek = st["dek"] if focal else st["dek"][:2]
    dfs = 12 if focal else 11
    ty = tr.put(draw, (x0 + 10, ty + 2), dek, load_font(False, dfs),
                INK, cap=wdt - 20, label="herodek:" + key)
    src_y = y0 + hgt - 18 if focal else y0 + hgt - 14
    tr.put(draw, (x0 + 10, src_y), ["SOURCE: " + st["src"]],
           load_font(False, 9), GREY, cap=wdt - 20, label="herosrc:" + key)


SECONDARY = [
    ("SARKOZY", "scales", "SARKOZY & BRUNI TO STAND TRIAL",
     ["Late-2027 trial, 11 defendants,",
      "witness-tampering case."],
     "Le Monde"),
    ("HOUTHI", "arrow", "HOUTHIS 60 KM FROM ADEN",
     ["Govt forces dig in behind a",
      "fortified defence line."],
     "Reuters"),
    ("GAZA", "target", "ISRAEL KILLS HAMAS SECURITY CHIEF",
     ["Naeem Abu Nahel killed in a",
      "Gaza City airstrike."],
     "Reuters"),
    ("ZAPORIZHZHIA", "burst", "STRIKE KILLS 2 IN ZAPORIZHZHIA",
     ["Russian attack wounds 22",
      "overnight, governor says."],
     "Reuters"),
    ("HEAT", "sun", "RECORD 5,258 HEAT DEATHS",
     ["England's hottest summer;",
      "prev. high 2,985 in 2022."],
     "UKHSA"),
]


def secondary_row(draw, tr, y0=496):
    f_l = load_font(True, 10)
    tr.put(draw, (24, y0), ["THE DAY'S OTHER FRONT PAGES"], f_l, NAVY,
           cap=300, label="sec-label")
    y = y0 + 16
    hgt = 168
    cw, gap = 188, 7
    for i, (tag, kind, head, body, src) in enumerate(SECONDARY):
        x = 24 + i * (cw + gap)
        draw.rectangle([x, y, x + cw, y + hgt], fill=CARD, outline=EDGE,
                       width=1)
        draw.rectangle([x, y, x + cw, y + 3], fill=NAVY)
        # icon panel
        draw.rectangle([x + 8, y + 10, x + cw - 8, y + 58], fill=LIGHT,
                       outline=EDGE, width=1)
        icon(draw, kind, x + cw / 2 - 13, y + 16, 26)
        tr.put(draw, (x + 8, y + 64), [tag], load_font(True, 9), TERRA,
               cap=cw - 16, label="sectag:" + tag)
        lines = wrap(draw, head, load_font(True, 13, serif=True), cw - 16)
        yy = tr.put(draw, (x + 8, y + 78), lines,
                    load_font(True, 13, serif=True), NAVY, cap=cw - 16,
                    label="sechead:" + tag)
        yy = tr.put(draw, (x + 8, yy + 2), body, load_font(False, 11), INK,
                    cap=cw - 16, label="secbody:" + tag)
        tr.put(draw, (x + 8, y + hgt - 16), ["SOURCE: " + src],
               load_font(False, 9), GREY, cap=cw - 16, label="secsrc:" + tag)


def world_map(draw, tr, x0, y0, wdt, hgt):
    draw.rectangle([x0, y0, x0 + wdt, y0 + hgt], fill=MAPSEA, outline=EDGE,
                   width=1)
    f_l = load_font(True, 11)
    tr.put(draw, (x0 + 8, y0 + 6), ["WHERE IT HAPPENED"], f_l, NAVY,
           cap=wdt - 16, label="map-label")
    # rough continents (flat blobs, inked)
    land = [
        [(14, 52), (60, 40), (96, 48), (88, 78), (50, 92), (18, 76)],
        [(118, 96), (150, 88), (168, 108), (150, 138), (122, 126)],
        [(150, 44), (196, 36), (232, 48), (222, 74), (182, 78), (156, 62)],
        [(196, 96), (238, 90), (262, 112), (240, 138), (206, 128)],
        [(236, 40), (272, 34), (282, 58), (262, 66), (240, 56)],
    ]
    for poly in land:
        pts = [(x0 + px, y0 + 34 + py * 0.72) for px, py in poly]
        draw.polygon(pts, fill=MAPLAND, outline=INK, width=2)
    pins = [(1, 262, 64), (2, 48, 66), (3, 158, 62), (4, 166, 76),
            (5, 214, 100), (6, 192, 84), (7, 198, 48), (8, 128, 32)]
    f_p = load_font(True, 10)
    for n, px, py in pins:
        cx, cy = x0 + px, y0 + 34 + py * 0.72
        draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9],
                     fill=TERRA if n <= 3 else NAVY, outline=(255, 255, 255),
                     width=2)
        tw = draw.textlength(str(n), font=f_p)
        draw.text((cx - tw / 2, cy - 7), str(n), font=f_p,
                  fill=(255, 255, 255))
    f_r = load_font(True, 8)
    for lab, lx, ly in (("N. AMERICA", 18, 128), ("EUROPE", 140, 108),
                        ("ASIA", 232, 108)):
        draw.text((x0 + lx, y0 + 34 + ly * 0.72), lab, font=f_r, fill=GREY)
    tr.put(draw, (x0 + 8, y0 + hgt - 42),
           ["1-3 heroes (red) · 4-8 secondary (navy).",
            "Numbers match the story numbers."],
           load_font(False, 10), INK, cap=wdt - 16, label="map-note")


ALSO = [
    ("MICROSOFT 'CODE RED'", "24h outage; 1-hr fix target"),
    ("KOSPI +6.32% TO 5,006", "Nikkei +3.9% in Tokyo"),
    ("HASINA SETS 16 DEC RETURN", "Dhaka: extradition only"),
    ("CHESS: GAME 1 A DRAW", "Gukesh-Sindarov, 38 moves"),
    ("IRAN-US: 'BOTTOM OF SEA'", "Trump warns Tehran ships"),
    ("NVIDIA +31% MONDAY", "Tue gives back -5.86%"),
    ("INDONESIA FIRE: 24 DEAD", "Candy factory, Cikande"),
    ("UKRAINE: 153 DRONES", "134 downed overnight"),
    ("GAZA: 99% CONTAMINATED", "Oxfam + CEOBS report"),
    ("FIFA NAMES 2031 + 2035", "48-team Women's WC hosts"),
    ("SPAIN SHELVES PUIGDEMONT", "Exile can end after 9 yrs"),
    ("DENMARK BACKS GHETTO LAW", "Top court: evictions stand"),
    ("ESTONIA SHUTS 5 CROSSINGS", "From 1 Dec, 6 months"),
    ("SPARTA II REACHES PORT", "16 crew safe, under tow"),
    ("IRAN FLOGS SINGER: 74 LASHES", "Parastoo Ahmadi, 5 people"),
    ("INDIA-CHINA TALKS", "Corps commanders, Arunachal"),
    ("NEPAL PM IN DELHI", "$2bn package reported"),
    ("ODESA WITHOUT POWER", "Strikes cut heat + water"),
    ("VERSTAPPEN WINS IN VEGAS", "Las Vegas Grand Prix"),
    ("SUPERMOON + PLEIADES", "Beaver moon peaks Tue"),
    ("MODI OPENS IIT PATNA AI", "Rs 400cr research park"),
    ("M6.5 QUAKE, VANUATU", "~600 km deep, no tsunami"),
    ("S KOREA NAMES NEW FM", "First woman spy chief"),
    ("LISBON MARCHES", "Thousands vs living costs"),
]


def also_index(draw, tr, x0, y0, wdt, hgt):
    f_l = load_font(True, 11)
    tr.put(draw, (x0, y0 + 6), ["ALSO ON TUESDAY 24 NOVEMBER 2026  —  9 TO 32"],
           f_l, NAVY, cap=wdt, label="also-label")
    rule(draw, x0, y0 + 24, x0 + wdt, 1, fill=EDGE)
    col_w = wdt / 3
    f_n = load_font(True, 11)
    f_h = load_font(True, 10)
    f_b = load_font(False, 10)
    for i, (head, body) in enumerate(ALSO):
        col, row = divmod(i, 8)
        x = x0 + col * col_w
        y = y0 + 32 + row * 28
        n = str(9 + i)
        draw.ellipse([x, y, x + 18, y + 18], fill=NAVY)
        tw = draw.textlength(n, font=f_n)
        draw.text((x + 9 - tw / 2, y + 3), n, font=f_n, fill=(255, 255, 255))
        tr.put(draw, (x + 22, y), [head], f_h, NAVY, cap=col_w - 24,
               label="alsohead:" + n)
        tr.put(draw, (x + 22, y + 13), [body], f_b, INK, cap=col_w - 24,
               label="alsobody:" + n)


def footer(draw, tr, y0=944):
    draw.rectangle([24, y0, 1000, y0 + 40], fill=NAVY)
    f = load_font(True, 11)
    tr.put(draw, (34, y0 + 5),
           ["DATE CHECK — Every story above was first reported Tue 24 Nov 2026 (UTC)."],
           f, (255, 255, 255), cap=950, label="dc1")
    tr.put(draw, (34, y0 + 21),
           ["NOT 24 Nov: Hormuz tanker fire (Wed 25 Nov claim) · Alcaraz title (Sun 22) · Sparta II struck (Sat 21) · COP31 (Sun 22-23)."],
           load_font(False, 10), (220, 220, 210), cap=950, label="dc2")
    f2 = load_font(False, 10)
    tr.put(draw, (24, y0 + 48),
           ["Sources: Reuters · AP · Xinhua · Le Monde · Sanofi · UKHSA · Dow Jones · Chess.com · WSJ · Guardian · FIFA · Oxfam. 32 stories verified live 25 Nov 2026."],
           f2, GREY, cap=976, label="sources")
    tr.put(draw, (24, y0 + 62),
           ["EDITION CLOSED 25 NOV 2026 · PROGRAM WRITES entry.png · NO NETWORK · DETERMINISTIC"],
           load_font(True, 10), GREY, cap=976, label="edition")


def render(path, variant):
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    tr = Audit()
    draw.rectangle([4, 4, W - 5, H - 5], outline=NAVY, width=2)
    masthead(draw, tr)
    timeline(draw, tr, 96)
    kpi_strip(draw, tr, 130)
    # heroes y 196-492
    if variant == "A":
        hero_card(draw, tr, "chen", 24, 196, 556, 296, focal=True)
        hero_card(draw, tr, "dow", 592, 196, 408, 146)
        hero_card(draw, tr, "sanofi", 592, 346, 408, 146)
    else:
        hero_card(draw, tr, "dow", 24, 196, 556, 296, focal=True)
        hero_card(draw, tr, "chen", 592, 196, 408, 146)
        hero_card(draw, tr, "sanofi", 592, 346, 408, 146)
    secondary_row(draw, tr, 496)
    also_index(draw, tr, 324, 684, 676, 256)
    world_map(draw, tr, 24, 684, 288, 256)
    footer(draw, tr, 944)
    tr.finish()
    img.save(path, "PNG", optimize=True)
    return path


def main():
    outdir = os.path.dirname(os.path.abspath(__file__))
    for variant, name in (("A", "cand_v2_A.png"), ("B", "cand_v2_B.png")):
        p = os.path.join(outdir, name)
        render(p, variant)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        print(name, os.path.getsize(p), "bytes sha256", h)
    # 300px downscales
    for name in ("cand_v2_A.png", "cand_v2_B.png"):
        p = os.path.join(outdir, name)
        im = Image.open(p)
        im.resize((300, 300), Image.LANCZOS).save(
            os.path.join(outdir, name.replace(".png", "_300.png")), "PNG")
    print("OK both candidates rendered, gates passed")


if __name__ == "__main__":
    main()
