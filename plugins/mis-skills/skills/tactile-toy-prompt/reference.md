# Reference

## Technique table

Pick the row whose "feels like" matches. The "say this" column is the
phrase to put in the prompt.

| Feels like | Technique | Say this in the prompt |
|---|---|---|
| Foam, sponge, bread, cushion, marshmallow | Per-vertex deformation of a dense mesh, per-dent state | "Densely tessellated mesh deformed per vertex every frame, normals recomputed" |
| Jelly, gummy, pudding, water balloon | Soft body: mass points + shape matching | "Soft body: mass points for ..., held together by volume-preserving shape matching" |
| Blobby organic shapes that merge (candy, creatures, wax) | Implicit surface | "Build the body as an implicit surface (metaballs / marching cubes), not separate spheres" |
| Dough, mochi, taffy, cheese pull | Mass-spring or PBD with plastic memory | "Stretches into a thinning strand, keeps part of the new shape (plastic), slowly relaxes" |
| Slime, honey, putty | Viscous particles or heightfield with viscosity | "Viscous: creeps back slowly, no bounce, strands neck down and break" |
| Cloth, napkin, tortilla, ribbon | Verlet cloth with constraints | "Verlet cloth grid with distance constraints, self-shadowing folds" |
| Liquid in a container | Heightfield waves or sloshing spring | "Surface is a damped heightfield: waves travel, reflect off walls and settle" |
| Fur, grass, bristles | Strand springs per tuft | "Each tuft is a spring that bends away from the cursor and sways back" |
| Many small pieces (beans, sprinkles, beads) | Rigid particles with collision, instanced | "Instanced pieces with collision, they pile, slide and settle" |
| Balloon, inflatable | Pressure soft body | "Soft body with internal pressure: dents bulge elsewhere, squeezes keep volume" |

Properties worth naming when they apply:

- **Volume preservation**: squash one way, bulge the other. "Barrel-bulges
  at mid-height", "pancakes, bulges sideways".
- **Thinning under stretch**: "thins as it stretches", "strands getting
  thinner as they stretch".
- **Anchoring**: what does not move. "The bottom stays planted on the
  table."
- **Collision**: "never pass through one another", "pushes other bears out
  of the way".
- **Normals**: if a mesh deforms, say they are recomputed, or the lighting
  stays frozen.

## Material vocabulary

Describe material as three layers: body, surface, light.

| Material | Body | Surface | Light |
|---|---|---|---|
| Bread crumb | Warm cream, procedural pores of varied size | Bump map, toasted edge fading inward | Matte, pore highlights |
| Crust / baked | Golden-brown | Subtle grain | Light sheen |
| Gummy / jelly | Translucent, transmission and refraction | Molded detail | Colored absorption deeper in thick parts, glossy clearcoat, sharp highlights |
| Jam, syrup, glaze | Deep saturated color | Glossy, slightly uneven | Clearcoat |
| Mashed / paste (avocado, hummus) | Opaque, variegated | Lumpy, mashed texture | Low sheen |
| Butter | Pale yellow, slightly translucent at edges | Smooth, melting | Soft sheen |
| Marshmallow, mochi | Powdery white or pastel | Fine dusting, matte | Subsurface glow |
| Slime | Translucent or pearlescent | Wet, stringy | Iridescence or clearcoat |
| Silicone, rubber | Opaque, saturated | Smooth, faint texture | Satin |
| Fabric | Woven | Thread grain | Sheen at grazing angles |

three.js `MeshPhysicalMaterial` terms a builder recognises: transmission,
thickness, attenuation color, ior, clearcoat, sheen, iridescence,
roughness, bump map. Use the plain-language version in the prompt and let
the builder map it.

## Staging

- White table, 3/4 angle, object lying the way it would in a photo.
- Contact shadow that carries information: "soft baked", "tinted by the
  bear's own color".
- Lighting: soft key, rim or back light, environment reflections, ACES tone
  mapping.

## Gesture menu

Write each as: **gesture**: immediate response, secondary response.
**Release / recovery**: curve.

| Gesture | Immediate | Secondary | Typical recovery |
|---|---|---|---|
| Press and hold | Local dent | Material bulges around the rim | Slow exponential rise, faint ripple |
| Poke (tap) | Small dimple | Ring wave | Quick elastic pop |
| Grab and pull | Stretches toward cursor, thins | The rest leans after it | Damped wobble back |
| Pull a part up | That part lifts, joint stretches | Body follows | Squash and hop on release |
| Press the top down | Pancakes | Bulges sideways | Launches back up / breathes back |
| Palm squash | Whole thing flattens | Barrel-bulges mid-height | Breathes back up |
| Twist | Wrings along the axis | Wrinkles or folds | Unwinds with overshoot |
| Throw | Flies with stretch along velocity | Squashes on landing | Bounces, settles, pushes neighbours |
| Drop | Falls | Squash and stretch on impact | Small decaying bounce |
| Shake / drag fast | Lags behind cursor | Jiggles | Settles with damped wobble |
| Pour / spawn more | Several fall from above | Pile up, collide | Wobbling, jiggling pile settles |
| Tear / pinch off | Neck forms and thins | Breaks into two | Both halves round off |
| Idle | Nothing touching | Small random hops, breathing, settling | - |

Coexistence lines to add when they apply: "Several dents can coexist, each
recovering on its own", "Bears collide with each other and never pass
through one another".

## Recovery vocabulary

| Curve | Feels like | Phrase |
|---|---|---|
| Slow exponential | Memory foam | "rises back slowly and exponentially, no instant snap" |
| Damped wobble | Jelly, rubber | "springs back with a damped wobble" |
| Decaying bounce | Ball, gummy | "small decaying bounce" |
| Elastic ripple | Membrane, crumb | "a faint elastic ripple runs across" |
| Viscous creep | Honey, slime | "creeps back, no bounce" |
| Plastic memory | Dough, clay | "keeps part of the new shape, slowly relaxes" |
| Snap and overshoot | Tight rubber | "snaps back, overshoots once, settles" |

## UI template

Keep the structure. Swap the bracketed parts.

```
UI
- Editorial product-page style on a white background. Large italic serif title "[Word] / [Word].", a short subtitle, a minimal card on the right with [variant] swatches, a [physical parameter] slider ([what it controls]), [live "Readout" meter / live "A" and "B" readouts] and a "[Playful action]" button
- A subtle circular cursor that [shrinks while pressing / grows while grabbing]
- ACES tone mapping, [soft key and rim / key and back] lights, environment reflections. Smooth 60fps
```

- The slider controls a real simulation parameter and the prompt says
  which: "softness slider (controls dent size and recovery time)".
- Readouts are named after the sensation, not the math: "Rise", "Stretch",
  "Bounces", "Jiggle", "Squish".
- The button is a verb the user wants to press: "Fresh slice", "Pour more
  bears", "Drop another", "Refill".
- Cursor: shrinks for press-type toys, grows for grab-type toys.

## Checklist

- [ ] First line: name in quotes, single self-contained HTML file, three.js
      from a CDN as the only dependency, then four verbs.
- [ ] Object section covers silhouette, surface, material, staging.
- [ ] Physics header has "this is the whole point - it must feel like X,
      not Y".
- [ ] A technique is named, and the property that makes it look right.
- [ ] Four to seven gestures, each with immediate, secondary and recovery.
- [ ] Every recovery uses a named curve.
- [ ] Coexistence or collision is stated.
- [ ] Idle or resting behavior is stated.
- [ ] Variants change material or physics, not only hue.
- [ ] UI follows the template; slider names its parameter; readouts named
      after sensations.
- [ ] Ends with "Smooth 60fps".
- [ ] No banned adjectives, no em dashes, 300 to 450 words.
