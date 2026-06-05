---
title: "Agent Pack 定价与订阅计划后端上线"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-04"
status: "待审核"
channels: ""
sha: "9440881e41c0864539169f69c446d6cc2dd30861"
repo: "ecap-workspace"
pr: "2219"
---

# Agent Pack 定价与订阅计划后端上线

## 核心宣传点

ZooClaw Agent Pack 订阅定价功能的后端基础已就绪，为后续 Agent Pack 付费/试用计划的推出奠定基础。

## 原始内容

### Commit Message

```
feat(vertical-pack-plans): add internal CRUD API (#2219)

## Linear

https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary
- Add `VerticalPackPlan` schemas for plan/add-on pricing, billing
cycles, publish state, and soft deletion.
- Add a Mongo-backed vertical pack plan repository with indexes,
Decimal-safe persistence, update guards, and soft-delete filtering.
- Expose SRP-gated internal CRUD routes under
`/internal/vertical-pack-plans`.
- Document the implementation plan and design notes for the vertical
pack plans backend slice.

## Test plan
- [x] `ruff check .`
- [x] `pyright app tests`
- [x] Focused vertical-pack-plan unit tests
- [ ] Full backend coverage gate attempted locally; the devcontainer run
completed with existing unrelated failures in `test_ci_lint_deptry`,
`test_pagerduty_client`, and OpenClaw resource-warning setup paths, plus
local total coverage `88.42%` below the `90%` gate. The
vertical-pack-plan tests passed within that run.

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary
- Add `VerticalPackPlan` schemas for plan/add-on pricing, billing cycles, publish state, and soft deletion.
- Add a Mongo-backed vertical pack plan repository with indexes, Decimal-safe persistence, update guards, and soft-delete filtering.
- Expose SRP-gated internal CRUD routes under `/internal/vertical-pack-plans`.
- Document the implementation plan and design notes for the vertical pack plans backend slice.

## Test plan
- [x] `ruff check .`
- [x] `pyright app tests`
- [x] Focused vertical-pack-plan unit tests
- [ ] Full backend coverage gate attempted locally; the devcontainer run completed with existing unrelated failures in `test_ci_lint_deptry`, `test_pagerduty_client`, and OpenClaw resource-warning setup paths, plus local total coverage `88.42%` below the `90%` gate. The vertical-pack-plan tests passed within that run.

