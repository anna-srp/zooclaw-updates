---
title: "修复：企业套餐付款链接过期后重复拿到同一条打不开的链接"
type: "Bug Fix"
priority: "中"
date: "2026-09-03"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：企业套餐付款链接过期后重复拿到同一条打不开的链接

## 核心宣传点

企业垂直套餐的购买流程以前只要发现本地还有一个「待支付」的订单，就直接把它上面的 Airwallex 收银台链接重新甩给你，只校验域名是不是官方主机，从来不看这条链接自己带的过期时间。结果链接在服务商那边早就失效了，本地订单还挂着待支付，你再点几次购买，每次拿到的都是同一条已经打不开的链接。

现在会解出收银台链接里 JWT 的过期时间来判断（不新增持久化字段）：只有在链接距离过期还剩五分钟以上的安全窗口内，才会复用这个待支付的收银台；否则先安全地把服务商那边处于活跃状态、又不可复用的收银台取消掉，再退役本地订单并创建一条新的。当服务商返回的结果含糊不清时，人工复核和并发保护的栅栏依然保留，不会误删或重复下单。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f5cb9e02deda6836c3c17ad6043fc2f08e065fd8`
- PR: #3639
- 作者: tim-srp
- 日期: 2026-09-03T09:05:25Z

### Commit Message

```
fix(billing): refresh expiring Airwallex checkout links (#3639)

## Summary

- Decode the Airwallex Checkout URL JWT expiry without adding a
persisted field.
- Reuse a pending Checkout only when it remains valid beyond a
five-minute safety window.
- Safely cancel an active non-reusable Checkout before retiring its
local order and creating a replacement.
- Preserve manual-review and concurrency fences when provider outcomes
are ambiguous.

## Root cause

The enterprise vertical-package flow replayed every pending URL on an
official Airwallex host without checking the JWT `exp`. A local order
could remain pending after the provider URL expired, so later purchase
attempts repeatedly received the same unusable link.

## Test plan

- [x] `pytest tests/unit/test_airwallex_enterprise_checkout.py -q` — 45
passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

```
## Summary

- Decode the Airwallex Checkout URL JWT expiry without adding a persisted field.
- Reuse a pending Checkout only when it remains valid beyond a five-minute safety window.
- Safely cancel an active non-reusable Checkout before retiring its local order and creating a replacement.
- Preserve manual-review and concurrency fences when provider outcomes are ambiguous.

## Root cause

The enterprise vertical-package flow replayed every pending URL on an official Airwallex host without checking the JWT `exp`. A local order could remain pending after the provider URL expired, so later purchase attempts repeatedly received the same unusable link.

## Test plan

- [x] `pytest tests/unit/test_airwallex_enterprise_checkout.py -q` — 45 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
```
