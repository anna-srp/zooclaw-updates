---
title: "对话框模型选择新增 Auto 自动选型"
type: "新功能上线"
priority: "高"
date: "2026-08-11"
status: "待审核"
channels: ""
---

## 核心宣传点

在对话输入框的模型下拉里直接选 “Auto”，系统会为每个 Agent 派发的子任务自动挑最合适的模型，你不用再逐个手动切换。

## 原始内容

### commit message

```
fix(chat): add Auto to composer model picker (#3307)

## Summary

- add `Auto` as the first option in the active composer model dropdown
for supported computer workspaces
- treat Auto as an Agent-scoped virtual model through
`agentModes.<agentId>`, not a bot-global routing toggle
- preserve each Agent's concrete model and route only its delegated
native subagent spawns
- keep session `/auto` and `/auto off` as narrower overrides
- use atomic Agent + router configuration writes and per-key deep merge
so concurrent edits to different Agents do not clobber each other

## Runtime contract

Companion model-router PR:
https://github.com/SerendipityOneInc/zooclaw-extras/pull/214

Selection precedence is session override, then Agent mode, then routing
off. The router evaluates every `sessions_spawn` independently. OpenClaw
persists the selected concrete model on the child session. Explicit
spawn models are preserved, and media-bearing spawns fail open unless
the candidate declares all required input modalities.

## Verification

- [x] focused web verification: TypeScript, ESLint, 123 tests
- [x] focused backend model/router tests: 33 passed
- [x] related Agent and OpenClaw settings suites: 332 passed
- [x] full backend Pyright with a clean Python 3.12 environment: 0
errors
- [x] Ruff and import contracts
- [x] companion router tests: 189 passed, typecheck, lint, pre-push
suite

The first local ECAP push attempt used the conda interpreter selected by
`verify-py.sh`; that interpreter could not resolve the worktree
environment. The same full Pyright command passed with the clean Python
3.12 environment used for the backend tests.
```

### PR body

## Summary

- add `Auto` as the first option in the active composer model dropdown for supported computer workspaces
- treat Auto as an Agent-scoped virtual model through `agentModes.<agentId>`, not a bot-global routing toggle
- preserve each Agent's concrete model and route only its delegated native subagent spawns
- keep session `/auto` and `/auto off` as narrower overrides
- use atomic Agent + router configuration writes and per-key deep merge so concurrent edits to different Agents do not clobber each other

## Runtime contract

Companion model-router PR: https://github.com/SerendipityOneInc/zooclaw-extras/pull/214

Selection precedence is session override, then Agent mode, then routing off. The router evaluates every `sessions_spawn` independently. OpenClaw persists the selected concrete model on the child session. Explicit spawn models are preserved, and media-bearing spawns fail open unless the candidate declares all required input modalities.

## Verification

- [x] focused web verification: TypeScript, ESLint, 123 tests
- [x] focused backend model/router tests: 33 passed
- [x] related Agent and OpenClaw settings suites: 332 passed
- [x] full backend Pyright with a clean Python 3.12 environment: 0 errors
- [x] Ruff and import contracts
- [x] companion router tests: 189 passed, typecheck, lint, pre-push suite

The first local ECAP push attempt used the conda interpreter selected by `verify-py.sh`; that interpreter could not resolve the worktree environment. The same full Pyright command passed with the clean Python 3.12 environment used for the backend tests.


