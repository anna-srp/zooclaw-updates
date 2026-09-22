---
title: "fix(billing): unblock subscriptions with legacy pending orders (#3832)"
type: "Bug Fix"
priority: "高"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 修复：历史未完成订单会挡住新的 Pro 订阅

## 核心宣传点

有些用户在 Antom、Airwallex、Creem 这些已经下线的支付渠道里留了未完成的订阅订单，结果即使旧订阅早就结束，也买不了当前的 Stripe Pro 套餐。现在做购买资格检查时会忽略这三个已退役渠道的未完成订单，同时保留「已有有效订阅」和「订单处于已创建/人工审核中」这两类保护。Stripe 自己的未完成订单规则不变：过期的 Checkout 会话不再阻塞，当前套餐的未关闭会话可以继续付，已完成或状态不确定的会话仍需先处理完才能再买。历史订单不删也不改写，不需要环境变量或数据迁移。

## 分级

- 内部：P1
- 外部：A
- 发布状态：已上线

## PR 说明

## Problem and change
Users with unfinished Antom, Airwallex, or Creem subscription orders cannot purchase the current Stripe Pro plan, even after their previous subscription has ended. Ignore pending orders from these retired providers when checking purchase eligibility. Keep active-subscription and created/manual-review protections.

Stripe pending orders retain the existing provider checks: expired Checkout sessions do not block, open current-plan sessions can be resumed, and completed or uncertain sessions must be resolved before another purchase. Keep the original checkout lease lifecycle; this PR does not release the lease early or allow multiple payable Stripe sessions.

Historical orders are not deleted or rewritten. No environment variables or data migration are required.

## Validation
- 159 focused tests passed; 5 existing retired-trial tests skipped.
- Regression tests cover the catalog guard and new Stripe checkout with pending Antom/Airwallex/Creem orders, plus retained Stripe open/completed/expired session handling and timeout recovery.
- Backend Ruff, formatting, Pyright and import-contract checks.

Not deployed; no production data modified by this PR.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8cbcad1ffdc766cf9c359da73cbcd3c516c03090`
- PR: #3832
- 作者：sam-srp
- 日期：2026-09-21T05:04:00Z

### Commit Message

```
fix(billing): unblock subscriptions with legacy pending orders (#3832)

## Problem and change
Users with unfinished Antom, Airwallex, or Creem subscription orders
cannot purchase the current Stripe Pro plan, even after their previous
subscription has ended. Ignore pending orders from these retired
providers when checking purchase eligibility. Keep active-subscription
and created/manual-review protections.

Stripe pending orders retain the existing provider checks: expired
Checkout sessions do not block, open current-plan sessions can be
resumed, and completed or uncertain sessions must be resolved before
another purchase. Keep the original checkout lease lifecycle; this PR
does not release the lease early or allow multiple payable Stripe
sessions.

Historical orders are not deleted or rewritten. No environment variables
or data migration are required.

## Validation
- 159 focused tests passed; 5 existing retired-trial tests skipped.
- Regression tests cover the catalog guard and new Stripe checkout with
pending Antom/Airwallex/Creem orders, plus retained Stripe
open/completed/expired session handling and timeout recovery.
- Backend Ruff, formatting, Pyright and import-contract checks.

Not deployed; no production data modified by this PR.
```

来源：SerendipityOneInc/ecap-workspace @ 8cbcad1f，PR #3832，作者 sam-srp。