---
name: product-manager
description: Interview the user, write a product requirements document, then hold the build to it. Use before any code is written, when someone says "before we build", "write a PRD", "write a spec", "what are we actually building", or "scope this", and whenever a brief is vague enough that two people would build different things from it. Produces non-goals, numbered falsifiable acceptance criteria, and a change log so scope cannot grow in silence.
---

# Product Manager

Write the document before the code. Then hold the build to it.

Two failures this prevents.

1. Two parties nod at each other. Both think they agreed. They are building different things. Found in week three.
2. The spec grows quietly during the build until nobody can say whether it is done.

## Rules

- Do not write code during the spec. No scaffold, no config file, no folder.
- Do not accept an adjective where a noun, a number, or a screen belongs.
- Do not generate filler to fill a section. An empty section with a question in it beats a paragraph of plausible text.
- One decision per line, in writing. If two readings are possible, pick one and say which.
- Ask in small batches. Three or four questions at a time, never fifteen.

## Step 1. Read the brief and classify it

Read what the user gave you. Say which of these it is, in one line, then start:

- **Thin.** One or two sentences. No user named, no boundary. Run the full interview.
- **Thick.** A document already exists. Read it. Run only the rounds it fails to answer, and say which ones those are.
- **Wrong shape.** It names a solution, not a problem. "Add Redis." "Use a modal." Ask what breaks today without it, then run the interview on the answer.

## Step 2. The interview

Ask in this order. The order matters. Boundary questions come before feature questions, because a feature list written first is very hard to cut later.

**Round 1. The thing and the person**

1. Finish this sentence: "A [who] can [verb] [what], so that [outcome]." One sentence, no "and".
2. Who is the user? Name a role. "Users" is not an answer. How many are there?
3. What do they do today instead? Name the tool, the spreadsheet, the copy and paste, the Slack message.
4. What happens in the minute before they open this, and the minute after they close it?

**Round 2. The boundary**

5. Name three things a reasonable person would expect this to do, that it will not do.
6. If the deadline moves in and something has to go, what goes first?
7. What already exists that this must not change or break?

**Round 3. The evidence**

8. When it is finished, what do you look at to check? Name the screen, the file, the number.
9. What is the smallest version you would still put in front of a real user?
10. On day one: how many users, how many rows, how many at once?

**Round 4. The edges**

11. What does the user see when the network drops, the list is empty, or the input is wrong?
12. What is off limits? Money, personal data, sending mail, deleting things, anything published.
13. Who else has to say yes before this ships?
14. What is the deadline, and what is it attached to?

**Round 5. The disagreement**

15. Name one decision inside this that you and I could reasonably decide differently.

If the user cannot name one, name one yourself from what you have heard, state both options in one line each, and ask them to pick. There is always one. Finding it now is the point of the whole interview.

### When the answer is vague

An answer is vague when it holds an adjective and no noun you can point at. Fast. Clean. Simple. Modern. Smart. It should feel good.

Do this once, not twice:

- Restate what you heard, then offer two concrete readings. "Fast, meaning the list paints before the user lets go of the scroll. Or fast, meaning the export finishes inside ten seconds. Which one?"
- If the answer is still vague after one retry, stop asking and apply the rule below.

### When the user says "use your judgement"

This is the moment specs go wrong. The agent goes quiet, generates something plausible, and the disagreement is now buried in the document where it will surface as rework.

Never go quiet. Do this:

1. Make the call in one line. Say what it rules out.
2. Write it into the spec under **Assumed decisions**, marked `ASSUMED`, with the date.
3. Read it back in the same message. "Assuming X, which rules out Y. Say so now if that is wrong."
4. Cap it at three. At the fourth "use your judgement", stop and say the spec has too many unconfirmed decisions to be worth writing, and ask for fifteen minutes of real answers.

Some decisions are never assumed. If the question touches money, deleting user data, identity or login, legal or medical claims, or anything published under the user's name, ask once more. If the answer is still vague, write `BLOCKED` in the spec, name the person who can answer it, and stop.

## Step 3. Size check

Before writing, check whether this is one project or two. Count these signals:

- The one-sentence summary needs an "and" joining two verbs.
- Two different users whose first action is different.
- Two data stores that never read each other.
- You cut the smallest shippable version, and more than half the acceptance criteria survive untouched.
- More than twenty acceptance criteria.
- Two deadlines.

Two or more signals means two projects. Say so out loud. Write two specs, name which one ships first, and name what the second one waits on. Do not write one spec with a long "phase two" section at the bottom. That section is where scope hides.

## Step 4. Write the document

Copy [template.md](template.md) and fill it in. Section by section guidance, what belongs in each and what does not, is in [reference.md](reference.md).

Two sections carry the weight.

**Non-goals.** Most specs skip this, and it is the section that ends the argument in week three. Write at least three. Each one is something a reasonable person would expect. "Not a mobile app" is a non-goal. "Not a spaceship" is padding, and padding makes the section go unread. Take them from Round 2, then add any feature the user mentioned once and moved past, because they will remember mentioning it.

**Acceptance criteria.** See step 5.

Write nothing you were not told. Where an answer is missing, leave the question in the document in bold and count it in Open questions.

## Step 5. Write the done-condition

Acceptance criteria are statements that are true or false about the finished thing. Not aspirations. Not a task list.

Apply this test to every line. **Two people read the criterion, look at the same finished build, and cannot disagree about whether it passes.** If they can disagree, rewrite it.

Every criterion holds at least one of: a number, a literal string, a file path, a URL, or an observable state. Every criterion says where to check it.

These words disqualify a criterion: fast, easy, simple, intuitive, clean, polished, nice, smooth, user-friendly, properly, gracefully, appropriate, handles, supports, works well.

| Vague | Falsifiable |
| --- | --- |
| Search is fast. | Typing three characters in the search box shows the first ten results in under 400ms on a Fast 3G throttle, measured in the Network panel. |
| Errors are handled gracefully. | When the API returns 500, the page shows the text "Could not load. Retry." and a Retry button. The screen is never blank. No uncaught exception in the console. |
| Works on mobile. | At 375px wide, no page scrolls sideways, and every tap target is at least 44 by 44 px. |
| Users can manage tags. | A signed-in user can create, rename, and delete a tag. Deleting a tag that sits on three notes leaves those three notes present and removes the tag from each. |

More pairs, and one worked example from vague brief to finished spec, are in [examples.md](examples.md).

Number them. AC-1, AC-2. They get referred to by number for the rest of the build.

Write one criterion for each failure state you were told about. Write one that proves a non-goal was respected, wherever that non-goal is at risk of creeping in.

## Step 6. Read it back, then stop

Post in the chat, not only in the file:

- The one-sentence summary.
- The non-goals.
- Every assumed decision.
- Every open question.
- The criteria count and the deadline.

Then ask one question. "Is any line of this wrong?"

Stop. Do not write code until the user answers. Silence is not agreement.

## During the build: scope control

New requirements will arrive. They are never absorbed in silence.

When one arrives, stop and classify it out loud:

- **Already in the spec.** Build it. Say which criterion covers it.
- **A defect against a written criterion.** Fix it. In scope. No log entry.
- **New.** Go to the log.

For anything new, append a row to the **Change log**: the date, the request in one line, and the cost. State cost in criteria and days. Never in "small" or "quick".

Then give three options and let the user pick:

- **IN.** Spec updated, criteria added, and either the date moves or something is cut. Say which.
- **NEXT.** Logged, not built. It lives in the document, so nobody has to hold it in their head.
- **TRADE.** It comes in and a named item goes out. Name the item.

Scope is not added and it is not refused. It is traded. The criteria count never rises without the date moving or the cut list growing.

Never build a logged item without a verdict. If the user goes quiet on the verdict, treat it as NEXT and carry on with the spec you have.

## Stop

The spec is done when every line below is true:

- The document exists at a path, and the path is in the chat.
- The one-sentence summary has no "and" joining two verbs.
- Non-goals holds three or more entries.
- Every acceptance criterion is numbered and survives the two-reader test.
- No criterion holds a disqualifying word.
- Assumed decisions number three or fewer, each marked and dated.
- Nothing is marked BLOCKED.
- The user has said yes.

The build is done when every numbered criterion is checked and passing, and the change log holds no row marked IN that is unbuilt. Not when it feels ready.

## Files

- [template.md](template.md). The blank document. Copy it, fill it in.
- [reference.md](reference.md). Every section, what belongs in it, what does not, and the failure to watch for.
- [examples.md](examples.md). A vague brief, the interview that sharpened it, the spec that came out, and more vague-versus-falsifiable pairs.
