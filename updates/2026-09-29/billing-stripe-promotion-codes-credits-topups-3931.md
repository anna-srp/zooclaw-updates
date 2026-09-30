---
title: "Credits 充值支持 Stripe 优惠码：折扣只影响实付金额，到账 credits 照原数给足"
type: "Feature"
priority: "高"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# Credits 充值支持 Stripe 优惠码：折扣只影响实付金额，到账 credits 照原数给足

## 核心宣传点

Credits 充值的结账流程现在接受 Stripe 优惠码，沿用 Pro 订阅优惠码那一套设计。优惠码的适用范围、折扣力度、兑换次数限制和适用商品全部由 Stripe 管理，本地不发码。折扣只降低实付金额，每一笔校验通过的充值都按订单里写定的 credits 数量全额入账；标价由服务端固定的 credits 数推算（credits / 2 分），绝不从 Stripe 返回值或可能已经结算过的订单金额里反推。入账前会逐项校验币种为美元、小计等于标价、折扣金额落在合理区间、税费与运费为零、实付等于标价减折扣；实付为正必须有支付意图，实付为零必须没有支付意图。如果支付成功事件先到且金额偏低，系统会回读订单对应的结账会话，要求支付意图一致且金额校验通过才入账，没打折或已结算的支付意图沿用原有处理路径。

## 分级

- 内部：P0
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Linear
<!-- none -->

## Summary
Credits topup Checkout now accepts Stripe promotion codes, following the Pro promotion-code design (#3891). Stripe owns code eligibility, discount, redemption limits and applicable products; there is no local issuance.

- A discount lowers only the amount paid; every verified topup grants the order's full `credits_amount`. The list price is derived from the server-fixed credits (`credits / 2` cents), never from Stripe or the (possibly already-settled) order amount.
- `checkout.session.completed`: verifies USD, `amount_subtotal == list`, `total_details.amount_discount` in `[0, list]`, zero tax/shipping and `amount_total == list - discount`. A positive total requires `paid` plus a PaymentIntent; a zero total requires no PaymentIntent.
- `payment_intent.succeeded` arriving first with a lower amount re-reads the order's Checkout Session and requires the same PaymentIntent and verified amount. Undiscounted or already-settled PaymentIntents keep the existing exact-amount check.
- `invoice.paid` attaches when `amount_paid + discounts == list`, with no tax or credit notes. The order must still carry the list price before settlement, or exactly the paid amount after.
- The payment order records the actual paid amount (including 0) and `provider_discount_amount_cents`; existing `payment_order.recorded` audit events carry before/after values of both.
- **100% codes are allowed.** The entitlement guard admits a zero amount for a topup only when it is a current-policy Stripe USD topup, Checkout-sourced, with a Session, no PaymentIntent and a discount equal to the list price. A $0 topup has no charge, so Stripe refunds cannot revoke its credits; reversal must use the audited manual compensation flow. Coupon product and redemption limits in Stripe are the control.
- API Platform accounts share the same topup Checkout, so they also see the promotion-code field.
- Legacy topups, subscriptions and billing-gateway are unchanged. No new env vars, DB queries or jobs.
- Spec: `docs/superpowers/specs/2026-09-29-stripe-topup-promotion-codes.md`; ops notes in `services/claw-interface/docs/stripe-credits-v1.md` (充值优惠码).

## Test plan
- [x] New `tests/unit/test_stripe_topup_promotion_codes.py` (58 cases): partial/full discount Sessions, malformed or mismatched Sessions, PaymentIntent-first discounted delivery, invoice attachment before/after settlement, zero-amount guard not relaxing other orders, full-credit grant for $0 without a payment lookup.
- [x] Billing, Stripe, order, credit and Feishu unit suites locally (3363 passed).
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, import-linter) and ci-lint guards (file length, complexity, dead code).
- [ ] Stripe Sandbox acceptance: partial and 100% codes, real Session/invoice shape for $0 payment mode, webhook ordering. Not covered by unit tests.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `dbf7ef485ee9e350558df676fa7202076bc3e7c6`
- PR: #3931
- 作者：tim-srp
- 日期：2026-09-29T12:00:32Z

### Commit Message

```
feat(billing): support Stripe promotion codes for credits topups (#3931)

## Linear
<!-- none -->

## Summary
Credits topup Checkout now accepts Stripe promotion codes, following the
Pro promotion-code design (#3891). Stripe owns code eligibility,
discount, redemption limits and applicable products; there is no local
issuance.

- A discount lowers only the amount paid; every verified topup grants
the order's full `credits_amount`. The list price is derived from the
server-fixed credits (`credits / 2` cents), never from Stripe or the
(possibly already-settled) order amount.
- `checkout.session.completed`: verifies USD, `amount_subtotal == list`,
`total_details.amount_discount` in `[0, list]`, zero tax/shipping and
`amount_total == list - discount`. A positive total requires `paid` plus
a PaymentIntent; a zero total requires no PaymentIntent.
- `payment_intent.succeeded` arriving first with a lower amount re-reads
the order's Checkout Session and requires the same PaymentIntent and
verified amount. Undiscounted or already-settled PaymentIntents keep the
existing exact-amount check.
- `invoice.paid` attaches when `amount_paid + discounts == list`, with
no tax or credit notes. The order must still carry the list price before
settlement, or exactly the paid amount after.
- The payment order records the actual paid amount (including 0) and
`provider_discount_amount_cents`; existing `payment_order.recorded`
audit events carry before/after values of both.
- **100% codes are allowed.** The entitlement guard admits a zero amount
for a topup only when it is a current-policy Stripe USD topup,
Checkout-sourced, with a Session, no PaymentIntent and a discount equal
to the list price. A $0 topup has no charge, so Stripe refunds cannot
revoke its credits; reversal must use the audited manual compensation
flow. Coupon product and redemption limits in Stripe are the control.
- API Platform accounts share the same topup Checkout, so they also see
the promotion-code field.
- Legacy topups, subscriptions and billing-gateway are unchanged. No new
env vars, DB queries or jobs.
- Spec:
`docs/superpowers/specs/2026-09-29-stripe-topup-promotion-codes.md`; ops
notes in `services/claw-interface/docs/stripe-credits-v1.md` (充值优惠码).

## Test plan
- [x] New `tests/unit/test_stripe_topup_promotion_codes.py` (58 cases):
partial/full discount Sessions, malformed or mismatched Sessions,
PaymentIntent-first discounted delivery, invoice attachment before/after
settlement, zero-amount guard not relaxing other orders, full-credit
grant for $0 without a payment lookup.
- [x] Billing, Stripe, order, credit and Feishu unit suites locally
(3363 passed).
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, import-linter)
and ci-lint guards (file length, complexity, dead code).
- [ ] Stripe Sandbox acceptance: partial and 100% codes, real
Session/invoice shape for $0 payment mode, webhook ordering. Not covered
by unit tests.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

来源：SerendipityOneInc/ecap-workspace @ dbf7ef48，PR #3931，作者 tim-srp。
