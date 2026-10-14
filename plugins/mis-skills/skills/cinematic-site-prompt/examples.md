# Example

One full prompt, written for the redesign of guillermorogel.com from its live
site. It is the bar for length, coverage and tone.

## How it was made

**Facts gathered from the current site (Step 1):** name, role (web developer
and server administrator), Cuenca to Quito story, QuitoWeb, USFQ studies, the
bio line verbatim, the page title verbatim, section order and headings
("De Cuenca a Quito", "Cincuenta tickets al día", "Revisa tu dominio", "Lo que
he construido", "Trayectoria", "Lo que sé hacer", "Lo que dicen mis clientes",
"Cuéntame qué necesitas"), five projects with domains, two testimonials with
attribution, work history, skills, LinkedIn and GitHub, the obfuscated email,
the ES/EN switch, the CV download, the domain checker and the contact form.

**The film (Step 2):**
- Logline: from Cuenca to Quito, someone who answers fifty tickets a day and
  builds websites that load fast
- Feel contrast: a title sequence, not a template with fade-ins
- Signature moment: the project frame that expands into its case study in one
  continuous shot
- Scenes: opening titles, pinned photo + subtitles (Cuenca), map route
  (Quito), queue / counter (support), terminal (domain checker), horizontal
  reel (projects) with phone demo and day-to-night inside it, credits roll
  (career), departments (skills), one quote per frame (testimonials), final
  scene (contact), end credits

**Stack (Step 3):** Next.js, because the person already builds with it.

**What to notice:**
- The two working features (domain checker, contact form) are kept and
  restyled, never replaced by a mock.
- Every quote of copy is marked as existing; the case studies get explicit
  placeholders because no results were on the site.
- The performance section ties back to the person's own promise ("sitios web
  que cargan rápido"), which turns a generic budget into part of the story.
- "Done means" restates the non-negotiables as things a reviewer can tick.

## The prompt

````
Build "Guillermo Rogel" - a full cinematic redesign of guillermorogel.com: a bilingual (Spanish first, English switch) portfolio for a web developer and server administrator in Quito, that plays like a short film you scroll, pause, watch and reply to. It replaces the current site in place, keeps every piece of real content and every working feature, and must still load as fast as the bio promises.

---

## 0. The idea in one paragraph

The current site tells a good story - a person from Cuenca who moved to Quito, answers fifty support tickets a day, runs servers and builds websites that load fast - but it reads like a document. The new site tells the same story as a film. Each section is a scene with an establishing shot, an action and a cut. The visitor is the camera: scrolling moves it forward, stopping holds the frame, scrolling back rewinds. By the end credits they know who Guillermo is, what he has built, who vouches for him, and they are one click from writing to him.

The whole point - it must feel like a title sequence, not a template with fade-ins. If a section could be described as "the text fades up when it enters the viewport", it is not done.

---

## 1. Stack and architecture

- Next.js (App Router), TypeScript, React Server Components for all static content
- Styling: Tailwind CSS with design tokens defined as CSS variables (see section 2)
- Motion: GSAP + ScrollTrigger for scroll-driven scenes, Lenis for smooth scroll. No other animation library (no Framer Motion, no AOS, no Locomotive)
- Motion code is client-only, split per scene and lazy-loaded after first paint. The page is fully readable with JavaScript disabled
- Images through `next/image`, AVIF with WebP fallback, explicit sizes, blur placeholders
- Video: short MP4 (H.264) + WebM loops, muted, `playsinline`, poster frames, loaded only when the scene is near the viewport
- Fonts self-hosted with `next/font`, subset to Latin + Spanish characters, `font-display: swap`
- i18n with route segments `/es` and `/en`, Spanish as default at `/`, one shared content file per language (JSON or MDX), no copy hardcoded in components
- Deployable as a static export or on Vercel/any Node host; no database required. The contact form posts to the existing handler
- Project case studies as their own routes: `/proyectos/[slug]` and `/en/projects/[slug]`

Folder sketch:

```
app/
  [locale]/
    page.tsx                 # the film
    proyectos/[slug]/page.tsx
  api/domain-check/route.ts  # the existing domain diagnostic, ported
components/
  scenes/                    # one file per scene
  film/                      # Letterbox, Grain, Slate, Subtitle, Credits
  ui/
content/
  es.json
  en.json
lib/motion/                  # shared easing, timelines, reduced-motion guard
public/media/                # photos, posters, loops
```

---

## 2. Art direction

### Color grade
- `--ink`: near-black, slightly warm (around #0E0D0C), the base of every scene
- `--paper`: warm off-white (around #F2EEE6) for text on dark
- `--ash`: mid warm grey for secondary text and rules
- `--dusk`: one accent, Andean-dusk amber (around #E0A24A), used sparingly: the route line, the counter, active states, the cursor ring
- `--signal`: a WhatsApp-adjacent green used only inside the WhatsApp scene
- No gradients on UI. The only gradients are light: vignettes and the day-to-night shift
- All text meets WCAG AA on its background

### Photography
- Every photo graded to one look: lifted blacks, warm highlights, slightly desaturated greens, soft vignette
- Photos of Cuenca and Quito are hero plates, shown full bleed with a slow push-in, never in cards
- Portrait of Guillermo: one strong frame, side-lit, used once in the opening and once in the end credits

### Typography
- Titles: a condensed grotesk in wide-tracked capitals (for example "Neue Haas Grotesk Display Condensed", fallback "Oswald" or "Bebas Neue"), used like film titles
- Body: a readable text serif (for example "Source Serif 4" or "Newsreader") at 18-20 px on desktop, 17 px on mobile, line length 60-70 characters
- Data, terminal and counters: a monospace with tabular numerals (for example "JetBrains Mono" or "IBM Plex Mono")
- Subtitles: the body serif in italic, centered, in the lower third, like film subtitles

### Film texture
- Fine animated film grain over everything, 3-4% opacity, generated on a small canvas or as a tiled noise texture, never a large GIF
- Letterbox bars (2.39:1) in the opening and closing scenes only
- Slates: chapter cards that look like clapperboard slates, minimal - a scene number, a scene name, a thin rule
- Cuts are hard cuts or quick dips to black, never cross-dissolves between unrelated scenes

### Cursor
- Desktop only: a small ring in `--dusk` that grows over interactive elements and shows a word inside it ("Ver", "Abrir", "Escribir") on project frames, links and the form. Native cursor stays available for text selection

---

## 3. The motion system

Shared rules every scene follows:

- Easing: one house curve for entrances (expo out), one for exits (power2 in). Nothing linear except the film grain and the end-credit roll
- Durations: small UI 200-300 ms, element entrances 600-900 ms, scene transitions 1-1.4 s
- Scroll-scrubbed scenes are tied to scroll position (scrub with slight smoothing), not to time. Scrolling back rewinds exactly
- Pinned scenes never pin longer than about 1.5 screen heights of scroll; the visitor must never feel stuck
- Text arrives in reading order, one line or phrase at a time, never letter by letter (except the single typed bio line in the opening)
- Nothing animates off screen; loops pause when out of view (IntersectionObserver)
- No scroll-jacking of the wheel itself: Lenis smooths it, it does not hijack direction or speed
- `prefers-reduced-motion`: every scene has a still version (see section 6)

---

## 4. The film, scene by scene

Use all existing copy verbatim from the current site, in both languages. Where this prompt quotes copy, it is the current copy. Where it says "existing copy", pull it from the current site, do not rewrite it.

### Scene 00 - Opening titles
- Layout: full black screen, letterbox bars top and bottom, grain on
- Beat 1: after first paint, "GUILLERMO ROGEL" fades up in the condensed titles, tracking slowly tightening by a few percent over 1.5 s
- Beat 2: below it, the bio types in as a subtitle: "Me encargo de servidores, dominios y correo, y hago sitios web que cargan rápido." (EN: the existing English version)
- Beat 3: a small line at the bottom: "Quito, Ecuador · UTC−5" and a scroll cue - a thin vertical line that draws itself downward and repeats
- First scroll: the letterbox bars slide apart, the black opens onto the dawn photo of Cuenca at full bleed. The title shrinks and docks into the header as the name
- Header (appears after the opening): name on the left; on the right "Proyectos", "Trayectoria", "Soporte", "Contacto", ES/EN switch and "Descargar CV". Transparent over photos, gains a thin `--ink` backing once scrolled past the first scene. Keep the skip-to-content link as the first focusable element

### Scene 01 - Cuenca
- Slate: "01 · Cuenca"
- Establishing shot: the Cuenca photo, pinned, slow push-in (scale 1.0 to 1.08 over the pin)
- Action: the first part of the existing "De Cuenca a Quito" story arrives as subtitles, one sentence per scroll step, each replacing the last
- Cut: dip to black

### Scene 02 - Quito
- Slate: "02 · Quito"
- Establishing shot: a minimal outline map of Ecuador in `--ash` hairlines on `--ink`. A dot pulses at Cuenca
- Action: as you scroll, a thin `--dusk` line draws the route north from Cuenca to Quito, the camera (the SVG viewBox) follows the line's tip. When it reaches Quito the map crossfades into the Quito photo, which pushes in
- The rest of the existing story arrives as subtitles: moving to Quito, studying Finance and Business Administration at USFQ, starting QuitoWeb
- The existing personal photos appear as small "polaroid" frames that drift in from the edges at different scroll speeds (parallax), slightly rotated, with existing captions

### Scene 03 - Soporte: "Cincuenta tickets al día"
- Slate: "03 · Soporte"
- Title: "Cincuenta tickets al día" in titles
- Action: the existing sample support tickets fall into a vertical queue like cards dropping onto a desk, each with subject, a channel label and a time. As you scroll, each ticket gets a "Resuelto" stamp in `--dusk` that lands with a tiny overshoot, then slides off to the left
- A large tabular counter in the corner ticks from 0 to 50 in step with the scroll and holds at 50 with a short pulse
- Below, the existing support skills (technical documentation, ticket triage, escalation) appear as three short lines, not cards
- Mobile: the queue shows three tickets at a time, the counter sits above it

### Scene 04 - "Revisa tu dominio" (the working tool)
- Slate: "04 · Diagnóstico"
- Must keep working exactly like today: the visitor types a domain and gets the existing checks
- Styled as a terminal window: `--ink` panel, monospace, a blinking `--dusk` block cursor in the input, prompt prefix `$ revisa`
- On submit, results print line by line (DNS, SSL, mail records and whatever the current tool checks), each with a status mark (ok / warning / error) and a one-line human explanation in the serif. Lines print at the speed the real responses arrive; no fake delays beyond 80 ms per line
- Errors, empty input and network failure each have a clear message in both languages
- Under the result, one line: a soft invitation to the contact scene if something failed

### Scene 05 - Proyectos: "Lo que he construido"
- Slate: "05 · Proyectos"
- Desktop: a horizontal reel. The section pins and vertical scroll moves the reel sideways. A thin progress rule at the bottom shows position, with project numbers above it
- One scene per project, in this order:
  1. C.16 Beauty Studio (c16beauty.com) - online store with AI features
  2. QuitoWeb (quitoweb.com) - his company
  3. Kronic Arquitectura (kronic-arquitectura.com) - website
  4. Recorre Travel (recorretravel.com) - website and business email
  5. Spa Cumbayá - WhatsApp assistant demo
- Each project scene: a title card first (project number, client name in titles, one-line role in serif, stack in mono: Next.js, React, Supabase, n8n, Chatwoot, Mailcow - only what that project actually used), then the site inside a minimal browser frame showing its real domain in the address bar
- Hover a frame: it tilts up to 4 degrees toward the cursor (3D perspective), a muted screen-recording loop of the real site plays inside it, the cursor ring says "Abrir"
- Click: the frame expands to full screen in one continuous shot (shared-element transition) into the project's case study route. No white flash, no layout jump. Back button reverses the shot
- The QuitoWeb scene is special: the light over the frame shifts from day to night as you scroll through it, and the title reads "Tu WhatsApp vende mientras duermes"
- The Spa Cumbayá scene is special: instead of a browser frame, a phone frame plays the existing sample WhatsApp conversation in real time - incoming bubble, typing dots, reply - in `--signal` green tones, looping with a pause between runs. A small note: "Demo"
- Mobile: the reel becomes vertical; each project is a full-height card; posters instead of loops unless the visitor taps play

### Case study pages (`/proyectos/[slug]`)
- Open on the expanded frame from the reel, then scroll into:
  - Title card: client, year if known, role, stack
  - "El problema": two to four sentences
  - "Lo que hice": the work in short paragraphs, with screenshots full bleed
  - "El resultado": what changed for the client, only facts Guillermo provides, no invented metrics
  - A pull quote from the client if a testimonial exists
  - Link to the live site
  - "Siguiente proyecto" as a full-width cut to the next project's title card
- Leave clearly marked placeholders where Guillermo needs to write the copy; never invent results, numbers or quotes

### Scene 06 - Trayectoria
- Slate: "06 · Trayectoria"
- The existing work and education timeline, rolled as film credits: centered, role in small caps, organisation in titles, years in mono
  - QuitoWeb
  - Hostinger - technical support
  - WindshieldHUB LLC - sales and service
  - Hostal La Querencia - guest relations
  - USFQ - Finance and Business Administration
- The roll speed follows scroll speed; stopping scroll stops the roll
- A "Descargar CV" link sits at the end of the roll

### Scene 07 - "Lo que sé hacer"
- Slate: "07 · Oficio"
- The existing skills grouped in four columns, each column a "department" in the credits style:
  - Servidores: Linux, domains, DNS, SSL, business email (Mailcow)
  - Web: Next.js, React, Supabase / PostgreSQL
  - Automatización: WhatsApp assistants with AI, n8n, Chatwoot
  - Soporte: technical documentation, ticket triage, escalation
- Each line fades up with a 60 ms stagger; on hover a line underlines in `--dusk`
- No progress bars, no percentages, no logo walls

### Scene 08 - "Lo que dicen mis clientes"
- Slate: "08 · Clientes"
- One testimonial at a time, full screen, the quote in large italic serif, attribution beneath in small caps:
  - Alfredo Mora, CEO, AMG Legal
  - Silvia Guzmán, owner, Recorre Travel
- Use the existing quote text verbatim
- Scroll moves to the next quote with a hard cut; a small "1 / 2" counter in mono

### Scene 09 - Contacto: "Cuéntame qué necesitas"
- Slate: "09 · Contacto"
- Letterbox bars return. The portrait of Guillermo, side-lit, on the left; the form on the right
- The existing form: name, email, topic, message, with the same fields and handler as today. Labels always visible, not placeholder-only. Inline validation in both languages. Success state: the form fades and a subtitle reads a thank-you line in the current voice; error state keeps the visitor's text
- The email address stays obfuscated as it is today
- Links: LinkedIn (linkedin.com/in/guillermo-rogel-mora/), GitHub (github.com/guillermorogelm)

### Scene 10 - End credits (footer)
- The bars close almost shut, and a slow credit roll runs: "Un sitio de Guillermo Rogel", stack used to build this site, photo credits (existing), copyright, LinkedIn, GitHub, email
- Last frame: "Quito, Ecuador" and a back-to-top link that rewinds the whole film at high speed to the opening shot

---

## 5. Languages

- Spanish at `/` and `/es`, English at `/en`, `hreflang` tags both ways
- The ES/EN switch keeps the visitor in the same scene: copy swaps with a 200 ms crossfade, no reload, URL updates
- Every string in `content/es.json` and `content/en.json`, including alt text, form errors and terminal messages
- Dates, numbers and the counter formatted per locale

---

## 6. Reduced motion, mobile and no-JS

- `prefers-reduced-motion: reduce`: no pinning, no parallax, no grain, no letterbox animation, no auto-playing loops. Each scene becomes a still frame with a simple 200 ms opacity fade. The reel becomes a vertical list. The counter shows 50 directly. Everything stays readable and in order
- A small "Movimiento: on / off" toggle in the footer lets anyone switch to the still version, remembered in localStorage
- Mobile (under 768 px): thinner letterbox, no 3D tilt, no custom cursor, posters instead of loops, pinned scenes shortened, tap targets at least 44 px
- No JavaScript: the full page renders as a readable document, all links work, the form submits normally

---

## 7. Performance budget

This is a developer who promises fast websites, so the site is the proof:

- LCP under 2.0 s on a mid-range phone over 4G; CLS under 0.05; INP under 200 ms
- Lighthouse 95+ for Performance, Accessibility, Best Practices and SEO, on mobile
- Initial JavaScript under 120 KB gzipped; GSAP and scene code load after first paint
- Opening scene is pure HTML/CSS until the first scroll; the hero photo is the LCP element, preloaded, AVIF
- Screen-recording loops under 1.5 MB each, never loaded before their scene is within one screen of the viewport
- Fonts: at most three families, subset, preloaded

---

## 8. Accessibility

- Semantic landmarks: header, main, one h1 (the name), h2 per scene, footer
- Skip-to-content link kept as the first focusable element
- Full keyboard navigation through the reel (arrow keys move between projects when it has focus), the form and the domain tool
- Visible focus rings in `--dusk`
- Every image has meaningful alt text in both languages; decorative grain and bars are `aria-hidden`
- Subtitled text is real text in the DOM, readable by screen readers in order, not hidden and revealed only by animation
- Video loops have no audio and a pause control

---

## 9. SEO and sharing

- Title (ES): "Desarrollo web y servidores en Quito" with the name; English equivalent on `/en`
- Meta descriptions from the bio line
- Open Graph image: a graded still of the opening title over Cuenca, 1200×630, one per language
- JSON-LD `Person` (name, jobTitle, address Quito EC, sameAs LinkedIn and GitHub) and `Organization` for QuitoWeb
- `sitemap.xml` and `robots.txt` including case study routes in both languages

---

## 10. Assets needed (list them in the README, do not fake them)

- Dawn photo of Cuenca, Quito photo, portrait - high resolution, to be graded
- The existing personal photos from "De Cuenca a Quito"
- 8-12 s screen recordings of c16beauty.com, quitoweb.com, kronic-arquitectura.com, recorretravel.com
- Existing testimonial text, ticket samples and WhatsApp demo conversation
- Case study copy per project (placeholders until written)
- Where an asset is missing, use a clearly labeled neutral placeholder frame, not stock photography

---

## 11. Done means

- [ ] Every section of the current site exists in the new one, with its content verbatim in both languages
- [ ] The domain checker and contact form work exactly as before
- [ ] Each scene has an establishing shot, an action and a cut; none is just "fades in on enter"
- [ ] Scrolling back rewinds every scroll-driven scene without glitches
- [ ] The project frame expands into its case study and back with no flash or jump
- [ ] Reduced-motion and no-JS versions are complete and readable
- [ ] Performance and accessibility targets in sections 7 and 8 are met on mobile
- [ ] No invented metrics, quotes, clients or dates anywhere
- [ ] Smooth 60fps scroll on a mid-range laptop and phone
````
