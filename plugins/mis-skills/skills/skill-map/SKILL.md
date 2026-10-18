---
name: skill-map
description: The map of how every skill in the mis-skills, founder and linkedin-skills plugins connects - which files each one reads and writes, which runs next, which are alternatives, what each needs, and step-by-step recipes - as a Graphicle graph plus a readable map. Use before choosing or chaining skills, when asked which skill to use, how to combine skills, what to run next, what a skill reads or writes, "qué skill uso", "cómo combino", or when one skill's output should feed another.
---

# Skill map

Two graphs of these plugins, built with Graphicle, live next to this file
(`${CLAUDE_SKILL_DIR}`; if that looks unexpanded, use the "Base directory for
this skill" Claude Code printed above):

| File | What it is |
|---|---|
| `map.md` | The skill graph as text: recipes, shared files, requirements, and every skill's connections. **Read this first.** |
| `graph.json` | The same skill graph in Graphicle's format, for queries |
| `graph.html` | Interactive view; open it in a browser |
| `GRAPH_REPORT.md` | Graphicle's report: communities and hub skills |
| `code-graph.json` | Graphicle's code graph of every script inside the skills (functions, calls, imports) |

## How to use it

1. **Choosing or combining skills:** read `map.md`. Find the recipe that
   matches the goal, or the skill's entry, and follow its `siguiente`
   (next), `lee` (reads) and `escribe` (writes) lines. Tell the user the
   chain you picked and why, in one or two lines, then run the first step.
2. **Feeding one skill's output into another:** look up the file under
   "Archivos que comparten". Skills from different sets do not read each
   other's files on their own: name the file in the request ("use
   `founder/competitors.md` as the source").
3. **Precise questions**, if `graphicle-graph` is installed (see the
   `graphicle` skill):

```bash
G="${CLAUDE_SKILL_DIR}/graph.json"
graphicle-graph query "pricing" --graph "$G"                         # skills and files around a topic
graphicle-graph explain "mis-skills:founder-offer" --graph "$G"      # one skill's connections
graphicle-graph path "mis-skills:court" "mis-skills:founder-plan" --graph "$G"   # a chain from A to B
graphicle-graph explain "founder/competitors.md" --graph "$G"        # who writes and who reads a file
graphicle-graph affected "mis-skills:founder-cfo" --relation next --graph "$G"  # what leads into a skill
graphicle-graph god-nodes --graph "$G"                               # hub skills
graphicle-graph query "media-use" --graph "${CLAUDE_SKILL_DIR}/code-graph.json"  # script-level links
```

`affected` follows code relations unless `--relation` names one (`next`,
`reads`, `writes`…). Without Graphicle, read `map.md`, or open `graph.json`
and filter `links` by `source`, `target` and `relation`.

## Reading the graph

- Node `kind`: `skill`, `artifact` (a file skills share), `recipe`,
  `requirement`, `plugin` (`file_type` is Graphicle's own: `concept` or
  `document`). Skill labels are `plugin:name`; invoke them as
  `/plugin:name`.
- Link `relation`: `reads` (file to skill), `writes`, `next`, `routes_to`
  (the HyperFrames router picking a workflow), `runs_script_of`,
  `alternative_to`, `complements`, `requires`, `step_in` (skill to recipe,
  with `step`), `mentions`, `part_of`. A link may list more relations in
  `also`.
- `confidence`: `EXTRACTED` came from a SKILL.md line (see
  `source_file` and `source_location`) or from the curated recipes;
  `INFERRED` is a mention or a keyword match (requirements). Verify an INFERRED link in the SKILL.md
  before relying on it.

The graph describes the skills as they were when it was built. If a
SKILL.md says otherwise, the SKILL.md wins.

Rebuilt in the mis-skills repo with `python3 -I tools/skill-graph/build.py`
(needs `graphicle-graph` on PATH for the clustering, `graph.html` and
`code-graph.json`).
