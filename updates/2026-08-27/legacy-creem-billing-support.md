---
title: "修复：历史 Creem 渠道订阅在账单页点取消/管理会走错流程"
type: "Bug Fix"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 修复：历史 Creem 渠道订阅在账单页点取消/管理会走错流程

## 核心宣传点

线上仍有一批通过已下线的 Creem 渠道购买的订阅。网页端不认识这个渠道值，于是把它们当作另一家支付服务商来处理，点「取消订阅」「管理支付方式」都会走到错误的流程上。现在这类历史订阅会被明确识别为「不支持自助管理」，隐藏套餐变更、取消和支付方式入口，只保留联系账单支持的入口；当前在用的银行卡订阅管理不受任何影响。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5e485f139c25b27b3f04152aba0deb60bab5c5d1`
- PR: #3546
- 作者: tim-srp
- 日期: 2026-08-27T10:05:28Z

### Commit Message

```
fix(web): route legacy Creem billing to support (#3546)

## Summary

- recognize persisted legacy `creem` subscriptions as a non-self-service
billing channel
- hide plan changes, cancellation, Stripe portal, and payment-method
actions for those subscriptions
- keep the existing billing-support entry point visible and fail closed
before any provider request if a legacy cancellation is invoked
indirectly
- leave current Airwallex `card` subscription management unchanged

## Root cause

PR #3485 removed the Creem runtime based on the assumption that
production had no real Creem users or orders. Production still contains
active legacy agreements with `provider=creem`. The web client did not
recognize that runtime value and fell through to Stripe cancellation and
portal behavior.

Creem API configuration and lifecycle services have already been
removed, so these subscriptions cannot be canceled safely through the
current provider-neutral Card endpoint. This PR deliberately routes
affected users to billing support instead of restoring the retired
provider integration or performing a local-only cancellation.

## Test plan

- [x] TDD RED confirmed legacy Creem users saw Cancel and Stripe Payment
Method actions
- [x] TDD RED confirmed the billing service attempted a provider request
for Creem cancellation
- [x] targeted regression suite — 139 passed
- [x] `bash scripts/verify-web.sh ...` — TypeScript, 401 tests (1
skipped), ESLint passed
- [x] pre-commit frontend and backend quality hooks
```

### PR Description

```
## Summary

- recognize persisted legacy `creem` subscriptions as a non-self-service billing channel
- hide plan changes, cancellation, Stripe portal, and payment-method actions for those subscriptions
- keep the existing billing-support entry point visible and fail closed before any provider request if a legacy cancellation is invoked indirectly
- leave current Airwallex `card` subscription management unchanged

## Root cause

PR #3485 removed the Creem runtime based on the assumption that production had no real Creem users or orders. Production still contains active legacy agreements with `provider=creem`. The web client did not recognize that runtime value and fell through to Stripe cancellation and portal behavior.

Creem API configuration and lifecycle services have already been removed, so these subscriptions cannot be canceled safely through the current provider-neutral Card endpoint. This PR deliberately routes affected users to billing support instead of restoring the retired provider integration or performing a local-only cancellation.

## Test plan

- [x] TDD RED confirmed legacy Creem users saw Cancel and Stripe Payment Method actions
- [x] TDD RED confirmed the billing service attempted a provider request for Creem cancellation
- [x] targeted regression suite — 139 passed
- [x] `bash scripts/verify-web.sh ...` — TypeScript, 401 tests (1 skipped), ESLint passed
- [x] pre-commit frontend and backend quality hooks

```

---
