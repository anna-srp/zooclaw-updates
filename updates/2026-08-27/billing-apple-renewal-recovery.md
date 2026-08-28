---
title: "修复：Apple 渠道续费扣款成功，但会员权益没有恢复"
type: "Bug Fix"
priority: "高"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 修复：Apple 渠道续费扣款成功，但会员权益没有恢复

## 核心宣传点

通过 Apple 渠道续费时，付款订单已经记为成功，权益却因为订阅状态无法从「已过期」切回「生效中」而没有发放；更糟的是这次失败没有被正确记录，Apple 的重试会被当成重复通知直接放行，于是你付了钱但一直没有权益。现在这种「支付方已确认、且新周期确实更晚」的情况允许恢复权益，异常也会被如实记录以便重试真正生效，并且不会被延迟到达的旧通知覆盖掉。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `63ac01c0a9850cb45d34a65fec2214635c319a5e`
- PR: #3524
- 作者: sharplee-srp
- 日期: 2026-08-27T02:41:57Z

### Commit Message

```
fix(billing): recover Apple paid renewals (#3524)

## Summary
- allow a provider-authenticated Apple paid period to reactivate an
expired agreement only when its period end is strictly newer
- persist unexpected Apple processing errors as failed provider events,
so retries are not permanently ACKed as duplicates
- preserve a recovered paid period when an older non-revocation Apple
loss notification arrives out of order

## Root cause
Apple renewal processing persisted the succeeded payment order before
updating the subscription agreement and granting the entitlement. A
billing-recovery notification then attempted `expired -> active`, which
the generic agreement state machine rejected. That exception is a
`ValueError`, while the Apple adapter only marked `ServiceError`
failures, so the provider event remained in `processing`. Duplicate
delivery treated `processing` as a completed duplicate and returned
success, leaving the succeeded order without an entitlement.

The reactivation exception is deliberately narrow: provider actor only,
same provider, `expired -> active`, current agreement, and a strictly
newer paid period. Other terminal transitions remain invalid.

Apple loss handling ignores only non-revocation facts whose period end
is strictly older than the current paid period. Eligible loss writes use
the agreement period snapshot as a compare-and-set guard so a concurrent
recovery cannot be overwritten; `REVOKE` remains authoritative.

## Operational note
- this prevents the state-transition exception from leaving new Apple
events stuck in `processing`
- existing orphan orders are not automatically replayed because stored
Apple payloads are redacted; repair should use verified Apple source
data in a separate controlled production operation
- no production data is changed by this PR

## Test plan
- [x] `pytest -q tests/unit/test_apple_billing_v2.py
tests/unit/test_billing_v2_subscription_agreements.py` — 63 passed
- [x] `pytest -q tests/unit -k 'billing_v2 or apple'` — 749 passed, 5
skipped
- [x] `bash scripts/verify-py.sh` — Ruff, format, Pyright, and
import-linter passed
- [x] all `scripts/ci-lint/*.sh` checks passed
```

### PR Description

```
## Summary
- allow a provider-authenticated Apple paid period to reactivate an expired agreement only when its period end is strictly newer
- persist unexpected Apple processing errors as failed provider events, so retries are not permanently ACKed as duplicates
- preserve a recovered paid period when an older non-revocation Apple loss notification arrives out of order

## Root cause
Apple renewal processing persisted the succeeded payment order before updating the subscription agreement and granting the entitlement. A billing-recovery notification then attempted `expired -> active`, which the generic agreement state machine rejected. That exception is a `ValueError`, while the Apple adapter only marked `ServiceError` failures, so the provider event remained in `processing`. Duplicate delivery treated `processing` as a completed duplicate and returned success, leaving the succeeded order without an entitlement.

The reactivation exception is deliberately narrow: provider actor only, same provider, `expired -> active`, current agreement, and a strictly newer paid period. Other terminal transitions remain invalid.

Apple loss handling ignores only non-revocation facts whose period end is strictly older than the current paid period. Eligible loss writes use the agreement period snapshot as a compare-and-set guard so a concurrent recovery cannot be overwritten; `REVOKE` remains authoritative.

## Operational note
- this prevents the state-transition exception from leaving new Apple events stuck in `processing`
- existing orphan orders are not automatically replayed because stored Apple payloads are redacted; repair should use verified Apple source data in a separate controlled production operation
- no production data is changed by this PR

## Test plan
- [x] `pytest -q tests/unit/test_apple_billing_v2.py tests/unit/test_billing_v2_subscription_agreements.py` — 63 passed
- [x] `pytest -q tests/unit -k 'billing_v2 or apple'` — 749 passed, 5 skipped
- [x] `bash scripts/verify-py.sh` — Ruff, format, Pyright, and import-linter passed
- [x] all `scripts/ci-lint/*.sh` checks passed

```

---
