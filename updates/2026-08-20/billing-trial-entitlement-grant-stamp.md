---
title: "修复：免费试用订单的额度发放状态显示正确"
type: "Bug Fix"
priority: "中"
date: "2026-08-20"
status: "待审核"
channels: ""
---

# 修复：免费试用订单的额度发放状态显示正确

## 核心宣传点

信用卡免费试用的额度实际已经发放，但订单接口没有记录发放时间戳，导致订单页显示成「未发放」，试用额度的重置扫描也可能算不准起始时间。现已在额度确认到账后正确打上时间戳，重复回放也不会重复记账。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e09663116f672a5cd53c16512b6c91f82b1335ec`
- PR: #3451
- 作者: tim-srp
- 日期: 2026-08-20T04:09:31Z

### Commit Message

```
fix(billing): stamp bg_granted_at on settled Airwallex trial entitlements (#3451)

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary

Airwallex trial settlement records the entitlement as `ACTIVE` with the
trial credits, but never stamps `bg_granted_at` — the timestamp that
other grant flows (first payment, renewal, subscription code) write
**after** billing-gateway confirms the credits landed.

Missing stamp breaks two consumers:
- Order API `entitlement_granted` flag — `orders.py` treats
`bg_granted_at` as the proof the grant landed, so trial orders look
never-granted.
- Credit-reset scans (`credit_reset_repo.py`) that key off
`bg_granted_at` to know when trial credits started.

## Root cause

`record_trial_entitlement` had no `bg_granted_at` parameter and
`settle_airwallex_trial_subscription` wrote the entitlement only once,
before the billing-gateway grant — unlike the paid-card first payment
flow which writes `ACTIVE + bg_granted_at` after the grant succeeds.

## Change

- `record_trial_entitlement` gains an optional `bg_granted_at` parameter
(same pattern as `record_payment_entitlement` /
`record_subscription_code_entitlement`).
- `settle_airwallex_trial_subscription` re-records the entitlement with
`bg_granted_at=now` after the billing-gateway grant succeeds, and skips
the re-stamp when a replay already carries the timestamp (idempotent).

## Test plan

- [x] `test_settles_trial_when_all_facts_match` — asserts the second
`record_trial_entitlement` call carries `bg_granted_at`.
- [x] `test_replayed_trial_preserves_existing_credits` — asserts the
backfill keeps the reused credits (`777`) and adds the stamp.
- [x] New `test_replayed_trial_skips_grant_stamp_when_already_set` — a
replay that already has `bg_granted_at` is not re-stamped.
- [x] `verify-py` (ruff + pyright + import-linter) passes;
pre-commit/pre-push hooks pass.

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary

Airwallex trial settlement records the entitlement as `ACTIVE` with the trial credits, but never stamps `bg_granted_at` — the timestamp that other grant flows (first payment, renewal, subscription code) write **after** billing-gateway confirms the credits landed.

Missing stamp breaks two consumers:
- Order API `entitlement_granted` flag — `orders.py` treats `bg_granted_at` as the proof the grant landed, so trial orders look never-granted.
- Credit-reset scans (`credit_reset_repo.py`) that key off `bg_granted_at` to know when trial credits started.

## Root cause

`record_trial_entitlement` had no `bg_granted_at` parameter and `settle_airwallex_trial_subscription` wrote the entitlement only once, before the billing-gateway grant — unlike the paid-card first payment flow which writes `ACTIVE + bg_granted_at` after the grant succeeds.

## Change

- `record_trial_entitlement` gains an optional `bg_granted_at` parameter (same pattern as `record_payment_entitlement` / `record_subscription_code_entitlement`).
- `settle_airwallex_trial_subscription` re-records the entitlement with `bg_granted_at=now` after the billing-gateway grant succeeds, and skips the re-stamp when a replay already carries the timestamp (idempotent).

## Test plan

- [x] `test_settles_trial_when_all_facts_match` — asserts the second `record_trial_entitlement` call carries `bg_granted_at`.
- [x] `test_replayed_trial_preserves_existing_credits` — asserts the backfill keeps the reused credits (`777`) and adds the stamp.
- [x] New `test_replayed_trial_skips_grant_stamp_when_already_set` — a replay that already has `bg_granted_at` is not re-stamped.
- [x] `verify-py` (ruff + pyright + import-linter) passes; pre-commit/pre-push hooks pass.


