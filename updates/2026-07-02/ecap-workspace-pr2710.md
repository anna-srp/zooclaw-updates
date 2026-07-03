---
title: "修复部分老账号缺失组织信息导致无法正常使用的问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# 修复部分老账号缺失组织信息导致无法正常使用的问题
## 核心宣传点
部分早期账号因缺失组织信息登录后功能异常，现在系统会自动修复这类账号，进入即可正常使用。
## 原始内容
### [ecap-workspace PR #2710]

fix(auth): repair orgless accounts via org endpoint (#2710)

## Summary
- Repair existing webapp accounts with `org: null` through the dedicated
personal-org endpoint.
- Keep new-account bootstrap on `/account/personal-org`; only existing
orgless accounts use `/orgs/personal`.

## Root cause
The webapp treated both `account.not_found` and `200 + org: null` as the
same bootstrap case, so existing accounts missing org membership retried
`/account/personal-org`. That endpoint is for account registration plus
personal-org creation and rejects already existing accounts.

## Test plan
- [x] `git diff --check`
- [x] Backend smoke for existing org route behavior:
`/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_routes_account.py::TestRegisterHandler::test_personal_org_route_creates_personal_org
services/claw-interface/tests/unit/test_routes_account.py::TestRegisterHandler::test_personal_org_route_returns_existing_membership
-q`
- [ ] Frontend Vitest/tsc/eslint could not run locally: `pnpm` is
blocked by `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`, and local
`node_modules/.bin/{vitest,tsc,eslint}` point at missing packages.

---

## PR Description

## Summary
- Repair existing webapp accounts with `org: null` through the dedicated personal-org endpoint.
- Keep new-account bootstrap on `/account/personal-org`; only existing orgless accounts use `/orgs/personal`.

## Root cause
The webapp treated both `account.not_found` and `200 + org: null` as the same bootstrap case, so existing accounts missing org membership retried `/account/personal-org`. That endpoint is for account registration plus personal-org creation and rejects already existing accounts.

## Test plan
- [x] `git diff --check`
- [x] Backend smoke for existing org route behavior: `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_routes_account.py::TestRegisterHandler::test_personal_org_route_creates_personal_org services/claw-interface/tests/unit/test_routes_account.py::TestRegisterHandler::test_personal_org_route_returns_existing_membership -q`
- [ ] Frontend Vitest/tsc/eslint could not run locally: `pnpm` is blocked by `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`, and local `node_modules/.bin/{vitest,tsc,eslint}` point at missing packages.

