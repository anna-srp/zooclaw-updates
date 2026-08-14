---
title: "信用卡充值加油包换新支付通道，付完立即到账"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-13"
status: "待审核"
channels: ""
---

## 核心宣传点

1,000 / 5,000 / 10,000 额度的信用卡加油包换用新的支付通道，价格和规则不变；付款成功后即使回调延迟，成功页也会主动核对并立刻发放额度。

## 原始内容

仓库：SerendipityOneInc/ecap-workspace
commit：39e04324d8136134434deaef51adc7e092b40ca3
作者：tim-srp
日期：2026-08-13T10:52:49Z

**Commit message**

```
feat(billing): migrate Card topups to Creem (#3365)

## Linear

N/A

## Summary

- Route the existing three Card add-on packs (1,000 / 5,000 / 10,000
credits) through Creem one-time products while preserving the current
order admission and pricing rules.
- Add server-owned Creem top-up catalog validation, idempotent Checkout
creation, signed webhook settlement, and one-time entitlement
fulfillment.
- Add success-page active Checkout confirmation so completed payments
can recover immediately when the webhook is delayed, while leaving
subscription Card and Antom flows unchanged.
- Document the scoped migration design and implementation plan.

## Test plan

- [x] Backend top-up, Card route, Creem fulfillment, and reconciliation
tests: 87 passed.
- [x] Frontend selected verification: TypeScript, ESLint, 359 passed / 1
skipped.
- [x] Ruff formatting/lint and import contracts passed.
- [x] Pre-commit Pyright passed in the configured hook environment.
- [ ] GitHub Actions run in the authoritative CI environment.

## Deployment configuration

- Configure `CREEM_PRODUCT_ID_TOPUP_1000`,
`CREEM_PRODUCT_ID_TOPUP_5000`, and `CREEM_PRODUCT_ID_TOPUP_10000` with
the corresponding environment's Creem one-time Product IDs before
enabling the flow.
- No hourly top-up reconciliation fallback is included in this PR;
recovery is webhook-first with success-page active confirmation.
```

**PR #3365 body**

## Linear

N/A

## Summary

- Route the existing three Card add-on packs (1,000 / 5,000 / 10,000 credits) through Creem one-time products while preserving the current order admission and pricing rules.
- Add server-owned Creem top-up catalog validation, idempotent Checkout creation, signed webhook settlement, and one-time entitlement fulfillment.
- Add success-page active Checkout confirmation so completed payments can recover immediately when the webhook is delayed, while leaving subscription Card and Antom flows unchanged.
- Document the scoped migration design and implementation plan.

## Test plan

- [x] Backend top-up, Card route, Creem fulfillment, and reconciliation tests: 87 passed.
- [x] Frontend selected verification: TypeScript, ESLint, 359 passed / 1 skipped.
- [x] Ruff formatting/lint and import contracts passed.
- [x] Pre-commit Pyright passed in the configured hook environment.
- [ ] GitHub Actions run in the authoritative CI environment.

## Deployment configuration

- Configure `CREEM_PRODUCT_ID_TOPUP_1000`, `CREEM_PRODUCT_ID_TOPUP_5000`, and `CREEM_PRODUCT_ID_TOPUP_10000` with the corresponding environment's Creem one-time Product IDs before enabling the flow.
- No hourly top-up reconciliation fallback is included in this PR; recovery is webhook-first with success-page active confirmation.


