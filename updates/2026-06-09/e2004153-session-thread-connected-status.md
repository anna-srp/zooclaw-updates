---
title: "会话线程页正确显示「已连接」状态"
type: "Bug Fix"
priority: "中"
date: "2026-06-09"
status: "待审核"
channels: ""
---

# 会话线程页正确显示「已连接」状态

## 核心宣传点

在会话线程页里，连接状态会正确显示为「已连接」，不再明明能正常收发消息却错误地显示「未连接」。

## 原始内容

完整 commit message：

```
fix(web): show connected status on session threads (#2316)

## Summary
- Fix the `/new-chat` session-thread header status so it uses the
route-scoped computer id before the OpenClaw provider snapshot hydrates.
- Pass a small explicit connection status source through
`SessionThreadClient -> ChatHeader -> ClawPageHeader ->
ClawConnectionStatus`.
- Add local staging validation reports for `/chat`, refactor-impact
routes, and the `/new-chat` status fix.

## Root cause
Session-thread routes already know the correct `computerId` from the URL
and can send replies through the Mattermost token, but the shared header
status pill only derived its computer id from `OpenClawContext.oc.bot`.
On session-thread pages that provider snapshot can be missing or late,
so the status pill had no computer id, never polled
`/api/openclaw/computers/:computerId/status`, and fell back to
`Disconnected` even though the thread and send path worked.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/components/ClawPageHeader-extras.unit.spec.tsx
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `pnpm run lint`
- [x] `pnpm exec tsc --noEmit --project app/tsconfig.json`
- [x] `env NODE_OPTIONS='--no-deprecation --no-experimental-webstorage'
pnpm exec vitest run --config ./vitest.config.mts`
- [x] Local `pnpm dev:staging` with Chrome CDP: same session-thread
route changed from `Disconnected` to `Claw Connected`; composer visible;
thread not loading/not-found.

Reports:
-
`docs/staging-validation/2026-06-10-chat-route-refactor-staging-report.md`
-
`docs/staging-validation/2026-06-10-web-app-refactor-impact-staging-report.md`
-
`docs/staging-validation/2026-06-10-new-chat-status-fix-local-report.md`
```

PR 描述：

## Summary
- Fix the `/new-chat` session-thread header status so it uses the route-scoped computer id before the OpenClaw provider snapshot hydrates.
- Pass a small explicit connection status source through `SessionThreadClient -> ChatHeader -> ClawPageHeader -> ClawConnectionStatus`.
- Add local staging validation reports for `/chat`, refactor-impact routes, and the `/new-chat` status fix.

## Root cause
Session-thread routes already know the correct `computerId` from the URL and can send replies through the Mattermost token, but the shared header status pill only derived its computer id from `OpenClawContext.oc.bot`. On session-thread pages that provider snapshot can be missing or late, so the status pill had no computer id, never polled `/api/openclaw/computers/:computerId/status`, and fell back to `Disconnected` even though the thread and send path worked.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/components/ClawPageHeader-extras.unit.spec.tsx tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `pnpm run lint`
- [x] `pnpm exec tsc --noEmit --project app/tsconfig.json`
- [x] `env NODE_OPTIONS='--no-deprecation --no-experimental-webstorage' pnpm exec vitest run --config ./vitest.config.mts`
- [x] Local `pnpm dev:staging` with Chrome CDP: same session-thread route changed from `Disconnected` to `Claw Connected`; composer visible; thread not loading/not-found.

Reports:
- `docs/staging-validation/2026-06-10-chat-route-refactor-staging-report.md`
- `docs/staging-validation/2026-06-10-web-app-refactor-impact-staging-report.md`
- `docs/staging-validation/2026-06-10-new-chat-status-fix-local-report.md`

