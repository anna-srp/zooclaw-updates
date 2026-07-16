---
title: "Agent Studio 新建/Fork 时按目录模型策略配置（含折扣模型）"
type: "产品基础功能更新"
priority: "中"
date: "2026-07-15"
status: "待审核"
channels: ""
tags: []
---

# Agent Studio 新建/Fork 时按目录模型策略配置（含折扣模型）

## 核心宣传点
在 Agent Builder（Agent Studio）新建或 Fork 项目时，会按官方模型目录策略为新项目分配默认模型（含 Agent Studio 专属折扣模型），避免新建的 Builder 误用全价全局默认模型；后续打开/更新/重装等已有项目路径保持不变。

## 原始内容
### PR #2879 — feat(agent-builder): enforce Agent Studio model policy on creation (#2879)
作者: bill-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2879

## Summary

- Apply the discounted Agent Studio model policy only to the bootstrap that actually inserts a new Agent Builder project or fork.
- Keep reuse and every later lifecycle path independent of the catalog while preserving the shared-runtime routing/binding behavior that predates this change.
- Keep both discounted aliases internal, preserve the Sonnet 5 degradation mapping, and retain a repository-only guarded catalog updater.

Linear: https://linear.app/srpone/issue/ECA-1216

## Root cause

The V2 Agent Builder install path did not carry the official catalog model into the shared `agent_studio` entry, so a newly created Builder could inherit the full-price global default. The earlier implementation in this PR then made the catalog/model check too broad: generic official installs and later opens of existing Builder projects could depend on Agent Builder catalog availability or model convergence.

This revision makes the model an explicit, request-scoped input owned by the creation bootstrap. Generic install code can accept an explicit model but never resolves Agent Builder policy itself.

## Accepted lifecycle boundary

- Strict model policy runs only when `create_or_reuse_project()` actually inserts a new project or `fork_project()` inserts a fork.
- Create reuse, later open/GET, Update Agent Builder, restore, and reinstall do not resolve catalog policy, compare models, or repair `model.primary`.
- A creation catalog/install/model/runtime-verification failure is terminal for that project. It remains closed; the user must create a new project.
- A creation bootstrap that has not reached success or failure stays non-interactive and cannot create a Builder conversation.
- All non-Agent-Builder pack installs have zero Agent Builder catalog dependency, including generic official/private/shared, multi-install, and WhatsApp paths.
- Catalog migration affects only projects created afterward. Because `agent_studio` is shared by computer, a later new project may change the shared runtime observed indirectly by older projects; an older project's open path still performs no model enforcement.
- The legacy empty-catalog fallback remains `openai/agent-studio-sonnet-4-6` until an explicit catalog migration.

## Safety and migration

- Creation accepts only `openai/agent-studio-sonnet-4-6` or `openai/agent-studio-sonnet-5`; missing, unexpected, duplicate, or unavailable policy fails closed with sanitized errors.
- Live policy lookup reads the full official catalog and rejects duplicate normalized `agent_studio` rows deterministically, including whitespace-padded siblings.
- Targeted runtime reconciliation changes only the unique existing `agent_studio.model.primary` and preserves unrelated agent/config fields.
- The updater is dry-run by default and supports explicit write and rollback modes. Write mode creates a whitespace-aware targeted partial unique index before its first catalog read and before compare-and-set, so exact or normalized duplicate/index races abort before a model write.
- The updater remains under `services/claw-interface/scripts/`; it is not copied into the service image and is not called by app startup, deployment, CI, or release hooks.
- No staging/production deployment or live catalog mutation was performed as part of this PR.

## PR size exception

This is an incremental refactor of the existing ECA-1216 PR. Its full diff intentionally retains the superseded implementation history together with the authoritative spec/plan and the regression, lifecycle, and race tests needed to audit the changed design. Continuing on this PR was an explicit requirement; splitting now would lose implementation and review continuity. The `size-override` label waives only the size gate and is not evidence that functional checks passed.

## Test plan

- [x] Fresh affected suite: 562 passed, 0 skipped on Python 3.12.13.
- [x] Full-tree Ruff check passed; Ruff format check passed; all 8 import-linter contracts passed.
- [x] Scoped Pyright for the changed non-repository service/route/schema/updater/test surfaces passed with 0 errors.
- [ ] Full-tree Pyright in CI.

[NOTE: merged_at date confirmed as 2026-07-15 by updated-order position between #2880 (2026-07-15T06:39) and #2878 (2026-07-14T13:22); exact merge timestamp not retrievable due to tool output truncation. Body captured up to test plan; a trailing 'Staged release validation prerequisites' section was truncated by the API tool and could not be fully retrieved.]

## 备注
外部B级。本条为 2026-07-15 每日同步补录（原 cron 仅写入 raw，未落 updates/ 与多维表）。
