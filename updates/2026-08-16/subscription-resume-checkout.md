---
title: "订阅支付页关掉也能回去付：新增「重新打开支付页面」按钮"
type: 体验优化
priority: 高
date: 2026-08-16
status: "待审核"
channels: ""
---

## 核心宣传点

以前不小心关掉订阅支付页，就得干等一小时才能再付款。现在错误提示旁多了一个「重新打开支付页面」按钮，一键回到原来的支付页面继续完成付款，Stripe / Creem / Antom 三种支付方式都支持；同时等待时间也从 60 分钟缩短到 45 分钟。

## 原始内容

commit: 7a8b03bee9 (SerendipityOneInc/ecap-workspace, PR #3402, tim-srp, 2026-08-16T01:54:43Z)

```
feat(billing): 允许重新打开进行中的订阅支付页（解决 1 小时锁定后无法再支付） (#3402)
```

### PR body

## 问题

用户从订阅页进入支付页（如 Stripe 托管页）后**关闭页面**，之后 1 小时内无法再次点击支付：

- 订阅支付有 **1 小时独占租约**（`SUBSCRIPTION_CHECKOUT_LEASE_SECONDS = 3600`，防并发/重复支付，PR #3062 引入）
- 用户关掉支付页后租约**不释放**，Stripe session 依然有效（`expires_at` = 租约到期时间）
- 前端每次点击都**新建订单**（新 order_id），1 小时内再次发起会被 `billing_v2.order_request.checkout_in_progress` 409 拒绝，只能干等 1 小时

## 方案

在错误提示旁新增 **"重新打开支付页面"** 按钮，把用户带回**原订单的支付页**（租约到期前原 session 仍有效，可正常完成支付）。不做任何绕过租约的操作，仅恢复访问。

### 后端（claw-interface）
- 新增 `GET /orders/active-checkout`：读取租约 owner（被锁订单）→ 返回其当前有效的 provider 支付 URL
  - Stripe：通过订单上已关联的 `provider_checkout_session_id` 重新取 session URL
  - Creem：直接返回订单上存储的 `provider_checkout_url`
  - 无租约 / 订单非 pending 时返回 404
- 新增 service `get_active_subscription_checkout` + 6 个单元测试

### BFF
- `create-checkout-session` 透传后端错误 `code`（`checkout_in_progress`），前端不再靠匹配错误文案判断

### 前端
- `useCheckoutFlow` 新增 `canResumeCheckout` + `resumeCheckout`（重新打开 popup 并导航到原支付页）
- `SubscriptionPanel` 错误红条旁渲染按钮（i18n：en/zh）
- 新增 `getActiveCheckout()` 服务

## 测试
- 后端 service 单测：`test_billing_v2_order_requests.py`（6 个新用例，全部通过）
- BFF：code 透传测试 + 原有 22 个用例通过
- 前端：SubscriptionPanel（94）、Paywall（12）等套件通过
- eslint 干净

## 备注
- 该租约是防并发/重复支付的**有意设计**，本 PR 不修改租约语义（一次只能有一个进行中的订阅 checkout），只让用户能回到原支付页完成支付
- **租约时长 1 小时 → 45 分钟**：与 Antom 授权 URL 的 45 分钟过期时间对齐，避免在 45-60 分钟窗口内返回已失效的恢复链接（同时缩短了误关页面的等待时间）
- Stripe / Creem / Antom 三个渠道均支持恢复；Antom 恢复时后端校验授权 URL 是否在 `antom_subscription_expiry_time` 内（过期则返回 404、前端不显示按钮）
