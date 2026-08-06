---
title: "Agent Builder 自动恢复，模型选择更准确"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# Agent Builder 自动恢复，模型选择更准确

## 核心宣传点

切走再回到 Agent Builder 不会再卡在准备中需要手动刷新，模型列表也与常规对话保持一致。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`1f41a285f3d3a42a43bc7dfe67f74a4261fd415f`
- 作者：kaka-srp
- 日期：2026-08-05T09:31:12Z
- PR：#3254

### Commit Message

```
fix(agent-builder): recover V2 runtime and model selection (#3254)

## Summary

- keep Agent Builder V2 workspace access recoverable when a lease
renewal or runtime activation is temporarily unavailable
- make V2 model selection use the ordinary Engine-agent model catalog
and resolve public aliases to Engine provider IDs
- preserve activation compatibility for projects that already persisted
the historical Agent Studio model aliases, without exposing those
aliases for new selection
- hide the unsupported `auto` option in the V2 Builder composer by using
the same Engine runtime contract as ordinary Engine-agent chat

## Why

Returning to a backgrounded Builder page could leave it stuck in a
preparing/error state until a manual refresh. V2 Builder model selection
had also drifted from ordinary Engine-agent chat, while existing
projects still carried historical Agent Studio aliases. This change
restores automatic recovery and aligns new selections with the shared
catalog while keeping old projects usable during the catalog transition.

The two missing historical provider aliases were synchronized into the
staging Engine model catalog separately as operational data. This PR
does not introduce a second catalog source of truth.

## Scope

- Agent Builder V2 paths only
- Agent Builder V1 model resolution and runtime behavior are unchanged
- no changes to submitted-agent installation or post-submit workflows

## Validation

- `bash scripts/verify-web.sh` for the changed Builder files
- targeted frontend unit tests: 62 passed
- `bash scripts/verify-py.sh`
- targeted backend unit tests: 29 passed
- pre-push changed-surface verification passed after rebasing onto
current `origin/main`

## Design

-
`docs/superpowers/specs/2026-08-05-agent-builder-v2-recovery-model-artifact.md`
```

### PR Body

## Summary

- keep Agent Builder V2 workspace access recoverable when a lease renewal or runtime activation is temporarily unavailable
- make V2 model selection use the ordinary Engine-agent model catalog and resolve public aliases to Engine provider IDs
- preserve activation compatibility for projects that already persisted the historical Agent Studio model aliases, without exposing those aliases for new selection
- hide the unsupported `auto` option in the V2 Builder composer by using the same Engine runtime contract as ordinary Engine-agent chat

## Why

Returning to a backgrounded Builder page could leave it stuck in a preparing/error state until a manual refresh. V2 Builder model selection had also drifted from ordinary Engine-agent chat, while existing projects still carried historical Agent Studio aliases. This change restores automatic recovery and aligns new selections with the shared catalog while keeping old projects usable during the catalog transition.

The two missing historical provider aliases were synchronized into the staging Engine model catalog separately as operational data. This PR does not introduce a second catalog source of truth.

## Scope

- Agent Builder V2 paths only
- Agent Builder V1 model resolution and runtime behavior are unchanged
- no changes to submitted-agent installation or post-submit workflows

## Validation

- `bash scripts/verify-web.sh` for the changed Builder files
- targeted frontend unit tests: 62 passed
- `bash scripts/verify-py.sh`
- targeted backend unit tests: 29 passed
- pre-push changed-surface verification passed after rebasing onto current `origin/main`

## Design

- `docs/superpowers/specs/2026-08-05-agent-builder-v2-recovery-model-artifact.md`

