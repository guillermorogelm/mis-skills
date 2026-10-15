#!/usr/bin/env python3
"""Bookkeeping for the launch skill: launch your app the way NASA launches a rocket.

Before a NASA launch, the flight director polls every flight controller and each one answers GO or NO-GO for their
own system. One NO-GO and the countdown holds. This skill does the same for your app: 8 Claude sub-agents each check
one part of the launch and answer GO or NO-GO, then a flight director Claude writes up the holds and the fixes.

The skill's orchestrator (Claude) drives the launch with these commands. Every sub-agent reads a brief this script
writes and writes one report; this script checks the reports, counts the calls and renders the board. All state lives
in .launch/<run>/ in the current directory (the app's repo).

    python3 launch.py plan [--quick | --only a,b]
    python3 launch.py init --mission-file PATH [--quick | --only a,b | --recheck]
    python3 launch.py next
    python3 launch.py prompts <phase>
    python3 launch.py check <phase>
    python3 launch.py board
    python3 launch.py render

Phases, in order: poll, director.
"""
import argparse
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = ".launch"
LATEST = os.path.join(ROOT, "LATEST")
PHASES = ["poll", "director"]
QUICK = ["tests", "security", "database", "speed", "cost"]
WAVE = 4
CREDIT = ("_Made with [/launch](https://github.com/alexyc9381/launch-skill), a free Claude Code skill by Alex Chen "
          "([@nocodealex](https://instagram.com/nocodealex))._")
RULES = ("You may read any file in the project and run read-only commands (ls, cat, grep, git log, git diff), plus the "
         "project's own test, type-check, lint and build commands. Never edit, create, move or delete a project file, "
         "never install packages, never run a migration or a seed against a real database, never deploy, push, or call "
         "a paid API. If a check needs one of those, say so in your report instead of doing it.")


# ---------- state ----------

def load_stations():
    with open(os.path.join(HERE, "stations.json")) as f:
        return json.load(f)


def run_dir():
    if not os.path.exists(LATEST):
        sys.exit("launch: no launch yet. Run: launch.py init --mission-file .launch/mission.md")
    with open(LATEST) as f:
        return f.read().strip()


def load_state(rd=None):
    rd = rd or run_dir()
    with open(os.path.join(rd, "state.json")) as f:
        return json.load(f)


def save_state(state):
    with open(os.path.join(state["dir"], "state.json"), "w") as f:
        json.dump(state, f, indent=2)


def pick_stations(args, previous=None):
    """The stations this launch polls: all 8, --quick (the five in the video), --only a,b, or --recheck (the stations
    that said NO-GO, or gave no call, last time)."""
    stations = load_stations()
    ids = [s["id"] for s in stations]
    if getattr(args, "recheck", False):
        if not previous:
            sys.exit("launch: nothing to recheck yet. Run a full launch first.")
        want = [r["id"] for r in previous["stations"] if r["call"] != "GO"]
        if not want:
            sys.exit("launch: every station said GO last time. Nothing to recheck.")
    elif getattr(args, "only", None):
        want = [w.strip().lower() for w in args.only.split(",") if w.strip()]
        bad = [w for w in want if w not in ids]
        if bad:
            sys.exit("launch: unknown station %s (stations: %s)" % (", ".join(bad), ", ".join(ids)))
    elif getattr(args, "quick", False):
        want = QUICK
    else:
        want = ids
    return [s for s in stations if s["id"] in want]


# ---------- jobs ----------

def jobs(state, phase):
    """Each job: id, brief path, output path."""
    d = state["dir"]
    if phase == "poll":
        ids = [s["id"] for s in state["stations"]]
    elif phase == "director":
        ids = ["flight-director"]
    else:
        sys.exit("launch: unknown phase %r (phases: %s)" % (phase, ", ".join(PHASES)))
    return [{"id": jid,
             "brief": os.path.abspath(os.path.join(d, "briefs", "%s-%s.md" % (phase, jid))),
             "output": os.path.abspath(os.path.join(d, phase, "%s.md" % jid))} for jid in ids]


def done(job):
    p = job["output"]
    return os.path.exists(p) and os.path.getsize(p) > 0


def missing(state, phase):
    return [j for j in jobs(state, phase) if not done(j)]


# ---------- briefs ----------

def _abs(state, *parts):
    return os.path.abspath(os.path.join(state["dir"], *parts))


def brief_text(state, phase, job):
    mission = _abs(state, "mission.md")
    project = state["project"]
    head = ("You are one flight controller in a launch poll run by the launch skill. Before an app goes live, every "
            "controller checks one part of it and answers GO or NO-GO. One NO-GO holds the whole launch, so a GO "
            "means you would bet the launch on your part of it.\n\n"
            "You cannot see the user's conversation. Everything you know is in the mission file and the project:\n\n"
            "    mission: %s\n    project: %s\n\n"
            "%s\n\nNever invent facts, files or numbers. Every finding names its evidence (a file and line, a command "
            "and its output). Where you could not check something, say so: that is a finding too.\n\n"
            "Write your report to exactly this file and nothing else:\n\n    %s\n\n" % (mission, project, RULES,
                                                                                  job["output"]))
    if phase == "poll":
        st = next(s for s in state["stations"] if s["id"] == job["id"])
        checks = "\n".join("- " + c for c in st["checks"])
        return head + (
            "Your station: %s. You %s.\n\nWhat to check:\n\n%s\n\n"
            "Call NO-GO when: %s\n\n"
            "Call GO only if nothing in your part would hurt real users, their data or the owner's money on launch "
            "day. Smaller problems are WATCH items: they do not hold the launch, but they go in the report. Do not "
            "call NO-GO to look careful, and do not call GO to be kind: the owner is relying on this poll because "
            "the Claude that built the app graded its own work.\n\n"
            "Write exactly this, and nothing before it:\n\n"
            "STATION: %s\n"
            "CALL: GO or NO-GO\n"
            "REASON: one sentence a non-programmer understands\n"
            "FINDINGS:\n"
            "- NO-GO: <what is wrong, its evidence, and what it would do to a real user or the owner>\n"
            "- WATCH: <a smaller problem worth fixing soon, with its evidence>\n"
            "- CHECKED: <what you checked and found fine, in a few words>\n"
            "FIX: the one change that would turn this station GO (or \"none\" if GO)\n\n"
            "Keep it under 300 words. List NO-GO findings first.\n"
            % (st["name"], st["job"], checks, st["nogo"], st["name"]))
    if phase == "director":
        reports = "\n".join("    " + j["output"] for j in jobs(state, "poll"))
        return head + (
            "You are the FLIGHT DIRECTOR. The poll is in, and the call is already made by the rule: GO for launch "
            "only if every station said GO, otherwise HOLD. You cannot overrule a station. Read the mission file, "
            "every report:\n\n%s\n\nand the board in %s.\n\n"
            "Write these sections, plainly, for the person who built the app and may not be a programmer:\n\n"
            "## The holds\nEach NO-GO in one or two sentences: what is wrong and what it would do to a real user or "
            "to the owner's money, the most dangerous first.\n\n"
            "## Fix before launch\nA numbered list of the fixes, in the order to do them, each tagged with its "
            "station, each specific enough to paste into Claude as an instruction.\n\n"
            "## Watch list\nThe WATCH items worth doing in the first week after launch, at most five.\n\n"
            "## Then\nOne short paragraph: what to do after the fixes (rerun the stations that held: /launch "
            "--recheck).\n\n"
            "If every station said GO, write only a short \"## Cleared\" section and the watch list instead. 300 words "
            "at most. Do not repeat the board: it is printed above your write-up.\n"
            % (reports, _abs(state, "board.json")))
    raise ValueError(phase)


# ---------- the calls ----------

CALL_RE = re.compile(r"^\s*\**CALL\**\s*:\s*\**\s*(NO[\s-]*GO|GO)\b", re.I | re.M)
FIELD_RE = r"^\s*\**%s\**\s*:\s*(.+)$"


def parse_call(text):
    m = CALL_RE.search(text or "")
    if not m:
        return None
    call = "NO-GO" if m.group(1).upper().startswith("NO") else "GO"
    out = {"call": call}
    for key, name in (("reason", "REASON"), ("fix", "FIX")):
        f = re.search(FIELD_RE % name, text, re.I | re.M)
        out[key] = f.group(1).strip().strip("*").strip() if f else ""
    out["holds"] = len(re.findall(r"^\s*[-*]\s*\**NO[\s-]*GO\**\s*:", text, re.I | re.M))
    out["watch"] = len(re.findall(r"^\s*[-*]\s*\**WATCH\**\s*:", text, re.I | re.M))
    return out


def board(state):
    rows = []
    for j, st in zip(jobs(state, "poll"), state["stations"]):
        text = open(j["output"]).read() if done(j) else ""
        c = parse_call(text)
        rows.append({"id": st["id"], "station": st["name"], "call": c["call"] if c else "NO CALL",
                     "reason": c["reason"] if c else "", "fix": c["fix"] if c else "",
                     "holds": c["holds"] if c else 0, "watch": c["watch"] if c else 0})
    go = sum(1 for r in rows if r["call"] == "GO")
    held = len(rows) - go
    result = {"call": "GO" if held == 0 and rows else "HOLD", "go": go, "held": held, "polled": len(rows),
              "stations": rows}
    with open(os.path.join(state["dir"], "board.json"), "w") as f:
        json.dump(result, f, indent=2)
    return result


def call_line(b):
    if b["call"] == "GO":
        return "GO for launch: all %d stations say GO" % b["polled"]
    return "HOLD: %d of %d stations say NO-GO" % (b["held"], b["polled"])


def render(state):
    b = board(state)
    mission = open(os.path.join(state["dir"], "mission.md")).read().strip()
    first = mission.splitlines()[0].lstrip("# ").strip() if mission else "(empty mission)"
    fd = jobs(state, "director")[0]
    write_up = open(fd["output"]).read().strip() if done(fd) else "_The flight director has not reported yet._"
    lines = ["# %s" % call_line(b), "", "**The launch:** %s" % first, "", "## The poll", "",
             "| Station | Call | Why |", "|---|---|---|"]
    for r in b["stations"]:
        lines.append("| %s | %s | %s |" % (r["station"], r["call"], r["reason"].replace("|", "/")))
    lines += ["", write_up, "",
              "_The full poll is in %s: the mission and every station's report._" % os.path.abspath(state["dir"]),
              "", CREDIT]
    text = "\n".join(lines) + "\n"
    with open(os.path.join(state["dir"], "LAUNCH-REPORT.md"), "w") as f:
        f.write(text)
    return text


# ---------- commands ----------

def previous_board():
    try:
        with open(os.path.join(run_dir(), "board.json")) as f:
            return json.load(f)
    except (SystemExit, OSError, ValueError):
        return None


def cmd_plan(args):
    st = pick_stations(args, previous_board() if getattr(args, "recheck", False) else None)
    print("%d stations (%s) + 1 flight director = %d sub-agent calls"
          % (len(st), ", ".join(s["name"] for s in st), len(st) + 1))


def cmd_init(args):
    prev = previous_board() if args.recheck else None
    stations = pick_stations(args, prev)
    if not os.path.exists(args.mission_file):
        sys.exit("launch: mission file not found: %s" % args.mission_file)
    mission = open(args.mission_file).read().strip()
    if not mission:
        sys.exit("launch: the mission file is empty")
    base = rd = os.path.join(ROOT, time.strftime("%Y%m%d-%H%M%S"))
    k = 2
    while os.path.exists(rd):
        rd, k = "%s-%d" % (base, k), k + 1
    for sub in ("briefs", "poll", "director"):
        os.makedirs(os.path.join(rd, sub), exist_ok=True)
    with open(os.path.join(rd, "mission.md"), "w") as f:
        f.write(mission + "\n")
    state = {"dir": rd, "project": os.path.abspath("."), "stations": stations, "recheck": bool(args.recheck),
             "created": time.strftime("%Y-%m-%dT%H:%M:%S")}
    save_state(state)
    with open(LATEST, "w") as f:
        f.write(rd)
    print("launch: poll opened in %s (%d stations: %s)" % (rd, len(stations), ", ".join(s["name"] for s in stations)))
    print("next: python3 launch.py prompts poll")


def cmd_prompts(args):
    state = load_state()
    todo = missing(state, args.phase)
    if args.phase == "director":
        board(state)
    for j in jobs(state, args.phase):
        with open(j["brief"], "w") as f:
            f.write(brief_text(state, args.phase, j))
    if not todo:
        print("launch: %s is complete. Run: launch.py next" % args.phase)
        return
    for w in range(0, len(todo), WAVE):
        print("wave %d:" % (w // WAVE + 1))
        for j in todo[w:w + WAVE]:
            print("  %s  brief=%s" % (j["id"], j["brief"]))
    print("Launch one Agent call per job, one wave at a time. Prompt: "
          "\"Read <brief> and follow it exactly. It is your whole brief.\"")


def cmd_check(args):
    state = load_state()
    todo = missing(state, args.phase)
    if not todo:
        print("launch: %s complete" % args.phase)
    for j in todo:
        print("missing: %s -> %s" % (j["id"], j["output"]))


def cmd_next(args):
    state = load_state()
    for phase in PHASES:
        if missing(state, phase):
            if phase == "director":
                print("launch: the poll is in. %s." % call_line(board(state)))
            print("next phase: %s. Run: python3 launch.py prompts %s" % (phase, phase))
            return
    print("launch: the poll is complete. Run: python3 launch.py render")


def cmd_board(args):
    print(call_line(board(load_state())))


def cmd_render(args):
    sys.stdout.write(render(load_state()))


def main(argv=None):
    p = argparse.ArgumentParser(prog="launch.py")
    sub = p.add_subparsers(dest="cmd")
    for name in ("plan", "init"):
        sp = sub.add_parser(name)
        g = sp.add_mutually_exclusive_group()
        g.add_argument("--quick", action="store_true")
        g.add_argument("--only")
        g.add_argument("--recheck", action="store_true")
        if name == "init":
            sp.add_argument("--mission-file", required=True)
    for name in ("prompts", "check"):
        sp = sub.add_parser(name)
        sp.add_argument("phase", choices=PHASES)
    for name in ("next", "board", "render"):
        sub.add_parser(name)
    args = p.parse_args(argv)
    if not args.cmd:
        p.print_help()
        return 1
    {"plan": cmd_plan, "init": cmd_init, "prompts": cmd_prompts, "check": cmd_check, "next": cmd_next,
     "board": cmd_board, "render": cmd_render}[args.cmd](args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
