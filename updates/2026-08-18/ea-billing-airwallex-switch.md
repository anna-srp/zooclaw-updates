---
title: "信用卡订阅全面切换至 Airwallex 通道，升级套餐余额自动结转"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-18"
status: "待审核"
channels: ""
---

# 信用卡订阅全面切换至 Airwallex 通道，升级套餐余额自动结转

## 核心宣传点

所有信用卡订阅（新开通与升级）统一走 Airwallex 支付通道。升级套餐时不再走退款流程，原套餐剩余额度直接结转到新套餐，旧订阅在周期末自动取消，不会重复扣费或重复发放额度。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `7724ba1a45a60fa52787523410ca984026fabe57`
- PR: #3419
- 作者: tim-srp
- 日期: 2026-08-18T17:01:26Z

### Commit Message

```
feat(billing): unconditionally switch card subscription channel to Airwallex (#3419)

## Summary

Unconditionally switch the card subscription payment channel from Creem
to Airwallex (both new sign-ups and upgrades), per the design spec
`docs/superpowers/specs/2026-08-18-airwallex-subscription-unconditional-switch.md`.

### What changed

**1. Checkout — unconditional Airwallex**
- Removed the `AIRWALLEX_CHECKOUT_ENABLED` feature switch; new card
subscriptions always create an Airwallex checkout.
- Upgrades also go through Airwallex (`airwallex_upgrade_checkout.py`)
using the "new subscription replaces the superseded one" shape — no
refund, remaining credits carry over into the new subscription.
- Provider-parameterized replacement admission so the same admission
logic serves both Creem (legacy) and Airwallex.

**2. Paid replacement settlement**
(`app/services/airwallex/replacement.py`)
- `prepare_paid_checkout_replacement` — admit a paid checkout as a
replacement of a superseded subscription.
- `record_paid_checkout_agreement` / `commit_paid_checkout_replacement`
— atomic handoff: old agreement demoted (`current: False`,
`superseded_at`, `replacement_cleanup_required: True`), new agreement
promoted (`current: True`, `replaced_subscription_agreement_id`), plus
audit records.
- `cancel_replaced_subscription` — cancel the superseded subscription at
period end (Airwallex `proration_behavior=NONE`, scheduled cancel), with
read-back on failure.
- `retry_cleanup` — bounded retry used by the reconciliation sweep.

**3. First-payment settlement wiring** (`first_payment.py`)
- Detects replacement orders, settles the new agreement as non-current,
records the paid agreement, releases the checkout lease, then cancels
the superseded subscription.

**4. Renewal guard** (`renewal.py`)
- A superseded agreement (`current is not True` or
`replacement_cleanup_required is True`) never renews — prevents
duplicate credit grants.

**5. Reconciliation cleanup sweep** (`reconciliation.py`)
- `reconcile_current_airwallex_subscriptions` also lists superseded
Airwallex agreements needing cleanup and retries their cancellation.

**6. Repo compatibility** (`creem_replacement_cleanup_repo.py`,
`subscription_agreement_repo.py`)
- `commit_paid_replacement_handoff` and `list_candidates` are
provider-parameterized, defaulting to `creem` — the Creem path is
unchanged.

### Tests

- 134 unit tests pass across the affected suites:
`test_airwallex_first_payment`, `test_airwallex_reconciliation`,
`test_airwallex_renewal`,
`test_subscription_agreement_replacement_repo`, `test_billing_v2_repos`.
- New tests cover: upgrade settlement + superseded cancel,
reconciliation cleanup sweep, superseded renewal guard,
provider-parameterized replacement handoff,
`list_candidates(provider="airwallex")`.
- `ruff`, `ruff-format`, import-linter pass. Remaining pyright errors
are pre-existing boto3 stub noise in `r2_storage.py` (untouched by this
branch).

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

```
## Summary

Unconditionally switch the card subscription payment channel from Creem to Airwallex (both new sign-ups and upgrades), per the design spec `docs/superpowers/specs/2026-08-18-airwallex-subscription-unconditional-switch.md`.

### What changed

**1. Checkout — unconditional Airwallex**
- Removed the `AIRWALLEX_CHECKOUT_ENABLED` feature switch; new card subscriptions always create an Airwallex checkout.
- Upgrades also go through Airwallex (`airwallex_upgrade_checkout.py`) using the "new subscription replaces the superseded one" shape — no refund, remaining credits carry over into the new subscription.
- Provider-parameterized replacement admission so the same admission logic serves both Creem (legacy) and Airwallex.

**2. Paid replacement settlement** (`app/services/airwallex/replacement.py`)
- `prepare_paid_checkout_replacement` — admit a paid checkout as a replacement of a superseded subscription.
- `record_paid_checkout_agreement` / `commit_paid_checkout_replacement` — atomic handoff: old agreement demoted (`current: False`, `superseded_at`, `replacement_cleanup_required: True`), new agreement promoted (`current: True`, `replaced_subscription_agreement_id`), plus audit records.
- `cancel_replaced_subscription` — cancel the superseded subscription at period end (Airwallex `proration_behavior=NONE`, scheduled cancel), with read-back on failure.
- `retry_cleanup` — bounded retry used by the reconciliation sweep.

**3. First-payment settlement wiring** (`first_payment.py`)
- Detects replacement orders, settles the new agreement as non-current, records the paid agreement, releases the checkout lease, then cancels the superseded subscription.

**4. Renewal guard** (`renewal.py`)
- A superseded agreement (`current is not True` or `replacement_cleanup_required is True`) never renews — prevents duplicate credit grants.

**5. Reconciliation cleanup sweep** (`reconciliation.py`)
- `reconcile_current_airwallex_subscriptions` also lists superseded Airwallex agreements needing cleanup and retries their cancellation.

**6. Repo compatibility** (`creem_replacement_cleanup_repo.py`, `subscription_agreement_repo.py`)
- `commit_paid_replacement_handoff` and `list_candidates` are provider-parameterized, defaulting to `creem` — the Creem path is unchanged.

### Tests

- 134 unit tests pass across the affected suites: `test_airwallex_first_payment`, `test_airwallex_reconciliation`, `test_airwallex_renewal`, `test_subscription_agreement_replacement_repo`, `test_billing_v2_repos`.
- New tests cover: upgrade settlement + superseded cancel, reconciliation cleanup sweep, superseded renewal guard, provider-parameterized replacement handoff, `list_candidates(provider="airwallex")`.
- `ruff`, `ruff-format`, import-linter pass. Remaining pyright errors are pre-existing boto3 stub noise in `r2_storage.py` (untouched by this branch).

```
