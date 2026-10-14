---
name: cinematic-site-prompt
description: Writes a long, detailed build prompt (2,000-3,500 words) for a cinematic, scroll-driven website - a portfolio, personal site, studio or product page that plays like a short film - with art direction, a motion system, a scene-by-scene breakdown, languages, reduced motion, performance, accessibility, SEO, an assets list and a "done means" checklist. Use when asked for a prompt or spec to build or redesign a website, "a cinematic portfolio", "renew my site", "a prompt for a landing page that feels like a film", or when a short site prompt needs to become a full one. Pulls real content from the current site when a URL is given and never invents facts.
---

# Cinematic Site Prompt

Write the spec a builder could ship from without asking a single question.

The output is a build prompt, not a website. It is long on purpose: every
scene, every state and every budget is written down, so two builders given
the same prompt would ship the same site. Length comes from coverage, not
from adjectives.

Read `examples.md` once per session before writing. `template.md` is the
skeleton to fill. `reference.md` holds the scene patterns, motion rules,
stacks, budgets and the final checklist.

## Rules

- **Real content only.** Every name, client, quote, date, number and line of
  copy comes from the person or their current site. Quote existing copy
  verbatim and say so. Where something is missing, write a marked
  placeholder (`[PLACEHOLDER: one-line case study result from the client]`).
  Never invent metrics, testimonials, clients, awards or years.
- **Keep what works.** Every section and every working feature of the
  current site (forms, tools, language switch, CV download) appears in the
  new spec, or the spec says in one line why it is dropped.
- **Every scene has three beats**: an establishing shot, an action, a cut.
  "Fades in when it enters the viewport" is never a scene.
- **The whole point line.** The motion section opens with "this is the
  whole point - it must feel like X, not Y". Default: "a title sequence,
  not a template with fade-ins".
- **Fast is part of cinematic.** The spec always carries a performance
  budget, a reduced-motion version and a no-JS reading path. A slow
  cinematic site is a broken one.
- **No adjective without a mechanism.** "Stunning", "immersive", "modern",
  "sleek", "premium" are banned unless the same line says how (a duration,
  an easing, a size, a color, a behavior).
- Plain hyphen " - " as the dash. No em dashes.

## Step 1. Gather the facts

- **A URL is given**: fetch the current site. Extract name, role, location,
  the bio and taglines verbatim, the page title, the section order with
  their headings verbatim, every project or client with its domain, every
  testimonial with attribution, work history, skills, contact methods,
  social links, languages, and every interactive feature (forms, tools,
  demos, downloads). Note the current visual style in two lines.
  If the site has more pages, fetch the ones the navigation links to.
- **No URL**: ask, in one batch, for the minimum: who they are in one line,
  three to six projects with one line each, contact method, language(s),
  and any photos or recordings they already have. Do not start writing
  until you have at least the name, the role and the projects.
- Write the fact list down (in your head or a scratch file) before writing
  the prompt. The prompt draws only from it.

## Step 2. Find the film

- **Logline**: one sentence a trailer would say. The person, the arc, the
  promise. Example: "From Cuenca to Quito: someone who answers fifty
  tickets a day and builds websites that load fast."
- **The feel contrast**: what it must feel like, and what it must not
  ("a title sequence, not a template with fade-ins"; "a gallery opening,
  not a Behance page"; "a product reveal, not a SaaS landing page").
- **The signature moment**: the one interaction someone records and shares.
  Usually the project reel or the hero. Name it.
- **Scene list**: map every existing section to a scene from the scene
  patterns in `reference.md`, in story order, opening titles first, end
  credits last. Eight to twelve scenes for a one-page site.

## Step 3. Choose the stack

Default to what the person already builds with (look at their skills and
projects). Otherwise use the defaults in `reference.md`. Name the motion
libraries and forbid the rest, so the builder does not add three.

## Step 4. Write the prompt

Fill `template.md` section by section:

0. The idea in one paragraph, plus the "whole point" line
1. Stack and architecture, with a folder sketch
2. Art direction: color tokens with hex values, type roles with font
   suggestions and fallbacks, photography grade, texture, cursor
3. The motion system: easings, durations, scrub rules, pin limits,
   reading order, rewind, pause off screen
4. The film, scene by scene: slate name, layout, beats, copy (verbatim),
   mobile behavior. Sub-pages (case studies) get their own block
5. Languages
6. Reduced motion, mobile and no-JS
7. Performance budget with numbers
8. Accessibility
9. SEO and sharing
10. Assets needed, listed, with "do not fake them"
11. Done means: a checklist a reviewer can tick

## Step 5. Check it

Run the checklist at the end of `reference.md`. Then read the prompt as the
builder: is there any scene where you would have to guess? Fix it.

## Output

1. Save the prompt as `<site-or-name>-cinematic-prompt.md` in the current
   working directory (or the scratchpad if the working directory is a repo
   that should not hold it), and give the path.
2. In chat, at most five lines: the logline, the feel contrast, the stack,
   the signature moment, and the assets or facts the person still has to
   provide.
3. Offer to build it. Do not start building unless asked.

If the user hands you an existing site prompt to expand, keep every
decision it already makes, fill the missing sections from the template, and
list what you added.
