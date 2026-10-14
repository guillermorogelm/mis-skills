---
name: tactile-toy-prompt
description: Turns a one-line idea for something squishy, stretchy, wobbly or pourable into a build prompt for a single-file three.js toy you can poke, pull, squash and throw, in the "Squishy Toast" / "Gummy Bears" format - the object, physics written as gestures with a response and a recovery, variants, and an editorial product-page UI. Use when asked to write a prompt for a 3D toy, a squishy or jelly or foam or slime thing, an interactive physics demo, "a prompt like Squishy Toast", or to tighten an existing prompt of that kind.
---

# Tactile Toy Prompt

Write the prompt, not the toy.

The output is a build prompt that another model (or you, later) turns into
one HTML file. A good one reads like a product spec for an object that does
not exist yet: every line names something you could point at on screen and
say "that is there" or "that is missing".

Read `examples.md` before writing your first prompt in a session. The two
originals are the bar. `reference.md` holds the material, technique and
gesture vocabulary.

## What makes these prompts work

1. **One sentence of pitch.** Name in quotes, the file constraint, then "an
   interactive 3D X you can verb, verb, verb and verb". The verbs are the
   product.
2. **The object is described like a photograph.** Silhouette first, then
   surface, then material, then staging. Real-world nouns ("muffin top",
   "crust rim", "molded eyes"), not "realistic".
3. **Physics is the whole point, and the prompt says so.** The section
   header carries a contrast: "it must feel like foam, not geometry". That
   one line tells the builder what failure looks like.
4. **The technique is named where the naive approach fails.** "Densely
   tessellated mesh deformed per vertex", "implicit surface (metaballs /
   marching cubes), not separate spheres", "volume-preserving shape
   matching". Name it only where a builder would otherwise reach for the
   wrong thing.
5. **Every gesture has three beats.** What the hand does, what the
   material does right away, how it comes back. "Press and hold: a smooth
   gaussian dent, crumb bulges outward around the rim ... Release: rises
   back slowly and exponentially, no instant snap." The recovery is where
   the feel lives, so it always gets its own adjective with a mechanism.
6. **Things coexist.** Several dents at once, bears that collide and never
   pass through each other, idle motion when nobody touches it.
7. **Variants change the physics or the light, not just the color.** Jam
   gets a clearcoat; the spread deforms with the bread; clear pineapple has
   no tint to absorb.
8. **The UI is one fixed template.** Editorial product page, white
   background, italic serif title split over two lines with a period, a
   card on the right, one slider bound to a named physical parameter, live
   readouts named after the sensation, one playful action button, a cursor
   that reacts to pressure, then the rendering line and "Smooth 60fps".

## Step 1. Pin the subject

From the user's idea, decide in one line each:

- **The object.** One thing, or a handful of the same thing.
- **The material it must feel like**, and the thing it must not feel like
  ("jelly, not plastic"; "dough, not rubber"; "foam, not geometry").
- **The signature gesture.** The one interaction someone screenshots.
  Toast: the slow memory-foam rise. Gummy bears: pulling the head and the
  neck stretching.

If the idea is a bare noun, decide all three yourself and state the
choices after the prompt. Ask a question only if two readings would give
different physics (is the "slime" a blob in a bowl or a ball on a table?).
At most two questions.

## Step 2. Choose the simulation technique

Look the material up in the technique table in `reference.md`. Pick one
primary technique. Add a second only for a separate layer (a spread on the
toast, liquid inside a shell). Write it into the physics section in plain
words, with the one property that makes it look right (normals recomputed,
volume preserved, thinner as it stretches).

## Step 3. Write the gestures

Pick four to seven from the gesture menu in `reference.md`. Always include:

- the press or poke (the first thing anyone does),
- a grab-and-pull,
- one whole-body gesture (squash, throw, drop, pour, shake),
- what happens when nobody touches it (recovery, idle hops, settling).

Each gesture gets the three beats. Each recovery gets a curve from the
recovery vocabulary: slow exponential, damped wobble, decaying bounce,
elastic ripple, viscous creep, snap-and-overshoot. Never "returns to
normal".

## Step 4. Write the rest

- **The object section**: silhouette, surface detail, material, colors or
  variants, staging (white surface, angle, a contact shadow that says
  something: baked, soft, tinted by the object's own color).
- **Variants section** (optional, named after the domain: Flavors,
  Finishes, Colors, Fillings): three to five, each with what changes in
  the material or the physics.
- **UI section**: use the template in `reference.md`. Change the title, the
  subtitle, the slider's physical parameter, the readout names and the
  button verb. Keep everything else.

## Step 5. Check it against the bar

Run the checklist at the end of `reference.md`. Then cut. The originals are
300 to 450 words. If yours is longer, something is a paragraph where a
fragment belongs.

## Style rules

- Fragments, not sentences, inside bullets. Commas join beats.
- Plain hyphen " - " as the dash. No em dashes.
- No adjective without a mechanism. "Realistic", "beautiful", "smooth"
  (except "Smooth 60fps"), "nice", "satisfying" are banned unless the next
  words say how.
- Numbers only where they constrain: 60fps, "two ears", "a handful".
- No code, no library APIs beyond three.js material terms the builder will
  recognise (transmission, clearcoat, sheen, ACES).
- One file. three.js from a CDN is the only dependency, unless the user
  names another.

## Output

1. The prompt in a single fenced code block, ready to paste.
2. Under it, at most three lines: the material contrast, the technique and
   the signature gesture you chose, so the user can redirect.
3. Offer to build it. Do not start building unless asked.

If the user hands you an existing prompt to improve, return the rewritten
prompt and a short list of what changed and why, citing the numbered
points above.
