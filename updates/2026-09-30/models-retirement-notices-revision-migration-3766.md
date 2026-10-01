---
title: "模型选择里新增下线提示：显示下线日期与替代模型，过期选项置灰且不影响正在进行的对话"
type: "Feature"
priority: "高"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 模型选择里新增下线提示：显示下线日期与替代模型，过期选项置灰且不影响正在进行的对话

## 核心宣传点

Agent 可能在自己的产品源、Auto 目标或继承的默认值里一直留着已经排期下线的模型。这次把新版模型选择和引擎的生命周期元数据连起来：选择列表会显示下线日期和替代模型，已过期的选项直接禁用，模型目录和当前模型状态会刷新，旧版行为和权限范围都不变。更重要的是，它绝不会在聊天请求过程中偷偷换掉你的模型——模型变更只通过显式的、不可变的产品 Revision 迁移完成。新建 Agent 时，已过期的继承默认值会按 owner 权限（含图像生成权限）落地成具体值，迁移过程保留 Auto 设置，并把受影响的辅助默认值固化进新的 Revision。运维侧提供了配合引擎 plan/canary/分批工作流的迁移模块，会校验 owner 权益、未应用草稿、计划摘要、辅助状态和金丝雀指纹，发现漂移立即停止。本次没有改动任何生产或预发的用户数据。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

Agents can retain models scheduled for removal in their product source,
Auto targets or inherited defaults. This connects V2 model selection to
Engine lifecycle metadata and adds explicit operator migration through
immutable product Revisions. It never changes models during a chat
request.

- Show retirement dates/replacements, disable expired choices, and
refresh V2 catalog/current-model state without changing V1 behavior or
expanding entitlement.
- Materialize expired inherited defaults for new Agents with owner
permissions, including image-generation permissions. Migration preserves
Auto and materializes affected helper defaults into a new Revision.
- Provide the in-pod operator module used by Engine’s
plan/canary/serial-batch workflow. Check owner entitlement, unapplied
drafts, plan digest, CAS, auxiliary state and the exact canary
retirement fingerprint; stop on drift. Canary artifact provenance is
enforced by the companion Engine workflow.

Companion:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1482. Deploy
Engine’s additive schema, controld and all workers first, then this PR;
enable retirement operations only after both are deployed. The canonical
runbook is in the Engine PR. No production/staging user data was
changed.

Validation: 139 targeted Python tests passed; after extracting
install-default handling, all 95 directly related tests passed again.
`verify-py.sh` (ruff, pyright, 8 import contracts), frontend
typecheck/governance/lint, model hook/presentation tests and 20
model-picker tests passed. Commit and changed-surface push hooks also
run repository checks. CI follow-up regressions also passed: 52 backend
tests and 106 frontend tests. Full remote CI remains authoritative.

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8156c3048083fe5bb6b321dc7f5209bb2f5e6c2b`
- PR: #3766
- 作者：Chris@ZooClaw
- 日期：2026-09-30T12:19:29Z

### Commit Message

```
feat(models): add retirement notices and revision-aware migration (#3766)

Agents can retain models scheduled for removal in their product source,
Auto targets or inherited defaults. This connects V2 model selection to
Engine lifecycle metadata and adds explicit operator migration through
immutable product Revisions. It never changes models during a chat
request.

- Show retirement dates/replacements, disable expired choices, and
refresh V2 catalog/current-model state without changing V1 behavior or
expanding entitlement.
- Materialize expired inherited defaults for new Agents with owner
permissions, including image-generation permissions. Migration preserves
Auto and materializes affected helper defaults into a new Revision.
- Provide the in-pod operator module used by Engine’s
plan/canary/serial-batch workflow. Check owner entitlement, unapplied
drafts, plan digest, CAS, auxiliary state and the exact canary
retirement fingerprint; stop on drift. Canary artifact provenance is
enforced by the companion Engine workflow.

Companion:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1482. Deploy
Engine’s additive schema, controld and all workers first, then this PR;
enable retirement operations only after both are deployed. The canonical
runbook is in the Engine PR. No production/staging user data was
changed.

Validation: 139 targeted Python tests passed; after extracting
install-default handling, all 95 directly related tests passed again.
`verify-py.sh` (ruff, pyright, 8 import contracts), frontend
typecheck/governance/lint, model hook/presentation tests and 20
model-picker tests passed. Commit and changed-surface push hooks also
run repository checks. CI follow-up regressions also passed: 52 backend
tests and 106 frontend tests. Full remote CI remains authoritative.

---------

Co-authored-by: Claude Opus 5.5 <noreply@anthropic.com>
```

来源：SerendipityOneInc/ecap-workspace @ 8156c304，PR #3766，作者 Chris@ZooClaw。
