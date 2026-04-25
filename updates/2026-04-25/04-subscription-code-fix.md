---
title: "订阅码激活修复：积分正确到账 + 激活日期修正"
type: "Bug Fix"
priority: "高"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# 订阅码激活修复：积分正确到账 + 激活日期修正

## 核心宣传点

修复了使用订阅码时积分未正确发放、以及激活时间记录错误的问题。

## 原始内容

Commit: a02d3c36ecce04f8f1df4b8c06844c7aed17a1a6

Message:
fix(subscription-code): grant credits + fix start_date on active subs (#1318)

## Summary

Fixes two post-merge regressions from #1270 (subscription code redeem)
that are currently live in production:

### 1. Credits never arrive on redeem (the one you just reproduced)
`redeem_subscription_code` was calling `subscribe()` +
`update_team_models()` + `user_repo.update_fields()`, but **never topped
up the subscription wallet** (`wallet_subscription_id`). The plan badge
flipped to the new tier, but the user's credit balance was untouched.

Fix mirrors `stripe/billing_gateway.py:181-213`: after `subscribe()`,
call `billing_client.topup_wallet(wallet_id=wallet_subscription_id,
granted_credits=PLAN_CREDITS[plan_tier])` — `4800` for starter, `20000`
for pro, `40000` for ultra. On `404/422` (terminated/missing wallet) →
`recover_wallets_and_reread` + one retry; if recovery still can't
produce a wallet_id, raise `ServiceError` so the caller's rollback
branch unwinds the activation (avoids a silent credits-less
subscription).

The top-up logic is extracted into `_topup_subscription_wallet` so the
caller drops below the McCabe-20 complexity gate.

### 2. `start_date` sent to BG for already-subscribed users
`has_active_sub` was derived from `credits_info.get("plan")`, but BG's
`check_credits` response does **not** include a `plan` field (only
`{enough, available_credits, wallets, current_period_end, ...}`). So
`has_active_sub` was always `False`, `start_date` was always sent, and
BG rejected any active-subscriber retest with:

> `400 start_date is only supported when creating a new subscription`

Fix: derive `has_active_sub` from BG's own 400 signal (the only reliable
ground-truth we have), and read the current tier from the local user
doc's `plan` field — same single source of truth
`stripe/entitlement.py:372` uses via `BG_NO_SUBSCRIPTION_STATUSES`.

## Files
- `services/claw-interface/app/services/subscription_code.py` — credits
top-up + data-source fix + helper extraction
- `services/claw-interface/tests/unit/test_subscription_code.py` — mocks
realigned to new data source; happy-path asserts `topup_wallet` called
with `PLAN_CREDITS["pro"] = 20000` on `wallet-sub-123`

## Local verification
- `pytest tests/unit/test_subscription_code.py` — 12/12 pass
- `ruff check` / `ruff format --check` — clean
- `pyright app/ tests/` — `0 errors, 0 warnings, 0 informations`
- `scripts/ci-lint/03-complexity.sh` — `redeem_subscription_code` no
longer appears as a violation (was 22 > 20)

## Test plan
- [ ] CI all green (lint-and-typecheck was the original blocker on #1289
— this PR's squashed diff passes locally)
- [ ] Staging redeem against new-user case (BG returns 400 on
check_credits) → verify continues as rank=0, credits =
`PLAN_CREDITS[tier]`, no BG 400 on subscribe
- [ ] Staging redeem against active-subscriber case (BG already has
subscription) → verify no `start_date` 400, credits stack on existing
balance
- [ ] Staging redeem UI: subscription wallet balance increases by
`PLAN_CREDITS[tier]` after redeem

## Relation to #1289
This is a fresh PR with the same net content as #1289 squashed into a
single commit. #1289 can be closed once this lands; no need to carry
both.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

PR Description:
## Summary

Fixes two post-merge regressions from #1270 (subscription code redeem) that are currently live in production:

### 1. Credits never arrive on redeem (the one you just reproduced)
`redeem_subscription_code` was calling `subscribe()` + `update_team_models()` + `user_repo.update_fields()`, but **never topped up the subscription wallet** (`wallet_subscription_id`). The plan badge flipped to the new tier, but the user's credit balance was untouched.

Fix mirrors `stripe/billing_gateway.py:181-213`: after `subscribe()`, call `billing_client.topup_wallet(wallet_id=wallet_subscription_id, granted_credits=PLAN_CREDITS[plan_tier])` — `4800` for starter, `20000` for pro, `40000` for ultra. On `404/422` (terminated/missing wallet) → `recover_wallets_and_reread` + one retry; if recovery still can't produce a wallet_id, raise `ServiceError` so the caller's rollback branch unwinds the activation (avoids a silent credits-less subscription).

The top-up logic is extracted into `_topup_subscription_wallet` so the caller drops below the McCabe-20 complexity gate.

### 2. `start_date` sent to BG for already-subscribed users
`has_active_sub` was derived from `credits_info.get("plan")`, but BG's `check_credits` response does **not** include a `plan` field (only `{enough, available_credits, wallets, current_period_end, ...}`). So `has_active_sub` was always `False`, `start_date` was always sent, and BG rejected any active-subscriber retest with:

> `400 start_date is only supported when creating a new subscription`

Fix: derive `has_active_sub` from BG's own 400 signal (the only reliable ground-truth we have), and read the current tier from the local user doc's `plan` field — same single source of truth `stripe/entitlement.py:372` uses via `BG_NO_SUBSCRIPTION_STATUSES`.

## Files
- `services/claw-interface/app/services/subscription_code.py` — credits top-up + data-source fix + helper extraction
- `services/claw-interface/tests/unit/test_subscription_code.py` — mocks realigned to new data source; happy-path asserts `topup_wallet` called with `PLAN_CREDITS["pro"] = 20000` on `wallet-sub-123`

## Local verification
- `pytest tests/unit/test_subscription_code.py` — 12/12 pass
- `ruff check` / `ruff format --check` — clean
- `pyright app/ tests/` — `0 errors, 0 warnings, 0 informations`
- `scripts/ci-lint/03-complexity.sh` — `redeem_subscription_code` no longer appears as a violation (was 22 > 20)

## Test plan
- [ ] CI all green (lint-and-typecheck was the original blocker on #1289 — this PR's squashed diff passes locally)
- [ ] Staging redeem against new-user case (BG returns 400 on check_credits) → verify continues as rank=0, credits = `PLAN_CREDITS[tier]`, no BG 400 on subscribe
- [ ] Staging redeem against active-subscriber case (BG already has subscription) → verify no `start_date` 400, credits stack on existing balance
- [ ] Staging redeem UI: subscription wallet balance increases by `PLAN_CREDITS[tier]` after redeem

## Relation to #1289
This is a fresh PR with the same net content as #1289 squashed into a single commit. #1289 can be closed once this lands; no need to carry both.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
