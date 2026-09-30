---
title: "修复：订阅取消或到期后可以重新购买了，不再被历史周期结束日期挡住"
type: "Bug Fix"
priority: "高"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 修复：订阅取消或到期后可以重新购买了，不再被历史周期结束日期挡住

## 核心宣传点

订阅协议被取消或已到期时，如果它的历史计费周期结束日期还在未来，购买资格判定会把这个未来日期当成「你还有剩余访问权」，而访问权解析那边其实已经判定为过期——结果就是立即终止订阅的用户既没有权限，也买不了新套餐，彻底卡住。现在取消或过期的协议不再挡住新订阅；仍然生效的协议、处于取消中的协议、未结清的支付，以及旧版 Stripe「在 Stripe 中缺失」的恢复期，都保持原有保护。同时，已过期的个人权限摘要里不再显示那些来自失效协议的未来结束日期，真正生效的订阅仍然照常显示日期。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
- Allow a new subscription after an agreement is canceled or expired even if its historical billing cycle ends in the future. Keep active/canceling agreements, unresolved payments, and legacy Stripe `missing_in_stripe` recovery periods protected.
- Hide future historical end dates in the expired personal-access summary; effective subscriptions retain their existing dates.

## Root cause
Purchase eligibility treated a terminal agreement's original `current_period_end` as remaining access, while the access resolver correctly returned expired. Immediate termination therefore left users unable to buy a replacement plan. The expired summary also reused future dates from stale agreements/payment entitlements.

## Test plan
- [x] 99 targeted unit tests: terminal states across providers, active/canceling/manual-review protection, legacy cutover recovery boundaries, unresolved checkout protection, and access-summary contracts.
- [x] Full backend static checks: Ruff, formatting, Pyright and import architecture contracts.
- No database migration or new environment variables. This PR does not perform bulk account repairs.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `21c1d37bb80239fe6042e19cebe8af12b48d1cf7`
- PR: #3921
- 作者：sam-srp
- 日期：2026-09-29T04:42:47Z

### Commit Message

```
fix(billing): allow repurchase after terminal subscriptions (#3921)

## Summary
- Allow a new subscription after an agreement is canceled or expired
even if its historical billing cycle ends in the future. Keep
active/canceling agreements, unresolved payments, and legacy Stripe
`missing_in_stripe` recovery periods protected.
- Hide future historical end dates in the expired personal-access
summary; effective subscriptions retain their existing dates.

## Root cause
Purchase eligibility treated a terminal agreement's original
`current_period_end` as remaining access, while the access resolver
correctly returned expired. Immediate termination therefore left users
unable to buy a replacement plan. The expired summary also reused future
dates from stale agreements/payment entitlements.

## Test plan
- [x] 99 targeted unit tests: terminal states across providers,
active/canceling/manual-review protection, legacy cutover recovery
boundaries, unresolved checkout protection, and access-summary
contracts.
- [x] Full backend static checks: Ruff, formatting, Pyright and import
architecture contracts.
- No database migration or new environment variables. This PR does not
perform bulk account repairs.
```

来源：SerendipityOneInc/ecap-workspace @ 21c1d37b，PR #3921，作者 sam-srp。
