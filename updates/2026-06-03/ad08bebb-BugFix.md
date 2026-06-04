---
title: "修复取消订阅时本地状态覆盖问题"
type: "Bug Fix"
priority: "中"
date: "2026-06-03"
status: "待审核"
channels: "Discord, changelog"
---
# 修复取消订阅时本地状态覆盖问题

## 核心宣传点

修复订阅取消后状态显示异常的问题，避免用户困惑。

## 原始内容

**Repo:** SerendipityOneInc/ecap-workspace  
**SHA:** `ad08bebb4eb95c5eb1de29a8a556eacfe92bc95d`  
**作者:** kaka-srp  
**日期:** 2026-06-03T12:48:49Z  
**URL:** https://github.com/SerendipityOneInc/ecap-workspace/commit/ad08bebb4eb95c5eb1de29a8a556eacfe92bc95d

### Commit Message

```
fix(billing): preserve local cancel on stale active updates (#2201)

## Summary
- Preserve local `canceling` / `cancel_at_period_end` when non-user
stale ACTIVE subscription facts retry against the latest agreement
state.
- Keep user-initiated renew / clear-cancel flows allowed.
- Add regression coverage for the CAS race window raised by CI review.

## Root cause
After #2199 allowed the legitimate `canceling -> active` state
transition, a stale provider ACTIVE update could load an `active`
snapshot, lose CAS to a concurrent local cancel, then retry against the
latest `canceling` agreement and clear `cancel_at_period_end` because
the service-layer stale-live guard only preserved `current` and
`current_period_end`.

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/ruff check
app/services/billing_v2/subscription_agreement_upsert.py
app/services/billing_v2/subscription_agreements.py
tests/unit/test_billing_v2_subscription_agreements.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_billing_v2_subscription_agreements.py -q`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_billing_v2_*.py tests/unit/test_antom_billing_v2.py -q`
- [x] `cd services/claw-interface && scripts/ci-lint/01-file-length.sh`
```

### PR Description

## Summary
- Preserve local `canceling` / `cancel_at_period_end` when non-user stale ACTIVE subscription facts retry against the latest agreement state.
- Keep user-initiated renew / clear-cancel flows allowed.
- Add regression coverage for the CAS race window raised by CI review.

## Root cause
After #2199 allowed the legitimate `canceling -> active` state transition, a stale provider ACTIVE update could load an `active` snapshot, lose CAS to a concurrent local cancel, then retry against the latest `canceling` agreement and clear `cancel_at_period_end` because the service-layer stale-live guard only preserved `current` and `current_period_end`.

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/ruff check app/services/billing_v2/subscription_agreement_upsert.py app/services/billing_v2/subscription_agreements.py tests/unit/test_billing_v2_subscription_agreements.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_billing_v2_subscription_agreements.py -q`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_billing_v2_*.py tests/unit/test_antom_billing_v2.py -q`
- [x] `cd services/claw-interface && scripts/ci-lint/01-file-length.sh`
