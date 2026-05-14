---
title: "修复账单发票下载异常及积分显示不一致问题"
type: "Bug Fix"
priority: "高"
date: "2026-05-13"
status: "待审核"
channels: "Discord + changelog"
---

# 修复账单发票下载异常及积分显示不一致问题

## 核心宣传点

两个困扰用户的账单问题已修复：点击某张发票的下载按钮不再跳转到错误金额的发票；订阅后左右两侧积分数字现在保持一致。

## 原始内容

**来源**: ecap-workspace PR #1616 | SHA: bd058e20

**Commit Message**:
```
fix(billing): per-invoice download + Stripe customer reuse + credit-sync wallet sum (ECA-669) (#1616)

Half 1 — invoice download "点 24$ 显示 100$"

Two compounding defects:
1. Stripe customer not reused across checkouts — create-checkout-session/route.ts
   never passed customer= to stripe.checkout.sessions.create, so Stripe spawned a
   fresh customer object on every paid checkout. The checkout.session.completed webhook
   then overwrote user.stripe_customer_id with the newest one, orphaning previous
   customer (and all its invoices).
2. Download button had no per-invoice scope — each row in InvoiceHistory.tsx called
   the same no-arg openCustomerPortal(), which mounts Stripe Billing Portal against
   account.stripe_customer_id. Historical orphan invoices were unreachable regardless
   of which row was clicked.

Prod audit: 71 paid Stripe orders missing stripe_invoice_id (63 sub + 8 topup);
17 of those are orphan across 9 users (~$749).

Half 2 — credit-sync "订阅后左右积分不一致"

Root cause: this user has two active subscription wallets in BG (legacy duplicate).
check_user_credits iterated wallets and assigned balances per match, so the duplicate
overwrote the previous result and subscription_credits + topup_credits no longer agreed
with BG's own available_credits.

Fix: sum across non-terminated wallets of each kind. Defensive — keeps the display
consistent regardless of how many duplicate wallets BG carries.
```

**PR #1616 Description**:
```
Closes both halves of ECA-669:

Half 1: Stripe customer now reused across checkouts. Per-invoice download button
now correctly scoped to individual invoice via invoice_id param.

Half 2: credit-sync fixed by summing across all non-terminated wallets of each kind
instead of overwriting with the last match.

Prod audit confirmed: 71 paid Stripe orders missing stripe_invoice_id; 17 orphan
across 9 users (~$749). All resolvable via existing checkout_session_id.
```
