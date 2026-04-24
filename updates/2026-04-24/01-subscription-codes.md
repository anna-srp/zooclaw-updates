---
title: "订阅码：用礼品码直接激活订阅套餐"
type: "新功能上线"
priority: "高"
date: "2026-04-24"
status: "待审核"
channels: ""
---
# 订阅码：用礼品码直接激活订阅套餐

## 核心宣传点
现在可以发放订阅码，用户兑换后直接获得 Starter/Pro/Ultra 套餐订阅，不再只是积分——送礼更有价值，充值更灵活。

## 原始内容

feat: subscription code — redeem codes that grant real subscriptions (#1270)

### Summary
- Add subscription codes — gift codes that grant real subscriptions (Starter/Pro/Ultra) instead of credits
- Admin manages via independent "Subscription Code" tab with plan tier, duration days, max activations
- Users redeem via the same input — backend auto-detects code category and dispatches accordingly
- Rejects redeem if current plan is higher than code (no downgrade); same-tier appends duration

### Changes

#### Backend
- New `subscription_code` service with plan validation, time window calculation, rollback on failure
- Unified `POST /api/gift-code/redeem` dispatches by `category` field (credits vs subscription)
- New admin `POST/GET /admin/subscription-codes` endpoints
- New `ecap-subscription-code-activations` collection (independent frequency tracking)
- Extends `ecap-gift-codes` with `category`, `plan_tier`, `duration_days` fields
- 13 unit tests covering expiry, exhaustion, plan downgrade, CAS conflict, rollback

#### Frontend
- New `SubscriptionCodesTab` admin component with plan tier badges
- `useSubscriptionCodes` hook (React Query CRUD)
- Modified `UserMenu` redeem handler — shows subscription-specific toast
- i18n keys added to 7 locales (en, zh, ja, ko, es, pt, ar)
