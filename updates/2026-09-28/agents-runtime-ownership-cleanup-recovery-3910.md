---
title: "修复：加入企业团队时运行环境归属判断错误，导致个人续费已取消但资源清理失败"
type: "Bug Fix"
priority: "高"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 修复：加入企业团队时运行环境归属判断错误，导致个人续费已取消但资源清理失败

## 核心宣传点

新建的自演进工作区如果没有开发基线，运行环境的归属方是由工作区推导出来的，但清理和恢复流程却把业务账号/组织的 ID 报给了底层运行服务，于是在清理快照保存之前就拿到「渠道不存在」的错误。最糟的时机是加入企业团队的过程中——此时个人续费已经取消掉了，清理却失败，用户会卡在一个两头不靠的状态。这次让渠道增删改、清理快照、渠道停用与回读、订阅恢复统一走同一套归属解析，业务授权、基线归属、已迁移的渠道 ID 和共享算力的生命周期行为都保持原样。取消个人续费之前，会在成员身份迁移租约内先检查来源侧的引擎状态、定时任务和渠道；执行阶段仍然各自保存持久化快照并沿用原有的租约、CAS 与停止回读校验。交接失败时会额外记录个人续费取消是否已经完成，便于定位。

## 分级

- 内部：P0
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary
- Use the same Workspace-to-ACS ownership resolver for channel CRUD, cleanup snapshots, channel disable/readback, and subscription recovery. Preserve business authorization, baseline ownership, migrated channel IDs, and shared-Computer lifecycle behavior.
- Check source Engine state, schedules, and channels under the membership transition lease before canceling personal renewal. Execution still captures its own durable snapshot and enforces existing leases, CAS and stop/readback checks.
- Log safe lifecycle stages and upstream error metadata before wrapping failures, and record whether personal renewal cancellation had completed when a handoff fails.

Related: #3909 · [ECA-1473](https://linear.app/srpone/issue/ECA-1473)
Design and implementation plan: [2026-09-28-eca-1473-runtime-cleanup.md](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/docs/superpowers/specs/2026-09-28-eca-1473-runtime-cleanup.md)

## Root cause
New self-evolving workspaces without a development baseline use workspace-derived runtime owners. Cleanup and recovery sent the business UID/org to ACS instead, causing `channel.not_found` before the cleanup snapshot was saved. During enterprise join this happened after personal renewal had already been canceled.

## Test plan
- [x] 261 targeted tests: cleanup/recovery, enterprise handoff, baseline adoption, channel services/service proxy, recovery repository and personal subscription cancellation.
- [x] Stateful HTTP transport tests verify actual ACS actor headers and internal channel IDs for ordinary Engine, self-evolving without baseline, self-evolving with baseline, and migrated workspaces; cover 404, readback failure, lease loss and retry.
- [x] Preflight tests prove no runtime writes and no renewal cancellation/key bind/membership swap after a failed preflight. Post-preflight failure remains retryable with an already-canceling subscription.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8 import contracts passed.
- [x] CI: 12,776 tests passed, 5 skipped; coverage 89.79% (gate 89.5%). Lint/types, duplication, CodeQL and both automated reviews passed.
- [ ] Isolated staging E2E with real Engine/ACS, encrypted Mongo, billing-key readback and target membership activation. Local HTTP transports and repository mocks do not validate this boundary; no Mongo query forms were changed.

This is a backend code fix. Production recovery/deployment and a new user-facing durable handoff-progress API/UI remain tracked by #3909. Existing subscription audits, runtime cleanup snapshots and retry semantics are retained; renewal cancellation is not automatically reversed.

## Review follow-up
- Confirmed the adjacent Agent Builder channel helper is outside this defect: Project Agents are installed as hidden `agent_builder` workspaces with [business-owned Engine resources](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/services/claw-interface/app/services/agents/engine_agent_install_service.py#L355). Both the [baseline service guard](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/services/claw-interface/app/services/agents/agent_baseline_adoption.py#L36) and repository reject hidden/internal workspaces. No supported path converts that dedicated Project Agent to a new opaque-owned self-evolving workspace; the sibling helper is unchanged.
- Keeping renewal canceled after a later cleanup failure is intentional and follows #3909: retry is supported, while automatic renewal restoration would override the user's join intent.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9812c1a6bdb51828a424a02d1aeef0d80cb2ddda`
- PR: #3910
- 作者：rayrain-srp
- 日期：2026-09-28T12:52:00Z

### Commit Message

```
fix(agents): resolve runtime ownership during cleanup and recovery (#3910)

## Summary
- Use the same Workspace-to-ACS ownership resolver for channel CRUD,
cleanup snapshots, channel disable/readback, and subscription recovery.
Preserve business authorization, baseline ownership, migrated channel
IDs, and shared-Computer lifecycle behavior.
- Check source Engine state, schedules, and channels under the
membership transition lease before canceling personal renewal. Execution
still captures its own durable snapshot and enforces existing leases,
CAS and stop/readback checks.
- Log safe lifecycle stages and upstream error metadata before wrapping
failures, and record whether personal renewal cancellation had completed
when a handoff fails.

Related: #3909 · [ECA-1473](https://linear.app/srpone/issue/ECA-1473)
Design and implementation plan:
[2026-09-28-eca-1473-runtime-cleanup.md](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/docs/superpowers/specs/2026-09-28-eca-1473-runtime-cleanup.md)

## Root cause
New self-evolving workspaces without a development baseline use
workspace-derived runtime owners. Cleanup and recovery sent the business
UID/org to ACS instead, causing `channel.not_found` before the cleanup
snapshot was saved. During enterprise join this happened after personal
renewal had already been canceled.

## Test plan
- [x] 261 targeted tests: cleanup/recovery, enterprise handoff, baseline
adoption, channel services/service proxy, recovery repository and
personal subscription cancellation.
- [x] Stateful HTTP transport tests verify actual ACS actor headers and
internal channel IDs for ordinary Engine, self-evolving without
baseline, self-evolving with baseline, and migrated workspaces; cover
404, readback failure, lease loss and retry.
- [x] Preflight tests prove no runtime writes and no renewal
cancellation/key bind/membership swap after a failed preflight.
Post-preflight failure remains retryable with an already-canceling
subscription.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8
import contracts passed.
- [x] CI: 12,776 tests passed, 5 skipped; coverage 89.79% (gate 89.5%).
Lint/types, duplication, CodeQL and both automated reviews passed.
- [ ] Isolated staging E2E with real Engine/ACS, encrypted Mongo,
billing-key readback and target membership activation. Local HTTP
transports and repository mocks do not validate this boundary; no Mongo
query forms were changed.

This is a backend code fix. Production recovery/deployment and a new
user-facing durable handoff-progress API/UI remain tracked by #3909.
Existing subscription audits, runtime cleanup snapshots and retry
semantics are retained; renewal cancellation is not automatically
reversed.

## Review follow-up
- Confirmed the adjacent Agent Builder channel helper is outside this
defect: Project Agents are installed as hidden `agent_builder`
workspaces with [business-owned Engine
resources](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/services/claw-interface/app/services/agents/engine_agent_install_service.py#L355).
Both the [baseline service
guard](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/services/claw-interface/app/services/agents/agent_baseline_adoption.py#L36)
and repository reject hidden/internal workspaces. No supported path
converts that dedicated Project Agent to a new opaque-owned
self-evolving workspace; the sibling helper is unchanged.
- Keeping renewal canceled after a later cleanup failure is intentional
and follows #3909: retry is supported, while automatic renewal
restoration would override the user's join intent.
```

来源：SerendipityOneInc/ecap-workspace @ 9812c1a6，PR #3910，作者 rayrain-srp。
