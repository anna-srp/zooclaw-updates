---
title: "[平台] expire providerless v2 entitlements"
type: "Bug Fix"
priority: "中"
date: "2026-06-02"
status: "待审核"
channels: ""
---
# [平台] expire providerless v2 entitlements

## 核心宣传点
来自 ecap-workspace 仓库的更新：fix(billing): expire providerless v2 entitlements

## 原始内容
**Commit**: d74d617fa9fdb8cda8faa34bc0d267319ae65448
**Title**: fix(billing): expire providerless v2 entitlements (#2150)
**Author**: kaka-srp
**Date**: 2026-06-02T06:09:14Z

**PR**: #2150

### Commit Message
```
fix(billing): expire providerless v2 entitlements (#2150)

## Summary
- Add Billing v2 providerless subscription entitlement expiry for
trial/subscription-code/manual entitlements.
- Wire the job into existing Billing v2 subscription maintenance under
`/admin/cron/check-subscription-sync`.
- Add lease-based claiming, Billing Profile overlay for cleanup, and
tests for cleanup/retry/superseded-access behavior.

## Root cause
Provider-backed v2 subscriptions had period-end cleanup, but
providerless v2 entitlements only expired in read-time access
resolution. Pure v2 trial/code users could be blocked by access checks
after expiry while BG wallets, model/resource state, and OpenClaw bots
were not reclaimed by v2 cron.

## Rollout notes
- Requires the new `entitlement_due_providerless_expiry` index to be
created via the Billing v2 index script before/with production rollout.
- Controlled by `BILLING_V2_WRITES_ENABLED`; with writes disabled the
new job returns zero counts.

## Test plan
- [x] `ruff check app/database/entitlement_ledger_repo.py
app/services/billing_v2/expiry.py app/cron/billing_v2_subscription.py
tests/unit/test_billing_v2_expiry.py
tests/unit/test_billing_v2_subscription_cron.py
tests/unit/test_billing_v2_repos.py`
- [x] `pyright app/database/entitlement_ledger_repo.py
app/services/billing_v2/expiry.py app/cron/billing_v2_subscription.py
tests/unit/test_billing_v2_expiry.py
tests/unit/test_billing_v2_subscription_cron.py
tests/unit/test_billing_v2_repos.py`
- [x] `pytest tests/unit/test_billing_v2_expiry.py
tests/unit/test_billing_v2_subscription_cron.py
tests/unit/test_billing_v2_repos.py -q`
```

### PR Description
## Summary
- Add Billing v2 providerless subscription entitlement expiry for trial/subscription-code/manual entitlements.
- Wire the job into existing Billing v2 subscription maintenance under `/admin/cron/check-subscription-sync`.
- Add lease-based claiming, Billing Profile overlay for cleanup, and tests for cleanup/retry/superseded-access behavior.

## Root cause
Provider-backed v2 subscriptions had period-end cleanup, but providerless v2 entitlements only expired in read-time access resolution. Pure v2 trial/code users could be blocked by access checks after expiry while BG wallets, model/resource state, and OpenClaw bots were not reclaimed by v2 cron.

## Rollout notes
- Requires the new `entitlement_due_providerless_expiry` index to be created via the Billing v2 index script before/with production rollout.
- Controlled by `BILLING_V2_WRITES_ENABLED`; with writes disabled the new job returns zero counts.

## Test plan
- [x] `ruff check app/database/entitlement_ledger_repo.py app/services/billing_v2/expiry.py app/cron/billing_v2_subscription.py tests/unit/test_billing_v2_expiry.py tests/unit/test_billing_v2_subscription_cron.py tests/unit/test_billing_v2_repos.py`
- [x] `pyright app/database/entitlement_ledger_repo.py app/services/billing_v2/expiry.py app/cron/billing_v2_subscription.py tests/unit/test_billing_v2_expiry.py tests/unit/test_billing_v2_subscription_cron.py tests/unit/test_billing_v2_repos.py`
- [x] `pytest tests/unit/test_billing_v2_expiry.py tests/unit/test_billing_v2_subscription_cron.py tests/unit/test_billing_v2_repos.py -q`

