---
title: "支付宝/Antom 支付渠道全面强化上线"
type: "产品基础功能更新"
priority: "高"
date: "2026-05-13"
status: "待审核"
channels: "Discord + changelog"
---

# 支付宝/Antom 支付渠道全面强化上线

## 核心宣传点

ZooClaw 的支付宝充值和订阅体验更可靠了：支付金额由系统数据库权威校验（防篡改），退款自动撤回已发放积分，整体支付流程更加安全稳健。

## 原始内容

**来源**: ecap-workspace PR #1592 | SHA: 7ec66da8

**Commit Message**:
```
feat: harden Antom Alipay payment integration (#1592)

- Integrate Antom/Alipay as a provider-aware payment path alongside Stripe.
- Harden Antom Cashier one-time payment creation with DB-authoritative amount/currency,
  redirect URL allowlisting, and signed API response verification.
- Add official Subscription Payment create/cancel plumbing for when Antom enables
  the product on the merchant account.
- Make webhook/recovery fulfillment idempotent across success/failure/cancel paths.
- Add refund compensation that refunds through Antom and voids previously granted
  Billing Gateway credits with deterministic revoke transaction IDs.
- Treat refunded/compensating order states as non-success on the frontend payment success page.
- Document the rollout plan and current Subscription Payment activation gate.

Sandbox Notes:
- Cashier top-up path was tested end-to-end in sandbox through Antom redirect,
  inquiry/webhook recovery, order paid, and credits grant.
- Compensation was tested against sandbox refund plus Billing Gateway credit void replay behavior.
```

**PR #1592 Description**:
```
Summary:
- Integrate Antom/Alipay as a provider-aware payment path alongside Stripe.
- Harden Antom Cashier one-time payment creation with DB-authoritative amount/currency,
  redirect URL allowlisting, and signed API response verification.
- Add official Subscription Payment create/cancel plumbing.
- Make webhook/recovery fulfillment idempotent across success/failure/cancel paths.
- Add refund compensation that refunds through Antom and voids previously granted
  Billing Gateway credits with deterministic revoke transaction IDs.
- Treat refunded/compensating order states as non-success on the frontend payment success page.

Verification:
- Python pre-commit hooks: passed
- Targeted backend pytest: 68 passed
- Targeted pyright: 0 errors
- Cashier top-up path tested end-to-end in sandbox.
```
