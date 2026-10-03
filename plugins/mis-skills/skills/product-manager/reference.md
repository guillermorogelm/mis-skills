# Reference: the anatomy of the document

One entry per section, in the order the sections appear in [template.md](template.md). Read the entry, then fill in the section.

One rule covers every section. Write only what you were told. Where you were not told, leave the question in place. A missing answer is information. A plausible invention is damage, because it reads exactly like an agreement that never happened.

## Why the order is what it is

A reader who stops after two minutes should still have the load-bearing part. So the document runs: summary, user, non-goals, must do, criteria. Detail sits below that. If somebody skims only the top half, they still know what is being built and how it will be judged.

---

## 1. Header block

**Holds.** The name. The one sentence. The owner, a person, not a team. Today's date. The status: DRAFT, AGREED, BUILDING, DONE. The file path of the document itself.

**Does not hold.** Version numbers nobody increments. A table of contents. A revision history table. Git already holds history.

**Failure to watch for.** Status sits on DRAFT for the life of the project, so nobody can tell whether the build is allowed to start. Change it to AGREED the moment the user says yes, in the same message.

---

## 2. The one sentence

**Holds.** "A [who] can [verb] [what], so that [outcome]."

**Does not hold.** The word "and" joining two verbs. That is two projects wearing one coat.

**The test.** Read the sentence to somebody who was not in the conversation and ask what gets built. If they have to ask which thing you mean, the sentence has failed.

Bad: "A platform for managing customer relationships and reporting on them."
Good: "A support agent can see a customer's last ten invoices on one page, so they can answer a billing question without opening Stripe."

---

## 3. Who it is for

**Holds.** A named role. How many of them exist. What access they already have. What they already know. Where they are when they use it: desk, phone, warehouse floor, on a call.

**Does not hold.** Invented personas with names and coffee preferences. Market segments. Anything you made up to fill the space.

**Failure to watch for.** The word "users". Every product has users. Naming the role changes the build. "A support agent, signed in, on a laptop, on the phone with the customer right now" produces a different page from "the customer, on a phone, at midnight, annoyed".

---

## 4. Today, without this

**Holds.** What happens now. The tool, the spreadsheet, the copy and paste, the Slack message. How long it takes and how often it happens.

**Does not hold.** Market opportunity. Competitor lists. A business case.

**Why it earns its place.** It is the baseline the finished thing gets measured against, and it is where the acceptance criteria you would otherwise miss are hiding. Somebody who says "then I forward the PDF to my accountant" has told you the real job is download, not view.

---

## 5. Must do

**Holds.** Numbered requirements. One capability per line, in the user's words. Every line maps to at least one acceptance criterion further down.

**Does not hold.** Implementation. "Store the token in a cookie" is not a requirement, it is a decision. Decisions belong in Constraints if they are fixed, or in Assumed decisions if you made them yourself.

**Failure to watch for.** The list reaches forty lines and stops being read. If it passes fifteen, run the size check in SKILL.md again.

Bad: "Full search."
Good: "Find an invoice by number or by amount."

---

## 6. Non-goals

The most valuable section in the document, and the one most specs leave out.

**Holds.** Things a reasonable person would expect this to do, that it will not do. Flat statements. Where the reason matters, add one clause of why, or say where the thing lives instead.

**Does not hold.** Absurdities. "Does not cure disease" is padding, and padding trains people to skip the section.

**Where non-goals come from.**

- Round 2 of the interview.
- Anything the user mentioned once and moved past. They will remember mentioning it, usually in week three.
- The obvious neighbouring feature. If you built a list, somebody expects export. Say whether it is there.
- Anything the name implies. A page called Billing implies paying. Say so if it does not take payment.
- Anything you decided not to build while writing the spec. If you thought about it and dropped it, write it down.

**Minimum three.** A spec with no non-goals has no edges, and a thing with no edges cannot be finished.

Bad: "Not building everything."
Good: "No payments. The page shows invoices and their status. Paying still happens through the Stripe link in the email."

---

## 7. Assumed decisions

**Holds.** Every call you made without the user. One line each: what you chose, what it rules out, the marker `ASSUMED`, and the date.

**Does not hold.** More than three. A fourth assumption means the interview was not finished, and the document should say so instead.

**Why it exists.** An assumption written on line 40 of a document is cheap to reverse. The same assumption buried in code is expensive, and it usually surfaces as an argument about whether it was ever agreed.

Format: `ASSUMED 2026-09-02. Invoices are read from the existing Stripe sync table, not from the Stripe API live. Rules out invoices created in the last five minutes.`

---

## 8. Open questions

**Holds.** Numbered questions. Each one names the person who can answer it and what is waiting on the answer.

**Does not hold.** Questions you can answer yourself by reading the code or the existing product. Go and read it.

Mark anything that stops work with `BLOCKED`. A spec with a BLOCKED line is not agreed, whatever the status field says.

---

## 9. Constraints

**Holds.** The fixed things. The stack you must use. The system you must not touch. The deadline and what it is attached to. Who is available and for how long. Legal, policy, or privacy limits. The budget, if there is one.

**Does not hold.** Preferences. A preference that is not fixed is a decision, and it goes in Assumed decisions where it can be argued with.

**Failure to watch for.** "Must be secure" and "must be accessible". Both are wishes at this altitude. Convert them into something checkable and move them into acceptance criteria: no customer identifiers in the URL, every control reachable by keyboard, text contrast at 4.5:1 or better.

---

## 10. Failure and empty states

**Holds.** What the user sees when the list is empty, the network fails, the input is wrong, permission is denied, and the thing is still loading. One line each. Exact copy where the exact copy matters.

**Does not hold.** Nothing. This section is never empty.

**Why.** It is half the build and none of the brief. Specify it here, or somebody improvises it at six in the evening on the day it ships.

Every line in this section should produce an acceptance criterion.

---

## 11. Data and scale

**Holds.** Where the data comes from. Who owns it. How fresh it has to be. How much of it on day one, and how much in a year. Anything that counts as personal data, named as such.

**Does not hold.** A schema, unless the schema is fixed and therefore a constraint.

**Failure to watch for.** The number gets guessed. Ask. Five hundred rows and five million rows are different products with identical briefs.

---

## 12. Acceptance criteria

The done-condition. This is the section the rest of the document exists to produce.

**Holds.** Numbered statements. Each one true or false about the finished thing. Each one names where to check.

**Does not hold.** Tasks. "Write the tests" is a task. "The list shows ten rows, newest first" is a criterion.

**Rules.**

- Present tense, describing the finished thing, not the work.
- At least one number, literal string, file path, URL, or observable state per line.
- Names where to look: the screen, the file, the panel, the endpoint.
- No disqualifying words: fast, easy, simple, intuitive, clean, polished, nice, smooth, user-friendly, properly, gracefully, appropriate, handles, supports, works well.

**The two-reader test.** Two people read the line, look at the same build, and cannot disagree about the verdict. Anything that fails this is a wish, not a criterion.

**Coverage.** One criterion for every failure state in section 10. One for every line in Must do. One for any non-goal that is at risk of creeping in, written as a negative: the thing that must not appear.

**Count.** Under twenty for one project. Past twenty, run the size check again.

---

## 13. Cut list

**Holds.** The order things come out if time runs short. Numbered, first out at the top. Agreed in advance, while everybody is calm.

**Does not hold.** Things nobody intends to cut. A cut list of items you will fight for is theatre.

**Why.** Cutting under deadline pressure without a list produces the wrong cut and an argument about it. The list turns a fight into a decision somebody already made.

---

## 14. Change log

**Holds.** One row per request that arrived after sign-off. Date, the request in one line, the verdict (IN, NEXT, TRADE), and the cost stated in criteria and days.

**Does not hold.** Silent edits. If the spec changed, this table says when and why.

**Why.** At the end of the project this table is the answer to "why did it take longer than we said". It also stops the same rejected request arriving four more times, because it is written down with a verdict next to it.

---

## 15. Sign-off

**Holds.** Who agreed, on what date, to which version. One line each. Plus this sentence: "Anything not in this document is not in this build."

**Does not hold.** Signature blocks, approval workflows, ceremony. Two names and two dates is enough.

---

## Keeping the document alive

The spec is not an artefact you file. It is the thing the build gets checked against.

- Tick criteria as they pass. Leave the number visible.
- When you change the spec, change it in the document and say so in the chat. Never in the chat alone.
- When the build is finished, the status goes to DONE and every criterion has a tick or a written exception with a name against it.
