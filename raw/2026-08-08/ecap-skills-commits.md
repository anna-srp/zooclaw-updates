# ecap-skills commits 2026-08-08

## 3852a91491

- SHA: `3852a91491d78a2e3a4097a4f9319fb25400af23`
- 作者: felix-srp
- 日期: 2026-08-08T01:48:29Z

### Commit Message

```
feat(deep-research): RACE benchmark fixes — readability contract, format obedience, bounded routing triggers (#259)

## Why

The 2026-08-06 DeepResearch Bench evaluation (20/100 bilingual sample,
GPT-5.5 RACE judge, production ZooClaw + this skill) scored
**53.68/100** overall, with **Readability (51.25)** the persistently
weakest dimension across all three evaluation rounds (pilot 49.87,
canary 52.16, final 51.25) vs 53.6–54.5 for the other dimensions.
Per-task data shows the losses are presentation-shaped, not
research-shaped: tight 19–26K-char reports outscored 40–60K-char ones,
and URL count didn't correlate with score. Full analysis:
`zooclaw-benchmark` reports `deepresearch_prod20_20260806.md` /
`deepresearch_prod20_retry_20260806.md`.

A 5-task staging smoke (tasks 51–55, sonnet-5, this PR's skill) then
showed content dimensions already beat the expert references on
**every** comprehensiveness/insight criterion — the remaining deficit is
presentation-side and concentrated (scope discipline, diffuse
multi-entity organization). Criterion-level evidence:
`design-doc/deep-research/2026-08-07-smoke5-criterion-findings.md`.

## What changed (SKILL.md only)

- **Readability contract** (recipe-form): pyramid structure (each
section opens with its key finding; explicitly presentation order, not
advocacy) and tightness ("say each thing once; length is not rigor").
- **Scope discipline** (smoke-5 evidence): everything included serves
the original questions — interesting-but-unasked findings get one line
or nothing.
- **Question-shaped comparisons** (smoke-5 evidence): unless the user
specified a comparison layout, organize by the compared dimensions —
every subject in each section, not one section per subject.
- **Answer-skeleton synthesis** (52/54 probe evidence): before drafting,
state a few sentences each for every asked question and for the report's
key findings, tensions, and limitations; the report expands those
sentences with evidence — material expanding none of them stays in the
dossier.
- **Edit pass** on the assembled draft: cut cross-section repetition,
surface buried findings, unify terminology. Replaces the deep-breadth
"spot-check rather than re-reading" stitch guidance.
- **Readability item** added to the Pre-delivery Check (was the only
RACE dimension the self-check didn't cover).
- **Format obedience**: user-specified structure/genre overrides the
default section list; invariants pinned — limitations disclosure and
full source citations appear in every format.
- **Sub-question closure**: completeness gate + check require every
explicitly asked sub-question answered.
- **Terminal-delivery rule**: progress notes visibly partial; the report
is its own complete final message (runtime async defect mitigations;
real fix is v2026.7.1-beta.1+).
- **Routing triggers** in `description`: research reports, literature
reviews, 研究报告, 文献综述 — bounded with "researches, never reformats existing
content"; 趋势研究 dropped. 193/200 chars.
- **Token trim**: −134 tokens, dual-reviewed (zero constraints lost).
Net runtime cost vs main: 2,955 → ~3,150 tokens.

## Review rounds

- Round 1: srp-codex P1 (routing over-breadth) + srp-claude-assistant
(format override could drop Limitations/Sources) — fixed in `c39b4a9`.
- Round 2: both bots APPROVE.
- Round 3 (trim `10b1761`): pre-verified by independent Claude+Codex
constraint-loss review; bots clean.
- Round 4 (`508e20d` scope/comparison): claude APPROVE; codex P1 —
comparison rule could override an explicit user layout — fixed in
`911242f`.
- Round 5: both bots APPROVE `911242f`, zero findings.
- Round 6 (`b2bc5be` answer-skeleton): claude APPROVE; codex P1 — filter
could suppress landscape/tensions/limitations on exploratory prompts —
fixed in `ffa70a9`.
- Round 7: both bots APPROVE `ffa70a9`; claude re-verified all three
prior P1s at HEAD. CI green throughout.

## Verification

- Linter 0 errors at every commit; dual constraint-loss review on the
trim.
- 5-task staging smoke (sonnet-5): overall 52.08 vs July 52.64 (flat,
within n=5 judge noise); reports 19–25% tighter; content criteria all
won vs reference.
- 52/54 probe (`v0.6.14-beta.2`): task 54's scope + readability criteria
flipped from losses to wins (readability 49.30→51.93, beyond judge
noise); task 52 improved but not closed → answer-skeleton synthesis
added.
- Task-52 probe (`v0.6.14-beta.4` = HEAD): readability 47.90→50.39
(+2.49, beyond noise), directness criterion flipped to a win (9.2 vs
8.7) after being stuck two arms. Both criterion-driven edits validated;
remaining gate is the frozen-20 confirmation run on prod.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01A9rjGtByhu2o7aDZTXRKPE

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Why

The 2026-08-06 DeepResearch Bench evaluation (20/100 bilingual sample, GPT-5.5 RACE judge, production ZooClaw + this skill) scored **53.68/100** overall, with **Readability (51.25)** the persistently weakest dimension across all three evaluation rounds (pilot 49.87, canary 52.16, final 51.25) vs 53.6–54.5 for the other dimensions. Per-task data shows the losses are presentation-shaped, not research-shaped: tight 19–26K-char reports outscored 40–60K-char ones, and URL count didn't correlate with score. Full analysis: `zooclaw-benchmark` reports `deepresearch_prod20_20260806.md` / `deepresearch_prod20_retry_20260806.md`.

A 5-task staging smoke (tasks 51–55, sonnet-5, this PR's skill) then showed content dimensions already beat the expert references on **every** comprehensiveness/insight criterion — the remaining deficit is presentation-side and concentrated (scope discipline, diffuse multi-entity organization). Criterion-level evidence: `design-doc/deep-research/2026-08-07-smoke5-criterion-findings.md`.

## What changed (SKILL.md only)

- **Readability contract** (recipe-form): pyramid structure (each section opens with its key finding; explicitly presentation order, not advocacy) and tightness ("say each thing once; length is not rigor").
- **Scope discipline** (smoke-5 evidence): everything included serves the original questions — interesting-but-unasked findings get one line or nothing.
- **Question-shaped comparisons** (smoke-5 evidence): unless the user specified a comparison layout, organize by the compared dimensions — every subject in each section, not one section per subject.
- **Answer-skeleton synthesis** (52/54 probe evidence): before drafting, state a few sentences each for every asked question and for the report's key findings, tensions, and limitations; the report expands those sentences with evidence — material expanding none of them stays in the dossier.
- **Edit pass** on the assembled draft: cut cross-section repetition, surface buried findings, unify terminology. Replaces the deep-breadth "spot-check rather than re-reading" stitch guidance.
- **Readability item** added to the Pre-delivery Check (was the only RACE dimension the self-check didn't cover).
- **Format obedience**: user-specified structure/genre overrides the default section list; invariants pinned — limitations disclosure and full source citations appear in every format.
- **Sub-question closure**: completeness gate + check require every explicitly asked sub-question answered.
- **Terminal-delivery rule**: progress notes visibly partial; the report is its own complete final message (runtime async defect mitigations; real fix is v2026.7.1-beta.1+).
- **Routing triggers** in `description`: research reports, literature reviews, 研究报告, 文献综述 — bounded with "researches, never reformats existing content"; 趋势研究 dropped. 193/200 chars.
- **Token trim**: −134 tokens, dual-reviewed (zero constraints lost). Net runtime cost vs main: 2,955 → ~3,150 tokens.

## Review rounds

- Round 1: srp-codex P1 (routing over-breadth) + srp-claude-assistant (format override could drop Limitations/Sources) — fixed in `c39b4a9`.
- Round 2: both bots APPROVE.
- Round 3 (trim `10b1761`): pre-verified by independent Claude+Codex constraint-loss review; bots clean.
- Round 4 (`508e20d` scope/comparison): claude APPROVE; codex P1 — comparison rule could override an explicit user layout — fixed in `911242f`.
- Round 5: both bots APPROVE `911242f`, zero findings.
- Round 6 (`b2bc5be` answer-skeleton): claude APPROVE; codex P1 — filter could suppress landscape/tensions/limitations on exploratory prompts — fixed in `ffa70a9`.
- Round 7: both bots APPROVE `ffa70a9`; claude re-verified all three prior P1s at HEAD. CI green throughout.

## Verification

- Linter 0 errors at every commit; dual constraint-loss review on the trim.
- 5-task staging smoke (sonnet-5): overall 52.08 vs July 52.64 (flat, within n=5 judge noise); reports 19–25% tighter; content criteria all won vs reference.
- 52/54 probe (`v0.6.14-beta.2`): task 54's scope + readability criteria flipped from losses to wins (readability 49.30→51.93, beyond judge noise); task 52 improved but not closed → answer-skeleton synthesis added.
- Task-52 probe (`v0.6.14-beta.4` = HEAD): readability 47.90→50.39 (+2.49, beyond noise), directness criterion flipped to a win (9.2 vs 8.7) after being stuck two arms. Both criterion-driven edits validated; remaining gate is the frozen-20 confirmation run on prod.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01A9rjGtByhu2o7aDZTXRKPE


### 改动文件

- deep-research/SKILL.md
