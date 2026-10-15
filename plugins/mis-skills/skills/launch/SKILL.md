---
name: launch
description: >-
  Launch an app the way NASA launches a rocket: before it goes live, 8 Claude
  flight controllers each check one part of it (tests, security holes, the
  database, speed, the actual cost, the user's path, recovery, privacy and
  rules) and answer GO or NO-GO. One NO-GO holds the launch, and a flight
  director Claude writes up the holds and the fixes. Use when the user is about
  to launch, ship, deploy or go live, asks "is my app ready", "can I ship this",
  wants a pre-launch or production-readiness check, says Claude told them it's
  done but they aren't sure, or says "launch" or "go/no-go".
argument-hint: "[--quick | --only tests,security | --recheck] [what is launching]"
license: MIT
metadata:
  author: "Alex Chen (@nocodealex)"
  homepage: "https://chen.media"
  source: "https://github.com/alexyc9381/launch-skill"
  version: "1.0.0"
---

# launch

Before a NASA rocket leaves the pad, the flight director polls every flight controller, and each one answers GO
or NO-GO for their own system. One NO-GO and the countdown holds. This skill runs an app's launch the same way.

It exists because the Claude that built an app grades its own work, so it tends to say the app is ready even when
there are problems. Here the checking is split between 8 controllers who each own one part and never see each
other's calls. You are the launch coordinator: you write the mission, run the poll and read out the result. You
never make a call yourself, never soften one, and never fix anything during the poll.

What the user typed after `/launch`: `$ARGUMENTS`

If that is blank, or still reads like a placeholder, the launch is the app in the current directory.

## The tool

Every piece of bookkeeping goes through `launch.py` in this skill's folder:

```bash
python3 "${CLAUDE_SKILL_DIR}/launch.py" <command>
```

Below, `LAUNCH` means exactly that command. If the path looks unexpanded, use the "Base directory for this skill"
that Claude Code printed at the top of this skill. Run it from the root of the user's project. The state lives in
`.launch/<run>/` there, and every command after `init` finds it through `.launch/LATEST`.

## Step 1: size it

| flag | meaning |
| --- | --- |
| (none) | All 8 stations: TESTS, SECURITY, DATABASE, SPEED, COST, USERS, RECOVERY, RULES. |
| `--quick` | The first five: TESTS, SECURITY, DATABASE, SPEED, COST. |
| `--only a,b` | Just those stations, for example `--only security,cost`. |
| `--recheck` | Only the stations that said NO-GO last time, after the user fixed things. |

Run `LAUNCH plan` with the same flags and tell the user in one line how big the poll is, for example "8 stations
+ 1 flight director, 9 sub-agent calls", then start. If this skill fired on its own (the user never asked for a
launch check), ask once first and offer `--quick`.

The controllers write their reports into `.launch/`. In the default permission mode that is one approval per file;
suggest accept-edits mode (Shift+Tab) for the poll. Do not change the user's settings yourself. Suggest adding
`.launch/` to `.gitignore`.

## Step 2: write the mission file

**Sub-agents cannot see this conversation.** Every controller knows only the mission file and the project, so write
`.launch/mission.md` to stand on its own. Read the project first (README, package.json or pyproject, the folder
layout, recent commits), then write:

- First line: what is launching, in one sentence ("CaptionPal goes live: an AI caption writer for Instagram posts").
- What the app does and who uses it, its stack, and where it runs (Vercel, Supabase, a VPS...).
- How to run the tests, type check, lint and production build, if you found them.
- What this launch changes: the branch, the recent commits or the parts the user named.
- What the user told you that matters: expected users, budget for running costs, payments, launch date.

Do not write your own opinion of the app into it, and do not add facts nobody gave you. A mission file that says
"the app is solid" decides the poll before it starts.

## Step 3: open the poll

```bash
LAUNCH init --mission-file .launch/mission.md [--quick | --only a,b | --recheck]
```

## Step 4: the poll

Always drive it with `LAUNCH next`. It reads the files on disk and tells you the next phase and the exact command.
The phases run in this order: `poll` (the stations), `director` (the flight director).

Every phase works the same way:

1. `LAUNCH prompts <phase>` writes one brief per job and lists the jobs still to run, in waves.
2. Launch **one wave at a time**: a single message with one Agent tool call per job in that wave (the Agent tool is
   called Task in older Claude Code versions). Each call is:
   - `subagent_type`: `general-purpose`
   - `description`: `launch <job id>`
   - `prompt`: `Read <brief path> and follow it exactly. It is your whole brief.`

   Wait until every agent in the wave has replied before you launch the next wave.
3. After the last wave, run `LAUNCH next`. If a report is missing it sends you back to the same phase, and `prompts`
   then lists only the missing jobs. Re-run those once. If a station fails twice, leave it without a report: the
   board counts it as NO CALL, which holds the launch. Never write a report or a call yourself.

## Step 5: the board

When `LAUNCH next` says the poll is complete:

```bash
LAUNCH render
```

It counts the calls, writes `LAUNCH-REPORT.md` into the run folder and prints it. Show the user the call line, the
board and the flight director's sections exactly as written. Then add at most two lines of your own: the first fix
you would make, and the path to the full poll.

Rules for you, the coordinator:

- The call is the rule: GO for launch only if every station said GO. Never change it, soften it or re-count it.
- Never add reassurance the stations did not give. A HOLD is the poll doing its job.
- Do not start fixing during the poll. When it is over, offer to work through "Fix before launch" in order, then
  `/launch --recheck` to poll only the stations that held.
- If the user disagrees with a call, offer `/launch --only <station>` with what they told you written into the
  mission file. Do not argue for or against the app yourself.
