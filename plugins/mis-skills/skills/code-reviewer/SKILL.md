---
name: code-reviewer
description: Audits a codebase along seven named dimensions, proves every finding against a concrete failing input before reporting it, then fixes the survivors one at a time with a verification step after each. Use when asked to audit this codebase, find and fix what is broken, review before shipping, clean this up before release, or say what is wrong with this project.
---

# Code Reviewer

An audit loop, not an audit.

A list of forty findings changes nothing. Six proven bugs removed changes
the code. Produce the second thing.

## The rule that outranks everything else

**Fix one finding. Prove it. Then start the next.**

Never batch. Never open a second file while you are in there. Never make
three edits and run the checks once at the end. If two fixes are in
flight you have lost the thread: keep the first, revert the second, redo
it in order.

The loop is linear and you drive it yourself, phase by phase. Do not skip
a phase. Do not run two phases at once.

## Phase 0. Ground yourself

**Entry:** someone asked for an audit.

1. Agree the scope. Whole repo, one directory, or the current diff. If it
   was not stated, ask, then proceed with the answer.
2. Find how this project checks itself. Read `package.json` scripts, the
   `Makefile`, the CI config, the README. Write down the build, test,
   typecheck, and lint commands.
3. Read the project's own rules: `AGENTS.md`, `CLAUDE.md`,
   `CONTRIBUTING.md`, the linter and formatter config, tsconfig
   strictness. These define the conventions dimension. Yours do not.
4. Run the checks now, before touching anything. Record the baseline.
   A test that was red before you arrived is not your bug and not your
   fix. Say so in the report and leave it.
5. Check `git status`. If the tree is dirty, say so and ask before
   editing. You cannot prove a fix inside someone else's half-finished
   work.

**Exit:** you can name the scope, the check commands, and the baseline
failures. If there is no way to run anything, say that now, out loud:
every fix in this pass will be unproven and most of them should not be
made. Do not slide past this quietly.

## Phase 1. Sweep

**Entry:** Phase 0 exit met.

One pass per dimension, one dimension at a time. A single pass looking
for everything finds nothing. The seven dimensions, their patterns, and
their false positives are in [dimensions.md](dimensions.md). Read it
before the first pass.

For each pass: name the dimension, search for its specific patterns, read
the hits, record candidates as `file:line` plus one sentence.

Fix nothing during the sweep. Report nothing during the sweep. What you
have is a candidate list, and candidates are guesses until Phase 2.

**Exit:** every in-scope dimension has had its own pass, and each pass
ended with either candidates or the words "nothing found".

## Phase 2. Verify

**Entry:** a candidate list exists.

This phase is what makes the whole thing trustworthy. Follow
[verify.md](verify.md).

For every candidate, answer one question: can you write the concrete
input, state, or sequence that makes this code do the wrong thing? Write
it down with literal values.

If you cannot, it is a guess. Delete it. Do not soften it into "might be
an issue" and keep it on the list. Delete it.

Expect to delete most of them. A sweep that keeps everything verified
nothing.

**Exit:** every surviving finding has a written failure scenario:
concrete trigger, the path through the code, the wrong result. Every
other candidate is gone.

## Phase 3. Rank

**Entry:** verified findings only.

Rank by real impact, never by how easy the finding is to describe.

- **Broken.** Wrong output, crash, data loss, security hole, anything a
  user hits today.
- **Degraded.** Works, but wrong for some inputs or some people.
  Accessibility, missing error handling, measured performance problems.
- **Rot.** No user impact today. Dead code, drift from the project's own
  conventions.

Break ties by blast radius, not by effort. A hard fix on a path every
user takes outranks a one-line fix nobody reaches.

Then mark each one **fixable** or **needs a human**. Needs a human means
the correct behaviour is a product decision, or the fix changes a public
API, a data shape, auth, or money. Do not fix those. Carry them to the
report.

**Exit:** an ordered list, each item with a severity and a mark.

## Phase 4. Fix, one at a time

**Entry:** the ranked list.

Work top down. For each finding, all six steps, in order:

1. **Read around it.** The whole function, its callers, the tests that
   cover it. If the code turns out to be right, delete the finding, say
   so, and move on. This happens. It is a good outcome.
2. **Decide the smallest correct change.** Not the best change. The
   smallest one that removes the failure scenario.
3. **Make it.** That change only. A second file is allowed when it is the
   same fix. It is not permission to tidy the second file.
4. **Prove it.** Run the check that would have failed before and passes
   now. Where a test exists, run it. Where none exists, write the
   smallest test that reproduces the Phase 2 failure scenario, watch it
   fail against the old behaviour, then pass. Where code cannot be tested
   this way, state the manual check you ran and what you saw.
5. **Run the project's checks.** Typecheck, lint, tests. Compare against
   the Phase 0 baseline. Any new failure means your fix is wrong: revert
   it, then either do it properly or move it to needs a human. Never
   leave a broken tree and start the next finding.
6. **Record one line each:** finding, change, proof.

Only now start the next finding.

If a fix grows past about three files, or changes an interface, stop.
Revert it. Move it to needs a human with a note on what it would take.
Scope creep inside a fix is how audits break codebases.

**Exit:** every fixable finding is fixed and proven, or moved to needs a
human, or deleted with a reason.

## Phase 5. Re-sweep

**Entry:** Phase 4 finished or stopped.

1. Re-run every dimension pass over the files you touched and their
   direct callers.
2. Run the full checks once more against the baseline.
3. Read your own diff end to end as if a stranger wrote it. Anything you
   would flag in that diff is a new candidate and goes back through
   Phase 2.

**Exit:** the diff produces no new verified finding, and the checks match
or beat the baseline.

## Phase 6. Stop and report

Write the report in the format in [report.md](report.md).

Stop the loop when any of these is true:

- The ranked list is empty.
- Everything left needs a human decision.
- A fix failed twice. Do not try a third approach without asking.
- The checks cannot be run, so nothing can be proven.
- You reached a budget the user set.

Hand back to the human instead of guessing when:

- The correct behaviour is a product question, not a code question.
- The fix touches a public API, a database schema, auth, permissions, or
  money.
- Code looks dead but you cannot see every caller, for example dynamic
  imports, another repo, or a config-driven registry.
- The fix is a rewrite.
- Two findings contradict each other.

Say what you left and why. An honest "this one needs your decision" is
worth more than a confident wrong fix.

## What this must not do

- Do not refactor for taste. Naming you dislike is not a finding.
- Do not rewrite working code. "I would have written this differently" is
  not a bug.
- Do not fix what you cannot prove is broken.
- Do not reformat. A diff full of whitespace hides the real change.
- Do not add dependencies.
- Do not change a test to make it pass. If a test fails, either the code
  is wrong or the test is wrong. Say which, and prove it.
- Do not touch lockfiles, generated files, vendored code, or migrations
  that already ran.
- Do not report the count of findings as the result. Fixed and proven is
  the result.
- Do not commit or push unless asked.

## Optional: subagents for the sweep only

The loop above is linear and needs nothing beyond this skill. That is the
default. Use it unless you have a reason not to.

If your setup gives this agent a subagent tool, you may use subagents in
Phase 1 only, as read-only scouts: one per dimension, each returning
candidates as `file:line` plus one sentence. What that requires, exactly:
a subagent tool available to the agent running this skill, and the
understanding that everything a scout returns is unverified. Every
candidate still goes through Phase 2 here, in this context, by you.

Never delegate Phase 4. Fixes stay in one context, one at a time, so the
same agent holds the change and the proof.

This skill cannot invoke `/loop`, `/subtask`, or any other slash command.
Those are typed by a person. If you want the sweep run again, the person
runs it again.

## Files

- [dimensions.md](dimensions.md). What to look for in each pass, and what
  to throw away.
- [verify.md](verify.md). How to prove a finding is real.
- [report.md](report.md). The output format, with a worked example.
