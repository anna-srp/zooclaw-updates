---
title: "Council 研讨技能：新增「单专家主笔」合成、实时赛季/序列解析、论点处就地引用"
type: "Skill 上架/更新"
priority: "中"
外部: "B"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

Council 技能进一步打磨合成环节：由单一专家主笔统稿让报告更连贯、支持实时解析「本赛季/最新一期」等时间序列引用、把引用直接放在对应论点出处，减少「结论与出处对不上」的情况。

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- commit：a0f3b96ee56441185be15672cfe026654280f14e
- PR：#246
- 日期：2026-07-29T08:25:58Z

### Commit message

```
feat(council): one-expert-author synthesis, live series resolution, at-claim-site citations (#246)

Three staging-driven improvements to the council skill (validated on
betas v0.6.12-beta.1-.5, bot 9d52c157).

## 1. Synthesize as one expert author

A real staging report spent ~30% of its body on meta-commentary. Recast
synthesis deep-research-style: the composer picks the expert whose
judgment the topic deserves and writes the whole report in that voice;
the reader must never sense assembly from multiple reports - consensus
tags/counts forbidden. Claim map demoted to private bookkeeping.
Calibration survives quietly: contradictions still present both sides,
single-source hedges only on load-bearing claims, compact blind-spots
section near the end. Composer + fallback template now drift-gated by CI.

## 2. Live series version resolution - series_latest pins removed

Staging caught the pinned map's blind spot: a newer model was live on
litellm but the chair kept resolving the hand-declared pin. Version
bumps must cost zero maintenance. --propose-cast resolves each preset
series against the pod's per-run litellm catalog by version-free
signature: newest version wins, stable ahead of prerelease at equal
version. Line tokens survive the signature. series_latest deleted from
price_snapshot.json (prices only); a version newer than the snapshot
seats unpriced until --refresh-prices.

## 3. Citations at the claim site

Every key claim carries an inline markdown-link citation at the claim
site - a trailing Sources list alone is NOT citation; reviser hunts
uncited key claims.

## Testing

uv run --with pytest,pyyaml,jsonschema -m pytest council/tests/ - 271
passed. End-to-end against the real staging catalog (39 ids): casts all
resolve correctly.
```

### PR body

Three staging-driven improvements to the council skill (validated on betas v0.6.12-beta.1-.5, bot 9d52c157).

## 1. Synthesize as one expert author

A real staging report spent ~30% of its body on meta-commentary. Recast synthesis deep-research-style: the composer picks the expert whose judgment the topic deserves and writes the whole report in that voice; the reader must never sense assembly from multiple reports - consensus tags/counts forbidden. Claim map demoted to private bookkeeping. Calibration survives quietly. Composer + fallback template now drift-gated by CI.

## 2. Live series version resolution

Version bumps must cost zero maintenance. --propose-cast resolves each preset series against the pod's per-run litellm catalog by version-free signature: newest version wins, stable ahead of prerelease at equal version. series_latest deleted from price_snapshot.json; a version newer than the snapshot seats unpriced until --refresh-prices.

## 3. Citations at the claim site

Every key claim carries an inline markdown-link citation at the claim site - a trailing Sources list alone is NOT citation; reviser hunts uncited key claims.

## Testing

271 passed. End-to-end against the real staging catalog (39 ids): casts all resolve correctly.
