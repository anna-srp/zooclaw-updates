# ecap-agent-pack - 2026-05-14 Commits
共 2 条 commit

---
## [1] b3a174d6
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T12:15:13Z
- **SHA**: b3a174d62aa5ad1574497efe0fe3610d25b2cfd5
- **PR**: #123

### Commit Message

```
docs: add top-level AGENTS.md with link to ecap-workspace architecture guide (#123)

The repo top level had no AGENTS.md or CLAUDE.md (just an 18-byte
README). Each agent pack subdirectory already has its own AGENTS.md;
this adds a minimal landing AGENTS.md that points readers into those
subdirs and links to ecap-workspace's architecture & external dependencies
guide (EN + 中文), which documents the full ECAP platform topology:
which repo owns which piece, env var to service map, and control-plane
vs data-plane separation.

CLAUDE.md is a symlink to AGENTS.md so Claude Code clients see the same
content as the AGENTS.md convention. The .gitignore had CLAUDE.md to
protect personal Claude configs in subdirectories from being committed;
this top-level symlink is force-added (git add -f) following the same
pattern as the existing tracked creator-ops/echotik-influencer/claude-code/CLAUDE.md.
The .gitignore is left unchanged so subdirectory personal configs stay
protected.

No subdirectory AGENTS.md files are modified.

Originating PR: https://github.com/SerendipityOneInc/ecap-workspace/pull/1627

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

- The repo top level had no `AGENTS.md` or `CLAUDE.md` (just an 18-byte `README.md`). Add a minimal top-level `AGENTS.md` that orients readers to the per-pack subdirectories and links to ecap-workspace's architecture guide (EN + 中文).
- Add `CLAUDE.md` as a relative symlink → `AGENTS.md` so Claude Code clients see the same content.
- `.gitignore` has `CLAUDE.md` listed (to protect personal Claude configs in subdirectories). This top-level symlink is force-added following the same pattern as the existing tracked `creator-ops/echotik-influencer/claude-code/CLAUDE.md`. `.gitignore` is left unchanged so the subdirectory protection stays in place — once tracked, gitignore rules are inert for this specific path anyway.
- **No subdirectory `AGENTS.md` files are touched** — each agent pack continues to own its own.
- Originating PR: https://github.com/SerendipityOneInc/ecap-workspace/pull/1627 documents the full ECAP platform topology; this repo is named there as the home of agent packs loaded by OpenClaw bot pods at runtime.

## Test plan

- [ ] Confirm `CLAUDE.md` is a symlink (`git ls-tree HEAD CLAUDE.md` shows mode `120000`).
- [ ] Confirm subdirectory `AGENTS.md` files are unchanged (`git diff main..HEAD -- '**/AGENTS.md' ':!AGENTS.md'` is empty).
- [ ] Confirm the two ecap-workspace links resolve once that PR lands on main.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [2] a5923292
- **Author**: vincent-srp
- **Date**: 2026-05-14T03:52:21Z
- **SHA**: a592329293c88ad199cd011342b7169913c3b1aa
- **PR**: #121

### Commit Message

```
feat(leofit): update to 4.2.2 (#121)

* feat(leofit): update to 4.2.2

Replace 4.2.1 layout with 4.2.2 structural reorg from build/leofit-4.2.2.tar.gz:

- Migrate skills/ -> .agents/skills/
- Fix SOUL.md and IDENTITY.md (4.2.1 incorrectly contained Agent Studio
  persona content; restored to Leo fitness coach)
- Bump agent-pack.yaml to 4.2.2 and simplify data binding (src/dst -> path)
- Update fit-exercises/gen_muscle_map_v2.py, fit-exercises/SKILL.md,
  fit-planner/planner.py
- Remove obsolete top-level duplicates (agent/), helper module (shared/),
  empty placeholder dirs (deps/, scripts/.gitkeep), data/foods/,
  BOOTSTRAP.md, README.md, requirements.txt
- TOOLS.md: drop ZooClaw TTS Voice Directive section and Chinese
  zero-mixing rule, update sample agent identifier

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* fix(leofit): remove ReDoS-prone alternation in muscle-map regex

`[^>]` already matches `\n` under re.DOTALL, so the `(?:[^>]|\n)*?`
alternation was redundant and caused catastrophic backtracking on
inputs starting with `<path` followed by many newlines. Replace with
`[^>]*` — same matches, linear time.

Re-applies 87c7faf, which landed on feat/leofit-4.2.1 but was not
included in the build/leofit-4.2.2.tar.gz drop.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- Apply 4.2.2 from `build/leofit-4.2.2.tar.gz` as a clean replacement of the 4.2.1 layout.
- Migrate skill location from `skills/` → `.agents/skills/` (matches agent-studio convention).
- Fix `SOUL.md` and `IDENTITY.md` — 4.2.1 mistakenly carried Agent Studio persona content; restored to Leo (fitness coach).
- Bump `agent-pack.yaml` to `4.2.2` and simplify data binding (`src/dst` → `path`).
- Update 3 skill files: `fit-exercises/SKILL.md`, `fit-exercises/gen_muscle_map_v2.py`, `fit-planner/planner.py`.
- Remove obsolete artifacts: `agent/` (top-level duplicates), `shared/`, `deps/`, `data/foods/`, `BOOTSTRAP.md`, `README.md`, `requirements.txt`, `scripts/.gitkeep`.
- `TOOLS.md`: drop the ZooClaw TTS Voice Directive block and the "zero mixing" English/Chinese rule; update sample agent identifier.

## Stats
41 files changed, +206 / -1061. Most muscle-map PNG/SVG assets and exercises JSONs are byte-identical and renamed unchanged.

## Test plan
- [ ] Install pack to `~/.openclaw/workspace-leofit` and confirm session boot reads SOUL/IDENTITY for Leo (not Agent Studio).
- [ ] Verify `.agents/skills/*/SKILL.md` are discovered (check that skills load under the new convention).
- [ ] Run `fit-exercises` muscle-map generation on a representative exercise.
- [ ] Confirm `agent-pack.yaml` data binding (`path:`) still resolves `data/exercises` and `data/muscle-maps`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
