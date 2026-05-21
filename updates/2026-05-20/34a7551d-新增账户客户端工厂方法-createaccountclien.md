---
title: "新增账户客户端工厂方法 createAccountClient"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "34a7551de9cf502f4cc5cf7658073ebadf688b7c"
pr: 1759
---
# 新增账户客户端工厂方法 createAccountClient

## 核心宣传点

账户管理底层能力增强，为后续企业版多账户管理功能提供技术支撑。

## 原始内容

### Commit Message

```
feat(auth-client): Add createAccountClient factory (#1759)

## Summary

- **`createAccountClient({ accountUrl })` factory** — exposes
`sendEmailOTP`, `verifyEmailOTP`, `getUserMe` as bound methods on a
client object. Consumers configure the account-service base URL once at
construction time and get short call sites. Pattern keeps the shared
package decoupled from any specific env-var convention (follows the
earlier `getAccountBaseUrl(accountUrl)` injectable refactor).
- **10 unit tests** covering URL normalization (trailing slash stripped,
empty URL rejected at construction), POST body shape, optional
`device_id`, schema-validation failures, non-2xx error surfacing via
`body.message`, GET `/user/me` with bearer header, 401 path, and the
full org-bearing UserMe parse.
- **Plan amendment** marking Task A8 (migrate `web/app` to consume the
shared package) as skipped. `web/app/src/lib/auth/api.ts` has three
product-specific concerns the shared package doesn't model:
`?business=ecap` query param, `apiClient` wrapper required by the
`no-raw-fetch` ESLint rule, and `noAutoAuth: true` opt-out. A naive
migration would change live-login semantics. The plan records a re-eval
trigger for when the next change to web/app's account-service protocol
comes up.

This is Phase A6 + A9 of the plan merged in #1757. No `web/app`
production code touched.

## Test plan

- [x] `pnpm --filter @zooclaw/auth-client run test` — 26/26 passing (4
files)
- [x] `pnpm --filter @zooclaw/auth-client exec tsc --noEmit` — clean
- [x] `pnpm --filter @zooclaw/auth-client run lint` — zero warnings
- [x] `pnpm --filter @zooclaw/web-app run test:unit` — 5503/5503 passing
(confirms no production regression)
- [ ] CI `code-quality / lint-and-test` passes on `web/**` changes
- [ ] CI `auto-review` passes
```

### PR Description

## Summary

- **`createAccountClient({ accountUrl })` factory** — exposes `sendEmailOTP`, `verifyEmailOTP`, `getUserMe` as bound methods on a client object. Consumers configure the account-service base URL once at construction time and get short call sites. Pattern keeps the shared package decoupled from any specific env-var convention (follows the earlier `getAccountBaseUrl(accountUrl)` injectable refactor).
- **10 unit tests** covering URL normalization (trailing slash stripped, empty URL rejected at construction), POST body shape, optional `device_id`, schema-validation failures, non-2xx error surfacing via `body.message`, GET `/user/me` with bearer header, 401 path, and the full org-bearing UserMe parse.
- **Plan amendment** marking Task A8 (migrate `web/app` to consume the shared package) as skipped. `web/app/src/lib/auth/api.ts` has three product-specific concerns the shared package doesn't model: `?business=ecap` query param, `apiClient` wrapper required by the `no-raw-fetch` ESLint rule, and `noAutoAuth: true` opt-out. A naive migration would change live-login semantics. The plan records a re-eval trigger for when the next change to web/app's account-service protocol comes up.

This is Phase A6 + A9 of the plan merged in #1757. No `web/app` production code touched.

## Test plan

- [x] `pnpm --filter @zooclaw/auth-client run test` — 26/26 passing (4 files)
- [x] `pnpm --filter @zooclaw/auth-client exec tsc --noEmit` — clean
- [x] `pnpm --filter @zooclaw/auth-client run lint` — zero warnings
- [x] `pnpm --filter @zooclaw/web-app run test:unit` — 5503/5503 passing (confirms no production regression)
- [ ] CI `code-quality / lint-and-test` passes on `web/**` changes
- [ ] CI `auto-review` passes
