---
title: "修复：保存 API 模型时不再顺带改动 Agent 的算力规格，环境未就绪也不会让整次保存失败"
type: "Bug Fix"
priority: "高"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 修复：保存 API 模型时不再顺带改动 Agent 的算力规格，环境未就绪也不会让整次保存失败

## 核心宣传点

断开个人订阅后再保存一个 API 模型，原先会连带去改 Agent 的沙箱算力规格；一旦目标规格的环境变体缺失，整次模型保存就会被 environment_not_ready 直接拒掉。现在模型保存、启动与准备、默认 Agent 的读取与重试、Service API 配置写入、Pack 内容与环境更新都会保留原有算力不动。选择 API 模型会清掉订阅绑定。新建 Agent 仍按服务端可信权益选初始规格，真实运行时与环境校验照旧保留。从旧版迁移过来的 Agent 保留既有算力配置，并且按统一的迁移标识排除在权益变更同步和每小时规格对账任务之外；被跳过的记录不会阻断分页也不计为失败。该策略对升级和降级都适用，同一账号下的原生 Agent 仍然正常同步。本次没有新增任何自动的环境构建或重试。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已随正式 release 上线

## PR 说明

## Problem and behavior

Saving an API model after disconnecting a personal subscription also
tried to change the Agent's Sandbox class. A missing target-class
Environment variant could reject the entire model save with
`environment_not_ready`.

Model saves, start/prepare, existing default-Agent reads/retries,
Service API config writes, and Pack content/environment updates now
preserve compute. API model selection clears the subscription binding.
Agent creation still selects its initial class from trusted server
entitlements; actual runtime/Environment validation remains in place.

V1-migrated Agents retain their existing compute configuration. Both
migrated main and secondary workspaces are excluded from
entitlement-change synchronization and the hourly class-reconciliation
cron using the canonical `is_migrated_v1` identity. Skipped rows do not
block pagination or count as failures; cron `processed_count` continues
to count scanned rows. This policy covers upgrades and downgrades.
Native Agents in the same account still synchronize normally.

Native reconciliation reads the current class and skips matching values.
Older Engines that omit the projection retain the existing PUT fallback;
differing classes are updated normally and target-Environment failures
remain visible. No automatic Environment build or retry is added.

Service API Agents intentionally have no ECAP workspace row. Entitlement
synchronization now also pages Engine's tenant-scoped Agent inventory;
the hourly sweep independently enumerates active memberships using an
indexed `(uid, org_id)` cursor, so owners with no workspace and Agents
whose creation token was revoked are covered. The additional pass
excludes any Computer represented by a workspace record, including
retired or migrated siblings, preserving the existing lifecycle policy.
It validates inventory ownership and pagination, isolates individual
Agent failures, and shares the cron's batch budget. No synthetic
workspaces or foreground class updates are introduced.

The resource-class cron now has a separate 100-request Engine inventory
budget, charging empty, workspace-only, and failed pages before I/O. A
durable singleton checkpoint carries both the workspace and membership
cursors, current Engine page, and unfinished page IDs across
invocations. A 900-second atomic lease covers both phases; a shorter
600-second timeout bounds a live run, overlapping triggers skip work,
and owner/expiry checks fence stale checkpoint writers. Positive Agent
budgets also resume from their saved position. Each bounded inventory
slice yields back to workspace repair on the next invocation, retaining
independent inventory progress. A full sweep can span multiple hourly
invocations; foreground entitlement hooks still provide the fast path.

## Scope and compatibility

SerendipityOneInc/zooclaw-engine#1772's shared-Computer atomic upgrade
proposal is withdrawn. This PR does not require it or impose a new hard
deployment prerequisite on SerendipityOneInc/zooclaw-engine#1771. The
earlier automatic-build proposal SerendipityOneInc/zooclaw-engine#1767
remains withdrawn.

This change does not repair historical Computer/config drift or mutate
deployed data. Migrated Agents may retain a lower or higher class than
their current plan intentionally. It does not pin existing Sandbox
instances forever or introduce an upgrade-on-recreation mechanism.
Native synchronization remains best effort plus the hourly cron and
requires a ready target Environment; native downgrades may therefore
retain higher resources until synchronization succeeds.

Product ops owns Environment builds/retries. Issue #3933 retains
health/impact visibility, with intentional migrated-class retention
distinguished from actual runtime failures.

## Validation

- Latest bounded-scan fix: 62 targeted tests passed, covering
empty/workspace-only/failed inventory budgets, default-unlimited Agent
budgets, tail and large-owner page continuation, mid-page Agent limits,
failure isolation, native-workspace continuation, overlapping runs,
timeout checkpoints, expired-lease recovery, stale-owner fencing,
repository atomic-operation contracts, existing cron routes and CSFLE
syntax guards.
- `scripts/verify-changed.sh` passed: Ruff, formatting, Pyright, and all
8 import contracts.
- Final CI on `1464cc836`: **13,098 passed, 5 skipped**, coverage
**89.86%**. All quality, CodeQL and auto-review gates passed:
https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/36663154292.
Latest Codex and Claude reviews approve with no blocking findings.
- Prior review findings fixed: Service API inventory coverage and
membership cursor/index. Re-enabled native main Agents continue to use
the accepted background-convergence policy. The new scan-cost finding is
addressed by independent request/time budgets, durable continuation and
a singleton lease.
- No merge, deployment, or live user-data mutation. The new
`ecap-engine-class-scan` singleton uses Mongo's built-in unique `_id`;
atomic updates are classic single-collection operations, without
aggregation or pipeline updates. Live encrypted-client validation of
claim/checkpoint/release remains required before release; unit mocks and
syntax guards do not prove CSFLE compatibility.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `543ad5c901e927353a3889d3b91f4bcbe00be9f4`
- PR: #3928
- 作者：Chris@ZooClaw
- 日期：2026-09-30T04:26:53Z

### Commit Message

```
fix(claw): isolate model changes and agent lifecycle from compute upgrades (#3928)

## Problem and behavior

Saving an API model after disconnecting a personal subscription also
tried to change the Agent's Sandbox class. A missing target-class
Environment variant could reject the entire model save with
`environment_not_ready`.

Model saves, start/prepare, existing default-Agent reads/retries,
Service API config writes, and Pack content/environment updates now
preserve compute. API model selection clears the subscription binding.
Agent creation still selects its initial class from trusted server
entitlements; actual runtime/Environment validation remains in place.

V1-migrated Agents retain their existing compute configuration. Both
migrated main and secondary workspaces are excluded from
entitlement-change synchronization and the hourly class-reconciliation
cron using the canonical `is_migrated_v1` identity. Skipped rows do not
block pagination or count as failures; cron `processed_count` continues
to count scanned rows. This policy covers upgrades and downgrades.
Native Agents in the same account still synchronize normally.

Native reconciliation reads the current class and skips matching values.
Older Engines that omit the projection retain the existing PUT fallback;
differing classes are updated normally and target-Environment failures
remain visible. No automatic Environment build or retry is added.

Service API Agents intentionally have no ECAP workspace row. Entitlement
synchronization now also pages Engine's tenant-scoped Agent inventory;
the hourly sweep independently enumerates active memberships using an
indexed `(uid, org_id)` cursor, so owners with no workspace and Agents
whose creation token was revoked are covered. The additional pass
excludes any Computer represented by a workspace record, including
retired or migrated siblings, preserving the existing lifecycle policy.
It validates inventory ownership and pagination, isolates individual
Agent failures, and shares the cron's batch budget. No synthetic
workspaces or foreground class updates are introduced.

The resource-class cron now has a separate 100-request Engine inventory
budget, charging empty, workspace-only, and failed pages before I/O. A
durable singleton checkpoint carries both the workspace and membership
cursors, current Engine page, and unfinished page IDs across
invocations. A 900-second atomic lease covers both phases; a shorter
600-second timeout bounds a live run, overlapping triggers skip work,
and owner/expiry checks fence stale checkpoint writers. Positive Agent
budgets also resume from their saved position. Each bounded inventory
slice yields back to workspace repair on the next invocation, retaining
independent inventory progress. A full sweep can span multiple hourly
invocations; foreground entitlement hooks still provide the fast path.

## Scope and compatibility

SerendipityOneInc/zooclaw-engine#1772's shared-Computer atomic upgrade
proposal is withdrawn. This PR does not require it or impose a new hard
deployment prerequisite on SerendipityOneInc/zooclaw-engine#1771. The
earlier automatic-build proposal SerendipityOneInc/zooclaw-engine#1767
remains withdrawn.

This change does not repair historical Computer/config drift or mutate
deployed data. Migrated Agents may retain a lower or higher class than
their current plan intentionally. It does not pin existing Sandbox
instances forever or introduce an upgrade-on-recreation mechanism.
Native synchronization remains best effort plus the hourly cron and
requires a ready target Environment; native downgrades may therefore
retain higher resources until synchronization succeeds.

Product ops owns Environment builds/retries. Issue #3933 retains
health/impact visibility, with intentional migrated-class retention
distinguished from actual runtime failures.

## Validation

- Latest bounded-scan fix: 62 targeted tests passed, covering
empty/workspace-only/failed inventory budgets, default-unlimited Agent
budgets, tail and large-owner page continuation, mid-page Agent limits,
failure isolation, native-workspace continuation, overlapping runs,
timeout checkpoints, expired-lease recovery, stale-owner fencing,
repository atomic-operation contracts, existing cron routes and CSFLE
syntax guards.
- `scripts/verify-changed.sh` passed: Ruff, formatting, Pyright, and all
8 import contracts.
- Final CI on `1464cc836`: **13,098 passed, 5 skipped**, coverage
**89.86%**. All quality, CodeQL and auto-review gates passed:
https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/36663154292.
Latest Codex and Claude reviews approve with no blocking findings.
- Prior review findings fixed: Service API inventory coverage and
membership cursor/index. Re-enabled native main Agents continue to use
the accepted background-convergence policy. The new scan-cost finding is
addressed by independent request/time budgets, durable continuation and
a singleton lease.
- No merge, deployment, or live user-data mutation. The new
`ecap-engine-class-scan` singleton uses Mongo's built-in unique `_id`;
atomic updates are classic single-collection operations, without
aggregation or pipeline updates. Live encrypted-client validation of
claim/checkpoint/release remains required before release; unit mocks and
syntax guards do not prove CSFLE compatibility.
```

来源：SerendipityOneInc/ecap-workspace @ 543ad5c9，PR #3928，作者 Chris@ZooClaw。
