---
title: "Mattermost 聊天连接稳定性增强：自动检测并恢复掉线"
type: "体验优化"
priority: "中"
date: "2026-06-23"
status: "待审核"
channels: ""
---
# Mattermost 聊天连接稳定性增强：自动检测并恢复掉线

## 核心宣传点
聊天连接更稳定，遇到「假死」掉线会自动检测并重连，减少需要手动刷新页面才恢复的情况。

## 原始内容
```
feat(web): mattermost ws observability + keepalive watchdog & online/stale recovery (#2558)

## Summary

Two parts for ECA-1037, kept in one PR:

**1. Observability (was PR1)**
- enrich existing `mm.connection.transition` logs with Mattermost
browser WS diagnostics
- record connection age, last pong age, close metadata, readyState, and
tab visibility on existing transition events

**2. Recovery (the fix the observability was meant to inform)**
- **keepalive watchdog** (`websocket.ts`): after `MAX_MISSED_PONGS` (2)
unanswered keepalive pings (~30s), the socket is treated as a half-open
zombie — the browser never fires `onclose` for these — so we stop
pinging the dead socket and notify `onStale` consumers.
- **stale recovery** (`useMattermostConnection.ts`): `onStale` →
`forceReconnect('stale_timeout')`. Previously a visible-tab zombie was
only caught on the next tab refocus; now it self-heals while visible.
- **online recovery**: an `online` window listener →
`forceReconnect('online_retry')` revives a reconnect-exhausted
connection the moment the browser regains network, instead of waiting
for a tab refocus.
- two new transition reasons `stale_timeout` / `online_retry` (both
classified as anomalies) so Sentry can distinguish watchdog-driven and
network-recovery transitions.

Net: connection drops are now both *measured* (close-driven, zombie,
exhaustion, age distribution) and *recovered* (close → backoff
reconnect, zombie → watchdog reconnect, exhaustion → online/visibility
resume).

Linear: https://linear.app/srpone/issue/ECA-1037

## Tests

- devcontainer unit: `pnpm exec vitest run
tests/unit/lib/mattermost/websocket.unit.spec.ts
tests/unit/hooks/mattermost/useMattermostConnection.unit.spec.ts
tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts` (79
passed) — adds watchdog fire/no-fire, `stale_timeout`, `online_retry`,
and online-while-connected no-op cases
- devcontainer: `pnpm exec tsc --noEmit`; targeted ESLint on modified
files
- **Real staging E2E** (devcontainer + live staging bot `31b7ba01…`):
drove the real chat path against the real Mattermost socket and
confirmed the new diagnostics populate on (a) a client-injected
`close(4001)` drop (`was_clean=true`) and (b) a spontaneous real `1006`
drop (`was_clean=false`), plus `last_pong_age_ms` populating after a
real ping/pong and clean `reconnected` recovery.

## Out of scope

UI surface for the disconnected/exhausted state and any server-side
(Mattermost/LB) keepalive tuning — separate follow-ups if needed.
```

### PR description
## Summary

Two parts for ECA-1037, kept in one PR:

**1. Observability (was PR1)**
- enrich existing `mm.connection.transition` logs with Mattermost browser WS diagnostics
- record connection age, last pong age, close metadata, readyState, and tab visibility on existing transition events

**2. Recovery (the fix the observability was meant to inform)**
- **keepalive watchdog** (`websocket.ts`): after `MAX_MISSED_PONGS` (2) unanswered keepalive pings (~30s), the socket is treated as a half-open zombie — the browser never fires `onclose` for these — so we stop pinging the dead socket and notify `onStale` consumers.
- **stale recovery** (`useMattermostConnection.ts`): `onStale` → `forceReconnect('stale_timeout')`. Previously a visible-tab zombie was only caught on the next tab refocus; now it self-heals while visible.
- **online recovery**: an `online` window listener → `forceReconnect('online_retry')` revives a reconnect-exhausted connection the moment the browser regains network, instead of waiting for a tab refocus.
- two new transition reasons `stale_timeout` / `online_retry` (both classified as anomalies) so Sentry can distinguish watchdog-driven and network-recovery transitions.

Net: connection drops are now both *measured* (close-driven, zombie, exhaustion, age distribution) and *recovered* (close → backoff reconnect, zombie → watchdog reconnect, exhaustion → online/visibility resume).

Linear: https://linear.app/srpone/issue/ECA-1037

## Tests

- devcontainer unit: `pnpm exec vitest run tests/unit/lib/mattermost/websocket.unit.spec.ts tests/unit/hooks/mattermost/useMattermostConnection.unit.spec.ts tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts` (79 passed) — adds watchdog fire/no-fire, `stale_timeout`, `online_retry`, and online-while-connected no-op cases
- devcontainer: `pnpm exec tsc --noEmit`; targeted ESLint on modified files
- **Real staging E2E** (devcontainer + live staging bot `31b7ba01…`): drove the real chat path against the real Mattermost socket and confirmed the new diagnostics populate on (a) a client-injected `close(4001)` drop (`was_clean=true`) and (b) a spontaneous real `1006` drop (`was_clean=false`), plus `last_pong_age_ms` populating after a real ping/pong and clean `reconnected` recovery.

## Out of scope

UI surface for the disconnected/exhausted state and any server-side (Mattermost/LB) keepalive tuning — separate follow-ups if needed.

