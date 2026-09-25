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

**On purging, and why the flush inlay is nearly free on this machine.**
An earlier version of this note said that assigning all three colours to
one nozzle would make every colour change a real purge, and that they
needed spreading across nozzles. That is how a conventional AMS printer
behaves, and it is wrong for the H2C.

The H2C's right-hand side is the Vortek system: a rack of up to six
induction-heated hotends that the printhead physically swaps, heating each
one to temperature in about eight seconds. The left nozzle is a
conventional fixed hotend that cannot be changed mid-print. Each filament
gets its own dedicated hotend, so changing colour means stowing one hotend
and picking up another rather than pushing a new colour through the old
one. **Up to seven filaments — one on the left plus six on the Vortek rack
— print with no purge flushing at all.**

This print uses three. Whether they sit entirely on the right-hand AMS
units or are split across left and right makes no difference to waste:
three is comfortably under seven either way, so there is nothing to purge
and nothing to regroup. All three on the right is the simpler arrangement
and the one to use.

This is exactly why the flush inlay is the right choice here. On a
single-hotend printer it would be the expensive option — black and red
change over inside every one of the inlay's layers instead of twice for
the whole print. On the H2C those changes are hotend swaps, so the flush
version costs essentially nothing extra.

The one thing worth confirming in the preview is that the slicer really did
give each colour its own hotend rather than reusing one. If it has, the
prime tower will be small and there will be no flush volume between
colours.

The tightest thing in the mark is a 0.460 mm gap between two separate
shapes, and a 0.4 mm nozzle clears it by 0.06 mm — it works, but with very
little to spare. An obvious thought is to use the H2C's 0.2 mm hotend for
the two logo bodies and the 0.4 mm for the plate and post, which would give
those gaps better than twice the clearance they need.

**This is not possible, and the machine says so itself.** Bambu Studio's
Sync Nozzle dialog states plainly: *"Mixing nozzle diameters in one print is
not supported. If the selected size is only on one extruder, single-extruder
printing will be enforced."* Pick one diameter for the whole print.

That dialog also settles which diameter, because it reports how many of each
size the machine can reach on each extruder. On this printer, 0.2 mm is
available on the right extruder only — selecting it would force
single-extruder printing and **lose the multi-colour capability entirely**.
0.4 mm is available on both, so it is the only size that both renders the
mark and keeps the flush inlay possible.

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

**Strength does not come into it.** Take the post as it actually prints —
hollow, six walls of 0.40 mm, ignoring the infill entirely — and its root
section modulus is 1663 mm³. Against PETG's roughly 45 MPa across its layer
lines, the post does not fail until something pushes **578 N (130 lbf)**
sideways at the slide. In PLA it is 450 N (101 lbf).

You will never see those numbers, because **the stand tips over at 2.9 N
(0.65 lbf)** — about 200× sooner. Every failure mode this design has is a
tipping problem, not a strength problem, and no filament choice or infill
percentage changes that. See *Will it stay put* below.

So infill in the base is neither structure **nor** useful ballast: going
from 15 % to 100 % adds 187 g and buys 25 % more tip resistance, which is
not worth having. Run 25 % and put the weight somewhere that works.

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

Two profiles below. The **display profile** is what to print now: the brief
is maximum quality and print time does not matter. The **batch profile** is
there for when you want a dozen of these and an overnight print each is too
much.

**On layer height, and a correction.** An earlier version of this document
claimed the layer height *had* to divide both 9.6 mm (the top of the plate)
and 0.6 mm (the inlay) exactly, and that 0.08 mm was therefore disqualified.
That was wrong, and the reason it is wrong tells you which presets are
actually safe: all of them.

The plate and the inlay are separate bodies, and a slicer cuts every body on
the *same* global Z planes. At any given layer, either the slice plane sits
below 9.0 mm and the plate is solid there, or it sits between 9.0 and 9.6 and
the inlay owns the logo region while the body's pocket excludes it. The two
are complementary at every layer no matter where the boundaries fall, so
**the inlay always fills its pocket exactly.** Divisibility changes the
inlay's layer *count*, not the fit — and seven layers of colour is as opaque
as five.

What actually varies with layer height is the finish on the 2 mm round-over
along the top edge of the plate, the one surface where the layers go nearly
horizontal and stair-stepping shows:

| Layer height | Round-over step | Step on the post's lean | Inlay layers |
|---|---|---|---|
| **0.08 mm** | **0.560 mm** | 0.015 mm | 7 |
| 0.12 mm | 0.682 mm | 0.023 mm | 5 |
| 0.16 mm | 0.784 mm | 0.031 mm | 4 |
| 0.20 mm | 0.872 mm | 0.039 mm | 3 |

The post's 10.9° lean is invisible at all of them. The round-over is where
the difference goes. On a Bambu H2C that makes **0.08mm High Quality** the
one to use here, with **0.12mm High Quality** giving most of the benefit
considerably faster.

| Setting | Display | Batch | Why |
|---|---|---|---|
| Nozzle | **0.4 mm** | 0.4 mm | Hard limit. See below — 0.6 mm cannot render this mark, and no amount of extra time fixes that. |
| Line width | **0.40 mm** | 0.42 mm | The narrowest gap in the mark is 0.460 mm. Staying under it is the whole game. |
| Layer height | **0.08 mm** | 0.20 mm | Finest H2C preset — best finish on the plate's top round-over. |
| First layer | 0.20 mm | 0.20 mm | Adhesion over a 215 mm footprint. |
| Walls | **6** | 4 | The post carries its load entirely in the walls. Also the post's surface *is* its walls. |
| Top solid | **1.2 mm** (15 layers) | 1.0 mm (5) | Specify it in millimetres, not layers. At 0.08 mm a preset's "5 top layers" is only 0.4 mm and will pillow over the infill. |
| Bottom solid | 0.8 mm (10 layers) | 0.8 mm (4) | |
| Infill | **25 %** gyroid | 25 % gyroid | Not structural and it does not help stability either — see below. 25 % is simply enough to hold the top surface flat. |
| Nozzle temp | 240–250 °C | 240–250 °C | High end of the PETG range, for layer adhesion at the blade root. |
| Bed | 70–80 °C | 70–80 °C | |
| Part cooling | 30–50 % | 30–50 % | Full blast weakens PETG layer bonding. |
| Outer wall speed | **25–30 mm/s** | 50 mm/s | The single biggest lever on visible surface quality, and where your unlimited time actually buys something. |
| Seam | **Scarf around entire wall** = on | same | *Not* a "Seam position" option — that dropdown only offers Nearest / Aligned / Back / Random. Scarf is the separate block of settings under it. This is the fix for the line up the post. |
| Wall generator | **Arachne** | Arachne | Classic lays fixed-width beads, so a 0.46 mm channel gets one 0.40 mm line and a 0.06 mm void. Arachne varies the width to fill it exactly. |
| X-Y contour / hole compensation | **0** | 0 | Leave alone. Any nonzero value eats directly into the 0.460 mm gaps. |
| Ironing | **Off** | Off | See the warning below — on the flush set it drags black into the red. |
| Supports | None | None | Nothing overhangs. The blade leans 10.9°, well inside what prints unsupported. |
| Brim | None | None | PETG needs no help here, and removing a brim from a 215 mm perimeter is worse than the problem. |
| Orientation | As exported, flat | As exported | Puts the layer lines where they do the most good. |

The solid model is 246 cm³. At 25 % infill expect roughly **150 g**; the
slicer will give you the real number.

**Do not turn ironing on for the flush set.** Ironing drags a hot nozzle
sideways across the finished top surface, and on the flush inlay black and
red *share* that surface. It will smear one into the other along every
boundary — which is every edge of the mark. If you want ironing, it is only
safe on the single-colour engraved version.

**Where the extra time actually goes.** Of the settings above, the ones that
change what you see are the layer height on the plate's 2 mm top round-over — not on the post's
lean, which is invisible at any of these — and the outer wall speed
everywhere.
Infill, walls beyond about four, and top layers beyond 1.2 mm cost hours and
change nothing visible.

### Why a 0.4 mm nozzle, and not 0.6

**It is the gaps, not the strokes.** This is worth being precise about,
because the obvious worry — that the lettering is too fine to print — turns
out not to be the problem at all.

Measured on the actual geometry, at the current 145 mm mark size:

| | |
|---|---|
| Ink in the mark | 3005 mm² across 36 separate shapes |
| Thinnest *whole shape* | 1.72 mm — nothing is delicate |
| Narrowest interior counter (the hole in an **A**, etc.) | 1.13 mm |
| Ink living in features narrower than 0.42 mm | **0.09 %** — tapered tips and corners only |
| **Narrowest gap between two separate shapes** | **0.460 mm** |

That last row is the one that decides the nozzle. Between the letters, and
between the lettering and the firearms, the plate has to show through a
channel 0.46 mm wide. A printer cannot lay a bead narrower than its nozzle,
so once the line width reaches 0.46 mm the two shapes either side stop being
separate and fuse into one blob.

| Line width | Shapes that fuse | Counters that close |
|---|---|---|
| 0.40 mm (0.4 nozzle, display profile) | **0** | **0** |
| 0.42 mm (0.4 nozzle, batch profile) | **0** | **0** |
| 0.45 mm | 0 | 0 |
| 0.50 mm | 4 | 0 |
| 0.62 mm (0.6 nozzle, stock) | **4** | 0 |
| 0.68 mm (0.6 nozzle, wide) | **5** | 0 |

A 0.4 mm nozzle clears the 0.46 mm limit with room to spare. A 0.6 mm nozzle
does not, and cannot be made to — this is what you were looking at when the
first test print came back with the gap between the **N** and the **T**
filled in. It was not a slicing setting and not a quality problem. The
nozzle was simply wider than the gap.

An earlier version of the model made this far worse. Every stroke was grown
0.15 mm per side so the finest details would survive, which worked, but
growing strokes *narrows the gaps between them by the same amount*. Scaling
the mark from 90 mm to 145 mm and cutting that growth to 0.05 mm fixed both
ends at once: the strokes got thicker in absolute terms and the gaps got
wider.

A finer nozzle for the logo alone is not an option: Bambu Studio refuses to
mix nozzle diameters within one print, and on this machine 0.2 mm exists on
the right extruder only, so choosing it would force single-extruder printing
and lose the flush inlay. 0.4 mm on both extruders is the configuration that
works. See the note under *On a Bambu Lab H2C* above.

### The line up one side of the post

That is the seam, not the model — every perimeter loop has to start and stop
somewhere, and with **Seam position** set to *Aligned* Bambu Studio stacks
them all at the same angle, so they form a line. There is only ever one seam
per loop, which is why the far side is smooth.

To fix it, do **not** look for a "Scarf joint" entry in the Seam position
dropdown; there isn't one — it offers only Nearest, Aligned, Back and
Random. Scarf is the separate block of checkboxes directly beneath it. Tick
**Scarf around entire wall**. The stock preset ships with *Smart scarf seam
application* already on, but "smart" only applies the scarf where the angle
threshold (155° by default) is met, which on a post this straight means
mostly nowhere. Forcing it around the entire wall ramps every loop's start
and end into a taper instead of a blob, and the line all but disappears.

Leaving Seam position on *Aligned* is then fine, and preferable — an aligned
scarf is consistent all the way up, where *Random* scatters the taper and
can read as noise on a large smooth flank.

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

On a single-hotend printer the flush version costs more filament in purge —
black and red change over inside every one of the inlay's layers rather than
twice for the whole print, so budget a few extra cubic centimetres of waste.
**None of that applies to the H2C**, which swaps hotends instead of purging;
see *On purging* above.

## Getting the mark in red

### Multi-material printer (AMS, MMU, Palette, IDEX)

Load `MMFT_Stand_black_body.stl` and `MMFT_Stand_red_logo_full.stl` from the
folder you picked into one project, assign black and red, and slice. They
share a coordinate space, so they land in the right place with no alignment
step, and in the flush set the inlay fills its pocket exactly — no gap and
no overlap.

For three colours use `MMFT_Stand_black_body.stl`,
`MMFT_Stand_red_logo_text.stl` and `MMFT_Stand_light_logo_art.stl`.

**Which way round the two accent colours go is your choice, and the file
names are only the original suggestion.** The two bodies are just "the
lettering" and "the firearms"; whichever filament slot you point each at is
what it becomes.

The scheme in use is **white lettering with red firearms** on black, and it
is the better of the two. Red and black sit close together in luminance
even though they read as clearly different colours up close, so red
lettering on a black plate loses legibility at a distance. White against
black is the highest contrast available here, which puts the words where
they are readable across a room and leaves the red to work as an accent on
the rifle, scope and pistol — where drawing the eye is the whole point.

The file naming (`red_logo_text`, `light_logo_art`) predates that decision
and is kept so existing links and instructions stay valid.

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

Three colours cannot be done this way. The lettering and the
firearms sit in the same three layers, so that set needs a multi-material
printer.

### One colour

Two options, neither needing a filament change:

* `raised/MMFT_Stand_one_piece.stl` — the mark standing proud of the plate.
* `flush/MMFT_Stand_engraved_one_piece.stl` — the mark cut into the plate
  instead. Nothing proud of the surface at all, so it is the most durable
  thing here. The engraved channels are not the concern — the thinnest is
  1.72 mm — but the *ribs of plate left standing between them* are, and the
  narrowest of those is 0.46 mm, barely one bead wide. Expect a few of them
  to look soft. The lettering itself comes through cleanly, and this is the
  one version it is safe to iron.

## Will it stay put

Short answer: **it is far stronger than it needs to be and less stable than
I would want on a shop counter.** If you change one thing before putting
these out front, change the weight, not the infill.

All of the following is calculated from the actual model geometry — the
stand's real centre of mass at (118.9, 49.0, 10.7) mm — with a pistol
treated as a point mass on the post. Note that the post goes *up inside*
the magazine well, so the gun's mass sits low and does not perch on the tip.

It has not been measured on a finished print. Treat it as the right order of
magnitude and the right *ranking* of the options, not as three-significant-
figure truth. Every number here, and every feature width quoted above, is
reproduced by **`python src/analysis.py`**.

### The numbers

With a 625 g Glock 17 on it, at 25 % infill, pushing sideways at the slide:

| | Force to tip it |
|---|---|
| **Sideways, off the long edge** | **2.9 N — 0.65 lbf** |
| Backward, off the end behind the post | 3.6 N — 0.80 lbf |
| Forward, over the logo | 12 N — 2.7 lbf |

A heavier pistol helps a little, because the extra weight sits mostly low:
a SIG P226 goes to 4.2 N, a loaded Staccato 2011 to 4.7 N.

0.65 lbf is not much. It is a firm nudge with the back of your hand. The
geometry is simply against you — the plate is 98 mm wide with the post on
its centreline, so there is only 49 mm of lever holding up a pistol whose
mass sits around 100 mm in the air.

### Why infill is the wrong lever

This was the obvious thing to reach for and it does almost nothing:

| Infill | Stand mass | Sideways tip |
|---|---|---|
| 15 % | 126 g | 2.79 N |
| 25 % | 148 g | 2.87 N |
| 50 % | 203 g | 3.07 N |
| 100 % | 312 g | 3.48 N |

Going from 15 % to solid adds 187 g of filament and hours of print time to
move the number by a quarter. The reason is that infill adds mass *spread
through the whole part*, including the post, so it raises the centre of
mass almost as fast as it raises the weight.

### What does work

Mass low down. Ballast adds weight *and* drags the centre of mass toward
the plate, so it works on both terms at once:

| Ballast at plate level | Total weight | Sideways | Backward |
|---|---|---|---|
| none | 1.7 lb | 2.9 N | 3.6 N |
| +500 g | 2.8 lb | 4.7 N | 7.6 N |
| +1000 g | 3.9 lb | 6.6 N | 11.7 N |

Practical ways to get it there, roughly in order of how much I like them:

1. **Fasten the stand down.** If the display is a fixed shelf, two
   countersunk screws through the plate ends the conversation permanently
   and costs nothing. For a storefront this is usually the right answer.
2. **A steel plate bonded underneath.** 215 × 98 × 3 mm of steel is about
   500 g. Flat, invisible from the front, no model change needed.
3. **Lead tape or stick-on wheel weights** in the corners, if you would
   rather not commit to a full plate.
4. **A cast-in cavity** filled with shot or sand and capped. This is the
   tidiest result and the most work, and it needs a model change: a pocket
   opening downward cannot simply be bridged over a 70 mm span, so it would
   have to be a ribbed or cellular pocket with individually bridgeable
   cells, or a separate glued-on cap.

I have not made any of these changes to the model. Say the word and I will
add a ballast provision properly.

### The counterintuitive bit: do not use rubber feet

When something knocks the pistol, the stand can either **slide** — which is
harmless, the gun stays put and the stand scoots an inch — or **tip**, which
puts a firearm on the floor. Which one happens is decided by the friction
under it, and the grippier the feet, the more likely you get the bad one:

| Underside | Slides at | Verdict (no ballast, tips at 2.9 N) |
|---|---|---|
| Bare PETG on laminate | 2.3 N | **slides first** — gun stays on |
| Felt pads | 2.7 N | slides first, but only just |
| Cork | 4.2 N | **tips first** |
| Rubber / silicone feet | 6.1 N | **tips first** |

So the instinct to stick a rubber mat under a display stand is exactly
wrong here. Leave it on bare plastic or felt, and it fails safe. Add 500 g
of ballast and felt gets a comfortable margin again (slides at 4.4 N, tips
at 4.7 N) — but rubber is still the wrong choice even then.

### Strength, for completeness

None of the above is about the part breaking. Printed hollow with six
walls, the post does not fail until roughly **578 N (130 lbf)** pushes
sideways at the slide — about 200 times the force that tips the whole stand
over. You will never break one of these by using it.

## Before you print a batch

Print one and check the pistol actually sits on it. The blade section came
off the stand this design replaces and has not been tested here against a
real firearm. If it is tight, a few passes with sandpaper along the blade
sorts it out; if it is loose, raise `BLADE_HX` / `BLADE_HY` in
`src/build.py` by a few tenths and rebuild.

**Do not put rubber feet or a grippy mat under it.** That sounds backwards,
so see *Will it stay put* below — with this much height and this narrow a
base, high-grip feet convert a harmless slide into a topple. Felt or bare
plastic is the right answer unless you have added ballast.
