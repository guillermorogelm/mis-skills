# Verify

Run this on every candidate before it becomes a finding.

This is the phase that makes the report worth reading. Without it you
have a list of things that look wrong, which is what everyone already
has, and which nobody acts on.

## The bar

A finding is real when you can name the trigger, trace the path, and
state the wrong result, pointing at the lines that produce it.

Everything else is a guess. Guesses get deleted, not softened.

## The failure scenario

Write this out for every candidate. If any line stays empty, the
candidate does not survive.

```
FINDING:  one line, plain
FILE:     path/to/file.ts:120
TRIGGER:  the concrete input or state, with literal values
PATH:     what the code does with it, step by step, value by value
WRONG:    what comes out, or what crashes, or what renders
EXPECT:   what should have come out
PROOF:    the check that shows it
```

`TRIGGER` is the line that does the work. "A malicious user" is not a
trigger. "An empty array" is not a trigger unless you can say which call
passes an empty array. `POST /api/notes/42 with a session for user 7,
where note 42 belongs to user 9` is a trigger.

## Four questions

Answer all four. Any "no" ends the candidate.

**1. Can you name the input?**
Literal values. A request, a payload, a row, a click, a viewport width, a
clock time. If the best you can do is "bad input", you do not understand
the bug yet.

**2. Can you trace the path?**
Read the code, not the function name. Follow the value from the trigger
to the wrong result and say what it holds at each step. A trace that
skips a step is a trace that hides the guard you missed.

**3. Is it reachable?**
Follow the callers up until you hit an entry point: a route, a CLI
command, an event handler, an exported API, a test. If nothing reaches
it, this is not a correctness finding. It is either dead code, which is
pass 6, or it is nothing.

**4. Is it already handled?**
Look upstream before you report. A validator at the edge, a type the
compiler enforces, a framework default, a guard in the caller, a wrapper
that catches. Read them. Do not assume they exist, and do not assume
they do not.

## Three kinds of proof

Pick the strongest one available for that candidate.

**A. Executable.** Write the test or the script that reproduces the
scenario. Run it against the current code and watch it fail. Keep it.
This is the best proof there is: the failing test becomes the fix's proof
in Phase 4, and it stays behind as a regression guard.

**B. Observable.** Run the thing and look at it. Rendering, focus order,
contrast, a spinner that never resolves, a log line that never appears.
Record the exact steps you took and what you saw. "Opened /settings at
360px wide, the page scrolls sideways by 40px" is proof. "Probably
overflows on mobile" is not.

**C. Structural.** For findings that are about something missing: dead
code, a missing index, a missing ownership check. Proof is an exhaustive
search plus a negative result, and you state the searches you ran so
someone else can repeat them. This is the weakest kind. Use it only when
A and B do not apply.

## Bias to discard

Verification has a budget. If reading around fifty lines and running one
check leaves you unsure, the candidate is out. Either delete it or turn
it into one question for the human in the report.

Ambiguity is not a finding. Reporting it as one shifts your uncertainty
onto the reader and calls it work.

Expect to delete most candidates. That is the phase working, not the
sweep failing.

## What a guess looks like

Delete on sight:

- Hedged language. Could, may, might, potentially, in some cases.
- A finding that restates the code. "This function does not validate its
  argument" with no caller that passes a bad one.
- A trigger that names an actor instead of an input. "A malicious user
  sends a crafted request." Which request?
- Anything taken from a general checklist rather than from this code.
- A severity assigned before a trigger was found. Severity comes from
  impact, and impact needs a trigger.
- Two hedges stacked. "This may cause issues under load."

**The rewrite test.** Say the finding as "if X then Y". If X cannot be
filled with literal values, discard it.

## Worked example: survives

```
FINDING:  Notes can be read by any signed-in user, not only the owner.
FILE:     app/api/notes/[id]/route.ts:14
TRIGGER:  GET /api/notes/42 with a valid session cookie for user 7.
          Row 42 in notes has user_id 9.
PATH:     requireSession() at line 9 returns user 7 and passes.
          Line 14 reads db.notes.findFirst({ where: { id: params.id } }).
          No user_id in the where clause. The row for user 9 comes back.
          Line 21 returns it as JSON with no further check.
WRONG:    200 with another user's note body.
EXPECT:   404, and no row read.
PROOF:    Executable. Added a test that seeds two users and two notes,
          signs in as user 7, requests note 42, and asserts 404.
          Fails against current code with a 200.
```

That one is real. The trigger is a request anyone can send, the path
names the missing clause, and the proof runs.

## Worked example: discarded

```
FINDING:  formatPrice can produce NaN.
FILE:     lib/format.ts:8
TRIGGER:  price is undefined.
PATH:     undefined * 100 gives NaN, which renders as "NaN".
WRONG:    "NaN" on the page.
EXPECT:   an empty state.
```

Then question three. Who calls `formatPrice`? Three call sites, all
inside `ProductCard`, which takes a `Product` from a Zod schema where
`price` is required and the parse happens at the route boundary. Nothing
casts. Nothing spreads an untyped object in.

No caller can pass `undefined`. Delete the candidate. Do not keep it as
"defensive programming would be nice here". That is taste, and it belongs
nowhere in the report.

## When it survives

Move it to Phase 3 with the scenario attached. Carry that scenario all
the way through: it decides the severity in Phase 3, it tells you the
smallest correct change in Phase 4, and it is the proof line in the
report.

Anything new that turns up during the re-sweep comes back through this
file. No exceptions, including for findings you created yourself.
