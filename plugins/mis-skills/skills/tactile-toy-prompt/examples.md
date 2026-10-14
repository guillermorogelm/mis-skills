# Examples

The first two are the originals this skill is built from. They are the
bar. The third shows the skill applied to a new idea.

## 1. Squishy Toast (original)

Material contrast: foam, not geometry. Technique: per-vertex deformation.
Signature gesture: the slow memory-foam rise after a press.

```
Build "Squishy Toast" - a single self-contained HTML file (three.js from a CDN is the only dependency): an interactive 3D slice of slow-rise memory foam bread you can press, poke, stretch and squash.

The toast
- A real bread silhouette: square body, rounded "muffin top" crown, soft beveled edges
- Crumb face: warm cream color, procedural pores of varied size with highlights and a bump map, a toasted golden edge fading in toward the center
- Crust: golden-brown with subtle grain and a light sheen
- Lies flat on a white surface at a 3/4 angle with a soft baked contact shadow

Physics (this is the whole point - it must feel like foam, not geometry)
- Densely tessellated mesh deformed per vertex every frame, normals recomputed
- Press and hold: a smooth gaussian dent, crumb bulges outward around the rim, the bottom stays planted on the table
- Release: the dent rises back slowly and exponentially, like memory foam, with no instant snap. A faint elastic ripple runs across the crumb after release
- Several dents can coexist, each recovering on its own
- Grab the crust and pull: the bread stretches elastically, thins as it stretches, then springs back with a damped wobble
- Palm squash: the whole slice flattens and barrel-bulges at mid-height, then breathes back up
- Drop: lift and release, squash-and-stretch on impact, small decaying bounce

Flavors
- Butter, strawberry jam (glossy clearcoat, deeper color), avocado (mashed texture). The spread sits on the crumb, leaves a crust rim and deforms with the bread

UI
- Editorial product-page style on a white background. Large italic serif title "Squishy / Toast.", a short subtitle, a minimal card on the right with flavor swatches, a softness slider (controls dent size and recovery time), a live "Rise" meter and a "Fresh slice" reset button
- A subtle circular cursor that shrinks while pressing
- ACES tone mapping, soft key and rim lights, environment reflections. Smooth 60fps
```

What to notice:
- "The bottom stays planted on the table" is an anchoring rule. Without it
  the whole slice would sink.
- The recovery gets a speed ("slowly"), a curve ("exponentially") and a
  forbidden failure ("no instant snap").
- Jam is not just red: it gets clearcoat. The spread "leaves a crust rim"
  and "deforms with the bread", two things a builder would skip.

## 2. Gummy Bears (original)

Material contrast: jelly, not plastic. Technique: metaball body + soft body
shape matching. Signature gesture: pulling the head up and the neck
stretching.

```
Build "Gummy Bears" - a single self-contained HTML file (three.js from a CDN is the only dependency): a handful of translucent gummy bears on a white table that you can grab, stretch, squash, throw and pour.

The bears
- Classic gummy bear silhouette: round head with two ears, short snout, plump body, stubby arms and legs, tiny molded eyes and nose
- Every part melts smoothly into the next - build the body as an implicit surface (metaballs / marching cubes), not separate spheres
- Material: real gummy candy. Translucent with transmission and refraction, colored light absorption that gets deeper in thick parts, glossy clearcoat with sharp highlights
- Colors: cherry red, orange, lemon yellow, apple green, clear pineapple
- Soft colored shadow under each bear, tinted by the bear's own color

Physics (this is the whole point - it must feel like jelly, not plastic)
- Each bear is a soft body: mass points for head, ears, snout, body, belly, hands and feet, held together by volume-preserving shape matching
- Limbs and neck are rendered as stretchy strands between points, getting thinner as they stretch
- Grab any part and pull: it stretches like rubber, the rest of the bear leans after it, on release it snaps back with a damped wobble
- Pull the head up: the neck stretches, the body follows, on release the bear squashes and hops
- Press down on the head: the bear pancakes, bulges sideways, then launches itself back up
- Throw a bear: it flies, squashes on landing, bounces and pushes other bears out of the way
- Bears collide with each other and never pass through one another
- Idle bears do small random hops with squash and stretch
- "Pour more bears" drops a handful from above into a wobbling, jiggling pile

UI
- Editorial product-page style on a white background. Large italic serif title "Gummy / Bears.", a short subtitle, a minimal card on the right with flavor swatches, a wobble slider, live "Stretch" and "Bounces" readouts and a "Pour more bears" button
- A subtle circular cursor that grows while grabbing
- ACES tone mapping, environment reflections, soft key and back light. Smooth 60fps
```

What to notice:
- "Not separate spheres" names the lazy build and rules it out.
- The mass points are listed by body part, so the builder knows the
  resolution of the simulation.
- "Absorption that gets deeper in thick parts" is one phrase that forces
  real transmission with thickness, not a flat transparent color.
- The button in the UI is also a gesture in the physics section. The UI
  and the physics describe the same toy.

## 3. Mochi (new, written with this skill)

User asked: "a prompt like the toast one but for mochi".

```
Build "Pull Mochi" - a single self-contained HTML file (three.js from a CDN is the only dependency): a few soft rice-cake mochi on a white plate that you can poke, pinch, pull into long strands and squash flat.

The mochi
- Plump domed rounds, slightly flattened under their own weight, wider at the base where they sag onto the plate
- Surface: fine powdery dusting of starch, matte, denser in the creases, rubbed away where you touch
- Material: soft subsurface glow, light passes a few millimetres in and warms the edges
- Colors: plain white, sakura pink, matcha green, toasted kinako
- Sits on a white ceramic plate at a 3/4 angle, soft contact shadow that spreads as the mochi sags

Physics (this is the whole point - it must feel like dough, not rubber)
- Each mochi is a dense mass-spring mesh with plastic memory: it keeps part of every new shape and relaxes slowly toward round
- Poke: a deep, soft dimple, the dome sags around it. Release: the dimple fills back in over a couple of seconds, no bounce
- Pinch and pull: a strand necks down and gets thinner the further it goes, the body drags after it. Let go past a limit and the strand snaps, both ends round off and droop
- Pull two mochi together: they stick and merge into one, then slowly round off
- Palm squash: flattens into a wide disc and stays a little flat, then creeps back up
- Mochi sag and settle when left alone, never bounce, never pass through each other

Fillings
- Plain, red bean (dark paste visible through thin stretched parts), strawberry (a red shape inside that shows as a pink blush), ice cream (cold, stiffer, slower to stretch)

UI
- Editorial product-page style on a white background. Large italic serif title "Pull / Mochi.", a short subtitle, a minimal card on the right with filling swatches, a chewiness slider (controls stretch limit and how much shape it keeps), a live "Stretch" readout and a "Fresh batch" button
- A subtle circular cursor that grows while pinching
- ACES tone mapping, soft key and rim lights, environment reflections. Smooth 60fps
```

Choices made: dough, not rubber (no bounce anywhere); mass-spring with
plastic memory; signature gesture is the pull that necks and snaps.
