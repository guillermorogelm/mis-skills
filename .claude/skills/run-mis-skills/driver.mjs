#!/usr/bin/env node
// Driver for the mis-skills marketplace: validate it, install it into an
// isolated Claude Code config, and run a skill headlessly.
//
//   node .claude/skills/run-mis-skills/driver.mjs check
//   node .claude/skills/run-mis-skills/driver.mjs install
//   node .claude/skills/run-mis-skills/driver.mjs list
//   node .claude/skills/run-mis-skills/driver.mjs invoke <skill> [args...]
//   node .claude/skills/run-mis-skills/driver.mjs all
//
// Run from the repo root. Nothing touches your real ~/.claude: install,
// list and invoke use CLAUDE_CONFIG_DIR=$MIS_SKILLS_SANDBOX (default
// /tmp/mis-skills-sandbox).

import { spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(HERE, '../../..');
const SKILLS = join(ROOT, 'plugins/mis-skills/skills');
const SANDBOX = process.env.MIS_SKILLS_SANDBOX || '/tmp/mis-skills-sandbox';
const CFG = join(SANDBOX, 'config');
const CWD = join(SANDBOX, 'cwd');
const KNOWN_FAILURES = join(HERE, 'known-test-failures.txt');

let failed = false;
const ok = (m) => console.log(`  ok   ${m}`);
const bad = (m) => { failed = true; console.log(`  FAIL ${m}`); };
const warn = (m) => console.log(`  warn ${m}`);

function run(cmd, args, opts = {}) {
  return spawnSync(cmd, args, { encoding: 'utf8', maxBuffer: 64 << 20, ...opts });
}

function sandboxEnv() {
  mkdirSync(CFG, { recursive: true });
  mkdirSync(CWD, { recursive: true });
  return { ...process.env, CLAUDE_CONFIG_DIR: CFG };
}

// ---------- check ----------

function frontmatter(text) {
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return null;
  const fm = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (kv) fm[kv[1]] = kv[2].replace(/^["']|["']$/g, '');
  }
  return fm;
}

function checkManifests() {
  console.log('\n# claude plugin validate');
  for (const [target, strict] of [['.', false], ['plugins/mis-skills', false], ['plugins/mis-skills/skills', true]]) {
    const args = ['plugin', 'validate', ...(strict ? ['--strict'] : []), target];
    const r = run('claude', args, { cwd: ROOT });
    const label = `claude ${args.join(' ')}`;
    if (r.status === 0) ok(label);
    else { bad(label); console.log((r.stdout + r.stderr).trim().replace(/^/gm, '       ')); }
  }
}

function checkSkills() {
  console.log('\n# SKILL.md frontmatter and README');
  const readme = readFileSync(join(ROOT, 'README.md'), 'utf8');
  const dirs = readdirSync(SKILLS, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name);
  for (const dir of dirs) {
    const file = join(SKILLS, dir, 'SKILL.md');
    if (!existsSync(file)) { bad(`${dir}: no SKILL.md`); continue; }
    const fm = frontmatter(readFileSync(file, 'utf8'));
    if (!fm) { bad(`${dir}: no frontmatter`); continue; }
    if (fm.name !== dir) bad(`${dir}: frontmatter name is "${fm.name ?? ''}", must equal the folder name`);
    if (!fm.description) bad(`${dir}: empty description`);
    else if (fm.description.length > 1024) warn(`${dir}: description is ${fm.description.length} chars (over 1024)`);
    if (!readme.includes(`\`${dir}\``)) warn(`${dir}: not mentioned in README.md`);
  }
  ok(`${dirs.length} skill folders scanned`);
}

function checkTests() {
  console.log('\n# bundled node tests');
  const files = [];
  const walk = (d) => {
    for (const e of readdirSync(d, { withFileTypes: true })) {
      if (e.name === 'node_modules') continue;
      const p = join(d, e.name);
      if (e.isDirectory()) walk(p);
      else if (e.name.endsWith('.test.mjs')) files.push(p);
    }
  };
  walk(SKILLS);
  const r = run(process.execPath, ['--test', '--test-reporter=tap', ...files], {
    cwd: ROOT,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: '1' },
  });
  const out = r.stdout + r.stderr;
  const failing = [...out.matchAll(/^not ok \d+ - (.+)$/gm)].map((m) => m[1].trim());
  const total = out.match(/^# tests (\d+)/m)?.[1] ?? '?';
  const known = new Set(
    readFileSync(KNOWN_FAILURES, 'utf8').split('\n').map((l) => l.trim()).filter((l) => l && !l.startsWith('#')),
  );
  const unique = [...new Set(failing)];
  const fresh = unique.filter((t) => !known.has(t));
  ok(`${files.length} files, ${total} tests, ${unique.length} distinct failing names (${unique.length - fresh.length} known)`);
  for (const t of fresh) bad(`new test failure: ${t}`);
  if (process.env.UPDATE_KNOWN === '1') {
    writeFileSync(KNOWN_FAILURES, '# Vendored tests that fail in this repo layout (see SKILL.md).\n' + unique.join('\n') + '\n');
    console.log(`  wrote ${relative(ROOT, KNOWN_FAILURES)}`);
  }
}

// ---------- install / list / invoke ----------

function install() {
  console.log(`\n# install into sandbox ${SANDBOX}`);
  const env = sandboxEnv();
  const listed = run('claude', ['plugin', 'marketplace', 'list'], { env, cwd: CWD });
  if (!listed.stdout.includes('mis-skills')) {
    const r = run('claude', ['plugin', 'marketplace', 'add', ROOT], { env, cwd: CWD });
    if (r.status !== 0) return bad('marketplace add\n' + r.stdout + r.stderr);
  }
  const r = run('claude', ['plugin', 'install', 'mis-skills@mis-skills'], { env, cwd: CWD });
  if (r.status !== 0) return bad('plugin install\n' + r.stdout + r.stderr);
  const d = run('claude', ['plugin', 'details', 'mis-skills@mis-skills'], { env, cwd: CWD });
  const skills = d.stdout.match(/Skills \((\d+)\)/)?.[1];
  const cost = d.stdout.match(/Always-on:\s+(\S+ tok)/)?.[1];
  ok(`installed mis-skills@mis-skills from ${ROOT}: ${skills} skills, always-on ${cost}`);
}

function headless(prompt, maxTurns) {
  const env = sandboxEnv();
  const r = run('claude', [
    '-p', prompt,
    '--allowedTools', 'Read', 'Glob', 'Grep',
    '--output-format', 'stream-json', '--verbose',
    '--max-turns', String(maxTurns),
  ], { env, cwd: CWD, timeout: 600_000 });
  const events = r.stdout.trim().split('\n').flatMap((l) => { try { return [JSON.parse(l)]; } catch { return []; } });
  return { status: r.status, stderr: r.stderr, events };
}

function list() {
  console.log('\n# skills a headless session sees');
  const { events } = headless("Reply with only a comma-separated list of the skill names you have available whose names start with 'mis-skills:'. Nothing else.", 1);
  const result = events.find((e) => e.type === 'result');
  if (!result || result.subtype !== 'success') return bad('headless session did not finish');
  const seen = result.result.match(/mis-skills:[a-z0-9-]+/g) ?? [];
  const onDisk = readdirSync(SKILLS, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name);
  const missing = onDisk.filter((s) => !seen.includes(`mis-skills:${s}`));
  if (missing.length) bad(`not visible to the session: ${missing.join(', ')}`);
  else ok(`all ${onDisk.length} skills visible as mis-skills:<name>`);
}

function invoke(skill, args) {
  if (!skill) { console.error('usage: driver.mjs invoke <skill> [args...]'); process.exit(2); }
  const name = skill.replace(/^mis-skills:/, '');
  console.log(`\n# /mis-skills:${name} ${args}`);
  // An unknown slash command still ends in a "success" result, so check the folder first.
  if (!existsSync(join(SKILLS, name, 'SKILL.md'))) return bad(`no skill folder plugins/mis-skills/skills/${name}`);
  const { events, stderr } = headless(`/mis-skills:${name} ${args}`.trim(), 8);
  for (const e of events) {
    if (e.type === 'assistant') {
      for (const c of e.message.content) {
        if (c.type === 'tool_use') console.log(`  tool ${c.name} ${JSON.stringify(c.input).slice(0, 160)}`);
      }
    }
    if (e.type === 'user' && Array.isArray(e.message.content)) {
      for (const c of e.message.content) {
        if (c.type === 'tool_result' && c.is_error) bad(`tool error: ${JSON.stringify(c.content).slice(0, 200)}`);
      }
    }
  }
  const result = events.find((e) => e.type === 'result');
  if (!result) { bad('no result event'); console.log(stderr.slice(-2000)); return; }
  console.log(`  result ${result.subtype}, ${result.num_turns} turns\n`);
  console.log(result.result ?? '');
  const out = join(SANDBOX, `invoke-${name}.md`);
  writeFileSync(out, result.result ?? '');
  console.log(`\n  saved ${out}`);
  if (result.subtype !== 'success') bad(`session ended with ${result.subtype}`);
}

// ---------- main ----------

const [cmd = 'check', ...rest] = process.argv.slice(2);
switch (cmd) {
  case 'check': checkManifests(); checkSkills(); checkTests(); break;
  case 'install': install(); break;
  case 'list': list(); break;
  case 'invoke': invoke(rest[0], rest.slice(1).join(' ')); break;
  case 'all': checkManifests(); checkSkills(); checkTests(); install(); list(); break;
  default: console.error(`unknown command ${cmd}`); process.exit(2);
}
console.log(failed ? '\nFAILED' : '\nOK');
process.exit(failed ? 1 : 0);
