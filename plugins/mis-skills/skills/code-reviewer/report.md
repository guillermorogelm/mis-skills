# Report

Write this once, at the end.

## Rules

- Fixed and proven goes first. That is the result of the sweep.
- Every fixed item carries its proof. A fix with no proof line is not
  finished, it is a claim.
- Every left item carries the decision that blocks it, and one question
  that would unblock it.
- Counts are not the outcome. "Found 23 issues" is not a result.
- No praise section. Nobody asked what is good.
- No further recommendations. If it was worth reporting it went through
  verification, and if it did not go through verification it does not
  appear here.
- No severity inflation. If everything is critical, nothing is.
- Plain sentences. `file:line` for every item.

## Format

```
# Sweep report

Scope:      what was swept
Dimensions: which passes ran, and which were skipped and why
Baseline:   the checks run before any edit, and what already failed

## Fixed (n)

### 1. One line [Broken]
File:   path:line
Was:    the failure, with its trigger
Change: what you changed, one sentence
Proof:  the check that failed before and passes now

## Left for you (n)

### 1. One line [Broken]
File:     path:line
Failure:  the trigger and the wrong result
Blocked:  the decision this needs
Question: the one thing to answer

## Discarded (n)

How many candidates failed verification, and any that looked serious
and were not, one line each with the reason.

## Checks

Baseline versus now.

## Next

One line. The single most useful thing to do next.
```

## Worked example

```
# Sweep report

Scope:      apps/web, full repo pass. 214 files.
Dimensions: all seven ran.
Baseline:   pnpm typecheck clean. pnpm lint clean. pnpm test 41 passed,
            1 failed. The failure, notes.spec.ts "restores draft after
            reload", was already red at HEAD. Left alone.

## Fixed (3)

### 1. Any signed-in user could read any note [Broken]
File:   app/api/notes/[id]/route.ts:14
Was:    GET /api/notes/42 with a session for user 7 returned note 42
        even though it belongs to user 9. The where clause matched on id
        alone.
Change: Added userId to the where clause. Three lines.
Proof:  New test seeds two users and two notes, signs in as user 7, and
        asserts 404 on note 42. Fails before the change with 200, passes
        after. Full suite 42 passed, same 1 pre-existing failure.

### 2. Export crashed on an empty selection [Broken]
File:   lib/export.ts:31
Was:    Selecting no rows and pressing Export called reduce with no
        initial value on an empty array, which throws. The button is
        enabled with nothing selected, so a click reaches it.
Change: Passed an initial value of 0.
Proof:  Test added for the empty array case. Reproduced the throw
        first. Checks clean.

### 3. Dialog close discarded keyboard focus [Degraded]
File:   components/Dialog.tsx:52
Was:    Closing the settings dialog with Escape returned focus to body,
        so the next Tab started at the top of the page. Anyone using a
        keyboard lost their place.
Change: Stored the trigger element on open and focused it on close.
Proof:  Observable. Opened /settings, pressed Escape, and the Settings
        button holds focus. Repeated with VoiceOver on, which announces
        the button.

## Left for you (2)

### 1. Prices stored as floats [Broken]
File:     lib/pricing.ts:12, prisma/schema.prisma:44
Failure:  A cart of 3 items at 19.99 totals 59.96999999999999, which
          renders as 59.97 but is stored unrounded. Two of these in one
          order drift by a cent against the payment provider.
Blocked:  The fix changes the database column type and needs a
          migration on live data.
Question: Move to integer cents now, or after the billing work lands?

### 2. Two date formats on the dashboard [Degraded]
File:     components/ActivityRow.tsx:18, components/Header.tsx:9
Failure:  One shows 5 Jan 2026, the other 01/05/2026, on the same
          screen. The second is ambiguous outside the US.
Blocked:  No written rule and no majority. 6 files use each.
Question: Which format is the house style?

## Discarded (14)

14 candidates failed verification. Two worth naming:

- formatPrice returning NaN. Every caller receives a parsed Zod object
  where price is required. Not reachable.
- lib/legacy/csv.ts looked orphaned. It is imported by name as a string
  in the job registry at workers/index.ts:22. Alive.

## Checks

Before: typecheck clean, lint clean, tests 41 passed 1 failed.
After:  typecheck clean, lint clean, tests 44 passed 1 failed.
The failure is the same pre-existing one. Three tests added.

## Next

Answer the cents question. The pricing drift is the only item here that
costs money.
```

## The last line

End with one line naming the single most useful next step, and nothing
after it. Not a summary. Not an offer. One line, then stop.
