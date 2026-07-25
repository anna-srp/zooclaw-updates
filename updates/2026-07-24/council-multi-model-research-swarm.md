---
title: "AI 研究议会：多模型协作，一次调研让多家顶尖模型交叉验证"
type: "Skill 上架/更新"
priority: "高"
date: "2026-07-24"
status: "待审核"
channels: ""
---

## 核心宣传点

ZooClaw 新增「研究议会」深度调研技能：一次提问，自动召集来自不同厂商的多个顶级大模型（如 Claude、Gemini 等）并行独立研究同一课题，再经匿名盲评与多轮综合，产出经过交叉验证、更客观可靠的深度调研报告。适合需要高可信度结论的重要决策与研究场景。

## 原始内容

**Commit**: `d8a24677a5` — felix-srp — 2026-07-24T02:24:05Z

### Commit Message

```
feat(council): multi-model research council — swarm architecture (#237)

## What

The multi-model research **council** as a standalone ecap-skills skill
(deep-research form): `council/SKILL.md` (orchestration playbook) + 9
scripts + 2 schemas + 265 hermetic tests.

Architecture (measured across 9 staging runs / 12 blind judgings —
evidence trail in ecap-agent-pack PR #204 and the design vault):
- **Members** = cross-vendor subagents (`sessions_spawn` model
override), batched parallel spawn, native web tools, transient-failure
auto-respawn; two evidence modes (independent web research / shared
staged dossiers with the code-enforced NO_EVIDENCE gate); an unledgered
member failure requires the explicit `--no-session` attestation (spawn
accounting can't be silently bypassed).
- **Blinding** = deterministic scrub + shuffled anonymous numbering.
- **Synthesis** = append-composer + K fresh-context revision passes (K
by depth: 0/1/2), degrading to a one-shot streaming synthesis on double
failure — a run never dies of synthesis.
- **Casting** = tiers are curated QUALITY classes: preset lineups pin
SERIES (`claude-sonnet`, `gemini-flash`), the committed snapshot's
`series_latest` map supplies the current version (a model refresh is a
one-line JSON bump, never a code edit), and casts resolve against the
litellm catalog (`roster.py --fetch-models` — never `openclaw models
list`, whose static declaration drifts) for dispatchable ids.
- **Ops**: depth `auto` (topic-classified 3/4/5 lineup), synthesizer
discipline (one class above members, never a member), canonical
confirm-panel grammar (composer UI contract), per-stage empirical
estimate bands from historical ledgers (premium alt quoted only from a
real premium cast), cost collection with unmetered fail-loud,
executive-summary delivery with autonomous blind-spot gap follow-up.

Quality record vs the previous litellm-pipeline council: **4-2 and 4-0
on two topics** (blind, position-swapped, 3 judges).

## Origin

Extracted from `ecap-agent-pack/researcher` (PR #204 lineage); the pack
now consumes this skill via `external_skills`. Skill-lint passes clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01GHZD39FTQv5PLjZqBTpjkP

---------

Co-authored-by: felix-srp <felix@serendipityone.com>
Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## What

The multi-model research **council** as a standalone ecap-skills skill (deep-research form): `council/SKILL.md` (orchestration playbook) + 9 scripts + 2 schemas + 265 hermetic tests.

Architecture (measured across 9 staging runs / 12 blind judgings — evidence trail in ecap-agent-pack PR #204 and the design vault):
- **Members** = cross-vendor subagents (`sessions_spawn` model override), batched parallel spawn, native web tools, transient-failure auto-respawn; two evidence modes (independent web research / shared staged dossiers with the code-enforced NO_EVIDENCE gate); an unledgered member failure requires the explicit `--no-session` attestation (spawn accounting can't be silently bypassed).
- **Blinding** = deterministic scrub + shuffled anonymous numbering.
- **Synthesis** = append-composer + K fresh-context revision passes (K by depth: 0/1/2), degrading to a one-shot streaming synthesis on double failure — a run never dies of synthesis.
- **Casting** = tiers are curated QUALITY classes: preset lineups pin SERIES (`claude-sonnet`, `gemini-flash`), the committed snapshot's `series_latest` map supplies the current version (a model refresh is a one-line JSON bump, never a code edit), and casts resolve against the litellm catalog (`roster.py --fetch-models` — never `openclaw models list`, whose static declaration drifts) for dispatchable ids.
- **Ops**: depth `auto` (topic-classified 3/4/5 lineup), synthesizer discipline (one class above members, never a member), canonical confirm-panel grammar (composer UI contract), per-stage empirical estimate bands from historical ledgers (premium alt quoted only from a real premium cast), cost collection with unmetered fail-loud, executive-summary delivery with autonomous blind-spot gap follow-up.

Quality record vs the previous litellm-pipeline council: **4-2 and 4-0 on two topics** (blind, position-swapped, 3 judges).

## Origin

Extracted from `ecap-agent-pack/researcher` (PR #204 lineage); the pack now consumes this skill via `external_skills`. Skill-lint passes clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01GHZD39FTQv5PLjZqBTpjkP


