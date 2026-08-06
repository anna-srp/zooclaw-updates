---
title: "Council 开放经济档位，低成本也能跑"
type: "Skill 上架/更新"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# Council 开放经济档位，低成本也能跑

## 核心宣传点

想省钱跑 Council 现在有了明确入口：economy / standard / premium 三档任选，说“便宜点跑”就会用经济阵容。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-skills`
- Commit：`8159a6dc33a7b84b76763f839bac919a46a26603`
- 作者：felix-srp
- 日期：2026-08-05T04:41:36Z
- PR：#253

### Commit Message

```
fix(council): surface economy tier in SKILL.md (#253)

## Problem

`economy` tier doesn't work in practice: `roster.py` has carried a full
economy lineup since the 2026-07-20 tier redesign (members `claude-haiku
· gpt-luna · gemini-flash-lite · grok · glm · kimi · qwen`, sonnet
chair), the status schema accepts `tier: economy`, and the cast gates
pass it — verified with a local `--propose-cast --tier economy` repro
that resolves cleanly. But **SKILL.md never mentions the tier**: the
only vocabulary the orchestrating agent gets is "Default standard; offer
premium", and the confirm-gate panel's adjust tokens omit `economy`. A
user asking for an economy/cheap run has no documented path to `--tier
economy`.

## Fix (SKILL.md only, 2 lines)

- Tier paragraph now enumerates the three tiers — `economy / standard
(default) / premium` — and maps cheap/budget requests to economy
(mirroring the existing `ultra` → premium mapping).
- Confirm-gate panel adjust tokens: `premium` → `tier
economy|standard|premium` — the `tier` prefix keeps `standard`
unambiguous vs the `quick|standard|deep` depth tokens and gives a
one-token path back to the default tier (codex round-1 P1).

No script changes; `roster.py` already resolves the economy lineup.

## Verification

- `lint_skills.py`: all skills pass.
- Council suite: 271 passed.
- Local repro against a snapshot-shaped catalog: economy cast =
`claude-haiku-4-5 · gpt-5.6-luna · gemini-3.1-flash-lite · grok-4.5`,
synthesizer `claude-sonnet-5`, no skips, no unfilled seats.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Problem

`economy` tier doesn't work in practice: `roster.py` has carried a full economy lineup since the 2026-07-20 tier redesign (members `claude-haiku · gpt-luna · gemini-flash-lite · grok · glm · kimi · qwen`, sonnet chair), the status schema accepts `tier: economy`, and the cast gates pass it — verified with a local `--propose-cast --tier economy` repro that resolves cleanly. But **SKILL.md never mentions the tier**: the only vocabulary the orchestrating agent gets is "Default standard; offer premium", and the confirm-gate panel's adjust tokens omit `economy`. A user asking for an economy/cheap run has no documented path to `--tier economy`.

## Fix (SKILL.md only, 2 lines)

- Tier paragraph now enumerates the three tiers — `economy / standard (default) / premium` — and maps cheap/budget requests to economy (mirroring the existing `ultra` → premium mapping).
- Confirm-gate panel adjust tokens: `premium` → `tier economy|standard|premium` — the `tier` prefix keeps `standard` unambiguous vs the `quick|standard|deep` depth tokens and gives a one-token path back to the default tier (codex round-1 P1).

No script changes; `roster.py` already resolves the economy lineup.

## Verification

- `lint_skills.py`: all skills pass.
- Council suite: 271 passed.
- Local repro against a snapshot-shaped catalog: economy cast = `claude-haiku-4-5 · gpt-5.6-luna · gemini-3.1-flash-lite · grok-4.5`, synthesizer `claude-sonnet-5`, no skips, no unfilled seats.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
