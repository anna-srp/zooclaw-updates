---
title: "Pro 订阅结账支持 Stripe 优惠码，折扣后（含 0 元）也照样开通完整权益"
type: "新功能"
priority: "高"
date: "2026-09-24"
status: "待审核"
channels: ""
---

# Pro 订阅结账支持 Stripe 优惠码，折扣后（含 0 元）也照样开通完整权益

## 核心宣传点

Pro 订阅的 Checkout 页面现在能输入 Stripe 优惠码了，并且始终收集支付方式以保证自动续费。优惠码是否可用、折多少、折几期完全由 Stripe 侧控制，本地不发码、也不限制只能首期使用。按月履约的链路会去读并校验已支付的 Stripe 发票，记录真实支付金额、折扣额和客户发票余额凭证，然后授予完整的 Pro 权益——部分折扣和全额折扣都算，包括完全由折扣和/或账户余额抵掉、没有 PaymentIntent 的 0 元发票。0 元授权只限于校验过的当前策略 Pro 订阅发票，按周期履约的防重仍然拦得住重复的发票/Checkout 投递。财务审计事件保留了变更前后金额、折扣、余额抵扣和发票/订阅身份。充值、旧版支付链路和 billing-gateway 不受影响；要用优惠码，需要先在对应的 Stripe 账号/环境里创建 Coupon 和 Promotion Code。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已上线

## PR 说明

## Summary
Pro subscription Checkout now accepts Stripe promotion codes and always collects a payment method for automatic renewal. Stripe controls code eligibility, discount amount and duration; there is no local code issuance or first-period restriction.

The monthly fulfillment path reads and validates the paid Stripe invoice, records its actual paid amount, discount and customer invoice balance evidence, and grants the full Pro entitlement for partial or full discounts, including $0 invoices settled entirely by discounts and/or customer balance without a PaymentIntent. Zero-amount grants remain restricted to verified current-policy Pro subscription invoices. Existing period-based fulfillment protects against duplicate invoice/Checkout delivery. Financial audit events retain before/after amounts, discounts, balance offsets and invoice/subscription identities, including the actual prior row after a duplicate-insert race.

Topups, legacy payment flows and billing-gateway are unchanged. No new environment variables, queries or scheduled jobs. Coupons and Promotion Codes must be created in the intended Stripe account/environment. Customer invoice balance supports partial/full offsets, surplus balance, discount combinations and fully paid debit balances. Paid minimum-charge deferrals are accepted only after a read-only Stripe query verifies the unique invoice_too_small transaction for the same invoice/customer/currency/environment. Deferred amounts and transaction IDs are audited separately from discounts and balance consumption. Cancellation does not trigger extra local collection: the debit stays in Stripe for future applicable invoices, and may remain uncollected if no further invoice is issued. Tax and current-invoice credit notes remain outside the supported invoice contract.

## Test plan
- [x] 324 related unit tests passed, including full/partial/recurring discounts, legacy/modern Stripe invoice shapes, $0 entitlement guards, Checkout and invoice replay, cancellation periods, renewal, topup isolation, customer balance reconciliation and durable financial audit snapshots, small-amount carry-forward proof, rejected/ambiguous evidence, pagination, query failures, cancellation and next-period collection.
- [x] Backend pre-commit checks passed, including Ruff, Pyright, import contracts, file size and complexity.
- [ ] Stripe Sandbox end-to-end acceptance: actual code redemption, $0 payment-method collection, customer balance offsets, minimum-charge deferrals, renewal and cancellation. Not deployed by this PR.




## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `896730f7f50c5405a81d5ab5af2918596643a233`
- PR: #3891
- 作者：sam-srp
- 日期：2026-09-24T02:54:58Z

### Commit Message

```
feat(billing): support Stripe promotion codes for Pro subscriptions (#3891)

## Summary
Pro subscription Checkout now accepts Stripe promotion codes and always
collects a payment method for automatic renewal. Stripe controls code
eligibility, discount amount and duration; there is no local code
issuance or first-period restriction.

The monthly fulfillment path reads and validates the paid Stripe
invoice, records its actual paid amount, discount and customer invoice
balance evidence, and grants the full Pro entitlement for partial or
full discounts, including $0 invoices settled entirely by discounts
and/or customer balance without a PaymentIntent. Zero-amount grants
remain restricted to verified current-policy Pro subscription invoices.
Existing period-based fulfillment protects against duplicate
invoice/Checkout delivery. Financial audit events retain before/after
amounts, discounts, balance offsets and invoice/subscription identities,
including the actual prior row after a duplicate-insert race.

Topups, legacy payment flows and billing-gateway are unchanged. No new
environment variables, queries or scheduled jobs. Coupons and Promotion
Codes must be created in the intended Stripe account/environment.
Customer invoice balance supports partial/full offsets, surplus balance,
discount combinations and fully paid debit balances. Paid minimum-charge
deferrals are accepted only after a read-only Stripe query verifies the
unique invoice_too_small transaction for the same
invoice/customer/currency/environment. Deferred amounts and transaction
IDs are audited separately from discounts and balance consumption.
Cancellation does not trigger extra local collection: the debit stays in
Stripe for future applicable invoices, and may remain uncollected if no
further invoice is issued. Tax and current-invoice credit notes remain
outside the supported invoice contract.

## Test plan
- [x] 324 related unit tests passed, including full/partial/recurring
discounts, legacy/modern Stripe invoice shapes, $0 entitlement guards,
Checkout and invoice replay, cancellation periods, renewal, topup
isolation, customer balance reconciliation and durable financial audit
snapshots, small-amount carry-forward proof, rejected/ambiguous
evidence, pagination, query failures, cancellation and next-period
collection.
- [x] Backend pre-commit checks passed, including Ruff, Pyright, import
contracts, file size and complexity.
- [ ] Stripe Sandbox end-to-end acceptance: actual code redemption, $0
payment-method collection, customer balance offsets, minimum-charge
deferrals, renewal and cancellation. Not deployed by this PR.
```

来源：SerendipityOneInc/ecap-workspace @ 896730f7，PR #3891，作者 sam-srp。