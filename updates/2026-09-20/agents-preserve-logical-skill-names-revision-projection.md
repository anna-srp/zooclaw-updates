---
title: "fix(agents): preserve logical skill names across revision projections (#3816)"
type: "Bug Fix"
priority: "中"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 修复：Agent 修订投影时保留技能的原始名称

## 核心宣传点

创建、预览、提交、应用和共享更新的整个链路里，Engine 绑定都会保留技能的来源名称，不会重命名注册表 ID、版本或已存储的内容。之前修订绑定虽然留着来源名，但配置投影会把它丢掉，Engine 于是暴露了内部防冲突名，用户在 Agent 里看到的技能名和自己写的不一致。新投影/幂等键做了隔离，升级前的 R0 创建仍能按原键重放；新引入的名称（包括重命名目标）会做校验，历史遗留名称和已接受的草稿操作仍可读可编辑并给出警告。

## 分级

- 内部：P2
- 外部：C
- 发布状态：已合并待发版

## PR 说明

## Summary

- Preserve source skill names in Engine bindings throughout create, preview, commit, apply and shared updates, without renaming registry IDs, versions or stored content.
- Isolate new projection/idempotency keys; retain exact same-key replay for pre-upgrade R0 creates.
- Validate newly introduced names, including rename targets. Existing legacy names and already accepted draft operations remain readable/editable with warnings; renaming to a compliant name is supported, while introducing a different noncompliant name is rejected.
- Include the design, business regression tests and real-runtime validation evidence. The fixture-specific local trial script and its dedicated recovery tests are deliberately not part of this PR.

## Root cause

Revision bindings retained the source name, but configuration projection dropped it. Engine therefore exposed the collision-safe internal registry name to the model. The companion Engine change adds an optional Agent-local name while keeping storage identity and authorization unchanged.

Companion: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1561.

## Test plan

- [x] Independent review finding fixed: old accepted drafts must not be rejected when replayed; 14 regression cases cover compatibility.
- [x] Before main refresh: related backend suite 634 passed; backend static/complexity/file-length checks passed.
- [x] After rebase onto main including resource snapshot changes: 89 targeted tests passed, including authoring, turn snapshots and runtime projections.
- [x] Companion Engine verifies exact legacy replay using real service code and PGlite persistence (11 binding tests passed).
- [x] CI follow-up: refreshed the inherited-baseline commit regression to assert exact logical names along with unchanged skill IDs/versions. The inherited-materialization business suite remains in this PR.
- [x] Real local single-lane test on the existing test Agent and its existing active/Build sessions: both model turns succeeded, actual provider system captures use logical names, and each turn successfully read five global skills, one source-owned skill and its relative script.
- [x] Real authoring HTTP gateway plus encrypted Mongo: legacy draft read/validate/edit/rename and new-invalid-name rejection; draft operations restored.
- [x] Implicit global set and explicit empty set checked; active config and sandbox view restored. No Agent/skill/session created. Test history retained.

The full real-runtime trial preceded the main refresh; the refresh was validated with targeted regression tests and static gates, not claimed as another live trial. Build file reads and the authoring gateway were exercised separately: no claim that the model itself successfully called source_read. ACS/external Feishu delivery was out of scope.

## Rollout / scope

Deploy the companion Engine compatibility change before claw-interface. No frontend release, registry rewrite or production data migration is included. Existing persisted configs require a later normal revision projection or a separately authorized migration; this PR does not silently rewrite them.

Local environment repair was separately authorized: four missing staging R2 blobs were added only after hash verification with absent-only writes; existing objects and registry records were unchanged. No credentials are included.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `c6333408814661db3bc3d7e0f56d8ea3e9140167`
- PR: #3816
- 作者：kaka-srp
- 日期：2026-09-20T09:22:22Z

### Commit Message

```
fix(agents): preserve logical skill names across revision projections (#3816)

## Summary

- Preserve source skill names in Engine bindings throughout create,
preview, commit, apply and shared updates, without renaming registry
IDs, versions or stored content.
- Isolate new projection/idempotency keys; retain exact same-key replay
for pre-upgrade R0 creates.
- Validate newly introduced names, including rename targets. Existing
legacy names and already accepted draft operations remain
readable/editable with warnings; renaming to a compliant name is
supported, while introducing a different noncompliant name is rejected.
- Include the design, business regression tests and real-runtime
validation evidence. The fixture-specific local trial script and its
dedicated recovery tests are deliberately not part of this PR.

## Root cause

Revision bindings retained the source name, but configuration projection
dropped it. Engine therefore exposed the collision-safe internal
registry name to the model. The companion Engine change adds an optional
Agent-local name while keeping storage identity and authorization
unchanged.

Companion:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1561.

## Test plan

- [x] Independent review finding fixed: old accepted drafts must not be
rejected when replayed; 14 regression cases cover compatibility.
- [x] Before main refresh: related backend suite 634 passed; backend
static/complexity/file-length checks passed.
- [x] After rebase onto main including resource snapshot changes: 89
targeted tests passed, including authoring, turn snapshots and runtime
projections.
- [x] Companion Engine verifies exact legacy replay using real service
code and PGlite persistence (11 binding tests passed).
- [x] CI follow-up: refreshed the inherited-baseline commit regression
to assert exact logical names along with unchanged skill IDs/versions.
The inherited-materialization business suite remains in this PR.
- [x] Real local single-lane test on the existing test Agent and its
existing active/Build sessions: both model turns succeeded, actual
provider system captures use logical names, and each turn successfully
read five global skills, one source-owned skill and its relative script.
- [x] Real authoring HTTP gateway plus encrypted Mongo: legacy draft
read/validate/edit/rename and new-invalid-name rejection; draft
operations restored.
- [x] Implicit global set and explicit empty set checked; active config
and sandbox view restored. No Agent/skill/session created. Test history
retained.

The full real-runtime trial preceded the main refresh; the refresh was
validated with targeted regression tests and static gates, not claimed
as another live trial. Build file reads and the authoring gateway were
exercised separately: no claim that the model itself successfully called
source_read. ACS/external Feishu delivery was out of scope.

## Rollout / scope

Deploy the companion Engine compatibility change before claw-interface.
No frontend release, registry rewrite or production data migration is
included. Existing persisted configs require a later normal revision
projection or a separately authorized migration; this PR does not
silently rewrite them.

Local environment repair was separately authorized: four missing staging
R2 blobs were added only after hash verification with absent-only
writes; existing objects and registry records were unchanged. No
credentials are included.
```

来源：SerendipityOneInc/ecap-workspace @ c6333408，PR #3816，作者 kaka-srp。