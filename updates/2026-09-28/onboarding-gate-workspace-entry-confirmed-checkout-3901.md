---
title: "修复：打开 Stripe 结账窗口不再直接算作完成引导，必须确认到订阅权益才放行进入工作区"
type: "Bug Fix"
priority: "高"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 修复：打开 Stripe 结账窗口不再直接算作完成引导，必须确认到订阅权益才放行进入工作区

## 核心宣传点

此前结账弹窗一打开，前端就把「引导已完成」写进了库并跳转到 Agents——也就是说没付钱也能进工作区。现在前端会等到从账号或订单接口拿到确凿的订阅凭证之后，才保存完成状态并跳转：新链路认「订单成功且权益已发放」，同时保留旧的付费周期计数和支付方订阅凭证，老客户不受影响。校验没过、未完成或拿不到结果时，受保护的工作区页面会保持在门禁态，支付成功页和邮箱验证页的确切路由照旧放行。刷新和重新登录都会重新校验，结账未完成时会持续轮询，保存完成状态之前还会再校验一次，历史上写过的完成标记和本地进度都无法绕过门禁。结账弹窗关掉之后仍然可以接着付，等待与重试的文案覆盖了全部 10 个语种。活跃的普通团队成员保持放行，团队管理员需要个人或团队订阅凭证。

## 分级

- 内部：P0
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
Opening Stripe Checkout no longer completes onboarding or grants workspace access. The frontend waits for positive subscription evidence from existing account or order APIs, then saves onboarding completion and navigates to `/agents`. New checkout uses successful subscription orders with granted entitlement; legacy paid-cycle and provider-subscription evidence preserves established customers.

- Gate protected workspace rendering while verification is pending, incomplete, or unavailable; preserve exact payment-success and email-verification routes.
- Recheck on refresh/login, poll while checkout is incomplete, and verify again immediately before saving completion. Old `onboarding_completed` values and local progress cannot bypass the gate.
- Keep the checkout resumable after its popup closes, with waiting/retry copy across all 10 locales.
- Preserve legacy paid subscriptions through `/account/me` paid-cycle counts or current provider-backed paid access, as well as successful Billing v2 order history. Preserve active ordinary team memberships (including older responses using `org.status`). Team admins need successful personal or team subscription evidence.

## Root cause
`useOnboardingCardCheckout` forwarded the checkout-window-opened callback directly to `completeOnboarding`. That persisted `onboarding_completed=true` and redirected to `/agents` before payment confirmation. The prior provider also rendered workspace children underneath onboarding and trusted the historical completion flag.

## Test plan
- [x] 260 targeted tests across 18 files passed (2026-09-28).
- [x] TypeScript, changed-file ESLint, frontend governance guards, and import boundaries passed (import check has existing repository warnings).
- [x] Chromium with local mock endpoints: close checkout without completing; refresh; fresh login session; direct workspace URL with old completed flag; verification failure and retry; confirmed subscription followed by `/agents` navigation and refresh. No browser page errors.
- [ ] Real Stripe payment and production registration/OTP; not exercised locally.

## Scope and limits
Frontend only: no backend, BFF, dependency, or lockfile changes. This is a website entry restriction, not backend API authorization. The current $30/month subscription checkout is unchanged; this does not introduce a standalone zero-cost card-binding flow. Accounts without positive paid/account-subscription or successful order evidence are blocked even if onboarding was previously marked complete.


## Review follow-up
- Fixed the legacy history gap: `/orders/list` only exposes Billing v2; existing server-owned account billing projections now cover established legacy subscribers. Added expired-legacy, current-provider, free-grant and unverified-trial regressions.
- Fixed older team response compatibility using the existing membership-scoped `org.status` fallback while respecting explicit suspended/pending/none statuses.
- Kept the single provider-owned polling loop; the suggested future route-rewiring hazard is not reachable in this layout and does not need additional pollers.
- Verified the final payment-channel review note against the existing backend contract: `UserMeResponse.from_account_and_org` normalizes historical `creem` to `card` (`services/claw-interface/app/schema/account_api.py:329`), with an existing regression in `test_billing_v2_user_public_response.py`. The public response permits `offline`, which the admission allowlist already accepts. No additional backend or admission change is required.
- Final checks for `cbf06fa64`: CI, frontend build/test/lint/typecheck, CodeQL and review gates passed; Codex review reports no remaining findings.



## Tim review follow-up (2026-09-28)

Fixed [Tim's P1](https://github.com/SerendipityOneInc/ecap-workspace/pull/3901#issuecomment-5862349573): effective legacy enterprise subscriptions can have `plan=free`, zero personal paid cycles and no Billing v2 payment orders. Active team admins now have an additional positive-evidence path through the existing `/users/credits/check` subscription projection. It requires enterprise-package kind and id, a supported payment provider, effective active/canceling/past_due status and an unexpired period. Credits/balance, billing readiness and admin role alone never admit the user. Existing account/order proofs and ordinary member behavior remain unchanged. No backend changes.

- Reproduced the missing scenario before implementation: regression suite had 5 failures; all pass after the fix.
- Added negative coverage for free/expired/manual-review/trial/missing evidence, unsupported providers, inactive memberships, request errors, and rechecking a changed subscription.
- Added integration tests connecting the actual Provider, Modal, admission query/service and completion logic, with API/presentation mocks: eligible legacy enterprise admin, unpaid admin retaining a usable checkout path, ordinary member, and subscription expiry before saving completion.
- 260 relevant tests across 18 files passed; TypeScript and ESLint passed. Final CI for `6f27b353a` is green (23 passing checks, none pending/failed). Both Claude and Codex re-reviews report APPROVE with no findings. Live enterprise accounts and real payment were not exercised.

### Cross-PR merge constraint
[Tim's #3902 comment](https://github.com/SerendipityOneInc/ecap-workspace/pull/3902) also identifies a separate composition issue: #3902 currently skips checkout for every active team admin. That branch must use verified admission to decide whether an admin may skip checkout, and retain payment for an unpaid admin, before both PRs ship. #3901 alone retains payment and tests it; this update does not silently change #3902 or claim its role-only skip condition is fixed. Preserve this invariant when resolving the two PRs' Modal conflict.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `fac443103c5f8a22822763e4b7b4bb640e97aad2`
- PR: #3901
- 作者：ericma-srp
- 日期：2026-09-28T03:48:02Z

### Commit Message

```
fix(onboarding): gate workspace entry on confirmed checkout (#3901)

## Summary
Opening Stripe Checkout no longer completes onboarding or grants
workspace access. The frontend waits for positive subscription evidence
from existing account or order APIs, then saves onboarding completion
and navigates to `/agents`. New checkout uses successful subscription
orders with granted entitlement; legacy paid-cycle and
provider-subscription evidence preserves established customers.

- Gate protected workspace rendering while verification is pending,
incomplete, or unavailable; preserve exact payment-success and
email-verification routes.
- Recheck on refresh/login, poll while checkout is incomplete, and
verify again immediately before saving completion. Old
`onboarding_completed` values and local progress cannot bypass the gate.
- Keep the checkout resumable after its popup closes, with waiting/retry
copy across all 10 locales.
- Preserve legacy paid subscriptions through `/account/me` paid-cycle
counts or current provider-backed paid access, as well as successful
Billing v2 order history. Preserve active ordinary team memberships
(including older responses using `org.status`). Team admins need
successful personal or team subscription evidence.

## Root cause
`useOnboardingCardCheckout` forwarded the checkout-window-opened
callback directly to `completeOnboarding`. That persisted
`onboarding_completed=true` and redirected to `/agents` before payment
confirmation. The prior provider also rendered workspace children
underneath onboarding and trusted the historical completion flag.

## Test plan
- [x] 260 targeted tests across 18 files passed (2026-09-28).
- [x] TypeScript, changed-file ESLint, frontend governance guards, and
import boundaries passed (import check has existing repository
warnings).
- [x] Chromium with local mock endpoints: close checkout without
completing; refresh; fresh login session; direct workspace URL with old
completed flag; verification failure and retry; confirmed subscription
followed by `/agents` navigation and refresh. No browser page errors.
- [ ] Real Stripe payment and production registration/OTP; not exercised
locally.

## Scope and limits
Frontend only: no backend, BFF, dependency, or lockfile changes. This is
a website entry restriction, not backend API authorization. The current
$30/month subscription checkout is unchanged; this does not introduce a
standalone zero-cost card-binding flow. Accounts without positive
paid/account-subscription or successful order evidence are blocked even
if onboarding was previously marked complete.


## Review follow-up
- Fixed the legacy history gap: `/orders/list` only exposes Billing v2;
existing server-owned account billing projections now cover established
legacy subscribers. Added expired-legacy, current-provider, free-grant
and unverified-trial regressions.
- Fixed older team response compatibility using the existing
membership-scoped `org.status` fallback while respecting explicit
suspended/pending/none statuses.
- Kept the single provider-owned polling loop; the suggested future
route-rewiring hazard is not reachable in this layout and does not need
additional pollers.
- Verified the final payment-channel review note against the existing
backend contract: `UserMeResponse.from_account_and_org` normalizes
historical `creem` to `card`
(`services/claw-interface/app/schema/account_api.py:329`), with an
existing regression in `test_billing_v2_user_public_response.py`. The
public response permits `offline`, which the admission allowlist already
accepts. No additional backend or admission change is required.
- Final checks for `cbf06fa64`: CI, frontend build/test/lint/typecheck,
CodeQL and review gates passed; Codex review reports no remaining
findings.



## Tim review follow-up (2026-09-28)

Fixed [Tim's
P1](https://github.com/SerendipityOneInc/ecap-workspace/pull/3901#issuecomment-5862349573):
effective legacy enterprise subscriptions can have `plan=free`, zero
personal paid cycles and no Billing v2 payment orders. Active team
admins now have an additional positive-evidence path through the
existing `/users/credits/check` subscription projection. It requires
enterprise-package kind and id, a supported payment provider, effective
active/canceling/past_due status and an unexpired period.
Credits/balance, billing readiness and admin role alone never admit the
user. Existing account/order proofs and ordinary member behavior remain
unchanged. No backend changes.

- Reproduced the missing scenario before implementation: regression
suite had 5 failures; all pass after the fix.
- Added negative coverage for free/expired/manual-review/trial/missing
evidence, unsupported providers, inactive memberships, request errors,
and rechecking a changed subscription.
- Added integration tests connecting the actual Provider, Modal,
admission query/service and completion logic, with API/presentation
mocks: eligible legacy enterprise admin, unpaid admin retaining a usable
checkout path, ordinary member, and subscription expiry before saving
completion.
- 260 relevant tests across 18 files passed; TypeScript and ESLint
passed. Final CI for `6f27b353a` is green (23 passing checks, none
pending/failed). Both Claude and Codex re-reviews report APPROVE with no
findings. Live enterprise accounts and real payment were not exercised.

### Cross-PR merge constraint
[Tim's #3902
comment](https://github.com/SerendipityOneInc/ecap-workspace/pull/3902)
also identifies a separate composition issue: #3902 currently skips
checkout for every active team admin. That branch must use verified
admission to decide whether an admin may skip checkout, and retain
payment for an unpaid admin, before both PRs ship. #3901 alone retains
payment and tests it; this update does not silently change #3902 or
claim its role-only skip condition is fixed. Preserve this invariant
when resolving the two PRs' Modal conflict.
```

来源：SerendipityOneInc/ecap-workspace @ fac44310，PR #3901，作者 ericma-srp。
