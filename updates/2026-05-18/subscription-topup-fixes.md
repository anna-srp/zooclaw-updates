---
title: "充值/订阅 Bug 修复：Alipay 支付选项恢复 + 防止双重订阅"
type: "Bug Fix"
priority: "高"
date: "2026-05-18"
status: "待审核"
channels: ""
---
# 充值/订阅 Bug 修复：Alipay 支付选项恢复 + 防止双重订阅

## 核心宣传点
修复了 Stripe 订阅用户充值 Token 时 Alipay 选项被灰掉的问题，同时修复了 Apple 取消订阅用户误操作后可能产生双重订阅的安全漏洞。

## 原始内容

**Commit**: `7df6a686` | ecap-workspace | 2026-05-18T11:26:46Z  
**PR**: #1727 | fix(subscription): decouple topup modal + apple renew + backend gate

---

Three coupled gating bugs in the billing/topup flow, surfaced from one user report (Stripe subscriber wanted Alipay topup, the button was unclickable):

1. **PaymentMethodModal cross-flow leak** — 对于 Stripe 订阅用户点击"购买 Token"，Alipay 支付选项被错误地灰掉了。Fix: gate disable rules on `Boolean(paymentMethodPending)` so the topup path leaves both methods open.

2. **Apple Renew bypass** — Apple 取消订阅但当期仍有效的用户，点击续费按钮 → PaymentMethodModal 开启 → Stripe 可点击 → 在 Apple 订阅之上叠加了一个 Stripe 订阅。Fix: mirror the App Store toast.

3. **Backend topup gate** — 前端 `topupEnabled = userStatus === 'active'` 在 UI 层拦截了充值，但 `POST /orders/create` 接受任何用户，前端校验可被绕过。Fix: 后端也做同等校验，不满足时返回 403。
