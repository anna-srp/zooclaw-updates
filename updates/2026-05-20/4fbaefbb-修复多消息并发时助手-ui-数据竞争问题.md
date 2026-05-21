---
title: "修复多消息并发时助手 UI 数据竞争问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "4fbaefbb279ed32d0959c210ebdd21dc2b450fd1"
pr: 1720
---
# 修复多消息并发时助手 UI 数据竞争问题

## 核心宣传点

修复了在连续发送多条消息时，助手界面可能出现混乱或响应错误的问题，对话体验更稳定。

## 原始内容

### Commit Message

```
fix(web): isolate assistant-ui tap-client-lookup race per message (#1720)

## Summary

Wraps each `ThreadPrimitive.Messages` factory in `OpenClawThread` with
an `AssistantUiTapErrorBoundary` so the `tapClientLookup: Index N out of
bounds (length: N)` race from `@assistant-ui/store` blanks **one message
for one frame** instead of unwinding the whole thread.

## Why

Production users hit `Error: tapClientLookup: Index 4 out of bounds
(length: 4)` (sample: `_next/static/chunks/84940-836478b108b3d5cc.js`) —
chat surface goes blank, retry doesn't recover. Source confirmed at
`@assistant-ui/store/src/tapClientLookup.ts:66`.

Upstream tracking (all open, no shipped fix on
`@assistant-ui/store@0.2.10`):
-
[assistant-ui/assistant-ui#4051](https://github.com/assistant-ui/assistant-ui/issues/4051)
— exactly our env (`useExternalStoreRuntime` + React 19, high-frequency
WS replacement)
- [#3968](https://github.com/assistant-ui/assistant-ui/issues/3968),
[#3652](https://github.com/assistant-ui/assistant-ui/issues/3652) —
older reports with the same `index === length` off-by-one
- Maintainer wants an architectural fix (stable ID-based keying) over a
suppression layer; PRs #3976 / #4000 closed unmerged; #4002 open

### Mechanism

`notifySubscribers` fires synchronously to every subscriber when the
external-store messages array shrinks (dedup in `useOpenClawRuntime`,
tool-status aggregation, session switch). A stale child subscription
reads `getSnapshot()` against the new (shorter) array before React
unmounts it → out-of-bounds throw, error bubbles to React's native
`useSyncExternalStore`, the Thread subtree unmounts.

In zooclaw this is reachable via:
- Session switch mid-stream (hire → navigate to new agent's
`/chat?agent_id=…` while WS frames are still arriving)
- Rapid replay on WS reconnect (OpenClaw history catch-up)
- Subagent-heavy turns (parent / child tool calls produce frequent
message-list mutations)

## Approach

Per upstream guidance: catch the specific error, drop one frame, reset
on next microtask so React commits the post-shrink array; let the next
render redraw against consistent state.

- **Selective**: matches only on `tapClientLookup` in the error message.
Non-target errors stash in state and re-throw in `render()` so the
global `ErrorBoundary` still handles real bugs.
- **Per-message scope**: wraps inside `BoundedUserMessage` /
`BoundedAssistantMessage` (stable module-level functions so
`ThreadPrimitive.Messages` doesn't see new component references each
render). A stale subscription blanks one bubble for one frame; the
thread, scroll position, and composer stay alive.
- **Telemetry**: Sentry `captureMessage('aui_tap_lookup_race',
level=warning, tags.boundary='aui_tap_lookup')` + `logger.warn` per
occurrence. Lets us measure how often this fires once deployed and
compare against upstream fix readiness.

## Files

| File | Change |
|---|---|
|
`web/app/src/app/[locale]/chat/components/AssistantUiTapErrorBoundary.tsx`
| New. Class component, selective catch + 0ms reset + Sentry warning |
| `web/app/src/app/[locale]/chat/components/OpenClawThread.tsx` | Add
`BoundedUserMessage` / `BoundedAssistantMessage` wrappers; swap into
`ThreadPrimitive.Messages` `components` |
|
`web/app/tests/unit/app/chat/AssistantUiTapErrorBoundary.unit.spec.tsx`
| New. Renders children, swallows tap-lookup, reports to Sentry,
recovers on next tick, bubbles non-target errors |

## Test plan

- [x] `pnpm vitest run
tests/unit/app/chat/AssistantUiTapErrorBoundary.unit.spec.tsx` — 5/5
pass
- [x] `pnpm vitest run tests/unit/app/chat` — 505/505 pass (no
regression in surrounding chat tests)
- [x] `pnpm tsc --noEmit` — clean
- [x] `pnpm lint` on changed files — clean (one unrelated pre-existing
`GenClawInput.tsx:493` prettier nit is on main, not touched here)
- [ ] CI `web-quality` green
- [ ] Manual: a single forced throw from a stale `useMessage()` call
should blank one bubble for ≤1 frame, not the thread
- [ ] Sentry: after deploy, watch for `aui_tap_lookup_race` warnings to
quantify rate

## Follow-ups (out of scope)

- Upstream `@assistant-ui/store` fix in #4002 or successor — replace
this boundary once shipped.
- `GenClawInput.tsx:493` prettier ordering — needs a separate cleanup,
untouched here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Wraps each `ThreadPrimitive.Messages` factory in `OpenClawThread` with an `AssistantUiTapErrorBoundary` so the `tapClientLookup: Index N out of bounds (length: N)` race from `@assistant-ui/store` blanks **one message for one frame** instead of unwinding the whole thread.

## Why

Production users hit `Error: tapClientLookup: Index 4 out of bounds (length: 4)` (sample: `_next/static/chunks/84940-836478b108b3d5cc.js`) — chat surface goes blank, retry doesn't recover. Source confirmed at `@assistant-ui/store/src/tapClientLookup.ts:66`.

Upstream tracking (all open, no shipped fix on `@assistant-ui/store@0.2.10`):
- [assistant-ui/assistant-ui#4051](https://github.com/assistant-ui/assistant-ui/issues/4051) — exactly our env (`useExternalStoreRuntime` + React 19, high-frequency WS replacement)
- [#3968](https://github.com/assistant-ui/assistant-ui/issues/3968), [#3652](https://github.com/assistant-ui/assistant-ui/issues/3652) — older reports with the same `index === length` off-by-one
- Maintainer wants an architectural fix (stable ID-based keying) over a suppression layer; PRs #3976 / #4000 closed unmerged; #4002 open

### Mechanism

`notifySubscribers` fires synchronously to every subscriber when the external-store messages array shrinks (dedup in `useOpenClawRuntime`, tool-status aggregation, session switch). A stale child subscription reads `getSnapshot()` against the new (shorter) array before React unmounts it → out-of-bounds throw, error bubbles to React's native `useSyncExternalStore`, the Thread subtree unmounts.

In zooclaw this is reachable via:
- Session switch mid-stream (hire → navigate to new agent's `/chat?agent_id=…` while WS frames are still arriving)
- Rapid replay on WS reconnect (OpenClaw history catch-up)
- Subagent-heavy turns (parent / child tool calls produce frequent message-list mutations)

## Approach

Per upstream guidance: catch the specific error, drop one frame, reset on next microtask so React commits the post-shrink array; let the next render redraw against consistent state.

- **Selective**: matches only on `tapClientLookup` in the error message. Non-target errors stash in state and re-throw in `render()` so the global `ErrorBoundary` still handles real bugs.
- **Per-message scope**: wraps inside `BoundedUserMessage` / `BoundedAssistantMessage` (stable module-level functions so `ThreadPrimitive.Messages` doesn't see new component references each render). A stale subscription blanks one bubble for one frame; the thread, scroll position, and composer stay alive.
- **Telemetry**: Sentry `captureMessage('aui_tap_lookup_race', level=warning, tags.boundary='aui_tap_lookup')` + `logger.warn` per occurrence. Lets us measure how often this fires once deployed and compare against upstream fix readiness.

## Files

| File | Change |
|---|---|
| `web/app/src/app/[locale]/chat/components/AssistantUiTapErrorBoundary.tsx` | New. Class component, selective catch + 0ms reset + Sentry warning |
| `web/app/src/app/[locale]/chat/components/OpenClawThread.tsx` | Add `BoundedUserMessage` / `BoundedAssistantMessage` wrappers; swap into `ThreadPrimitive.Messages` `components` |
| `web/app/tests/unit/app/chat/AssistantUiTapErrorBoundary.unit.spec.tsx` | New. Renders children, swallows tap-lookup, reports to Sentry, recovers on next tick, bubbles non-target errors |

## Test plan

- [x] `pnpm vitest run tests/unit/app/chat/AssistantUiTapErrorBoundary.unit.spec.tsx` — 5/5 pass
- [x] `pnpm vitest run tests/unit/app/chat` — 505/505 pass (no regression in surrounding chat tests)
- [x] `pnpm tsc --noEmit` — clean
- [x] `pnpm lint` on changed files — clean (one unrelated pre-existing `GenClawInput.tsx:493` prettier nit is on main, not touched here)
- [ ] CI `web-quality` green
- [ ] Manual: a single forced throw from a stale `useMessage()` call should blank one bubble for ≤1 frame, not the thread
- [ ] Sentry: after deploy, watch for `aui_tap_lookup_race` warnings to quantify rate

## Follow-ups (out of scope)

- Upstream `@assistant-ui/store` fix in #4002 or successor — replace this boundary once shipped.
- `GenClawInput.tsx:493` prettier ordering — needs a separate cleanup, untouched here.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
