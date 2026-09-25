#!/usr/bin/env python3
"""
Reproduce every measured number quoted in docs/PRINTING.md.

Run ``python src/analysis.py``.  Two independent studies:

* **Feature widths** -- decides the nozzle.  Worked on the exact logo
  polygons, never on a raster: rasterising and skeletonising this mark
  gives garbage, because the medial axis runs into the tapered tip of
  every letter where the true width goes to zero, so the minimum is
  always about one pixel no matter how fine the grid.  Morphological
  opening and closing on the vector geometry ask the question that
  actually matters -- *how much* of the mark lives in features narrower
  than one bead, and which separate shapes fuse -- and have exact answers.

* **Statics** -- decides whether it survives a shop counter.  The pistol
  is a point mass.  Note that the post goes *up inside* the magazine
  well, so the gun's mass sits low, starting near the plate; it does not
  perch on the tip.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build as B
import logo as L

ROOT = Path(__file__).resolve().parent.parent

# Plate and post, from build.py.
BASE_L, BASE_W, BASE_H = B.BASE_L, B.BASE_W, B.BASE_H
RISE, BLADE_CX = B.BLADE_RISE, B.BLADE_CX
LEAN = np.arctan(abs(B.BLADE_LEAN))

RHO_PETG = 1.27             # g/cm^3
SIGMA = {"PETG": 45.0, "PLA": 35.0}     # MPa across the layer lines
G = 9.80665

# The grip bottoms out just clear of the 4 mm root fillet.
GRIP_Z = BASE_H + 2.0

# (mass g, CoM above the grip bottom, push point above the grip bottom)
GUNS = {
    "Glock 17 (empty, polymer)":   (625.0, 92.0, 120.0),
    "Glock 17 (loaded mag)":       (890.0, 82.0, 120.0),
    "SIG P226 (empty, alloy)":     (964.0, 86.0, 118.0),
    "Staccato 2011 (loaded)":      (1130.0, 84.0, 122.0),
}

MU = {"bare PETG on laminate": 0.30, "felt pads": 0.35,
      "cork": 0.55, "rubber / silicone feet": 0.80}


def rule(title: str) -> None:
    print(f"\n{title}\n" + "-" * len(title))


# --------------------------------------------------------------------------
# Feature widths
# --------------------------------------------------------------------------
def feature_study() -> None:
    mark = unary_union(
        [g for g in L.vectorise(B.LOGO_SRC, width_mm=B.LOGO_W,
                                bold_mm=B.LOGO_BOLD).values()
         if not g.is_empty]
    )
    n0, area = len(mark.geoms), mark.area
    rule("Feature widths")
    print(f"mark {mark.bounds[2]-mark.bounds[0]:.1f} x {mark.bounds[3]-mark.bounds[1]:.1f} mm, "
          f"{n0} separate shapes, {area:.0f} mm^2 of ink")

    def fused(w: float):
        c = mark.buffer(w / 2, resolution=32).buffer(-w / 2, resolution=32)
        return n0 - (len(c.geoms) if hasattr(c, "geoms") else 1)

    # The gap that decides the nozzle.
    lo, hi = 0.05, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        lo, hi = (lo, mid) if fused(mid) else (mid, hi)
    print(f"\nnarrowest gap between two separate shapes : {hi:.3f} mm   <-- sets the nozzle")

    # The thinnest shape, for contrast: nothing here is delicate.
    lo, hi2 = 0.05, 3.0
    for _ in range(50):
        mid = (lo + hi2) / 2
        e = mark.buffer(-mid / 2, resolution=48)
        n = 0 if e.is_empty else (len(e.geoms) if hasattr(e, "geoms") else 1)
        lo, hi2 = (lo, mid) if (e.is_empty or n < n0) else (mid, hi2)
    print(f"thinnest whole shape                      : {hi2:.3f} mm")

    holes = [Polygon(r) for p in mark.geoms for r in p.interiors]
    widths = []
    for h in holes:
        a, b = 0.0, 5.0
        for _ in range(40):
            mid = (a + b) / 2
            a, b = (a, mid) if h.buffer(-mid / 2, resolution=24).is_empty else (mid, b)
        widths.append(b)
    print(f"narrowest interior counter ({len(holes)} of them)   : {min(widths):.3f} mm")

    print(f"\n{'line W':>8} {'ink in thinner features':>24} {'shapes fused':>13} {'counters closed':>16}")
    for w in (0.20, 0.30, 0.40, 0.42, 0.45, 0.50, 0.62, 0.68):
        o = mark.buffer(-w / 2, resolution=32).buffer(w / 2, resolution=32)
        print(f"{w:8.2f} {100*(area-o.area)/area:23.2f}% {fused(w):13d} "
              f"{sum(1 for x in widths if x < w):16d}")


# --------------------------------------------------------------------------
# Statics
# --------------------------------------------------------------------------
def statics() -> None:
    mesh = trimesh.load(ROOT / "stl/raised/MMFT_Stand_one_piece.stl")
    vol, area = mesh.volume / 1000.0, mesh.area / 100.0     # cm^3, cm^2
    shell = min(area * 0.135, vol * 0.95)                   # ~3 walls of 0.45
    core = vol - shell
    cx, cy, cz = mesh.center_mass

    def mass(infill: float) -> float:
        return RHO_PETG * (shell + core * infill)

    def tip(infill, gun_g, h_com, h_push, ballast=0.0, ballast_z=3.0):
        ms = mass(infill)
        gx = BLADE_CX - h_com * np.sin(LEAN)
        gz = GRIP_Z + h_com * np.cos(LEAN)
        pz = GRIP_Z + h_push * np.cos(LEAN)
        w = ms + gun_g + ballast
        bx = (ms * cx + gun_g * gx + ballast * BASE_L / 2) / w
        by = (ms * cy + gun_g * cy + ballast * BASE_W / 2) / w
        lever = {"sideways": BASE_W - by, "backward": BASE_L - bx, "forward": bx}
        return w, {k: (w / 1000) * G * (v / 1000) / (pz / 1000) for k, v in lever.items()}

    rule("Statics")
    print(f"stand centre of mass at ({cx:.1f}, {cy:.1f}, {cz:.1f}) mm; "
          f"post on the centreline at x={BLADE_CX:.0f}")

    print("\ntipping force, 25% infill, pushed at the slide:")
    for name, (gm, hc, hp) in GUNS.items():
        _, o = tip(0.25, gm, hc, hp)
        print(f"  {name:28s} " + "  ".join(
            f"{k} {v:5.2f} N ({v/4.448:4.2f} lbf)" for k, v in o.items()))

    gm, hc, hp = GUNS["Glock 17 (empty, polymer)"]
    print("\ninfill does not help:")
    for f in (0.15, 0.25, 0.50, 1.00):
        w, o = tip(f, gm, hc, hp)
        print(f"  {int(f*100):3d}% -> stand {mass(f):3.0f} g, total {w:4.0f} g, "
              f"sideways {o['sideways']:5.2f} N")

    print("\nballast does:")
    for b in (0, 250, 500, 750, 1000):
        w, o = tip(0.25, gm, hc, hp, ballast=b)
        print(f"  +{b:4d} g -> total {w/453.6:4.1f} lb, sideways {o['sideways']:5.2f} N, "
              f"backward {o['backward']:5.2f} N")

    print("\nslide before tip?  (grippier feet are worse, not better)")
    for b in (0, 500):
        w, o = tip(0.25, gm, hc, hp, ballast=b)
        t = min(o["sideways"], o["backward"])
        print(f"  +{b} g ballast, tips at {t:.2f} N:")
        for k, mu in MU.items():
            sl = mu * (w / 1000) * G
            print(f"      {k:24s} slides at {sl:5.2f} N -> "
                  f"{'slides first (safe)' if sl < t else 'TIPS FIRST'}")

    # Hollow section: the walls carry it, the infill is ignored.
    w_, d_ = B.BLADE_NOMINAL_W, B.BLADE_NOMINAL_D
    t_ = 6 * 0.40
    inertia = (w_ * d_**3 - (w_ - 2*t_) * (d_ - 2*t_)**3) / 12.0
    z_mod = inertia / (d_ / 2)
    lever = (GRIP_Z + hp * np.cos(LEAN)) / 1000.0
    print(f"\npost as printed (hollow, 6 walls of 0.40): section modulus {z_mod:.0f} mm^3")
    for mat, sy in SIGMA.items():
        print(f"  {mat}: breaks at {sy*z_mod/1000/lever:5.0f} N "
              f"({sy*z_mod/1000/lever/4.448:4.0f} lbf) pushed at the slide")
    _, o = tip(0.25, gm, hc, hp)
    print(f"  ...against {o['sideways']:.2f} N to tip the whole stand over "
          f"({SIGMA['PETG']*z_mod/1000/lever/o['sideways']:.0f}x)")


def main() -> None:
    feature_study()
    statics()
    rule("Layer heights that keep 9.6 mm and 0.6 mm on boundaries")
    for lh in (0.08, 0.10, 0.12, 0.15, 0.16, 0.20, 0.24, 0.25, 0.30):
        ok = all(abs(v / lh - round(v / lh)) < 1e-9 for v in (BASE_H, B.LOGO_RELIEF))
        print(f"  {lh:.2f} mm  {'OK ' if ok else 'no '} "
              f"plate {BASE_H/lh:6.1f} layers, inlay {B.LOGO_RELIEF/lh:4.1f}")


if __name__ == "__main__":
    main()
