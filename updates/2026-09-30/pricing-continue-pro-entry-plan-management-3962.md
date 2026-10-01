---
title: "定价页 Pro 按钮点了直接进套餐管理：登录后不再被甩回定价页"
type: "Improvement"
priority: "高"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 定价页 Pro 按钮点了直接进套餐管理：登录后不再被甩回定价页

## 核心宣传点

定价页上的 Pro 按钮原先会强行弹登录，而且登录完人还留在定价页，等于白点一次。现在两个入口都会复用已验证的会话，或者在登录（含 OAuth 跳转）完成后继续前往套餐管理。未登录用户登录后直接进入原有的套餐弹窗；已登录的非 Pro 用户和已过期用户跳过登录，走原有的 Get started / Resubscribe 流程；已是 Pro 的用户看到 Manage Subscription，进入原有的订阅与支付管理流程。弹窗关闭前页面会停在订阅路径上，避免首次订阅的用户下面突然冒出工作区引导，关闭后的落地页保持原样。定价页到套餐的埋点链路也修回来了，取消登录时会清掉。纯前端行为改动，后端接口、价格、权益、商品目录限制、Stripe 处理和计费状态规则一律没动；点开入口不会产生订单，结账仍然需要在原有弹窗里确认。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

Pricing's Pro buttons currently force a login prompt and leave users on
the pricing page after authentication. Both entry points now reuse a
verified session, or continue to Manage plan after login, including
OAuth redirects.

- Signed-out users log in, then continue to the existing plan dialog.
Signed-in non-Pro and expired users skip login and use the existing Get
started / Resubscribe flow.
- Existing Pro subscribers see Manage Subscription and enter the
existing subscription and payment-management flow.
- Keep the dialog on `/subscription` until it closes, preventing
workspace onboarding from opening underneath it for first-time
subscribers. Preserve the existing landing destination on close.
- Restore the pricing-to-plan analytics handoff and clear it when login
is canceled.

This is a frontend-only behavior change, plus tests and tracking
documentation. It does not change backend APIs, prices, entitlements,
catalog restrictions, Stripe handling, or billing state rules. Opening
the entry does not create an order; checkout still requires confirmation
in the existing dialog. The local scenario hub and mock billing pages
are excluded from this PR.

## Validation

Latest commit: `4aadf7f6d`. All applicable CI checks passed; CodeQL and
both automated reviews report no blocking findings. The full web suite
passed: 877 files, 11,013 tests passed, 70 skipped, 1 todo.

- 126 targeted unit tests passed across pricing, authentication
continuation, subscription entry, existing plan actions, translations,
and tracking.
- The existing specialist-return regression tests now assert that
navigation happens on dialog close, preserving both `?sp=` and the plain
`/chat` fallback.
- TypeScript, ESLint, and frontend governance guards passed.
- Seven browser scenarios passed with the real frontend and mocked
authentication/billing responses: signed out, free, active Pro, expired,
sign-in to an existing Pro account, payment failure, and Chinese active
Pro.
- All seven scenarios produced zero order/checkout requests before
confirmation. Get started / Resubscribe used the existing order and
checkout endpoints; Update payment method used the existing
customer-portal endpoint.
- Real Google/phone authentication and real Stripe payment were not
exercised; browser evidence is local simulation, not production payment
verification.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `41ecb2799ceaffa3c3db6a29fcdc2c3c539c3b47`
- PR: #3962
- 作者：ericma-srp
- 日期：2026-09-30T17:30:48Z

### Commit Message

```
fix(pricing): continue Pro entry to plan management (#3962)

## Summary

Pricing's Pro buttons currently force a login prompt and leave users on
the pricing page after authentication. Both entry points now reuse a
verified session, or continue to Manage plan after login, including
OAuth redirects.

- Signed-out users log in, then continue to the existing plan dialog.
Signed-in non-Pro and expired users skip login and use the existing Get
started / Resubscribe flow.
- Existing Pro subscribers see Manage Subscription and enter the
existing subscription and payment-management flow.
- Keep the dialog on `/subscription` until it closes, preventing
workspace onboarding from opening underneath it for first-time
subscribers. Preserve the existing landing destination on close.
- Restore the pricing-to-plan analytics handoff and clear it when login
is canceled.

This is a frontend-only behavior change, plus tests and tracking
documentation. It does not change backend APIs, prices, entitlements,
catalog restrictions, Stripe handling, or billing state rules. Opening
the entry does not create an order; checkout still requires confirmation
in the existing dialog. The local scenario hub and mock billing pages
are excluded from this PR.

## Validation

Latest commit: `4aadf7f6d`. All applicable CI checks passed; CodeQL and
both automated reviews report no blocking findings. The full web suite
passed: 877 files, 11,013 tests passed, 70 skipped, 1 todo.

- 126 targeted unit tests passed across pricing, authentication
continuation, subscription entry, existing plan actions, translations,
and tracking.
- The existing specialist-return regression tests now assert that
navigation happens on dialog close, preserving both `?sp=` and the plain
`/chat` fallback.
- TypeScript, ESLint, and frontend governance guards passed.
- Seven browser scenarios passed with the real frontend and mocked
authentication/billing responses: signed out, free, active Pro, expired,
sign-in to an existing Pro account, payment failure, and Chinese active
Pro.
- All seven scenarios produced zero order/checkout requests before
confirmation. Get started / Resubscribe used the existing order and
checkout endpoints; Update payment method used the existing
customer-portal endpoint.
- Real Google/phone authentication and real Stripe payment were not
exercised; browser evidence is local simulation, not production payment
verification.
```

来源：SerendipityOneInc/ecap-workspace @ 41ecb279，PR #3962，作者 ericma-srp。
