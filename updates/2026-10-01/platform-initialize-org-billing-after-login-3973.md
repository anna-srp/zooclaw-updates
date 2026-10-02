---
title: "修复：登录后自动初始化组织钱包，创建 API Key 不必先去充值"
type: "Bug Fix"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：登录后自动初始化组织钱包，创建 API Key 不必先去充值

## 核心宣传点

开发者平台现在会在登录完成、完成鉴权引导之后，自动为尚未初始化的组织钱包调用已有的初始化接口。用户不需要先走一遍充值流程才能创建 API Key，新账号上手路径少了一步。

## 分级

- 内部：P2
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

Platform now initializes an uninitialized Organization wallet after authenticated bootstrap, using the existing `POST /platform/v1/billing/initialize`. Users can create API keys without first starting a top-up. Initialization runs alongside the shell: navigation, existing API keys, Projects, Account and payment history remain accessible during setup or a billing outage. Failures retain the login session, show the returned error inside the page, and offer explicit Retry. API key creation uses its existing permissions and does not depend on billing reads or initialization. Only top-ups wait for initialized billing; existing keys can still be revoked. Existing wallets are reused and their actual balance is displayed.

The change is entirely in `web/platform`. Only the Platform frontend needs deployment; there are no new environment variables. Agent creation, Engine forwarding, server authentication and consumption-time balance enforcement are unchanged from main. Setup creates no credits, payment order, Stripe Checkout or promotional reservation.

## Root cause

Wallet initialization currently happens when starting a top-up. A user who has only signed in can therefore receive `409 platform.billing_not_ready` from SDK Agent creation because the Organization has no billing association.

The frontend reads billing status and initializes only when it is explicitly `uninitialized` and the user has billing-management permission. It makes one automatic initialization POST per page session, including React StrictMode. A failed initialization POST requires explicit Retry: query refetches and network reconnects cannot retry it automatically.

Billing GET recovery is separate from retrying a failed initialization POST. While GET is failing, the frontend does not infer a missing wallet or initialize. GET may recover through manual Retry or automatic network-reconnect refetch. If it then explicitly returns `uninitialized` and no initialization POST has been attempted, the first automatic initialization is allowed. This recovery is intentional. Window-focus refetch is already disabled globally in `AppProviders`; `retryOnMount: false` only prevents route mounts from restarting a failed GET.

Members without billing permission neither read nor initialize billing. `failed` and `manual_review` states show explicit setup messages; neither is automatically retried, and manual review directs the user to support. The current backend actually returns only `uninitialized` or `ready` from GET, and success or HTTP errors from initialization; the extra state handling preserves the existing public schema.

## Test plan

- [x] Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (48 tests), and `pnpm build`.
- [x] StrictMode coverage for one automatic initialization, zero-balance display, explicit Retry after failure, existing-wallet reuse, and unchanged Checkout behavior.
- [x] Degraded-mode coverage for pending billing reads/setup, API key creation during billing failures (including failed reads before and after a ready wallet and navigation), existing key visibility/revocation availability, payment history and navigation after setup failure, billing-read recovery, members without billing permission, and failed/manual-review statuses.
- [x] Real focus/reconnect events through TanStack Query: focus does not refetch billing; reconnect permits the first initialization after GET recovery but never automatically retries a failed initialization POST.
- [x] Merged latest main, preserving the Organization Usage page and branding changes. Final diff contains only eight files under `web/platform`; no backend or dependency changes.
- [ ] Staging login and SDK consumption verification after frontend deployment.

Supersedes #3971 with a frontend-only change.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `27184baa732470236e4a86931e9360100cac31da`
- PR: #3973
- 作者：finn-srp
- 日期：2026-10-01T06:07:30Z

### Commit Message

```
fix(platform): initialize organization billing after login (#3973)

## Summary

Platform now initializes an uninitialized Organization wallet after
authenticated bootstrap, using the existing `POST
/platform/v1/billing/initialize`. Users can create API keys without
first starting a top-up. Initialization runs alongside the shell:
navigation, existing API keys, Projects, Account and payment history
remain accessible during setup or a billing outage. Failures retain the
login session, show the returned error inside the page, and offer
explicit Retry. API key creation uses its existing permissions and does
not depend on billing reads or initialization. Only top-ups wait for
initialized billing; existing keys can still be revoked. Existing
wallets are reused and their actual balance is displayed.

The change is entirely in `web/platform`. Only the Platform frontend
needs deployment; there are no new environment variables. Agent
creation, Engine forwarding, server authentication and consumption-time
balance enforcement are unchanged from main. Setup creates no credits,
payment order, Stripe Checkout or promotional reservation.

## Root cause

Wallet initialization currently happens when starting a top-up. A user
who has only signed in can therefore receive `409
platform.billing_not_ready` from SDK Agent creation because the
Organization has no billing association.

The frontend reads billing status and initializes only when it is
explicitly `uninitialized` and the user has billing-management
permission. It makes one automatic initialization POST per page session,
including React StrictMode. A failed initialization POST requires
explicit Retry: query refetches and network reconnects cannot retry it
automatically.

Billing GET recovery is separate from retrying a failed initialization
POST. While GET is failing, the frontend does not infer a missing wallet
or initialize. GET may recover through manual Retry or automatic
network-reconnect refetch. If it then explicitly returns `uninitialized`
and no initialization POST has been attempted, the first automatic
initialization is allowed. This recovery is intentional. Window-focus
refetch is already disabled globally in `AppProviders`; `retryOnMount:
false` only prevents route mounts from restarting a failed GET.

Members without billing permission neither read nor initialize billing.
`failed` and `manual_review` states show explicit setup messages;
neither is automatically retried, and manual review directs the user to
support. The current backend actually returns only `uninitialized` or
`ready` from GET, and success or HTTP errors from initialization; the
extra state handling preserves the existing public schema.

## Test plan

- [x] Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (48 tests),
and `pnpm build`.
- [x] StrictMode coverage for one automatic initialization, zero-balance
display, explicit Retry after failure, existing-wallet reuse, and
unchanged Checkout behavior.
- [x] Degraded-mode coverage for pending billing reads/setup, API key
creation during billing failures (including failed reads before and
after a ready wallet and navigation), existing key visibility/revocation
availability, payment history and navigation after setup failure,
billing-read recovery, members without billing permission, and
failed/manual-review statuses.
- [x] Real focus/reconnect events through TanStack Query: focus does not
refetch billing; reconnect permits the first initialization after GET
recovery but never automatically retries a failed initialization POST.
- [x] Merged latest main, preserving the Organization Usage page and
branding changes. Final diff contains only eight files under
`web/platform`; no backend or dependency changes.
- [ ] Staging login and SDK consumption verification after frontend
deployment.

Supersedes #3971 with a frontend-only change.
```

来源：SerendipityOneInc/ecap-workspace @ 27184baa，PR #3973，作者 finn-srp。
