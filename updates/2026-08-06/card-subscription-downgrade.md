---
title: "Card 订阅现在支持降级"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

使用 Card（Creem）支付的用户现在可以直接在订阅页发起降级，按当前周期结束时生效，不用再联系客服。

## 原始内容

**fix(billing): enable card subscription downgrades (#3278)**

- sha: `3448bd5362eb1dab919a2ef346b631be2287d745`
- PR: #3278

```
fix(billing): enable card subscription downgrades (#3278)

## Summary

- remove the temporary frontend block for active Card subscription
downgrades
- route Card downgrades through the existing provider-neutral
confirmation and scheduling flow
- preserve the existing Stripe, Antom, and Apple behavior

## Why

The Creem backend already supports same-cycle downgrade scheduling
through the existing subscription downgrade endpoint. The frontend still
returned an informational toast before opening the confirmation modal,
so the backend was never called.

## Validation

- TDD regression: confirmed the Card confirmation-flow test failed
before the source change
- `pnpm exec vitest run
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` — 73
passed
- billing unit suite — 205 passed
- `bash scripts/verify-web.sh
web/app/src/components/billing/hooks/useCheckoutFlow.ts
web/app/tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` —
passed
- pre-push changed-surface gate — passed

## Staging follow-up

After deploy, resume the currently canceling Test Mode subscription,
then schedule Ultra to Pro or Starter downgrade and verify the effective
period-end state.
```

**PR Body:**

## Summary

- remove the temporary frontend block for active Card subscription downgrades
- route Card downgrades through the existing provider-neutral confirmation and scheduling flow
- preserve the existing Stripe, Antom, and Apple behavior

## Why

The Creem backend already supports same-cycle downgrade scheduling through the existing subscription downgrade endpoint. The frontend still returned an informational toast before opening the confirmation modal, so the backend was never called.

## Validation

- TDD regression: confirmed the Card confirmation-flow test failed before the source change
- `pnpm exec vitest run tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` — 73 passed
- billing unit suite — 205 passed
- `bash scripts/verify-web.sh web/app/src/components/billing/hooks/useCheckoutFlow.ts web/app/tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` — passed
- pre-push changed-surface gate — passed

## Staging follow-up

After deploy, resume the currently canceling Test Mode subscription, then schedule Ultra to Pro or Starter downgrade and verify the effective period-end state.

