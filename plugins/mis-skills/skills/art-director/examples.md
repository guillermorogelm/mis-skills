# Art Director examples

Five things a coding agent produces by default, why each one is wrong, and the replacement. Tailwind and plain CSS are labelled. Numbers come from [reference.md](reference.md).

---

## 1. The hero

### What gets produced (Tailwind)

```html
<section class="flex flex-col items-center justify-center text-center py-24
                bg-gradient-to-br from-indigo-500 to-purple-600">
  <h1 class="text-5xl font-bold text-white mb-6">Build better products, faster</h1>
  <p class="text-xl text-white/80 max-w-2xl mb-8">
    The all-in-one platform for modern teams.
  </p>
  <div class="flex gap-4">
    <button class="rounded-full bg-white px-8 py-3 font-semibold shadow-lg">Get started</button>
    <button class="rounded-full border border-white/40 px-8 py-3 text-white">Learn more</button>
  </div>
</section>
```

### Why it is wrong

1. `text-5xl` is 48px against `text-xl` at 20px. A 2.4x jump. Under 4x reads generic.
2. `font-bold` at 48px. Optical weight climbs with size, so large type needs less weight, not more.
3. Centred stack. No grid, no asymmetry, no empty quadrant, no tension.
4. Gradient hero plus `text-white/80` body. Two banned defaults in one screen.
5. Two buttons of equal weight. The page has no first move.

### Replacement (Tailwind, Newsprint palette, left-heavy archetype)

```html
<section class="grid grid-cols-12 gap-6 px-[clamp(20px,5vw,120px)] pt-[18vh] pb-32
                bg-[#F4F1EA] text-[#14110D]">

  <p class="col-span-12 mb-[clamp(48px,10vh,120px)] text-[11px] font-medium uppercase
            tracking-[0.1em] text-[#6B655C]">01 / Studio</p>

  <h1 class="col-span-12 md:col-span-8 font-normal
             text-[clamp(3.25rem,10vw,9rem)] leading-[0.94] tracking-[-0.035em]">
    <span class="block">A grid you</span>
    <span class="block">can <span class="text-[#A8331B]">see</span></span>
  </h1>

  <p class="col-span-12 md:col-start-10 md:col-span-3 self-end max-w-[42ch]
            text-[1.0625rem] leading-[1.6] text-[#6B655C]">
    Pages built to a written direction card. Type, grid, colour, one move.
  </p>

  <a href="#work" class="col-span-12 md:col-span-4 mt-24 border-t border-[#14110D]/15 pt-4
            text-[1.125rem] transition-colors duration-150 hover:text-[#A8331B]">
    Start a project
  </a>
</section>
```

Display is 144px at desktop against 17px body. That is 8.5x. Weight 400, tracking -0.035em, leading 0.94. Lines are broken by hand. The headline takes columns 1-8 and the lead sits low in 10-12, so the bottom-right quadrant stays empty. One accent, on one word and on one hover.

---

## 2. Three feature cards

### What gets produced (Tailwind)

```html
<div class="grid grid-cols-3 gap-8">
  <div class="rounded-xl border bg-white p-8 shadow-md">
    <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-indigo-100 text-2xl">⚡</div>
    <h3 class="mb-2 text-xl font-semibold">Fast</h3>
    <p class="text-gray-600">We ship quickly without cutting corners.</p>
  </div>
  <!-- two more, identical -->
</div>
```

### Why it is wrong

1. Rounded card plus shadow plus white fill is dashboard language, not page language.
2. Emoji standing in for an icon.
3. Three equal columns. Equal weight means no reading order.
4. `text-xl` headings sit in the middle of the scale. Nothing on screen is large and nothing is small.
5. Content is a list, so it should be a list, and a list reads better as rows than as boxes.

### Replacement (plain CSS, hairline ledger)

```html
<ol class="ledger">
  <li>
    <span class="idx">01</span>
    <h3>Fast</h3>
    <p>Two week builds. Scope written down before anything is drawn.</p>
    <span class="meta">2 weeks</span>
  </li>
  <li>
    <span class="idx">02</span>
    <h3>Direct</h3>
    <p>You talk to the person building it. No account layer.</p>
    <span class="meta">1 person</span>
  </li>
</ol>
```

```css
.ledger{ list-style:none; margin:0; padding:0; }
.ledger li{
  display:grid;
  grid-template-columns: 1fr 5fr 4fr 2fr;      /* uneven, never four equal */
  gap: var(--gutter);
  align-items: baseline;
  padding-block: 40px;
  border-top: 1px solid var(--rule);
}
.ledger li:last-child{ border-bottom: 1px solid var(--rule); }

.idx{ font: 500 11px/1.3 var(--mono); letter-spacing:.1em; color: var(--muted); }
.ledger h3{ margin:0; font-weight:400; letter-spacing:-.02em; line-height:1.05;
            font-size: clamp(1.75rem, 3.2vw, 2.6rem); }
.ledger p{ margin:0; max-width:46ch; font-size:1.0625rem; line-height:1.6; color: var(--muted); }
.meta{ justify-self:end; font-size:11px; text-transform:uppercase;
       letter-spacing:.08em; color: var(--muted); }

@media (max-width: 900px){
  .ledger li{ grid-template-columns: 1fr; gap:12px; }
  .meta{ justify-self:start; }
}
```

Rows instead of boxes. Numbers instead of icons. A 42px heading against an 11px label is a real jump. One hairline does the work three borders and three shadows were doing.

---

## 3. Motion

### What gets produced

```css
.section{ opacity:0; transform: translateY(60px); transition: all .8s ease; }
.section.visible{ opacity:1; transform:none; }
.btn{ transition: all .6s ease; }
.card:hover{ transform: scale(1.05); transition: .5s; }
```

```js
new IntersectionObserver(entries => {
  entries.forEach(e => e.target.classList.toggle('visible', e.isIntersecting));
}).observe(document.querySelector('.section'));
```

### Why it is wrong

1. Every block does the same 60px fade-up. When everything is the signature move, there is no signature move. Travel should be 8-24px.
2. `transition: all` animates layout properties as well as `transform` and `opacity`.
3. A 600ms button transition and a 500ms hover are in the slow band. Hover belongs in 120-180ms.
4. `toggle` re-runs the animation every time a section re-enters, so scrolling back up replays the page.
5. No `prefers-reduced-motion` block, so with motion off the sections stay at `opacity: 0` and the page is blank.

### Replacement (plain CSS and vanilla JS)

One signature move, fast feedback for everything else, and a real reduced-motion state.

```css
/* signature: display lines mask up, once, slow band */
.display .line{ display:block; overflow:hidden; }
.display .line > span{
  display:block; transform: translateY(105%);
  transition: transform 900ms cubic-bezier(.16,1,.3,1);
}
.display.is-in .line > span{ transform:none; }
.display .line:nth-child(2) > span{ transition-delay: 80ms; }

/* everything else: 16px, medium band, opacity and transform only */
.js [data-reveal]{
  opacity:0; transform: translateY(16px);
  transition: opacity 480ms cubic-bezier(.16,1,.3,1),
              transform 480ms cubic-bezier(.16,1,.3,1);
}
.js [data-reveal].is-in{ opacity:1; transform:none; }

/* feedback: fast band, one property */
.btn{ transition: background-color 150ms cubic-bezier(.4,0,.2,1); }
.card-link{ transition: color 150ms cubic-bezier(.4,0,.2,1); }

@media (prefers-reduced-motion: reduce){
  *, *::before, *::after{
    animation-duration:1ms !important; animation-iteration-count:1 !important;
    transition-duration:1ms !important; scroll-behavior:auto !important;
  }
  .js [data-reveal]{ opacity:1; transform:none; }
  .display .line > span{ transform:none; }
}
```

```js
document.documentElement.classList.add('js');
const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
if (!still) {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add('is-in');
      io.unobserve(e.target);          // once, never again
    }
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
  document.querySelectorAll('[data-reveal], .display').forEach(el => io.observe(el));
}
```

The `.js` class is added by script, so if the script never runs the content is visible rather than stuck at zero opacity.

---

## 4. Colour

### What gets produced

```css
:root{
  --primary:#6366F1; --secondary:#EC4899; --success:#10B981;
  --warning:#F59E0B; --dark:#111827; --light:#F9FAFB;
}
.hero{ background: linear-gradient(135deg, #6366F1, #EC4899); }
.btn{ background: linear-gradient(90deg, #6366F1, #8B5CF6);
      border-radius: 9999px; box-shadow: 0 10px 30px rgba(99,102,241,.4); }
h1{ background: linear-gradient(90deg, #6366F1, #EC4899);
    -webkit-background-clip: text; color: transparent; }
```

### Why it is wrong

1. Six hues, all doing equal work. A palette with no hierarchy is a palette with no accent.
2. Gradient text destroys the letterforms at display size and cannot be contrast-checked.
3. A coloured glow shadow under a pill button. Two banned defaults stacked.
4. `#F9FAFB` on `#111827` is the shipped default of every starter template.
5. The indigo appears in the hero, the buttons, the links and the icons. Used everywhere, it carries nothing.

### Replacement (plain CSS, Newsprint)

```css
:root{
  --paper:#F4F1EA; --ink:#14110D; --muted:#6B655C;
  --rule: rgba(20,17,13,.14);
  --accent:#C8452B;        /* blocks and fills: 4.3:1 on paper */
  --accent-text:#A8331B;   /* text: 5.9:1 on paper */
}
body{ background: var(--paper); color: var(--ink); }

h1{ color: var(--ink); }
h1 em{ font-style: normal; color: var(--accent-text); }   /* exactly one word */

.cta{
  background: var(--accent); color: var(--paper);
  border-radius: 2px; padding: 18px 32px; box-shadow: none;
  transition: background-color 150ms cubic-bezier(.4,0,.2,1);
}
.cta:hover{ background: var(--accent-text); }

hr{ border:0; border-top: 1px solid var(--rule); }
a{ color: var(--ink); text-decoration-color: var(--rule); text-underline-offset: 3px; }
a:hover{ color: var(--accent-text); }
```

The accent now appears twice on the first screen: one word and one button. Under 5% of the pixels. Every ratio is measured, not guessed. Full palettes in [reference.md](reference.md).

---

## 5. Section rhythm and small type

### What gets produced (Tailwind)

```html
<section class="py-16">
  <h2 class="text-3xl font-bold mb-4">Services</h2>
  <p class="text-gray-600">What we do for clients.</p>
</section>
<section class="py-16">
  <h2 class="text-3xl font-bold mb-4">Work</h2>
  <p class="text-gray-600">Selected projects.</p>
</section>
```

### Why it is wrong

1. Identical `py-16` on every section. Uniform spacing is a page with no pacing.
2. The gap inside the group and the gap between the groups are close in size, so the groups do not read as groups.
3. `text-3xl font-bold` for every heading. No scale contrast down the page.
4. No small type anywhere. No section numbers, no labels, no meta.
5. One-word headings carrying no content, with the real sentence pushed into grey body text.

### Replacement (plain CSS)

```css
.section{ padding-block: 0 160px; }        /* the gap lives after each section */
.section:first-of-type{ padding-top: 18vh; }
.section--pair{ padding-bottom: 96px; }    /* a closely related pair sits nearer */

.section__label{
  font-size:11px; text-transform:uppercase; letter-spacing:.1em; color: var(--muted);
  border-top: 1px solid var(--rule); padding-top: 12px; margin: 0 0 56px;
}
.section__title{
  margin: 0 0 16px; font-weight: 400; line-height: 1.03; letter-spacing: -.025em;
  font-size: clamp(2.4rem, 6vw, 4.75rem);
}
.section__lead{
  margin: 0; max-width: 44ch; font-size: 1.5rem; line-height: 1.35;
  letter-spacing: -.005em; color: var(--muted);
}
.col-label{ grid-column: 1 / -1; }
.col-title{ grid-column: 1 / span 7; }
.col-lead { grid-column: 9 / -1; align-self: end; }

@media (max-width: 900px){
  .section{ padding-block: 96px; }
  .col-title, .col-lead{ grid-column: 1 / -1; }
}
```

```html
<section class="section grid">
  <p  class="section__label col-label">02 / Services</p>
  <h2 class="section__title col-title">Pages that hold a direction</h2>
  <p  class="section__lead  col-lead">Type, grid, colour, one move. Written before anything is drawn.</p>
</section>
```

Heading at 76px against a label at 11px is a 7x jump on one line of the page. The rule and the number give the section an address. The 56px gap under the label, the 16px gap under the title and the 160px gap between sections build a rhythm you can feel while scrolling.
