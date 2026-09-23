# Printing the stand

## On a Bambu Lab H2C

Open **`3mf/MMFT_Stand_flush_2color.3mf`** and print it in **Bambu PETG
Basic**, black and red.

That one file holds both parts, already positioned and already tagged with
the filament slot each wants, so there is nothing to import twice or line up
by hand. The `stl/flush/` set is the same model if you would rather load the
parts yourself.

**On PETG Basic rather than PETG HF.** HF was the recommendation here until
Bambu began phasing it out in every colour but black and brought back a
reformulated Basic in its place, so for a three-colour print HF may simply
not be available in red or white. Basic is the better choice regardless:
published figures put it ahead on flexural strength, layer adhesion and
impact, and it was reformulated specifically to string less and pick up
less moisture. Stringing is the one that matters on this model — the flush
inlay puts three colours inside the same three layers, so there are a lot
of tool changes happening right at the surface you end up looking at. What
you give up is HF's matte finish; Basic is glossier, which is a matter of
taste rather than a defect.

Either way, dry it first. PETG is hygroscopic and a damp spool strings
badly, which again lands on the visible face. The AMS 2 Pro is heated for
exactly this — a few hours in it before the print is enough.

Third-party PETG works too. You lose the RFID profile, so pick a generic
PETG profile and dry the spool yourself.

For the three-colour set, take the light colour from the same range as the
other two so all three behave identically on the plate.

**On purging.** The H2C can assign filaments across nozzles and swap
hotends rather than purge, which is why a flush inlay costs so little here
compared with a single-hotend machine. That only holds when the filaments
actually end up spread across nozzles — check the Filament Grouping panel.
With all three assigned to one nozzle every colour change is a real purge,
and "Regroup filament" is worth a click before slicing.

One thing worth trying: the thinnest features in the mark are 0.42 mm
against a 0.4 mm nozzle, which works but with nothing to spare. The H2C
ships with a 0.2 mm hotend, so if the finest detail in the scope and the
pistol matters to you, it is worth checking whether your slicer will let you
drive the mark with the 0.2 mm and the rest of the part with a 0.4 mm. I
have not verified that this particular combination is supported — confirm it
in Bambu Studio before planning a batch around it.

### "The 3mf file has invalid config, load geometry data only"

Bambu Studio says this when you open one of these files. **It is expected,
and nothing is wrong.**

The message is about the *print profile* -- printer, nozzle, filament
settings -- not about the model. Bambu Studio shows it for any 3MF that is
not one of its own project files, which includes files out of Fusion,
Onshape, SolidWorks and everything else. These files deliberately carry no
print profile: guessing your printer and filament settings and quietly
overwriting your own would be worse than the notice.

Click OK. The geometry, the parts and their filament assignments all load.

**Worth a glance once you have:** the object list should show *MMFT Pistol
Stand* with two parts under it (or three, for the three-colour file), each
with its own filament number. If it does, everything came through and you
can slice.

If the filament numbers did not come through, it is two clicks -- right-click
each part and set its filament -- or load the matching `stl/` pair and assign
them there. The parts are in the same coordinate space either way, so
nothing needs lining up.

For the record, the packages are built to the specification: the reference
3MF library reads them with zero warnings, and the per-part filament slots
are written the way Bambu Studio's own importer expects (`<part>` matched to
its sub-object id, `subtype="normal_part"`, filament under a `<metadata
key="extruder">`).

## Which filament

For a stand that lives on a shop counter and has guns lifted off and
dropped back on all day, the answer is **PETG** — but for one reason, not
the two I would have guessed.

**Strength does not come into it.** The post's root section has a modulus
of 4314 mm³, and a Glock 17 leaning at 10.9° puts a moment of 0.118 N·m
into it. That is a stress of **0.028 MPa**, against roughly 35 MPa for PLA
across its layer lines — a safety factor of about **1275**. A steel-framed
P226 makes it 0.037 MPa. Five kilos of someone leaning on the post is
0.20 MPa, still 170× under. Nothing about holding a pistol troubles any
filament you might reasonably load.

So infill in the base is **ballast, not structure** — a heavier plate sits
better on a counter, and that is the only reason to run 30 %.

What is left is **heat**, and that one is real rather than theoretical.
PLA starts going soft around 55–60 °C. A dark part in a sunny window, in a
lit display case, or in a vehicle in July gets there easily. When it does
the post droops under a load it would otherwise ignore forever, and it does
not come back. PETG holds its shape to about 80 °C. That margin, plus
better UV stability over months of window light, is the whole case.

Impact matters a little as well — PLA is notch-sensitive where PETG bends
and springs back — but it is a second-order argument, not the main one.

**If the stands stay indoors, away from windows, and never travel in a hot
vehicle, PLA is a perfectly sound choice.** An impact-modified one beats
plain, and a matte finish suits a display piece. It renders the fine logo
detail marginally more crisply than PETG and is easier on a 215 mm flat
plate. The case for PETG is environmental, not structural.

**Whatever you pick, use the same material family for all three colours.**
PETG and PLA barely bond to one another, and on the flush inlay the colours
interlock inside the same three layers — a mixed print would leave the mark
sitting in its pocket with nothing holding it there.

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
| **ASA** | The display sits in direct sun. Best heat and UV resistance of the practical options. | Needs an enclosure; a 215 × 98 mm flat plate will lift at the corners without one. |
| **PCTG** | A tougher PETG, if your supplier carries it. Prints much the same. | Less widely stocked. |
| **PLA+ / Tough PLA** | Climate-controlled room, out of the sun, and you want the crispest possible lettering. | Still softens at ~60 °C. Plain PLA is too brittle here — if you go this route use an impact-modified one. |
| **ABS** | Only if it is what you already run in an enclosure. | Worse UV resistance than ASA, and the fumes. |

Skip the carbon-fibre filled versions. They are stiffer but more brittle,
they chew through brass nozzles, and the fibres dull the fine lettering.

## Settings

Nothing exotic. Start from your printer's stock PETG profile and change:

| Setting | Value | Why |
|---|---|---|
| Nozzle | **0.4 mm** | See below — a 0.6 mm nozzle cannot render this mark. |
| Layer height | **0.20 mm** | Plate, pocket floor and inlay all land exactly on layer boundaries. 0.30, 0.15 and 0.12 mm do too. |
| Seam position | **Scarf joint** | Otherwise the seams stack into a visible line up one face of the post. |
| Walls / perimeters | **4** | The blade carries its load in the walls, not the infill. |
| Infill | **30 %**, gyroid or grid | Also adds useful weight to the base. |
| Top layers | **5** | The mark sits on this surface; it needs to be flat and solid. |
| Bottom layers | 4 | |
| Nozzle temp | High end of the range (**typically 240–250 °C** for PETG) | Layer adhesion at the blade root. |
| Part cooling | **30–50 %** | Full blast weakens PETG layer bonding. |
| Supports | **None** | Nothing overhangs. The blade leans 10.9°, well inside what prints unsupported. |
| Orientation | As exported, flat on the plate | Puts the layer lines where they do the most good. |

The solid model is about 246 cm³; at the settings above expect somewhere
around 140–170 g of filament. Your slicer will give you the real number.

### Why a 0.4 mm nozzle, and not 0.6

Not because the strokes are thin — at this size the thinnest is 0.48 mm. It
is the **gaps**. Between the letters, and between the lettering and the
firearms, the plate colour has to be laid down in a narrow channel, and a
nozzle cannot lay a bead narrower than itself. Where the channel is too
narrow the slicer puts nothing there at all, and you get an empty trench
instead of a clean edge.

At 0.4 mm there is now nothing in the mark it cannot fill. At 0.6 mm five
channels are still too narrow, mostly around the sub-text — printable, but
expect those few to close up.

An earlier version of this model made the problem far worse. Every stroke
was grown 0.15 mm per side so that the finest details would survive, which
worked, but growing strokes narrows the gaps between them by the same
amount: it left 21 channels a 0.4 mm nozzle could not fill, and 29 for a
0.6 mm. Scaling the mark up and cutting that growth to 0.05 mm fixed both
ends at once.

| | thinnest stroke | gaps a 0.4 mm nozzle can't fill | gaps a 0.6 mm can't fill |
|---|---|---|---|
| Old: 90 mm mark, 0.15 mm growth | 0.57 mm | 21 | 29 |
| **Now: 145 mm mark, 0.05 mm growth** | **0.48 mm** | **0** | **5** |

### The line up one side of the post

That is the seam, not the model — every perimeter loop has to start and stop
somewhere, and by default Bambu Studio stacks them all at the same angle so
they form a line. Set **Seam position** to **Scarf joint** and it all but
disappears. There is only ever one seam per loop, which is why the far side
is smooth.

The ridge over the *top* of the post is a different thing and is meant to be
there: it is the chisel-shaped lead-in, carried over from the stand this one
replaces.

## Raised or flush

Pick this first; it decides which folder you print from.

**`stl/flush/` — the mark is let 0.6 mm into the plate, sitting level with
it.** This is what to print for a shop counter. Nothing stands above the
surface, so there is nothing for a muzzle or a slide to catch, and each
piece of the mark is surrounded on all four sides by the black plate — to
move one you would have to break the plate. It needs a multi-material
printer: black and red occupy the same three layers.

**`stl/raised/` — the mark stands 0.6 mm proud.** Print this if you have a
single extruder, because it is the version that can be done with filament
changes. Everything above the top of the plate is mark and nothing else.

The reason the distinction matters is scale, though far less than it used
to. Since the mark was scaled up, the smallest piece of lettering has a
9.6 mm² footprint and the rifle alone has 1900 mm² — raised, none of that is
delicate. What is still small are the two slivers of the scope's crosshair
showing through the gaps in "ND", at 0.71 and 1.02 mm². Raised, those are
0.6 mm tall nubs held on by that much bonded area and loaded in peel if
something catches an edge. Nothing about that is unusual for a raised logo,
and plenty of parts live like that for years; it is simply a failure mode
the flush version does not have at all.

The flush version costs more filament in purge — black and red change over
inside every one of those three layers rather than twice for the whole print.
Budget a few extra cubic centimetres of waste. This does not apply to a
printer that swaps hotends rather than purging, such as the H2C.

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
2. Add a filament change at **Z = 9.6 mm** — the top of the plate.
3. Add a second one at **Z = 10.2 mm** — the top of the mark.
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
firearms sit in the same three layers, so that set needs a multi-material
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
