---
title: "修复：Agent Builder 初始化卡住不再无限等待，超时后可一键重试"
type: "Bug Fix"
priority: "高"
date: "2026-08-19"
status: "待审核"
channels: ""
---

# 修复：Agent Builder 初始化卡住不再无限等待，超时后可一键重试

## 核心宣传点

以前 Agent Builder 环境准备失败时，页面会一直停在「准备中」，既不报错也无法继续。现在设置了 15 分钟的准备上限，超过 1 分钟会给出等待说明，失败后直接提供「重试」按钮复用当前项目重新准备，不用重建 Agent。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5b15d93ad2dd1b4d63a6abf4a35952e7302794f3`
- PR: #3418
- 作者: kaka-srp
- 日期: 2026-08-19T04:09:47Z

### Commit Message

```
fix(agent-builder): add bounded setup recovery (#3418)

## Summary
- bound Engine v2 Agent Builder setup to a fifteen-minute attempt
deadline shared by background execution and state refresh
- add stable timeout/failure codes plus an owner-scoped retry action
that reuses the current project, fences stale setup writes, and
preserves lifecycle state
- show delayed preparation guidance after one minute, slow delayed
polling, and resynchronize ambiguous retry results
- add backend and frontend regression coverage for timeout, retry,
concurrency, polling, and UI recovery

## Root cause
Retryable Engine v2 setup failures left the persisted workspace state at
`installing`. Project-state polling kept scheduling background setup,
but there was no attempt timestamp, bounded terminal transition, or
explicit retry action. The frontend therefore continued showing the
initial preparation state without time-based progress guidance or an
in-place recovery path.

The initial five-minute recovery window was also shorter than the Engine
environment-replacement client's 390-second timeout. The final
implementation uses one fifteen-minute attempt deadline for both the
background setup execution and persisted state convergence, while
retaining the one-minute delayed-preparation notice.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] related backend unit tests: 243 passed
- [x] related frontend unit tests: 94 passed
- [x] `bash scripts/verify-py.sh`
- [x] frontend TypeScript, ESLint, and governance guards
- [x] Python complexity check
- [x] `git diff --check`
```

### PR Body

## Summary
- bound Engine v2 Agent Builder setup to a fifteen-minute attempt deadline shared by background execution and state refresh
- add stable timeout/failure codes plus an owner-scoped retry action that reuses the current project, fences stale setup writes, and preserves lifecycle state
- show delayed preparation guidance after one minute, slow delayed polling, and resynchronize ambiguous retry results
- add backend and frontend regression coverage for timeout, retry, concurrency, polling, and UI recovery

## Root cause
Retryable Engine v2 setup failures left the persisted workspace state at `installing`. Project-state polling kept scheduling background setup, but there was no attempt timestamp, bounded terminal transition, or explicit retry action. The frontend therefore continued showing the initial preparation state without time-based progress guidance or an in-place recovery path.

The initial five-minute recovery window was also shorter than the Engine environment-replacement client's 390-second timeout. The final implementation uses one fifteen-minute attempt deadline for both the background setup execution and persisted state convergence, while retaining the one-minute delayed-preparation notice.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] related backend unit tests: 243 passed
- [x] related frontend unit tests: 94 passed
- [x] `bash scripts/verify-py.sh`
- [x] frontend TypeScript, ESLint, and governance guards
- [x] Python complexity check
- [x] `git diff --check`

