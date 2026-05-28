---
title: "聊天界面稳定性提升：修复过时回调引发的状态异常"
type: "Bug Fix"
priority: "中"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# 聊天界面稳定性提升：修复过时回调引发的状态异常

## 核心宣传点

修复了聊天页面因内部状态管理问题偶发的数据显示异常，界面响应更加稳定。

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**SHA**: [0318bb11](https://github.com/SerendipityOneInc/ecap-workspace/commit/0318bb11eb15e0e25f4d4785fcf26987fa7c62a0)
**PR**: [#1974](https://github.com/SerendipityOneInc/ecap-workspace/pull/1974)  
**作者**: Chris@ZooClaw  
**日期**: 2026-05-27T08:29:59Z

**Commit Message:**

```
fix(web): tighten OpenClawProvider consumer/callee corners around stale closures and silent failures (#1974)

## Summary

Audit follow-up to PR #1970 (#1959 OpenClawProvider reducer refactor).
Provider本体 + sub-hooks + reducer 都已干净;本 PR 收 4 个周边代码 audit 出来的 quick
wins。

### 1. `useOpenClawInit` auto-retry stale uid guard (HIGH — real bug)

`web/app/src/hooks/useOpenClawInit.ts:275-282`

The 1s `setTimeout` that retries `doInit(targetUid)` on auth errors
captured a stale `targetUid`. If a user logged out and re-logged in as a
different user within that 1s window, the pending retry fired `doInit`
against the old uid. Fix: gate the retry on `uidRef.current ===
targetUid`; when the uid drifted, let the regular auto-init `useEffect`
handle the new uid.

### 2. `FeedbackDialog` derived state during render (HIGH — UX race)

`web/app/src/components/feedback/FeedbackDialog.tsx:46-64`

A new `crashInfo` reset the dialog state via `useEffect`, leaving one
render where the dialog showed stale messages between mount and effect
flush — race window for user clicks during crash arrival. Switched to
React's
[recommended](https://react.dev/learn/you-might-not-need-an-effect#adjusting-some-state-when-a-prop-changes)
"store previous prop in state + compare during render" pattern so reset
is atomic with the render that observes the new crash. Also extracted
`buildCrashGreeting` / `buildGreeting` helpers to dedupe inline message
construction (saves ~25 lines).

### 3. `RestartPromptModal` silent redeploy failure (MED — silent bug)

`web/app/src/components/RestartPromptModal.tsx:21-35`

`await openClaw.redeploy()` inside `try/finally` swallowed rejections —
modal closed showing "done" even when the restart actually failed. Added
a catch clause that surfaces an error toast via `showToast(...,
'error')` and keeps the modal open so the user can retry.

### 4. `ArchivedSessionPanel` discarded `useOpenClaw()` call (MED —
cleanup)

`web/app/src/app/[locale]/session-history/ArchivedSessionPanel.tsx:110`

The archive page called `useOpenClaw()` purely for the implicit
activation side-effect with no use of the return value — wasted a
WebSocket connection while the user browsed past sessions. Dropped the
call; activation fires naturally when the user navigates back to
`/chat`.

## Test plan

- [x] `pnpm test:unit` — 5974 tests pass (+ 1 todo). New regression
tests:
- `useOpenClawInit-extras.unit.spec.ts`: auth-error auto-retry happy
path + uid-swap-mid-retry guard
- `FeedbackDialog.unit.spec.tsx`: null→crash atomic transition +
crash→new-crash full reset
- `RestartPromptModal.unit.spec.tsx`: 7 cases including the
silent-failure regression
- [x] `pnpm lint` clean
- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm dup` under threshold (tests 5.93%, src 3.68%)
- [ ] Manual: trigger a crash → verify dialog shows crash content
without flicker
- [ ] Manual: mock backend 500 on redeploy → verify error toast surfaces

## Out of scope (登记 follow-up issue)

Two larger refactor opportunities were identified in the audit but
deferred:
- `useOpenClawInit` 4 sentinel refs → reducer (#1959 同款模板，单独 issue)
- `AgentsManagerClient` modal state → discriminated union (减少
useCallback dep churn，单独 issue)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```


**PR Description:**

## Summary

Audit follow-up to PR #1970 (#1959 OpenClawProvider reducer refactor). Provider本体 + sub-hooks + reducer 都已干净;本 PR 收 4 个周边代码 audit 出来的 quick wins。

### 1. `useOpenClawInit` auto-retry stale uid guard (HIGH — real bug)

`web/app/src/hooks/useOpenClawInit.ts:275-282`

The 1s `setTimeout` that retries `doInit(targetUid)` on auth errors captured a stale `targetUid`. If a user logged out and re-logged in as a different user within that 1s window, the pending retry fired `doInit` against the old uid. Fix: gate the retry on `uidRef.current === targetUid`; when the uid drifted, let the regular auto-init `useEffect` handle the new uid.

### 2. `FeedbackDialog` derived state during render (HIGH — UX race)

`web/app/src/components/feedback/FeedbackDialog.tsx:46-64`

A new `crashInfo` reset the dialog state via `useEffect`, leaving one render where the dialog showed stale messages between mount and effect flush — race window for user clicks during crash arrival. Switched to React's [recommended](https://react.dev/learn/you-might-not-need-an-effect#adjusting-some-state-when-a-prop-changes) "store previous prop in state + compare during render" pattern so reset is atomic with the render that observes the new crash. Also extracted `buildCrashGreeting` / `buildGreeting` helpers to dedupe inline message construction (saves ~25 lines).

### 3. `RestartPromptModal` silent redeploy failure (MED — silent bug)

`web/app/src/components/RestartPromptModal.tsx:21-35`

`await openClaw.redeploy()` inside `try/finally` swallowed rejections — modal closed showing "done" even when the restart actually failed. Added a catch clause that surfaces an error toast via `showToast(..., 'error')` and keeps the modal open so the user can retry.

### 4. `ArchivedSessionPanel` discarded `useOpenClaw()` call (MED — cleanup)

`web/app/src/app/[locale]/session-history/ArchivedSessionPanel.tsx:110`

The archive page called `useOpenClaw()` purely for the implicit activation side-effect with no use of the return value — wasted a WebSocket connection while the user browsed past sessions. Dropped the call; activation fires naturally when the user navigates back to `/chat`.

## Test plan

- [x] `pnpm test:unit` — 5974 tests pass (+ 1 todo). New regression tests:
  - `useOpenClawInit-extras.unit.spec.ts`: auth-error auto-retry happy path + uid-swap-mid-retry guard
  - `FeedbackDialog.unit.spec.tsx`: null→crash atomic transition + crash→new-crash full reset
  - `RestartPromptModal.unit.spec.tsx`: 7 cases including the silent-failure regression
- [x] `pnpm lint` clean
- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm dup` under threshold (tests 5.93%, src 3.68%)
- [ ] Manual: trigger a crash → verify dialog shows crash content without flicker
- [ ] Manual: mock backend 500 on redeploy → verify error toast surfaces

## Out of scope (登记 follow-up issue)

Two larger refactor opportunities were identified in the audit but deferred:
- `useOpenClawInit` 4 sentinel refs → reducer (#1959 同款模板，单独 issue)
- `AgentsManagerClient` modal state → discriminated union (减少 useCallback dep churn，单独 issue)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
