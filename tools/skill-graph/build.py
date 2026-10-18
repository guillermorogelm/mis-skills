#!/usr/bin/env python3
"""Build the skill graphs that ship inside the skill-map skill.

    python3 -I tools/skill-graph/build.py           # rebuild everything
    python3 -I tools/skill-graph/build.py --check   # fail if graph.json is stale

Outputs, in plugins/mis-skills/skills/skill-map/:
  graph.json       how the skills connect (Graphicle node-link format)
  map.md           the same graph as readable text
  graph.html       interactive view (needs graphicle-graph on PATH)
  GRAPH_REPORT.md  Graphicle's community report (needs graphicle-graph)
  code-graph.json  Graphicle code graph of every script in the plugins (needs graphicle-graph)

The graph has two layers. Extracted: read from each SKILL.md (files a skill
reads and writes, "Next:" lines, skills it names, scripts of other skills it
runs, what it needs). Curated: tools/skill-graph/curated.json (recipes,
alternatives, complements).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
OUT = os.path.join(ROOT, 'plugins', 'mis-skills', 'skills', 'skill-map')
CURATED = os.path.join(HERE, 'curated.json')

# Relation priority when two relations join the same pair: the first wins,
# the others are kept in the link's "also" list.
PRIORITY = ['next', 'routes_to', 'runs_script_of', 'writes', 'reads', 'step_in',
            'alternative_to', 'complements', 'requires', 'mentions', 'part_of']

REQUIREMENTS = [
    ('req_publora', 'Clave o conector de Publora', r'publora'),
    ('req_apify', 'Clave de Apify', r'apify'),
    ('req_pixfaro', 'Clave de Pixfaro', r'pixfaro'),
    ('req_gemini', 'Clave de Gemini', r'gemini_api_key|google-genai|gemini api key'),
    ('req_python', 'Python 3', r'\bpython3?\b'),
    ('req_ffmpeg', 'ffmpeg', r'\bffmpeg\b'),
    ('req_node', 'Node.js', r'\bnpx\b|\bnpm\b|node\.js|\bnode [\w${}./"-]+\.m?js\b'),
    ('req_chrome', 'Chrome / Chromium', r'\b(chromium|puppeteer|playwright|headless chrome)\b'),
    ('req_claude_plan', 'Plan Claude Pro o Max', r'\bpro,? (or|o) max\b|\bpro/max\b|pro, max'),
]

# Artifacts outside founder/ and references/ that a skill creates.
EXTRA_ARTIFACTS = [
    ('mis-skills:night-crew', 'NIGHT-CREW.md', 'writes'),
    ('mis-skills:harvey', '~/harvey', 'writes'),
    ('mis-skills:graphicle', '.graphicle/', 'writes'),
    ('mis-skills:graphicle', '.mcp.json', 'writes'),
    ('mis-skills:cinematic-site-prompt', '<sitio>-cinematic-prompt.md', 'writes'),
]

WRITE_BEFORE = r'(?:\bwrites?\b|\bsaves?\b|--out\b|\bcreates?\b|\bappends?(?: to)?\b|\bfills\b|\bupdate\b|\bre-?writes?\b)'
READ_WORDS = re.compile(r'\b(read|reads|from|load|loads|uses|if)\b', re.I)
FOUNDER_PATH = r'founder/[A-Za-z0-9_./*<>-]*?(?:\.md|\.json|\.csv|/)'


def written_here(line, start):
    """True when a write verb sits at most four words before the path at `start`."""
    before = line[:start]
    return bool(re.search(WRITE_BEFORE + r'\W+(?:[^\s]+\s+){0,4}[`(]*$', before, re.I))


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')


def slug(s):
    return re.sub(r'[^a-z0-9]+', '_', s.lower()).strip('_')


def frontmatter(text):
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.S)
    if not m:
        return {}
    fm, key = {}, None
    for line in m.group(1).split('\n'):
        k = re.match(r'^([A-Za-z_-]+):\s*(.*)$', line)
        if k:
            key, val = k.group(1), k.group(2).strip()
            if val in ('>-', '>', '|', '|-'):
                val = ''
            elif len(val) > 1 and val[0] == "'" and val[-1] == "'":
                val = val[1:-1].replace("''", "'")
            elif len(val) > 1 and val[0] == '"' and val[-1] == '"':
                val = val[1:-1].replace('\\"', '"')
            fm[key] = val
        elif key and line.strip():
            fm[key] = (fm[key] + ' ' + line.strip()).strip()
    return fm


def summary(desc, n=220):
    desc = re.sub(r'\s+', ' ', desc).strip()
    first = re.split(r'(?<=[.!?])\s', desc, maxsplit=1)[0]
    return first if len(first) <= n else first[: n - 1].rstrip() + '…'


class Graph:
    def __init__(self):
        self.nodes, self.links = {}, {}

    def node(self, nid, label, kind, source_file=None, **extra):
        # Graphicle only knows a few file types; the skill-map kind goes in "kind".
        # It also shortens labels that end in "/" to their last segment, so
        # folders are labelled "dir/*".
        if label.endswith('/'):
            label += '*'
        if nid not in self.nodes:
            self.nodes[nid] = {'id': nid, 'label': label, 'norm_label': label.lower(), 'kind': kind,
                               'file_type': 'document' if kind == 'artifact' else 'concept',
                               'source_file': source_file or '', '_origin': 'skill-map', **extra}
        return nid

    def link(self, s, t, relation, confidence, source_file, line=None, **extra):
        if s == t:
            return
        key = (s, t)
        new = {'source': s, 'target': t, 'relation': relation, 'confidence': confidence,
               'confidence_score': 1.0 if confidence == 'EXTRACTED' else 0.6,
               'source_file': source_file, 'source_location': f'L{line}' if line else '',
               'weight': 1.0, '_origin': 'skill-map', **extra}
        old = self.links.get(key)
        if old is None:
            self.links[key] = new
            return
        rels = [old['relation']] + old.get('also', [])
        if relation in rels:
            return
        if PRIORITY.index(relation) < PRIORITY.index(old['relation']):
            new['also'] = sorted(set(rels))
            self.links[key] = new
        else:
            old['also'] = sorted(set(old.get('also', []) + [relation]))

    def dump(self):
        return {
            'directed': True, 'multigraph': False,
            'graph': {'schema_version': 1, 'graphicle_version': 'skill-map',
                      'name': 'mis-skills: how the skills connect'},
            'nodes': [self.nodes[k] for k in sorted(self.nodes)],
            'links': [self.links[k] for k in sorted(self.links)],
            'hyperedges': [],
        }


def load_skills():
    market = json.load(open(os.path.join(ROOT, '.claude-plugin', 'marketplace.json')))
    skills = {}
    for p in market['plugins']:
        sdir = os.path.join(ROOT, p['source'], 'skills')
        for name in sorted(os.listdir(sdir)):
            path = os.path.join(sdir, name, 'SKILL.md')
            if not os.path.isfile(path):
                continue
            text = open(path, encoding='utf-8').read()
            fm = frontmatter(text)
            skills[f"{p['name']}:{name}"] = {
                'plugin': p['name'], 'name': name, 'dir': os.path.dirname(path),
                'path': path, 'text': text, 'desc': fm.get('description', ''),
            }
    return market['plugins'], skills


def skill_id(sid):
    return 'skill_' + slug(sid)


def file_id(path):
    return 'file_' + slug(path)


def resolve(token, here, skills):
    """Map a mention like '/founder:pricing-strategy' or 'founder-offer' to a skill id."""
    token = token.strip().lstrip('/')
    m = re.match(r'^(?:(mis-skills|founder|linkedin-skills):)?([a-z][a-z0-9-]*)$', token)
    if not m:
        return None
    plugin, name = m.group(1), m.group(2)
    if plugin:
        sid = f'{plugin}:{name}'
        return sid if sid in skills else None
    same = f"{skills[here]['plugin']}:{name}"
    if same in skills:
        return same
    hits = [s for s in skills if s.endswith(':' + name)]
    return hits[0] if len(hits) == 1 else None


def extract(g, skills):
    for sid, sk in skills.items():
        if sid == 'mis-skills:skill-map':
            continue  # the map itself
        src = rel(sk['path'])
        lines = sk['text'].split('\n')
        me = skill_id(sid)
        in_output = in_next = False
        for i, line in enumerate(lines, 1):
            if line.startswith('#'):
                in_output = bool(re.search(r'\b(output|outputs|salida)\b', line, re.I))
                in_next = False
            if not line.strip():
                in_next = False
            if re.search(r'\bnext\b', line, re.I):
                in_next = True
            tokens = re.findall(r'`([^`\n]{2,60})`', line) + re.findall(r'(?<![\w`/.-])(/(?:[a-z-]+:)?[a-z][a-z0-9-]+)', line)
            for tok in tokens:
                tok = tok.split()[0] if tok.split() else tok
                plain = tok.lstrip('/')
                if ':' not in plain and '-' not in plain and not tok.startswith('/'):
                    continue  # one-word names ("launch", "court") only count as /commands
                other = resolve(tok, sid, skills)
                if not other or other == sid:
                    continue
                relation = 'next' if in_next else 'mentions'
                g.link(me, skill_id(other), relation, 'EXTRACTED' if relation == 'next' else 'INFERRED', src, i)
            # Runs another skill's script.
            for other in re.findall(r'\$\{CLAUDE_SKILL_DIR\}/\.\./([a-z0-9-]+)/', line):
                o = f"{sk['plugin']}:{other}"
                if o in skills:
                    g.link(me, skill_id(o), 'runs_script_of', 'EXTRACTED', src, i)
            # founder/ files.
            for m in re.finditer(FOUNDER_PATH, line):
                path = m.group(0)
                if sk['plugin'] == 'founder':
                    continue  # handled from the Reads line and the shared rules below
                fid = g.node(file_id(path), path, 'artifact', path)
                if in_output or written_here(line, m.start()):
                    g.link(me, fid, 'writes', 'EXTRACTED', src, i)
                else:
                    g.link(fid, me, 'reads', 'EXTRACTED' if READ_WORDS.search(line) else 'INFERRED', src, i)
            # LinkedIn shared references.
            for m in re.finditer(r'\.\./\.\./references/([a-z0-9-]+\.md)', line):
                path = f'linkedin-skills/references/{m.group(1)}'
                fid = g.node(file_id(path), path, 'artifact', f'plugins/{path}')
                if written_here(line, m.start()):
                    g.link(me, fid, 'writes', 'EXTRACTED', src, i)
                else:
                    g.link(fid, me, 'reads', 'EXTRACTED', src, i)
        # Requirements.
        low = sk['text'].lower()
        for rid, label, pattern in REQUIREMENTS:
            m = re.search(pattern, low)
            if m:
                g.node(rid, label, 'requirement')
                g.link(me, rid, 'requires', 'INFERRED', src, low[: m.start()].count('\n') + 1)  # keyword match
        # Sub-skill files of linkedin-humanizer (voice profile builder).
        if sid == 'linkedin-skills:linkedin-humanizer':
            vp = g.node(file_id('linkedin-skills/references/voice-profile.md'), 'linkedin-skills/references/voice-profile.md',
                        'artifact', 'plugins/linkedin-skills/references/voice-profile.md')
            line = next((i for i, l in enumerate(lines, 1) if 'sub-skills/voice-profile.md' in l), None)
            g.link(me, vp, 'writes', 'EXTRACTED', src, line)

    # Emotix founder plugin: explicit Reads lines and the shared rules file.
    rules = 'plugins/founder/shared/conventions.md'
    for sid, sk in skills.items():
        if sk['plugin'] != 'founder':
            continue
        me, src = skill_id(sid), rel(sk['path'])
        for i, line in enumerate(sk['text'].split('\n'), 1):
            if line.strip().startswith('- Reads:'):
                for path in re.findall(r'`(founder/[^`]+)`', line):
                    g.link(g.node(file_id(path), path, 'artifact', path), me, 'reads', 'EXTRACTED', src, i)
        out = f"founder/{sk['name']}.md"
        g.link(me, g.node(file_id(out), out, 'artifact', out), 'writes', 'EXTRACTED', rules)
        g.link(me, g.node(file_id('founder/facts.md'), 'founder/facts.md', 'artifact', 'founder/facts.md'),
               'writes', 'EXTRACTED', rules)

    # HyperFrames router.
    hf = 'mis-skills:hyperframes'
    if hf in skills:
        routes = os.path.join(skills[hf]['dir'], 'references', 'routes')
        for f in sorted(os.listdir(routes)):
            w = f'mis-skills:{f[:-3]}'
            if f.endswith('.md') and w in skills:
                g.link(skill_id(hf), skill_id(w), 'routes_to', 'EXTRACTED', rel(os.path.join(routes, f)))

    for sid, path, relation in EXTRA_ARTIFACTS:
        if sid not in skills:
            continue
        line = next((i for i, l in enumerate(skills[sid]['text'].split('\n'), 1) if path.strip('<>') in l), None)
        g.link(skill_id(sid), g.node(file_id(path), path, 'artifact', path), relation, 'EXTRACTED', rel(skills[sid]['path']), line)


def curated(g, skills):
    data = json.load(open(CURATED, encoding='utf-8'))
    src = rel(CURATED)

    def need(sid):
        if sid not in skills:
            sys.exit(f'curated.json names unknown skill {sid}')
        return skill_id(sid)

    for r in data['recipes']:
        rid = g.node('recipe_' + slug(r['id']), r['label'], 'recipe', src, recipe=r['id'],
                     steps=[[s for s in step] for step in r['steps']])
        for n, step in enumerate(r['steps'], 1):
            for sid in step:
                g.link(need(sid), rid, 'step_in', 'EXTRACTED', src, step=n)
        for a, b in zip(r['steps'], r['steps'][1:]):
            for x in a:
                for y in b:
                    g.link(need(x), need(y), 'next', 'EXTRACTED', src, context=r['id'])
    for alt in data['alternatives']:
        for x in alt['skills']:
            for y in alt['skills']:
                if x < y:
                    g.link(need(x), need(y), 'alternative_to', 'EXTRACTED', src, note=alt['note'])
    for c in data['complements']:
        for y in c['to']:
            g.link(need(c['from']), need(y), 'complements', 'EXTRACTED', src, note=c['note'])
    return data


def build():
    plugins, skills = load_skills()
    g = Graph()
    for p in plugins:
        g.node('plugin_' + slug(p['name']), f"plugin {p['name']}", 'plugin', p['source'].lstrip('./') + '/.claude-plugin/plugin.json',
               invoke=f"/{p['name']}:<skill>")
    for sid, sk in skills.items():
        g.node(skill_id(sid), sid, 'skill', rel(sk['path']), plugin=sk['plugin'], name=sk['name'],
               invoke=f'/{sid}', summary=summary(sk['desc']))
        g.link(skill_id(sid), 'plugin_' + slug(sk['plugin']), 'part_of', 'EXTRACTED', rel(sk['path']))
    extract(g, skills)
    data = curated(g, skills)
    return g, skills, data


def signature(graph):
    """Labels and labelled edges: stable across Graphicle's id rewrite."""
    label = {n['id']: n['label'] for n in graph['nodes']}
    return (sorted(label.values()),
            sorted((label[l['source']], label[l['target']], l['relation']) for l in graph['links']))


# ---------- map.md ----------

def write_map(graph, skills, data):
    nodes = {n['id']: n for n in graph['nodes']}
    out_links, in_links = {}, {}
    for l in graph['links']:
        out_links.setdefault(l['source'], []).append(l)
        in_links.setdefault(l['target'], []).append(l)

    def lab(nid):
        return nodes[nid]['label']

    def names(ls, side, relation):
        seen = []
        for l in ls:
            if l['relation'] == relation or relation in l.get('also', []):
                v = lab(l[side])
                if v not in seen:
                    seen.append(v)
        return seen

    L = ['# Mapa de skills', '',
         'Generado por `tools/skill-graph/build.py` desde los `SKILL.md` y `tools/skill-graph/curated.json`. No lo edites a mano.', '',
         f"{sum(1 for n in graph['nodes'] if n['kind'] == 'skill')} skills, "
         f"{sum(1 for n in graph['nodes'] if n['kind'] == 'artifact')} archivos compartidos, "
         f"{len(graph['links'])} conexiones. El mismo grafo, para Graphicle: `graph.json`.", '',
         'Relaciones: **lee** / **escribe** (archivos), **siguiente** (paso que sigue), **enruta a** (elige un flujo), '
         '**usa el script de**, **alternativa a**, **complementa**, **necesita**, **menciona**.', '',
         '## Recetas', '']
    for r in data['recipes']:
        L.append(f"### {r['label']}")
        for n, step in enumerate(r['steps'], 1):
            L.append(f"{n}. " + ' o '.join(f'`/{s}`' for s in step))
        if r.get('source'):
            L.append(f"\n<sub>Orden: {r['source']}</sub>")
        L.append('')
        L.append('```mermaid')
        L.append('flowchart LR')
        for n, step in enumerate(r['steps'], 1):
            ids = [f's{n}_{i}' for i in range(len(step))]
            for i, s in zip(ids, step):
                L.append(f'  {i}["{s}"]')
            if n > 1:
                L.append(f"  {' & '.join(prev)} --> {' & '.join(ids)}")
            prev = ids
        L.append('```')
        L.append('')

    L += ['## Archivos que comparten', '', '| Archivo | Lo escriben | Lo leen |', '|---|---|---|']
    for nid in sorted(n for n in nodes if nodes[n]['kind'] == 'artifact'):
        w = names(in_links.get(nid, []), 'source', 'writes')
        r = names(out_links.get(nid, []), 'target', 'reads')
        L.append(f"| `{lab(nid)}` | {', '.join(f'`{x}`' for x in w) or '-'} | {', '.join(f'`{x}`' for x in r) or '-'} |")
    L.append('')

    L += ['## Requisitos', '', 'Detectados por palabra clave en cada SKILL.md (enlaces INFERRED): confírmalos en la skill antes de pedirle algo al usuario.', '',
          '| Necesita | Skills |', '|---|---|']
    for nid in sorted(n for n in nodes if nodes[n]['kind'] == 'requirement'):
        L.append(f"| {lab(nid)} | {', '.join(f'`{x}`' for x in names(in_links.get(nid, []), 'source', 'requires'))} |")
    L.append('')

    L.append('## Cada skill')
    for plugin in ['mis-skills', 'founder', 'linkedin-skills']:
        L += ['', f'### Plugin `{plugin}`', '']
        for sid in sorted(s for s in skills if skills[s]['plugin'] == plugin):
            nid = skill_id(sid)
            n = nodes[nid]
            o, i = out_links.get(nid, []), in_links.get(nid, [])
            parts = []
            for title, side, relation, ls in [
                ('lee', 'source', 'reads', i), ('escribe', 'target', 'writes', o),
                ('siguiente', 'target', 'next', o), ('viene después de', 'source', 'next', i),
                ('enruta a', 'target', 'routes_to', o), ('usa el script de', 'target', 'runs_script_of', o),
                ('complementa', 'target', 'complements', o), ('la complementan', 'source', 'complements', i),
                ('necesita', 'target', 'requires', o), ('menciona', 'target', 'mentions', o)]:
                v = names(ls, side, relation)
                if v:
                    parts.append(f"{title}: " + ', '.join(f'`{x}`' for x in v[:12]) + (' …' if len(v) > 12 else ''))
            alts = names(o, 'target', 'alternative_to') + names(i, 'source', 'alternative_to')
            if alts:
                parts.append('alternativas: ' + ', '.join(f'`{x}`' for x in alts))
            recipes = [lab(l['target']) for l in o if l['relation'] == 'step_in' or 'step_in' in l.get('also', [])]
            if recipes:
                parts.append('en: ' + '; '.join(r.replace('Receta: ', '') for r in recipes))
            L.append(f"- **`/{sid}`** {n['summary']}")
            for p in parts:
                L.append(f'  - {p}')
    open(os.path.join(OUT, 'map.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')


# ---------- Graphicle ----------

def graphicle(env):
    exe = shutil.which('graphicle-graph')
    if not exe:
        print('graphicle-graph not on PATH: skipped clustering, graph.html and code-graph.json')
        return
    gpath = os.path.join(OUT, 'graph.json')
    work = os.path.join(OUT, '.graphicle')
    # cluster-only writes the clustered graph and its report under .graphicle/;
    # keep those two files next to SKILL.md and drop the working folder.
    subprocess.run([exe, 'cluster-only', OUT, '--graph', gpath, '--no-label', '--no-viz'], check=True, env=env,
                   stdout=subprocess.DEVNULL)
    clustered = json.load(open(os.path.join(work, 'graph.json'), encoding='utf-8'))
    clustered.pop('built_at_commit', None)
    json.dump(clustered, open(gpath, 'w', encoding='utf-8'), indent=1, ensure_ascii=False, sort_keys=True)
    report = open(os.path.join(work, 'GRAPH_REPORT.md'), encoding='utf-8').read()
    report = re.sub(r'## Graph Freshness.*?(?=\n## )', '', report, flags=re.S)  # commit-specific, goes stale
    open(os.path.join(OUT, 'GRAPH_REPORT.md'), 'w', encoding='utf-8').write(report)
    shutil.rmtree(work)
    subprocess.run([exe, 'export', 'html', '--graph', gpath, '--output', os.path.join(OUT, 'graph.html')], check=True, env=env,
                   stdout=subprocess.DEVNULL)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run([exe, 'extract', os.path.join(ROOT, 'plugins'), '--code-only', '--out', tmp],
                       check=True, env=env, stdout=subprocess.DEVNULL)
        code = json.load(open(os.path.join(tmp, '.graphicle', 'graph.json')))
        code.setdefault('graph', {})['name'] = 'mis-skills: code graph of the scripts inside every skill (paths relative to plugins/)'
        json.dump(code, open(os.path.join(OUT, 'code-graph.json'), 'w'), separators=(',', ':'), sort_keys=True)


def main():
    g, skills, data = build()
    graph = g.dump()
    gpath = os.path.join(OUT, 'graph.json')
    if '--check' in sys.argv:
        try:
            old = json.load(open(gpath))
        except FileNotFoundError:
            sys.exit('skill-map/graph.json is missing: run python3 -I tools/skill-graph/build.py')
        if signature(old) != signature(graph):
            sys.exit('skill-map/graph.json is stale: run python3 -I tools/skill-graph/build.py')
        print(f"skill graph up to date: {len(graph['nodes'])} nodes, {len(graph['links'])} links")
        return
    os.makedirs(OUT, exist_ok=True)
    json.dump(graph, open(gpath, 'w', encoding='utf-8'), indent=1, ensure_ascii=False, sort_keys=True)
    write_map(graph, skills, data)
    env = {**os.environ, 'GRAPHICLE_NO_UPDATE_NOTIFIER': '1'}
    graphicle(env)
    print(f"wrote {rel(OUT)}: {len(graph['nodes'])} nodes, {len(graph['links'])} links")


if __name__ == '__main__':
    main()
