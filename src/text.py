"""Set a line of text as real outlines, for parts of the mark the raster
cannot carry.

Two runs in the mark are too small in the source to trace well.
"FIREARMS TRAINING" is about 34 px of cap height and the small caps of
"MOUNTAIN MARYLAND" about 47 px, so both inherit that resolution: edges
that should be straight come out soft and the counters close up.  The two
large M's are 177 px and trace cleanly, and they are a drawn lockup rather
than two letters set side by side, so they are left alone.

Each run was matched by normalising cap height, solving tracking to match
the run's width, and scoring pixel overlap against the source.

The sub-text lands in the Helvetica family -- FreeSans Bold Oblique 0.871
and Nimbus Sans Bold Italic 0.870, against 0.791 for Arial's metrics
(Liberation Sans Bold Italic).

The wordmark is a different, much heavier face: its stroke-to-cap ratio is
0.265 against the sub-text's 0.176, so the mark pairs a Bold with a Black.
Archivo Black matches it at 0.885, ahead of Archivo at weight 900 (0.870)
and Asap at 900 (0.865), and well ahead of any Bold.  Every letter of the
wordmark traces 4-7 % narrower than Archivo Black draws it, so the original
face is slightly the narrower of the two; condensing Archivo Black by 3 %
takes the match to 0.895 and, more usefully, brings the tracking needed to
fill the line back near zero, where the letters stop colliding.

Both fonts ship here with their licences; both allow redistribution.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

FONTS = Path(__file__).resolve().parent.parent / "assets" / "fonts"
FONT = FONTS / "FreeSansBoldOblique.ttf"
WORDMARK_FONT = FONTS / "ArchivoBlack-Regular.ttf"

# Settled by the matches described above.  The sub-text's face is already
# oblique and needs only a touch more; Archivo Black is upright, so the
# wordmark carries the mark's full slant.
SLANT_DEG = -1.5
TRACKING_EM = 0.0142
WORDMARK_SLANT_DEG = 12.0
WORDMARK_CONDENSE = 0.97


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
             slant_deg: float = SLANT_DEG, condense: float = 1.0) -> MultiPolygon:
    """Lay out ``text`` and return its outlines, in font units, y up.

    ``condense`` squeezes the finished line horizontally, shapes and spacing
    together, the way a photo-setter would.
    """
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

    if condense != 1.0:
        for a in rings:
            a[:, 0] *= condense

    return _rings_to_polygons(rings)


def fit_line_to_box(text: str, bounds: tuple[float, float, float, float],
                    font_path: Path = FONT, slant_deg: float = SLANT_DEG,
                    condense: float = 1.0) -> MultiPolygon:
    """Set ``text`` to exactly fill ``bounds``.

    Tracking is solved rather than fixed: each run gets whatever spacing
    makes it the right width for the box it has to fill, so a run keeps the
    proportions the artwork gave it instead of being stretched into place.
    """
    tx0, ty0, tx1, ty1 = bounds
    target = (tx1 - tx0) / (ty1 - ty0)

    lo, hi = -0.25, 0.30
    geom = None
    for _ in range(40):
        mid = (lo + hi) / 2
        geom = set_line(text, font_path, mid, slant_deg, condense)
        gx0, gy0, gx1, gy1 = geom.bounds
        if (gx1 - gx0) / (gy1 - gy0) < target:
            lo = mid
        else:
            hi = mid
    return fit_to_box(geom, bounds)


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
