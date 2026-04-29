---
title: "修复：订阅码兑换计费参数异常"
type: "Bug Fix"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 修复：订阅码兑换计费参数异常

## 核心宣传点

修复了订阅码兑换时传入多余参数导致的计费异常，确保订阅正常生效。

## 原始内容

**Commit**: `d985a34016459cf1983bcc8d4c1d66343176f39a`
**仓库**: ecap-workspace
**作者**: bryce-srp
**时间**: 2026-04-28T11:22:57Z

### 完整 Commit Message

```
fix(claw-interface): remove ending_at from subscription code billing call (#1444)

## Summary
- Remove `ending_at` parameter from `billing_client.subscribe()` call in
subscription code redemption path
- Aligns with all other subscribe call sites (billing init, subscription
manager, Stripe entitlement) which already omit `ending_at`
- Subscription expiry is managed by cron terminate via MongoDB
`subscription_end_time` — passing `ending_at` to BG caused redundant
auto-termination

## Context
All 21 BG subscriptions with `ending_at` set (April 24-28) were traced
to subscription code redemptions (`ZC-*` codes, mostly ultra tier). This
was the last call site still passing `ending_at` to Billing Gateway.

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify existing subscription code tests still pass
- [ ] Redeem a test subscription code on staging — confirm BG
subscription is created without `ending_at`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1444 完整描述

## Summary
- Remove `ending_at` parameter from `billing_client.subscribe()` call in subscription code redemption path
- Aligns with all other subscribe call sites (billing init, subscription manager, Stripe entitlement) which already omit `ending_at`
- Subscription expiry is managed by cron terminate via MongoDB `subscription_end_time` — passing `ending_at` to BG caused redundant auto-termination

## Context
All 21 BG subscriptions with `ending_at` set (April 24-28) were traced to subscription code redemptions (`ZC-*` codes, mostly ultra tier). This was the last call site still passing `ending_at` to Billing Gateway.

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify existing subscription code tests still pass
- [ ] Redeem a test subscription code on staging — confirm BG subscription is created without `ending_at`

🤖 Generated with [Claude Code](https://claude.com/claude-code)
