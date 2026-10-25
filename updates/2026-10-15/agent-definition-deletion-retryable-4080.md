---
title: "修复：Agent 删除中途失败后可以安全重试，不会卡在「卸载中」动不了"
type: "Bug Fix"
priority: "高"
date: "2026-10-15"
status: "待审核"
channels: ""
---

# 修复：Agent 删除中途失败后可以安全重试，不会卡在「卸载中」动不了

## 核心宣传点

原生 Agent 定义删除被中断后，现在可以针对同一个 Agent/Computer 身份重新发起删除，不再因为残留的 uninstalling 状态而被拒绝。删除意图与可续期租约会被持久化，成功/失败写入都绑定当前操作令牌，迟到的回调无法覆盖更新的尝试或终态。删除一旦开始，新的 Build、设置、启动与运行时恢复写入都会被拒绝，但只读的源码与历史访问仍然保留。组织关停时也能停掉删除失败的 Agent，且不会覆盖其删除状态、租约与集成清理，这些 Agent 保持不可恢复并维持共享 Computer 的隔离分支。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `030cc4a4164a2305dadf3b425fe5d3be8851b179`
- PR: #4080
- 作者：kaka-srp
- 日期：2026-10-15T07:35:20Z

### Commit Message

```
fix(agents): make definition deletion safely retryable (#4080)

## Summary
- Make interrupted native Agent-definition deletions retryable against
the same Agent/Computer identity. Persist deletion intent and a
renewable lease, and fence success/failure writes with the current
operation/token so late callbacks cannot overwrite a newer attempt or a
terminal state.
- Reject new Build, settings, start and runtime-recovery writes once
deletion begins. Preserve existing read-only source/history access and
the existing integration cleanup mechanism.
- Allow organization shutdown to stop Agents whose deletion failed,
without overwriting their deletion state, lease or integration cleanup.
Keep those Agents non-restorable and preserve the shared-Computer
isolation branch.

## Root cause
Deletion entry points and claims rejected retained `uninstalling` rows,
while finalization and failure writes were not bound to an execution
attempt. Authoring entry points also applied inconsistent lifecycle
checks. Shutdown and recovery share persistence helpers, so deletion
guards must block reactivation while still allowing shutdown to finish
safely.

## Test plan
- [x] 747 focused regression tests passed across Agent development,
authoring, deletion, lifecycle, integration cleanup and runtime
shutdown/recovery.
- [x] 23 additional enterprise-invite handoff tests passed.
- [x] 151 affected ChangeSet read/write, authoring, apply,
route-boundary and repository contract tests passed after review
corrections.
- [x] Real local MongoDB tests: concurrent claims/takeovers, stale
callbacks, failure retries, organization shutdown with a failed
deletion, repeated shutdown, and deletion starting/completing during
shutdown.
- [x] Backend static verification: Ruff, formatting, Pyright and
import-linter; complexity and source duplication checks passed.
- [x] Local code review and regression coverage for deletion/shutdown
interaction.
- [x] Staging encrypted-client compatibility: 5 deletion statements and
8 shutdown/recovery statements executed with randomly generated
nonexistent identities. Encryption remained enabled; no documents
matched or were modified. This validates query compatibility, not full
business E2E.
- [ ] Full business-resource cross-service kill/restart E2E was not
performed.

Real Mongo tests require an explicit local
`TEST_AGENT_DELETION_MONGO_URI`; they skip when it is unset.

## Rollout
Backend only. `AGENT_DELETION_RECOVERY_ENABLED` defaults to `false`;
enable after all relevant writers are upgraded and old requests have
drained. Disabling the flag prevents new operations but existing
deletion records continue through the leased path. Do not roll back to
writers that ignore retained deletion intent while operations remain
pending.

Recovery is triggered by retrying the existing delete endpoint; no new
background scanner or client response contract is introduced. Creation
recovery and strict fencing of already-in-flight remote writes remain
outside this change.


## Related issues
- Related to #3963: adds deletion-time write admission for new authoring
operations. Strict fencing of already-in-flight remote
skill/Environment/config side effects remains outside this PR; this
issue stays open.
- Related to #3960: this PR covers interrupted definition deletion only.
Recovery of interrupted creation stuck in `installing` remains outside
this PR; this issue stays open.
```

