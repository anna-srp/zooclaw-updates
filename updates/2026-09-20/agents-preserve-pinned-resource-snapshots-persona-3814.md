---
title: "fix(agents): preserve pinned resource snapshots and runtime persona (#3814)"
type: "Bug Fix"
priority: "高"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 修复：Agent 固定的资源快照与运行时人格不会再被重置

## 核心宣传点

Agent 调用资源时必须用它 pinned 配置选定的那份绑定，包括保留的 Build 预览。这次把运行时投影与来源/绑定的对应关系以不可变形式存到业务库，Save/Undo、恢复、分享和来源 Revision 身份都保留，Engine 转发通用上下文、Proxy 读到的是真正生效的那条关联。资源初始化改为注册已有配置键，而不是拿过期的 declared.persona 新建并激活配置——这修掉了一个已复现的回归：编辑过的 AGENTS.md 被重置、onboarding 创建的 USER.md 被删除。已有 Agent 保留继承的选择，新建的 Builder Agent 从明确的空选择开始。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已上线

## PR 说明

## Problem and behavior

Agent resource calls must retain the binding selected by their pinned config, including retained Build previews. Store immutable runtime projection-to-source/binding associations in the business database; preserve Save/Undo, recovery, sharing and source Revision identity. Engine forwards generic context and Proxy reads the exact applied association.

Resource initialization now registers the existing configuration key instead of creating and activating a configuration from stale `declared.persona`. This fixes a reproduced regression that reset edited AGENTS.md and deleted an onboarding-created USER.md. Null-key Agents retain their business policy head for existing MCP synchronization, without any Engine configuration write.

## Scope and rollout

- Existing Agents retain inherited selections; new Builder Agents start with explicit empty selections. Main/Pack Settings remain unsupported.
- No new credentials, environment variables, flags, Proxy callbacks, frontend changes, or Engine business-policy fields.
- Add a dry-run-first staging registration command for reviewed exact historical keys. Per-Agent encrypted Mongo transactions reject stale scope, pending saves, conflicting maps and revoked heads; reruns are idempotent.
- Deploy the producer, revalidate/register retained history, then deploy strict Proxy/Engine readers from the companion feature branches. Preserve Engine pointers and existing persona/session state. The audited staging snapshot contains 36 eligible Agents and 89 keys; revalidate before applying.
- Companion PRs: [Engine #1523](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1523), updated on its original `feature/agent-resource-bindings` branch, and [Proxy #203](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/203) on `feature/agent-resource-snapshots`.

## Validation

- CI follow-up `fc90144359`: reuse the resource-projection store fixture in seven sharing/skill pipeline tests; no production changes or weakened assertions. Both affected modules pass locally (41 tests), full backend static/commit/push gates pass, and the updated PR CI passes with **11,447 tests passed / 5 skipped**.
- Final expanded backend regressions: **2,523 passed**, including initialization/retry persona preservation, null-key MCP sync, registration conflicts, Save/Undo, sharing and authoring.
- Full backend static gate and commit hooks passed. Broader pre-correction affected suite: 1,021 passed.
- Actual staging CSFLE canary passed dry-run/no-write, repeat registration, pending-save refusal, transactional rollback on a later-key conflict, and revoked-head refusal. Exact isolated fixture rows were cleaned and verified absent.
- Three-agent review completed; P1 persona overwrite and follow-up null-key MCP regression fixed and independently re-reviewed.
- Fleet registration and deployed provider/browser smoke are separate rollout steps, not claimed by unit tests.

## Staging cutover

Backend published from the feature branch as `service-v0.18.11-beta.11`. Registered 36 reviewed legacy Agents / 89 exact historical keys. Verified all associations with the actual Proxy reader, denied unknown contexts, and confirmed all 36 Engine pointers/keys remain unchanged. Retained session inventory: 118 sessions, no uncovered contexts. PR CI was not awaited, as explicitly requested for this staging test release.

## Pending-Save review correction

Commits `60b4d4ffe0` and `ecd79d0379` stop Undo, MCP synchronization, and idempotent Save retry before mutation when an intermediate-build configuration declares a resource binding without a registered projection. Save retry checks before credential seeding and checks the fresh post-seeding config again. The legacy field is a rejection signal only, never authorization. Normal source/baseline/null-key behavior remains unchanged. Rollout requires pausing resource Saves and completing/reconciling pending operations on the originating build before producer deployment; the runtime guard prevents silent rollback if this prerequisite is violated.

Validation: the initial correction passed **2,285 affected tests**. The additional Save-retry finding was reproduced by three failing cases before correction; **113 directly affected tests now pass**, including nine no-mutation cases across Undo/MCP synchronization/Save retry and normal resource Save. Backend static and commit/push gates passed. A read-only encrypted staging query at 2026-09-20 07:48:35 UTC found **0 pending Saves across all Engine workspaces**. This is current-state evidence, not retrospective proof of the earlier deployment window. These corrections are not yet redeployed to staging.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bce6e7056ea1e9fb24f3b0e765f88a5f1e47d8a6`
- PR: #3814
- 作者：kaka-srp
- 日期：2026-09-20T08:29:14Z

### Commit Message

```
fix(agents): preserve pinned resource snapshots and runtime persona (#3814)

## Problem and behavior

Agent resource calls must retain the binding selected by their pinned
config, including retained Build previews. Store immutable runtime
projection-to-source/binding associations in the business database;
preserve Save/Undo, recovery, sharing and source Revision identity.
Engine forwards generic context and Proxy reads the exact applied
association.

Resource initialization now registers the existing configuration key
instead of creating and activating a configuration from stale
`declared.persona`. This fixes a reproduced regression that reset edited
AGENTS.md and deleted an onboarding-created USER.md. Null-key Agents
retain their business policy head for existing MCP synchronization,
without any Engine configuration write.

## Scope and rollout

- Existing Agents retain inherited selections; new Builder Agents start
with explicit empty selections. Main/Pack Settings remain unsupported.
- No new credentials, environment variables, flags, Proxy callbacks,
frontend changes, or Engine business-policy fields.
- Add a dry-run-first staging registration command for reviewed exact
historical keys. Per-Agent encrypted Mongo transactions reject stale
scope, pending saves, conflicting maps and revoked heads; reruns are
idempotent.
- Deploy the producer, revalidate/register retained history, then deploy
strict Proxy/Engine readers from the companion feature branches.
Preserve Engine pointers and existing persona/session state. The audited
staging snapshot contains 36 eligible Agents and 89 keys; revalidate
before applying.
- Companion PRs: [Engine
#1523](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1523),
updated on its original `feature/agent-resource-bindings` branch, and
[Proxy
#203](https://github.com/SerendipityOneInc/ecap-proxy-service/pull/203)
on `feature/agent-resource-snapshots`.

## Validation

- CI follow-up `fc90144359`: reuse the resource-projection store fixture
in seven sharing/skill pipeline tests; no production changes or weakened
assertions. Both affected modules pass locally (41 tests), full backend
static/commit/push gates pass, and the updated PR CI passes with
**11,447 tests passed / 5 skipped**.
- Final expanded backend regressions: **2,523 passed**, including
initialization/retry persona preservation, null-key MCP sync,
registration conflicts, Save/Undo, sharing and authoring.
- Full backend static gate and commit hooks passed. Broader
pre-correction affected suite: 1,021 passed.
- Actual staging CSFLE canary passed dry-run/no-write, repeat
registration, pending-save refusal, transactional rollback on a
later-key conflict, and revoked-head refusal. Exact isolated fixture
rows were cleaned and verified absent.
- Three-agent review completed; P1 persona overwrite and follow-up
null-key MCP regression fixed and independently re-reviewed.
- Fleet registration and deployed provider/browser smoke are separate
rollout steps, not claimed by unit tests.

## Staging cutover

Backend published from the feature branch as `service-v0.18.11-beta.11`.
Registered 36 reviewed legacy Agents / 89 exact historical keys.
Verified all associations with the actual Proxy reader, denied unknown
contexts, and confirmed all 36 Engine pointers/keys remain unchanged.
Retained session inventory: 118 sessions, no uncovered contexts. PR CI
was not awaited, as explicitly requested for this staging test release.

## Pending-Save review correction

Commits `60b4d4ffe0` and `ecd79d0379` stop Undo, MCP synchronization,
and idempotent Save retry before mutation when an intermediate-build
configuration declares a resource binding without a registered
projection. Save retry checks before credential seeding and checks the
fresh post-seeding config again. The legacy field is a rejection signal
only, never authorization. Normal source/baseline/null-key behavior
remains unchanged. Rollout requires pausing resource Saves and
completing/reconciling pending operations on the originating build
before producer deployment; the runtime guard prevents silent rollback
if this prerequisite is violated.

Validation: the initial correction passed **2,285 affected tests**. The
additional Save-retry finding was reproduced by three failing cases
before correction; **113 directly affected tests now pass**, including
nine no-mutation cases across Undo/MCP synchronization/Save retry and
normal resource Save. Backend static and commit/push gates passed. A
read-only encrypted staging query at 2026-09-20 07:48:35 UTC found **0
pending Saves across all Engine workspaces**. This is current-state
evidence, not retrospective proof of the earlier deployment window.
These corrections are not yet redeployed to staging.
```

来源：SerendipityOneInc/ecap-workspace @ bce6e705，PR #3814，作者 kaka-srp。