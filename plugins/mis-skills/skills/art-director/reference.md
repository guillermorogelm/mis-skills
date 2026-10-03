# Art Director reference

Numbers, tables and code. Open the section you need. Do not read it end to end.

---

## 1. Type scales

Pick one ratio for the page. Every size except display comes off that ladder.

**1.2 minor third, base 16px. Dense pages, documentation, anything with a lot of running text.**

| Step | px | Use |
| --- | --- | --- |
| -2 | 11 | label, uppercase |
| -1 | 13 | caption, meta |
| 0 | 16 | body |
| 1 | 19 | lead |
| 2 | 23 | subhead |
| 3 | 28 | h3 |
| 4 | 33 | h2 |
| 5 | 40 | h1 |
| display | 72-110 | off the ladder |

**1.333 perfect fourth, base 18px. The default. Landing pages, editorial, most work.**

| Step | px | Use |
| --- | --- | --- |
| -2 | 10 | micro label |
| -1 | 13.5 | caption |
| 0 | 18 | body |
| 1 | 24 | lead |
| 2 | 32 | subhead |
| 3 | 43 | h3 |
| 4 | 57 | h2 |
| 5 | 76 | h1 |
| display | 100-150 | off the ladder |

**1.5 perfect fifth, base 18px. Posters, single-idea pages, very little text.**

| Step | px | Use |
| --- | --- | --- |
| -1 | 12 | label |
| 0 | 18 | body |
| 1 | 27 | lead |
| 2 | 41 | subhead |
| 3 | 61 | h2 |
| 4 | 91 | h1 |
| display | 137-205 | off the ladder |

**Display sits above the ladder.** Minimum 5x body. That jump is the contrast that reads as art direction. A page whose largest type is 2.5x its body looks like a template even with perfect colour and spacing.

### Fluid sizes

For a target size S in px at a 1440px viewport, the vw term is `S / 14.4`.

```css
:root{
  --step--1: clamp(0.78rem, 0.76rem + 0.1vw, 0.84rem);
  --step-0:  clamp(1rem, 0.96rem + 0.2vw, 1.125rem);   /* body 16 -> 18 */
  --step-1:  clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);  /* lead */
  --step-2:  clamp(1.5rem, 1.3rem + 1vw, 2rem);        /* subhead */
  --step-3:  clamp(1.9rem, 1.5rem + 2vw, 2.7rem);
  --step-4:  clamp(2.4rem, 1.7rem + 3.5vw, 3.6rem);
  --display: clamp(3.25rem, 1.2rem + 10vw, 9rem);      /* 52 -> 144 */
}
```

Set the minimum around 55-65% of the maximum. Below that, phones lose the scale contrast entirely and the page flattens.

### Optical settings

| Size | Weight | Tracking | Leading | Notes |
| --- | --- | --- | --- | --- |
| 10-13px | 500-600 | +0.08em to +0.12em uppercase | 1.3 | labels, section numbers |
| 14-15px | 400-500 | +0.01em | 1.45 | captions, meta rows |
| 16-20px | 400 | 0 | 1.5-1.65 | body |
| 21-28px | 400 | -0.005em | 1.3-1.4 | lead paragraph |
| 30-40px | 400-500 | -0.015em | 1.2 | subhead |
| 44-72px | 400-500 | -0.02em | 1.05-1.12 | headline |
| 80-140px | 300-400 | -0.035em | 0.94-1.0 | display |
| 140px+ | 300 | -0.045em | 0.88-0.92 | poster display |

Two more, both cheap and both visible:

```css
h1, h2, .display { text-wrap: balance; }
p { text-wrap: pretty; }
body { font-optical-sizing: auto; }
.numbers { font-variant-numeric: tabular-nums; }
```

### Measure

| Role | Characters |
| --- | --- |
| body | 60-75 |
| lead paragraph 22-24px | 40-50 |
| caption | 30-45 |
| display | 8-18, hand-broken |

Set it with `max-width: 66ch` on the text element, not on the container.

Break display lines by hand. Do not let a box decide where a headline wraps.

```html
<h1 class="display">
  <span class="line">A grid you can</span>
  <span class="line">actually see</span>
</h1>
```

### Font stacks with no download

```css
--sans: ui-sans-serif, -apple-system, "Segoe UI", Inter, "Helvetica Neue", Arial, sans-serif;
--serif: ui-serif, "Iowan Old Style", Georgia, "Times New Roman", serif;
--mono: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, Consolas, monospace;
```

On Apple platforms `ui-serif` resolves to New York, which holds up at display sizes. `ui-monospace` at 11px uppercase makes a good label face on any platform.

### Pairings that exist on Google Fonts

Load two weights maximum from each. Always `font-display: swap`.

| Display | Body | Character |
| --- | --- | --- |
| Instrument Serif 400 | Inter 400/500 | editorial, quiet |
| Fraunces 300 (soft optical) | Inter 400 | warm, printed |
| Archivo Expanded 500 | Newsreader 400 | poster, loud |
| Space Grotesk 500 | IBM Plex Sans 400 | technical |
| Libre Caslon Display 400 | Public Sans 400 | classical |

One family in three weights is a valid answer and often the better one.

---

## 2. Grid

```css
:root{
  --cols: 12;
  --gutter: 24px;
  --margin: clamp(20px, 5vw, 120px);
  --unit: 8px;
}
@media (max-width: 900px){ :root{ --cols: 6; --gutter: 16px } }
@media (max-width: 600px){ :root{ --cols: 4 } }

.grid{
  display: grid;
  grid-template-columns: repeat(var(--cols), minmax(0, 1fr));
  gap: var(--gutter);
  padding-inline: var(--margin);
  max-width: 1680px;
  margin-inline: auto;
}
```

Placement, written as intent rather than magic numbers:

```css
.hero-type   { grid-column: 1 / span 8; }
.hero-meta   { grid-column: 11 / -1; align-self: end; }
.body-copy   { grid-column: 3 / span 5; }
.side-note   { grid-column: 9 / span 3; }

/* the one deliberate break: bleeds off the right edge */
.bleed-right { grid-column: 8 / -1; margin-right: calc(var(--margin) * -1); }
.bleed-full  { grid-column: 1 / -1; margin-inline: calc(var(--margin) * -1); }
```

### Splits

| Split | Reads as |
| --- | --- |
| 6+6 | template |
| 7+5 | decided |
| 8+4 | editorial, image plus caption column |
| 5+7 with 1-col offset | magazine spread |
| 4+7, one column left empty | gallery |

### Spacing scale

`8, 16, 24, 32, 48, 64, 96, 128, 160, 192, 256`

| Gap | Meaning |
| --- | --- |
| 8-16 | parts of the same object |
| 24-32 | related items in a group |
| 48-64 | groups inside a section |
| 96-128 | between sections |
| 160-256 | between chapters, or before a section that must land |

Vary it. A page where every section is 96px apart has no pacing. Compress a heading and its lead to 16px, then leave 160px.

### Hairlines instead of cards

```css
.rule       { border: 0; border-top: 1px solid color-mix(in srgb, var(--ink) 14%, transparent); }
.ledger > * { border-top: 1px solid color-mix(in srgb, var(--ink) 14%, transparent);
              padding-block: 32px; }
.ledger > *:last-child { border-bottom: 1px solid color-mix(in srgb, var(--ink) 14%, transparent); }
```

Fallback without `color-mix`: `rgba(20, 17, 13, 0.14)`.

Rules to keep: no `border-radius` above 4px, no `box-shadow` on content blocks, no filled card backgrounds unless a block is genuinely a different surface.

---

## 3. Colour

Every ratio below is measured, not estimated. Body text needs 4.5:1.

**Newsprint.** Warm paper, vermillion.

```css
--paper:#F4F1EA; --ink:#14110D; --muted:#6B655C;
--rule:rgba(20,17,13,.14); --accent:#C8452B; --accent-text:#A8331B;
```
ink 16.7:1, muted 5.1:1, accent block 4.3:1, accent-text 5.9:1, paper on accent block 4.3:1.

**Gallery.** Near white, electric blue.

```css
--paper:#FAFAF8; --ink:#0E0E0E; --muted:#6E6E6E;
--rule:rgba(14,14,14,.12); --accent:#1B4DF0; --accent-text:#1B4DF0;
```
ink 18.5:1, muted 4.9:1, accent 6.0:1, white on accent 6.2:1.

**Studio dark.** Near black ground, acid accent.

```css
--paper:#0C0C0D; --ink:#E9E6E1; --muted:#8B8781;
--rule:rgba(233,230,225,.16); --accent:#D6FF4B; --accent-text:#D6FF4B;
```
ink 15.7:1, muted 5.5:1, accent 17.0:1. Put ground colour on the accent block, never white.

**Bauhaus.** Flat red, one flat blue used exactly once.

```css
--paper:#EFEBE4; --ink:#101010; --muted:#6A665F;
--rule:rgba(16,16,16,.14); --accent:#E23D28; --accent-text:#C6301C; --second:#1D4E9B;
```
ink 16.0:1, muted 4.8:1, accent block 3.6:1 so never as body text, accent-text 4.6:1, second 6.8:1. The blue appears as one solid block on the page and nowhere else.

**Stone.** Cool grey paper, deep green.

```css
--paper:#E8E6E1; --ink:#1C1B19; --muted:#5F5D58;
--rule:rgba(28,27,25,.14); --accent:#2E5E4E; --accent-text:#2E5E4E;
```
ink 13.8:1, muted 5.3:1, accent 6.0:1, white on accent 7.4:1.

### Accent discipline

- Under 5% of visible pixels on any screenful.
- One use per screenful. A filled block, or a rule, or one live word. Not all three.
- Body text stays ink. Secondary text stays muted. The accent is never a paragraph.
- The strongest use is a single solid rectangle at scale, not a coloured word here and there.
- Hover states shift ink opacity or add an underline. They do not add a new colour.

### Dark mode

Do not invert. Write a second palette and re-check ratios.

```css
@media (prefers-color-scheme: dark){
  :root{ --paper:#0C0C0D; --ink:#E9E6E1; --muted:#8B8781;
         --rule:rgba(233,230,225,.16); --accent:#D6FF4B; }
}
```

Reduce weight by 100 in dark mode at display sizes. Light type on dark ground gains apparent weight.

---

## 4. Motion

### Bands

| Band | Duration | Easing | Use |
| --- | --- | --- | --- |
| Fast | 120-180ms | `cubic-bezier(0.4, 0, 0.2, 1)` | hover, focus, press, toggle |
| Medium | 300-500ms | `cubic-bezier(0.16, 1, 0.3, 1)` | entrances, small layout change |
| Slow | 700-1200ms | `cubic-bezier(0.16, 1, 0.3, 1)` | the signature move |
| Scrubbed | tied to scroll | `linear` | one scroll-linked element |

Distance: entrances travel 8-24px. Scale entrances go 0.96 to 1, never 0.8 to 1.
Stagger: 40-80ms, six items maximum.
Properties: `transform` and `opacity` only. Add `will-change` only to the one signature element, and remove it when the move is finished.

### Reveal machinery

Hide from CSS only after JS confirms it is running, so a JS failure leaves a readable page.

```html
<section data-reveal>...</section>
```

```js
document.documentElement.classList.add('js');
const io = new IntersectionObserver((entries) => {
  for (const e of entries) {
    if (!e.isIntersecting) continue;
    e.target.classList.add('is-in');
    io.unobserve(e.target);
  }
}, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
document.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));
```

```css
.js [data-reveal]{
  opacity: 0; transform: translateY(16px);
  transition: opacity 480ms cubic-bezier(.16,1,.3,1),
              transform 480ms cubic-bezier(.16,1,.3,1);
}
.js [data-reveal].is-in{ opacity: 1; transform: none; }
```

Wait for fonts before the first reveal, or the headline animates and then reflows.

```js
document.fonts.ready.then(() => document.documentElement.classList.add('fonts-ready'));
```

### Signature move menu

Pick one per page. Code is plain CSS and vanilla JS.

**A. Line-masked display reveal.** The editorial default.

```html
<h1 class="display reveal">
  <span class="line"><span>A grid you</span></span>
  <span class="line"><span>can see</span></span>
</h1>
```
```css
.reveal .line{ display:block; overflow:hidden; }
.reveal .line > span{
  display:block; transform: translateY(105%);
  transition: transform 900ms cubic-bezier(.16,1,.3,1);
}
.reveal.is-in .line > span{ transform: none; }
.reveal .line:nth-child(2) > span{ transition-delay: 80ms; }
.reveal .line:nth-child(3) > span{ transition-delay: 160ms; }
```

**B. Horizontal rail on vertical scroll.** One section only.

```css
.rail-wrap{ height: 300vh; }
.rail-stick{ position: sticky; top: 0; height: 100vh; overflow: hidden;
             display: flex; align-items: center; }
.rail{ display: flex; gap: 48px; will-change: transform; }
```
```js
const wrap = document.querySelector('.rail-wrap');
const rail = document.querySelector('.rail');
const travel = () => rail.scrollWidth - window.innerWidth;
addEventListener('scroll', () => {
  const r = wrap.getBoundingClientRect();
  const p = Math.min(1, Math.max(0, -r.top / (wrap.offsetHeight - innerHeight)));
  rail.style.transform = `translate3d(${-p * travel()}px,0,0)`;
}, { passive: true });
```

**C. Image scale-out on scroll.** Pure CSS where supported.

```css
@supports (animation-timeline: view()){
  .scale-out{ animation: scaleOut linear both; animation-timeline: view();
              animation-range: entry 0% cover 60%; }
  @keyframes scaleOut{ from{ transform: scale(1.14) } to{ transform: scale(1) } }
}
```
Without support the image sits at scale 1. That is a correct fallback, not a broken one.

**D. Sticky column against a scrolling column.** Costs nothing, reads as designed.

```css
.pair{ display:grid; grid-template-columns: 5fr 7fr; gap: var(--gutter); }
.pair > .fixed{ position: sticky; top: 12vh; align-self: start; }
```

**E. Ground colour change at a section boundary.**

```css
body{ background: var(--paper); transition: background-color 800ms ease; }
body[data-ground="dark"]{ --paper:#0C0C0D; --ink:#E9E6E1; }
```
```js
const groundIO = new IntersectionObserver((es) => {
  for (const e of es) if (e.isIntersecting)
    document.body.dataset.ground = e.target.dataset.ground;
}, { threshold: 0.5 });
document.querySelectorAll('[data-ground]').forEach(el => groundIO.observe(el));
```
Set `color: var(--ink)` on `body` so text follows the ground. Give every section a `data-ground` value, including the light ones, or the ground never changes back.

**F. Progress-tied index.** A sticky 11px label that names the current section and its number. Quiet, and it carries meaning rather than decorating.

### Reduced motion

Write this in the same edit as the animation.

```css
@media (prefers-reduced-motion: reduce){
  *, *::before, *::after{
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 1ms !important;
    scroll-behavior: auto !important;
  }
  /* then restore final states explicitly */
  .js [data-reveal]{ opacity: 1; transform: none; }
  .reveal .line > span{ transform: none; }
  .rail{ transform: none !important; }
  .rail-wrap{ height: auto; }
  .rail-stick{ position: static; height: auto; overflow-x: auto; }
}
```

Guard the JS as well, so scroll handlers do not fight the query.

```js
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!still) { /* attach scroll and rail handlers */ }
```

Test by turning reduced motion on and reloading. Every word must be visible, every section reachable, nothing mid-animation.

---

## 5. Hero archetypes

Four that work. Pick one, do not blend two.

**Left-heavy.** Display in columns 1-8, hand-broken to two lines. An 11px label in column 12, bottom-aligned. One image bleeding off the right edge, its top aligned to the headline baseline. Bottom-left quadrant empty.

**Split rule.** Display across columns 1-10 above a full-bleed hairline. Below the rule, a four-item meta row on uneven spans: 3, 2, 4, 3. Nothing else on the screen.

**Off-axis.** Display in columns 3-11, pushed down 22vh so the top of the screen is empty. Lead paragraph in columns 3-6 at 24px. A single accent rule in column 12 running full height.

**Poster block.** Display fills the viewport at 140px or more, tracking -0.045em, weight 300. One word in the accent colour. A single 11px line in the bottom corner. Nothing else, and no scroll cue.

---

## 6. Before you show it

- Body text 4.5:1 against its real background, including over images.
- Focus visible on every interactive element: `outline: 2px solid var(--accent); outline-offset: 3px`.
- Tap targets 44px minimum.
- No horizontal scroll at 360px wide.
- Images have width and height set so nothing jumps as they load.
- Headlines are real `h1`/`h2`, not styled divs.
- Reduced motion tested by reloading with the setting on.
