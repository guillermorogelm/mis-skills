---
name: night-crew
description: >-
  Set up a night crew for your app: three Claude Code cloud routines that work on your GitHub repo
  while you sleep. A builder ships the next feature from your backlog as a pull request, a scout
  looks for people who need what you make and drafts a week of social posts, and a tracker checks
  what's working and what's broken. House rules keep them off your money, your data and your live
  app: they only ever open pull requests for you to review. Use when the user wants Claude to work
  overnight, while they sleep, on a schedule, "a night shift", "a night crew", or to wake up to
  finished work. Also `/night-crew morning` for the morning briefing.
argument-hint: "[setup | morning]"
license: MIT
metadata:
  author: "Alex Chen (@nocodealex)"
  homepage: "https://chen.media"
  source: "https://github.com/alexyc9381/night-crew-skill"
  version: "1.0.0"
---

# night-crew

You set up a night crew for the user's app: three Claude Code **routines** (scheduled cloud agents)
that run against their GitHub repository every night, on Anthropic's cloud, while their laptop is
closed. Each one opens a pull request in the morning. Nothing they make reaches the user's live app
until the user merges it.

What the user typed after `/night-crew`: `$ARGUMENTS`

- Blank, `setup`, or anything about setting it up: do **Setup** below.
- `morning`, "what did the crew do", "briefing": do **Morning** below.

## What you need to know first (tell the user only what applies)

- Routines need a Claude **Pro, Max, Team or Enterprise** plan, and a GitHub repository. They are
  a research preview, so names and limits can change. Each run uses the user's plan usage like a
  normal session.
- A routine clones the repo from its **default branch** every run and pushes to `claude/` branches.
  So the crew's standing orders must be committed on the default branch, in a file called
  `NIGHT-CREW.md` at the repo root.
- Routines run with no permission prompts. That is why the house rules exist, and why Setup ends
  with three hard guardrails the user switches on in GitHub and claude.ai. Rules in a prompt are
  instructions; the guardrails are what actually stop a mistake.

## Setup

### 1. Find the repo

Work in the folder the user ran this from. Check it is a git repo with a GitHub remote
(`git remote -v`) and note the default branch (`git symbolic-ref refs/remotes/origin/HEAD` or ask).
If there is no GitHub remote, stop and tell the user the crew needs the app on GitHub first.

### 2. Interview the user (one short message, then wait)

Ask for, in plain words, and offer an example answer for each:

1. **The app in one sentence**, and who it is for ("a booking app for dog groomers").
2. **The backlog**: 3 to 10 things they want built, most important first ("a signup page with
   email and Google", "a pricing page", "dark mode"). Each should be something one night can
   finish. Split anything bigger.
3. **The customers**: who would pay, and where those people talk online (subreddits, forums,
   communities). If they don't know, the scout will find out.
4. **Marketing they want drafted**: for example a week of social posts, or a launch video script.
5. **Bedtime**: when they go to sleep and wake up, and their time zone.
6. **Anything the crew must never touch**: folders, files or services beyond the house rules.

Look at the repo yourself before asking about anything you can read: the stack, how to run the
tests (`package.json` scripts, `Makefile`, `pyproject.toml`), the README. Don't ask for those.

### 3. Write NIGHT-CREW.md

Copy `NIGHT-CREW.template.md` from this skill's folder (`${CLAUDE_SKILL_DIR}`; if that path looks
unexpanded, use the "Base directory for this skill" Claude Code printed above) to `NIGHT-CREW.md` at
the repo root and fill in every `{{...}}` from the interview and what you read in the repo:

- Keep the backlog as a checklist, most important first, one line each, each small enough for a night.
- Fill **How to check your work** with the real commands (install, test, build, lint) you found.
  If there are no tests, say so plainly; the tracker will note it every morning.
- Keep the **House rules** section exactly as written, then add the user's own never-touch list
  under it.
- Don't invent customers, numbers or plans the user didn't give you.

Show the user the finished file and ask them to read the house rules.

### 4. Put it on the default branch

The routines read `NIGHT-CREW.md` from the default branch. Ask the user whether to commit it now.
On a yes, commit only that file with the message `Add the night crew's standing orders` and push it
to the default branch (or open a pull request for it if the branch is protected, and tell them to
merge it before bedtime). Never commit anything else in this step.

### 5. Create the three routines

Routines are created with `/schedule` (in the Claude Code CLI), at **claude.ai/code/routines**, or
in the Desktop app (Code tab, then Routines, then New routine, then **Cloud**). You can't run
`/schedule` for the user from inside this skill; give them the three lines to paste, one at a time,
with the times filled in from their bedtime. Space the runs an hour apart, and put them a few minutes
past the hour (runs exactly on the hour can start late):

```
/schedule every night at {{builder time}}: in {{owner/repo}}, read NIGHT-CREW.md and do the Builder's job. Follow its house rules exactly.
/schedule every night at {{scout time}}: in {{owner/repo}}, read NIGHT-CREW.md and do the Scout's job. Follow its house rules exactly.
/schedule every night at {{tracker time}}: in {{owner/repo}}, read NIGHT-CREW.md and do the Tracker's job. Follow its house rules exactly.
```

A good default for someone asleep from 11pm to 7am: builder 1:07am, scout 2:07am, tracker 5:07am
(the tracker goes last so it can check the builder's pull request).

`/schedule` asks follow-up questions. Tell the user how to answer them:

- **Repository**: only this app's repo.
- **Environment**: the builder and the tracker use **Default** (Trusted network access: package
  registries and common development sites only). The scout reads the web, so give it an environment
  with **Custom** network access listing the sites it should read (for example `reddit.com`,
  `news.ycombinator.com`, `indiehackers.com`), or **Full** if they accept that.
- **Connectors**: remove all of them unless one is needed. A routine can use every tool in an
  included connector, including writes, without asking. Never include a payments, banking, email or
  social-posting connector.
- **Model**: their usual model is fine.

If `/schedule` says "Unknown command", they are not signed in with a claude.ai subscription, or
they're inside a cloud session; they can create the same three routines at claude.ai/code/routines
with the prompts above and a **Daily** schedule.

### 6. The three guardrails (walk the user through them; you can't do these for them)

1. **Protect the default branch on GitHub**: Settings, then Rules (or Branches), add a rule for the
   default branch that requires a pull request before merging and blocks force pushes and deletions,
   with no bypass for the account the routines push as (it's the user's own account, so admins
   must not be exempt). Then the crew can only ever propose changes.
2. **No real secrets in the cloud environment**: no production database URLs, payment keys or
   admin tokens in the routine's environment variables. Test keys only, and only if the tests
   need them.
3. **No connectors that can spend or publish**: as in step 5.

### 7. Tell the user what happens next

In two or three lines: tonight the routines run at the times set; tomorrow there will be up to
three pull requests from `claude/` branches (code from the builder, a report from the scout, a
report from the tracker); run `/night-crew morning` with coffee; nothing ships until they merge it.
They can pause or delete any routine at claude.ai/code/routines, or with `/schedule list`.

## Morning

The briefing. Read-only: don't merge, close, push or edit anything.

1. List the crew's open pull requests: `gh pr list --search "head:claude/" --state open` (if `gh`
   isn't installed or signed in, ask the user to open the repo's pull requests page and paste the
   list). Also look at routine runs if the user mentions any failed.
2. For each one, read the description and the report files it adds under `night-crew/`.
3. Give the user one screen, most important first:
   - **Ready to review**: what the builder built, which backlog item, whether its checks passed.
   - **Needs your OK**: anything a crew member flagged instead of doing (spending, deleting,
     touching the live app, posting publicly).
   - **What the scout found**: the best 3 leads (with links) and where the post drafts are.
   - **What the tracker says**: what works, what's broken, and what it suggests building next.
4. Offer the next step: review a pull request together, move a backlog item, or change the crew's
   orders in `NIGHT-CREW.md`.

## Never

- Never merge a pull request, push to the default branch (except the one standing-orders commit the
  user approved in Setup step 4), or change GitHub, claude.ai or routine settings yourself.
- Never put secrets, keys or tokens into `NIGHT-CREW.md` or any prompt.
- Never promise the crew will finish everything: one backlog item a night is a good night.
