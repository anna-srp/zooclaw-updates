---
title: "修复：历史上取消过的 Stripe 授权不再挡住新订阅和结账"
type: "Bug Fix"
priority: "高"
date: "2026-09-23"
status: "待审核"
channels: ""
---

# 修复：历史上取消过的 Stripe 授权不再挡住新订阅和结账

## 核心宣传点

部分用户之前撤销过 Stripe 授权，这条历史记录会一直把他们判定为「不可订阅」，想重新付费也下不了单。现在历史已撤销的授权不再阻止新订阅。另外，支付渠道查询失败时不再抛出未处理异常，而是返回一个明确的 billing.migration_requires_review 提示并上报 Sentry，用户看到的是可理解的说明而不是报错页。结账创建带上了显式幂等键，资格校验改用 Stripe SDK 自带的重试机制，网络抖动时不会重复扣款或误判。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
Historical revoked Stripe agreements no longer block a new subscription. Provider lookup failures return a controlled `billing.migration_requires_review` response and are reported to Sentry, rather than producing an unhandled error.

Checkout creation with an explicit idempotency key and eligibility reads now use the Stripe SDK's built-in retry/backoff policy, with at most two retries. Requests retain the same parameters and idempotency key; validation errors are not blindly retried.

Handle `checkout.session.expired` to atomically cancel the exactly linked unpaid pending order (or a checkout-outcome-unknown review) with an audit record. Subscription checkout reservations are released only for that order. Repeated deliveries are safe, concurrent settlement and same-status session/review changes are protected by status and expected-field CAS, and paid/granted/unrelated-review orders are not canceled. Existing active-subscription and Team restrictions remain in place.

When creation succeeds at Stripe but its response is lost, the expiry handler can recover the order by metadata order ID and UID. Recovery requires the exact provider/environment, an uncertain checkout with a recorded request, and no existing Session ID. The transaction persists the Session ID together with cancellation and its audit, so delivery retries can finish lease release safely.

## Root cause
The eligibility gate queried revoked historical subscriptions, and Stripe lookup errors escaped the order/Checkout paths. Transient creation failures had no explicit SDK retry budget. Expired Checkout events were ignored, leaving local orders pending even though on-demand eligibility queries could recognize their expiration.

A missing resource in the current Stripe account is not proof that a historical payment failed. This PR does not automatically cancel missing-resource orders, introduce background reconciliation, or add a user cancellation UI.

## Test plan
- [x] 143 focused tests across Stripe SDK facade/retries, expiry handling, adapter dispatch, checkout recovery, billing policy, legacy eligibility, and catalog availability.
- [x] In-memory HTTP transport exercises the actual Stripe SDK retry loop: same body/key, two-retry limit, non-retryable validation failures, and GET retries.
- [x] Expiry regressions: subscription/top-up, repeated deliveries, owner/environment isolation, settled/granted/manual-review protection, settlement races, recovery after lease-release failure, and new-subscription eligibility after cancellation.
- [x] Ruff, formatting, Pyright, and import contracts.

## Rollout
Backend-only; no new environment variables. The audit transaction adds optional equality predicates for optimistic concurrency. CSFLE query-contract tests pass; the expanded predicate has not been exercised through staging’s encrypted client and requires validation before release. Ensure the relevant Stripe webhook endpoint subscribes to `checkout.session.expired` when deploying this change (documented in `docs/setup/stripe.md`). Live webhook configuration and end-to-end delivery have not been changed/tested in this PR.



## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `53dde279e8c5440d1a853e6002a3f7f86549cbb9`
- PR: #3873
- 作者：sam-srp
- 日期：2026-09-23T04:01:13Z

### Commit Message

```
fix(billing): recover Stripe checkout and subscription eligibility (#3873)

## Summary
Historical revoked Stripe agreements no longer block a new subscription.
Provider lookup failures return a controlled
`billing.migration_requires_review` response and are reported to Sentry,
rather than producing an unhandled error.

Checkout creation with an explicit idempotency key and eligibility reads
now use the Stripe SDK's built-in retry/backoff policy, with at most two
retries. Requests retain the same parameters and idempotency key;
validation errors are not blindly retried.

Handle `checkout.session.expired` to atomically cancel the exactly
linked unpaid pending order (or a checkout-outcome-unknown review) with
an audit record. Subscription checkout reservations are released only
for that order. Repeated deliveries are safe, concurrent settlement and
same-status session/review changes are protected by status and
expected-field CAS, and paid/granted/unrelated-review orders are not
canceled. Existing active-subscription and Team restrictions remain in
place.

When creation succeeds at Stripe but its response is lost, the expiry
handler can recover the order by metadata order ID and UID. Recovery
requires the exact provider/environment, an uncertain checkout with a
recorded request, and no existing Session ID. The transaction persists
the Session ID together with cancellation and its audit, so delivery
retries can finish lease release safely.

## Root cause
The eligibility gate queried revoked historical subscriptions, and
Stripe lookup errors escaped the order/Checkout paths. Transient
creation failures had no explicit SDK retry budget. Expired Checkout
events were ignored, leaving local orders pending even though on-demand
eligibility queries could recognize their expiration.

A missing resource in the current Stripe account is not proof that a
historical payment failed. This PR does not automatically cancel
missing-resource orders, introduce background reconciliation, or add a
user cancellation UI.

## Test plan
- [x] 143 focused tests across Stripe SDK facade/retries, expiry
handling, adapter dispatch, checkout recovery, billing policy, legacy
eligibility, and catalog availability.
- [x] In-memory HTTP transport exercises the actual Stripe SDK retry
loop: same body/key, two-retry limit, non-retryable validation failures,
and GET retries.
- [x] Expiry regressions: subscription/top-up, repeated deliveries,
owner/environment isolation, settled/granted/manual-review protection,
settlement races, recovery after lease-release failure, and
new-subscription eligibility after cancellation.
- [x] Ruff, formatting, Pyright, and import contracts.

## Rollout
Backend-only; no new environment variables. The audit transaction adds
optional equality predicates for optimistic concurrency. CSFLE
query-contract tests pass; the expanded predicate has not been exercised
through staging’s encrypted client and requires validation before
release. Ensure the relevant Stripe webhook endpoint subscribes to
`checkout.session.expired` when deploying this change (documented in
`docs/setup/stripe.md`). Live webhook configuration and end-to-end
delivery have not been changed/tested in this PR.
```

来源：SerendipityOneInc/ecap-workspace @ 53dde279，PR #3873，作者 sam-srp。