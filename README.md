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

### Files

| File | Colour | Used by |
|---|---|---|
| `stl/MMFT_Stand_black_body.stl` | black | 2- and 3-colour sets |
| `stl/MMFT_Stand_red_logo_full.stl` | red | 2-colour set |
| `stl/MMFT_Stand_red_logo_text.stl` | red | 3-colour set |
| `stl/MMFT_Stand_light_logo_art.stl` | bone / silver / white | 3-colour set |
| `stl/MMFT_Stand_one_piece.stl` | any single colour | on its own |

Every part is modelled in the same coordinate space, so a multi-material
slicer only needs them loaded together and assigned colours — there is
nothing to line up by hand.

**Printing it in two colours on a single-extruder printer** works too,
because the mark stands 0.8 mm proud of an otherwise flat plate: slice
`MMFT_Stand_one_piece.stl`, add a filament change at **Z = 10.0 mm** and
another at **Z = 10.8 mm**, and the four layers in between come out red.
See [docs/PRINTING.md](docs/PRINTING.md) for settings and filament choice.

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
