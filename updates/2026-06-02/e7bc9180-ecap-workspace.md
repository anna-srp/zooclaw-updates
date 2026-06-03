---
title: "[平台] handle apple renewal status webhooks"
type: "Bug Fix"
priority: "中"
date: "2026-06-02"
status: "待审核"
channels: ""
---
# [平台] handle apple renewal status webhooks

## 核心宣传点
来自 ecap-workspace 仓库的更新：fix(billing): handle apple renewal status webhooks

## 原始内容
**Commit**: e7bc9180520607a50f7f8bf43954f5dfd4aea40a
**Title**: fix(billing): handle apple renewal status webhooks (#2145)
**Author**: kaka-srp
**Date**: 2026-06-02T02:33:01Z

**PR**: #2145

### Commit Message
```
fix(billing): handle apple renewal status webhooks (#2145)

## Summary
- Read Apple notification environment from the real App Store Server
Notification v2 shape (`data.environment`) and normalize SDK enum
strings before routing.
- Handle `DID_CHANGE_RENEWAL_STATUS` for Apple Billing v2 so
`AUTO_RENEW_DISABLED` marks the agreement canceling and
`AUTO_RENEW_ENABLED` restores active renewal.
- Decode `data.signedRenewalInfo` and process renewal-status webhooks
even when Apple omits `signedTransactionInfo`, using the existing
Billing v2 agreement as the owner/period context.
- Prevent Billing v2 current access from falling back to providerless
trial after a paid provider subscription has started and later reaches
period end. Trial credits remain active/auditable and can still be
included in credit balance; this only fixes subscription state
resolution.
- Split Apple paid transaction fact recording into `billing_v2_facts.py`
to keep notification routing small and under the app file-size guard.

## Root cause
Apple sends the notification environment under `data.environment`, but
the route only checked a top-level `environment`. The cancellation
webhook was acknowledged but rejected as `received=unknown`. Billing v2
also only handled the old legacy Apple webhook set and ignored
renewal-status changes.

During staging iOS sandbox testing, a second state-resolution issue was
found: after a paid provider subscription period ends, an earlier active
providerless trial entitlement could make `current_access` fall back to
`trial`. That is incorrect for subscription state once a paid provider
subscription has started, even though the trial credit ledger entry
itself should remain active.

CI review also correctly pointed out that Apple renewal-status
notifications can rely on `signedRenewalInfo`; this PR now decodes that
payload and covers the no-transaction renewal-status path.

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff format --check
app/routes/apple.py app/services/apple/billing_v2.py
app/services/apple/billing_v2_facts.py
app/services/apple/billing_v2_notifications.py
app/services/billing_summary/current_access.py
tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py
tests/unit/test_billing_summary_v2.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check
app/routes/apple.py app/services/apple/billing_v2.py
app/services/apple/billing_v2_facts.py
app/services/apple/billing_v2_notifications.py
app/services/billing_summary/current_access.py
tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py
tests/unit/test_billing_summary_v2.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright
app/routes/apple.py app/services/apple/billing_v2.py
app/services/apple/billing_v2_facts.py
app/services/apple/billing_v2_notifications.py
app/services/billing_summary/current_access.py
tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py
tests/unit/test_billing_summary_v2.py`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_billing_summary_v2.py
services/claw-interface/tests/unit/test_apple_routes.py
services/claw-interface/tests/unit/test_apple_billing_v2.py`
- [x] Staging iOS sandbox: subscribe, restore auto-renew, cancel
auto-renew; verified Apple `DID_CHANGE_RENEWAL_STATUS` events process
and agreement transitions active/canceling correctly.
- [x] Staging data simulation: current access before Apple period end
resolves to `canceling`; after period end resolves to `expired/free`
instead of trial fallback.

## Staging beta
- `service-v0.7.3-beta.4` deployed initial Apple webhook fix.
- `service-v0.7.3-beta.5` was cut for the trial-fallback fix; staging
deploy monitoring is intentionally not required for this PR gate.
```

### PR Description
## Summary
- Read Apple notification environment from the real App Store Server Notification v2 shape (`data.environment`) and normalize SDK enum strings before routing.
- Handle `DID_CHANGE_RENEWAL_STATUS` for Apple Billing v2 so `AUTO_RENEW_DISABLED` marks the agreement canceling and `AUTO_RENEW_ENABLED` restores active renewal.
- Decode `data.signedRenewalInfo` and process renewal-status webhooks even when Apple omits `signedTransactionInfo`, using the existing Billing v2 agreement as the owner/period context.
- Prevent Billing v2 current access from falling back to providerless trial after a paid provider subscription has started and later reaches period end. Trial credits remain active/auditable and can still be included in credit balance; this only fixes subscription state resolution.
- Split Apple paid transaction fact recording into `billing_v2_facts.py` to keep notification routing small and under the app file-size guard.

## Root cause
Apple sends the notification environment under `data.environment`, but the route only checked a top-level `environment`. The cancellation webhook was acknowledged but rejected as `received=unknown`. Billing v2 also only handled the old legacy Apple webhook set and ignored renewal-status changes.

During staging iOS sandbox testing, a second state-resolution issue was found: after a paid provider subscription period ends, an earlier active providerless trial entitlement could make `current_access` fall back to `trial`. That is incorrect for subscription state once a paid provider subscription has started, even though the trial credit ledger entry itself should remain active.

CI review also correctly pointed out that Apple renewal-status notifications can rely on `signedRenewalInfo`; this PR now decodes that payload and covers the no-transaction renewal-status path.

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff format --check app/routes/apple.py app/services/apple/billing_v2.py app/services/apple/billing_v2_facts.py app/services/apple/billing_v2_notifications.py app/services/billing_summary/current_access.py tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py tests/unit/test_billing_summary_v2.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check app/routes/apple.py app/services/apple/billing_v2.py app/services/apple/billing_v2_facts.py app/services/apple/billing_v2_notifications.py app/services/billing_summary/current_access.py tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py tests/unit/test_billing_summary_v2.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright app/routes/apple.py app/services/apple/billing_v2.py app/services/apple/billing_v2_facts.py app/services/apple/billing_v2_notifications.py app/services/billing_summary/current_access.py tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py tests/unit/test_billing_summary_v2.py`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_billing_summary_v2.py services/claw-interface/tests/unit/test_apple_routes.py services/claw-interface/tests/unit/test_apple_billing_v2.py`
- [x] Staging iOS sandbox: subscribe, restore auto-renew, cancel auto-renew; verified Apple `DID_CHANGE_RENEWAL_STATUS` events process and agreement transitions active/canceling correctly.
- [x] Staging data simulation: current access before Apple period end resolves to `canceling`; after period end resolves to `expired/free` instead of trial fallback.

## Staging beta
- `service-v0.7.3-beta.4` deployed initial Apple webhook fix.
- `service-v0.7.3-beta.5` was cut for the trial-fallback fix; staging deploy monitoring is intentionally not required for this PR gate.

