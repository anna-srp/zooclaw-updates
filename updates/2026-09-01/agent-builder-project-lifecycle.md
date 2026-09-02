---
title: "Agent Builder 取消项目数量上限：项目随用随建，闲置自动回收、归档才彻底清理"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-01"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# Agent Builder 取消项目数量上限：项目随用随建，闲置自动回收、归档才彻底清理

## 核心宣传点

Agent Builder 以前是固定「槽位/容量」制，能同时开的项目数量有硬上限，占满了就得先腾位置。现在改成项目自己管生命周期：不再有项目配额，想建多少建多少。

闲置超过 24 小时的项目会自动回收对外通道（关闭 ACS Channels、把专属 Builder 机器人移出 Mattermost 团队），但项目本身和你的内容都还在——下次你真正在这个项目里操作时，路由、成员和频道会自动幂等地恢复，你基本感知不到。只有当你主动「归档」项目时，才会立刻深度清理专属工作区、Engine Agent 运行时/沙箱、频道和成员；外部步骤失败的话会保留项目身份，按小时重试直到清干净。

归档和 Builder 里的每一次发言（普通消息、`/stop`、Test 反馈、Preflight 反馈）通过一把可续期的短租约串行化，保证已被接受的消息处理期间不会被归档抽走资源；同时 `/stop` 始终作用于当前这一版运行时，即使期间已经有更新的 Builder 版本发布。清理逻辑只对 engine_v2、且是专属 Agent 结构的项目生效，历史共享 Agent 记录和不是这套生命周期写入的旧归档记录都排除在外。

配套还去掉了 Agent Builder 清理定时任务上一个遗留的 warm-pool 服务密钥依赖——这个接口本来就不用 warm-pool 资源，调度侧不必再配置 `X-Warm-Pool-Key`，访问边界仍由 `/admin/cron` 部署层管控。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `1e7750d26ccfd484d7246f637afb9d4a63dc8979`
- PR: #3602
- 作者: kaka-srp
- 日期: 2026-09-01T02:41:16Z

### Commit Message

```
refactor(agent-builder): simplify runtime resource lifecycle (#3602)

## Summary

- Replace the fixed Agent Builder Project slot/capacity state machine
with a Project-owned lifecycle: no Project quota, 24-hour idle ingress
cleanup, and Archive-only deep runtime cleanup.
- Idle cleanup disables ACS Channels and removes the dedicated Builder
bot from the Mattermost team; the next real Builder action restores
route, membership, and Channels idempotently.
- Archive immediately deep-cleans the dedicated Workspace, Engine Agent
runtime/Sandbox, ACS Channels, and Mattermost membership. Failed
external steps retain Project identity for hourly retry.
- Serialize Archive with every Builder post (ordinary message, `/stop`,
Test feedback, and Preflight feedback) through one short renewable
Project lease. Archive cannot retire resources during an accepted-post
window, while `/stop` remains available against the exact current
runtime even when a newer Builder release exists.
- Keep claim release best-effort so a Mongo release failure cannot turn
an already accepted post or persisted Archive into a client-visible
failure; the two-minute lease TTL remains the fallback.
- Restrict cleanup adoption to `engine_v2` Projects with the exact
`dedicated_project_agent` layout. Historical shared-Agent rows and old
archived rows that were not written by this lifecycle are excluded.
- Keep partially initialized runtimes cleanup-visible even when session
creation fails or the setup lease is lost, using a narrow identity CAS
that cannot overwrite a newer setup owner.
- Reuse the existing Engine cleanup contract (`status=cleaned`, matching
Agent identity, and `sandbox_released=true`); no Engine change or
rolling compatibility branch is required.
- Add an externally triggered hourly cleanup endpoint and remove the old
in-process slot reconciler.

This supersedes #3577. The diff exceeds the normal size budget because
it removes the old slot/capacity implementation and tests while adding
the smaller lifecycle. The changed-line total is dominated by 4,343
deletions; splitting deletion and replacement would leave an unsafe
intermediate release, so this PR carries `size-override`.

## Deployment

1. Deploy this ECAP PR.
2. Configure Cloud Scheduler to call `POST
/admin/cron/cleanup-agent-builder-runtime` hourly with
`X-Warm-Pool-Key`.

## Validation

- [x] `bash scripts/verify-changed.sh`: Ruff, format, Pyright, and all 8
import-linter contracts passed after merging current `main`.
- [x] 359 Agent Builder lifecycle, service, route, feedback, recovery,
Mattermost, and turn tests passed on the final change.
- [x] Independent review agent completed design,
concurrency/failure-window, scope, and regression passes. All reported
P2/P3 findings were fixed; final verdict is PASS with no remaining
actionable findings.
- [x] The setup/Archive race false positive was traced through both
service and repo CAS layers; an explicit regression test now proves the
losing setup write returns the latest archived snapshot.
- [x] Local real Archive test confirmed Project identity, Workspace,
Engine Agent/Sandbox, ACS Channel, and Mattermost membership cleanup.
- [x] Local real idle task processed all 31 eligible dedicated Projects
successfully; final idle and archived-retry candidate counts were both
zero, and sampled Agents/Workspaces remained intact while ACS/Mattermost
ingress was released.
- [x] Latest PR merge-ref CI passed 38/38 checks, including backend
tests, lint/typecheck, duplication, CodeQL, and both automated reviews.
- [ ] After deployment, configure and smoke-test the external hourly
scheduler.
```

### PR Body

```
## Summary

- Replace the fixed Agent Builder Project slot/capacity state machine with a Project-owned lifecycle: no Project quota, 24-hour idle ingress cleanup, and Archive-only deep runtime cleanup.
- Idle cleanup disables ACS Channels and removes the dedicated Builder bot from the Mattermost team; the next real Builder action restores route, membership, and Channels idempotently.
- Archive immediately deep-cleans the dedicated Workspace, Engine Agent runtime/Sandbox, ACS Channels, and Mattermost membership. Failed external steps retain Project identity for hourly retry.
- Serialize Archive with every Builder post (ordinary message, `/stop`, Test feedback, and Preflight feedback) through one short renewable Project lease. Archive cannot retire resources during an accepted-post window, while `/stop` remains available against the exact current runtime even when a newer Builder release exists.
- Keep claim release best-effort so a Mongo release failure cannot turn an already accepted post or persisted Archive into a client-visible failure; the two-minute lease TTL remains the fallback.
- Restrict cleanup adoption to `engine_v2` Projects with the exact `dedicated_project_agent` layout. Historical shared-Agent rows and old archived rows that were not written by this lifecycle are excluded.
- Keep partially initialized runtimes cleanup-visible even when session creation fails or the setup lease is lost, using a narrow identity CAS that cannot overwrite a newer setup owner.
- Reuse the existing Engine cleanup contract (`status=cleaned`, matching Agent identity, and `sandbox_released=true`); no Engine change or rolling compatibility branch is required.
- Add an externally triggered hourly cleanup endpoint and remove the old in-process slot reconciler.

This supersedes #3577. The diff exceeds the normal size budget because it removes the old slot/capacity implementation and tests while adding the smaller lifecycle. The changed-line total is dominated by 4,343 deletions; splitting deletion and replacement would leave an unsafe intermediate release, so this PR carries `size-override`.

## Deployment

1. Deploy this ECAP PR.
2. Configure Cloud Scheduler to call `POST /admin/cron/cleanup-agent-builder-runtime` hourly with `X-Warm-Pool-Key`.

## Validation

- [x] `bash scripts/verify-changed.sh`: Ruff, format, Pyright, and all 8 import-linter contracts passed after merging current `main`.
- [x] 359 Agent Builder lifecycle, service, route, feedback, recovery, Mattermost, and turn tests passed on the final change.
- [x] Independent review agent completed design, concurrency/failure-window, scope, and regression passes. All reported P2/P3 findings were fixed; final verdict is PASS with no remaining actionable findings.
- [x] The setup/Archive race false positive was traced through both service and repo CAS layers; an explicit regression test now proves the losing setup write returns the latest archived snapshot.
- [x] Local real Archive test confirmed Project identity, Workspace, Engine Agent/Sandbox, ACS Channel, and Mattermost membership cleanup.
- [x] Local real idle task processed all 31 eligible dedicated Projects successfully; final idle and archived-retry candidate counts were both zero, and sampled Agents/Workspaces remained intact while ACS/Mattermost ingress was released.
- [x] Latest PR merge-ref CI passed 38/38 checks, including backend tests, lint/typecheck, duplication, CodeQL, and both automated reviews.
- [ ] After deployment, configure and smoke-test the external hourly scheduler.

```

## 备注

本条为架构级重构，用户侧最直接的感知是「项目数量不再受限」和「闲置项目再次点开时会自动恢复」。归档为不可逆的深度清理操作。
