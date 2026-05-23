---
title: "Chameleon 视频生成（Seedance）优化：更稳定的排队机制与更清晰的任务命名"
type: "Skill 上架/更新"
priority: "高"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# Chameleon 视频生成（Seedance）优化：更稳定的排队机制与更清晰的任务命名

## 核心宣传点

Chameleon AI 视频生成功能优化：任务排队更稳定不易丢失，任务名称更清晰易识别，整体视频生成体验更流畅。

## 原始内容

**Commit**: 760b9c2e1fd0fe56c6078dfff3399aa7722bd86e
**Author**: david-srp
**Date**: 2026-05-22T09:59:00Z
**PR**: #199

### Commit Message
```
feat(chameleon-seedance): queue priority + rename for stronger Seedance routing (#199)

* feat(chameleon): expose Seedance 2.0 queue priority field

Add --priority CLI flag (int 0-9, default 0) on chameleon_generate.py,
validate the range client-side, and inject "priority" into the payload
only when non-zero so default requests stay clean. Document the field
semantics (per-endpoint queue jump, never preempts running, not honored
under service_tier=flex) in the BytePlus API reference and KB summary.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

* refactor(chameleon-seedance): rename skill to surface Seedance in routing

Rename the skill directory chameleon -> chameleon-seedance so "seedance"
appears in the skill's canonical name (a stronger routing signal than the
description alone). Rewrite the SKILL.md description into an English
TRIGGER / SKIP pattern that lists Seedance / Dreamina / dreamina-seedance
keywords plus common request verbs, and explicitly defers burned-in
subtitle removal to the user-level subtitle-erasure skill so the two no
longer compete on the "Seedance" keyword.

Also update PUBLISHED_SKILLS so the S3 release tracks the renamed dir.
The trace/archive layer at ~/openclaw/chameleon/ is intentionally left
untouched — that path follows the project codename, not the skill name,
so existing user archives are preserved.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description
## Summary

Two commits on this branch:

### 1. `feat`: expose Seedance 2.0 queue priority field
- New `--priority N` CLI flag on the generation script (int, default `0`, range `0-9`); client-side rejects out-of-range
- Payload only carries `"priority": N` when `priority > 0`, so default requests stay clean
- Updated `byteplus-dreamina-seedance-2.0-api.md` and `chameleon-kb-summary.md` with the field's semantics: Seedance 2.0 only, per-endpoint queue jump, same-priority stays FIFO, never preempts a `running` task, not honored under `service_tier=flex`

### 2. `refactor`: rename `chameleon` → `chameleon-seedance`
- Surface "seedance" in the skill's canonical name → strongest routing signal when users mention Seedance / Dreamina
- Rewrite the `SKILL.md` description into an explicit English **TRIGGER / SKIP** pattern, listing common keywords (seedance, Seedance 2.0, Dreamina, dreamina-seedance-2-0, ByteDance video model, Volcengine video generation) and request verbs (generate / produce / render / chain / extend a video, lock first/last frame, attach reference media, set queue priority)
- **SKIP and route to `subtitle-erasure`** for burned-in subtitle removal — disambiguates the two skills that both mention "Seedance"
- `PUBLISHED_SKILLS` updated so the S3 release picks up the renamed directory
- Trace/archive layer `~/openclaw/chameleon/` **intentionally left untouched** — that path is tied to the project codename, not the skill name, so existing user archives are preserved

## Test plan
- [x] `--priority 5` / `--priority 7` → payload contains `"priority": N`
- [x] Default invocation → payload omits `priority`
- [x] `--priority 10` / `--priority -1` → rejected client-side with clear error
- [x] Dry-run still works from the renamed `chameleon-seedance/scripts/` path
- [ ] Submit one real task with `--priority` set, confirm ecap-proxy / upstream ModelArk accepts the new field
- [ ] After merge, confirm openclaw harness picks up the renamed `chameleon-seedance` skill from S3 and Seedance keyword queries route to it (no more drift to subtitle-erasure)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

