---
title: "侧边栏历史会话显示更准确"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 侧边栏历史会话显示更准确

## 核心宣传点

没有聊天记录的 Agent 会清楚显示「No chats」，不再出现忽隐忽现的历史入口和假的任务记录。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`9e4df1d8f1061f2ffd419db5bf43050f7cf01edc`
- 作者：lynn Zhuang
- 日期：2026-08-05T10:16:00Z
- PR：#3253

### Commit Message

```
fix(chat): show No chats for empty agent history (#3253)

## Summary

- derive Session History visibility from an explicit default-DM history
fact instead of session-row count
- show a non-interactive `No chats` empty state when both DM history and
session rows are empty
- remove the expanded child `New Task` fallback while keeping the
agent-row pencil action as the creation entry point
- treat any stored DM post as history; no author, `Hi`, or `/new`
filtering
- preserve the legacy session-derived UI only when an older backend
omits `has_dm_history`, so independent frontend/backend rollout is safe

## Root cause

The sidebar used session-channel rows to infer whether the independent
default Mattermost DM had history. Those data sources can diverge, so
Session History appeared inconsistently. The zero-session fallback also
rendered a clickable New Task child that looked like a history record.

## Test plan

- [x] Backend DM-history and workspace-conversation tests: 36 passed
- [x] Frontend sidebar/query/council tests: 61 passed
- [x] Frontend TypeScript and ESLint checks
- [x] Backend Ruff check and format check
- [x] Backend Pyright with the worktree Python environment: 0 errors
- [x] Backend import-linter contracts: 8 kept
- [x] Synchronized the branch with `origin/main`; GitHub's merge-preview
checks also passed against current main
- [x] Added a regression test preserving cached `No chats` during a
failed background refresh
- [x] Added a regression test for a frontend-first rollout against an
older backend response

## Manual verification

1. Expand a new agent with no DM posts and no session rows; confirm `No
chats` is shown.
2. Confirm the empty state is not clickable and no child New Task row is
present.
3. Click the pencil icon, send a message, then confirm Session History
appears.
4. Confirm real session rows remain visible independently of default-DM
history.
```

### PR Body

## Summary

- derive Session History visibility from an explicit default-DM history fact instead of session-row count
- show a non-interactive `No chats` empty state when both DM history and session rows are empty
- remove the expanded child `New Task` fallback while keeping the agent-row pencil action as the creation entry point
- treat any stored DM post as history; no author, `Hi`, or `/new` filtering
- preserve the legacy session-derived UI only when an older backend omits `has_dm_history`, so independent frontend/backend rollout is safe

## Root cause

The sidebar used session-channel rows to infer whether the independent default Mattermost DM had history. Those data sources can diverge, so Session History appeared inconsistently. The zero-session fallback also rendered a clickable New Task child that looked like a history record.

## Test plan

- [x] Backend DM-history and workspace-conversation tests: 36 passed
- [x] Frontend sidebar/query/council tests: 61 passed
- [x] Frontend TypeScript and ESLint checks
- [x] Backend Ruff check and format check
- [x] Backend Pyright with the worktree Python environment: 0 errors
- [x] Backend import-linter contracts: 8 kept
- [x] Synchronized the branch with `origin/main`; GitHub's merge-preview checks also passed against current main
- [x] Added a regression test preserving cached `No chats` during a failed background refresh
- [x] Added a regression test for a frontend-first rollout against an older backend response

## Manual verification

1. Expand a new agent with no DM posts and no session rows; confirm `No chats` is shown.
2. Confirm the empty state is not clickable and no child New Task row is present.
3. Click the pencil icon, send a message, then confirm Session History appears.
4. Confirm real session rows remain visible independently of default-DM history.

