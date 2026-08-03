---
title: "Council 研讨技能升级：议题自动消歧、引用更完整、盲点排查、专家分工更合理"
type: "Skill 上架/更新"
priority: "高"
外部: "B"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

Council 专家研讨技能迎来质变升级：在开跑前先对议题做同语言消歧（避免同一问题在不同节点跑出不同年份/口径的结果）、强化引用完整性并把引用放到论点出处、新增盲点排查与「一专家主笔」的合成机制、按成员设置分会主席，产出的调研报告更准更可信。

## 原始内容

- 仓库：SerendipityOneInc/ecap-skills
- commit：edc97f48dfdc6cf31f48f47dfc4d1502abec2cfa
- PR：#247
- 日期：2026-07-29T19:39:19Z

### Commit message

```
feat(council): topic rewrite, citation completeness, blind-spot triage, member-chairs (#247)

Staging-driven improvements across four areas (validated on betas
v0.6.12-beta.6-.7, bot 9d52c157; design doc §9.9-§9.11).

## 1. Topic rewrite at Stage 0

Same input produced a 2025 full-season report on one pod and 2026-H1 on
another - ambiguity resolution was implicit and per-model. Now: the
topic is rewritten before init (same language, disambiguated only) and
the rewrite is the sole topic everywhere. Deterministic references
resolve against the CURRENT date silently; judgment calls surface as the
panel's Assumed line; an unattended coin-flip referent refuses the run
(zero spend). Members get a Today anchor.

## 2. Citation completeness

Load-bearing secondhand claims: members chase them upstream before
breadth, unreachable ones land in Risks, the composer's blind-spots
section carries them onto the delivery's follow-up path. Data tables
carry a source line beneath.

## 3. Blind-spot triage replaces the mandatory gap-research pass

Disclosed items stand; synthesis-emergent questions answerable by <=3
direct searches get checked inline (no spawn); user-dependent items
become questions; the triage outcome is one delivery line - never
silent.

## 4. Member-chairs permitted (synthesizer-not-in-members gate removed)

The blinding scrub stays, and the v3 composer merges rather than scores.
Auto-picked chairs still prefer fresh eyes; only an explicit synthesizer
override seats a member as chair. A two-topic appendix-blind A/B
validated the same-tier-chair option for fact-recap topics (~25-40%
cheaper, equal quality) while confirming the opus default for
judgment-heavy ones.

## Testing

uv run --with pytest,pyyaml,jsonschema -m pytest council/tests/ - 271
passed.
```

### PR body

Staging-driven improvements across four areas (validated on betas v0.6.12-beta.6-.7, bot 9d52c157; design doc §9.9-§9.11).

## 1. Topic rewrite at Stage 0

Same input produced a 2025 full-season report on one pod and 2026-H1 on another - ambiguity resolution was implicit and per-model. Now the topic is rewritten before init (same language, disambiguated only) and the rewrite is the sole topic everywhere. Deterministic references resolve against the CURRENT date silently; judgment calls surface as the panel's Assumed line; an unattended coin-flip referent refuses the run (zero spend). Members get a Today anchor.

## 2. Citation completeness

Load-bearing secondhand claims: members chase them upstream before breadth, unreachable ones land in Risks, the composer's blind-spots section carries them onto the delivery's follow-up path. Data tables carry a source line beneath.

## 3. Blind-spot triage

Disclosed items stand; synthesis-emergent questions answerable by <=3 direct searches get checked inline; user-dependent items become questions; the triage outcome is one delivery line.

## 4. Member-chairs permitted

The blinding scrub stays, and the v3 composer merges rather than scores. Auto-picked chairs still prefer fresh eyes; only an explicit synthesizer override seats a member as chair. A two-topic appendix-blind A/B validated the same-tier-chair option for fact-recap topics (~25-40% cheaper, equal quality) while confirming the opus default for judgment-heavy ones.

## Testing

271 passed.
