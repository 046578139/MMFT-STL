# MMFT-STL

3D-printable models for **Mountain Maryland Firearms Training**.

## Pistol display stand

A counter-top display stand: a filleted base plate with a leaning
magazine-well blade at one end and the MMFT mark standing proud of the plate
in front of it. Designed to print in a black body with the mark in red.

![The stand in black with a red mark](docs/images/2color_hero.png)

| | |
|---|---|
| ![top](docs/images/2color_top.png) | ![three colour](docs/images/3color_hero.png) |
| Two colours — black and red | Three colours — lettering red, firearms bone |

**160 × 70 × 71 mm.** Fits any bed from 180 mm up. No supports, no bridging,
flat on the plate.

### Raised or flush

The mark comes two ways. Both look the same from straight on; they differ
in whether it stands on the plate or is let into it.

| ![raised](docs/images/raised_detail.png) | ![flush](docs/images/flush_detail.png) |
|---|---|
| **`stl/raised/`** — stands 0.8 mm proud | **`stl/flush/`** — let 0.8 mm into the plate |

**Flush is the one to print for a shop counter.** Nothing stands above the
surface to be caught or chipped, and every piece of the mark is boxed in on
all four sides by the black around it — a muzzle dragged across it just
slides. It needs a multi-material printer, because black and red share the
same four layers.

**Raised** is there because it prints in two colours on *any* printer. Every
layer above the plate is mark and nothing else, so a single extruder only
needs a filament change at Z = 10.0 mm and another at Z = 10.8 mm. The
trade-off is that a few pieces are small: the two accent marks in the
wordmark have a footprint under 0.75 mm², which is not much holding a 0.8 mm
tall nub. Most of the mark is far sturdier than that, but those are the
pieces that would go first.

### Files

| File | Colour | Set |
|---|---|---|
| `raised/MMFT_Stand_black_body.stl` | black | 2- and 3-colour |
| `raised/MMFT_Stand_red_logo_full.stl` | red | 2-colour |
| `raised/MMFT_Stand_red_logo_text.stl` | red | 3-colour |
| `raised/MMFT_Stand_light_logo_art.stl` | bone / silver / white | 3-colour |
| `raised/MMFT_Stand_one_piece.stl` | any single colour | on its own |
| `flush/MMFT_Stand_black_body.stl` | black | 2- and 3-colour |
| `flush/MMFT_Stand_red_logo_full.stl` | red | 2-colour |
| `flush/MMFT_Stand_red_logo_text.stl` | red | 3-colour |
| `flush/MMFT_Stand_light_logo_art.stl` | bone / silver / white | 3-colour |
| `flush/MMFT_Stand_engraved_one_piece.stl` | any single colour | on its own |

Every part is modelled in the same coordinate space, so a multi-material
slicer only needs them loaded together and assigned colours — there is
nothing to line up by hand. The flush body and its inlay reassemble into the
solid plate to within a hundred-thousandth of a cubic millimetre, with no
overlap for a slicer to argue with.

`flush/MMFT_Stand_engraved_one_piece.stl` is the flush plate with its
pockets left empty — one colour, nothing proud of the surface at all. The
thinnest strokes are around 0.4 mm, so a 0.4 mm nozzle will skip some of the
finest detail in the scope and the pistol; the lettering comes through
cleanly.

See [docs/PRINTING.md](docs/PRINTING.md) for settings and filament choice.

### How crisp is the mark?

It is traced as vector outlines, not stamped from pixels — straight edges
come out exactly straight (the rule under the wordmark is two points across
46 mm) and the scope ring is round to 0.026 mm RMS, about a fifteenth of an
extrusion width. Nothing in the geometry is stepped.

![detail](docs/images/detail.png)

The preview images are rendered at a size where one pixel is roughly 0.2 mm
of real part, so curves in them can look stepped when the model is not.
`src/preview.py` supersamples to keep that under control.

### The "FIREARMS TRAINING" line

Everything in the mark traces well except this one line, and for a reason
the tracing cannot fix: in the source image it is only about **34 px** of
cap height. There is no detail in the file to recover.

![before and after](docs/images/subtext_before_after.png)

*Traced from the raster, then the same line set from outlines.*

So it is re-set from type instead. Matching the source against a range of
candidates — normalising cap height, solving tracking to match the line's
width, and scoring pixel overlap — puts the typeface squarely in the
**Helvetica** family:

| Candidate | Overlap with the source |
|---|---|
| FreeSans Bold Oblique (Helvetica clone) | **0.872** |
| Nimbus Sans Bold Italic (Helvetica clone) | 0.871 |
| Arial metrics (Liberation Sans Bold Italic) | 0.800 |
| Barlow Bold Italic | 0.609 |

The two Helvetica clones tie and Arial is clearly behind, so the line is set
in FreeSans Bold Oblique with 1.4 % tracking and 1.5° of extra slant — the
values that matched — and dropped into the box the traced line occupied, so
it lands exactly where the artwork puts it. Stroke weight comes out at
1.08 mm median against the traced line's 1.05 mm, so the line reads at the
same weight; only the edges change.

The wordmark above it is eight times larger in the same file and traces
cleanly, so it is left alone.

**If you have the original vector logo** (`.ai`, `.eps`, `.svg` or a vector
`.pdf`), that would beat all of this — send it over and the whole mark can
come from it rather than from a 720 px raster.

### Regenerating

The models are generated, not hand-modelled — every dimension is a named
constant near the top of `src/build.py`, and the mark is traced from
`assets/mmft_logo.png` at build time. Change the plate size, move the mark,
swap the artwork, and rebuild:

```sh
pip install -r requirements.txt
python src/build.py      # writes stl/
python src/preview.py    # writes docs/images/
```

| Module | What it does |
|---|---|
| `src/build.py` | Dimensions, the stand, and the exported part sets |
| `src/logo.py` | Traces the logo raster into polygons, splits it into its parts |
| `src/geometry.py` | Rounded rectangles, lofts, extrusions, booleans |
| `src/preview.py` | Renders the images in `docs/images` |

### About the blade

The blade's dimensions are carried over from a Glock-branded stand supplied
as the starting point for this design, so anything that fitted that one fits
this: a 33.67 × 22.84 mm rounded-rectangle section with 6.5 mm corners,
leaning 10.89°, standing 61.1 mm clear of the plate, with a chisel-shaped
lead-in at the tip. The root fillet is opened up from 3.57 mm to 4 mm for
strength. The plate around it and the mark on it are new work, written from
scratch in `src/` — no part of the original mesh is redistributed here.

> If that original model carried a licence, it is worth checking before
> selling prints of this one. The blade section is a functional dimension
> rather than creative expression, but we did take it from somewhere.

### Sizing it to a different pistol

The blade is what sets the fit. `BLADE_HX`, `BLADE_HY` and `BLADE_R` in
`src/build.py` are the half-width, half-depth and corner radius of its
constant section; `BLADE_RISE` is how far it stands above the plate and
`BLADE_LEAN` is how far it moves in x per mm of height. Print the blade on
its own first and check it before committing to a full plate.
