---
title: "修复：个人版用户在境外用邮箱登录会被区域校验挡住"
type: "Bug Fix"
priority: "高"
date: "2026-09-03"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：个人版用户在境外用邮箱登录会被区域校验挡住

## 核心宣传点

邮箱登录的区域准入校验以前有两个毛病。一是判断口径太窄：Web 路由只在请求头 `cf-ipcountry=CN` 时才去调准入服务，后端也只认「活跃的团队组织（Team Org）」，于是个人组织（Personal Org）上明明已经存了权威的区域信息，登录时却完全不看，把人挡在外面。二是漏了个洞：请求里如果压根没带国家头，整套区域准入检查等于被绕过去了。

现在的逻辑是：活跃团队组织的邮箱登录资格不受区域影响，行为完全不变；个人组织用户如果配置了明确的非中国区 `region_code`，就按这个区域正常放行；个人组织上没有权威区域信息时，回落到规范化后的 `cf-ipcountry`；而当国家信息缺失或非法时改为「失败关闭」（fail closed），不再放行。请求方的 IP 国家信息也会经 Web 的邮箱验证码 BFF 层透传给后端。

考虑到 Web 与后端是分批灰度发布的，这次同时保留了对旧版严格后端 schema 的兼容，滚动升级期间登录行为不会抖动。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f2254e5657bd697a20b3c20b5bf76b0e78d40052`
- PR: #3633
- 作者: sam-srp
- 日期: 2026-09-03T07:34:30Z

### Commit Message

```
fix(auth): honor personal org region for email login (#3633)

## Summary
- keep active Team Org email login eligibility unchanged regardless of
region
- let Personal Org users authenticate using an explicitly configured
non-CN `region_code`
- fall back to normalized `cf-ipcountry` when no authoritative
personal-org region exists, and fail closed when the IP country is
missing or invalid
- pass the request IP country through the Web email-OTP BFF to
`claw-interface`
- preserve login behavior against the previous strict backend schema
during a staggered Web/backend rollout
- constrain AnyIO below 4.15 until the pinned Starlette version stops
importing its newly deprecated alias

## Root cause
The existing Web route only called the eligibility service for
`cf-ipcountry=CN`, while the backend only accepted active Team Orgs.
This ignored the authoritative region already stored on Personal Orgs
and allowed a missing country header to bypass regional eligibility
checks.

## Test plan
- [x] `pytest -q tests/unit/test_domestic_access.py
tests/unit/test_domestic_access_routes.py` (23 passed)
- [x] `bash scripts/verify-web.sh
web/app/src/app/api/auth/email-otp/send/route.ts
web/app/src/lib/auth/domestic-access-bff.ts
web/app/tests/unit/app/api/auth-routes.unit.spec.ts` (12 files, 91 tests
passed)
- [x] rollout compatibility tests for legacy CN, non-CN, and
unknown-country eligibility paths (19 focused route tests passed)
- [x] Ruff check/format, targeted Pyright for all changed Python files,
and import-linter contracts
- [ ] Full local Pyright is blocked by an existing environment-dependent
type error in unchanged `app/connectors/google.py:131`; CI will run in
the repository-pinned environment
```

### PR Body

```
## Summary
- keep active Team Org email login eligibility unchanged regardless of region
- let Personal Org users authenticate using an explicitly configured non-CN `region_code`
- fall back to normalized `cf-ipcountry` when no authoritative personal-org region exists, and fail closed when the IP country is missing or invalid
- pass the request IP country through the Web email-OTP BFF to `claw-interface`
- preserve login behavior against the previous strict backend schema during a staggered Web/backend rollout
- constrain AnyIO below 4.15 until the pinned Starlette version stops importing its newly deprecated alias

## Root cause
The existing Web route only called the eligibility service for `cf-ipcountry=CN`, while the backend only accepted active Team Orgs. This ignored the authoritative region already stored on Personal Orgs and allowed a missing country header to bypass regional eligibility checks.

## Test plan
- [x] `pytest -q tests/unit/test_domestic_access.py tests/unit/test_domestic_access_routes.py` (23 passed)
- [x] `bash scripts/verify-web.sh web/app/src/app/api/auth/email-otp/send/route.ts web/app/src/lib/auth/domestic-access-bff.ts web/app/tests/unit/app/api/auth-routes.unit.spec.ts` (12 files, 91 tests passed)
- [x] rollout compatibility tests for legacy CN, non-CN, and unknown-country eligibility paths (19 focused route tests passed)
- [x] Ruff check/format, targeted Pyright for all changed Python files, and import-linter contracts
- [ ] Full local Pyright is blocked by an existing environment-dependent type error in unchanged `app/connectors/google.py:131`; CI will run in the repository-pinned environment
```
