"""
Vectorise the Mountain Maryland Firearms Training logo from a raster image
into 2D polygons suitable for extrusion into printable geometry.

The logo is a flat black-on-white mark.  We threshold it, split it into its
semantic parts (rifle / scope / wordmark / rule / sub-text / pistol) by
connected component, trace sub-pixel contours, and hand back shapely
geometry in millimetres.

A small outward offset ("bold") is applied so that every stroke survives a
0.4 mm nozzle -- the scope reticle ring and the finer pistol details are
well under half a millimetre at the size we print them.
"""

from __future__ import annotations

import numpy as np
from PIL import Image
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union
from skimage import measure

import text as text_mod

# The runs the source raster is too small to carry; see text.py.  The two
# large M's are left as traced: they are big enough in the source, and they
# are a drawn lockup rather than two letters set side by side.
SUBTEXT_LINE = "FIREARMS TRAINING"
WORDMARK_UPPER = "OUNTAIN"
WORDMARK_LOWER = "ARYLAND"

# The artwork holds the scope's ring and crosshair off the wordmark by a
# thin white halo.  Re-set letters are cut back by the same amount so the
# scope still reads as passing in front of them.
KNOCKOUT_MM = 0.35

# Semantic grouping of the logo's connected components.
GROUPS = ("rifle", "scope", "wordmark", "rule", "subtext", "pistol")

# Parts that carry lettering -- these are the ones that go red.
TEXT_GROUPS = ("wordmark", "rule", "subtext")
ART_GROUPS = ("rifle", "scope", "pistol")


def _load_gray(path: str, px_per_mm: float, width_mm: float) -> np.ndarray:
    """Load the logo, flatten onto white, and resample to the print raster."""
    im = Image.open(path).convert("RGBA")
    im = Image.alpha_composite(Image.new("RGBA", im.size, (255, 255, 255, 255)), im)
    im = im.convert("L")
    w = int(round(width_mm * px_per_mm))
    h = int(round(w * im.height / im.width))
    return np.asarray(im.resize((w, h), Image.LANCZOS), dtype=np.float64) / 255.0


def _classify(prop, shape) -> str:
    """Assign one connected component to a semantic group.

    Thresholds are expressed as fractions of the raster so they hold at any
    resolution.  They key off the layout of this particular mark: the rifle
    is the full-height silhouette on the left, the scope is the big circle
    top right, the pistol sits under it, the rule is the long thin bar, and
    everything below the rule is the "FIREARMS TRAINING" line.
    """
    H, W = shape
    r0, c0, r1, c1 = prop.bbox
    h, w = (r1 - r0) / H, (c1 - c0) / W
    left, top = c0 / W, r0 / H
    right = c1 / W

    if right < 0.21 and h > 0.82:
        return "rifle"
    if left > 0.73 and top < 0.25 and h > 0.37:
        return "scope"
    if top > 0.63 and left > 0.85:
        return "pistol"
    if h < 0.05 and w > 0.46:
        return "rule"
    if top > 0.70:
        return "subtext"
    return "wordmark"


def _contours_to_polygons(contours, to_mm) -> MultiPolygon:
    """Turn a set of closed contours into polygons, nesting holes correctly.

    ``find_contours`` gives us every boundary -- outlines and the counters of
    letters alike -- with no indication of which is which.  Depth of nesting
    decides: a ring contained by an even number of other rings is solid, an
    odd number makes it a hole.
    """
    rings = []
    for c in contours:
        pts = to_mm(c)
        if len(pts) < 4:
            continue
        poly = Polygon(pts)
        if not poly.is_valid:
            poly = poly.buffer(0)
        if poly.is_empty or poly.area <= 0:
            continue
        rings.append(Polygon(pts))

    rings.sort(key=lambda p: p.area, reverse=True)
    prepared = [(p, p.representative_point()) for p in rings]

    depth = []
    for i, (p, _) in enumerate(prepared):
        d = 0
        for j, (q, _) in enumerate(prepared):
            if i != j and q.area > p.area and q.contains(prepared[i][1]):
                d += 1
        depth.append(d)

    solids = []
    for i, (p, _) in enumerate(prepared):
        if depth[i] % 2 != 0:
            continue
        # Holes are the rings one level deeper that sit directly inside p.
        holes = [
            q.exterior.coords
            for j, (q, pt) in enumerate(prepared)
            if depth[j] == depth[i] + 1 and p.contains(pt)
        ]
        poly = Polygon(p.exterior.coords, holes)
        if not poly.is_valid:
            poly = poly.buffer(0)
        if not poly.is_empty:
            solids.append(poly)

    merged = unary_union(solids)
    return merged if isinstance(merged, MultiPolygon) else MultiPolygon([merged])


def _reset_wordmark(raw: dict) -> tuple[MultiPolygon, list]:
    """Re-set the wordmark's two small-cap runs, keeping the M lockup.

    Returns the rebuilt wordmark and any stray pieces that turned out not to
    be lettering at all.
    """
    block = raw["wordmark"].bounds
    height = block[3] - block[1]

    kept, strays = [], []
    runs: dict[str, list] = {"upper": [], "lower": []}
    for poly in raw["wordmark"].geoms:
        x0, y0, x1, y1 = poly.bounds
        tall = (y1 - y0) / height
        centre = ((y0 + y1) / 2 - block[1]) / height
        if tall > 0.6:
            kept.append(poly)                     # the two large M's
        elif tall < 0.12:
            strays.append(poly)                   # not a letter
        else:
            runs["upper" if centre > 0.5 else "lower"].append(poly)

    # Everything the artwork draws in front of the lettering, plus the strays,
    # which are part of the scope and so knock out of the letters too.
    in_front = unary_union(
        [raw[g] for g in ("scope", "rifle", "pistol") if g in raw] + strays
    ).buffer(KNOCKOUT_MM)

    rebuilt = list(kept)
    for key, line in (("upper", WORDMARK_UPPER), ("lower", WORDMARK_LOWER)):
        if not runs[key]:
            continue
        box = unary_union(runs[key]).bounds
        geom = text_mod.fit_line_to_box(
            line, box, text_mod.WORDMARK_FONT,
            text_mod.WORDMARK_SLANT_DEG, text_mod.WORDMARK_CONDENSE,
        )
        rebuilt.append(geom.difference(in_front))

    merged = unary_union(rebuilt)
    return (merged if isinstance(merged, MultiPolygon) else MultiPolygon([merged]),
            strays)


def vectorise(
    path: str,
    width_mm: float,
    px_per_mm: float = 24.0,
    bold_mm: float = 0.15,
    simplify_mm: float = 0.02,
    set_subtext: bool = True,
    set_wordmark: bool = True,
) -> dict:
    """Return ``{group: MultiPolygon}`` in millimetres.

    The logo is placed with its bounding box origin at (0, 0) and y pointing
    up, so callers only have to translate it into place.

    ``bold_mm`` grows every stroke by that much per side.  At our print size
    the scope ring is about 0.42 mm and parts of the pistol are thinner
    still; 0.15 mm per side lifts everything to a width a 0.4 mm nozzle can
    actually lay down, and is far too small to read as a change of weight.

    ``set_subtext`` and ``set_wordmark`` replace the traced lettering with
    the same runs set from outlines.  "FIREARMS TRAINING" is about 34 px of
    cap height in the source and the wordmark's small caps about 47 px, too
    little to trace cleanly either way.  The two large M's are 177 px and
    are left as traced.
    """
    gray = _load_gray(path, px_per_mm, width_mm)
    H, W = gray.shape
    mask = gray < 0.5

    labels = measure.label(mask, connectivity=2)
    props = measure.regionprops(labels)

    buckets: dict[str, list[int]] = {g: [] for g in GROUPS}
    for p in props:
        buckets[_classify(p, gray.shape)].append(p.label)

    def to_mm(contour: np.ndarray) -> np.ndarray:
        # contour is (row, col); flip rows so y points up.
        xy = np.empty((len(contour), 2))
        xy[:, 0] = contour[:, 1] / px_per_mm
        xy[:, 1] = (H - 1 - contour[:, 0]) / px_per_mm
        return xy

    raw: dict[str, MultiPolygon] = {}
    for group, lab_ids in buckets.items():
        if not lab_ids:
            continue
        sel = np.isin(labels, lab_ids)
        # Trace on the greyscale (not the binary mask) so contours land on the
        # sub-pixel edge; mask to this group, padding by a couple of pixels so
        # the component's own anti-aliased fringe is kept.
        from scipy import ndimage

        near = ndimage.binary_dilation(sel, iterations=3)
        g = np.where(near, gray, 1.0)
        g = np.pad(g, 2, constant_values=1.0)
        contours = measure.find_contours(g, 0.5)
        raw[group] = _contours_to_polygons([c - 2 for c in contours], to_mm)

    # Swap the traced lettering for properly set outlines, dropped into the
    # boxes the traced runs occupied so they land where the artwork puts
    # them.
    if set_subtext and "subtext" in raw:
        raw["subtext"] = text_mod.fit_line_to_box(SUBTEXT_LINE, raw["subtext"].bounds)

    if set_wordmark and "wordmark" in raw:
        raw["wordmark"], strays = _reset_wordmark(raw)
        if strays and "scope" in raw:
            # Slivers of the scope's crosshair, showing through the gaps in
            # "ND", that land in the wordmark's band and get grouped with it.
            # They belong to the scope, and in the three-colour set that is
            # the difference between printing them red and printing them
            # with the rest of the optic.
            raw["scope"] = unary_union([raw["scope"], *strays])

    out: dict[str, MultiPolygon] = {}
    for group, polys in raw.items():
        if simplify_mm:
            polys = polys.simplify(simplify_mm, preserve_topology=True)
        if bold_mm:
            polys = polys.buffer(bold_mm, join_style=1, quad_segs=6)
        polys = polys.buffer(0)
        out[group] = polys if isinstance(polys, MultiPolygon) else MultiPolygon([polys])

    # Normalise so the whole mark starts at (0, 0).
    all_geom = unary_union(list(out.values()))
    minx, miny, _, _ = all_geom.bounds
    from shapely.affinity import translate

    return {g: translate(p, -minx, -miny) for g, p in out.items()}
