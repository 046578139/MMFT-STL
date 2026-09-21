#!/usr/bin/env python3
"""Render preview images of the stand into ``docs/images``.

A small software rasteriser -- orthographic, z-buffered, flat-shaded -- so
previews can be regenerated anywhere without a GPU or a headless GL stack.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import trimesh
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
STL = ROOT / "stl"
IMG = ROOT / "docs" / "images"

BLACK = (40, 40, 44)
RED = (196, 28, 32)
BONE = (226, 226, 222)
BG = (247, 247, 245)


def camera(elev: float, azim: float) -> np.ndarray:
    """World -> camera basis for an orthographic view."""
    e, a = np.radians(elev), np.radians(azim)
    fwd = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    # +z is the natural reference up, except when we are looking straight
    # down it and the cross product collapses.
    up_ref = np.array([0.0, 1.0, 0.0]) if abs(fwd[2]) > 0.995 else np.array([0.0, 0.0, 1.0])
    right = np.cross(up_ref, fwd)
    right /= np.linalg.norm(right)
    up = np.cross(fwd, right)
    return np.stack([right, up, fwd])


def render(meshes, colours, path: Path, elev=28.0, azim=125.0, size=1000, margin=1.07,
           supersample=3, crop=None):
    """Rasterise the meshes to ``path``.

    Rendering at ``supersample`` times the final size and scaling back down
    is what keeps edges from looking stepped; without it a render pixel is
    about 0.2 mm of real part and every curve reads as a staircase that is
    not in the geometry.

    ``crop`` is an optional (cx, cy, cz, half_width) in model millimetres for
    a close-up -- cz matters because the default centre sits halfway up the
    blade, well above the plate the mark is on.
    """
    R = camera(elev, azim)
    size = size * supersample
    allv = np.vstack([m.vertices for m in meshes])
    centre = (allv.min(axis=0) + allv.max(axis=0)) / 2
    P = (allv - centre) @ R.T
    half = max(np.ptp(P[:, 0]), np.ptp(P[:, 1])) / 2 * margin
    if crop is not None:
        cx, cy, cz, half = crop
        centre = np.array([cx, cy, cz], float)
    scale = size / (2 * half)

    img = np.empty((size, size, 3), np.float64)
    img[:] = BG
    zbuf = np.full((size, size), -np.inf)

    light = np.array([0.42, 0.34, 0.84])
    light /= np.linalg.norm(light)

    for mesh, colour in zip(meshes, colours):
        v = (mesh.vertices - centre) @ R.T
        sx = v[:, 0] * scale + size / 2
        sy = size / 2 - v[:, 1] * scale
        sz = v[:, 2]
        # Faces pointing away from the camera can never be seen.
        facing = mesh.face_normals @ R[2] > 0
        shade = 0.24 + 0.76 * np.clip(mesh.face_normals @ light, 0, 1)
        base = np.array(colour, float)

        tris = np.stack(
            [np.stack([sx[mesh.faces[:, i]], sy[mesh.faces[:, i]], sz[mesh.faces[:, i]]], 1)
             for i in range(3)], axis=1)

        for ti in np.nonzero(facing)[0]:
            t = tris[ti]
            x0 = int(max(np.floor(t[:, 0].min()), 0))
            x1 = int(min(np.ceil(t[:, 0].max()), size - 1))
            y0 = int(max(np.floor(t[:, 1].min()), 0))
            y1 = int(min(np.ceil(t[:, 1].max()), size - 1))
            if x1 < x0 or y1 < y0:
                continue
            X, Y = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
            det = ((t[1, 1] - t[2, 1]) * (t[0, 0] - t[2, 0])
                   + (t[2, 0] - t[1, 0]) * (t[0, 1] - t[2, 1]))
            if abs(det) < 1e-12:
                continue
            w0 = ((t[1, 1] - t[2, 1]) * (X - t[2, 0]) + (t[2, 0] - t[1, 0]) * (Y - t[2, 1])) / det
            w1 = ((t[2, 1] - t[0, 1]) * (X - t[2, 0]) + (t[0, 0] - t[2, 0]) * (Y - t[2, 1])) / det
            w2 = 1 - w0 - w1
            inside = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
            if not inside.any():
                continue
            z = w0 * t[0, 2] + w1 * t[1, 2] + w2 * t[2, 2]
            window = zbuf[y0:y1 + 1, x0:x1 + 1]
            hit = inside & (z > window)
            if not hit.any():
                continue
            window[hit] = z[hit]
            img[y0:y1 + 1, x0:x1 + 1][hit] = np.clip(base * shade[ti], 0, 255)

    path.parent.mkdir(parents=True, exist_ok=True)
    out = Image.fromarray(img.astype(np.uint8))
    if supersample > 1:
        out = out.resize((size // supersample, size // supersample), Image.LANCZOS)
    out.save(path)
    try:
        print(f"  {path.relative_to(ROOT)}")
    except ValueError:
        print(f"  {path}")


def main() -> None:
    body = trimesh.load(STL / "raised" / "MMFT_Stand_black_body.stl")
    logo = trimesh.load(STL / "raised" / "MMFT_Stand_red_logo_full.stl")
    text = trimesh.load(STL / "raised" / "MMFT_Stand_red_logo_text.stl")
    art = trimesh.load(STL / "raised" / "MMFT_Stand_light_logo_art.stl")

    # The mark reads left to right along +x and the viewer stands at -y,
    # so the useful angles all sit on the negative-y side of the model.
    views = {
        "hero": dict(elev=26, azim=-62),
        "iso": dict(elev=34, azim=-118),
        "top": dict(elev=90, azim=-90),
        "front": dict(elev=7, azim=-90),
        "side": dict(elev=6, azim=-2),
    }
    for name, kw in views.items():
        render([body, logo], [BLACK, RED], IMG / f"2color_{name}.png", **kw)

    render([body, text, art], [BLACK, RED, BONE], IMG / "3color_hero.png", elev=26, azim=-62)
    render([body, text, art], [BLACK, RED, BONE], IMG / "3color_top.png", elev=90, azim=-90)

    single = trimesh.load(STL / "MMFT_Stand_one_piece.stl".replace(
        "MMFT", "raised/MMFT"))
    render([single], [BLACK], IMG / "1color_hero.png", elev=26, azim=-62)

    # A close-up, so the edge quality of the mark is actually visible: at the
    # size of the other renders one pixel is about 0.2 mm of real part.
    render([body, logo], [BLACK, RED], IMG / "detail.png",
           elev=90, azim=-90, supersample=4, crop=(60, 31, 10.4, 19))

    # Raised against flush, lit from a low angle so the relief reads.
    fbody = trimesh.load(STL / "flush" / "MMFT_Stand_black_body.stl")
    flogo = trimesh.load(STL / "flush" / "MMFT_Stand_red_logo_full.stl")
    render([body, logo], [BLACK, RED], IMG / "raised_detail.png",
           elev=20, azim=-68, size=800, supersample=3, crop=(46, 33, 10.4, 21))
    render([fbody, flogo], [BLACK, RED], IMG / "flush_detail.png",
           elev=20, azim=-68, size=800, supersample=3, crop=(46, 33, 10.4, 21))


if __name__ == "__main__":
    main()
