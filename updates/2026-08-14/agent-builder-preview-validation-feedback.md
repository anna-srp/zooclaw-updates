---
title: "预览校验失败不再误报成功，问题直接显示出来"
type: "Bug Fix"
priority: "中"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

预览生成失败时页面曾错误地弹出成功提示；现在会明确给出警告和失败原因，并把项目退回草稿状态继续修改。

## 原始内容

fix(agent-builder): surface preview validation repairs (#3386)

## Summary
- Preserve repairable Preview preflight failures after they are
delivered to Builder, while returning the Project to `drafting`.
- Render the resulting state as a warning in Agent Builder and replace
the misleading success toast for synchronous failures.
- Refine Preview-result feedback so technical gaps are fixed directly,
product or interaction changes wait for explicit approval, and changes
are validated before asking for Refresh Preview.
- Document the cross-repo repair-loop contract.

## Root cause
Preview preflight correctly blocked invalid candidates and posted the
validation error to Builder, but successful delivery cleared the Project
failure fields. The frontend therefore had no state indicating that no
Test Agent was created and showed an unconditional success toast. The
feedback prompt also did not distinguish technical repairs from product
decisions or require post-change validation.

## Cross-repo dependency
Companion Agent Studio PR:
https://github.com/SerendipityOneInc/ecap-agent-pack/pull/243. It adds
the V1 and V2 feedback repair gate and bumps both Pack versions.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pytest tests/unit/test_agent_builder_service.py -q` — 170 passed
- [x] Targeted Agent Builder frontend tests — 81 passed
- [x] Commit hooks: frontend lint, Python
ruff/format/pyright/import-linter and repository guards

---
### PR Body

## Summary
- Preserve repairable Preview preflight failures after they are delivered to Builder, while returning the Project to `drafting`.
- Render the resulting state as a warning in Agent Builder and replace the misleading success toast for synchronous failures.
- Refine Preview-result feedback so technical gaps are fixed directly, product or interaction changes wait for explicit approval, and changes are validated before asking for Refresh Preview.
- Document the cross-repo repair-loop contract.

## Root cause
Preview preflight correctly blocked invalid candidates and posted the validation error to Builder, but successful delivery cleared the Project failure fields. The frontend therefore had no state indicating that no Test Agent was created and showed an unconditional success toast. The feedback prompt also did not distinguish technical repairs from product decisions or require post-change validation.

## Cross-repo dependency
Companion Agent Studio PR: https://github.com/SerendipityOneInc/ecap-agent-pack/pull/243. It adds the V1 and V2 feedback repair gate and bumps both Pack versions.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pytest tests/unit/test_agent_builder_service.py -q` — 170 passed
- [x] Targeted Agent Builder frontend tests — 81 passed
- [x] Commit hooks: frontend lint, Python ruff/format/pyright/import-linter and repository guards

