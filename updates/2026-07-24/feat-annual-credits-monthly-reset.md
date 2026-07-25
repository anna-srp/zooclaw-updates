---
title: "年度订阅积分：按自然月定期重置"
type: "产品基础功能更新"
priority: "中"
date: "2026-07-24"
status: "待审核"
channels: ""
---

## 核心宣传点

年度订阅（及线下多月订阅）的额度现在会按自然月边界定期重置，每月发放当月配额，重置逻辑更规范、更符合预期，避免额度发放的歧义。

## 原始内容

**Commit**: `705b3bb23c` — kaka-srp — 2026-07-24T02:42:10Z

### Commit Message

```
feat(billing): reset annual credits by calendar month (#3055)

## Linear


https://linear.app/srpone/issue/ECA-1312/implement-calendar-month-credit-resets-for-annual-orders

## Summary

- Reset online annual and offline multi-month subscription credits on
anchored calendar-month boundaries.
- Grant only the monthly quota when confirming offline annual orders,
with strict source, lifecycle, and partial-state validation.
- Keep team resets non-bootstrapping and bound Billing Gateway mutation
retries to its 24-hour idempotency window.
- Isolate payment entitlements from reset entitlements and scope reset
history to the current contract period.
- Guard the complete reset-source fingerprint before and after BG, with
lease-owner CAS for source refresh and mutation markers.
- Document the completed production audit in the full design
specification; the one-time audit/cleanup script is intentionally not
included.

## Rollout evidence

- Production audit found 393 successful historical `yearly_credit_reset`
rows.
- Finalizable legacy rows: 0.
- Ambiguous legacy rows: 0.
- Production database rows changed by cleanup: 0.
- One current offline annual order was inventoried; its corrected
monthly order quota is preserved while the original historical payment
entitlement remains flagged for review.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] 276 targeted Billing v2 unit tests covering calendar boundaries,
renewal isolation, source validation, stale-source recovery, lease
ownership, BG retry bounds, team no-bootstrap behavior, and offline
order lifecycle.
- [x] Independent data-accuracy and idempotency agent reviews after
remediation.
- [x] Pre-commit and pre-push repository gates.
```

### PR Body

## Linear

https://linear.app/srpone/issue/ECA-1312/implement-calendar-month-credit-resets-for-annual-orders

## Summary

- Reset online annual and offline multi-month subscription credits on anchored calendar-month boundaries.
- Grant only the monthly quota when confirming offline annual orders, with strict source, lifecycle, and partial-state validation.
- Keep team resets non-bootstrapping and bound Billing Gateway mutation retries to its 24-hour idempotency window.
- Isolate payment entitlements from reset entitlements and scope reset history to the current contract period.
- Guard the complete reset-source fingerprint before and after BG, with lease-owner CAS for source refresh and mutation markers.
- Document the completed production audit in the full design specification; the one-time audit/cleanup script is intentionally not included.

## Rollout evidence

- Production audit found 393 successful historical `yearly_credit_reset` rows.
- Finalizable legacy rows: 0.
- Ambiguous legacy rows: 0.
- Production database rows changed by cleanup: 0.
- One current offline annual order was inventoried; its corrected monthly order quota is preserved while the original historical payment entitlement remains flagged for review.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] 276 targeted Billing v2 unit tests covering calendar boundaries, renewal isolation, source validation, stale-source recovery, lease ownership, BG retry bounds, team no-bootstrap behavior, and offline order lifecycle.
- [x] Independent data-accuracy and idempotency agent reviews after remediation.
- [x] Pre-commit and pre-push repository gates.

