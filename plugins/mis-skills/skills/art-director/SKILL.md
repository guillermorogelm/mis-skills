---
name: art-director
description: Art-directs web pages the way an editorial designer would, with real typographic scale contrast, a committed grid, one accent colour and one signature motion. Use when designing or redesigning a page, building a landing page, hero or marketing section, choosing type, grid, colour or animation, or when someone says the layout looks generic, looks like a template, looks like Bootstrap, feels flat, or needs art direction. Not for backend or component logic.
---

# Art Director

Art-direct the page. Decide type, grid, colour and motion before you write markup.

Reference points: Readymag editorial sites, Swiss and Bauhaus posters, printed magazines. Not dashboards. Not component library demos.

Numbers and full tables live in [reference.md](reference.md). Worked fixes live in [examples.md](examples.md). Open them when you need a value or a pattern.

## Start with the direction card

Write these nine lines and show them before you build anything. It takes two minutes and it is the whole difference.

```
Ratio      1.333
Body       18px / 1.6 / measure 66ch
Display    clamp(3.25rem, 10vw, 9rem) / 0.94 / weight 400 / -0.035em
Grid       12 cols, gutter 24px, page margin clamp(20px, 5vw, 120px)
Unit       8px
Paper      #F4F1EA   Ink #14110D   Muted #6B655C   Rule rgba(20,17,13,.14)
Accent     #C8452B, under 5% of pixels, one use per screenful
Signature  Display line masks up per line, 900ms, once
Motion off Everything at final position, opacity 1, nothing moves
```

Swap values to fit the brief. Do not skip a line. A missing line is a decision you will make badly later.

## Order of work

1. Name in one sentence what the page must make someone do or feel.
2. Write the direction card.
3. Build the first screen only. Show it.
4. Build the rest to the same card.
5. Add the signature move last.
6. Run Stop.

## Type

**Pick one ratio and derive everything.** 1.2 for dense information pages. 1.333 for most pages. 1.5 for poster-like pages with little text. Tables in [reference.md](reference.md).

**Break the ratio at the top.** The ladder gives you caption, body, subhead, headline. Display type sits above the ladder and ignores it. Display must be at least 5x body size. Body 18px means display 90px or more. If your largest type is under 4x your body type, the page reads generic whatever else you do.

**Big type gets lighter and tighter.** Optical weight grows with size, so weight comes down and tracking goes negative as size goes up.

| Size | Weight | Tracking | Leading |
| --- | --- | --- | --- |
| 11-13px label | 500-600 | +0.08em, uppercase | 1.3 |
| 16-20px body | 400 | 0 | 1.5-1.65 |
| 24-32px | 400 | -0.01em | 1.25 |
| 40-72px | 400-500 | -0.02em | 1.05-1.12 |
| 80-140px | 300-400 | -0.035em | 0.94-1.0 |
| 140px and up | 300 | -0.045em | 0.88-0.92 |

Never set 700 or heavier above 72px unless the design is a solid poster block. A 700 weight at 120px is a shout, not a headline.

**Set the measure.** Body 60-75 characters. Lead paragraph at 22-24px: 40-50 characters. Display: 8-18 characters a line, and break the lines yourself rather than letting the box decide.

**Two families maximum, and make them fight.** A grotesque against a high-contrast serif. Not two grotesques. One family in three weights beats two families used timidly. Stacks that need no download are in [reference.md](reference.md).

**Small type is a design element.** Section numbers, 11px uppercase labels at +0.08em in muted ink, a real caption under an image. This is the fastest visible difference between editorial and marketing.

## Grid

**Commit to columns.** 12 columns, 24px gutter, page margin `clamp(20px, 5vw, 120px)`. Declare it once and place everything on it. Six columns under 900px, four under 600px.

**Never split 6+6.** Halves read as a template. Use 7+5, 8+4, 5+7, or 4+7 with a one-column offset. Uneven splits are what makes a layout look decided.

**Hairlines, not cards.** Separate content with 1px rules at 12-15% ink. Drop the rounded corners, the soft shadows and the card backgrounds. Cards say dashboard. Rules say printed page. Both patterns in full in [examples.md](examples.md).

**One deliberate break.** Exactly one element ignores the grid: bleeds off the right edge, crosses a gutter, or hangs into the margin. One. Two breaks and there is no grid left to break.

**Base unit 8px.** Every gap, pad and offset is a multiple. Section spacing is large: 96, 128, 160, 192.

**Vary the vertical rhythm.** Tight blocks and wide silence. If every section carries the same padding the page has no pacing. Compress a related pair to 32px, then leave 160px before the next idea.

## Colour

**Three values and two tints.** Paper, ink, accent, plus ink at ~62% for secondary text and ink at ~14% for rules. That is the palette. Five ready palettes with measured contrast in [reference.md](reference.md).

**Never pure black on pure white.** Ink `#14110D` on paper `#F4F1EA` reads as printed. `#000` on `#FFF` reads as unstyled.

**One accent, used with force.** The accent covers under 5% of the pixels and appears once per screenful: one filled block, or one rule, or one live word. Five colours sprinkled evenly is what a template looks like. One colour used once, at size, is a decision.

**Banned by default:** purple-to-blue gradient heroes, gradient text, glass panels, coloured drop shadows, a second accent hue. Break one only when the brand supplies the colour, and say so in one line.

**Check contrast against the real background.** Body text 4.5:1 minimum. Saturated accents often fail as text and pass as blocks. Use the darker text variant listed for each palette.

## Composition

**Put the weight off centre.** The heavy element sits in the left half or the upper-left quadrant. Answer it with something small and far away. Centred stacks are the default look you are being asked to avoid.

**Leave one quadrant empty.** Split the first screen in four. One quarter stays empty. That emptiness is the design.

**Use one scale jump.** On the first screen one element is roughly 10x another. Display type against an 11px label. Nothing in between.

**Align or bleed, nothing in the middle.** Every edge either sits on a column line or clearly runs off the page. An element 30px inside the margin for no reason is the most common tell of a generated layout.

**Tension by proximity.** Two related things 8px apart, then 160px of nothing before the next idea. Even spacing everywhere is silence with no rhythm.

**Rotate at most one thing,** and only vertical type running along a rule. Never rotate a card.

## Motion

**One signature move per page.** Everything else is 150ms feedback or a plain 400ms fade with a 12px rise. Two signature moves is a page fighting itself. The menu, with code: line-masked display reveal, one horizontal rail, image scale-out on scroll, sticky column against a scrolling column, ground colour change at a section boundary, progress-tied index. See [reference.md](reference.md).

**Three speeds. Never mix the bands.**

| Band | Duration | Use |
| --- | --- | --- |
| Fast | 120-180ms | hover, focus, press, toggle |
| Medium | 300-500ms | element entrance, small layout change |
| Slow | 700-1200ms | the signature move, and nothing else |

A 700ms hover is broken. A 150ms hero reveal is invisible. If you cannot name the band, cut the move.

**Four kinds of motion.**
- Entrance-once: fires when a section first enters view, never re-runs. The default for content.
- Scroll-scrubbed: tied to scroll progress, reverses when you scroll back. One element per page, and only when the movement carries meaning.
- Hover and pointer: state feedback. Fast band only.
- Continuous: marquees and loops. Once per page or not at all, and never beside body copy.

**Travel 8-24px.** A 100px fade-up on every block is the signature of a generated page.

**Stagger 40-80ms, six items maximum.** Past six, animate the group as one object.

**Ease out.** Entrances `cubic-bezier(0.16, 1, 0.3, 1)`. Exits `cubic-bezier(0.4, 0, 1, 1)`. Scrubbed and continuous are `linear`. No bounce or back curves on editorial work.

**Animate `transform` and `opacity` only.** Anything else costs a layout pass on every frame.

**Motion off is the finished page, not a lesser one.** Under `prefers-reduced-motion: reduce` every element sits at its final position with opacity 1. Never ship content that only becomes visible after an animation runs. Write the query in the same edit as the animation.

## The generic tells

If the page has any of these, it is not art-directed. Fix before showing.

1. Largest type under 4x the body size.
2. Three rounded cards in a row with soft shadows.
3. Icons in circles above three feature headings.
4. Everything centre-aligned.
5. A purple or blue gradient behind the hero.
6. Identical padding on every section.
7. Fade-up on every block, same distance, same duration.
8. Four or more hues doing equal work.
9. Emoji standing in for icons.
10. A pill button with a gradient and a shadow.

## Frameworks

Plain CSS is the default here. Custom properties on `:root`, one `.grid` class, real media queries. It runs on any machine with no install.

Tailwind: every value maps to an arbitrary value, for example `text-[clamp(3.25rem,10vw,9rem)] leading-[0.94] tracking-[-0.035em] font-normal`. Put the palette and the scale in the theme instead of repeating arbitrary values everywhere. Do not reach for the default scale. `text-5xl font-bold` is what generic looks like.

Do not install an animation library for one move. `IntersectionObserver` plus a class is nine lines. `animation-timeline: view()` handles scrubbing where supported. Both are in [reference.md](reference.md).

## Stop

Answer every line yes.

- [ ] The direction card is written and the build matches it.
- [ ] Largest type is at least 5x body size, lighter in weight, negative in tracking.
- [ ] No split is 50/50, and exactly one element breaks the grid.
- [ ] Palette is paper, ink, one accent, two tints. Accent under 5% of pixels.
- [ ] One quadrant of the first screen is empty.
- [ ] Exactly one signature move. Every other animation is fast-band or a 12px fade.
- [ ] With reduced motion on, the page is complete and readable.
- [ ] Body text passes 4.5:1 against its real background.
- [ ] None of the ten generic tells is present.

When every line passes, stop. Do not add a section. Do not add a second animation. Do not add a third colour. Show the page.
