---
title: "垂直套餐结账接入 Stripe 托管支付并支持优惠码，支付方式更多但会加收价外税"
type: "后端功能"
priority: "高"
date: "2026-10-13"
status: "待审核"
channels: ""
---

# 垂直套餐结账接入 Stripe 托管支付并支持优惠码，支付方式更多但会加收价外税

## 核心宣传点

延续上一步的 Stripe 改造，垂直包结账会话跟随 STRIPE_MANAGED_PAYMENTS_ENABLED 开关（与 Pro 共用，不新增配置）：开启时使用托管支付、不再限定支付方式；未开启时与现状一致仍是刷卡。两种情况都允许在结账页使用优惠码。下单时会把是否托管支付写进支付订单并进入审计，保证订单与实际发给 Stripe 的参数一致；开启托管支付时会在调用 Stripe 前校验每个行项目必须为价外税。只改后端，无前端改动。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## 备注

上线后行为变化需提前告知客户：标价之上会按账单地址加收价外税并由 Stripe 代缴；账单地址在中国、俄罗斯、伊朗等受限国家的客户无法线上付款；企业客户无法在结账页填写税号；支付方式由 Stripe 决定不再限定为卡；非美客户可能看到本地货币报价，换汇费 2–4% 由客户承担。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `c32b13fc4319fffce27a3c0e97986c2f5c38bea4`
- PR: #4069
- 作者：tim-srp
- 日期：2026-10-13T11:08:28Z

### Commit Message

```
feat(billing): sell vertical packs through Stripe Managed Payments with promotion codes (#4069)

## Summary

延续 #4061。设计见
`docs/superpowers/specs/2026-10-13-vertical-pack-managed-payments-promo.md`。只改后端
`services/claw-interface`，没有前端改动。

- **托管支付**：垂直包的 Stripe 结账跟随 `STRIPE_MANAGED_PAYMENTS_ENABLED`（与 Pro
共用，不新增配置）。
- 启用时：会话带 `managed_payments[enabled]=true`，不带
`payment_method_types`，使用托管 API 版本 `2026-04-22.dahlia`。
  - 未启用时：与现状一致，仍是 card，使用 SDK 默认版本。
- **优惠码**：两种情况下会话都带 `allow_promotion_codes=true`。
- **订单与审计**：下单时把 `checkout_managed_payments`
写进支付订单，会话参数从已记录的订单读取，所以订单和实际发给 Stripe
的参数不会不一致。这个字段已在审计的支付事实里，`payment_order.recorded` 审计事件会带上它。Antom
订单不写这个字段。
- **下单前校验**：启用托管支付时，每个行项目的 Stripe 价格必须是
`tax_behavior=exclusive`。否则在记录订单、调用 Stripe 之前返回
`billing_v2.enterprise_package.stripe_price_tax_behavior_invalid`。
- **新建包自动满足条件**：Console 建包时创建的 Stripe 产品带税码 `txcd_10105002`，价格带
`tax_behavior=exclusive`。基础包、addon、改价后新建的价格都适用。
- **结算**：不改代码，只补测试。现有的 `_validate_amounts` 已支持「折扣 + 价外税」，是否允许税以 Stripe
返回的订阅是否为托管订阅为准。

## 上线后的行为变化

- 客户在标价之上被加税（价外），税额由 Stripe 按账单地址计算并代缴。
- 账单地址在受限国家（中国、俄罗斯、伊朗等）的客户无法线上付款。
- 企业客户不能在结账页填写税号。
- 支付方式由 Stripe 决定，不再限定为卡。测试模式下同一个会话展示的是 card 和 Cash App。
- 非美国客户可能看到本地货币报价（托管支付强制开启 Adaptive Pricing）。选择本地货币付款时，汇率里含 2–4%
的换汇费，由客户承担。Stripe 文档确认会话和 PaymentIntent 上的金额、币种始终是美元，结算里 `currency ==
"usd"` 的规则不受影响。
- 付款页出现优惠码输入框。账号里任何适用于该产品的有效优惠码都可以使用。
- Stripe 可以在购买后 60 天内主动退款。

## 部署前提

- 不新增环境变量。`STRIPE_MANAGED_PAYMENTS_ENABLED` 在 staging 和 production 都已是
`true`，**后端部署后立即生效**。这个开关与 Pro 共用，不能单独关；需要回退时回滚部署。
- 只需要发布 `services/claw-interface`。
- 生产上唯一线上售卖的餐厅包已满足条件（2026-10-13 只读核对）：只有基础行项目，价格
`tax_behavior=exclusive`，产品税码 `txcd_10105002`。
- 运营：给垂直包发优惠码时，新建 coupon 并限定到对应产品（餐厅包是 `prod_VQbQ8eIXIyCWUD`），折扣不能是
100%。生产现有 448 个有效优惠码中，447 个限定了产品；1 个不限产品（减 $24.99，一次性），上线后可用于垂直包。

## 不在本 PR 范围 / 已知事项

- **退款**（按确认另开 PR）：
- 企业包 `charge.refunded` 仍会报
`billing_v2.subscription_agreement.team_owner_conflict`；
- agreement 已是 `canceled` 时再退款，会报非法状态转换 `canceled -> revoked`（Pro 同样存在）。

  托管支付会让 Stripe 侧发起的退款更常见。修复上线前，企业包退款需要人工处理。
- **100% 折扣码（待决定，Codex 评审 P1）**：如果适用于垂直包产品，代码不拦截，目前只能靠运营不发全额码来避免。后果分两期：
- 首期：0 元账单结算被拒（`billing.invoice_mismatch`），不写订单、不建
agreement、不发权益。webhook 报错，Stripe 会重试。
- 下一期：Stripe 里的订阅仍然有效。如果优惠码只减首月，Stripe 按原价扣款。后端找不到这张账单对应的订单和
agreement，webhook 返回未处理；对账任务只遍历本地已有的
agreement，同样发现不了。结果是客户被扣款，后端不报错也不发权益。

所以首期报错后必须人工取消 Stripe
订阅或线下补发。是否在发布生产前加「零元首期自动取消订阅并留审计」，或改为支持零元首期发放，需要确认。本 PR 没有改这部分。
- **已有的包不回填**。在本次改动之前创建、之后要线上售卖的包，需要在 Stripe 后台做两件事：给产品补税码；把价格的
`tax_behavior` 从 unspecified 设为 exclusive。实测托管会话不会回落到账号的默认税码，产品上必须显式有税码。
- 通用内部接口 `POST /internal/stripe/products`、`POST /internal/stripe/prices`
没有改。本仓库的前端没有调用方。通过它们创建的价格不带 `tax_behavior`，托管结账时会被新的校验拦下。
- Agent 商店订阅的 Stripe
结账（`pack_store/ecap_pack_subscription_service.py`）是另一条流程，没有改，仍是普通支付。
- `account.stripe_customer_id` 如果是旧 Stripe 账号遗留的客户
ID，创建会话会失败。这是现有问题，生产上只有 29 个账号带这个字段。

## Test plan

- [x] 新增 `test_enterprise_package_managed_checkout.py`。只对 Stripe、Mongo
仓储和归属查询打桩，价格校验、订单构造、审计构造都跑真实代码：
  - 启用时会话是托管的，不带 `payment_method_types`，使用托管 API 版本；
  - 未启用时仍是 card；
  - 两种情况都带优惠码；
  - 落库的订单和审计事件都带 `checkout_managed_payments`，Antom 订单不带；
  - addon 的价格不是 exclusive 时，在记录订单和创建会话之前被拒；未启用时不校验。
- [x]
`test_vertical_pack_plan_service.py`、`test_stripe_client.py`：基础包、addon、改价三条路径都带税码和
`tax_behavior=exclusive`。
- [x] `test_stripe_enterprise_payment.py` 补结算测试：
  - 托管订阅的多行账单在「部分折扣 + 价外税」下通过，订单记录折扣和税额，发放的积分不变；
  - Stripe 没有标记为托管订阅时，带税账单不写任何记录；
  - 被优惠码全额抵扣的账单不写任何记录。
- [x] 变异检查：有 6 个测试属于「保持现状」或「只补测试」，不改代码就会通过。对每一个都临时改错实现，确认测试会失败。共 10
处改错，全部被发现。
- [x] 后端全量单测 `pytest tests/unit -n auto`：11996 passed, 5 skipped
- [x] `scripts/verify-py.sh`、`scripts/ci-lint` 01–08、jscpd（app
1.46%，tests 5.09%）、pre-commit、pre-push
- [x] 无新的查询形态：只复用现有 repo 方法，没有新增 CSFLE 风险
- [x] 接口级验证（staging 的 Stripe 测试账号，直接运行本次的建包和建会话代码，未经过后端部署）：
  - 建包代码创建的产品带 `tax_code=txcd_10105002`，价格是 `tax_behavior=exclusive`；
  - 真实的 Stripe 价格对象通过托管模式的价格校验，旧式资源（无税码、`unspecified`）被校验拦下；
- Stripe
接受托管会话：`managed_payments.enabled=true`、`allow_promotion_codes=true`、两个行项目、使用
`customer_email`；
  - 绕过校验、用无税码的产品创建托管会话，Stripe 拒绝（`the product tax code is missing`）。

  测试中创建的会话已置为过期，产品和价格已归档。
- [ ] Staging E2E（需先部署本 PR）。上面的接口级验证没有覆盖付款和结算，第 3
步是「真实的托管账单能通过结算」的首次端到端验证，**发布生产前必须完成**：
  1. 在 Console 新建测试包，确认 Stripe 里的产品带税码、价格是 exclusive；
  2. 从结账页下单，确认会话启用了托管支付，付款页能输入优惠码并显示税额；
  3. 用一个部分折扣的测试优惠码付款，核对支付订单的折扣和税额、entitlement、团队钱包只发一次；
  4. 用 Test Clock 推进到下一期，核对续费账单结算；
  5. 通过产品接口取消，核对 agreement 投影。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

