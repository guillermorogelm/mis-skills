# Dimensions

Seven passes. One dimension per pass.

A single pass looking for everything finds nothing. It drifts, it reads a
file, it notices something interesting, and it never covers the ground.
A pass with one question in mind covers the ground.

## How to run one pass

1. Say the dimension out loud before you start. "Pass 3 of 7: security."
2. Search for that dimension's patterns. Grep first to find candidates,
   then read the code around each hit. A grep hit is not a finding.
3. Record each candidate as `file:line` plus one sentence. Nothing else.
4. Fix nothing. Report nothing. Move to the next dimension.

Run them in this order. Correctness first, because if you run out of time
the later dimensions are the cheaper ones to defer.

1. Correctness
2. Error handling
3. Security
4. Accessibility
5. Performance
6. Dead code
7. Consistency with the project's own conventions

On a large repo, scope each pass before you start it: the directories the
scope covers, entry points first. A finished loop over three dimensions
beats an abandoned pass over seven.

Every dimension below has a **Discard** list. Read it before you record a
candidate, not after. It is the difference between a report someone acts
on and a report someone closes.

---

## 1. Correctness

The code runs and gives the wrong answer.

**Where to look.** Branching logic, index and boundary arithmetic, async
code, comparisons, anything handling money, dates, or user counts. State
updates. Anything with two similar-looking branches.

**Patterns**

1. **Off by one.** `<=` where `<` belongs. `length` used as an index.
   Slices that drop the last element or read one past the end. Pagination
   arithmetic that repeats or skips a row at the page boundary.
2. **Empty and single-item cases.** `arr[0]` with no length check.
   `reduce` with no initial value, which throws on an empty array.
   `Math.max(...arr)` on an empty array, which returns `-Infinity` and
   poisons everything downstream. Averages dividing by zero.
3. **Falsy versus missing.** `if (x)` where `0`, `""`, or `false` are
   valid values. A count of zero treated as "no data". Optional chaining
   that returns `undefined` into arithmetic, producing `NaN` that then
   renders as text.
4. **Equality.** `===` on objects or arrays where value equality was
   meant. `NaN !== NaN`. A `==` against `null` that catches `undefined`
   on purpose, next to one that does it by accident.
5. **Async.** A missing `await`: the promise is truthy, so the check
   passes and the rejection goes unhandled. `forEach` with an async
   callback, which waits for nothing. `Promise.all` where one rejection
   discards the other results and the caller needed them.
6. **Stale state and races.** Two readers writing back the same record.
   State computed from a stale closure instead of the updater form. An
   effect that fetches with no cancel flag, so a slow first response
   lands after a fast second one and overwrites it. Debounced input where
   the last keystroke loses to an earlier request.
7. **Shared mutation.** A default argument object mutated across calls. A
   module-level array pushed to per request, growing forever. `.sort()`
   and `.reverse()` mutating an array the caller still reads.
8. **Numbers and money.** Floats holding currency. `parseInt` with no
   radix. Rounding applied twice. Percentages computed on an already
   rounded value.
9. **Dates.** `new Date("2026-01-05")` parses as UTC while
   `new Date("2026/01/05")` parses as local, so the day shifts. Month
   index off by one. Duration arithmetic across a DST boundary.
   Timestamps compared in different units, seconds against milliseconds.
10. **Copy-paste divergence.** Two branches that should be identical and
    differ by one variable name. The same condition tested twice, so the
    second branch is dead. A loop body using the outer variable instead
    of the loop variable.
11. **A fallback that looks like data.** A catch that returns `[]` or
    `{}`, so the caller renders "no results" for what was a failed
    request.

**Discard**

- Guarded paths. A private function whose only caller validates the input
  first. Find the caller. If the guard is there, discard.
- Type-system guarantees. If TypeScript makes the value non-null and
  there is no `any`, no `as`, and no external boundary, there is no
  finding. Boundaries are not guaranteed: `JSON.parse`, `fetch` results,
  `process.env`, database rows, form data, and anything cast.
- Style. `for` versus `map`. Early return versus nesting. Not findings.
- Missing validation at a point where the framework already validates at
  the edge. Check the edge first.
- Anything you would report as "could be a problem if". That sentence is
  the sound of an unverified guess.

---

## 2. Error handling

The code fails and nobody finds out, or the user is left staring at a
spinner.

**Where to look.** Every `catch`, every `.then` with no `.catch`, every
network call, every file and database access, every parser, every
boundary between your code and something else.

**Patterns**

1. **Empty catch.** `catch {}` or a catch that only logs and then
   continues as though the call succeeded, so the next line reads
   `undefined`.
2. **Lost cause.** `throw new Error("failed")` inside a catch that
   discards the original error. The stack trace stops at the wrong place
   and nobody can debug it.
3. **Exceptions as normal flow.** A 404 is not exceptional. An empty
   result is not exceptional. Throwing for these buries the real errors
   in noise.
4. **Unhandled rejection.** An async function called with no `await` and
   no `.catch`. An async event handler, which nothing awaits by
   definition.
5. **Retry with no cap and no backoff.** A loop that hammers a service
   that is already failing.
6. **No timeout.** `fetch` with no abort signal. A database call with no
   statement timeout. One hung dependency becomes one hung request,
   then a hung pool, then a hung service.
7. **Resource leaked on the failure path.** A file handle, a transaction,
   a lock, a subscription opened inside `try` and released only after the
   success path.
8. **The user sees nothing.** A failed request that leaves a spinner
   forever. An error state that renders as an empty list, which reads as
   "nothing here" rather than "this broke".
9. **Internals leaked outward.** Stack traces, SQL, or absolute file
   paths rendered to the user or returned in an API response.
10. **Partial writes.** Two writes with no transaction, where the first
    can succeed and the second can fail, leaving a half-written record.
11. **Exit in a library path.** `process.exit` or an uncatchable throw
    somewhere that should have returned an error to its caller.

**Discard**

- A deliberately empty catch with a comment saying why, where the failure
  genuinely does not matter. A best-effort analytics ping is allowed to
  fail. Read the comment before you record the candidate.
- A missing local handler where a framework error boundary, a global
  handler, or an error page already covers it. Find that handler first.
- Logging you find thin. Not a finding unless the failure is invisible.
- Error copy you would word differently. That is taste.

---

## 3. Security

Report these. Fix only the unambiguous ones.

Anything touching auth, permissions, secrets, or money goes to needs a
human even when the fix looks obvious, unless the fix is a one-line
addition of a check that clearly belongs there.

**Patterns**

1. **Secrets in the repo.** API keys, tokens, private keys, a committed
   `.env`. Also secrets leaking client-side: a server-only key referenced
   from client code, which ends up in the bundle a stranger can read. In
   Next.js, check for server keys used inside client components, and for
   anything server-only inlined at build time.
2. **Injection.** SQL built by string concatenation. A shell command
   built from user input. HTML built from user input. `eval`,
   `new Function`, or `dangerouslySetInnerHTML` fed anything that is not
   a literal.
3. **Authorization missing under authentication.** The most common real
   finding on the list. The handler checks who you are and then reads a
   record by an id from the request with no check that the record belongs
   to you. Look at every handler that takes an id and does a lookup.
4. **Guessable ids.** Sequential integer ids used for lookups with no
   ownership filter.
5. **Open redirect.** Redirecting to a URL taken from the request with no
   allowlist.
6. **Path traversal.** User input concatenated into a file path with no
   normalise and no prefix check.
7. **Signatures not checked.** A webhook handler that trusts the body. A
   token decoded rather than verified, `decode` where `verify` belongs.
8. **Cookies and CORS.** Cookies without `httpOnly`, `secure`,
   `sameSite`. `Access-Control-Allow-Origin: *` on an endpoint that
   returns user data.
9. **No rate limit** on login, password reset, invite, or anything that
   sends mail or costs money per call.
10. **Timing-unsafe comparison** of a token or a signature with `===`.
11. **Known-vulnerable dependencies.** Run the project's own audit
    command if it has one. Report the result. Do not bump major versions
    on your own.
12. **Sensitive data in logs.** Tokens, passwords, full request bodies,
    personal data.

**Discard**

- Missing CSRF protection where the framework enables it by default and
  nothing in the config disables it. Read the config.
- Hardcoded strings that are not secrets. Publishable keys, public keys,
  fixture values in tests.
- `dangerouslySetInnerHTML` fed a literal or an already sanitised source.
  Trace the source to where it comes from.
- Any finding whose trigger is "an attacker could" with no reachable
  path. Name the request, or discard it.

---

## 4. Accessibility

Some people cannot use it.

**Where to look.** Anything interactive. Forms, dialogs, menus, custom
controls, images, animation.

**Patterns**

1. **Click handler on a `div` or a `span`.** No keyboard access, no
   focus, no role, no announcement.
2. **Controls with no accessible name.** Icon-only buttons with no
   `aria-label` and no visually hidden text. A link whose only content is
   an image with no alt.
3. **Images.** Alt missing, so a screen reader reads the filename. Alt
   that names the file rather than describing the picture. Decorative
   images given descriptive alt when they should carry `alt=""`.
4. **Forms.** An input with no associated label. A placeholder used as
   the label, which disappears the moment someone types. Error text not
   tied to its field with `aria-describedby`.
5. **Focus.** `outline: none` with nothing put back. A dialog that opens
   without moving focus into it, or closes without returning focus. Tab
   escaping to the page behind an open dialog.
6. **Heading order.** `h1` straight to `h3`. Several `h1` on one page.
   Headings chosen for their size.
7. **Contrast.** Body text under 4.5:1, large text and UI boundaries
   under 3:1. Measure against the background that actually renders, not
   the one the token names.
8. **Motion.** Animation with no `prefers-reduced-motion` branch. An
   auto-playing carousel with no pause. Scroll-driven content that
   becomes unreachable when animation is off.
9. **State not announced.** Custom toggles, tabs, and accordions with no
   `aria-expanded`, `aria-selected`, or `aria-current`. Content that
   changes after an action with no live region, so it changes in silence.
10. **Touch and viewport.** Tap targets under 44px. Sideways scroll at
    360px wide.
11. **Page level.** No `lang` on `html`. The same `title` on every page.

**Discard**

- ARIA added where a native element already carries the meaning.
  `role="button"` on a `<button>` is noise.
- Contrast on disabled controls, which are exempt, and on purely
  decorative graphics.
- Alt text on an image inside a link that already has text, where the
  image adds nothing.
- A missing landmark in a component that renders inside a page-level
  landmark. Look at the composed page, not the one file.
- Anything where you are guessing at the rendered result. Open it and
  look, or discard it.

---

## 5. Performance

Measure it or discard it.

**Patterns**

1. **N+1.** A database call inside a loop over rows. The same shape in
   network calls: one request per item in a list.
2. **Work repeated per render.** Sorting or filtering a large array in a
   component body with no memo. Both halves matter: large array and
   frequent render. One without the other is not a finding.
3. **Missing index** on a column used in a where, a join, or an order by,
   on a table that grows.
4. **Unbounded reads.** A query with no limit on a growing table. Loading
   a whole collection to count it, or to find one row.
5. **Serial awaits that are independent.** Three fetches in a row that do
   not depend on each other.
6. **Images.** No width and height, so the layout jumps. Full-resolution
   originals served into a thumbnail. No lazy loading below the fold.
7. **Bundle weight.** A whole date library imported for one format call.
   A whole icon set for three icons. A heavy dependency pulled into a
   client component when it was only needed on the server.
8. **Main thread blocked.** A synchronous file read on a request path.
   `JSON.parse` on megabytes. A long loop inside an event handler.
9. **Caching.** An expensive call with an unchanging result recomputed
   per request. Or a cache with no invalidation, which is a correctness
   finding, not a performance one, and belongs in pass 1.
10. **Leaks.** Listeners added and never removed. Intervals never
    cleared. A module-level map used as a cache with no bound.

**Discard**

- Micro-optimisation with no measurement. Loop style. String concat
  versus template literal. Discard on sight.
- "This is O(n squared)" where n is bounded and small. Find the real
  size. Ten items is not a problem.
- Memoisation proposed everywhere. `useMemo` around a cheap computation
  costs more than it saves.
- Anything you cannot state as: this input size, this frequency, this
  measured cost. If there is no number, there is no finding.

---

## 6. Dead code

Code that runs nowhere, and code that cannot run.

**Patterns**

1. **Exports nobody imports.**
2. **Files nobody imports.** Whole components, routes, or utilities
   orphaned by a rewrite that nobody finished deleting.
3. **Unreachable branches.** Code after a return or a throw. A condition
   that cannot be false. A feature flag that has been on for a year, and
   the off branch beneath it.
4. **Commented-out blocks.** Git holds the old version. The file does
   not need to.
5. **Two implementations of the same thing** where only one is wired up.
6. **Dependencies in the manifest that nothing imports.** Scripts
   pointing at files that were deleted.
7. **Orphans in config.** Env vars nothing reads. CSS classes nothing
   uses. Translation keys nothing looks up.
8. **Stale TODOs** describing work that is already done, which mislead
   the next reader.

**Proving it.** Dead code is proven by absence, and absence is the
hardest thing to prove. Before recording a candidate, search for the
symbol three ways: as an identifier, as a string literal, which catches
dynamic imports and registries, and in any config that picks files up by
glob. Then say which searches you ran.

**Discard**

- The public surface of a published package. An unused export may be the
  product.
- Files a framework picks up by path rather than by import. In Next.js
  that includes `page.tsx`, `layout.tsx`, `route.ts`, `middleware.ts`,
  and the metadata files. Also test setup, migrations, and seeds.
- Anything referenced only from documentation, examples, or another repo.
  If you cannot see every caller, you cannot prove it is dead. Say that
  instead of deleting.
- New code behind a flag that has not launched. Check `git log` on the
  file before you call it dead.

---

## 7. Consistency with the project's own conventions

Not your conventions. The project's.

**Derive the rule before you report a break.** A convention is what the
project writes down, and where nothing is written, what most comparable
files do. In order: `AGENTS.md` and `CLAUDE.md`, `CONTRIBUTING.md`, the
linter and formatter config, tsconfig, then the majority of similar
files, counted rather than felt. If there is no written rule and no
majority, there is no finding.

**Patterns**

1. One file fetching data differently from every other, for example a
   raw call where the rest of the codebase goes through a client wrapper
   that adds auth headers and error shaping.
2. Error shape drift. Most handlers return a typed error object and one
   throws, so the caller's handling misses it.
3. Two ways of doing the same thing living side by side after a partial
   migration. Report the drift and say which side is the majority.
   Finishing the migration is a human decision, not a fix in this pass.
4. Naming or placement that breaks a real rule, for example a route file
   in the wrong directory in a file-routed framework. That one is a
   correctness finding as well.
5. Imports that bypass a configured alias, or reach into a module's
   internals instead of its entry point.
6. A rule the repo states in its own instruction file, broken in code.
   Cite the file and the line. That is the strongest finding in this
   dimension.
7. Types loosened locally with `any`, `as unknown as`, `@ts-ignore`, or
   an inline lint disable, with no comment saying why, in a repo that is
   strict everywhere else.
8. Surface drift. Two date formats on one screen. Two spellings of the
   same label. Two button components with the same job.

**Discard**

- Your preference. If the project has no rule and no majority, drop it.
- Old files that predate a convention and that nobody is touching. Note
  the drift once in the report. Do not fix them one by one in this pass.
- Anything a formatter owns. Run the formatter. Do not hand-edit
  whitespace.
- A deliberate exception with a comment explaining it. Read the comment.
