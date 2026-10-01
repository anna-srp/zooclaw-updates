---
title: "修复：同一账号重复购买不再在 Stripe 里生成多个客户记录，也不会被当成首次购买"
type: "Bug Fix"
priority: "中"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 修复：同一账号重复购买不再在 Stripe 里生成多个客户记录，也不会被当成首次购买

## 核心宣传点

订阅和充值的结账此前只传了邮箱，导致同一个 ZooWork 用户重复购买会在 Stripe 里生成多个独立客户记录，并被重新当作首次购买处理（优惠码的首购限制因此会被反复命中）。现在新的结账请求共用一份按用户 ID 和 Stripe 账号作用域绑定的持久客户关系。系统会从该用户 ID 名下成功的付款历史（含 0 元和已退款订单）、协议或历史记录中找回已有客户，绝不只靠邮箱来关联账号。绑定会原子化预留并用稳定的幂等键创建，重试时冻结创建参数，所选客户会持久化到付款订单上；超出安全重试窗口仍未解析出客户，或身份校验不通过时一律失败而不是放行。订阅和充值两条结账链路都会传客户参数，同一 Stripe 账号内轮换 API Key 不影响绑定关系。优惠码和商品配置、环境变量都没有改动。

## 分级

- 内部：P1
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
Subscription and top-up Checkout previously supplied only
`customer_email`, allowing repeat purchases by one ZooWork user to
create separate Stripe Customers and be treated as first-time purchases
again. New Checkout requests now share a durable Customer binding scoped
to UID and Stripe account. Staging and production already use separate
databases; no test/live binding field or API-key-prefix parsing is
added.

## Root cause and fix
- Recover an existing Customer from UID-owned successful payment history
(including zero-dollar/refunded orders), agreements or legacy records;
never associate accounts by email alone.
- Reserve one binding atomically and create with a stable Stripe
idempotency key. Freeze creation parameters for retries, persist the
selected Customer on the payment order, and fail closed on unresolved
creation beyond the safe retry window or invalid canonical identity.
- Both subscription and top-up Checkout pass `customer`. API-key
rotation within a Stripe account preserves the binding. Coupon/product
settings and environment variables are unchanged.

## Test plan
- [x] Billing-policy and Stripe unit suite: 644 passed, 5 skipped; CSFLE
query guard passed; all 18 new customer/repository tests passed.
- [x] Full `scripts/verify-py.sh`: Ruff, format, Pyright, import
contracts; commit hooks also passed.
- [x] New read operations exercised through staging's actual encrypted
Mongo client (`encryption_enabled=True`).
- [ ] Staging encrypted write/CAS exercise with an isolated fixture and
Stripe sandbox end-to-end redemption validation before release.

## Rollout boundaries
Existing Checkout URLs and pre-deployment uncertain requests retain
their original parameters for payment/idempotency safety; already issued
URLs are not retroactively expired and can remain usable until normal
expiry. Existing Stripe Customers/balances/subscriptions are not merged
or modified. This PR has not been deployed and does not change
production data.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `c6cb0bec51108a936e856196146a11de888f5117`
- PR: #3940
- 作者：sam-srp
- 日期：2026-09-30T05:46:12Z

### Commit Message

```
fix(billing): reuse Stripe customers across checkout purchases (#3940)

## Summary
Subscription and top-up Checkout previously supplied only
`customer_email`, allowing repeat purchases by one ZooWork user to
create separate Stripe Customers and be treated as first-time purchases
again. New Checkout requests now share a durable Customer binding scoped
to UID and Stripe account. Staging and production already use separate
databases; no test/live binding field or API-key-prefix parsing is
added.

## Root cause and fix
- Recover an existing Customer from UID-owned successful payment history
(including zero-dollar/refunded orders), agreements or legacy records;
never associate accounts by email alone.
- Reserve one binding atomically and create with a stable Stripe
idempotency key. Freeze creation parameters for retries, persist the
selected Customer on the payment order, and fail closed on unresolved
creation beyond the safe retry window or invalid canonical identity.
- Both subscription and top-up Checkout pass `customer`. API-key
rotation within a Stripe account preserves the binding. Coupon/product
settings and environment variables are unchanged.

## Test plan
- [x] Billing-policy and Stripe unit suite: 644 passed, 5 skipped; CSFLE
query guard passed; all 18 new customer/repository tests passed.
- [x] Full `scripts/verify-py.sh`: Ruff, format, Pyright, import
contracts; commit hooks also passed.
- [x] New read operations exercised through staging's actual encrypted
Mongo client (`encryption_enabled=True`).
- [ ] Staging encrypted write/CAS exercise with an isolated fixture and
Stripe sandbox end-to-end redemption validation before release.

## Rollout boundaries
Existing Checkout URLs and pre-deployment uncertain requests retain
their original parameters for payment/idempotency safety; already issued
URLs are not retroactively expired and can remain usable until normal
expiry. Existing Stripe Customers/balances/subscriptions are not merged
or modified. This PR has not been deployed and does not change
production data.
```

来源：SerendipityOneInc/ecap-workspace @ c6cb0bec，PR #3940，作者 sam-srp。
