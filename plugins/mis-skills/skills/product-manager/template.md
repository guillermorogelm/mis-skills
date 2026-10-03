<!--
THE SPEC. Copy everything below this comment into a new file.
Suggested path: docs/spec-[short-name].md
Delete every HTML comment and every [bracket] as you fill it in.
Leave a section empty and unanswered rather than filling it with invention.
An unanswered question is information. Invented text reads like agreement.
-->

# [Name]

**One sentence.** A [who] can [verb] [what], so that [outcome].
**Owner.** [Person, not a team]
**Date.** [YYYY-MM-DD]
**Status.** DRAFT
<!-- DRAFT until the user says yes. Then AGREED. Then BUILDING. Then DONE. -->
**Path.** [path to this file]

---

## 1. Who it is for

**Role.** [Named role, not "users"]
**How many.** [Number on day one]
**Where they are.** [Desk, phone, on a call, warehouse floor]
**What they already have.** [Login, permissions, prior knowledge]

## 2. Today, without this

[What happens now. The tool, the spreadsheet, the copy and paste, the Slack
message. How long it takes. How often it happens. Keep it to five lines.]

## 3. Must do

<!-- One capability per line, in the user's words. Not implementation.
     Every line here maps to at least one criterion in section 9.
     Past fifteen lines, run the size check again. -->

1. [Capability]
2. [Capability]
3. [Capability]

## 4. Non-goals

<!-- The section most specs skip. Minimum three. Each one is something a
     reasonable person would expect. Where it matters, say where the thing
     lives instead. No absurdities. -->

- No [thing]. [Where it lives instead, or why not.]
- No [thing]. [Where it lives instead, or why not.]
- No [thing]. [Where it lives instead, or why not.]

## 5. Assumed decisions

<!-- Every call made without the user. Maximum three. Each one dated and
     marked. Say what it rules out, not only what it chose.
     Never assume anything touching money, deleting user data, identity,
     legal claims, or anything published under the user's name. Ask, or
     mark it BLOCKED in section 6. -->

- `ASSUMED [YYYY-MM-DD]` [Decision]. Rules out [what it closes off].

## 6. Open questions

<!-- Each one names who can answer it and what waits on the answer.
     Mark anything that stops work as BLOCKED. A spec with a BLOCKED line
     is not agreed, whatever the status field says. -->

1. [Question] Asked of: [name]. Waiting on it: [what cannot start].

## 7. Constraints

**Deadline.** [Date] because [what it is attached to].
**Must use.** [Stack, service, existing system]
**Must not touch.** [System, file, table, integration]
**People.** [Who is building it, for how long]
**Legal or policy.** [Limits, or "none stated"]

## 8. Failure and empty states

<!-- Never leave this empty. Every line here produces a criterion in section 9. -->

| Situation | What the user sees |
| --- | --- |
| Nothing to show yet | [Exact copy] |
| Still loading | [What is on screen] |
| Network or upstream failure | [Exact copy, plus what they can do next] |
| Input rejected | [Exact copy, and where it appears] |
| Permission denied | [Exact copy] |

## 9. Acceptance criteria

<!-- The done-condition. Statements that are true or false about the finished
     thing. Present tense. Each one holds a number, a literal string, a path,
     a URL, or an observable state, and says where to check.
     Two people read the line, look at the same build, and cannot disagree.
     Banned here: fast, easy, simple, intuitive, clean, polished, nice,
     smooth, user-friendly, properly, gracefully, appropriate, handles,
     supports, works well.
     Past twenty criteria, run the size check again. -->

| # | Criterion | Where to check | Pass |
| --- | --- | --- | --- |
| AC-1 | [Statement] | [Screen, file, panel, endpoint] | [ ] |
| AC-2 | [Statement] | [Where] | [ ] |
| AC-3 | [Statement] | [Where] | [ ] |

## 10. Data and scale

**Source.** [Where the data comes from, who owns it]
**Freshness.** [How out of date it may be]
**Day one.** [Rows, users, requests]
**In a year.** [Rows, users, requests]
**Personal data.** [What is personal, or "none"]

## 11. Cut list

<!-- The order things come out if time runs short. First out at the top.
     Agreed now, while everybody is calm. Only put things here you would
     genuinely cut. -->

1. [First to go]
2. [Second]
3. [Third]

## 12. Change log

<!-- One row per request arriving after sign-off. Nothing is absorbed in
     silence. Cost is stated in criteria and days, never in "small".
     IN: spec updated, and either the date moves or something is cut.
     NEXT: logged, not built.
     TRADE: it comes in, a named item goes out. -->

| Date | Request | Verdict | Cost |
| --- | --- | --- | --- |
| [YYYY-MM-DD] | [One line] | [IN / NEXT / TRADE] | [+n criteria, +n days, or what came out] |

## 13. Sign-off

Anything not in this document is not in this build.

- [Name], [YYYY-MM-DD]
- [Name], [YYYY-MM-DD]
