---
title: "企业版新功能：组织级 Agent Pack 商店后端上线"
type: "新功能上线"
priority: "高"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 企业版新功能：组织级 Agent Pack 商店后端上线

## 核心宣传点

企业/团队用户即将可以在组织内部创建和分发专属 Agent Pack，让团队共享 AI 工作流成为可能。

## 原始内容

**Commit**: 6645dd5fd01f6d1731b2d924f65e6bd76dfeb650
**Author**: bill-srp
**Date**: 2026-05-22T06:29:48Z
**PR**: #1833

### Commit Message
```
feat(enterprise): add org pack store backend (#1833)

## Summary
- Adds org-scoped pack store schemas, repositories, services, and
enterprise routes.
- Wires Mongo collections and startup indexes for packs and submissions.
- Covers submission/review approval/deprecation flows, including
concurrent review CAS and deprecated-pack guards.

## Linear

https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Tests
- `docker exec service-agent-pack-bill ... ruff check .`
- `docker exec service-agent-pack-bill ... ruff format --check app
tests`
- `docker exec service-agent-pack-bill ... lint-imports`
- `docker exec service-agent-pack-bill ... pyright app tests`
- `docker exec service-agent-pack-bill ... pytest
tests/unit/test_schema_pack.py tests/unit/test_pack_repo.py
tests/unit/test_pack_submission_repo.py tests/unit/test_pack_services.py
tests/unit/test_routes_pack_store.py
tests/unit/test_enterprise_wiring.py -q`

Note: the full repository coverage command completed test execution but
failed locally in this devcontainer because `test_ci_lint_deptry.py`
cannot resolve the host worktree `.git` path from inside the container,
and the aggregate coverage report is 87.88% against the repository-wide
90% threshold.
```

### PR Description
## Summary
- Adds org-scoped pack store schemas, repositories, services, and enterprise routes.
- Wires Mongo collections and startup indexes for packs and submissions.
- Covers submission/review approval/deprecation flows, including concurrent review CAS and deprecated-pack guards.

## Linear
https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Tests
- `docker exec service-agent-pack-bill ... ruff check .`
- `docker exec service-agent-pack-bill ... ruff format --check app tests`
- `docker exec service-agent-pack-bill ... lint-imports`
- `docker exec service-agent-pack-bill ... pyright app tests`
- `docker exec service-agent-pack-bill ... pytest tests/unit/test_schema_pack.py tests/unit/test_pack_repo.py tests/unit/test_pack_submission_repo.py tests/unit/test_pack_services.py tests/unit/test_routes_pack_store.py tests/unit/test_enterprise_wiring.py -q`

Note: the full repository coverage command completed test execution but failed locally in this devcontainer because `test_ci_lint_deptry.py` cannot resolve the host worktree `.git` path from inside the container, and the aggregate coverage report is 87.88% against the repository-wide 90% threshold.

