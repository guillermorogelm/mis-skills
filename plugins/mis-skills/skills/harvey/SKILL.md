---
name: harvey
description: Install, set up and run Harvey (github.com/ethanplusai/harvey), an open-source autonomous sales agent that finds local businesses, learns something specific about each, writes cold email, sends it only after your approval, and works replies toward a meeting - using your Claude Pro/Max subscription through the claude CLI, with no API bill. Use when asked to set up Harvey, "an AI SDR", "find clients and email them", automate cold outreach or prospecting, or check Harvey's pipeline, outbox or dashboard.
---

# Harvey

Harvey is a separate Python app, not a skill. This skill installs it from
upstream, gets it configured, and runs its commands. The app keeps its own
data (`data/harvey.db`, `.env`, `harvey.yaml`) in its folder.

Upstream: https://github.com/ethanplusai/harvey (MIT, Ethan Rogers).

## Rules

- **The user is the sender.** Before the first send, say this in plain words:
  cold email has legal rules (CAN-SPAM in the US, GDPR/PECR in the EU and
  UK, local law elsewhere), it needs a physical mailing address in the
  footer and a working opt-out, and it should go from a **dedicated sending
  domain** with SPF, DKIM and DMARC, warmed up for 2-4 weeks. Not legal
  advice.
- **Never turn off approval** (`channels.email.require_approval`) and never
  run `harvey outbox --approve-all` unless the user asks for it in this
  conversation. Show drafts; let the user approve.
- **Never enable LinkedIn automation** unless asked. It breaks LinkedIn's
  terms and can get the account restricted.
- **Never paste secrets into chat or commit them.** Keys go in Harvey's
  `.env` only, typed by the user or written by them.
- If a prospect asks whether they are talking to an AI, Harvey answers
  truthfully. Never configure it otherwise.

## Step 1. Install (once)

Default location `~/harvey`, outside any other repo. Needs Python 3.11+
(`python3 --version`; on macOS use `python3.13`, installed with
`brew install python@3.13`, because the system `python3` is 3.9) and a
logged-in `claude` CLI on a Pro or Max plan.

```bash
git clone https://github.com/ethanplusai/harvey.git ~/harvey
cd ~/harvey
python3 -m venv .venv && .venv/bin/pip install -e .
.venv/bin/harvey --help
```

If `~/harvey` already exists, `cd ~/harvey && git pull && .venv/bin/pip install -e .`
to update instead.

## Step 2. Set up

Two ways. Prefer the first:

- **Its own wizard.** Tell the user to open a new Claude Code session in
  `~/harvey` and say "set up Harvey for me". Harvey ships a `CLAUDE.md` that
  turns that session into its setup wizard (mailbox, product training,
  signals).
- **By hand**, from `~/harvey` with the venv active
  (`source .venv/bin/activate`):

```bash
cp .env.example .env        # the user fills it in; every variable is documented inline
harvey train https://their-company.com
harvey signals              # review the 23 signals it can collect
harvey signals --confirm free
harvey discover
harvey dashboard            # http://localhost:5555
```

Signals are deliberately opt-in: nothing is collected until the user
confirms it. Paid signals (for example `SERP_RANK`) are confirmed one by one.

## Step 3. Run and check

```bash
harvey status               # pipeline counts
harvey outbox               # drafts waiting for approval
harvey run                  # the loop: prospect, write, queue, send approved, read replies
harvey sending pause        # kill switch
harvey sending resume
harvey sending status
harvey usage                # subscription usage
harvey export               # prospects as a sequencer-ready CSV
```

`harvey run` keeps going until stopped. Run it in the user's own terminal
(or under tmux/screen), not inside this session, unless they ask.

## When the user asks how it is going

Run `harvey status` and `harvey outbox` from `~/harvey`, then summarize in
three lines: prospects found, drafts waiting for approval, replies waiting.
Offer to open the dashboard.
