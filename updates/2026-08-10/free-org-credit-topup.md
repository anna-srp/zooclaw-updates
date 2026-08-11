---
title: "修复：未购企业套餐的团队无法充值 Credits"
type: "Bug Fix"
priority: "中"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 修复：未购企业套餐的团队无法充值 Credits

## 核心宣传点

免费团队组织此前因为没有企业套餐协议而无法创建/确认线下充值订单，现已放开，充值即可正常到账。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `275f746640619f3560738029e189ad5a5107c96c`
- PR: #3317

### Commit Message

```
fix(billing): allow free org credit topups (#3317)

## Summary
- allow team organizations without an Enterprise Package agreement to
create and confirm offline credit topups
- idempotently ensure the baseline Billing Gateway subscription before
granting team topup credits
- create and persist the team topup wallet when Billing Gateway has no
usable wallet, including a 404 credits response
- update the org-topup design contract and regression coverage

## Root cause

The org-topup lifecycle required an effective Enterprise Package
agreement at both order creation and confirmation. That policy blocked
free team organizations even though topup credits do not grant package
benefits or change model access. Personal-to-team upgrades could also
lack the Billing Gateway subscription and wallet required for
fulfillment.

## Test plan
- [x] `.venv/bin/pytest -q tests/unit/test_offline_topup_orders.py
tests/unit/test_billing_v2_fulfillment.py` — 37 passed
- [x] changed-file Pyright with the claw-interface venv — 0 errors
- [x] Ruff check and format — passed
- [x] import-linter — 8 contracts kept
- [x] dashboard-console Vitest — 71 files / 631 tests passed
- [x] dashboard-console ESLint and TypeScript build check — passed

The full local `verify-changed.sh` could not complete because the local
Pyright invocation did not resolve installed venv dependencies and
reported repository-wide missing imports. The same changed files pass
when Pyright is explicitly pointed at `.venv/bin/python`; CI remains
authoritative for the full backend gate.
```

### PR Body

## Summary
- allow team organizations without an Enterprise Package agreement to create and confirm offline credit topups
- idempotently ensure the baseline Billing Gateway subscription before granting team topup credits
- create and persist the team topup wallet when Billing Gateway has no usable wallet, including a 404 credits response
- update the org-topup design contract and regression coverage

## Root cause

The org-topup lifecycle required an effective Enterprise Package agreement at both order creation and confirmation. That policy blocked free team organizations even though topup credits do not grant package benefits or change model access. Personal-to-team upgrades could also lack the Billing Gateway subscription and wallet required for fulfillment.

## Test plan
- [x] `.venv/bin/pytest -q tests/unit/test_offline_topup_orders.py tests/unit/test_billing_v2_fulfillment.py` — 37 passed
- [x] changed-file Pyright with the claw-interface venv — 0 errors
- [x] Ruff check and format — passed
- [x] import-linter — 8 contracts kept
- [x] dashboard-console Vitest — 71 files / 631 tests passed
- [x] dashboard-console ESLint and TypeScript build check — passed

The full local `verify-changed.sh` could not complete because the local Pyright invocation did not resolve installed venv dependencies and reported repository-wide missing imports. The same changed files pass when Pyright is explicitly pointed at `.venv/bin/python`; CI remains authoritative for the full backend gate.

