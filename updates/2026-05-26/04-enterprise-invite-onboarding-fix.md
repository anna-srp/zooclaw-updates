---
title: "企业邀请入驻流程修复"
type: "Bug Fix"
priority: "高"
date: "2026-05-26"
status: "待审核"
channels: "Discord + changelog"
---
# 企业邀请入驻流程修复

## 核心宣传点

通过企业邀请链接加入团队的流程现在更顺畅，注册和加入步骤清晰分开，减少卡壳情况。

## 原始内容

**Commit:** 3bc3dbb6
**Repo:** ecap-workspace
**Author:** bill-srp

**Commit Message:**
```
fix(enterprise): align invite onboarding flow (#1936)

## Summary
- split account registration into explicit `/account`,
`/account/personal-org`, and `/account/invite` paths
- document that old combined `POST /account` compatibility is
intentionally not kept because the split happened before release
- route enterprise join through `/account/invite` and guard missing
invite context before firing the mutation
- include non-expired pending org invites in `/orgs/{org_id}/users` and
render pending invite rows in admin users
- provision team org billing plan and grant initial team credits with a
retry-safe idempotent topup transaction

## Reviewer Notes
- `POST /account` is intentionally account-only; org creation and invite
redemption must use the split routes.
- Trial credits remain limited to newly created personal registrations.
- Duplicate-subscription handling is narrowed to duplicate-looking
Billing Gateway 400 responses.
- Pending invite rows exclude expired invites.

## Tests
- `docker exec enterprise-bill sh -lc "cd
/workspaces/enterprise/services/claw-interface && .venv/bin/python -m
ruff check app/services/org/org_service.py
tests/unit/test_org_service.py && .venv/bin/python -m pytest
tests/unit/test_org_service.py -q"`
- `docker exec enterprise-bill sh -lc "cd
/workspaces/enterprise/services/claw-interface && .venv/bin/python -m
ruff check app/routes/account.py"`
- `docker exec enterprise-bill sh -lc "cd
/workspaces/enterprise/services/claw-interface && .venv/bin/python -m
pytest tests/unit/test_org_invite_repo.py
tests/unit/test_routes_org_users.py -q"`
- focused backend account/org/org-users pytest suites passed
- `pnpm --dir web/enterprise-admin test
hooks/__tests__/useInvite.test.tsx`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- focused enterprise-admin invite/users vitest suites passed
- `pnpm --dir web run test:unit`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/packages/auth-client exec tsc --noEmit`

## Local Check Notes
- `pnpm --dir web run lint` fails on pre-existing generated coverage
warning: `web/enterprise-admin/coverage/block-navigation.js`
- `pnpm --dir web run tsc` fails because the root script passes
unsupported `--if-present` to this local pnpm
- backend `pyright` is not installed in the devcontainer venv
- full backend pytest hits local worktree/devcontainer issues in deptry
and OpenClaw unclosed socket warnings; focused touched suites pass
```

**PR #1936: fix(enterprise): align invite onboarding flow**

## Summary
- split account registration into explicit `/account`, `/account/personal-org`, and `/account/invite` paths
- document that old combined `POST /account` compatibility is intentionally not kept because the split happened before release
- route enterprise join through `/account/invite` and guard missing invite context before firing the mutation
- include non-expired pending org invites in `/orgs/{org_id}/users` and render pending invite rows in admin users
- provision team org billing plan and grant initial team credits with a retry-safe idempotent topup transaction

## Reviewer Notes
- `POST /account` is intentionally account-only; org creation and invite redemption must use the split routes.
- Trial credits remain limited to newly created personal registrations.
- Duplicate-subscription handling is narrowed to duplicate-looking Billing Gateway 400 responses.
- Pending invite rows exclude expired invites.

## Tests
- `docker exec enterprise-bill sh -lc "cd /workspaces/enterprise/services/claw-interface && .venv/bin/python -m ruff check app/services/org/org_service.py tests/unit/test_org_service.py && .venv/bin/python -m pytest tests/unit/test_org_service.py -q"`
- `docker exec enterprise-bill sh -lc "cd /workspaces/enterprise/services/claw-interface && .venv/bin/python -m ruff check app/routes/account.py"`
- `docker exec enterprise-bill sh -lc "cd /workspaces/enterprise/services/claw-interface && .venv/bin/python -m pytest tests/unit/test_org_invite_repo.py tests/unit/test_routes_org_users.py -q"`
- focused backend account/org/org-users pytest suites passed
- `pnpm --dir web/enterprise-admin test hooks/__tests__/useInvite.test.tsx`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- focused enterprise-admin invite/users vitest suites passed
- `pnpm --dir web run test:unit`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/packages/auth-client exec tsc --noEmit`

## Local Check Notes
- `pnpm --dir web run lint` fails on pre-existing generated coverage warning: `web/enterprise-admin/coverage/block-navigation.js`
- `pnpm --dir web run tsc` fails because the root script passes unsupported `--if-present` to this local pnpm
- backend `pyright` is not installed in the devcontainer venv
- full backend pytest hits local worktree/devcontainer issues in deptry and OpenClaw unclosed socket warnings; focused touched suites pass
