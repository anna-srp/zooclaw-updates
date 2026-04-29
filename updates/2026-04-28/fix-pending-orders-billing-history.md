---
title: "修复：账单记录中不再显示未付款订单"
type: "Bug Fix"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 修复：账单记录中不再显示未付款订单

## 核心宣传点

修复了账单历史页面错误显示未完成支付订单（如 $240 假记录）的问题，账单信息更准确。

## 原始内容

**Commit**: `dd7ff269b0ad81e9118eb001431ab2742db07fdc`
**仓库**: ecap-workspace
**作者**: bryce-srp
**时间**: 2026-04-28T11:18:51Z

### 完整 Commit Message

```
fix(claw-interface): exclude pending orders from billing history (#1438)

## Summary
- Abandoned checkout sessions leave `status=pending` orders in MongoDB
that were never paid
- These showed up in the billing page as real charges (e.g. $240 for a
yearly starter plan)
- Added `exclude_pending` flag to `count_for_uid` and `list_for_uid`
repo methods
- `list_orders` route now uses `exclude_pending=True` so pending orders
don't appear in billing history
- Admin endpoints are unaffected (they don't use these methods)

## Root cause
User clicked "Subscribe Starter Yearly" → order created (pending) →
Stripe checkout never completed → order stuck as pending → billing page
showed $240 charge that doesn't exist in Stripe

## Test plan
- [ ] CI passes (pyright + pytest)
- [ ] Verify billing page no longer shows pending/abandoned orders
- [ ] Verify paid orders still appear correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1438 完整描述

## Summary
- Abandoned checkout sessions leave `status=pending` orders in MongoDB that were never paid
- These showed up in the billing page as real charges (e.g. $240 for a yearly starter plan)
- Added `exclude_pending` flag to `count_for_uid` and `list_for_uid` repo methods
- `list_orders` route now uses `exclude_pending=True` so pending orders don't appear in billing history
- Admin endpoints are unaffected (they don't use these methods)

## Root cause
User clicked "Subscribe Starter Yearly" → order created (pending) → Stripe checkout never completed → order stuck as pending → billing page showed $240 charge that doesn't exist in Stripe

## Test plan
- [ ] CI passes (pyright + pytest)
- [ ] Verify billing page no longer shows pending/abandoned orders
- [ ] Verify paid orders still appear correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)
