---
title: "修复订阅试用流程，确保 trial 正常履约"
type: "Bug Fix"
priority: "中"
date: "2026-06-03"
status: "待审核"
channels: "Discord, changelog"
---
# 修复订阅试用流程，确保 trial 正常履约

## 核心宣传点

修复了部分用户试用订阅未能正常激活的问题。

## 原始内容

**Repo:** SerendipityOneInc/ecap-workspace  
**SHA:** `96f639e44a65ed01969ec026078424aa80424cfe`  
**作者:** kaka-srp  
**日期:** 2026-06-03T13:22:49Z  
**URL:** https://github.com/SerendipityOneInc/ecap-workspace/commit/96f639e44a65ed01969ec026078424aa80424cfe

### Commit Message

```
fix(billing): subscribe trial fulfillment in billing gateway (#2203)

## Summary
- Ensure Billing v2 subscription-wallet fulfillment always
creates/updates the BG/Lago subscription relationship before topup,
including trial entitlements.
- Update the trial fulfillment unit test to assert BG subscribe is
called.
- Include the workspace `AGENTS.md` cluster/startup instruction update.

## Root cause
Trial entitlements used `source_type=trial`, and the shared fulfillment
path skipped `billing_client.subscribe()` for that source type. The
entitlement ledger and v2 current access became active/trialing, but BG
`/credits/check` still failed because Lago had no active subscription
for the customer.

## Production repair
- Repaired customer `7453048380181188608` by creating BG subscription
`starter_20_month` under customer id `7453048380181188608`.
- Verified `/credits/check` returns `enough=true` with
`available_credits=5040`.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/ruff check
app/services/billing_v2/fulfillment.py
tests/unit/test_billing_v2_fulfillment.py`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_antom_billing_v2.py tests/unit/test_stripe_billing_v2.py
-q`
```

### PR Description

## Summary
- Ensure Billing v2 subscription-wallet fulfillment always creates/updates the BG/Lago subscription relationship before topup, including trial entitlements.
- Update the trial fulfillment unit test to assert BG subscribe is called.
- Include the workspace `AGENTS.md` cluster/startup instruction update.

## Root cause
Trial entitlements used `source_type=trial`, and the shared fulfillment path skipped `billing_client.subscribe()` for that source type. The entitlement ledger and v2 current access became active/trialing, but BG `/credits/check` still failed because Lago had no active subscription for the customer.

## Production repair
- Repaired customer `7453048380181188608` by creating BG subscription `starter_20_month` under customer id `7453048380181188608`.
- Verified `/credits/check` returns `enough=true` with `available_credits=5040`.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/ruff check app/services/billing_v2/fulfillment.py tests/unit/test_billing_v2_fulfillment.py`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_v2_fulfillment.py tests/unit/test_antom_billing_v2.py tests/unit/test_stripe_billing_v2.py -q`
