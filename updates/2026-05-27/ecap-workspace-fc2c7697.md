---
title: "计费系统修复：防止订阅状态漂移导致的错误扣费"
type: "Bug Fix"
priority: "高"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# 计费系统修复：防止订阅状态漂移导致的错误扣费

## 核心宣传点

修复了计费系统中可能导致已过期/取消订阅用户被错误扣费的漏洞，保障您的账单准确无误。

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**SHA**: [fc2c7697](https://github.com/SerendipityOneInc/ecap-workspace/commit/fc2c76970d4dea62a54865b3533511926865becf)
**PR**: [#1973](https://github.com/SerendipityOneInc/ecap-workspace/pull/1973)  
**作者**: kaka-srp  
**日期**: 2026-05-27T08:50:48Z

**Commit Message:**

```
fix(billing): prevent reconciliation drift regressions (#1973)

## Summary
- Prevent implicit billing init from creating BG subscriptions for
expired/canceled users.
- Clean stale Stripe ownership fields on expiry and terminal
subscription-code recovery.
- Make Stripe reconcile treat a dead Stripe sub older than current local
entitlement as residual cleanup instead of expiring the user.
- Migrate only remaining legacy purchased credits into BG topup wallets.

## Root cause
Expired/canceled Mongo users could still pass through normal billing
init, which preserved the terminal Mongo status but created an active BG
subscription and wallets. Separately, stale Stripe fields could survive
terminal transitions or code redemption, so reconcile write mode could
target the wrong owner/state.

Linear:
https://linear.app/srpone/issue/ECA-838/fix-billing-reconciliation-drift

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check app tests`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_invite_codes.py::TestCreateUserPublicResponse::test_create_user_response_omits_team_key
tests/unit/test_stripe_entitlement_service.py::TestProductDispatch::test_subscription_recovery_syncs_bot_credentials_when_billing_key_is_created
tests/unit/test_stripe_entitlement_service.py::TestProductDispatch::test_subscription_existing_billing_key_syncs_bot_credentials_when_marker_set
tests/unit/test_user_billing.py tests/unit/test_subscription_manager.py
tests/unit/test_subscription_code.py tests/unit/test_stripe_reconcile.py
tests/unit/test_bg_reconcile.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m py_compile
app/cron/stripe_reconcile.py app/services/antom/subscription_trials.py
app/services/billing.py app/services/stripe/billing_gateway.py
app/services/stripe/entitlement.py
app/services/stripe/handlers/checkout.py
app/services/subscription_code.py app/services/subscription_manager.py`
- [x] `git diff --check`
- [x] Real read-only scan with local `.env`: Stripe scanned=26,
status_drift=0, failed=0; BG scanned=7, bg_orphan=3, failed=0.
- [x] Actual-case dry-run: real expired Mongo user returned unchanged
without touching BG; real BG orphan write-mode path would terminate 3
actual subscriptions with termination faked.
- [ ] `pyright app tests` not run locally: pyright is not installed in
`/home/node/.venvs/claw-interface`.
- [ ] Full pytest not rerun against local root `.env`: that environment
is non-hermetic and makes real OpenClaw/Mattermost/Redis calls.
```


**PR Description:**

## Summary
- Prevent implicit billing init from creating BG subscriptions for expired/canceled users.
- Clean stale Stripe ownership fields on expiry and terminal subscription-code recovery.
- Make Stripe reconcile treat a dead Stripe sub older than current local entitlement as residual cleanup instead of expiring the user.
- Migrate only remaining legacy purchased credits into BG topup wallets.

## Root cause
Expired/canceled Mongo users could still pass through normal billing init, which preserved the terminal Mongo status but created an active BG subscription and wallets. Separately, stale Stripe fields could survive terminal transitions or code redemption, so reconcile write mode could target the wrong owner/state.

Linear: https://linear.app/srpone/issue/ECA-838/fix-billing-reconciliation-drift

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check app tests`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_invite_codes.py::TestCreateUserPublicResponse::test_create_user_response_omits_team_key tests/unit/test_stripe_entitlement_service.py::TestProductDispatch::test_subscription_recovery_syncs_bot_credentials_when_billing_key_is_created tests/unit/test_stripe_entitlement_service.py::TestProductDispatch::test_subscription_existing_billing_key_syncs_bot_credentials_when_marker_set tests/unit/test_user_billing.py tests/unit/test_subscription_manager.py tests/unit/test_subscription_code.py tests/unit/test_stripe_reconcile.py tests/unit/test_bg_reconcile.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m py_compile app/cron/stripe_reconcile.py app/services/antom/subscription_trials.py app/services/billing.py app/services/stripe/billing_gateway.py app/services/stripe/entitlement.py app/services/stripe/handlers/checkout.py app/services/subscription_code.py app/services/subscription_manager.py`
- [x] `git diff --check`
- [x] Real read-only scan with local `.env`: Stripe scanned=26, status_drift=0, failed=0; BG scanned=7, bg_orphan=3, failed=0.
- [x] Actual-case dry-run: real expired Mongo user returned unchanged without touching BG; real BG orphan write-mode path would terminate 3 actual subscriptions with termination faked.
- [ ] `pyright app tests` not run locally: pyright is not installed in `/home/node/.venvs/claw-interface`.
- [ ] Full pytest not rerun against local root `.env`: that environment is non-hermetic and makes real OpenClaw/Mattermost/Redis calls.

