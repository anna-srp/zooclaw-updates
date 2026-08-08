---
title: "深度研究技能提速省钱：标准模式砍掉一轮修订"
type: "Skill 上架/更新"
priority: "高"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

council 深度研究的标准模式不再跑额外修订轮，报告出得更快、消耗的额度更少，确认页的费用预估也同步修正为真实值。

## 原始内容

### perf(council): revision only at deep depth (K: standard 1→0, deep 2→1) (#255)

- SHA: `0d503bb63b16a82e67578555dc46afb6b56b41fc`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
perf(council): revision only at deep depth (K: standard 1→0, deep 2→1) (#255)

## What

One-line change to Stage 5's K schedule: `quick 0 · standard 1 · deep 2`
→ `quick 0 · standard 0 · deep 1`. Standard runs (the default) become
composer-only; deep keeps one batched revision pass.

## Why

**Cost basis broke.** K-by-depth was ruled (design doc, 2026-07-11 blind
eval) when a full Stage 5 ran ~8–11 min. Production passes now cost
15–25 min each (bigger reports, 140K-context ingests, and an openclaw
idle-watchdog bug that kills+respawns long opus calls — 4/4 recent
aborts were synthesis sessions), making synthesis run 25–35 min against
the design doc's documented 3–5 min envelope.

**Quality evidence was always a weak trade.** The vault's blind eval
recorded: coverage/actionability ↑, calibration/citation ↓, K=2 over K=0
only 3-1 with a judge position-flip, diminishing pass-2 returns;
composer-only (K=0) beat the old v3 pipeline 4-0.

**A 2026 reflection survey confirms it on every axis** (30+ papers +
shipping systems): revision gains concentrate in pass 1 (Self-Refine,
Chain-of-Density, RefineBench); second passes undo earlier fixes and
citation faithfulness degrades universally across deep-research agents
(Mr DRE, ACL 2026 — break rate ~31%, worst-case −67pt faithfulness); no
flagship ships holistic draft revision (LangChain ODR explicitly
retreated to one-shot synthesis; the only shipped post-draft passes are
narrow grounded verification like Anthropic's CitationAgent). Deep's
single batched ≤8-edit pass is the literature-optimal form (Mr DRE
k-scaling: batching targets into one pass lowers break rate 32%→20%).

Full reconciliation recorded in the design doc as §9.12 (reviser origin,
cost drift, survey, ruling, shelved propose+apply redesign).

## Verification

274 council tests pass, lint clean. Prose-only change; the reviser
template and Stage 5(b) mechanics are unchanged (still used at deep).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR Body:**

## What

One-line change to Stage 5's K schedule: `quick 0 · standard 1 · deep 2` → `quick 0 · standard 0 · deep 1`. Standard runs (the default) become composer-only; deep keeps one batched revision pass.

## Why

**Cost basis broke.** K-by-depth was ruled (design doc, 2026-07-11 blind eval) when a full Stage 5 ran ~8–11 min. Production passes now cost 15–25 min each (bigger reports, 140K-context ingests, and an openclaw idle-watchdog bug that kills+respawns long opus calls — 4/4 recent aborts were synthesis sessions), making synthesis run 25–35 min against the design doc's documented 3–5 min envelope.

**Quality evidence was always a weak trade.** The vault's blind eval recorded: coverage/actionability ↑, calibration/citation ↓, K=2 over K=0 only 3-1 with a judge position-flip, diminishing pass-2 returns; composer-only (K=0) beat the old v3 pipeline 4-0.

**A 2026 reflection survey confirms it on every axis** (30+ papers + shipping systems): revision gains concentrate in pass 1 (Self-Refine, Chain-of-Density, RefineBench); second passes undo earlier fixes and citation faithfulness degrades universally across deep-research agents (Mr DRE, ACL 2026 — break rate ~31%, worst-case −67pt faithfulness); no flagship ships holistic draft revision (LangChain ODR explicitly retreated to one-shot synthesis; the only shipped post-draft passes are narrow grounded verification like Anthropic's CitationAgent). Deep's single batched ≤8-edit pass is the literature-optimal form (Mr DRE k-scaling: batching targets into one pass lowers break rate 32%→20%).

Full reconciliation recorded in the design doc as §9.12 (reviser origin, cost drift, survey, ruling, shelved propose+apply redesign).

## Verification

274 council tests pass, lint clean. Prose-only change; the reviser template and Stage 5(b) mechanics are unchanged (still used at deep).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

### fix(council): estimate K_BY_DEPTH follows PR #255 schedule (#256)

- SHA: `044d8742100b19cb804b347a535786c1c430f3f5`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
fix(council): estimate K_BY_DEPTH follows PR #255 schedule (#256)

## Problem (codex post-merge P1 on #255)

PR #255 changed SKILL.md's Stage 5 reviser schedule (`quick 0 · standard
0 · deep 1`) but `estimate_band.py` carries its own hardcoded
`K_BY_DEPTH` copy and prices synthesis as `1+K` spawns — so the confirm
gate overquoted every standard run (2 synthesis spawns priced, 1
actually spawned) and every deep run (3 vs 2). The gate is the user's
go/cancel decision point, so this is message-fidelity, not stale prose.
My #255 claim of "prose-only change" was wrong — codex caught it in
post-outage review.

## Fix

- `K_BY_DEPTH` → `{quick: 0, standard: 0, deep: 1}`; standard
fallback-band example now quotes 495/2580 (was 660/3440).
- Updated the pricing test's expectations.
- **New drift-gate test**
`test_k_by_depth_matches_skill_md_stage5_schedule`: parses the schedule
out of SKILL.md and enforces equality with the estimator's table — the
"MUST match SKILL.md" comment just failed its live trial, so the sync is
now machine-checked (same pattern as the composer-template drift gate).

## Verification

275 council tests pass (274 + new gate), lint clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

**PR Body:**

## Problem (codex post-merge P1 on #255)

PR #255 changed SKILL.md's Stage 5 reviser schedule (`quick 0 · standard 0 · deep 1`) but `estimate_band.py` carries its own hardcoded `K_BY_DEPTH` copy and prices synthesis as `1+K` spawns — so the confirm gate overquoted every standard run (2 synthesis spawns priced, 1 actually spawned) and every deep run (3 vs 2). The gate is the user's go/cancel decision point, so this is message-fidelity, not stale prose. My #255 claim of "prose-only change" was wrong — codex caught it in post-outage review.

## Fix

- `K_BY_DEPTH` → `{quick: 0, standard: 0, deep: 1}`; standard fallback-band example now quotes 495/2580 (was 660/3440).
- Updated the pricing test's expectations.
- **New drift-gate test** `test_k_by_depth_matches_skill_md_stage5_schedule`: parses the schedule out of SKILL.md and enforces equality with the estimator's table — the "MUST match SKILL.md" comment just failed its live trial, so the sync is now machine-checked (same pattern as the composer-template drift gate).

## Verification

275 council tests pass (274 + new gate), lint clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

