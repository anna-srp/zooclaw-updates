---
title: "修复：银行卡试用期显示剩余 300 多天，实际只有 7 天"
type: "Bug Fix"
priority: "中"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 修复：银行卡试用期显示剩余 300 多天，实际只有 7 天

## 核心宣传点

银行卡渠道的试用订阅里，「试用结束时间」和「当前计费周期结束时间」是两回事，之前一律按后者计算——年付 Starter 试用因此在界面上显示还剩约 372 天，而不是真实的 7 天，权益时长也可能被错误延长。现在试用期一律以真实的试用结束时间为准，界面、权益和下单记录三处保持一致，历史上被算长的记录也会在对账时安全修正。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f50c5e89c9c90e87dc64789e8d76ad8d481dbc2e`
- PR: #3541
- 作者: tim-srp
- 日期: 2026-08-27T02:43:20Z

### Commit Message

```
fix(billing): use card trial end for access (#3541)

## Summary

- use Airwallex `trial_ends_at` as the Billing v2 trial access boundary
- keep the provider `current_period_end` as the separate billing-period
fact
- align the trial agreement, entitlement, and checkout projection end
times
- safely shorten pre-fix succeeded checkout projections during replay

## Root cause

Airwallex trial events expose both a trial end and a subscription
billing-period end. The trial settlement projected `current_period_end`
into every trial boundary. For annual Starter trials this made the UI
calculate roughly 372 days remaining instead of 7 days and could also
extend the entitlement incorrectly.

Existing succeeded projections are reconciled only when the complete
order/subscription/agreement/entitlement identity matches and the stored
trial end is longer than the corrected end.

## Test plan

- `services/claw-interface/.venv/bin/pytest
tests/unit/test_card_checkout_projection_repo.py
tests/unit/test_airwallex_trial_lifecycle.py -q`
- `bash scripts/verify-py.sh`
- pre-push `bash scripts/verify-changed.sh`
```

### PR Description

```
## Summary

- use Airwallex `trial_ends_at` as the Billing v2 trial access boundary
- keep the provider `current_period_end` as the separate billing-period fact
- align the trial agreement, entitlement, and checkout projection end times
- safely shorten pre-fix succeeded checkout projections during replay

## Root cause

Airwallex trial events expose both a trial end and a subscription billing-period end. The trial settlement projected `current_period_end` into every trial boundary. For annual Starter trials this made the UI calculate roughly 372 days remaining instead of 7 days and could also extend the entitlement incorrectly.

Existing succeeded projections are reconciled only when the complete order/subscription/agreement/entitlement identity matches and the stored trial end is longer than the corrected end.

## Test plan

- `services/claw-interface/.venv/bin/pytest tests/unit/test_card_checkout_projection_repo.py tests/unit/test_airwallex_trial_lifecycle.py -q`
- `bash scripts/verify-py.sh`
- pre-push `bash scripts/verify-changed.sh`

```

---
