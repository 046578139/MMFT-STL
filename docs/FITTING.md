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

## Known sections

What could actually be sourced. All of these are caliper readings posted by
people who own the magazines, not manufacturer specifications — treat them
as good starting points, not gospel.

| Platform | Long axis | Thin axis | Source |
|---|---|---|---|
| Glock 9 mm — 17/19/26/34/45 | 33.1 mm | 22.8 mm | [Glock Talk](https://www.glocktalk.com/threads/glock-17-9mm-and-40-mag-dimensions.1669367/) |
| Sig P320 9 mm / .40 / .357 | ~31.4 mm | ~21.6 mm | [SIGforum](https://sigforum.com/eve/forums/a/tpc/f/430601935/m/7630051774) |
| Sig P227 .45 | ~34.9 mm | ~23.8 mm | [SIGforum](https://sigforum.com/eve/forums/a/tpc/f/430601935/m/7630051774) |
| 1911 single stack .45 | 34.8 mm | 13.7 mm | [Pistol Smith](https://www.pistolsmith.com/threads/1911-magazine-dimensions.21328/) |
| 2011 — Staccato, Atlas, Infinity, Prodigy | — | — | none found |
| Sig P226, S&W M&P, FN 509 | — | — | none found |

Two things fall out of that table. The platforms really are distinct — a
Glock post is 1.7 mm too long for a P320 well and 9 mm too thick for a
1911 — and the spread is wider than it looks, because single stacks are
barely half the thickness of a double stack.

Cartridge length sets a floor nobody can go under: 9 mm Luger is 29.69 mm
overall, .40 S&W 28.88, .45 ACP 32.39, .38 Super 32.0. A magazine body has
to be roughly 2.5 mm longer than the round it holds, so **no centrefire
pistol magazine is much under 31 mm in its long axis**, and a .45 cannot
be under about 35. If something is binding below that, it is not the long
axis doing it.

## Two sets of stubs

**`stl/gauge/platforms/`** — ten stubs aimed at specific pistols, each
labelled with the platform on the first line and its section on the second.
Start here.

| Stub | Section | What it is |
|---|---|---|
| `GLOCK` | 33.1 × 22.8 | Glock 9 mm; one post covers 17/19/26/34/45 |
| `P320` | 31.4 × 21.6 | Sig P320, 9 mm / .40 / .357 |
| `1911` | 34.8 × 13.7 | 1911 single stack |
| `1911-S` | 34.2 × 12.9 | 1911, one size under |
| `1911-L` | 35.4 × 14.6 | 1911, one size over |
| `2011-A` | 34.0 × 21.0 | 2011 family, bracketed |
| `2011-B` | 35.0 × 22.5 | 2011 family, bracketed |
| `2011-C` | 35.8 × 24.0 | 2011 family, bracketed |
| `DS-A` | 32.5 × 23.5 | P226 / M&P / FN, bracketed |
| `DS-B` | 34.0 × 25.0 | P226 / M&P / FN, bracketed |

The three sourced sections are drawn at the figure as measured. The
bracketed ones are guesses spread across the plausible range, because no
measurement could be found — if none of a bracket fits, say which way it
missed and the next set can be aimed properly.

**`stl/gauge/`** — the original twelve, a plain grid of 30/32/34 against
16/19/22/25. Its range was wrong for single stacks: nothing in it is
thinner than 16 mm, so no 1911 was ever going to take one, and at 34 mm
its longest is shorter than a .45 magazine. It is still useful for
anything the platform set brackets badly.

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

Per pistol:

* which stub fitted best — the name is enough, `2011-B` or `GLOCK`
* whether it bottomed out, and at which tick if it did
* whether it felt snug, loose, or between two sizes
* if nothing fitted, **which way it missed** — too long, too short, too
  thick, too thin. That is the most useful thing you can tell me about a
  bracketed family.

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
