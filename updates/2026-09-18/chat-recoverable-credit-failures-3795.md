---
title: "fix(chat): surface recoverable credit failures outside history (#3795)"
type: "Bug Fix"
priority: "高"
date: "2026-09-18"
status: "待审核"
channels: ""
---

# 修复：额度不足导致的运行失败不会再让对话卡在 Thinking

## 核心宣传点

此前托管 Agent 因为额度不足在输出任何文字之前就失败时，Builder 和聊天会一直停在 Thinking，既没有提示也没法继续发消息。现在终止状态会正确结束 Thinking 并恢复发送，旧轮次的迟到事件不会误清掉新轮次；额度/订阅相关的失败会在输入框上方显示本地化提示，并带一个直接进充值面板的入口。提示完全根据 error_code 判断，不依赖服务端文案。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已合并待发版

## PR 说明

## Problem and behavior
When a managed-agent run fails for insufficient credits before producing assistant text, Builder/chat can remain stuck on Thinking without recovery guidance.

- Correlated terminal status ends Thinking and restores sending even without assistant output. A late terminal event for an older turn cannot clear a newer turn.
- Show a localized credit/subscription notice above the shared composer, chosen entirely from `error_code`, with an entry to the existing billing panel. No server display copy is needed.
- Clear the notice only after a fresh successful `/users/credits/check` confirms usable credits and subscription. Stale positive cache, failed refreshes, and closing the billing panel do not dismiss it.
- Historical billing failures retain the short Failed status without a persistent recharge warning. No automatic payment or resend.

## Integration and scope
- Channel projection: https://github.com/SerendipityOneInc/agent-channel-service/pull/136 maps existing Engine `run.finished.terminalReason` to `error_code`.
- No Engine change or deployment required. Engine PR #1520 was closed without merging.
- Deploy web before the channel projection. Optional fields are backward compatible; no backfill or new normal chat message.
- Does not change gateway degradation/routing. Feedback appears when a run is actually rejected, not when a downgrade succeeds.

## Validation
- Previous revision: complete CI and both automatic reviews passed; 221 targeted frontend tests passed with 1 pre-existing skipped test.
- This revision adds code-only parsing coverage for both billing reasons and subscription-specific frontend copy; all 24 targeted tests passed. Complete CI and both automatic reviews passed on final commit `3c4325d13`.
- TypeScript, ESLint, and frontend governance gates run on push.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `edd8bb8bef71e7835ab207a9e6caf000ade1d24e`
- PR: #3795
- 作者：tim-srp
- 日期：2026-09-18T10:17:14Z

### Commit Message

```
fix(chat): surface recoverable credit failures outside history (#3795)

## Problem and behavior
When a managed-agent run fails for insufficient credits before producing
assistant text, Builder/chat can remain stuck on Thinking without
recovery guidance.

- Correlated terminal status ends Thinking and restores sending even
without assistant output. A late terminal event for an older turn cannot
clear a newer turn.
- Show a localized credit/subscription notice above the shared composer,
chosen entirely from `error_code`, with an entry to the existing billing
panel. No server display copy is needed.
- Clear the notice only after a fresh successful `/users/credits/check`
confirms usable credits and subscription. Stale positive cache, failed
refreshes, and closing the billing panel do not dismiss it.
- Historical billing failures retain the short Failed status without a
persistent recharge warning. No automatic payment or resend.

## Integration and scope
- Channel projection:
https://github.com/SerendipityOneInc/agent-channel-service/pull/136 maps
existing Engine `run.finished.terminalReason` to `error_code`.
- No Engine change or deployment required. Engine PR #1520 was closed
without merging.
- Deploy web before the channel projection. Optional fields are backward
compatible; no backfill or new normal chat message.
- Does not change gateway degradation/routing. Feedback appears when a
run is actually rejected, not when a downgrade succeeds.

## Validation
- Previous revision: complete CI and both automatic reviews passed; 221
targeted frontend tests passed with 1 pre-existing skipped test.
- This revision adds code-only parsing coverage for both billing reasons
and subscription-specific frontend copy; all 24 targeted tests passed.
Complete CI and both automatic reviews passed on final commit
`3c4325d13`.
- TypeScript, ESLint, and frontend governance gates run on push.
```

## 备注

发布状态：已合并待发版（尚未包含在任何 ecap-*-release tag 中，最新正式 release 为 ecap-v0.19.16-release）。

来源：SerendipityOneInc/ecap-workspace @ edd8bb8b，PR #3795，作者 tim-srp。
