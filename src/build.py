#!/usr/bin/env python3
"""
Build the Mountain Maryland Firearms Training pistol display stand.

Run ``python src/build.py`` to regenerate everything in ``stl/``.

The stand is a filleted base plate with a leaning, rounded magazine-well
blade at one end and the MMFT mark raised out of the plate in front of it.

The blade's dimensions are carried over from the Glock stand this replaces,
so anything that fitted that one still fits this: a 33.67 x 22.84 mm
rounded-rectangle section (6.5 mm corners) leaning 10.89 degrees, standing
61.1 mm clear of the plate, with a filleted root and a chisel-shaped
lead-in at the tip.  The plate around it and the mark on it are new.

Because the mark stands proud of an otherwise flat plate, it comes out in a
second colour on any printer: multi-material slicers take the two bodies as
they are, and a single-extruder printer only needs a filament swap at the
top of the plate and another at the top of the mark.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import trimesh
from shapely.affinity import translate
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))

import logo as logo_mod
import threemf
from geometry import extrude, loft, rounded_rect, union

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "stl"
OUT_3MF = ROOT / "3mf"

# Colours the parts are tagged with, and the filament slot each asks for.
BLACK, RED, BONE = "#28282C", "#C41C20", "#E2E2DE"

# --------------------------------------------------------------------------
# Base plate
# --------------------------------------------------------------------------
BASE_L = 215.0          # x
BASE_W = 98.0           # y
BASE_H = 9.6            # z -- divides exactly by 0.12/0.15/0.2/0.24/0.3 mm
BASE_CORNER_R = 8.0     # plan-view corner radius
BASE_TOP_ROUND = 2.0    # round-over along the top edge
BASE_BOTTOM_CHAMFER = 0.6   # keeps elephant's foot off the parting line

# --------------------------------------------------------------------------
# Magazine-well blade -- carried over from the stand being replaced
# --------------------------------------------------------------------------
# The post is sheared, not tilted, so its horizontal section is wider than
# the one the magazine well actually sees.  Quote the nominal (perpendicular)
# section -- the number you would measure on a magazine or read off the fit
# gauge -- and let the shear correction fall out of it.
BLADE_NOMINAL_W = 33.06     # front-to-back, matches a measured G17 mag (33.1)
BLADE_NOMINAL_D = 22.837    # side-to-side
BLADE_R = 6.5           # section corner radius
BLADE_RISE = 61.14      # height above the plate
BLADE_LEAN = -0.19240   # dx per dz -- 10.89 degrees, leaning over the plate
BLADE_ROOT_FILLET = 4.0
BLADE_CX = 180.0        # section centre where it meets the plate
BLADE_CY = BASE_W / 2

BLADE_HX = BLADE_NOMINAL_W / 2 / np.cos(np.arctan(abs(BLADE_LEAN)))
BLADE_HY = BLADE_NOMINAL_D / 2

# Tip profile, measured off the original at 0.2 mm steps:
# (depth below the tip, half-width in x, half-width in y).
BLADE_TIP = [
    (8.2666, 16.8350, 11.4185), (8.0666, 16.8651, 11.4185),
    (7.8666, 16.8538, 11.4185), (7.6666, 16.8367, 11.4185),
    (7.4666, 16.8028, 11.4185), (7.2666, 16.7689, 11.4185),
    (7.0666, 16.7224, 11.4185), (6.8666, 16.6644, 11.4185),
    (6.6666, 16.6063, 11.4185), (6.4666, 16.5211, 11.4185),
    (6.2666, 16.4342, 11.4185), (6.0666, 16.3215, 11.4185),
    (5.8666, 16.1953, 11.4185), (5.6666, 16.0191, 11.4185),
    (5.4666, 15.7716, 11.4185), (5.2666, 15.3213, 11.4185),
    (5.0666, 14.7829, 11.4185), (4.8666, 14.2445, 11.4185),
    (4.6666, 13.7060, 11.4185), (4.4666, 13.1675, 11.4185),
    (4.2666, 12.6291, 11.4185), (4.0666, 12.0907, 11.4185),
    (3.8666, 11.5522, 11.4185), (3.6666, 11.0138, 11.4185),
    (3.4666, 10.4753, 11.4185), (3.2666,  9.9369, 11.4185),
    (3.0666,  9.3984, 11.4185), (2.8666,  8.8600, 11.4185),
    (2.6666,  8.3215, 11.4185), (2.4666,  7.7830, 11.4185),
    (2.2666,  7.2445, 11.3964), (2.0666,  6.7059, 11.3734),
    (1.8666,  6.1594, 11.3369), (1.6666,  5.6089, 11.2653),
    (1.4666,  5.0576, 11.1938), (1.2666,  4.4801, 11.0902),
    (1.0666,  3.9027, 10.9610), (0.8666,  3.3026, 10.8253),
    (0.6666,  2.6899, 10.6167), (0.4666,  2.0435, 10.3814),
    (0.2666,  1.3687, 10.0405), (0.1000,  0.7500,  9.6000),
]

# --------------------------------------------------------------------------
# Logo
# --------------------------------------------------------------------------
LOGO_SRC = ROOT / "assets" / "mmft_logo.png"
LOGO_W = 145.0          # width of the mark on the plate
LOGO_RELIEF = 0.6       # how proud it stands, or how deep it is let in --
                        # 3 layers at 0.20 mm, 2 at 0.30 mm, 4 at 0.15 mm
LOGO_MARGIN_X = 8.0     # left edge of the mark
LOGO_BOLD = 0.05        # per-side stroke growth, see logo.py

N_BASE = 400            # perimeter samples for the plate
N_BLADE = 256           # perimeter samples for the blade


# --------------------------------------------------------------------------


def build_base() -> trimesh.Trimesh:
    """The plate: chamfered at the bottom, rounded over at the top."""
    hx, hy, r = BASE_L / 2, BASE_W / 2, BASE_CORNER_R
    sections = []

    c = BASE_BOTTOM_CHAMFER
    sections.append((0.0, rounded_rect(hx - c, hy - c, max(r - c, 0.1), N_BASE), (0, 0)))
    sections.append((c, rounded_rect(hx, hy, r, N_BASE), (0, 0)))

    z_round = BASE_H - BASE_TOP_ROUND
    sections.append((z_round, rounded_rect(hx, hy, r, N_BASE), (0, 0)))

    steps = 10
    for i in range(1, steps + 1):
        a = (np.pi / 2) * i / steps
        inset = BASE_TOP_ROUND * (1.0 - np.cos(a))
        z = z_round + BASE_TOP_ROUND * np.sin(a)
        sections.append(
            (z, rounded_rect(hx - inset, hy - inset, max(r - inset, 0.05), N_BASE), (0, 0))
        )

    m = loft(sections)
    m.apply_translation((hx, hy, 0.0))
    return m


def build_blade() -> trimesh.Trimesh:
    """The leaning blade, root fillet through chisel tip."""
    sections = []

    def push(z_local: float, hx: float, hy: float, r: float) -> None:
        z = BASE_H + z_local
        dx = BLADE_CX + BLADE_LEAN * z_local
        sections.append((z, rounded_rect(hx, hy, r, N_BLADE), (dx, BLADE_CY)))

    # Concave fillet where the blade meets the plate: at height h the section
    # is grown outward by R - sqrt(2Rh - h^2), which is R at the plate and
    # zero once h reaches R.
    R = BLADE_ROOT_FILLET
    steps = 12
    for i in range(steps + 1):
        h = R * i / steps
        grow = R - np.sqrt(max(2 * R * h - h * h, 0.0))
        push(h, BLADE_HX + grow, BLADE_HY + grow, BLADE_R + grow)

    for depth, hx, hy in BLADE_TIP:
        push(BLADE_RISE - depth, hx, hy, min(BLADE_R, hx, hy))

    return loft(sections)


def build_logo(z0: float) -> dict[str, trimesh.Trimesh]:
    """Extrude each part of the mark as a solid whose base sits at ``z0``.

    At ``z0 = BASE_H`` the solids stand on the plate; at
    ``z0 = BASE_H - LOGO_RELIEF`` they occupy the top of it instead, which is
    what the flush set subtracts to make its pockets.
    """
    groups = logo_mod.vectorise(str(LOGO_SRC), LOGO_W, bold_mm=LOGO_BOLD)

    whole = unary_union(list(groups.values()))
    minx, miny, maxx, maxy = whole.bounds
    dx = LOGO_MARGIN_X - minx
    dy = (BASE_W - (maxy - miny)) / 2.0 - miny

    return {
        name: extrude(translate(geom, dx, dy), z0, LOGO_RELIEF)
        for name, geom in groups.items()
    }


def report(name: str, mesh: trimesh.Trimesh) -> None:
    ok = "watertight" if mesh.is_watertight else "NOT WATERTIGHT"
    print(
        f"  {name:<34} {len(mesh.faces):>7,} tris  "
        f"{mesh.volume / 1000:>7.1f} cm3  {ok}"
    )


def split(parts: dict[str, trimesh.Trimesh]):
    """Group the mark's parts into the lettering, the firearms, and both."""
    text = union([parts[g] for g in logo_mod.TEXT_GROUPS if g in parts])
    art = union([parts[g] for g in logo_mod.ART_GROUPS if g in parts])
    return text, art, union([text, art])


def main() -> None:
    body = union([build_base(), build_blade()])

    # Raised: the mark stands on the plate.  Every layer above the plate is
    # mark and nothing else, which is what lets a single extruder do this in
    # two colours with a pair of filament changes.
    print("raised set ...")
    raised = build_logo(BASE_H)
    r_text, r_art, r_full = split(raised)
    files = {
        "raised/MMFT_Stand_black_body.stl": body,
        "raised/MMFT_Stand_red_logo_full.stl": r_full,
        "raised/MMFT_Stand_red_logo_text.stl": r_text,
        "raised/MMFT_Stand_light_logo_art.stl": r_art,
        "raised/MMFT_Stand_one_piece.stl": union([body, r_full]),
    }

    # Flush: the mark is let into the plate instead, so nothing stands proud
    # to be caught or chipped and each piece is boxed in on all four sides by
    # the black around it.  Needs a multi-material printer -- black and red
    # share the same four layers.
    print("flush set ...")
    flush = build_logo(BASE_H - LOGO_RELIEF)
    f_text, f_art, f_full = split(flush)
    pocketed = trimesh.boolean.difference([body, f_full], engine="manifold")
    files.update({
        "flush/MMFT_Stand_black_body.stl": pocketed,
        "flush/MMFT_Stand_red_logo_full.stl": f_full,
        "flush/MMFT_Stand_red_logo_text.stl": f_text,
        "flush/MMFT_Stand_light_logo_art.stl": f_art,
        # The pockets left empty: one colour, engraved, nothing to knock off.
        "flush/MMFT_Stand_engraved_one_piece.stl": pocketed,
    })

    print("writing stl ...")
    for fname, mesh in files.items():
        path = OUT / fname
        path.parent.mkdir(parents=True, exist_ok=True)
        mesh.export(path)
        report(fname, mesh)

    # The same models as 3MF projects: one file each, parts held together and
    # already tagged with their colours.  STL can carry none of that.
    print("writing 3mf ...")
    projects = {
        "MMFT_Stand_flush_2color.3mf": [
            ("Stand body", pocketed, BLACK, 1),
            ("Logo", f_full, RED, 2)],
        "MMFT_Stand_flush_3color.3mf": [
            ("Stand body", pocketed, BLACK, 1),
            ("Lettering", f_text, RED, 2),
            ("Firearms", f_art, BONE, 3)],
        "MMFT_Stand_raised_2color.3mf": [
            ("Stand body", body, BLACK, 1),
            ("Logo", r_full, RED, 2)],
        "MMFT_Stand_raised_3color.3mf": [
            ("Stand body", body, BLACK, 1),
            ("Lettering", r_text, RED, 2),
            ("Firearms", r_art, BONE, 3)],
    }
    for fname, parts in projects.items():
        threemf.write(OUT_3MF / fname, parts, "MMFT Pistol Stand")
        size = (OUT_3MF / fname).stat().st_size
        print(f"  {fname:<34} {len(parts)} parts  {size / 1e6:>5.2f} MB")

    bounds = files["raised/MMFT_Stand_one_piece.stl"].bounds
    size = bounds[1] - bounds[0]
    print(f"\n  overall {size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f} mm")


if __name__ == "__main__":
    main()
