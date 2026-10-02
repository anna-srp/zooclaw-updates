---
title: "开发者平台 Project Key 可用于 Agent Webhook 接口，不再一律返回 404"
type: "新功能"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 开发者平台 Project Key 可用于 Agent Webhook 接口，不再一律返回 404

## 核心宣传点

开发者平台的 Project Key 虽然已经能通过运行时接口管理 Agent，但调用 Agent 的 Webhook 相关路由时一律返回 404，等于这块能力对 API 用户是封闭的。现在在已有的组织、显式项目归属等校验之后放开了 Agent 维度的 Webhook 路由，用 Project Key 就能为自己有权限的 Agent 配置和管理 Webhook，权限边界和原有校验顺序保持不变。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

Platform Project keys currently return 404 for every Agent webhook route, even when they can manage the same Agent through the runtime API. Allow the existing Agent-scoped webhook routes after the existing organization, explicit project (including default), and owner checks. Work owner/Agent routes stay available; Platform owner/project-wide registration remains unavailable.

Also strip caller `project_id` alongside `org_id`/`owner_uid`. Engine selects owner versus project creation from the query, so forwarding a caller project selector could change the Work owner route's scope. Engine continues to validate body scope and endpoint/event/delivery scope.

Keep Work idempotency hashes byte-compatible. Platform hashes add a credential-family/project namespace and remain stable across key rotation. Existing POST update/delete aliases and `Cache-Control: no-store` are retained. Update the service spec and API documentation. The receiver guidance explicitly requires durable enqueue before ACK, as already required by #3975; this is an intentional documentation correction.

Validation:
- 195 targeted webhook, Platform Agent runtime, and service proxy tests passed.
- Ruff, Pyright, import-linter and applicable pre-commit checks passed. The legacy GitHub-login suffix hook was skipped because this workspace explicitly requires Finn's verified `finn930` account; commit author is `finn-srp <finn@srp.one>`.
- `ecap-verify-py-ci` on final commit `7517de0f0`: Linux dependency resolution, static checks, all ci-lint guards and both duplication checks passed; 13,438 tests passed, 5 skipped, coverage 89.92% (CI threshold 89.5%).

All applicable GitHub checks passed, including backend tests/static checks, duplication checks and CodeQL. Codex and Claude reviews both approved with no actionable findings.

Refs #3975 and #3786. This PR delivers the backend portion only. SDK management helpers remain tracked in TypeScript #34/Python #5; public bilingual docs/Coding Skill and an authorized staging receiver smoke remain follow-ups. No Engine flags, deployments or live webhook tests were performed.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `e8a0e5f596baedd6f33ab84d6b4a86a10ce7f103`
- PR: #3976
- 作者：finn-srp
- 日期：2026-10-01T09:24:53Z

### Commit Message

```
feat(platform): enable agent-scoped webhooks for Project keys (#3976)

Platform Project keys currently return 404 for every Agent webhook
route, even when they can manage the same Agent through the runtime API.
Allow the existing Agent-scoped webhook routes after the existing
organization, explicit project (including default), and owner checks.
Work owner/Agent routes stay available; Platform owner/project-wide
registration remains unavailable.

Also strip caller `project_id` alongside `org_id`/`owner_uid`. Engine
selects owner versus project creation from the query, so forwarding a
caller project selector could change the Work owner route's scope.
Engine continues to validate body scope and endpoint/event/delivery
scope.

Keep Work idempotency hashes byte-compatible. Platform hashes add a
credential-family/project namespace and remain stable across key
rotation. Existing POST update/delete aliases and `Cache-Control:
no-store` are retained. Update the service spec and API documentation.
The receiver guidance explicitly requires durable enqueue before ACK, as
already required by #3975; this is an intentional documentation
correction.

Validation:
- 195 targeted webhook, Platform Agent runtime, and service proxy tests
passed.
- Ruff, Pyright, import-linter and applicable pre-commit checks passed.
The legacy GitHub-login suffix hook was skipped because this workspace
explicitly requires Finn's verified `finn930` account; commit author is
`finn-srp <finn@srp.one>`.
- `ecap-verify-py-ci` on final commit `7517de0f0`: Linux dependency
resolution, static checks, all ci-lint guards and both duplication
checks passed; 13,438 tests passed, 5 skipped, coverage 89.92% (CI
threshold 89.5%).

All applicable GitHub checks passed, including backend tests/static
checks, duplication checks and CodeQL. Codex and Claude reviews both
approved with no actionable findings.

Refs #3975 and #3786. This PR delivers the backend portion only. SDK
management helpers remain tracked in TypeScript #34/Python #5; public
bilingual docs/Coding Skill and an authorized staging receiver smoke
remain follow-ups. No Engine flags, deployments or live webhook tests
were performed.
```

来源：SerendipityOneInc/ecap-workspace @ e8a0e5f5，PR #3976，作者 finn-srp。
