"""Small solid-modelling helpers: rounded rectangles, lofts, extrusions."""

from __future__ import annotations

import numpy as np
import trimesh
from shapely.geometry import MultiPolygon


def rounded_rect(hx: float, hy: float, r: float, n: int = 160) -> np.ndarray:
    """A rounded rectangle centred on the origin, as an (n, 2) point loop.

    Points are spaced evenly along the perimeter and the count is fixed, which
    is what lets :func:`loft` stitch a stack of these together without having
    to solve a correspondence problem.  Sampling by arc length rather than by
    quadrant keeps the points distinct even when the shape degenerates -- at
    the tip of the blade the corner radius grows to equal the half-width and
    the straight runs vanish entirely.
    """
    r = max(0.0, min(r, hx, hy))
    a, b = hx - r, hy - r

    # Perimeter, anticlockwise from (hx, 0): up the right side, round the
    # corner, across the top, and so on back to the start.
    quarter = 0.5 * np.pi * r
    segs = [
        ("line", b, (hx, 0.0), (hx, b)),
        ("arc", quarter, (a, b), 0.0),
        ("line", 2 * a, (a, hy), (-a, hy)),
        ("arc", quarter, (-a, b), 0.5 * np.pi),
        ("line", 2 * b, (-hx, b), (-hx, -b)),
        ("arc", quarter, (-a, -b), np.pi),
        ("line", 2 * a, (-a, -hy), (a, -hy)),
        ("arc", quarter, (a, -b), 1.5 * np.pi),
        ("line", b, (hx, -b), (hx, 0.0)),
    ]
    lengths = np.array([s[1] for s in segs])
    edges = np.concatenate([[0.0], np.cumsum(lengths)])
    total = edges[-1]

    s = np.linspace(0.0, total, n, endpoint=False)
    idx = np.clip(np.searchsorted(edges, s, side="right") - 1, 0, len(segs) - 1)

    pts = np.empty((n, 2))
    for k, seg in enumerate(segs):
        sel = idx == k
        if not sel.any():
            continue
        length = lengths[k]
        t = np.zeros(sel.sum()) if length <= 0 else (s[sel] - edges[k]) / length
        if seg[0] == "line":
            p0 = np.array(seg[2])
            p1 = np.array(seg[3])
            pts[sel] = p0 + np.outer(t, p1 - p0)
        else:
            centre = np.array(seg[2])
            ang = seg[3] + t * (0.5 * np.pi)
            pts[sel] = centre + np.stack([np.cos(ang), np.sin(ang)], axis=1) * r
    return pts


def loft(sections: list[tuple[float, np.ndarray, tuple[float, float]]]) -> trimesh.Trimesh:
    """Stitch equal-length point loops stacked in z into a closed solid.

    Each section is ``(z, points, (dx, dy))`` -- the offset lets a stack lean
    without changing its cross-section.  Winding is set up by hand and the
    mesh is built unprocessed, so coincident points in a degenerate section
    cannot be merged away and break the topology.
    """
    n = len(sections[0][1])
    assert all(len(p) == n for _, p, _ in sections), "sections must match in length"

    rings = []
    for z, pts, (dx, dy) in sections:
        ring = np.empty((n, 3))
        ring[:, 0] = pts[:, 0] + dx
        ring[:, 1] = pts[:, 1] + dy
        ring[:, 2] = z
        rings.append(ring)
    V = np.vstack(rings)

    faces = []
    for k in range(len(sections) - 1):
        a, b = k * n, (k + 1) * n
        for i in range(n):
            j = (i + 1) % n
            # Sections run anticlockwise and stack upwards, so this winding
            # points outwards.
            faces.append([a + i, a + j, b + j])
            faces.append([a + i, b + j, b + i])

    last = (len(sections) - 1) * n
    bottom_c, top_c = len(V), len(V) + 1
    V = np.vstack([V, rings[0].mean(axis=0), rings[-1].mean(axis=0)])
    for i in range(n):
        j = (i + 1) % n
        faces.append([bottom_c, j, i])                 # faces down
        faces.append([top_c, last + i, last + j])      # faces up

    return trimesh.Trimesh(vertices=V, faces=np.array(faces), process=False)


def extrude(polys: MultiPolygon, z0: float, height: float) -> trimesh.Trimesh:
    """Extrude 2D shapely geometry into a solid sitting at ``z0``."""
    parts = []
    for p in polys.geoms:
        if p.area <= 1e-9:
            continue
        solid = trimesh.creation.extrude_polygon(p, height, engine="earcut")
        solid.apply_translation((0.0, 0.0, z0))
        parts.append(solid)
    return trimesh.util.concatenate(parts)


def union(meshes: list[trimesh.Trimesh]) -> trimesh.Trimesh:
    """Boolean union via manifold3d."""
    if len(meshes) == 1:
        return meshes[0]
    return trimesh.boolean.union(meshes, engine="manifold")
