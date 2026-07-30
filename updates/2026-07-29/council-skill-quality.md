---
title: "Council 研讨技能升级：议题自动消歧、引用更完整、盲点排查、专家分工更合理"
type: "Skill 上架/更新"
priority: "高"
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
v0.6.12-beta.6–.7, bot 9d52c157; design doc §9.9–§9.11).

## 1. Topic rewrite at Stage 0

Same input ("调研今年上半赛季F1") produced a 2025 full-season report on one pod
and 2026-H1 on another — ambiguity resolution was implicit and
per-model. Now: the topic is rewritten before `init` (same language,
disambiguated only) and the rewrite is the sole topic everywhere.
Deterministic references resolve against the CURRENT date silently;
judgment calls surface as the panel's `Assumed:` line; an unattended
coin-flip referent refuses the run (zero spend). The rewrite resolves
references and never ASSERTS new facts (staging: an invented "第14站" fed
members a false premise — caught and corrected by the report itself).
Members get a `Today:` anchor. Referent-only boundary: no shared
dimension framework is ever dispatched (anti-anchoring).

## 2. Citation completeness

Load-bearing secondhand claims: members chase them upstream before
breadth, unreachable ones land in Risks, the composer's blind-spots
section carries them onto the delivery's follow-up path. Data tables
carry a source line beneath (member + composer/fallback templates,
drift-gated pair).

## 3. Blind-spot triage replaces the mandatory gap-research pass

Forensics showed the old delivery gate was silently skipped, and
following it would have spent deep-research passes on member-chased-dry
items. Now: disclosed items stand; synthesis-emergent questions
answerable by ≤3 direct searches get checked inline (no spawn);
user-dependent items become questions; the triage outcome is one
delivery line — never silent.

## 4. Member-chairs permitted (synthesizer∉members gate removed)

User decision: the blinding scrub stays, and the v3 composer merges
rather than scores. Auto-picked chairs still prefer fresh eyes; only an
explicit `synthesizer <model>` override seats a member as chair. The one
real side effect — cast-pricing identity collisions letting an unpriced
chair twin clobber a priced member entry — is fixed with a regression
test. A two-topic appendix-blind A/B (design doc §9.11) validated the
same-tier-chair option for fact-recap topics (~25–40% cheaper, equal
quality) while confirming the opus default for judgment-heavy ones (it
caught an arithmetic contradiction in circulating GMV figures that the
same-tier chair credited).

## Review trail

13 bot rounds. Three codex P1s adjudicated: unattended judgment-call
spend → fixed (Stage-0 refusal); non-version-suffix resolution →
documented design boundary; cost-join collision → fixed (c51dbae). Final
verdicts APPROVE / severity NONE; claude's last minor note (missing
regression test) is factually covered by
`test_cli_member_chair_overlap_keeps_the_priced_entry`.

## Testing

`uv run --with pytest,pyyaml,jsonschema -m pytest council/tests/` — 271
passed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01THqUHU4BtCMq7xLxE7ZPKa

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR body

Staging-driven improvements across four areas (validated on betas v0.6.12-beta.6–.7, bot 9d52c157; design doc §9.9–§9.11).

## 1. Topic rewrite at Stage 0

Same input ("调研今年上半赛季F1") produced a 2025 full-season report on one pod and 2026-H1 on another — ambiguity resolution was implicit and per-model. Now: the topic is rewritten before `init` (same language, disambiguated only) and the rewrite is the sole topic everywhere. Deterministic references resolve against the CURRENT date silently; judgment calls surface as the panel's `Assumed:` line; an unattended coin-flip referent refuses the run (zero spend). The rewrite resolves references and never ASSERTS new facts (staging: an invented "第14站" fed members a false premise — caught and corrected by the report itself). Members get a `Today:` anchor. Referent-only boundary: no shared dimension framework is ever dispatched (anti-anchoring).

## 2. Citation completeness

Load-bearing secondhand claims: members chase them upstream before breadth, unreachable ones land in Risks, the composer's blind-spots section carries them onto the delivery's follow-up path. Data tables carry a source line beneath (member + composer/fallback templates, drift-gated pair).

## 3. Blind-spot triage replaces the mandatory gap-research pass

Forensics showed the old delivery gate was silently skipped, and following it would have spent deep-research passes on member-chased-dry items. Now: disclosed items stand; synthesis-emergent questions answerable by ≤3 direct searches get checked inline (no spawn); user-dependent items become questions; the triage outcome is one delivery line — never silent.

## 4. Member-chairs permitted (synthesizer∉members gate removed)

User decision: the blinding scrub stays, and the v3 composer merges rather than scores. Auto-picked chairs still prefer fresh eyes; only an explicit `synthesizer <model>` override seats a member as chair. The one real side effect — cast-pricing identity collisions letting an unpriced chair twin clobber a priced member entry — is fixed with a regression test. A two-topic appendix-blind A/B (design doc §9.11) validated the same-tier-chair option for fact-recap topics (~25–40% cheaper, equal quality) while confirming the opus default for judgment-heavy ones (it caught an arithmetic contradiction in circulating GMV figures that the same-tier chair credited).

## Review trail

13 bot rounds. Three codex P1s adjudicated: unattended judgment-call spend → fixed (Stage-0 refusal); non-version-suffix resolution → documented design boundary; cost-join collision → fixed (c51dbae). Final verdicts APPROVE / severity NONE; claude's last minor note (missing regression test) is factually covered by `test_cli_member_chair_overlap_keeps_the_priced_entry`.

## Testing

`uv run --with pytest,pyyaml,jsonschema -m pytest council/tests/` — 271 passed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01THqUHU4BtCMq7xLxE7ZPKa
