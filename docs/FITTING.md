# Fitting the post to a platform

The post on this stand is shaped like a magazine, because that is what it
stands in for — it goes up into the magazine well and holds the pistol the
way a seated magazine would. A measured Glock 17 magazine is 33.1 × 22.8 mm
and the post presents 33.06 × 22.84 mm, so it fits a Glock and very little
else. A single-stack 1911 well is far narrower; a 2011 or a wide double
stack is wider again.

Everything about the stand except the post is independent of the platform,
so a variant is just a different post on the same base. What is missing is
the number to draw it to, and that is what the gauge is for.

## Why a gauge rather than a caliper

Measuring a magazine gets you the magazine, not the well. It misses the
flare at the mouth, how far the well actually runs before something stops
the magazine, and how much clearance still feels secure rather than tight.
Trying a shaped post in the real pistol answers all three at once, and the
gauge then serves every platform you add later.

## Printing it

`stl/gauge/MMFT_FitGauge_all.stl` is all twelve on one plate, 146 × 220 mm.
The individual stubs are beside it if you would rather print a few at a
time.

These only need their outside surface, so print them **hollow — two walls,
0 % infill**. As solids they come to 286 cm³; hollow they are a fraction of
that. Any nozzle and layer height will do; nothing here is fine detail.

## Using it

Work with the pistol cleared and the magazine out, the same as you would
for any dry function check.

Twelve stubs cover 30, 32 and 34 mm front-to-back against 16, 19, 22 and
25 mm side-to-side. Each is labelled with its own size on the flange.

Start small and work up. You are looking for **the largest stub that seats
without being forced** — it should go in under its own weight or close to
it, and hold the pistol without slop. If you have to push, it is too big;
if the pistol rocks on it, go up a size.

The ticks up one narrow face are every 5 mm, with a longer tick every
10 mm. If a stub bottoms out before it is all the way in, read off the tick
sitting at the mouth of the well — that is how deep the well runs, and it
sets how tall the post can be.

## What to send back

Per platform:

* the label of the best-fitting stub, e.g. `32x19`
* whether it bottomed out, and at which tick if it did
* whether the best fit felt snug, loose, or between two sizes

Between two sizes is useful information, not a problem — the generator
takes any dimensions, not just the ones on the gauge, so `32.5 x 20.5` is
as easy to draw as `32 x 19`.

## What happens to those numbers

Report the gauge figure as it is. The stubs stand straight up, so their
section is the section the well sees. The post on the finished stand leans
10.9° and is *sheared* rather than tilted, so it has to be drawn wider by
1/cos(lean) to present the same section to the well. The generator applies
that itself — `BLADE_NOMINAL_W` and `BLADE_NOMINAL_D` in `src/build.py` are
the numbers you read off the gauge.

Expect the finished post to come out a few tenths under the stub that fit
best. A post that matches a magazine exactly is a magazine-tight fit, which
is more than a display needs; on a counter where pistols come off and on all
day, a little clearance means less wear on the well and easier one-handed
seating.
