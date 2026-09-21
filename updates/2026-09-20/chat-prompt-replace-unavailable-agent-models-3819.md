---
title: "feat(chat): prompt to replace unavailable agent models (#3819)"
type: "新功能"
priority: "中"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# Agent 模型不可用时会提示你换一个，而不是直接失败

## 核心宣传点

已安装的 Agent 可能还挂着你账号里已经不再提供的模型。现在打开这类 Agent 的会话，会在模型列表加载完成后弹出一个紧凑的替换弹窗让你挑新模型：按目录原始顺序展示、默认预选 is_default，带供应商图标、消耗倍率、详情、搜索和滚动。关掉弹窗不会丢会话和草稿，尝试发送会重新弹出而不提交、也不清空已输入内容和附件。模型目录为空时视为无法判断，不弹窗也不阻止发送；保存失败会保留你的选择，保存成功沿用原有的运行时重启流程。Auto 配置仍然有效，托管/只读 Agent 不在范围内。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已合并待发版

## PR 说明

## Problem and behavior

An installed Agent can retain a model that is no longer in the user's available catalog. Opening its conversation now prompts the user to choose a replacement after both model queries have completed successfully. Dismissing the prompt preserves the conversation and draft; trying to send reopens it without submitting or clearing text/attachments.

The compact dialog uses the catalog's original order and preselects `is_default`, with provider icons, consumption multipliers, details, scrolling, and search. It does not synthesize Auto. Supported existing Auto configurations remain valid. Empty catalogs are inconclusive and do not prompt or block sending; failed saves preserve the selection, and successful changes retain the existing runtime restart flow.

Scope: editable installed Agent conversations using the workspace model API. Managed/read-only Agents, draft creation, and Builder-specific model controllers are excluded. Includes English and Chinese copy. Deploy frontend and backend. The backend reports Revision-managed engine models as managed, matching the existing direct-update restriction; ordinary engine models remain editable.

## Validation

- `scripts/verify-web.sh` passed: governance guards, TypeScript, targeted Vitest, ESLint.
- Review follow-up: 64 targeted frontend tests and 14 agent-model service tests passed; frontend type/lint checks and backend ruff, pyright, and import checks passed.
- 22 existing shared ModelPicker tests passed.
- Regression coverage: normalized IDs, loading/errors, managed Agents, supported Auto, empty catalogs, workspace switching, dismissal/send guard, draft preservation, catalog ordering/default selection, save failure/retry, and search.
- Full app test/build suites are delegated to CI. No production configuration was modified.

## Review decisions

- Empty successful catalogs fail open; removed the unused guard `empty` field.
- Restored shared query `ready` semantics and exposed post-mount freshness separately for the warning guard.
- Fixed the concrete Revision-managed case instead of treating all engine Agents as read-only.
- Retained the agreed nonempty-catalog send guard and API-only replacement options. Adding synthetic Auto or bypassing a confirmed missing model would change the approved interaction.

## Final review verification

- All 46 reported checks completed successfully or were intentionally skipped. Codex found no issues. Claude confirmed the three fixes and requested confirmation of a legacy authoring-model scenario.
- The installation resolver can accept pack defaults present in the engine catalog, so it would be incorrect to assert that internal IDs can never appear on installed Agents. However, the replacement path resolves the newly requested model against the engine catalog; it does not depend on the old primary model or reject replacements because that old ID is internal. Builder controllers remain excluded. No concrete additional defect was established from the legacy-ID hypothesis; do not make all engine models read-only. General catalog/runtime divergence remains a follow-up rather than a reason to alter the approved send guard in this PR.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `a2013e3261a75791f746f6326521b23a09162cd5`
- PR: #3819
- 作者：tim-srp
- 日期：2026-09-20T14:45:07Z

### Commit Message

```
feat(chat): prompt to replace unavailable agent models (#3819)

## Problem and behavior

An installed Agent can retain a model that is no longer in the user's
available catalog. Opening its conversation now prompts the user to
choose a replacement after both model queries have completed
successfully. Dismissing the prompt preserves the conversation and
draft; trying to send reopens it without submitting or clearing
text/attachments.

The compact dialog uses the catalog's original order and preselects
`is_default`, with provider icons, consumption multipliers, details,
scrolling, and search. It does not synthesize Auto. Supported existing
Auto configurations remain valid. Empty catalogs are inconclusive and do
not prompt or block sending; failed saves preserve the selection, and
successful changes retain the existing runtime restart flow.

Scope: editable installed Agent conversations using the workspace model
API. Managed/read-only Agents, draft creation, and Builder-specific
model controllers are excluded. Includes English and Chinese copy.
Deploy frontend and backend. The backend reports Revision-managed engine
models as managed, matching the existing direct-update restriction;
ordinary engine models remain editable.

## Validation

- `scripts/verify-web.sh` passed: governance guards, TypeScript,
targeted Vitest, ESLint.
- Review follow-up: 64 targeted frontend tests and 14 agent-model
service tests passed; frontend type/lint checks and backend ruff,
pyright, and import checks passed.
- 22 existing shared ModelPicker tests passed.
- Regression coverage: normalized IDs, loading/errors, managed Agents,
supported Auto, empty catalogs, workspace switching, dismissal/send
guard, draft preservation, catalog ordering/default selection, save
failure/retry, and search.
- Full app test/build suites are delegated to CI. No production
configuration was modified.

## Review decisions

- Empty successful catalogs fail open; removed the unused guard `empty`
field.
- Restored shared query `ready` semantics and exposed post-mount
freshness separately for the warning guard.
- Fixed the concrete Revision-managed case instead of treating all
engine Agents as read-only.
- Retained the agreed nonempty-catalog send guard and API-only
replacement options. Adding synthetic Auto or bypassing a confirmed
missing model would change the approved interaction.

## Final review verification

- All 46 reported checks completed successfully or were intentionally
skipped. Codex found no issues. Claude confirmed the three fixes and
requested confirmation of a legacy authoring-model scenario.
- The installation resolver can accept pack defaults present in the
engine catalog, so it would be incorrect to assert that internal IDs can
never appear on installed Agents. However, the replacement path resolves
the newly requested model against the engine catalog; it does not depend
on the old primary model or reject replacements because that old ID is
internal. Builder controllers remain excluded. No concrete additional
defect was established from the legacy-ID hypothesis; do not make all
engine models read-only. General catalog/runtime divergence remains a
follow-up rather than a reason to alter the approved send guard in this
PR.
```

来源：SerendipityOneInc/ecap-workspace @ a2013e32，PR #3819，作者 tim-srp。