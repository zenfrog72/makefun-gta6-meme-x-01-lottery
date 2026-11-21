#!/usr/bin/env python3
"""Original PIL-drawn meme candidates for gta6-meme-x-01.
Formats follow the leaderboard evidence (faux official documents, itemised
13-year-wait jokes, PAID stamp, make.fun agent footer) but every document
type here is one with zero entries on the board: resignation letter,
lottery ticket, speed-camera notice."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

OUT = os.path.dirname(os.path.abspath(__file__))
S = 1600

ANTON = "/home/hatch/workspace/makefun-gta6-cover-art-01/repo/app/fonts/Anton-Regular.ttf"
MONO = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
MONOB = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

def F(path, size): return ImageFont.truetype(path, size)

def tw(d, text, font):
    b = d.textbbox((0, 0), text, font=font)
    return b[2] - b[0]

def fit(d, text, path, start, min_size=20):
    size = start
    while size > min_size:
        f = F(path, size)
        if tw(d, text, f) <= S - 240:
            return f
        size -= 4
    return F(path, min_size)

def center(d, y, text, font, fill, x0=0, x1=S):
    w = tw(d, text, font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)
    return y

def gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    dr = ImageDraw.Draw(img)
    for y in range(h):
        t = y / max(h - 1, 1)
        dr.line([(0, y), (w, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return img

def ghost(d, cx, cy, scale=1.0, body=(255, 255, 255), outline=(20, 16, 40)):
    """Simple original blob-ghost with a pink star badge (make.fun-style agent mascot)."""
    w, h = 150 * scale, 170 * scale
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    d.rounded_rectangle([x0, y0, x1, y1 - 30 * scale], radius=70 * scale, fill=body, outline=outline, width=max(3, int(7 * scale)))
    # wavy bottom
    n = 5
    for i in range(n):
        bx = x0 + (i + 0.5) * (w / n)
        d.ellipse([bx - w / n / 2, y1 - 55 * scale, bx + w / n / 2, y1 - 5 * scale], fill=body)
    d.rectangle([x0 + 3, y1 - 42 * scale, x1 - 3, y1 - 26 * scale], fill=body)
    # eyes (sparkle diamonds)
    for ex in (cx - 32 * scale, cx + 32 * scale):
        r = 11 * scale
        d.polygon([(ex, cy - 28 * scale - r), (ex + r, cy - 28 * scale), (ex, cy - 28 * scale + r), (ex - r, cy - 28 * scale)], fill=outline)
    # smile
    d.arc([cx - 20 * scale, cy - 18 * scale, cx + 20 * scale, cy + 22 * scale], 15, 165, fill=outline, width=max(3, int(6 * scale)))
    # pink star badge
    bx, by, br = cx + 62 * scale, cy + 28 * scale, 34 * scale
    d.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 64, 150), outline=outline, width=max(3, int(5 * scale)))
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = br * 0.62 if i % 2 == 0 else br * 0.28
        pts.append((bx + rr * math.cos(ang), by + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 255, 255))

def stamp(base, cx, cy, lines, color=(200, 30, 60), angle=-9, scale=1.0):
    """Rotated rubber-stamp with double border."""
    f1 = F(MONOB, int(92 * scale))
    tmp_d = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    widths = [tw(tmp_d, t, f1) for t in lines]
    w = int(max(widths) + 90 * scale)
    h = int(len(lines) * 108 * scale + 46 * scale)
    layer = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([10, 10, w + 30, h + 30], radius=int(18 * scale), outline=color + (255,), width=int(10 * scale))
    d.rounded_rectangle([26, 26, w + 14, h + 14], radius=int(12 * scale), outline=color + (255,), width=int(4 * scale))
    y = 34 * scale
    for t in lines:
        lw = tw(d, t, f1)
        d.text(((w + 40 - lw) / 2, y), t, font=f1, fill=color + (255,))
        y += 108 * scale
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    base.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))

def row(d, y, label, sub, value, x0=130, x1=1470, label_color=(25, 25, 35), val_color=(25, 25, 35), accent=None, step=118):
    fL = F(MONOB, 47)
    fS = F(MONO, 33)
    fV = F(MONOB, 47)
    d.text((x0, y), label, font=fL, fill=label_color)
    if sub:
        d.text((x0 + 4, y + 56), sub, font=fS, fill=(90, 90, 100))
    vw = tw(d, value, fV)
    d.text((x1 - vw, y), value, font=fV, fill=accent or val_color)
    return y + step

# ---------------------------------------------------------------- candidate 1
def candidate1():
    img = gradient(S, S, (38, 18, 74), (122, 28, 92)).convert("RGBA")
    d = ImageDraw.Draw(img)
    # cream paper
    d.rounded_rectangle([60, 60, 1540, 1540], radius=26, fill=(250, 244, 224, 255))
    d.rounded_rectangle([60, 60, 1540, 1540], radius=26, outline=(20, 16, 40, 255), width=6)
    # header
    ghost(d, 220, 205, 0.85)
    d.text((330, 128), "FROM THE DESK OF", font=F(MONOB, 44), fill=(25, 25, 35))
    d.text((330, 182), "ONE PATIENT GAMER", font=F(MONOB, 44), fill=(25, 25, 35))
    d.text((330, 240), "VICE CITY  •  EMPLOYEE SINCE 2013", font=F(MONO, 34), fill=(110, 40, 90))
    d.line([130, 330, 1470, 330], fill=(200, 30, 90), width=5)
    # headline
    f = fit(d, "LETTER OF RESIGNATION", ANTON, 118)
    center(d, 356, "LETTER OF RESIGNATION", f, (18, 18, 30))
    center(d, 500, "EFFECTIVE: LAUNCH DAY — 19 NOV 2026", F(MONOB, 42), (200, 30, 60))
    d.line([130, 592, 1470, 592], fill=(25, 25, 35), width=4)
    d.text((130, 616), "TO: MY BOSS / THE REAL WORLD", font=F(MONO, 36), fill=(25, 25, 35))
    d.text((130, 664), "FROM: YOUR (EX-)EMPLOYEE", font=F(MONO, 36), fill=(25, 25, 35))
    d.line([130, 726, 1470, 726], fill=(25, 25, 35), width=3)
    y = 756
    y = row(d, y, "NOTICE PERIOD", "13 years — served in full, waiting", "GIVEN")
    y = row(d, y, "REASON FOR LEAVING", "Grand Theft Auto VI — finally out", "GTA VI")
    y = row(d, y, "DELAY No.1 + No.2", "notice extended twice, no pay rise", "$0.00")
    y = row(d, y, "SICK DAYS, LAUNCH WEEK", "5 days — doctor approved, couch ready", "BOOKED")
    y = row(d, y, "FINAL PAYCHECK WANTED", "one copy of the game, standard edition", "$79.99")
    d.line([130, y + 6, 1470, y + 6], fill=(25, 25, 35), width=4)
    d.text((130, y + 26), "TOTAL OWED:", font=F(ANTON, 54), fill=(18, 18, 30))
    vt = "ONE LAUNCH WEEK"
    fV = F(ANTON, 54)
    d.text((1470 - tw(d, vt, fV), y + 26), vt, font=fV, fill=(200, 30, 60))
    # stamp + footer (kept clear of the total row)
    stamp(img, 800, 1438, ["RESIGNED"], color=(200, 30, 60), angle=-8, scale=0.60)
    d = ImageDraw.Draw(img)
    d.text((130, 1440), "PAID BY MY AI AGENT", font=F(MONOB, 37), fill=(150, 20, 110))
    d.text((130, 1490), "ON MAKE.FUN", font=F(MONOB, 37), fill=(150, 20, 110))
    img.convert("RGB").save(os.path.join(OUT, "candidate1_resignation.png"))
    print("candidate1 done")

# ---------------------------------------------------------------- candidate 2
def candidate2():
    img = gradient(S, S, (24, 16, 64), (96, 20, 110)).convert("RGBA")
    d = ImageDraw.Draw(img)
    # ticket panel
    d.rounded_rectangle([70, 70, 1530, 1530], radius=30, fill=(16, 22, 52, 255), outline=(255, 200, 60, 255), width=6)
    # perforation dots
    for yy in range(120, 1500, 56):
        d.ellipse([52, yy, 88, yy + 34], fill=(40, 20, 80, 255))
        d.ellipse([1512, yy, 1548, yy + 34], fill=(40, 20, 80, 255))
    center(d, 108, "LEONIDA STATE LOTTERY", F(MONOB, 46), (255, 200, 60))
    center(d, 168, "OFFICIAL WINNING TICKET", fit(d, "OFFICIAL WINNING TICKET", ANTON, 104), (255, 255, 255))
    center(d, 300, "DRAW DATE: 19 NOV 2026  •  TICKET No. 000006", F(MONO, 36), (170, 200, 255))
    d.line([140, 372, 1460, 372], fill=(255, 200, 60), width=4)
    # number balls
    nums = [("13", "YEARS"), ("2", "DELAYS"), ("214", "GB"), ("19", "DAY"), ("11", "MONTH"), ("26", "YEAR")]
    cx = 218
    for n, lab in nums:
        d.ellipse([cx - 86, 420, cx + 86, 592], fill=(255, 64, 150), outline=(255, 255, 255), width=6)
        fn = F(ANTON, 84 if len(n) < 3 else 68)
        w = tw(d, n, fn)
        d.text((cx - w / 2, 462 if len(n) < 3 else 472), n, font=fn, fill=(255, 255, 255))
        fl = F(MONOB, 30)
        w = tw(d, lab, fl)
        d.text((cx - w / 2, 612), lab, font=fl, fill=(255, 200, 60))
        cx += 233
    d.line([140, 690, 1460, 690], fill=(120, 130, 200), width=3)
    def lrow(y, label, sub, value, vcol=(255, 255, 255)):
        d.text((140, y), label, font=F(MONOB, 46), fill=(255, 255, 255))
        if sub:
            d.text((144, y + 56), sub, font=F(MONO, 33), fill=(160, 175, 230))
        fv = F(MONOB, 46)
        d.text((1460 - tw(d, value, fv), y), value, font=fv, fill=vcol)
        return y + 122
    y = 730
    y = lrow(y, "NUMBERS MATCHED", "all six — a perfect ticket", "6 OF 6", (120, 255, 170))
    y = lrow(y, "DAYS WAITED FOR DRAW", "entered in 2013, drawn at last", "4,811")
    y = lrow(y, "JACKPOT — DAY-ONE SALES", "the game sold this in 24 hours", "$3.79B", (255, 200, 60))
    y = lrow(y, "MY ACTUAL PRIZE", "one copy of GTA VI, standard edition", "$79.99")
    d.line([140, y + 4, 1460, y + 4], fill=(255, 200, 60), width=4)
    center(d, y + 30, "I WAITED 13 YEARS AND ALL I WON WAS THE GAME.", F(MONOB, 40), (255, 255, 255))
    center(d, y + 88, "WORTH EVERY DAY.", F(MONOB, 40), (255, 64, 150))
    # gold claim band
    d.rounded_rectangle([140, 1370, 1460, 1480], radius=16, fill=(255, 200, 60, 255))
    center(d, 1396, "JACKPOT CLAIMED — PAID BY MY AI AGENT ON MAKE.FUN", F(MONOB, 38), (20, 16, 40))
    img.convert("RGB").save(os.path.join(OUT, "candidate2_lottery.png"))
    print("candidate2 done")

# ---------------------------------------------------------------- candidate 3
def candidate3():
    img = Image.new("RGBA", (S, S), (210, 210, 215, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=(210, 210, 215))
    # paper
    d.rectangle([70, 60, 1530, 1540], fill=(248, 248, 246))
    d.rectangle([70, 60, 1530, 1540], outline=(30, 30, 30), width=5)
    # header bar
    d.rectangle([70, 60, 1530, 208], fill=(18, 18, 26))
    d.text((120, 92), "LEONIDA TRAFFIC ENFORCEMENT", font=F(MONOB, 50), fill=(255, 255, 255))
    d.text((120, 152), "PHOTO ENFORCEMENT NOTICE  •  VICE CITY DISTRICT", font=F(MONO, 33), fill=(255, 90, 90))
    d.rectangle([70, 208, 1530, 222], fill=(220, 30, 50))
    # photo evidence panel
    px0, py0, px1, py1 = 120, 258, 1480, 700
    photo = gradient(px1 - px0, py1 - py0, (30, 20, 80), (255, 110, 90))
    img.paste(photo, (px0, py0))
    d = ImageDraw.Draw(img)
    # sun + palms silhouettes
    d.ellipse([1150, 330, 1330, 510], fill=(255, 210, 90))
    def palm(d, bx, by, h=190, s=1.0):
        # curved trunk: stacked segments leaning right
        pts = []
        for i in range(21):
            t = i / 20
            pts.append((bx + 26 * s * t * t, by - h * s * t))
        d.line(pts, fill=(20, 14, 30), width=int(15 * s))
        cxp, cyp = pts[-1]
        # drooping fronds: polylines bending downward
        for ang, ln in ((-168, 118), (-138, 132), (-104, 126), (-70, 126), (-38, 132), (-8, 116)):
            x, y = cxp, cyp
            dx = math.cos(math.radians(ang)); dy = math.sin(math.radians(ang))
            seg = []
            for k in range(4):
                seg.append((x, y))
                x += dx * ln * s / 3; y += dy * ln * s / 3 + k * 13 * s
            seg.append((x, y))
            d.line(seg, fill=(20, 14, 30), width=int(10 * s))
    palm(d, 278, 668, 195, 0.92)
    palm(d, 1288, 668, 210, 0.98)
    # couch + tv silhouettes
    d.rectangle([420, 400, 760, 520], fill=(16, 12, 28))  # TV
    d.rectangle([436, 416, 744, 504], fill=(90, 200, 255))
    center(d, 428, "VI", F(ANTON, 64), (16, 12, 28), 436, 744)
    d.rounded_rectangle([330, 540, 880, 660], radius=26, fill=(16, 12, 28))  # couch back
    d.rounded_rectangle([300, 610, 910, 690], radius=22, fill=(24, 18, 40))  # couch seat
    d.rectangle([120, 690, 1480, 700], fill=(16, 12, 28))
    # photo overlay text
    d.rectangle([px0, py0, px1, py0 + 52], fill=(0, 0, 0, 170))
    d.text((px0 + 22, py0 + 10), "CAM 06 — VICE CITY  •  19 NOV 2026  •  00:01 AM", font=F(MONOB, 34), fill=(255, 255, 120))
    spd = "214 GB/H"
    fs = F(ANTON, 92)
    d.rectangle([px1 - tw(d, spd, fs) - 60, py1 - 142, px1 - 18, py1 - 22], fill=(0, 0, 0, 185))
    d.text((px1 - tw(d, spd, fs) - 38, py1 - 126), spd, font=fs, fill=(255, 70, 70))
    d.rectangle([px0 + 14, py0 + 66, px0 + 330, py0 + 152], fill=(0, 0, 0, 150))
    d.text((px0 + 30, py0 + 78), "SPEED", font=F(MONOB, 32), fill=(255, 255, 255))
    d.text((px0 + 30, py0 + 114), "RECORDED", font=F(MONOB, 32), fill=(255, 255, 255))
    # rows
    def mrow(y, label, value, vcol=(25, 25, 35)):
        d.text((120, y), label, font=F(MONOB, 42), fill=(25, 25, 35))
        fv = F(MONOB, 42)
        d.text((1480 - tw(d, value, fv), y), value, font=fv, fill=vcol)
        return y + 62
    y = 734
    y = mrow(y, "VEHICLE:", "ONE COUCH + CONTROLLER")
    y = mrow(y, "SPEED 2013–2026:", "0 MPH — 4,811 DAYS")
    y = mrow(y, "SPEED, LAUNCH NIGHT:", "0 → 214 GB/H", (200, 20, 50))
    y = mrow(y, "VIOLATION:", "LAUNCH-DAY WHIPLASH")
    d.line([120, y + 8, 1480, y + 8], fill=(30, 30, 30), width=3)
    y += 28
    y = row(d, y, "WHIPLASH (2 DELAYS)", "release date moved, neck did not survive", "$0.00", x0=120, x1=1480, step=110)
    y = row(d, y, "PATIENCE", "none left — spent by 2025", "$0.00", x0=120, x1=1480, step=110)
    y = row(d, y, "GTA VI (FINALLY)", "standard edition, worth the ticket", "$79.99", x0=120, x1=1480, step=110)
    d.line([120, y + 2, 1480, y + 2], fill=(30, 30, 30), width=4)
    d.text((120, y + 20), "TOTAL FINE", font=F(ANTON, 54), fill=(18, 18, 30))
    fv = F(ANTON, 54)
    d.text((1480 - tw(d, "$79.99", fv), y + 20), "$79.99", font=fv, fill=(200, 20, 50))
    stamp(img, 1015, 1452, ["PAID IN FULL"], color=(220, 20, 120), angle=-7, scale=0.58)
    d = ImageDraw.Draw(img)
    d.text((120, 1470), "PAID BY MY AI AGENT ON MAKE.FUN", font=F(MONOB, 34), fill=(170, 10, 100))
    img.convert("RGB").save(os.path.join(OUT, "candidate3_speedcamera.png"))
    print("candidate3 done")

candidate1()
candidate2()
candidate3()
