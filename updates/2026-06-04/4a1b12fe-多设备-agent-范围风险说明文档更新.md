---
title: "多设备 Agent 范围风险说明文档更新"
type: "产品基础功能更新"
priority: "低"
date: "2026-06-04"
status: "待审核"
channels: ""
sha: "4a1b12fe27b41585c01fb8f412d9b62c6bb8e244"
repo: "ecap-workspace"
pr: "2191"
---

# 多设备 Agent 范围风险说明文档更新

## 核心宣传点

内部技术文档更新，记录多电脑场景下 Agent 配置的注意事项，为后续多设备功能做准备。

## 原始内容

### Commit Message

```
docs(claw-interface): note multi-computer scoping risk on drop-bots plan (#2191)

## Summary

Records two transitional **open design risks** on the OpenClaw
legacy-removal plan, surfaced by review of the v2 read-flip (#2176).
Docs only — no code.

- **Multi-computer scoping:** the v2 read path resolves "the bot" as the
*oldest* computer, while the dual-write scopes to
`openclaw_bots[0].bot_id`. These diverge on multi-computer accounts (now
reachable via `POST /computer`). The legacy-removal redesign must
replace "primary computer = the bot" with explicit per-bot/per-computer
scope.
- **Phantom legacy bot:** V2-only `provision_agent_mm` still writes
`openclaw_bots.0` unconditionally; the legacy-write destination needs a
guard once legacy bots aren't guaranteed.

These are accepted transitional limitations for the read-flip; this note
ensures the redesign addresses them.

## Test plan
- [x] Docs only — no code/CI test impact
```

### PR Description

## Summary

Records two transitional **open design risks** on the OpenClaw legacy-removal plan, surfaced by review of the v2 read-flip (#2176). Docs only — no code.

- **Multi-computer scoping:** the v2 read path resolves "the bot" as the *oldest* computer, while the dual-write scopes to `openclaw_bots[0].bot_id`. These diverge on multi-computer accounts (now reachable via `POST /computer`). The legacy-removal redesign must replace "primary computer = the bot" with explicit per-bot/per-computer scope.
- **Phantom legacy bot:** V2-only `provision_agent_mm` still writes `openclaw_bots.0` unconditionally; the legacy-write destination needs a guard once legacy bots aren't guaranteed.

These are accepted transitional limitations for the read-flip; this note ensures the redesign addresses them.

## Test plan
- [x] Docs only — no code/CI test impact
