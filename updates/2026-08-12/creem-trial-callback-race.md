---
title: "修复：信用卡支付成功后页面误报失败"
type: "Bug Fix"
priority: "高"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# 修复：信用卡支付成功后页面误报失败

## 核心宣传点

支付渠道回调偶尔比订单绑定更快到达，导致明明扣款成功、页面却提示失败；现在会主动向支付方核对真实状态，成功页等待时间也从 30 秒放宽到 60 秒。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `2fdb4b17ee10c70910b72f32de27e39d1601296d`
- PR: #3348

### Commit Message

```
fix(billing): recover Creem trial callback race (#3348)

## Summary
- Recover an unbound Creem checkout from the authoritative Checkout API
when a Trial subscription webhook arrives before `checkout.completed`
finishes binding the local order.
- Reuse the existing checkout identity validation, atomic binding, and
Trial entitlement projection; already-bound Trial orders keep the
original projection path.
- Persist Trial recovery mismatches as stable `ConflictError` failures
instead of leaving provider events stuck in a processing lease.
- Extend Card success-page polling from 30 seconds to a bounded 60
seconds. Explicit failed, canceled, refund, and manual-review states
still fail immediately.
- No Antom/Alipay, Catalog, renewal, past-due, or production-purchase
behavior is changed.

## Root cause
Creem emits `checkout.completed` and the Trial `subscription.paid` event
at nearly the same time. The webhook receiver processes them
independently, so the subscription event can validate the local order
before the checkout event has persisted its provider
subscription/customer binding. That event fails and succeeds only after
Creem retries roughly 38–44 seconds later, while the success page
previously stopped polling after 30 seconds and displayed a false
failure.

## Test plan
- [x] TDD regression: Trial subscription webhook recovers and projects a
completed but unbound Checkout without waiting for provider retry.
- [x] Bound Trial orders remain on the existing projection path and do
not create a Creem API client.
- [x] Pending/expired Checkout state is not acknowledged as recovered.
- [x] Identity, Checkout-state, and subscription mismatches are
recordable service errors.
- [x] Card success page remains processing before 60 seconds and times
out at the 60-second wall-clock deadline.
- [x] Backend targeted suite: 109 passed.
- [x] Frontend targeted suite: 35 passed; TypeScript and ESLint passed.
- [x] Ruff and changed-file Pyright: 0 errors.

## Local verification note
The repository-wide host Pyright run still reports seven unchanged
`r2_storage.py` boto client typing errors from `origin/main`; the four
changed Python files pass Pyright with 0 errors, and CI remains
authoritative for the complete environment.
```

### PR Body

## Summary
- Recover an unbound Creem checkout from the authoritative Checkout API when a Trial subscription webhook arrives before `checkout.completed` finishes binding the local order.
- Reuse the existing checkout identity validation, atomic binding, and Trial entitlement projection; already-bound Trial orders keep the original projection path.
- Persist Trial recovery mismatches as stable `ConflictError` failures instead of leaving provider events stuck in a processing lease.
- Extend Card success-page polling from 30 seconds to a bounded 60 seconds. Explicit failed, canceled, refund, and manual-review states still fail immediately.
- No Antom/Alipay, Catalog, renewal, past-due, or production-purchase behavior is changed.

## Root cause
Creem emits `checkout.completed` and the Trial `subscription.paid` event at nearly the same time. The webhook receiver processes them independently, so the subscription event can validate the local order before the checkout event has persisted its provider subscription/customer binding. That event fails and succeeds only after Creem retries roughly 38–44 seconds later, while the success page previously stopped polling after 30 seconds and displayed a false failure.

## Test plan
- [x] TDD regression: Trial subscription webhook recovers and projects a completed but unbound Checkout without waiting for provider retry.
- [x] Bound Trial orders remain on the existing projection path and do not create a Creem API client.
- [x] Pending/expired Checkout state is not acknowledged as recovered.
- [x] Identity, Checkout-state, and subscription mismatches are recordable service errors.
- [x] Card success page remains processing before 60 seconds and times out at the 60-second wall-clock deadline.
- [x] Backend targeted suite: 109 passed.
- [x] Frontend targeted suite: 35 passed; TypeScript and ESLint passed.
- [x] Ruff and changed-file Pyright: 0 errors.

## Local verification note
The repository-wide host Pyright run still reports seven unchanged `r2_storage.py` boto client typing errors from `origin/main`; the four changed Python files pass Pyright with 0 errors, and CI remains authoritative for the complete environment.


---
