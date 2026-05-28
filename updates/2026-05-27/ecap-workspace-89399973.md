---
title: "企业版支持 Team Wallet 个人组织自动初始化"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# 企业版支持 Team Wallet 个人组织自动初始化

## 核心宣传点

企业版用户现在可以自动获得个人组织空间，无需手动配置即可开始团队协作。

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**SHA**: [89399973](https://github.com/SerendipityOneInc/ecap-workspace/commit/89399973a65d946cd17d342e278971c853a99f24)
**PR**: [#1947](https://github.com/SerendipityOneInc/ecap-workspace/pull/1947)  
**作者**: bill-srp  
**日期**: 2026-05-27T03:42:37Z

**Commit Message:**

```
feat(enterprise): add personal org bootstrap (#1947)

## Linear
https://linear.app/srpone/issue/ECA-827/support-team-wallet-user

## Summary
- Add an idempotent personal org creation API and web BFF/client
wrapper.
- Create org + admin membership transactionally, reusing an existing
account team_id for billing when present.
- Include org context in legacy user/create and user/get responses, and
only call createPersonalOrg from the frontend when the user response has
no org.

## Test plan
- [x] docker exec -w /workspaces/enterprise/services/claw-interface
enterprise-bill /home/node/.venvs/claw-interface/bin/ruff check .
- [x] docker exec -w /workspaces/enterprise/services/claw-interface
enterprise-bill /home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_org_repo.py tests/unit/test_routes_org.py
tests/unit/test_routes_account.py tests/unit/test_org_service.py
tests/unit/test_enterprise_wiring.py
tests/unit/test_user_enrichment_service.py
tests/unit/test_user_routes_coverage.py -q
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm
run lint
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm
exec tsc --noEmit
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm
exec vitest run tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/lib/api/org.unit.spec.ts --config ./vitest.config.mts
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm
exec vitest run tests/unit/app/api/routes.unit.spec.ts -t
"/api/orgs/personal" --config ./vitest.config.mts

## Notes
- Full backend coverage run reached test completion but failed local
broad-suite coverage at 87.95% < 90 and also reported unrelated
full-suite failures/resource warnings.
- Full web unit run initially found the auth test setup issue fixed in
this branch; the other three admin hook timeouts passed when run
directly.
- web root lint failed on an existing generated coverage warning in
web/enterprise-admin/coverage/block-navigation.js; app-scoped lint
passed.
- web root tsc script failed because pnpm rejected --if-present in the
recursive exec script; app-scoped tsc passed.
```


**PR Description:**

## Linear
https://linear.app/srpone/issue/ECA-827/support-team-wallet-user

## Summary
- Add an idempotent personal org creation API and web BFF/client wrapper.
- Create org + admin membership transactionally, reusing an existing account team_id for billing when present.
- Include org context in legacy user/create and user/get responses, and only call createPersonalOrg from the frontend when the user response has no org.

## Test plan
- [x] docker exec -w /workspaces/enterprise/services/claw-interface enterprise-bill /home/node/.venvs/claw-interface/bin/ruff check .
- [x] docker exec -w /workspaces/enterprise/services/claw-interface enterprise-bill /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_org_repo.py tests/unit/test_routes_org.py tests/unit/test_routes_account.py tests/unit/test_org_service.py tests/unit/test_enterprise_wiring.py tests/unit/test_user_enrichment_service.py tests/unit/test_user_routes_coverage.py -q
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm run lint
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm exec tsc --noEmit
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm exec vitest run tests/unit/lib/auth/manager.unit.spec.ts tests/unit/lib/api/org.unit.spec.ts --config ./vitest.config.mts
- [x] docker exec -w /workspaces/enterprise/web/app enterprise-bill pnpm exec vitest run tests/unit/app/api/routes.unit.spec.ts -t "/api/orgs/personal" --config ./vitest.config.mts

## Notes
- Full backend coverage run reached test completion but failed local broad-suite coverage at 87.95% < 90 and also reported unrelated full-suite failures/resource warnings.
- Full web unit run initially found the auth test setup issue fixed in this branch; the other three admin hook timeouts passed when run directly.
- web root lint failed on an existing generated coverage warning in web/enterprise-admin/coverage/block-navigation.js; app-scoped lint passed.
- web root tsc script failed because pnpm rejected --if-present in the recursive exec script; app-scoped tsc passed.
