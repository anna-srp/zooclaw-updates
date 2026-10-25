---
title: "垂直行业套餐统一改走 Stripe 结账，按账单周期自动给团队钱包发积分"
type: "新功能"
priority: "高"
date: "2026-10-12"
status: "待审核"
channels: ""
---

# 垂直行业套餐统一改走 Stripe 结账，按账单周期自动给团队钱包发积分

## 核心宣传点

所有垂直包（含 Restaurant）的购买能力统一返回 Stripe，下单走 Stripe Checkout。两个前端的结账页只保留一个 Card 按钮，移除了支付宝按钮与「Card 或 Alipay」文案，用户看到的支付入口变成单一刷卡。发放侧新增独立的企业支付处理：首付、续费、order_confirm 和对账兜底都按「已支付 Invoice」的明细周期给团队钱包发积分，幂等键沿用订阅加周期起止，同一期只发一次。金额校验与 Pro 对齐，订阅生命周期改由 Stripe 管理。

## 分级

- 内部：P0
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## 备注

同一购买人已有另一个未终止的 current 订阅时，结算层抛 billing.overlapping_subscription 转人工，不发权益也不取消 Stripe 订阅；下单层防重复见 #4060。对 Stripe 订阅禁止套餐变更接口，需运营知悉。取代未合并的 #4056。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `b971edece751235d024374d86b41ba38f81abcf2`
- PR: #4061
- 作者：tim-srp
- 日期：2026-10-12T15:19:25Z

### Commit Message

```
fix(billing): switch vertical packs to Stripe with invoice-period settlement (#4061)

## Summary

取代 #4056（不合并）。#4056 的路由改动（`af644cb87`）保留原作者身份 cherry-pick 进来，并按 #4056
的评审补齐业务逻辑。设计见
`docs/superpowers/specs/2026-10-12-vertical-pack-stripe-settlement.md`。

- **支付入口**：所有垂直包（含 Restaurant）的 purchase-capability 都返回 Stripe，下单走
Stripe Checkout。两个前端（`web/app`、`web/enterprise-admin`）的结账页都只保留一个 Card
按钮：移除 Alipay 按钮、Alipay 处理函数和「Card 或 Alipay」文案。
-
**发放**：企业包的首付（`checkout.session.completed`）、续费（`invoice.paid`）、`order_confirm`
和 reconcile 兜底，都分流到新的 `stripe/enterprise_payment.py`。按「已支付
Invoice」的明细周期给团队钱包发积分，幂等键沿用 `(subscription, period_start,
period_end)`，同一期只发一次。
- **金额校验对齐 Pro**：复用
`monthly_invoice._validate_amounts`，目录价换成套餐快照总价（新增带默认值的 `price_cents`
参数，Pro 调用点不变）。另外逐行核对：
  - base + addon 的 price 与金额；
  - 订阅归属、非 proration、数量为 1；
  - 各行周期一致。

  明细超过一页时拉取全量。
- **重复订阅（结算层，对齐 Pro `_record_agreement`）**：同一购买人已有另一个未终止的 current 订阅时，抛
`billing.overlapping_subscription` 转人工。不发权益，也不取消任何 Stripe 订阅。下单 /
Checkout 层的防重复另见 #4060。
- **生命周期由 Stripe 管理**：企业 agreement 收到
`customer.subscription.updated/deleted` 时，重新 retrieve 最新订阅再投影（与 Pro
一致）。写入时带上 `team_id / subscription_kind / enterprise_package_id`。
- **禁止 Stripe 套餐变更**：`POST /subscription/enterprise-package/change` 对
Stripe
订阅直接拒绝（`billing_v2.enterprise_package.change.unsupported_provider`），在调用
Stripe、写订单之前返回。否则 Stripe 会按新价格扣款，结算却按原套餐快照拒绝这张账单（Codex review）。Antom 不变。

## Root cause

- Restaurant plan 的 capability / provider 被改写到 Airwallex（#4056 已修，本 PR
沿用）。
- 企业包付款走 legacy 写入，带来两个问题（#4056 评审 P1-3）：
- 发放周期取的是 Stripe Subscription
的当前周期（`subscription_period_start/end`），不是这张已支付 Invoice
的周期。账单迟到或乱序时会记错期，或占用下一期的幂等键；
  - 金额只比对事件总额，不核对明细，也不识别 Stripe 折扣。
- 生命周期事件写企业 agreement 时没带团队身份字段，触发
`billing_v2.subscription_agreement.team_owner_conflict`，webhook 失败（#4056
评审 P1-2）。修复前，新增的 3 个企业用例都以这个错误失败。

## 部署前提

1. 每个垂直包 plan 的基础包和每个 addon，在当前 Stripe 账号里都要有可用的价格。staging（test mode）和
production（live mode）各确认一次。
- 不需要手动建：`POST /internal/vertical-pack-plans/{plan_id}` 会为缺少 id 的基础包 /
addon 自动创建 product 和按月 USD 价格。
- 下单时 `validate_stripe_prices_for_snapshot` 会逐条校验
active、USD、按月、product、金额，不通过就在付款前报错。
2. Stripe webhook（与 Pro 共用的 `/stripe/webhook`）订阅以下事件：
   - `checkout.session.completed`
   - `invoice.paid`
   - `invoice.payment_failed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
3. 前后端都要部署，建议先后端、后前端。

## 不在本 PR 范围 / 已知事项

- 下单 / Checkout 层防重复支付：见 #4060。
- 实付为 0 的企业包账单（100%
折扣、余额全额抵扣）会被明确拒绝（`billing.invoice_mismatch`），需要人工处理。Pro
有专门的零元发放门槛，这次没有扩展到企业包。
-
企业包退款（`charge.refunded`）：`billing_v2_refunds._record_refunded_subscription_loss`
仍是旧投影，对企业 agreement 同样会触发 `team_owner_conflict`。这不在本次「购买 → 发放 →
续费」范围内，确认后另行修复。
- `invoice.payment_failed` 只解析旧版 payload 的
`invoice.subscription`。这是现有行为，Pro 也一样。新版 payload 下由
`customer.subscription.updated` 重新 retrieve 来同步 `past_due`。
- 套餐变更：Stripe 订阅不再允许变更，`change_enterprise_package` 中的 Stripe 分支（价格校验、修改
Stripe 订阅项）因此走不到。按「不做清理」保留，未删除。
- Airwallex 代码清理与重构：按要求这次不做。jscpd 报告 `enterprise_payment` ↔
`monthly_payment` 有两处小段重复（15 + 18 行）。app 重复率 1.47%（阈值 3%），tests 5.2%（阈值
7.5%）。

## Test plan

- [x] 新增单测
`test_stripe_enterprise_invoice.py`、`test_stripe_enterprise_payment.py`、`test_stripe_enterprise_lifecycle.py`，覆盖：
  - 两种事件顺序加重放，只发一次；
  - 迟到账单记 EXPIRED，下一期照常发放；
  - 明细分页；
  - price / 税 / proration / 跨订阅 / 零元都被拒；
  - 重叠订阅转人工，且不取消订阅；
  - 生命周期事件保留团队身份。
  - Stripe 套餐变更在任何副作用之前被拒绝（`test_enterprise_package_subscription.py`）。
- [x] 后端全量单测 `pytest tests/unit -n auto`：12003 passed, 5 skipped
- [x] `scripts/ci-lint` 01–08、jscpd、pre-push `verify-py` + `verify-web`
- [x] 前端：
- `web/app` 的 `verify-web.sh`（guards + tsc + billing 单测 + eslint）和 knip；
- `web/enterprise-admin` 全量单测（451 passed）和 lint，结账页测试断言只渲染 Card、没有
Alipay。
- [x] 无新的查询形态：只复用现有 repo 方法，没有新增 CSFLE 风险
- [ ] Staging（需先完成部署前提）：用 Stripe Test Clock 走一遍：
  1. 真实 Checkout 付款，首期发放；
  2. 推进时钟，续扣后发放下一期；
  3. 取消订阅。

  每一步都核对团队钱包和 agreement。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
Co-authored-by: bill-srp <bill@srp.one>
```

