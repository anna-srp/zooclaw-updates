---
title: 定时任务（cron-job）技能升级 v2.3：飞书定时消息校验更可靠、更新提示不再误伤权限
type: Skill 上架/更新
priority: 中
外部: "B"
date: 2026-07-28
status: 待审核
channels: ""
---

## 核心宣传点

定时任务技能升级到 v2.3：给飞书/Lark 设定时消息时，校验会正确识别同一个收件人（不再因目标写法差异被误判为“未通过”）；只改定时任务的提示词时，不会再悄悄放宽工具权限或改动模型等设置；校验测试也改用独立会话，不会打扰你真实的对话。整体让定时任务用起来更稳、更安全。

## 原始内容

**Commit:** 7d63ca145a... (PR #243, ecap-skills) by sharplee-srp @ 2026-07-28T02:33:50Z

```
fix(cron-job): harden route and payload updates (#243)

## What changed

- Canonicalize Feishu/Lark route identities before comparing declared message sinks with `messageToolSentTo` run evidence.
- Preserve `chat_id`, `open_id`, and `user_id` distinctions, and make already-canonical targets idempotent.
- Reuse the canonical route key for duplicate test-sink and live/test overlap checks.
- Preserve existing `agentTurn` payload controls when changing `agentMessage`, including tool allowlists, model selection, thinking level, fallbacks, and timeout unless explicitly overridden.
- Force disposable jobs into an isolated session, remove inherited session keys, and strip live routing context from completion-free tests.
- Require a request-only `delivery.testTo` sink for completion-only `announce` tests; strip it from the final job and substitute it only into the disposable copy.
- Keep every other channel on exact target comparison and bump `cron-job` to version 2.3.

## Root causes

OpenClaw accepts a Feishu target such as `user:ou_xxx`, but cron run history records the successfully sent target as the provider-normalized bare Open ID `ou_xxx`. The driver compared those strings literally and returned `needs_agent` even though the channel, account, target type, and ID matched.

When updating an existing job's `agentMessage`, the driver rebuilt the whole payload from three fields. That discarded existing safety and runtime controls such as `toolsAllow`, model, thinking level, fallbacks, and the previous timeout.

Disposable copies also inherited concrete live `sessionTarget` / `sessionKey` values. Completion-only `announce` jobs had no separate test recipient, so a forced validation run could reuse a real conversation or notify the live destination.

## User impact

Valid Feishu cron message tests can now reach `validated` when OpenClaw records a canonical bare target. A different recipient, account, channel, or Feishu target kind still fails closed.

Prompt-only updates no longer silently broaden tool access or change unrelated model/runtime behavior.

Validation runs now use a fresh isolated session and an explicit sink while final jobs preserve their authorized live session and recipient.
```
