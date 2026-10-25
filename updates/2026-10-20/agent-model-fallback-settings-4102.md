---
title: "Agent 设置支持配置备用模型，主模型不可用时自动兜底"
type: "新功能"
priority: "高"
date: "2026-10-20"
status: "待审核"
channels: ""
---

# Agent 设置支持配置备用模型，主模型不可用时自动兜底

## 核心宣传点

Agent 设置面板新增「模型兜底」能力：可以开启兜底开关，并按顺序挑选最多两个备用模型，保存走现有的 Revision/ChangeSet 流程。界面会明确区分模型不支持、未知、已保存来源、运行中状态以及个人订阅绑定关系；后端会校验模型权限与协议支持，保存时沿用现有 CAS 与幂等回执，运行态与保存态不一致时需要逐项确认。退出个人订阅会自动清掉已不可用的备用模型并关闭兜底，同时保留已保存的 Revision。无需新增表、索引或迁移，也不依赖独立发版开关。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 备注

包含仅开发环境使用的 Mattermost 同源 mock 代理，用于本地验证设置页。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `dba0d9047c8ec38ffc10cf313d094c9ec005fa52`
- PR: #4102
- 作者：kaka-srp
- 日期：2026-10-20T10:05:04Z

### Commit Message

```
feat(agents): configure model fallback in Agent settings (#4102)

## Summary

Adds fallback controls to the existing Agent Settings panel: opt in,
select up to two ordered backup models, and save through the existing
Revision/ChangeSet flow. Reads distinguish unsupported/unknown, saved
source, running state, and personal subscription binding.

The backend validates model access and supported protocols, preserves
unrelated model fields, and uses the existing configuration/revision CAS
and idempotency receipts. Runtime drift requires confirmation of each
affected field; saved resource changes resume their original pending
operation. Leaving a personal subscription automatically clears
unavailable backups and disables fallback while preserving the saved
Revision.

Includes the development-only same-origin Mattermost mock proxy needed
to validate the Settings UI on localhost:3000. No new table, collection,
index, migration, deployment flag, or independent model-settings dialog.
Fallback is not enabled for existing Agents. Requires the Engine
fallback support already merged in SerendipityOneInc/zooclaw-engine#2047
and #2048; follows issue SerendipityOneInc/zooclaw-engine#2041.

## Validation

- Independent Astra implementation review and targeted re-review;
verified findings fixed before submission.
- Focused frontend/backend regressions, TypeScript/ESLint/governance
checks, Ruff/format/Pyright/import contracts. Full CI exposed four stale
test fixtures; these now model the new Settings/rebase/apply contracts
and authoritative subscription readback (30 frontend and 16 backend
focused tests passed).
- Local browser → ECAP API → staging Mongo (CSFLE) → shared local
Engine/Temporal/PG/Redis validation: 13 real-model execution scenarios
covering 503/429 failover, two backups, continuation without duplicate
tools, next-run reset, disabled/fixed models, cancellation,
post-publication failure and terminal provider errors. Nine additional
rendered-config boundary checks; these are not scheduler/spawn E2E
proof.
- Review fixes have focused automated regressions; the 13 execution
scenarios preceded those fixes. Real Feishu send/receive was excluded as
requested. Real personal-provider authorization and full
share/install/resource-pending browser flows were not exercised end to
end.
- Detailed scope, outcomes and cleanup:
`docs/research/2026-10-20-agent-model-failover-settings-implementation-validation.md`.

Backend and frontend both require deployment; this PR does not publish
or deploy either surface.

Size exception: 3,315 governed lines after exclusions (including
regression coverage and review/validation evidence). This keeps the
frontend and backend contract change together; `size-override` is used
for this PR.
```

