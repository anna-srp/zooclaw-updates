---
title: "修复切换标签页后聊天连接断开的问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 修复切换标签页后聊天连接断开的问题

## 核心宣传点

修复了从其他标签页切回聊天时，消息连接中断导致收不到回复的问题，现在切回后会自动重连恢复正常。

## 原始内容

**Commit**: 23b6a5e78031f230e4162d316115aca91834fc26
**Author**: Chris@ZooClaw
**Date**: 2026-05-22T06:20:05Z
**PR**: #1844

### Commit Message
```
fix(chat): recover Mattermost reconnect on tab resume (#1844)

## Summary
- Recover Mattermost WebSocket when returning to a tab after a stale
hidden interval.
- Re-arm Mattermost reconnect after retry exhaustion while the tab was
hidden or backgrounded.
- Track low-level Mattermost WS activity, including ping replies, so
healthy quiet sockets are not treated as stale.
- Avoid recursive reconnect scheduling when intentionally replacing a
stale Mattermost socket.

## Root cause
Mattermost chat depended on the browser delivering WebSocket close
events to enter its reconnect loop. Backgrounded tabs throttle timers
and can return with a stale socket still marked connected, or with
reconnect attempts already exhausted. Unlike the OpenClaw WS path, the
Mattermost path had no visible-tab recovery probe. The stale detector
now keys off any valid WS frame, not just user-facing Mattermost events,
so ping replies keep healthy idle sockets fresh.

## Review-driven fixes
- Addressed Codex review feedback that event-only freshness would
reconnect healthy quiet channels because Mattermost seq_reply ping
responses were ignored before onEvent.
- Added MattermostWebSocketService.onActivity and a regression test
proving idle ping activity prevents unnecessary visible-tab reconnect.

## Test plan
- [x] pnpm --dir web/app exec vitest run
tests/unit/hooks/useMattermost.unit.spec.ts
- [x] pnpm --dir web/app exec eslint src/hooks/useMattermost.ts
src/lib/mattermost/websocket.ts
tests/unit/hooks/useMattermost.unit.spec.ts
- [x] pnpm --dir web exec tsc --noEmit --project app/tsconfig.json
- [x] pnpm --dir web/app run lint
- [x] pnpm --dir web/app run test:unit
- [ ] pnpm --dir web run lint (blocked locally by
web/packages/auth-client missing typescript-eslint; web/app lint passed)
- [ ] pnpm --dir web run test:unit (one local recursive run exited
nonzero on jsdom navigation noise; direct web/app unit suite passed and
CI web-quality/test is authoritative)
```

### PR Description
## Summary
- Recover Mattermost WebSocket when returning to a tab after a stale hidden interval.
- Re-arm Mattermost reconnect after retry exhaustion while the tab was hidden or backgrounded.
- Track low-level Mattermost WS activity, including ping replies, so healthy quiet sockets are not treated as stale.
- Avoid recursive reconnect scheduling when intentionally replacing a stale Mattermost socket.

## Root cause
Mattermost chat depended on the browser delivering WebSocket close events to enter its reconnect loop. Backgrounded tabs throttle timers and can return with a stale socket still marked connected, or with reconnect attempts already exhausted. Unlike the OpenClaw WS path, the Mattermost path had no visible-tab recovery probe. The stale detector now keys off any valid WS frame, not just user-facing Mattermost events, so ping replies keep healthy idle sockets fresh.

## Review-driven fixes
- Addressed Codex review feedback that event-only freshness would reconnect healthy quiet channels because Mattermost seq_reply ping responses were ignored before onEvent.
- Added MattermostWebSocketService.onActivity and a regression test proving idle ping activity prevents unnecessary visible-tab reconnect.

## Test plan
- [x] pnpm --dir web/app exec vitest run tests/unit/hooks/useMattermost.unit.spec.ts
- [x] pnpm --dir web/app exec eslint src/hooks/useMattermost.ts src/lib/mattermost/websocket.ts tests/unit/hooks/useMattermost.unit.spec.ts
- [x] pnpm --dir web exec tsc --noEmit --project app/tsconfig.json
- [x] pnpm --dir web/app run lint
- [x] pnpm --dir web/app run test:unit
- [ ] pnpm --dir web run lint (blocked locally by web/packages/auth-client missing typescript-eslint; web/app lint passed)
- [ ] pnpm --dir web run test:unit (one local recursive run exited nonzero on jsdom navigation noise; direct web/app unit suite passed and CI web-quality/test is authoritative)

