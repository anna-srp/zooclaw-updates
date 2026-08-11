---
title: "修复：信用卡免费试用开通后未到账 Starter 额度"
type: "Bug Fix"
priority: "高"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 修复：信用卡免费试用开通后未到账 Starter 额度

## 核心宣传点

部分用户开通免费试用后订单一直挂着、Starter 权益没有发放，现已修复并可自动补发。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `65f33fe3f400bfb6aae9e7ca5567676efff777de`
- PR: #3325

### Commit Message

```
fix(billing): handle Creem trial paid events (#3325)
```

### PR Body

## Summary
- Route Creem `subscription.paid` events whose subscription is still `trialing` through the existing fail-closed trial projection.
- Preserve the strict transaction and amount validation for normal `active` first payments.
- Cover both Creem event shapes accepted by the trial projection.

## Root cause
Creem starts a provider-managed free trial by sending `subscription.paid` with subscription status `trialing`. It does not send the expected `subscription.trialing` event in this checkout flow. The dispatcher therefore sent the event to normal first-payment settlement, which correctly rejected the zero-paid trial invoice and left the local order pending without Starter credits.

## Test plan
- [x] RED: new dispatcher regression test failed against the old routing.
- [x] `python -m pytest tests/unit/test_creem_first_payment.py tests/unit/test_creem_trial_lifecycle.py -q` (44 passed)
- [x] `python -m pytest tests/unit/test_creem*.py -q` (542 passed)
- [x] Ruff check and format for changed files
- [x] Pyright for changed files with the active Python interpreter (0 errors)
- [x] Pre-commit backend hooks, including repository Pyright and import contracts

## Staging evidence
- Creem subscription was created as `trialing` with a seven-day period and a zero-paid trial invoice.
- The signed `subscription.paid` webhook was recorded as failed with `billing.creem.first_payment_conflict`.
- Checkout binding completed, but the payment order remained pending and no Starter entitlement was granted.

## Recovery
After deployment, Creem webhook retry or the existing bound-trial reconciliation job can project affected pending trial orders idempotently.

