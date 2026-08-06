---
title: "新增 Card 银行卡支付通道（分阶段开放）"
type: "新功能上线"
priority: "高"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 新增 Card 银行卡支付通道（分阶段开放）

## 核心宣传点

订阅付费新增“Card”银行卡通道，支持同周期升级，取消与管理流程同样安全可用。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`461ab48d555e0fdfa838f2c57049e141a306cabf`
- 作者：tim-srp
- 日期：2026-08-05T16:23:01Z
- PR：#3265

### Commit Message

```
feat(billing): add staged Card checkout (#3265)
```

### PR Body

## Linear

N/A — this is the final frontend slice of the existing staged Creem Card rollout.

## Summary

- expose the new payment path to users only as `Card`; no Creem provider branding leaks into the UI
- in staging/development only, route a paid subscription to Billing v2 Card checkout when the authenticated backend capability is explicitly available
- support active, same-cycle Card upgrades through the already-merged `checkout_intent=upgrade` backend contract
- poll the local Billing v2 order after Card checkout and report success only after both a successful order status and `entitlement_granted=true`
- make Card subscription management provider-safe: generic cancellation, no Stripe portal/Edit billing/download leakage, and fail-closed unsupported Card downgrade or cycle/provider changes
- preserve the existing Stripe, Antom, Apple, trial, and top-up flows

## Rollout safety

- frontend Card routing is enabled only when `NEXT_PUBLIC_APP_ENV=staging` (or local development) and `/billing/card-checkout-capability` returns `card_available=true`
- production does not query the capability and cannot enter the new Card checkout branch through this change
- PR #3263 already provides the required backend upgrade contract
- merge PR #3264 before final staging validation so Creem yearly agreements participate in the existing annual credit-reset lifecycle and the rollout checklist is available

## Test plan

- [x] local `bash scripts/verify-web.sh` after rebase onto current `main`: governance guards, TypeScript, and ESLint passed; 603/603 Vitest files passed with 8272 passed, 67 skipped, and 1 todo
- [x] a102 devcontainer: governance guards, TypeScript, and ESLint passed
- [x] a102 Card-focused suite: 6/6 files and 182/182 tests passed
- [x] a102 full Vitest run: 602/603 files and 8271 tests passed; one unrelated existing `MarkdownContent` hydration test exceeded its 5-second timeout under full parallel load
- [x] reran that unrelated `MarkdownContent` file three times in isolation on a102: 48/48 passed on each run
- [x] independent specification and code-quality reviews approved after Card downgrade, refund-status display, and success-state conflict tests were added
- [x] push gate: PR size, changed-surface guards, TypeScript, and ESLint passed

## Deferred until staging deployment

Real Creem Test Mode browser E2E is intentionally performed after this PR and PR #3264 are merged and the automatic staging deployment finishes. The final staging pass covers new monthly/yearly subscription checkout, same-cycle upgrade, signed webhook fulfillment/idempotency, local order return polling, cancellation, annual credit state, and rollback gating.

