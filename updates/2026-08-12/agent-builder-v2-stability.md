---
title: "Agent Builder v2 稳定性修复：预览可刷新、测试回复完整、创建不再卡住"
type: "Bug Fix"
priority: "高"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# Agent Builder v2 稳定性修复：预览可刷新、测试回复完整、创建不再卡住

## 核心宣传点

修复了 Agent Builder v2 的三类卡点：预览刷新被误判为「有任务在跑」而拒绝、测试对话拿不到 Agent 的完整回复、以及新建项目卡在初始化后无法重试；同时从 Agent Studio 导入工作区时会保留项目模式与版本信息。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `c3f2ec74ea143b04f4662e77f92c75cd3a21c23c`
- PR: #3338

### Commit Message

```
fix(agent-builder): preserve project context and preview refresh (#3338)

## Summary

- preserve Project mode, source identity/version, and fork target
identity when ECAP imports a dedicated Agent Studio workspace
- let Refresh Preview renew the Project's existing package-test capacity
lease instead of rejecting it as a competing runtime operation
- fence terminal cleanup by both package operation and iteration so a
stale finalizer cannot clear or cool down a newly refreshed preview
- roll back a reclaimed lease generation when the Project start CAS
fails

## Root causes

1. The dedicated Project runtime serialized only `project_id`,
`source_type`, and `source_ref`, so Agent Studio could not apply fork
target identity or preserve the source version used by the pre-publish
guard.
2. A previewing TestRun intentionally retained the Project's
package-test slot, but Refresh Preview attempted to acquire a new
operation and was rejected by the same Project's active lease.
3. Reusing that lifecycle lease without an iteration fence allowed a
stale terminal snapshot to finish the slot and clear
`workspace_operation_id` after a newer refresh had started.

## Design

- Keep the existing per-user three-Project capacity model and existing
Project/slot persistence.
- Treat refresh as another iteration in the same active package-test
lifecycle; do not add a lock or a new state machine.
- Use the Project's `current_iteration_id` CAS to serialize lifecycle
cleanup with refresh, and the slot `fence` to distinguish an unchanged
lease from a reclaimed generation.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] focused runtime/repository/sandbox unit suite — 37 passed
- [x] pre-commit Python hooks
- [x] pre-push changed-surface verification

## Dependency

- Companion Agent Studio runtime fix:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/236
```

### PR Body

## Summary

- preserve Project mode, source identity/version, and fork target identity when ECAP imports a dedicated Agent Studio workspace
- let Refresh Preview renew the Project's existing package-test capacity lease instead of rejecting it as a competing runtime operation
- fence terminal cleanup by both package operation and iteration so a stale finalizer cannot clear or cool down a newly refreshed preview
- roll back a reclaimed lease generation when the Project start CAS fails

## Root causes

1. The dedicated Project runtime serialized only `project_id`, `source_type`, and `source_ref`, so Agent Studio could not apply fork target identity or preserve the source version used by the pre-publish guard.
2. A previewing TestRun intentionally retained the Project's package-test slot, but Refresh Preview attempted to acquire a new operation and was rejected by the same Project's active lease.
3. Reusing that lifecycle lease without an iteration fence allowed a stale terminal snapshot to finish the slot and clear `workspace_operation_id` after a newer refresh had started.

## Design

- Keep the existing per-user three-Project capacity model and existing Project/slot persistence.
- Treat refresh as another iteration in the same active package-test lifecycle; do not add a lock or a new state machine.
- Use the Project's `current_iteration_id` CAS to serialize lifecycle cleanup with refresh, and the slot `fence` to distinguish an unchanged lease from a reclaimed generation.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] focused runtime/repository/sandbox unit suite — 37 passed
- [x] pre-commit Python hooks
- [x] pre-push changed-surface verification

## Dependency

- Companion Agent Studio runtime fix: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/236


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `cc1b99d17fced476edd0946bc8dcde8d0f61e507`
- PR: #3349

### Commit Message

```
fix(agent-builder): stabilize v2 preview runtime (#3349)

## Summary

Follow-up to merged PR #3338 for the v2 Agent Builder preview/runtime
path.

- replace the process-owned v2 Preview background loop with request/poll
reconciliation backed by persisted TestRun state
- keep Builder chat independent from Preview packaging/deployment and
remove stale runtime-operation blocking
- make session-channel creation and runtime allocation idempotent across
retries and duplicate-key races
- reconcile stale Preview creation after worker/deploy interruption
without a fixed 30-minute ownership TTL
- return the Test Agent's user-visible `message.send` response to
Builder instead of the hidden `NO_REPLY` terminal sentinel
- authorize Share Chat for the creator's canonical v2 Builder session
backed by its hidden Engine workspace, without broadening generic
hidden-channel ownership
- include the v2 Preview reconciliation design document and regression
coverage

## Verification

- backend Agent Builder / packaging targeted suite: 225 passed
- backend Share Chat suite: 37 passed
- frontend Agent Builder targeted suite: 45 passed
- Ruff, ESLint, Prettier, and `git diff --check` passed
- replayed the reported Test run: extracted the complete 4,786-character
visible response with no `NO_REPLY`
- resolved the reported Builder session/channel through the new
ownership path against staging-backed local data

## Manual checks

- local frontend and backend both healthy
- latest `origin/main` merged, including PR #3347 `manifest_metadata`
packaging compatibility
```

### PR Body

## Summary

Follow-up to merged PR #3338 for the v2 Agent Builder preview/runtime path.

- replace the process-owned v2 Preview background loop with request/poll reconciliation backed by persisted TestRun state
- keep Builder chat independent from Preview packaging/deployment and remove stale runtime-operation blocking
- make session-channel creation and runtime allocation idempotent across retries and duplicate-key races
- reconcile stale Preview creation after worker/deploy interruption without a fixed 30-minute ownership TTL
- return the Test Agent's user-visible `message.send` response to Builder instead of the hidden `NO_REPLY` terminal sentinel
- authorize Share Chat for the creator's canonical v2 Builder session backed by its hidden Engine workspace, without broadening generic hidden-channel ownership
- include the v2 Preview reconciliation design document and regression coverage

## Verification

- backend Agent Builder / packaging targeted suite: 225 passed
- backend Share Chat suite: 37 passed
- frontend Agent Builder targeted suite: 45 passed
- Ruff, ESLint, Prettier, and `git diff --check` passed
- replayed the reported Test run: extracted the complete 4,786-character visible response with no `NO_REPLY`
- resolved the reported Builder session/channel through the new ownership path against staging-backed local data

## Manual checks

- local frontend and backend both healthy
- latest `origin/main` merged, including PR #3347 `manifest_metadata` packaging compatibility


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `36917eb316e4f1d07bc6eee9829d948e653b3c70`
- PR: #3342

### Commit Message

```
fix(agent-builder): recover stale v2 project creation (#3342)

## Summary

- allow a new dedicated-layout v2 Project to replace stale pending
creation when the user changes input or the original Project is terminal
- reconcile ambiguous successful initialization by opening the
already-progressed Project instead of creating a duplicate
- serialize automatic recovery and explicit submission, and keep
recovery UI aligned with the authoritative pending Project
- preserve existing v1 and legacy-layout behavior

## Validation

- code-review agent review and post-fix re-review: no remaining findings
- 48 Agent Builder entry unit tests passed
- TypeScript passed
- ESLint passed
- all web governance guards passed via scripts/verify-web.sh
```

### PR Body

## Summary

- allow a new dedicated-layout v2 Project to replace stale pending creation when the user changes input or the original Project is terminal
- reconcile ambiguous successful initialization by opening the already-progressed Project instead of creating a duplicate
- serialize automatic recovery and explicit submission, and keep recovery UI aligned with the authoritative pending Project
- preserve existing v1 and legacy-layout behavior

## Validation

- code-review agent review and post-fix re-review: no remaining findings
- 48 Agent Builder entry unit tests passed
- TypeScript passed
- ESLint passed
- all web governance guards passed via scripts/verify-web.sh

---
