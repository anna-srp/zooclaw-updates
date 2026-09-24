---
title: "修复：任务里工具等待审批时，可以直接点「确认」或「取消」了"
type: "Bug Fix"
priority: "高"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# 修复：任务里工具等待审批时，可以直接点「确认」或「取消」了

## 核心宣传点

以前 Web Tasks 里遇到需要审批的工具调用，界面只显示一个转圈的工具计时器，用户根本不知道流程卡在等自己点头，任务就这么干等到超时。现在等待审批时会弹出可操作的确认/取消卡片，状态文案也从「运行中」改成「等待审批」。在任务里直接回复「确认」「取消」也算数——但只有当前恰好只有一个未过期、未提交的审批请求时才会被翻译成明确的审批指令，避免多个审批同时在场时点错。仅含元数据的审批请求也会被完整保留，不会在运行时丢失。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
Web Tasks now show an actionable confirmation/cancel card when a tool waits for approval, and display “Waiting for approval” instead of a running tool spinner/timer. A plain “确认”/“取消” reply in the Task is converted to an explicit approval command only when exactly one unexpired, unsubmitted approval is present.

Metadata-only approvals are retained through runtime filtering and rendering even when their text is empty. Cards follow durable request/resolution metadata, survive history replay, disable after submission/expiry/resolution, prevent duplicate clicks, and allow retry after a failed send. Approval lifecycle events are correlated by conversation and the Engine’s globally unique approval ID; tool-step projection also matches the run and tool-call ID. Ordinary replies arriving during approval display as queued. While approval is pending, the composer remains available so a typed confirmation can be sent. Deleted provisional status posts are excluded from thread views even if a late WebSocket edit arrives after their deletion, preventing stale running/unknown status after the tool has finished.

## Root cause
Task conversations are Mattermost threads with group semantics. ACS deliberately accepts plain confirmation words only in direct chats, so “确认” in a Task was queued as normal input. The tool UI also treated `awaiting_approval` as actively running.

Companion contract: https://github.com/SerendipityOneInc/agent-channel-service/pull/145. Deploy ACS before Web. Existing historical text-only approval posts keep their explicit slash-command path; buttons require the new structured metadata. Feishu confirmation behavior and backend group approval restrictions are unchanged.

## Test plan
- [x] Rebased onto `c2ff27963` (head `549f50efc`): preserved Build `/new` validation before Task approval-reply conversion. All 239 targeted tests across 8 files passed, including both sides of the conflict; TypeScript, ESLint and changed-surface governance checks passed. The 5/5 local E2E below was run on the explicitly recorded pre-rebase head, not claimed as a fresh E2E of this head.
- [x] Focused approval/card/real message component integration: 66 tests passed.
- [x] Runtime/message integration after the metadata-only review fix: 82 tests passed.
- [x] Existing typewriter hook tests: 23 passed.
- [x] Targeted tool-status/activity/shared tool-group tests passed; package ToolGroup suite: 70 passed.
- [x] Web TypeScript, ESLint and governance checks passed; repository commit/push gates run before submission.
- [x] Composer confirmation/cancellation regression and approval helpers: 63 tests passed.
- [x] Deleted-placeholder race regression (red → green), thread component and waiting reconciliation: 85 tests passed.
- [x] Fresh isolated browser E2E (Web `21f0a1bfd`, ACS `e34f54b`, Engine `78bd62c`): button confirm/cancel, typed 确认/取消, and reload-then-confirm all passed. Every pending approval had zero tool executions; each approval executed once and each denial executed zero times. All five runs completed, and the composer returned to send mode without stale running/unknown status.
- [x] Runtime audit: 64 outbox events published, 40 channel deliveries sent, 45 receiver outputs acknowledged; no pending/failed deliveries. Full-size browser screenshots inspected.
- Scope: actual local Engine/Temporal/Postgres/Redis/ACS/Mattermost and Chrome; account/workspace metadata and a harmless MCP counter were isolated fixtures. This does not claim deployed staging or Feishu acceptance.
- [ ] Deployed ACS → Engine → outbox → Web/channel E2E after coordinated rollout. No staging/production approval action or deployment was performed for this PR.



## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9296c3bf44220cf077e7f6278142209cd37f5443`
- PR: #3870
- 作者：sharplee-srp
- 日期：2026-09-23T08:37:14Z

### Commit Message

```
fix(chat): make task tool approvals actionable (#3870)

## Summary
Web Tasks now show an actionable confirmation/cancel card when a tool
waits for approval, and display “Waiting for approval” instead of a
running tool spinner/timer. A plain “确认”/“取消” reply in the Task is
converted to an explicit approval command only when exactly one
unexpired, unsubmitted approval is present.

Metadata-only approvals are retained through runtime filtering and
rendering even when their text is empty. Cards follow durable
request/resolution metadata, survive history replay, disable after
submission/expiry/resolution, prevent duplicate clicks, and allow retry
after a failed send. Approval lifecycle events are correlated by
conversation and the Engine’s globally unique approval ID; tool-step
projection also matches the run and tool-call ID. Ordinary replies
arriving during approval display as queued. While approval is pending,
the composer remains available so a typed confirmation can be sent.
Deleted provisional status posts are excluded from thread views even if
a late WebSocket edit arrives after their deletion, preventing stale
running/unknown status after the tool has finished.

## Root cause
Task conversations are Mattermost threads with group semantics. ACS
deliberately accepts plain confirmation words only in direct chats, so
“确认” in a Task was queued as normal input. The tool UI also treated
`awaiting_approval` as actively running.

Companion contract:
https://github.com/SerendipityOneInc/agent-channel-service/pull/145.
Deploy ACS before Web. Existing historical text-only approval posts keep
their explicit slash-command path; buttons require the new structured
metadata. Feishu confirmation behavior and backend group approval
restrictions are unchanged.

## Test plan
- [x] Rebased onto `c2ff27963` (head `549f50efc`): preserved Build
`/new` validation before Task approval-reply conversion. All 239
targeted tests across 8 files passed, including both sides of the
conflict; TypeScript, ESLint and changed-surface governance checks
passed. The 5/5 local E2E below was run on the explicitly recorded
pre-rebase head, not claimed as a fresh E2E of this head.
- [x] Focused approval/card/real message component integration: 66 tests
passed.
- [x] Runtime/message integration after the metadata-only review fix: 82
tests passed.
- [x] Existing typewriter hook tests: 23 passed.
- [x] Targeted tool-status/activity/shared tool-group tests passed;
package ToolGroup suite: 70 passed.
- [x] Web TypeScript, ESLint and governance checks passed; repository
commit/push gates run before submission.
- [x] Composer confirmation/cancellation regression and approval
helpers: 63 tests passed.
- [x] Deleted-placeholder race regression (red → green), thread
component and waiting reconciliation: 85 tests passed.
- [x] Fresh isolated browser E2E (Web `21f0a1bfd`, ACS `e34f54b`, Engine
`78bd62c`): button confirm/cancel, typed 确认/取消, and reload-then-confirm
all passed. Every pending approval had zero tool executions; each
approval executed once and each denial executed zero times. All five
runs completed, and the composer returned to send mode without stale
running/unknown status.
- [x] Runtime audit: 64 outbox events published, 40 channel deliveries
sent, 45 receiver outputs acknowledged; no pending/failed deliveries.
Full-size browser screenshots inspected.
- Scope: actual local Engine/Temporal/Postgres/Redis/ACS/Mattermost and
Chrome; account/workspace metadata and a harmless MCP counter were
isolated fixtures. This does not claim deployed staging or Feishu
acceptance.
- [ ] Deployed ACS → Engine → outbox → Web/channel E2E after coordinated
rollout. No staging/production approval action or deployment was
performed for this PR.
```

来源：SerendipityOneInc/ecap-workspace @ 9296c3bf，PR #3870，作者 sharplee-srp。