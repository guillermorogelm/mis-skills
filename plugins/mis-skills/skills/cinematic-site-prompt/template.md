# Template

Copy this skeleton and fill every bracket. Delete a section only if it
truly does not apply, and say so in one line where it was.

````
Build "[Site name]" - a cinematic [redesign of domain.com / new site]: a [languages] [type of site] for [who, one line], that plays like a short film you [verb], [verb], [verb] and [verb]. [It replaces the current site in place, keeps every piece of real content and every working feature,] and must still [load fast / the promise the person makes].

---

## 0. The idea in one paragraph

[What the current site does well and why it reads like a document. The film version: each section a scene with an establishing shot, an action and a cut. The visitor is the camera: scrolling moves forward, stopping holds the frame, scrolling back rewinds. What the visitor knows and can do by the end credits.]

The whole point - it must feel like [X], not [Y]. If a section could be described as "the text fades up when it enters the viewport", it is not done.

---

## 1. Stack and architecture

- [Framework, language, rendering]
- Styling: [system] with design tokens as CSS variables (section 2)
- Motion: [libraries]. No other animation library ([name the usual suspects])
- Motion code client-only, split per scene, lazy-loaded after first paint. Fully readable with JavaScript off
- Images: [pipeline], AVIF with WebP fallback, explicit sizes, blur placeholders
- Video: short MP4 + WebM loops, muted, playsinline, posters, loaded only near their scene
- Fonts self-hosted, subset to [character sets]
- i18n: [routes], one content file per language, no copy hardcoded
- Hosting: [target]. [Form handler / API routes kept from today]
- Sub-pages: [routes]

Folder sketch:

```
[tree]
```

---

## 2. Art direction

### Color grade
- `--ink`: [hex] [role]
- `--paper`: [hex] [role]
- `--ash`: [hex] [role]
- `--accent`: [hex] [name] - used only for [list]
- [`--scene`: hex, one scene only]
- All text meets WCAG AA on its background

### Photography
- [One grade for every photo]
- [Which photos are hero plates]
- [Portrait: where, how often]

### Typography
- Titles: [font, fallback, how used]
- Body: [font, size desktop/mobile, line length]
- Data: [font] with tabular numerals
- Subtitles: [style, position]

### Film texture
- [Grain spec]
- [Letterbox: where]
- [Slates: look]
- [Cut rules]

### Cursor
- [Desktop spec, words shown, mobile off]

---

## 3. The motion system

- [Easings]
- [Durations]
- [Scrub and rewind rule]
- [Pin limit]
- [Reading order rule]
- [Off-screen rule]
- [Smooth scroll rule]
- prefers-reduced-motion: see section 6

---

## 4. The film, scene by scene

Use all existing copy verbatim. Where this prompt quotes copy, it is the current copy. Where it says "existing copy", pull it from the current site, do not rewrite it.

### Scene 00 - [Opening titles]
- Layout: [...]
- Beat 1: [...]
- Beat 2: [...]
- Beat 3: [...]
- First scroll: [...]
- Header (after the opening): [items, behavior, skip link]

### Scene 01 - [Name]
- Slate: "01 · [Name]"
- Establishing shot: [...]
- Action: [...]
- Cut: [...]
- Mobile: [...]

[... one block per scene ...]

### [Sub-pages, e.g. case studies]
- Opening: [continuous shot from the reel]
- Sections: [list with headings]
- [PLACEHOLDER rules: never invent results, numbers or quotes]
- Next: [transition to the next one]

### Scene [n] - Contact
- [Layout, the real form fields, states, contact details as today]

### Scene [n+1] - End credits
- [Credits, links, back-to-top rewind]

---

## 5. Languages
- [Routes, hreflang, switch behavior, content files, formatting]

## 6. Reduced motion, mobile and no-JS
- Reduced motion: [...]
- Toggle: [...]
- Mobile (under [px]): [...]
- No JavaScript: [...]

## 7. Performance budget
[Why it matters for this person, one line]
- [LCP, CLS, INP, Lighthouse, initial JS, video, fonts, LCP element]

## 8. Accessibility
- [Landmarks, headings, skip link, keyboard paths, focus, alt text, aria-hidden layers, DOM text, video controls]

## 9. SEO and sharing
- [Title and description from real copy, OG images, JSON-LD types, sitemap, robots]

## 10. Assets needed (list them in the README, do not fake them)
- [Every photo, recording, text and quote the build needs]
- Where an asset is missing, use a clearly labeled neutral placeholder frame, not stock photography

## 11. Done means
- [ ] Every section of the current site exists in the new one, with its content verbatim [in both languages]
- [ ] [Every working feature] works exactly as before
- [ ] Each scene has an establishing shot, an action and a cut
- [ ] Scrolling back rewinds every scroll-driven scene cleanly
- [ ] [Signature moment works with no flash or jump]
- [ ] Reduced-motion and no-JS versions are complete and readable
- [ ] Performance and accessibility targets met on mobile
- [ ] No invented metrics, quotes, clients or dates anywhere
- [ ] Smooth 60fps scroll on a mid-range laptop and phone
````
