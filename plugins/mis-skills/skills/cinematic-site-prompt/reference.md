# Reference

## Scene patterns

Map each section of the site to one of these. Each has its three beats.
Mix freely; never use the same pattern three times in a row.

| Pattern | Good for | Establishing shot | Action | Cut |
|---|---|---|---|---|
| Opening titles | Hero | Black screen, letterbox bars, grain | Name fades up in wide-tracked capitals, one line types in as a subtitle | First scroll opens the bars onto a full-bleed photo; the name docks into the header |
| Pinned photo + subtitles | Personal story, about | Full-bleed photo, pinned | Slow push-in (scale 1.0 to 1.08); story arrives one sentence per scroll step as subtitles | Dip to black |
| Map route | Moving, travel, origin story | Minimal hairline map | A line draws from A to B as you scroll, the view follows the tip | Map crossfades into the destination photo |
| Queue / counter | Volume of work, support, deliveries | Empty desk or panel | Items drop into a queue, each gets stamped, a tabular counter ticks to the real number | Counter holds with a short pulse |
| Terminal | A working tool, a technical skill | Dark panel, monospace, blinking cursor | The real tool runs; results print line by line as they arrive | One-line invitation to the next scene |
| Horizontal reel | Projects | Section pins; title card for project 1 | Vertical scroll moves the reel sideways; each project gets a title card then the work in a browser or phone frame; hover tilts and plays a muted loop | Click expands the frame into the case study in one continuous shot |
| Phone demo | Chatbots, apps, WhatsApp flows | Phone frame centered | A real conversation plays in real time, typing dots included, loops with a pause | Hard cut |
| Day-to-night | A product that works while you sleep, before/after | Scene in daylight grade | Light shifts across the scene as you scroll | Night holds |
| Credits roll | Work history, clients, skills, footer | Black, centered type | Roll speed follows scroll speed; stopping scroll stops the roll | Last line holds |
| Departments | Skills | Four columns like credit departments | Lines fade up with a 60 ms stagger | Hard cut |
| One quote per frame | Testimonials | Full-screen quote in large italic serif | Scroll cuts to the next quote; "1 / n" counter | Hard cut |
| Final scene | Contact | Letterbox returns, portrait on one side | The real form on the other side, labels always visible | Success state as a subtitle |
| End credits | Footer | Bars almost closed | Slow roll of credits, links, copyright | Back-to-top rewinds the film at speed |

Slates between scenes: "01 · Name", "02 · Name" - a scene number, a scene
name, a thin rule. They double as the navigation anchors.

## The motion system (copy and adjust)

- One easing for entrances (expo out), one for exits (power2 in). Nothing
  linear except grain and credit rolls
- Durations: small UI 200-300 ms, element entrances 600-900 ms, scene
  transitions 1-1.4 s
- Scroll-scrubbed scenes are tied to scroll position, not time; scrolling
  back rewinds exactly
- No pin longer than about 1.5 screen heights of scroll
- Text arrives in reading order, one line or phrase at a time, never letter
  by letter (one typed line in the opening is the exception)
- Nothing animates off screen; loops pause when out of view
- Smooth scrolling never hijacks direction or speed
- Cuts are hard cuts or dips to black; no cross-dissolves between unrelated
  scenes

## Stacks

| Situation | Stack |
|---|---|
| Person builds with Next.js / React (default) | Next.js App Router, TypeScript, Tailwind with CSS-variable tokens, GSAP + ScrollTrigger, Lenis. No Framer Motion, AOS or Locomotive |
| Astro / content-first person | Astro, islands for motion only, GSAP + ScrollTrigger, Lenis |
| Tiny site, no build step wanted | One self-contained HTML file, GSAP + ScrollTrigger and Lenis from a CDN, no other dependency |
| 3D hero wanted | Add three.js for the hero only, lazy-loaded, with a still image fallback |

Always: motion code client-only and lazy-loaded after first paint; the page
fully readable with JavaScript off; images AVIF with WebP fallback and
explicit sizes; fonts self-hosted and subset.

## Art direction defaults

Color tokens (adjust hue to the person, keep the roles; names can follow the theme, e.g. `--dusk` for the accent):

| Token | Role | Default |
|---|---|---|
| `--ink` | Base background, slightly warm near-black | #0E0D0C |
| `--paper` | Text on dark, warm off-white | #F2EEE6 |
| `--ash` | Secondary text, rules | #8A847B |
| `--accent` | One accent, used sparingly: route lines, counters, focus, cursor | pick from their place or brand (Andean dusk amber #E0A24A, Lisbon tile blue, etc.) |
| `--scene` | Optional, one scene only (WhatsApp green, a client's brand) | - |

Type roles:

| Role | Use | Suggestions (with fallback) |
|---|---|---|
| Titles | Wide-tracked capitals, film titles | Neue Haas Grotesk Display Condensed, Oswald, Bebas Neue |
| Body | Readable serif, 18-20 px desktop, 17 px mobile, 60-70 characters per line | Source Serif 4, Newsreader |
| Subtitles | Body serif italic, centered, lower third | - |
| Data | Monospace with tabular numerals for counters and terminals | JetBrains Mono, IBM Plex Mono |

Photography: one grade for every photo (lifted blacks, warm highlights,
slightly desaturated greens, soft vignette); heroes full bleed, never in
cards; the portrait used at most twice.

Texture: fine animated grain at 3-4% opacity from a small canvas or tiled
noise, never a large GIF; letterbox (2.39:1) in opening and closing only.

Cursor (desktop only): a small ring in the accent that grows over
interactive elements and shows a verb inside ("Ver", "Open", "Write").

## Budgets

| Area | Default target |
|---|---|
| LCP | under 2.0 s, mid-range phone, 4G |
| CLS | under 0.05 |
| INP | under 200 ms |
| Lighthouse (mobile) | 95+ Performance, Accessibility, Best Practices, SEO |
| Initial JS | under 120 KB gzipped |
| Each video loop | under 1.5 MB, loaded within one screen of its scene |
| Fonts | at most three families |

## Always-included sections

- **Languages**: route per language, `hreflang` both ways, switch keeps the
  scene and crossfades copy without reload, every string in a content file
- **Reduced motion**: no pinning, parallax, grain or loops; each scene a
  still frame with a 200 ms fade; reel becomes a list; counters show the
  final number. Plus a footer toggle remembered locally
- **Mobile**: vertical reel, thinner letterbox, no tilt, no custom cursor,
  posters instead of loops, 44 px tap targets
- **No-JS**: readable document, links work, forms submit
- **Accessibility**: landmarks, one h1, h2 per scene, skip link first,
  keyboard path through reel, tool and form, visible focus in the accent,
  alt text in every language, decorative layers `aria-hidden`, animated
  text present in the DOM in reading order
- **SEO**: title and description from the real copy, Open Graph image per
  language, JSON-LD `Person` and `Organization` where they apply, sitemap
  and robots including sub-pages

## Banned

- "Fade in on scroll" as a scene's only motion
- Skill percentage bars, logo walls, stock photography, typewriter effects
  on every heading, scroll-jacking, auto-playing sound
- Invented numbers, quotes, clients, awards or dates
- Rewriting the person's existing copy without saying so

## Checklist

- [ ] First line: name in quotes, what is being redesigned (domain), who it
      is for, "plays like a short film you scroll, pause, watch and reply to"
      or equivalent verbs
- [ ] Section 0 has the logline and the "whole point - must feel like X,
      not Y" line
- [ ] Stack names motion libraries and forbids the rest
- [ ] Color tokens with hex values, type roles with fallbacks
- [ ] Motion system with numbers (easing, durations, pin limit)
- [ ] Every scene has a slate, layout, establishing shot, action, cut and
      mobile behavior
- [ ] Every existing section and working feature is present or its drop is
      explained
- [ ] All quoted copy is verbatim and marked as existing; every gap is a
      `[PLACEHOLDER: ...]`
- [ ] Languages, reduced motion, mobile, no-JS, performance (with numbers),
      accessibility and SEO sections all present
- [ ] Assets list with "do not fake them"
- [ ] "Done means" checklist at the end
- [ ] No banned adjectives, no em dashes, 2,000-3,500 words
