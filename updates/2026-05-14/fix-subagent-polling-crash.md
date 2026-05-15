---
title: "修复 Subagent 轮询引发服务崩溃的 Bug"
type: "Bug Fix"
priority: "高"
date: "2026-05-14"
status: "待审核"
channels: ""
---
# 修复 Subagent 轮询引发服务崩溃的 Bug

## 核心宣传点

修复了 Subagent 运行时因频繁轮询导致服务卡顿甚至崩溃重启的严重问题，AI 任务运行更稳定，不再出现莫名断开或超时。

## 原始内容

**Commit**: de5589f4 | refactor(web): subagent sessions event subscription (ECA-662) (#1609)

**Commit Message**:
```
refactor(web): subagent sessions event subscription (ECA-662) (#1609)
```

**PR Body**:
## Summary

Replace the 3s `sessions.list` polling loop with `sessions.subscribe` + `sessions.changed` push events to stop overwhelming OpenClaw bot gateways. Drop three defensive `chat.history` reloads that were redundant with the streaming/event path. All review-cycle follow-ups (epoch counter, fallback polling, closure-leak guard) included.

- **Root cause**: clients polled `sessions.list` every 3s while bot generated; JuiceFS lock contention spiked, Node event loop blocked, liveness probes timed out → kubelet SIGKILL (Exit 137). See [ECA-662](https://linear.app/srpone/issue/ECA-662).
- **Mechanism**: OpenClaw 2026.4.2+ emits `sessions.changed` on subagent create / status-change / message; verified in production via `openclaw gateway call sessions.subscribe --params '{}' --json` → `{"subscribed": true}`.
- **Impact**: eliminates the primary source of gateway overload during concurrent subagent runs; removes ~150ms latency added by the polling interval.

## Test plan

- [x] Subagent run visible in panel without polling (events fire correctly)
- [x] Fallback polling still kicks in after 30s if no events arrive
- [x] No closure leak: unsubscribe called on unmount
- [x] `pnpm lint` / `tsc --noEmit` clean
