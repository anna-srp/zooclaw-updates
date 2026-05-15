---
title: "LeoFit 健身 Agent 更新至 4.2.2"
type: "Agent 上架/更新"
priority: "中"
date: "2026-05-14"
status: "待审核"
channels: ""
---
# LeoFit 健身 Agent 更新至 4.2.2

## 核心宣传点

LeoFit 健身教练 Agent 升级到 4.2.2 版本，修复了角色个性问题（之前误用了 Agent Studio 的人设），更新了训练计划和肌肉图谱生成功能，让 Leo 回归专业健身教练定位。

## 原始内容

**Commit**: a5923292 | feat(leofit): update to 4.2.2 (#121)

**Commit Message**:
```
feat(leofit): update to 4.2.2 (#121)
```

**PR Body**:
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
