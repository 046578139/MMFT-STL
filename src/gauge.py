#!/usr/bin/env python3
"""Generate the magazine-well fit gauge.

A set of short posts across a range of sections, each labelled, so a real
magazine well can be tried against them rather than measured.  That catches
things a caliper on a magazine misses: the flare at the mouth, how far in
the well actually runs, and how tight is tight enough to still be pleasant
to seat one-handed.

Sections are quoted as the magazine well sees them -- perpendicular to the
post.  The stubs here stand straight up, so their section *is* that nominal
figure; the post on the finished stand is sheared over by 10.9 degrees and
so has to be drawn wider by 1/cos(lean) to present the same section.  The
stand's generator does that conversion itself, so report the number off the
gauge and nothing else.

Run ``python src/gauge.py`` to write ``stl/gauge/``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import trimesh
from shapely.affinity import translate

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build
import text as text_mod
from geometry import extrude, loft, rounded_rect, union

OUT = build.ROOT / "stl" / "gauge"

# Front-to-back and side-to-side, in millimetres, spanning single stack
# through wide double stack.  A measured Glock 17 magazine is 33.1 x 22.8,
# which lands inside this grid.
WIDTHS = (30.0, 32.0, 34.0)
DEPTHS = (16.0, 19.0, 22.0, 25.0)

STUB_RISE = 35.0        # enough to judge the fit; print these hollow
FLANGE_T = 2.0
FLANGE_MARGIN = 5.0     # flange overhang around the section
LABEL_STRIP = 22.0      # extra flange at the front, for the label
LABEL_CAP = 4.2         # cap height of the first label line
LABEL_CAP2 = 3.2        # cap height of the second line
LABEL_RELIEF = 0.6
TICK_EVERY = 5.0        # depth ticks up one narrow face
TICK_DEPTH = 0.4
N = 192                 # perimeter samples


def corner_radius(depth: float) -> float:
    """Keep the corners in proportion and never let them degenerate."""
    return min(build.BLADE_R, depth / 2 * 0.7)


def stub(width: float, depth: float, lines: list[str] | None = None) -> trimesh.Trimesh:
    """One gauge post: flange, straight stub, lead-in tip, depth ticks.

    ``lines`` is what gets embossed on the flange; it defaults to the
    section.  Platform stubs carry the platform on the first line and the
    section on the second, because the section is the part worth reporting
    back -- if a stub labelled for one pistol turns out to fit another, the
    number is still the useful half.
    """
    hx, hy = width / 2, depth / 2
    r = corner_radius(depth)

    # Flange, with a strip at the front (-y) to carry the label.
    fx = hx + FLANGE_MARGIN
    fy = hy + FLANGE_MARGIN
    plate = trimesh.creation.box(
        extents=(2 * fx, 2 * fy + LABEL_STRIP, FLANGE_T))
    plate.apply_translation((0.0, -LABEL_STRIP / 2, FLANGE_T / 2))

    sections = [(FLANGE_T, rounded_rect(hx, hy, r, N), (0.0, 0.0))]

    # Straight run, then the same lead-in the real post has, scaled to this
    # section so the stub enters a well the way the finished one will.
    sx, sy = hx / build.BLADE_HX, hy / build.BLADE_HY
    tip_start = STUB_RISE - build.BLADE_TIP[0][0]
    sections.append((FLANGE_T + tip_start, rounded_rect(hx, hy, r, N), (0.0, 0.0)))
    for drop, thx, thy in build.BLADE_TIP:
        ax, ay = thx * sx, thy * sy
        sections.append((FLANGE_T + STUB_RISE - drop,
                         rounded_rect(ax, ay, min(r, ax, ay), N), (0.0, 0.0)))

    body = union([plate, loft(sections)])

    # Depth ticks on one narrow face, every 5 mm, longer every 10 mm.  Local
    # notches rather than full rings, so nothing catches on the well's mouth.
    cuts = []
    height = TICK_EVERY
    while height <= STUB_RISE - 6.0:
        half = 4.0 if abs(height % 10.0) < 1e-6 else 2.0
        cut = trimesh.creation.box(extents=(TICK_DEPTH + 1.0, 2 * half, 0.8))
        cut.apply_translation((hx + 0.5 - TICK_DEPTH, 0.0, FLANGE_T + height))
        cuts.append(cut)
        height += TICK_EVERY
    body = trimesh.boolean.difference([body, union(cuts)], engine="manifold")

    from shapely.affinity import scale as sc

    if lines is None:
        lines = ["%gx%g" % (width, depth)]
    caps = (LABEL_CAP, LABEL_CAP2)
    baselines = (-fy - 8.0, -fy - 16.0) if len(lines) > 1 else (-fy - 10.0,)

    marks = []
    for line, cap, base in zip(lines, caps, baselines):
        geom = text_mod.set_line(line, text_mod.WORDMARK_FONT,
                                 tracking_em=0.0, slant_deg=0.0)
        gx0, gy0, gx1, gy1 = geom.bounds
        k = cap / (gy1 - gy0)
        geom = sc(geom, k, k, origin=(gx0, gy0))
        gx0, gy0, gx1, gy1 = geom.bounds
        marks.append(translate(geom, -(gx0 + gx1) / 2, base - gy0))

    embossed = [extrude(m, FLANGE_T, LABEL_RELIEF) for m in marks]
    return union([body] + embossed)


# Sections to try, by platform.  Where a figure is measured it is used as
# it stands; where none could be found the family is bracketed instead and
# the stubs are named to say so.
PLATFORMS = [
    # (long axis, thin axis, first label line, what it is)
    (33.1, 22.8, "GLOCK",  "Glock 9mm - 17/19/26/34/45, measured"),
    (31.4, 21.6, "P320",   "Sig P320 9mm/.40/.357, measured"),
    (34.8, 13.7, "1911",   "1911 single stack .45, measured"),
    (34.2, 12.9, "1911-S", "1911 bracket, one size under"),
    (35.4, 14.6, "1911-L", "1911 bracket, one size over"),
    (34.0, 21.0, "2011-A", "2011 family bracket - no source found"),
    (35.0, 22.5, "2011-B", "2011 family bracket - no source found"),
    (35.8, 24.0, "2011-C", "2011 family bracket - no source found"),
    (32.5, 23.5, "DS-A",   "P226 / M&P / FN bracket - no source found"),
    (34.0, 25.0, "DS-B",   "P226 / M&P / FN bracket - no source found"),
]


def platforms() -> None:
    """The platform-named set."""
    out = OUT / "platforms"
    out.mkdir(parents=True, exist_ok=True)
    pitch_x = 2 * (max(p[0] for p in PLATFORMS) / 2 + FLANGE_MARGIN) + 8.0
    pitch_y = (2 * (max(p[1] for p in PLATFORMS) / 2 + FLANGE_MARGIN)
               + LABEL_STRIP + 8.0)

    plate = []
    for i, (w, d, name, note) in enumerate(PLATFORMS):
        lines = [name, "%.1fx%.1f" % (w, d)]
        one = stub(w, d, lines)
        one.export(out / ("MMFT_Fit_%s.stl" % name))
        placed = stub(w, d, lines)
        placed.apply_translation(((i % 3) * pitch_x, (i // 3) * pitch_y, 0.0))
        plate.append(placed)
        print("  %-8s %5.1f x %5.1f mm   %s" % (name, w, d, note))
    combined = trimesh.util.concatenate(plate)
    combined.export(out / "MMFT_Fit_platforms_all.stl")
    e = combined.extents
    print("  -> %d stubs, %.0f x %.0f mm on the plate, %.1f cm3 of solid"
          % (len(plate), e[0], e[1], combined.volume / 1000))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    pitch_x = 2 * (max(WIDTHS) / 2 + FLANGE_MARGIN) + 8.0
    pitch_y = 2 * (max(DEPTHS) / 2 + FLANGE_MARGIN) + LABEL_STRIP + 8.0

    plate = []
    for row, depth in enumerate(DEPTHS):
        for col, width in enumerate(WIDTHS):
            one = stub(width, depth)
            one.apply_translation((col * pitch_x, row * pitch_y, 0.0))
            plate.append(one)
            single = OUT / ("MMFT_FitGauge_%gx%g.stl" % (width, depth))
            solo = stub(width, depth)
            solo.export(single)
    combined = trimesh.util.concatenate(plate)
    combined.export(OUT / "MMFT_FitGauge_all.stl")

    size = combined.extents
    print("  %d stubs, %.0f x %.0f mm on the plate, %.1f cm3 of solid"
          % (len(plate), size[0], size[1], combined.volume / 1000))
    print("  print these hollow -- 2 walls, 0%% infill -- they only need "
          "their outside surface")
    print("  sections: %s front-to-back x %s side-to-side"
          % (WIDTHS, DEPTHS))


if __name__ == "__main__":
    main()
    print()
    platforms()
