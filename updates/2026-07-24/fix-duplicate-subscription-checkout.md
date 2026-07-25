---
title: "修复：同一套餐重复下单/重复扣款风险"
type: "Bug Fix"
priority: "中"
date: "2026-07-24"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了订阅结算的重复下单问题：同一套餐同一计费周期不再能重复下单，切换计费周期时会给出清晰的「取消并等待」提示，避免因并发或历史遗留订单导致的重复订阅与潜在重复扣款。

## 原始内容

**Commit**: `db00013199` — kaka-srp — 2026-07-24T11:36:45Z

### Commit Message

```
fix(billing): prevent duplicate subscription checkout (#3062)

## Summary

- reject duplicate personal subscriptions for the same plan and billing
cycle
- require canonical plan and billing-cycle fields for all subscription
orders
- revalidate pending orders immediately before Stripe or Antom provider
calls
- serialize concurrent personal subscription checkouts with an expiring
per-user lease
- show persistent cancel-and-wait instructions for billing-cycle
changes, including Apple and canceling states
- route effective subscribers away from the trial paywall checkout path

## Root cause

Subscription eligibility was checked only when a local order was
created. Legacy Stripe orders could omit the canonical plan or billing
cycle, and an older pending order could still reach a provider after
another subscription became effective. Concurrent pending orders also
had no atomic provider-stage guard.

The frontend handled billing-cycle changes with a short generic toast,
and the paywall maintained a separate checkout entry that could still
open payment UI before the backend rejected it.

## Test plan

- [x] backend targeted regression suite: 207 passed
- [x] frontend targeted regression suite: 115 passed
- [x] frontend TypeScript and ESLint
- [x] backend Ruff, Ruff format, Pyright, and import-linter
- [x] pre-push changed-surface verification
- [x] PR size budget

## Scope notes

- the checkout lease applies only to personal plan orders created
through the standard order flow
- Enterprise Package and ECAP Pack subscriptions retain their existing
ownership and concurrency guards
- Stripe Checkout expiry is aligned with the one-hour lease; Antom
subscription authorization already expires before the lease
```

### PR Body

## Summary

- reject duplicate personal subscriptions for the same plan and billing cycle
- require canonical plan and billing-cycle fields for all subscription orders
- revalidate pending orders immediately before Stripe or Antom provider calls
- serialize concurrent personal subscription checkouts with an expiring per-user lease
- show persistent cancel-and-wait instructions for billing-cycle changes, including Apple and canceling states
- route effective subscribers away from the trial paywall checkout path

## Root cause

Subscription eligibility was checked only when a local order was created. Legacy Stripe orders could omit the canonical plan or billing cycle, and an older pending order could still reach a provider after another subscription became effective. Concurrent pending orders also had no atomic provider-stage guard.

The frontend handled billing-cycle changes with a short generic toast, and the paywall maintained a separate checkout entry that could still open payment UI before the backend rejected it.

## Test plan

- [x] backend targeted regression suite: 207 passed
- [x] frontend targeted regression suite: 115 passed
- [x] frontend TypeScript and ESLint
- [x] backend Ruff, Ruff format, Pyright, and import-linter
- [x] pre-push changed-surface verification
- [x] PR size budget

## Scope notes

- the checkout lease applies only to personal plan orders created through the standard order flow
- Enterprise Package and ECAP Pack subscriptions retain their existing ownership and concurrency guards
- Stripe Checkout expiry is aligned with the one-hour lease; Antom subscription authorization already expires before the lease

