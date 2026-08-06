---
title: "修复生成中「停止」按钮提前消失"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 修复生成中「停止」按钮提前消失

## 核心宣传点

长任务运行途中「停止」按钮不再提前变回发送键，整个生成过程都能随时叫停。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`0c96ce4ad077340861b15e3f42ba74611136e15f`
- 作者：kaka-srp
- 日期：2026-08-05T12:23:25Z
- PR：#3261

### Commit Message

```
fix(web): keep v2 stop available until terminal reply (#3261)

## Summary
- keep the v2 session composer in generating/Stop state through
intermediate assistant segments
- clear generation only on the same validated terminal assistant-segment
contract used by Agent Builder (`final`/`error`, `terminal=true`)
- reconcile the waiting state from persisted Mattermost thread history
after WebSocket reconnects, while keeping button-triggered `/stop`
hidden

## Root cause
The session page cleared `isWaitingForBotReply` on every ordinary bot
`posted` event. Engine v2 publishes intermediate assistant segments
before tool execution finishes, so the first segment replaced Stop with
the disabled send arrow even though the run was still active. A fixed
60-second fallback also expired during healthy long-running turns.

## Performance
- no polling, network request, or new timer
- ordinary event classification is constant-time metadata parsing
- history reconciliation is skipped while idle and reverse-scans only
back to the latest user post while waiting

## Test plan
- [x] `bash scripts/verify-web.sh <changed paths>` (TypeScript, 263
related tests, ESLint)
- [x] targeted state-machine and Agent Builder tests (203 tests)
- [x] `pnpm dup:tests`
- [x] `bash scripts/verify-changed.sh` after rebasing onto latest
`origin/main`
- [x] local `$code-review`: no findings
```

### PR Body

## Summary
- keep the v2 session composer in generating/Stop state through intermediate assistant segments
- clear generation only on the same validated terminal assistant-segment contract used by Agent Builder (`final`/`error`, `terminal=true`)
- reconcile the waiting state from persisted Mattermost thread history after WebSocket reconnects, while keeping button-triggered `/stop` hidden

## Root cause
The session page cleared `isWaitingForBotReply` on every ordinary bot `posted` event. Engine v2 publishes intermediate assistant segments before tool execution finishes, so the first segment replaced Stop with the disabled send arrow even though the run was still active. A fixed 60-second fallback also expired during healthy long-running turns.

## Performance
- no polling, network request, or new timer
- ordinary event classification is constant-time metadata parsing
- history reconciliation is skipped while idle and reverse-scans only back to the latest user post while waiting

## Test plan
- [x] `bash scripts/verify-web.sh <changed paths>` (TypeScript, 263 related tests, ESLint)
- [x] targeted state-machine and Agent Builder tests (203 tests)
- [x] `pnpm dup:tests`
- [x] `bash scripts/verify-changed.sh` after rebasing onto latest `origin/main`
- [x] local `$code-review`: no findings

