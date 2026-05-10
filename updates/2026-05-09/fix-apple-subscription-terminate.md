---
title: "修复：Apple 订阅到期后账户权益正确终止"
type: "Bug Fix"
priority: "高"
date: "2026-05-09"
status: "待审核"
channels: ""
---
# 修复：Apple 订阅到期后账户权益正确终止

## 核心宣传点
修复了 Apple 订阅到期时，后台计费服务（BG/Lago）仍保持活跃状态的问题，现在 Apple 订阅过期后会正确终止所有关联权益，避免因状态不同步导致的支付失败或无法续费。

## 原始内容

**Commit**: `87752450` | **PR**: #1582

### Commit Message

```
fix(claw-interface): Apple webhook BG terminate + Stripe drift recovery (ECA-647) (#1582)

## Summary

- A. app/routes/apple.py — Apple S2S webhook DEACTIVATE (EXPIRED / DID_FAIL_TO_RENEW / REVOKE) now calls billing.terminate_subscription(team_id) before clear_wallet, mirroring subscription_cron.py:_handle_expired_subscription. Closes the asymmetry that left BG/Lago with active subs after Apple expiry.
- B. app/services/stripe/billing_gateway.py — grant_subscription_via_billing_gateway catches the BG 400 `start_date is only supported when creating a new subscription` and retries without start_date. Mirrors the existing pattern in subscription_manager.py:178-195. Belt-and-braces for any future drift from sources other than the Apple webhook.
```

### PR Body

## Summary

- **A.** `app/routes/apple.py` — Apple S2S webhook DEACTIVATE (`EXPIRED` / `DID_FAIL_TO_RENEW` / `REVOKE`) now calls `billing.terminate_subscription(team_id)` before `clear_wallet`, mirroring `subscription_cron.py:_handle_expired_subscription`. Closes the asymmetry that left BG/Lago with active subs after Apple expiry.
- **B.** `app/services/stripe/billing_gateway.py` — `grant_subscription_via_billing_gateway` catches the BG 400 `start_date is only supported when creating a new subscription` and retries without `start_date`. Mirrors the existing pattern in `subscription_manager.py:178-195`. Belt-and-braces for any future drift from sources other than the Apple webhook.

## Production incident

`uid=7274359038282399744` on 2026-05-09 05:57–05:58 UTC paid $20 via Stripe → BG subscribe rejected with the 400 above (Apple sub from 2026-04-03 still alive in Lago) → saga refunded → user got money back but no entitlement. Sweep across all 2298 expired accounts found 11 affected users; data wash already applied (BG terminate + mongo cleanup of stale Stripe IDs).

## Test plan

- [x] `tests/unit/test_apple_routes.py` — 4 updated tests assert `terminate_subscription` is called (or skipped when no `team_id`); 1 new test covers terminate failure not breaking the cleanup chain
- [x] `tests/unit/test_stripe_billing_gateway.py` — 3 new tests: drift-400 retries without `start_date` (same `transaction_id` for BG idempotency), other-400 propagates, no-`start_date`-400 propagates (no infinite retry)

Linear-issue: Fixes ECA-647
