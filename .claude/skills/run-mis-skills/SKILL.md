---
name: run-mis-skills
description: Validate, install, list and run the skills in this mis-skills marketplace from a clean container. Use when asked to check, test, validate, install, run, try or smoke-test a skill or the plugin, before opening a PR that adds or edits a skill, or to see what a skill actually outputs headlessly.
---

# Run mis-skills

This repo is a Claude Code plugin marketplace (`.claude-plugin/marketplace.json`)
with two plugins: `plugins/mis-skills` (a folder per skill) and
`plugins/linkedin-skills` (vendored as a whole plugin, because its skills share
`references/`, `lib/` and `scripts/` at its root). The driver reads the plugin
list from `marketplace.json`, so a new plugin is picked up automatically. "Running" it
means three things: the manifests and every `SKILL.md` validate, a real Claude
Code install loads all skills, and a skill produces output when invoked. The
driver does all three without touching your real `~/.claude`.

All paths are relative to the repo root.

## Prerequisites

`claude` (Claude Code CLI) and Node 22 on `PATH`. Nothing to install: the
bundled tests use only `node:test`. Verified with Claude Code 2.1.299 and
Node v22.22.0.

## Run (agent path)

```bash
node .claude/skills/run-mis-skills/driver.mjs check
```

Offline, no model calls. Runs `claude plugin validate` on the marketplace,
each plugin and (with `--strict`) each skills folder; checks every
`SKILL.md` has frontmatter whose `name` equals its folder and a non-empty
description; warns on descriptions over 1024 characters and skills missing
from `README.md`; runs every bundled `*.test.mjs` and fails only on test
failures not listed in `known-test-failures.txt`. Exit 0 means OK.

```bash
node .claude/skills/run-mis-skills/driver.mjs install
node .claude/skills/run-mis-skills/driver.mjs list
```

`install` adds this checkout as a local marketplace in a sandbox config
(`CLAUDE_CONFIG_DIR=/tmp/mis-skills-sandbox/config`, override with
`MIS_SKILLS_SANDBOX`) and installs every plugin as `<plugin>@mis-skills`; it prints each
plugin's skill count and always-on token cost. `list` starts a headless
session and fails if any skill folder is not visible as `<plugin>:<name>`. One short
model call.

```bash
node .claude/skills/run-mis-skills/driver.mjs invoke product-manager "a habit tracker app for one person"
node .claude/skills/run-mis-skills/driver.mjs invoke linkedin-skills:linkedin-humanizer "--mode audit for this draft (do not publish anything): <text>"
```

Runs `/<plugin>:<skill> <args>` (a bare skill name is looked up in every plugin) in a headless session (read-only tools:
Read, Glob, Grep; max 8 turns), prints each tool call, any tool errors and
the final answer, and saves the answer to
`/tmp/mis-skills-sandbox/invoke-<skill>.md`. Run `install` first.

`all` = `check` + `install` + `list`.

### Before a PR that adds or edits a skill

```bash
node .claude/skills/run-mis-skills/driver.mjs all
node .claude/skills/run-mis-skills/driver.mjs invoke <new-skill> "<a realistic request>"
```

Read the saved output: did it read the skill's reference files, and does the
answer follow the skill?

## Run (human path)

In any project whose `.claude/settings.json` enables `mis-skills@mis-skills`
(this repo's does), type `/mis-skills:<skill>` in Claude Code. That pulls the
plugin from GitHub `main`, so it does not show unpushed changes; use the
driver for those.

## Gotchas

- **Edits are live.** A local-path marketplace reads straight from the
  checkout ("Read from: /home/user/mis-skills/plugins/mis-skills"). Adding or
  editing a skill shows up in `install`/`list`/`invoke` without reinstalling.
- **Headless sessions can't read plugin files by default.** Without
  `--allowedTools Read`, `claude -p` is denied Read on the skill's own
  `reference.md`/`examples.md`, and the skill silently answers "from memory".
  The driver passes `--allowedTools Read Glob Grep`; keep that if you call
  `claude -p` by hand.
- **An unknown slash command is not an error.** `claude -p "/mis-skills:nope"`
  ends with `subtype: success` and a chat reply. The driver checks the folder
  exists first.
- **`claude plugin validate` misses things.** It passes a skill with no
  `name:` (falls back to the folder) and, without `--strict`, a `SKILL.md`
  with no frontmatter at all. It also passed `onetake`'s 1260-character
  description. Hence the driver's own frontmatter checks.
- **`--strict` on the marketplace fails** today on two metadata warnings (no
  marketplace description, no plugin author). The driver uses `--strict`
  only on the skills folder.
- **8 vendored HyperFrames / media-use tests fail by design.** They expect
  upstream's layout: workflow skills like `faceless-explainer` and
  `product-launch-video` that the README says are installed on demand, an
  in-repo hyperframes package version, symlinked skill dirs. They are listed
  in `known-test-failures.txt`. After an intentional change, regenerate it
  with `UPDATE_KNOWN=1 node .claude/skills/run-mis-skills/driver.mjs check`.
- **`node --test <dir>/` does not recurse here** (it reported one failing
  "test" for the directory). The driver passes the file list explicitly.
- **Several imported skills run Python from their own folder** via
  `${CLAUDE_SKILL_DIR}` (`shark.py`, `court.py`, `launch.py`, the
  `founder-*` scripts). `invoke` only allows Read/Glob/Grep, so those skills
  stop where they would run the script; smoke the scripts directly, e.g.
  `python3 -I plugins/mis-skills/skills/founder-cfo/unit_economics.py plugins/mis-skills/skills/founder-cfo/example.json --out /tmp/cfo.md`.
- **The media-use tests spawn Python** and leave `__pycache__/` in
  `media-use/audio/scripts/lib/`. The driver sets `PYTHONDONTWRITEBYTECODE=1`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `FAIL <skill>: frontmatter name is "...", must equal the folder name` | Make `name:` in `SKILL.md` match the folder; the folder name is the slash command |
| `FAIL new test failure: ...` | A bundled test broke. Run `node --test <that file>` to see it; only add it to `known-test-failures.txt` if the failure is the upstream-layout kind above |
| `FAIL not visible to the session: <skill>` | Run `install` again; check the folder has a `SKILL.md` with frontmatter |
| Invoke output says it couldn't read `examples.md`/`reference.md` | You ran `claude -p` without `--allowedTools Read` |
| `FAIL no skill folder plugins/mis-skills/skills/<name>` | Typo in the skill name; use the folder name, with or without the `mis-skills:` prefix |
