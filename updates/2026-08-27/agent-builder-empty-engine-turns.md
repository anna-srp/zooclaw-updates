---
title: "修复：Agent Builder 预览里 Agent 干完活却不「收尾」，一直显示进行中"
type: "Bug Fix"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 修复：Agent Builder 预览里 Agent 干完活却不「收尾」，一直显示进行中

## 核心宣传点

在 Agent Builder 预览中，如果 Agent 只调用了工具、最后没有输出可见回复，这一轮就永远不会被判定为结束，界面一直卡在进行中，刷新页面也一样。现在只要收到终止状态就正常收尾，并明确显示「已完成，但没有可见回复」；工具执行过程的中间消息也不会再被误当成 Agent 的正式回答。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `7b8524d3067c65774fb0cbc4d79e24feebcd4e61`
- PR: #3539
- 作者: kaka-srp
- 日期: 2026-08-27T03:34:44Z

### Commit Message

```
fix(agent-builder): finish empty engine turns (#3539)

## Summary

- Accept hidden `custom_turn_status` posts in Agent Builder monitoring
and finalization.
- Treat a terminal status as the end of an Engine preview turn even when
the assistant produces no visible response.
- Keep tool-progress posts out of visible-reply detection and show the
completed-without-visible-response state.

## Root cause

Agent Builder depended on a terminal assistant segment to end an Engine
preview turn. Runs that emitted tool progress and then finished without
a visible assistant segment never reached that boundary; tool metadata
could also be mistaken for an assistant delivery. Refreshing reloaded
the same incomplete event history, so it did not resolve the stuck
state.

## Scope

- ECAP consumer changes only; no Engine changes.
- Agent Builder monitor/finalizer, preview state derivation, and shared
chat message labeling.
- Producer PR:
https://github.com/SerendipityOneInc/agent-channel-service/pull/94

## Test plan

- [x] Targeted claw-interface tests (207 passed)
- [x] Agent Builder terminal-status component regression (1 passed)
- [x] Turn-status parser regression (1 passed)
- [x] Shared chat message-helper tests (12 passed)
- [ ] Full local suite intentionally skipped at request; PR CI is
authoritative.

## Rollout

Deploy this backward-compatible consumer first, then the linked Agent
Channel Service producer.
```

### PR Description

```
## Summary

- Accept hidden `custom_turn_status` posts in Agent Builder monitoring and finalization.
- Treat a terminal status as the end of an Engine preview turn even when the assistant produces no visible response.
- Keep tool-progress posts out of visible-reply detection and show the completed-without-visible-response state.

## Root cause

Agent Builder depended on a terminal assistant segment to end an Engine preview turn. Runs that emitted tool progress and then finished without a visible assistant segment never reached that boundary; tool metadata could also be mistaken for an assistant delivery. Refreshing reloaded the same incomplete event history, so it did not resolve the stuck state.

## Scope

- ECAP consumer changes only; no Engine changes.
- Agent Builder monitor/finalizer, preview state derivation, and shared chat message labeling.
- Producer PR: https://github.com/SerendipityOneInc/agent-channel-service/pull/94

## Test plan

- [x] Targeted claw-interface tests (207 passed)
- [x] Agent Builder terminal-status component regression (1 passed)
- [x] Turn-status parser regression (1 passed)
- [x] Shared chat message-helper tests (12 passed)
- [ ] Full local suite intentionally skipped at request; PR CI is authoritative.

## Rollout

Deploy this backward-compatible consumer first, then the linked Agent Channel Service producer.

```

---
