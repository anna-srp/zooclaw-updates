---
title: "Council 调研：每次运行独立线程，审批/取消更稳定"
type: "新功能上线"
priority: "中"
外部: "B"
date: "2026-07-30"
status: "待审核"
channels: ""
---

## 核心宣传点

Council 每次调研运行现在拥有专属的独立会话线程，审批与取消操作更可靠，历史调研记录清晰不串场。

## 原始内容

**Commit**: 374e610a (PR #3158)
**外部评级**: B | **内部**: P2 | **信息类型**: 新功能上线

### Commit Message

```
fix(council): preserve dedicated run thread identity (#3158)

## Summary

Second slice of #3139, stacked on #3157.

- Create an untracked Mattermost thread for each Council run without
adding it to normal Chat conversations.
- Resolve the exact owner-scoped main workspace, including migrated
Engine mains.
- Persist immutable workspace, channel, root-post, and bot-user thread
identity on the run.
- Use the persisted channel for later approval/cancel replies, with a
root-only fallback for pre-existing runs.
- Preserve stable Council-domain error codes from the backend.
- Keep independent web/backend rollout compatibility: only a generic
route-missing 404 may use the legacy conversation bootstrap.

The event-driven refresh and synthesis summary remain in later slices.

## Stack

1. #3157 — approval, depth, and tier intent
2. This PR — dedicated run thread identity
3. #3160 — event-driven status refresh
4. #3161 — terminal thread synthesis

Review and merge in that order.

## Test plan

- [x] 112 targeted backend tests
- [x] 69 selected frontend Council tests
- [x] `bash scripts/verify-web.sh ...` for the changed Council hooks,
models, services, and tests
- [x] Ruff check and format
- [x] Pyright: 0 errors, 0 warnings (explicit existing venv interpreter
for the new worktree)
- [x] Import-linter: 8 contracts kept
```

### PR Body

## Summary

Second slice of #3139, stacked on #3157.

- Create an untracked Mattermost thread for each Council run without adding it to normal Chat conversations.
- Resolve the exact owner-scoped main workspace, including migrated Engine mains.
- Persist immutable workspace, channel, root-post, and bot-user thread identity on the run.
- Use the persisted channel for later approval/cancel replies, with a root-only fallback for pre-existing runs.
- Preserve stable Council-domain error codes from the backend.
- Keep independent web/backend rollout compatibility: only a generic route-missing 404 may use the legacy conversation bootstrap.

The event-driven refresh and synthesis summary remain in later slices.

## Stack

1. #3157 — approval, depth, and tier intent
2. This PR — dedicated run thread identity
3. #3160 — event-driven status refresh
4. #3161 — terminal thread synthesis

Review and merge in that order.

## Test plan

- [x] 112 targeted backend tests
- [x] 69 selected frontend Council tests
- [x] `bash scripts/verify-web.sh ...` for the changed Council hooks, models, services, and tests
- [x] Ruff check and format
- [x] Pyright: 0 errors, 0 warnings (explicit existing venv interpreter for the new worktree)
- [x] Import-linter: 8 contracts kept

