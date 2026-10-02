---
title: "修复：开发者平台在新标签页或重新打开后不再要求重新登录"
type: "Bug Fix"
priority: "高"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：开发者平台在新标签页或重新打开后不再要求重新登录

## 核心宣传点

开发者平台此前只把账号 JWT 存在 sessionStorage 里，所以另开一个独立标签页、或者关掉页面再回来，即使令牌还有效也得再登一次。现在会持久化保存已验证的平台登录态，跨标签页和重新打开页面都能继续使用原会话，不用反复登录。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary / 改动
Platform previously stored its account JWT only in sessionStorage. Opening an independent tab or returning after closing the page required another login even while the token remained valid.

- Persist a verified, Platform-only JWT in a host-only HttpOnly/Secure/SameSite=Lax cookie, bounded by its signed expiry; migrate existing tab credentials without discarding them on transient failures.
- Add a same-origin Cloudflare Worker session BFF and `/platform/v1` proxy. Preserve `ecap-platform` identity isolation and existing upstream authorization/idempotency contracts; enforce same-origin mutations and no-store responses.
- Synchronize login/logout across tabs, revalidate confirmed business authentication errors without replaying writes, and preserve OTP/Google login across focus changes.
- Always route development, preview and production API calls through the page origin, ignoring legacy VITE_API_BASE_URL overrides. Wire Worker upstream URLs from existing deployment variables and document local development.

新标签页、关页重开可恢复登录；退出和切换账号同步其他标签页。业务 API 401 会重新验证账号，网络/权限故障不会误清会话，写操作不会自动重放。

## Root cause / 原因与边界
Session persistence was scoped to a browser tab, while business 401 responses had no identity recovery path. The existing interrupted-restoration fix (#3979) is retained.

Account service main currently signs registered-user JWTs for 300 days by default and has no general refresh-token endpoint. This PR respects the actual signed expiry; it does not invent renewal, extend tokens, share Work's cookie, change backend billing, or claim production validation. Actual expiry still requires sign-in.

## Validation / 验证
- [x] Platform lint and TypeScript checks
- [x] Platform unit/component suite: 148 tests passed
- [x] Production Vite build
- [x] Local Chromium + real Wrangler Worker against synthetic Account/API fixtures: persistent HttpOnly cookie, new-tab authentication, close-all-pages/reopen authentication, no JWT in Web Storage, cross-tab logout
- [x] Real Vite → Wrangler → synthetic Account/API smoke with an existing-style `.env.local` pointing `VITE_API_BASE_URL` at the old backend: cookie issuance, same-origin business calls with upstream Bearer, new-tab login, cross-tab logout, and no JWT in Web Storage
- [x] Worker regressions: business/expiry validation, CSRF, transient preservation, proxy header/idempotency contract, upstream cookie stripping
- [x] Independent code review; fixed and regression-tested the focus/OTP/Google-login race it found
- [x] `git diff --check`

No live business writes, deployment or release were performed. Staging integration with real Account/Firebase remains a deployment verification step.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `253ce6ab4f605ce91ef683d4c528b462e7305f90`
- PR: #3984
- 作者：david-srp
- 日期：2026-10-01T13:00:01Z

### Commit Message

```
fix(platform): persist login across tabs / 跨标签页保持登录 (#3984)

## Summary / 改动
Platform previously stored its account JWT only in sessionStorage.
Opening an independent tab or returning after closing the page required
another login even while the token remained valid.

- Persist a verified, Platform-only JWT in a host-only
HttpOnly/Secure/SameSite=Lax cookie, bounded by its signed expiry;
migrate existing tab credentials without discarding them on transient
failures.
- Add a same-origin Cloudflare Worker session BFF and `/platform/v1`
proxy. Preserve `ecap-platform` identity isolation and existing upstream
authorization/idempotency contracts; enforce same-origin mutations and
no-store responses.
- Synchronize login/logout across tabs, revalidate confirmed business
authentication errors without replaying writes, and preserve OTP/Google
login across focus changes.
- Always route development, preview and production API calls through the
page origin, ignoring legacy VITE_API_BASE_URL overrides. Wire Worker
upstream URLs from existing deployment variables and document local
development.

新标签页、关页重开可恢复登录；退出和切换账号同步其他标签页。业务 API 401
会重新验证账号，网络/权限故障不会误清会话，写操作不会自动重放。

## Root cause / 原因与边界
Session persistence was scoped to a browser tab, while business 401
responses had no identity recovery path. The existing
interrupted-restoration fix (#3979) is retained.

Account service main currently signs registered-user JWTs for 300 days
by default and has no general refresh-token endpoint. This PR respects
the actual signed expiry; it does not invent renewal, extend tokens,
share Work's cookie, change backend billing, or claim production
validation. Actual expiry still requires sign-in.

## Validation / 验证
- [x] Platform lint and TypeScript checks
- [x] Platform unit/component suite: 148 tests passed
- [x] Production Vite build
- [x] Local Chromium + real Wrangler Worker against synthetic
Account/API fixtures: persistent HttpOnly cookie, new-tab
authentication, close-all-pages/reopen authentication, no JWT in Web
Storage, cross-tab logout
- [x] Real Vite → Wrangler → synthetic Account/API smoke with an
existing-style `.env.local` pointing `VITE_API_BASE_URL` at the old
backend: cookie issuance, same-origin business calls with upstream
Bearer, new-tab login, cross-tab logout, and no JWT in Web Storage
- [x] Worker regressions: business/expiry validation, CSRF, transient
preservation, proxy header/idempotency contract, upstream cookie
stripping
- [x] Independent code review; fixed and regression-tested the
focus/OTP/Google-login race it found
- [x] `git diff --check`

No live business writes, deployment or release were performed. Staging
integration with real Account/Firebase remains a deployment verification
step.
```

来源：SerendipityOneInc/ecap-workspace @ 253ce6ab，PR #3984，作者 david-srp。
