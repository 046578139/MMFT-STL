"""Set a line of text as real outlines, for parts of the mark the raster
cannot carry.

"FIREARMS TRAINING" is only about 34 px of cap height in the source image,
so tracing it inherits every bit of that resolution: edges that should be
straight come out soft and the counters close up.  The wordmark above it is
eight times larger in the same file and traces cleanly, so only this line
needs re-setting.

Matching the source against a range of candidates -- normalising cap height,
solving tracking to match the line's width, and scoring overlap -- puts the
typeface in the Helvetica family: FreeSans Bold Oblique and Nimbus Sans Bold
Italic score 0.872 and 0.871, while Arial's metrics (Liberation Sans Bold
Italic) only reach 0.800.  FreeSans ships here because it is a faithful
Helvetica clone and its licence allows redistribution.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

FONT = Path(__file__).resolve().parent.parent / "assets" / "fonts" / "FreeSansBoldOblique.ttf"

# Settled by the match described above: a touch of extra slant on top of the
# face's own oblique, and a little tracking to reach the line's width.
SLANT_DEG = -1.5
TRACKING_EM = 0.0142


class _PolygonPen(BasePen):
    """Collects glyph contours as flat point loops."""

    def __init__(self, glyph_set, steps: int = 12):
        super().__init__(glyph_set)
        self.steps = steps
        self.contours: list[list[tuple[float, float]]] = []
        self._current: list[tuple[float, float]] = []

    def _moveTo(self, pt):
        self._flush()
        self._current = [pt]

    def _lineTo(self, pt):
        self._current.append(pt)

    def _curveToOne(self, c1, c2, pt):
        p0 = self._current[-1]
        t = np.linspace(0, 1, self.steps + 1)[1:]
        mt = 1 - t
        xs = (mt**3 * p0[0] + 3 * mt**2 * t * c1[0] + 3 * mt * t**2 * c2[0] + t**3 * pt[0])
        ys = (mt**3 * p0[1] + 3 * mt**2 * t * c1[1] + 3 * mt * t**2 * c2[1] + t**3 * pt[1])
        self._current.extend(zip(xs, ys))

    def _closePath(self):
        self._flush()

    def _endPath(self):
        self._flush()

    def _flush(self):
        if len(self._current) >= 3:
            self.contours.append(self._current)
        self._current = []


def _rings_to_polygons(rings: list[np.ndarray]) -> MultiPolygon:
    """Nest contours into polygons with holes, by containment depth."""
    polys = []
    for r in rings:
        p = Polygon(r)
        if not p.is_valid:
            p = p.buffer(0)
        if not p.is_empty and p.area > 0:
            polys.append(Polygon(r))
    polys.sort(key=lambda p: p.area, reverse=True)
    pts = [p.representative_point() for p in polys]

    depth = [sum(1 for j, q in enumerate(polys)
                 if j != i and q.area > p.area and q.contains(pts[i]))
             for i, p in enumerate(polys)]

    out = []
    for i, p in enumerate(polys):
        if depth[i] % 2:
            continue
        holes = [polys[j].exterior.coords for j in range(len(polys))
                 if depth[j] == depth[i] + 1 and p.contains(pts[j])]
        q = Polygon(p.exterior.coords, holes)
        out.append(q if q.is_valid else q.buffer(0))

    merged = unary_union(out)
    return merged if isinstance(merged, MultiPolygon) else MultiPolygon([merged])


def set_line(text: str, font_path: Path = FONT, tracking_em: float = TRACKING_EM,
             slant_deg: float = SLANT_DEG) -> MultiPolygon:
    """Lay out ``text`` and return its outlines, in font units, y up."""
    font = TTFont(font_path)
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap()
    upem = font["head"].unitsPerEm
    hmtx = font["hmtx"]

    shear = np.tan(np.radians(slant_deg))
    rings: list[np.ndarray] = []
    x = 0.0
    for ch in text:
        name = cmap.get(ord(ch))
        if name is None:
            raise KeyError(f"{font_path.name} has no glyph for {ch!r}")
        pen = _PolygonPen(glyph_set)
        glyph_set[name].draw(pen)
        for contour in pen.contours:
            a = np.asarray(contour, float)
            a[:, 0] += x + a[:, 1] * shear
            rings.append(a)
        x += hmtx[name][0] + tracking_em * upem

    return _rings_to_polygons(rings)


def fit_to_box(geom: MultiPolygon, bounds: tuple[float, float, float, float]) -> MultiPolygon:
    """Scale and place ``geom`` so its bounding box matches ``bounds``.

    The scale is uniform and taken from the height, so the line keeps its
    proportions; tracking was already solved so the widths agree.
    """
    from shapely.affinity import scale, translate

    minx, miny, maxx, maxy = geom.bounds
    tx0, ty0, tx1, ty1 = bounds
    s = (ty1 - ty0) / (maxy - miny)
    g = scale(geom, s, s, origin=(minx, miny))
    gx0, gy0, gx1, gy1 = g.bounds
    return translate(g, tx0 + ((tx1 - tx0) - (gx1 - gx0)) / 2 - gx0, ty0 - gy0)
