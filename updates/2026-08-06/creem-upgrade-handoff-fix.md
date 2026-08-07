---
title: "修复 Card 订阅升级付款成功但套餐未切换的问题"
type: "Bug Fix"
priority: "高"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

部分用户升级付款成功、额度已到账，但订阅未完成切换；现已修复，同时订阅周期会默认跟随你当前的计费周期而不是强制年付。

## 原始内容

**fix(billing): recover Creem upgrade handoff (#3267)**

- sha: `2b6d0aea2108c03a4ebcbc611b8c54bf99a7d0db`
- PR: #3267

```
fix(billing): recover Creem upgrade handoff (#3267)
```

**PR Body:**

## Summary

- recover Creem same-cycle upgrade handoff when the existing Billing v2 Agreement omits the default `cancel_at_period_end` field
- default an active Card subscription to its asynchronously loaded current billing cycle until the user explicitly selects another cycle
- preserve the existing yearly default for new subscriptions, Stripe, and Antom, and preserve cross-cycle fail-closed behavior
- record the real staging Test Mode upgrade result and the exact post-deploy replay check

## Root cause

The real staging Test Mode payment succeeded and created the Ultra order, 40,000-credit entitlement, and new Agreement. The atomic replacement handoff then failed with `billing.creem.replacement_current_changed`.

The existing Pro Agreement is a valid sparse Billing v2 document without a stored `cancel_at_period_end` field. Upgrade admission already treats missing/null/false as not canceled, but the handoff CAS converted a missing field to literal `false` and required that literal field in Mongo. The query therefore matched no document.

The first UI correction also exposed a separate loading edge: `useBillingCredits` starts empty and resolves asynchronously. A one-time state initializer still left a monthly Card subscriber on the yearly default. The final implementation derives the Card cycle from loaded subscription state until the user makes an explicit selection.

## Scope

- Creem replacement handoff only on the backend
- Card subscription cycle selection only on the frontend
- no Stripe, Antom, product catalog, API contract, schema, or database migration changes

## Test plan

- [x] TDD: backend regression failed on literal `false`, then passed with the non-true CAS condition
- [x] TDD: frontend regression failed across empty-to-loaded billing context, then passed with derived Card cycle state
- [x] replacement-focused backend unit tests: 55 passed
- [x] all Creem/Card backend unit tests: 555 passed
- [x] SubscriptionPanel tests: 73 passed
- [x] frontend selected verification: TypeScript, Vitest, ESLint passed
- [x] backend verification: Ruff check/format, Pyright, import-linter passed
- [x] changed-surface pre-push gate passed
- [x] independent code review found no remaining blocker or non-blocking issue

## Staging evidence and follow-up

On staging revision `461ab48d5`, Creem Test Mode accepted the Pro Monthly to Ultra Monthly payment. The local order reached `succeeded`, the deterministic Ultra entitlement reached `active`, and 40,000 credits were granted once. The new Agreement remained `current=false` while the old Pro Agreement remained current because the handoff CAS failed.

After this fix is deployed to staging, replay the original signed `subscription.paid` event through Creem automatic retry or dashboard resend. Verify that the new Ultra Agreement becomes current, the old Pro subscription is scheduled for cancellation, the order projection is attached, and no duplicate credit grant occurs. Do not create another checkout for the partially settled payment.

