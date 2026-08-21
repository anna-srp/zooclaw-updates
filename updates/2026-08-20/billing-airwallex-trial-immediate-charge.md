---
title: "修复：信用卡免费试用不再被立即扣费"
type: "Bug Fix"
priority: "高"
date: "2026-08-20"
status: "待审核"
channels: ""
---

# 修复：信用卡免费试用不再被立即扣费

## 核心宣传点

此前通过信用卡开启年度 Starter 免费试用时，Airwallex 侧会立刻扣掉全年 200 美元——用户既被扣费又拿到了试用额度。现在创建试用订单时会明确声明 7 天试用窗口（与其他支付渠道一致），试用期内不再产生任何扣费。已被误扣的订单会单独人工退款处理。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `2489fd13c080f809d7b5c9dc66cc52e0c54ca75a`
- PR: #3450
- 作者: tim-srp
- 日期: 2026-08-20T02:35:46Z

### Commit Message

```
fix(billing): declare trial window on Airwallex trial checkout creation (#3450)

## Problem

生产环境通过 free trial 订阅年度 Starter，Airwallex 端**立即扣费 200 USD**（预期 trial
不应扣费）。Issue: #3448

## Root cause

`create_card_checkout` 创建 Airwallex Billing Checkout 时只传了 trial 价格
id（`pri_uspd5s6n8hlgn9vy366`），没有把 trial 窗口传给 provider：

```python
subscription_data=AirwallexSubscriptionData(duration=_subscription_duration(intent.billing_cycle))
```

Airwallex 的 trial 语义完全由 checkout
请求决定（`subscription_data.trial_ends_at`），trial 价格本身只是一个普通的 200
USD/年预付费价格。因此订阅创建后直接进入付费周期并扣费。

生产环境证据（uid 7495857210153504768）：
- checkout `bco_uspdfkhxhhlhq51leki`：`subscription_data` 无
`trial_ends_at`
- subscription `sub_uspd67vdnhlhq5qk662`：`duration: {period: 0,
period_unit: "DAY"}`
- invoice `inv_uspd67vdnhlhq5qkx6c`：`total_amount:
200.0`，`payment_status: PAID`

业务层随后凭本地 `order.is_trial` 把订阅投影为 trialing 并发放 1000 trial credits，造成「被扣费
+ 拿到 trial credits」的双重伤害。

Design spec `2026-08-18-airwallex-subscription-channel-design.md` 第 190
行明确要求创建请求带 `trial_ends_at`，这是实现遗漏。

## Fix

当 intent 是 Starter trial 时，在 checkout 创建请求中声明 provider-managed trial
窗口（`now + AIRWALLEX_TRIAL_DURATION_DAYS`，7 天，与 Stripe/Antom trial 时长一致）：

```python
subscription_data = AirwallexSubscriptionData(
    trial_ends_at=trial_ends_at,
    duration=_subscription_duration(intent.billing_cycle),
)
```

新增设置 `AIRWALLEX_TRIAL_DURATION_DAYS =
7`（`app/schema/airwallex_settings.py`）。

非 trial 路径不变（`trial_ends_at` 为 `None`）。升级路径不受影响（trial 资格校验强制
`new_subscription` intent）。

## Tests

- `test_trial_checkout_uses_server_selected_trial_product`：新增断言 trial
checkout 请求携带 `trial_ends_at == now + 7 days`（patch `time.time` 固定时间）
- 非 trial 主路径新增断言 `trial_ends_at is None`
- 全套 Airwallex + card checkout 测试 449 passed

## 后续（不在本 PR 范围）

- #3448 中已扣费的订单需要人工退款处理
- 上线后需在 staging/production 各验证一次 trial checkout 全流程（sandbox 优先）

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Problem

生产环境通过 free trial 订阅年度 Starter，Airwallex 端**立即扣费 200 USD**（预期 trial 不应扣费）。Issue: #3448

## Root cause

`create_card_checkout` 创建 Airwallex Billing Checkout 时只传了 trial 价格 id（`pri_uspd5s6n8hlgn9vy366`），没有把 trial 窗口传给 provider：

```python
subscription_data=AirwallexSubscriptionData(duration=_subscription_duration(intent.billing_cycle))
```

Airwallex 的 trial 语义完全由 checkout 请求决定（`subscription_data.trial_ends_at`），trial 价格本身只是一个普通的 200 USD/年预付费价格。因此订阅创建后直接进入付费周期并扣费。

生产环境证据（uid 7495857210153504768）：
- checkout `bco_uspdfkhxhhlhq51leki`：`subscription_data` 无 `trial_ends_at`
- subscription `sub_uspd67vdnhlhq5qk662`：`duration: {period: 0, period_unit: "DAY"}`
- invoice `inv_uspd67vdnhlhq5qkx6c`：`total_amount: 200.0`，`payment_status: PAID`

业务层随后凭本地 `order.is_trial` 把订阅投影为 trialing 并发放 1000 trial credits，造成「被扣费 + 拿到 trial credits」的双重伤害。

Design spec `2026-08-18-airwallex-subscription-channel-design.md` 第 190 行明确要求创建请求带 `trial_ends_at`，这是实现遗漏。

## Fix

当 intent 是 Starter trial 时，在 checkout 创建请求中声明 provider-managed trial 窗口（`now + AIRWALLEX_TRIAL_DURATION_DAYS`，7 天，与 Stripe/Antom trial 时长一致）：

```python
subscription_data = AirwallexSubscriptionData(
    trial_ends_at=trial_ends_at,
    duration=_subscription_duration(intent.billing_cycle),
)
```

新增设置 `AIRWALLEX_TRIAL_DURATION_DAYS = 7`（`app/schema/airwallex_settings.py`）。

非 trial 路径不变（`trial_ends_at` 为 `None`）。升级路径不受影响（trial 资格校验强制 `new_subscription` intent）。

## Tests

- `test_trial_checkout_uses_server_selected_trial_product`：新增断言 trial checkout 请求携带 `trial_ends_at == now + 7 days`（patch `time.time` 固定时间）
- 非 trial 主路径新增断言 `trial_ends_at is None`
- 全套 Airwallex + card checkout 测试 449 passed

## 后续（不在本 PR 范围）

- #3448 中已扣费的订单需要人工退款处理
- 上线后需在 staging/production 各验证一次 trial checkout 全流程（sandbox 优先）


