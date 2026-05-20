---
title: "订阅状态修复：解决部分用户订阅数据不一致问题"
type: "Bug Fix"
priority: "高"
date: "2026-05-19"
status: "待审核"
channels: ""
---
# 订阅状态修复：解决部分用户订阅数据不一致问题

## 核心宣传点
修复了部分用户订阅计划与实际付款记录不匹配的问题，确保订阅状态准确无误，避免被误扣费或无法正常使用。

## 原始内容
```
commit: fff5a50b468d287b1ce1e8e4defc4dda35e0c06f
repo: SerendipityOneInc/ecap-workspace
author: kaka-srp
date: 2026-05-19T09:26:43Z

fix(subscription): complete ECA-681 reconciliation phase 2.5 (#1732)

## Summary

- Extend Stripe/Mongo reconciliation for Phase 2.5 drift classes:
plan/billing/product drift, legacy monthly product mapping,
unknown-product detection, mixed-provider Stripe residue, and
plan-correction resource sync.
- Add BG active-subscription detection for yearly cron renewals so
missing BG subscriptions are recreated without `ending_at` before wallet
refill, while healthy active BG subscriptions are left untouched.
- Add Apple production subscription-status fallback to Sandbox and
update cron/runbook docs with the current production scheduler gaps: BG
reconcile flow missing, stale `check-grace-expiry` hourly node, and
orphan monitor cadence mismatch.

## Verification

- `/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_subscriptions.py
tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py
tests/unit/test_subscription_manager.py
tests/unit/test_process_cron_renewal.py` — 124 passed
- `/home/node/.venvs/claw-interface/bin/ruff format --check app
tests/unit/test_billing_subscriptions.py
tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py
tests/unit/test_subscription_manager.py
tests/unit/test_process_cron_renewal.py`
- `/home/node/.venvs/claw-interface/bin/ruff check app
tests/unit/test_billing_subscriptions.py
tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py
tests/unit/test_subscription_manager.py
tests/unit/test_process_cron_renewal.py`
- `/home/node/.venvs/claw-interface/bin/pyright --pythonpath
/home/node/.venvs/claw-interface/bin/python app tests/`
- `git diff --check origin/main...HEAD`

Linear: ECA-681

--- PR #1732 Body ---
## Summary

- Extend Stripe/Mongo reconciliation for Phase 2.5 drift classes: plan/billing/product drift, legacy monthly product mapping, unknown-product detection, mixed-provider Stripe residue, and plan-correction resource sync.
- Add BG active-subscription detection for yearly cron renewals so missing BG subscriptions are recreated without `ending_at` before wallet refill, while healthy active BG subscriptions are left untouched.
- Add Apple production subscription-status fallback to Sandbox and update cron/runbook docs with the current production scheduler gaps: BG reconcile flow missing, stale `check-grace-expiry` hourly node, and orphan monitor cadence mismatch.

## Verification

- `/home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_subscriptions.py tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py tests/unit/test_subscription_manager.py tests/unit/test_process_cron_renewal.py` — 124 passed
- `/home/node/.venvs/claw-interface/bin/ruff format --check app tests/unit/test_billing_subscriptions.py tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py tests/unit/test_subscription_manager.py tests/unit/test_process_cron_renewal.py`
- `/home/node/.venvs/claw-interface/bin/ruff check app tests/unit/test_billing_subscriptions.py tests/unit/test_stripe_reconcile.py tests/unit/test_apple_service.py tests/unit/test_subscription_manager.py tests/unit/test_process_cron_renewal.py`
- `/home/node/.venvs/claw-interface/bin/pyright --pythonpath /home/node/.venvs/claw-interface/bin/python app tests/`
- `git diff --check origin/main...HEAD`

Linear: ECA-681

```
