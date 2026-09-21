# Printing the stand

## Which filament

For a stand that lives on a shop counter and has guns lifted off and dropped
back on all day, the answer is **PETG**.

The two things that kill a part like this are not strength in the ordinary
sense — nothing here is near its load limit — but **brittleness** and
**heat**.

* **Brittleness.** The blade prints standing up, so every time a pistol is
  set on it or knocked sideways the load pulls across the layer lines at the
  root. PLA is stiff and strong but notch-sensitive: it takes that kind of
  abuse for months and then snaps clean off one afternoon. PETG is far more
  forgiving — it bends and springs back where PLA cracks, and it welds
  between layers better, which is exactly the direction the load runs.
* **Heat.** PLA starts going soft around 55–60 °C. A black part in a sunny
  window, in a lit display case, or left in a vehicle in July will get
  there. When it does, the blade droops and never comes back. PETG holds its
  shape to about 80 °C.

PETG also keeps its colour under UV far longer than PLA, prints on any
machine without an enclosure, and comes in a good deep black and a strong
red from nearly every brand.

Its one real drawback is that it sticks *too* well to smooth PEI and glass.
Print on a textured plate, or put a thin layer of glue stick down as a
release agent, or you risk taking a chunk of the build surface with the
part.

### If not PETG

| Filament | When it makes sense | Watch out for |
|---|---|---|
| **ASA** | The display sits in direct sun. Best heat and UV resistance of the practical options. | Needs an enclosure; a 160 × 70 mm flat plate will lift at the corners without one. |
| **PCTG** | A tougher PETG, if your supplier carries it. Prints much the same. | Less widely stocked. |
| **PLA+ / Tough PLA** | Climate-controlled room, out of the sun, and you want the crispest possible lettering. | Still softens at ~60 °C. Plain PLA is too brittle here — if you go this route use an impact-modified one. |
| **ABS** | Only if it is what you already run in an enclosure. | Worse UV resistance than ASA, and the fumes. |

Skip the carbon-fibre filled versions. They are stiffer but more brittle,
they chew through brass nozzles, and the fibres dull the fine lettering.

## Settings

Nothing exotic. Start from your printer's stock PETG profile and change:

| Setting | Value | Why |
|---|---|---|
| Layer height | **0.20 mm** | The mark is 0.8 mm tall — exactly four layers. |
| Walls / perimeters | **4** | The blade carries its load in the walls, not the infill. |
| Infill | **30 %**, gyroid or grid | Also adds useful weight to the base. |
| Top layers | **5** | The mark sits on this surface; it needs to be flat and solid. |
| Bottom layers | 4 | |
| Nozzle temp | High end of the range (**typically 240–250 °C** for PETG) | Layer adhesion at the blade root. |
| Part cooling | **30–50 %** | Full blast weakens PETG layer bonding. |
| Supports | **None** | Nothing overhangs. The blade leans 10.9°, well inside what prints unsupported. |
| Orientation | As exported, flat on the plate | Puts the layer lines where they do the most good. |

The solid model is about 155 cm³; at the settings above expect somewhere
around 90–110 g of filament. Your slicer will give you the real number.

## Raised or flush

Pick this first; it decides which folder you print from.

**`stl/flush/` — the mark is let 0.8 mm into the plate, sitting level with
it.** This is what to print for a shop counter. Nothing stands above the
surface, so there is nothing for a muzzle or a slide to catch, and each
piece of the mark is surrounded on all four sides by the black plate — to
move one you would have to break the plate. It needs a multi-material
printer: black and red occupy the same four layers.

**`stl/raised/` — the mark stands 0.8 mm proud.** Print this if you have a
single extruder, because it is the version that can be done with filament
changes. Everything above the top of the plate is mark and nothing else.

The reason the distinction matters is scale. Most of the mark is chunky —
the rifle alone has a 300 mm² footprint. But the two small accent marks in
the wordmark are under 0.75 mm², and raised they are 0.8 mm tall nubs held
on by that much bonded area, loaded in peel if something catches their edge.
Nothing about that is unusual for a raised logo, and plenty of parts live
like that for years; it is simply a failure mode that the flush version does
not have.

The flush version costs more filament in purge — black and red change over
inside every one of those four layers rather than twice for the whole print.
Budget a few extra cubic centimetres of waste.

## Getting the mark in red

### Multi-material printer (AMS, MMU, Palette, IDEX)

Load `MMFT_Stand_black_body.stl` and `MMFT_Stand_red_logo_full.stl` from the
folder you picked into one project, assign black and red, and slice. They
share a coordinate space, so they land in the right place with no alignment
step, and in the flush set the inlay fills its pocket exactly — no gap and
no overlap.

For three colours use `MMFT_Stand_black_body.stl`,
`MMFT_Stand_red_logo_text.stl` and `MMFT_Stand_light_logo_art.stl`.

Most of the filament a multi-material print wastes on this goes to purging
between black and red, not into the part — the mark itself is only 1 cm³.
Flushing into infill or into the object's own sparse regions cuts that down
a lot. Do not cut the flush volume too far on the flush set: black bleeding
into red shows up on the top surface, which is the surface you are looking
at.

### Single-extruder printer

This works because the mark stands proud of a flat plate, so everything
above the top of the plate is mark and nothing else.

Use the **`stl/raised/`** set for this.

1. Slice `raised/MMFT_Stand_one_piece.stl`.
2. Add a filament change at **Z = 10.0 mm** — the top of the plate.
3. Add a second one at **Z = 10.8 mm** — the top of the mark.
4. Load black, and swap to red and back when the printer pauses.

Place the changes by **Z height** in the slicer's preview rather than by
counting layers; a thicker first layer shifts the layer numbers but not the
heights.

* **Bambu Studio / Orca** — right-click the layer slider at that height,
  "Add filament change".
* **PrusaSlicer** — click the `+` on the layer slider at that height.
* **Cura** — Extensions → Post Processing → Modify G-Code → Filament Change,
  read the layer number off the preview at that Z.

Three colours cannot be done this way. The red lettering and the light
firearms sit in the same four layers, so that set needs a multi-material
printer.

### One colour

Two options, neither needing a filament change:

* `raised/MMFT_Stand_one_piece.stl` — the mark standing proud of the plate.
* `flush/MMFT_Stand_engraved_one_piece.stl` — the mark cut into the plate
  instead. Nothing proud of the surface at all, so it is the most durable
  thing here, but the thinnest strokes are about 0.4 mm and a 0.4 mm nozzle
  will skip some of the finest detail in the scope and the pistol. The
  lettering comes through cleanly.

## Before you print a batch

Print one and check the pistol actually sits on it. The blade section came
off the stand this design replaces and has not been tested here against a
real firearm. If it is tight, a few passes with sandpaper along the blade
sorts it out; if it is loose, raise `BLADE_HX` / `BLADE_HY` in
`src/build.py` by a few tenths and rebuild.

A few felt pads or a strip of rubber mat on the underside keeps it from
sliding on a glass counter and stops it marking the surface.
