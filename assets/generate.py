#!/usr/bin/env python3
"""
Generates the monochrome SVG artwork for the profile README.

Each piece has a light and a dark variant, transparent background, swapped
by <picture> on GitHub's theme.

  hero-*.svg        the nameplate that sits under the banner
  inspect-*.svg     what design-tool actually does, drawn
  process-*.svg     how i work — the mess resolving into meaning

Run:  python3 assets/generate.py
"""

import math
import os
import random

MONO = "ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, monospace"

THEMES = {
    "light": dict(ink="#111111", dim="#8a8a8a", faint="#d8d8d8"),
    "dark": dict(ink="#ffffff", dim="#8b8b8b", faint="#2a2a2a"),
}

STEPS = [
    ("01", "look out", "analyse patterns"),
    ("02", "build", "with my own craft"),
    ("03", "find", "meaning in the mess"),
    ("04", "prototype", "feel the experience"),
    ("05", "refine", "until it looks right"),
    ("06", "ship", "with confidence"),
]


def head(w, h, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" fill="none" role="img" aria-label="{label}">'
    )


def txt(x, y, s, size, fill, anchor="start", weight=None, track=None, op=None):
    a = f'<text x="{x:.1f}" y="{y:.1f}" font-family="{MONO}" font-size="{size}" fill="{fill}" text-anchor="{anchor}"'
    if weight:
        a += f' font-weight="{weight}"'
    if track:
        a += f' letter-spacing="{track}"'
    if op:
        a += f' opacity="{op}"'
    return a + f">{s}</text>"


# ───────────────────────────────────────────────────────────── hero

def hero(theme):
    """A nameplate: the name set large, with technical annotation around it."""
    c = THEMES[theme]
    W, H = 1200, 300

    # the frame the four crosshairs describe
    L, R, T, B = 60, 1140, 40, H - 40
    PAD = 37                      # even breathing room on all four sides
    x0, x1 = L + PAD, R - PAD     # content spans this, ruler included

    # the content block, measured so it centres inside the frame:
    #   name cap-height above the baseline, tagline descender below it
    CAP, DESC, TAIL = 54, 4, 88   # 76px caps, 17px descender, baseline offsets
    block_h = CAP + TAIL + DESC
    base = (T + B) / 2 - block_h / 2 + CAP

    p = [head(W, H, "nameplate reading naresh sain, product designer slowly "
                    "becoming a design engineer, with technical annotation")]

    # corner crosshairs — the frame of a drawing, not a decoration
    for cx, cy in ((L, T), (R, T), (L, B), (R, B)):
        p += [
            f'<line x1="{cx - 12}" y1="{cy}" x2="{cx + 12}" y2="{cy}" stroke="{c["dim"]}" stroke-width="1"/>',
            f'<line x1="{cx}" y1="{cy - 12}" x2="{cx}" y2="{cy + 12}" stroke="{c["dim"]}" stroke-width="1"/>',
        ]

    # top annotation row — sits on the crosshair centreline, inset to clear it
    p.append(txt(x0 + 12, T + 5, "N 28.61°  E 77.21°", 13, c["dim"], track="1.2"))
    p.append(txt(x1 - 12, T + 5, "NEW DELHI, INDIA", 13, c["dim"], anchor="end", track="1.2"))

    # the name
    p.append(txt(x0, base, "naresh sain", 76, c["ink"], weight="600", track="-2"))

    # baseline rule running out from the name
    ry = base + 22
    p.append(f'<line x1="{x0}" y1="{ry}" x2="{x1}" y2="{ry}" stroke="{c["faint"]}" stroke-width="1"/>')
    x = x0
    i = 0
    while x <= x1:
        h = 9 if i % 4 == 0 else 4
        p.append(
            f'<line x1="{x:.1f}" y1="{ry}" x2="{x:.1f}" y2="{ry - h}" '
            f'stroke="{c["dim"]}" stroke-width="1" opacity="0.45"/>'
        )
        i += 1
        x = x0 + i * 24

    # role line
    p.append(txt(x0, base + 58, "product designer, slowly becoming a design engineer",
                 20, c["ink"], op="0.9"))
    p.append(txt(x0, base + TAIL, "i build the things i wish i had.", 17, c["dim"]))

    p.append("</svg>")
    return "\n".join(p)


# ─────────────────────────────────────────────────────────── process

def ease(t):
    return t * t * (3 - 2 * t) if t < 1 else 1.0


def process(theme):
    c = THEMES[theme]
    W, H = 1200, 400
    top, bottom = 48, 250
    left, right = 60, 1140
    cols, rows = 48, 9

    random.seed(7)
    dots = []
    for cx in range(cols):
        t = ease(cx / (cols - 1))
        x_grid = left + (right - left) * (cx / (cols - 1))
        for ry in range(rows):
            y_grid = top + (bottom - top) * (ry / (rows - 1))
            spread = 1 - t
            dots.append((
                x_grid + random.uniform(-1, 1) * 46 * spread,
                y_grid + random.uniform(-1, 1) * 58 * spread,
                2.0 + 1.4 * t,
                0.18 + 0.72 * t,
            ))

    p = [head(W, H, "a scatter of points resolving into an ordered grid, "
                    "labelled with six workflow steps")]
    for x, y, r, o in dots:
        p.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}" fill="{c["ink"]}" opacity="{o:.3f}"/>')

    p.append(txt(left, 30, "THE MESS", 15, c["dim"], track="1.5"))
    p.append(txt(right, 30, "THE MEANING", 15, c["ink"], anchor="end", track="1.5"))

    axis = bottom + 46
    p.append(f'<line x1="{left}" y1="{axis}" x2="{right}" y2="{axis}" stroke="{c["faint"]}" stroke-width="1"/>')
    for i, (num, verb, tail) in enumerate(STEPS):
        x = left + (right - left) * (i / (len(STEPS) - 1))
        anchor = "start" if i == 0 else "end" if i == len(STEPS) - 1 else "middle"
        dx = 0 if anchor == "middle" else (6 if anchor == "start" else -6)
        p.append(f'<line x1="{x:.1f}" y1="{axis - 7}" x2="{x:.1f}" y2="{axis + 7}" stroke="{c["ink"]}" stroke-width="1.5"/>')
        p.append(txt(x + dx, axis + 32, num, 14, c["dim"], anchor=anchor))
        p.append(txt(x + dx, axis + 54, verb, 17, c["ink"], anchor=anchor))
        p.append(txt(x + dx, axis + 76, tail, 13, c["dim"], anchor=anchor))
    p.append("</svg>")
    return "\n".join(p)


# ───────────────────────────────────────────────────────────── inspect

def inspect(theme):
    c = THEMES[theme]
    W, H = 1200, 520
    p = [head(W, H, "a browser window with a type and spacing inspection "
                    "overlay measuring a heading")]

    p.append(f'<rect x="24" y="24" width="{W - 48}" height="{H - 48}" rx="10" stroke="{c["faint"]}" stroke-width="1.5"/>')
    p.append(f'<line x1="24" y1="76" x2="{W - 24}" y2="76" stroke="{c["faint"]}" stroke-width="1.5"/>')
    for i in range(3):
        p.append(f'<circle cx="{54 + i * 22}" cy="50" r="5" stroke="{c["dim"]}" stroke-width="1.2"/>')
    p.append(f'<rect x="130" y="38" width="300" height="24" rx="12" stroke="{c["faint"]}" stroke-width="1.2"/>')
    p.append(txt(148, 55, "any website", 13, c["dim"]))

    p.append(f'<rect x="72" y="128" width="150" height="14" rx="7" fill="{c["ink"]}" opacity="0.28"/>')

    hx, hy, hw, hh = 72, 172, 520, 46
    p.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="4" fill="{c["ink"]}" opacity="0.14"/>')
    p.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="4" stroke="{c["ink"]}" stroke-width="1.5" stroke-dasharray="5 4"/>')
    for cx, cy in [(hx, hy), (hx + hw, hy), (hx, hy + hh), (hx + hw, hy + hh)]:
        p.append(f'<rect x="{cx - 4}" y="{cy - 4}" width="8" height="8" fill="{c["ink"]}"/>')

    for i, w in enumerate([470, 500, 430, 360]):
        p.append(f'<rect x="72" y="{262 + i * 26}" width="{w}" height="10" rx="5" fill="{c["ink"]}" opacity="0.16"/>')

    gap_top, gap_bottom, mx = hy + hh, 262, 640
    p.append(f'<line x1="{mx}" y1="{gap_top}" x2="{mx}" y2="{gap_bottom}" stroke="{c["ink"]}" stroke-width="1.2"/>')
    for yy in (gap_top, gap_bottom):
        p.append(f'<line x1="{mx - 7}" y1="{yy}" x2="{mx + 7}" y2="{yy}" stroke="{c["ink"]}" stroke-width="1.2"/>')
    p.append(txt(mx + 14, (gap_top + gap_bottom) / 2 + 5, "44", 14, c["ink"]))

    for yy in (hy, hy + hh):
        p.append(f'<line x1="{hx + hw}" y1="{yy}" x2="{mx + 60}" y2="{yy}" stroke="{c["ink"]}" stroke-width="1" stroke-dasharray="3 5" opacity="0.5"/>')

    px, py, pw, ph = 800, 150, 328, 210
    p.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="8" stroke="{c["ink"]}" stroke-width="1.5"/>')
    p.append(f'<line x1="{px}" y1="{py + 42}" x2="{px + pw}" y2="{py + 42}" stroke="{c["faint"]}" stroke-width="1.2"/>')
    p.append(txt(px + 20, py + 27, "INSPECT", 14, c["ink"], track="1.2"))
    for i, (k, v) in enumerate([("font", "Inter"), ("size", "32 / 40"), ("weight", "600"),
                                ("tracking", "-0.02em"), ("color", "#111111")]):
        yy = py + 72 + i * 28
        p.append(txt(px + 20, yy, k, 14, c["dim"]))
        p.append(txt(px + pw - 20, yy, v, 14, c["ink"], anchor="end"))

    p.append(f'<path d="M {hx + hw} {hy + 10} L {px - 28} {hy + 10} L {px - 28} {py + 21} L {px} {py + 21}" stroke="{c["ink"]}" stroke-width="1.2" stroke-dasharray="4 4" opacity="0.6"/>')
    p.append(f'<circle cx="{px - 28}" cy="{py + 21}" r="3" fill="{c["ink"]}"/>')

    ry = H - 62
    p.append(f'<line x1="72" y1="{ry}" x2="{W - 72}" y2="{ry}" stroke="{c["faint"]}" stroke-width="1"/>')
    for i in range(44):
        x = 72 + i * 24
        if x > W - 72:
            break
        h = 10 if i % 4 == 0 else 5
        p.append(f'<line x1="{x}" y1="{ry}" x2="{x}" y2="{ry - h}" stroke="{c["dim"]}" stroke-width="1" opacity="0.7"/>')

    p.append("</svg>")
    return "\n".join(p)


PIECES = {
    "hero": hero,
    "inspect": inspect,
    "process": process,
}

if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for name, fn in PIECES.items():
        for theme in THEMES:
            path = os.path.join(here, f"{name}-{theme}.svg")
            with open(path, "w") as f:
                f.write(fn(theme))
            print(f"wrote {name}-{theme}.svg")
