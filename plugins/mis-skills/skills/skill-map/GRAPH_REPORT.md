# Graph Report - skill-map  (2026-10-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 156 nodes · 699 edges · 6 communities
- Extraction: 68% EXTRACTED · 32% INFERRED · 0% AMBIGUOUS · INFERRED: 225 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output


## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5

## God Nodes (most connected - your core abstractions)
1. `plugin mis-skills` - 63 edges
2. `mis-skills:hyperframes` - 42 edges
3. `linkedin-skills:linkedin-comment-drafter` - 20 edges
4. `linkedin-skills:linkedin-post-writer` - 20 edges
5. `mis-skills:founder-cfo` - 20 edges
6. `mis-skills:founder-offer` - 20 edges
7. `mis-skills:founder-pricing` - 20 edges
8. `mis-skills:founder-consumer` - 18 edges
9. `linkedin-skills:linkedin-humanizer` - 17 edges
10. `linkedin-skills:linkedin-interviewer` - 17 edges

## Surprising Connections (you probably didn't know these)
- `founder:competitor-matrix` --step_in--> `Receta: conseguir clientes (QuitoWeb)`  [EXTRACTED]
  plugins/founder/skills/competitor-matrix/SKILL.md → tools/skill-graph/curated.json
- `founder:email-sequence` --step_in--> `Receta: conseguir clientes (QuitoWeb)`  [EXTRACTED]
  plugins/founder/skills/email-sequence/SKILL.md → tools/skill-graph/curated.json
- `founder:landing-page` --step_in--> `Receta: conseguir clientes (QuitoWeb)`  [EXTRACTED]
  plugins/founder/skills/landing-page/SKILL.md → tools/skill-graph/curated.json
- `founder:pricing-strategy` --step_in--> `Receta: conseguir clientes (QuitoWeb)`  [EXTRACTED]
  plugins/founder/skills/pricing-strategy/SKILL.md → tools/skill-graph/curated.json
- `mis-skills:content-principles` --step_in--> `Receta: video corto`  [EXTRACTED]
  plugins/mis-skills/skills/content-principles/SKILL.md → tools/skill-graph/curated.json

## Communities (6 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.18
Nodes (15): mis-skills:court, mis-skills:founder-board, mis-skills:founder-brand, mis-skills:founder-cfo, mis-skills:founder-competitors, mis-skills:founder-consumer, mis-skills:founder-launch, mis-skills:founder-marketing (+7 more)

### Community 1 - "Community 1"
Cohesion: 0.33
Nodes (30): plugin mis-skills, mis-skills:claude-animation, mis-skills:embedded-captions, mis-skills:faceless-explainer, mis-skills:figma, mis-skills:find-skills, mis-skills:gbro-collage-broll, mis-skills:general-video (+22 more)

### Community 2 - "Community 2"
Cohesion: 0.31
Nodes (15): plugin founder, founder:competitor-matrix, founder:email-sequence, founder:fundraise-prep, founder:go-to-market, founder:landing-page, founder:metrics-dashboard, founder:mvp-scope (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.39
Nodes (15): plugin linkedin-skills, linkedin-skills:linkedin-comment-drafter, linkedin-skills:linkedin-content-planner, linkedin-skills:linkedin-employee-advocacy, linkedin-skills:linkedin-engager-analytics, linkedin-skills:linkedin-hook-extractor, linkedin-skills:linkedin-humanizer, linkedin-skills:linkedin-interviewer (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.21
Nodes (19): mis-skills:art-director, mis-skills:brandkit, mis-skills:cinematic-site-prompt, mis-skills:code-reviewer, mis-skills:design-inspiration, mis-skills:design-taste-frontend, mis-skills:full-output-enforcement, mis-skills:graphicle (+11 more)

### Community 5 - "Community 5"
Cohesion: 0.46
Nodes (5): mis-skills:agency, mis-skills:content-principles, mis-skills:harvey, mis-skills:night-crew, Receta: conseguir clientes (QuitoWeb)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `mis-skills:founder-offer` connect `Community 0` to `Community 1`, `Community 5`?**
  _High betweenness centrality (0.216) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `mis-skills:hyperframes` (e.g. with `mis-skills:figma` and `mis-skills:hyperframes-animation`) actually correct?**
  _`mis-skills:hyperframes` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Why does `mis-skills:content-principles` connect `Community 5` to `Community 0`, `Community 1`, `Community 3`?**
  _High betweenness centrality (0.201) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `linkedin-skills:linkedin-comment-drafter` (e.g. with `linkedin-skills:linkedin-employee-advocacy` and `linkedin-skills:linkedin-hook-extractor`) actually correct?**
  _`linkedin-skills:linkedin-comment-drafter` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Why does `founder:pricing-strategy` connect `Community 2` to `Community 0`, `Community 5`?**
  _High betweenness centrality (0.090) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `linkedin-skills:linkedin-post-writer` (e.g. with `linkedin-skills:linkedin-hook-extractor` and `linkedin-skills:linkedin-interviewer`) actually correct?**
  _`linkedin-skills:linkedin-post-writer` has 4 INFERRED edges - model-reasoned connections that need verification._