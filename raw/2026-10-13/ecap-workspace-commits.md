# SerendipityOneInc/ecap-workspace — commits 2026-10-13

## feat(billing): sell vertical packs through Stripe Managed Payments with promotion codes (#4069)

- **SHA**: `c32b13fc4319fffce27a3c0e97986c2f5c38bea4`
- **作者**: tim-srp
- **日期**: 2026-10-13T11:08:28Z
- **PR**: #4069

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

### PR Body

## Summary

延续 #4061。设计见 `docs/superpowers/specs/2026-10-13-vertical-pack-managed-payments-promo.md`。只改后端 `services/claw-interface`，没有前端改动。

- **托管支付**：垂直包的 Stripe 结账跟随 `STRIPE_MANAGED_PAYMENTS_ENABLED`（与 Pro 共用，不新增配置）。
  - 启用时：会话带 `managed_payments[enabled]=true`，不带 `payment_method_types`，使用托管 API 版本 `2026-04-22.dahlia`。
  - 未启用时：与现状一致，仍是 card，使用 SDK 默认版本。
- **优惠码**：两种情况下会话都带 `allow_promotion_codes=true`。
- **订单与审计**：下单时把 `checkout_managed_payments` 写进支付订单，会话参数从已记录的订单读取，所以订单和实际发给 Stripe 的参数不会不一致。这个字段已在审计的支付事实里，`payment_order.recorded` 审计事件会带上它。Antom 订单不写这个字段。
- **下单前校验**：启用托管支付时，每个行项目的 Stripe 价格必须是 `tax_behavior=exclusive`。否则在记录订单、调用 Stripe 之前返回 `billing_v2.enterprise_package.stripe_price_tax_behavior_invalid`。
- **新建包自动满足条件**：Console 建包时创建的 Stripe 产品带税码 `txcd_10105002`，价格带 `tax_behavior=exclusive`。基础包、addon、改价后新建的价格都适用。
- **结算**：不改代码，只补测试。现有的 `_validate_amounts` 已支持「折扣 + 价外税」，是否允许税以 Stripe 返回的订阅是否为托管订阅为准。

## 上线后的行为变化

- 客户在标价之上被加税（价外），税额由 Stripe 按账单地址计算并代缴。
- 账单地址在受限国家（中国、俄罗斯、伊朗等）的客户无法线上付款。
- 企业客户不能在结账页填写税号。
- 支付方式由 Stripe 决定，不再限定为卡。测试模式下同一个会话展示的是 card 和 Cash App。
- 非美国客户可能看到本地货币报价（托管支付强制开启 Adaptive Pricing）。选择本地货币付款时，汇率里含 2–4% 的换汇费，由客户承担。Stripe 文档确认会话和 PaymentIntent 上的金额、币种始终是美元，结算里 `currency == "usd"` 的规则不受影响。
- 付款页出现优惠码输入框。账号里任何适用于该产品的有效优惠码都可以使用。
- Stripe 可以在购买后 60 天内主动退款。

## 部署前提

- 不新增环境变量。`STRIPE_MANAGED_PAYMENTS_ENABLED` 在 staging 和 production 都已是 `true`，**后端部署后立即生效**。这个开关与 Pro 共用，不能单独关；需要回退时回滚部署。
- 只需要发布 `services/claw-interface`。
- 生产上唯一线上售卖的餐厅包已满足条件（2026-10-13 只读核对）：只有基础行项目，价格 `tax_behavior=exclusive`，产品税码 `txcd_10105002`。
- 运营：给垂直包发优惠码时，新建 coupon 并限定到对应产品（餐厅包是 `prod_VQbQ8eIXIyCWUD`），折扣不能是 100%。生产现有 448 个有效优惠码中，447 个限定了产品；1 个不限产品（减 $24.99，一次性），上线后可用于垂直包。

## 不在本 PR 范围 / 已知事项

- **退款**（按确认另开 PR）：
  - 企业包 `charge.refunded` 仍会报 `billing_v2.subscription_agreement.team_owner_conflict`；
  - agreement 已是 `canceled` 时再退款，会报非法状态转换 `canceled -> revoked`（Pro 同样存在）。

  托管支付会让 Stripe 侧发起的退款更常见。修复上线前，企业包退款需要人工处理。
- **100% 折扣码（待决定，Codex 评审 P1）**：如果适用于垂直包产品，代码不拦截，目前只能靠运营不发全额码来避免。后果分两期：
  - 首期：0 元账单结算被拒（`billing.invoice_mismatch`），不写订单、不建 agreement、不发权益。webhook 报错，Stripe 会重试。
  - 下一期：Stripe 里的订阅仍然有效。如果优惠码只减首月，Stripe 按原价扣款。后端找不到这张账单对应的订单和 agreement，webhook 返回未处理；对账任务只遍历本地已有的 agreement，同样发现不了。结果是客户被扣款，后端不报错也不发权益。

  所以首期报错后必须人工取消 Stripe 订阅或线下补发。是否在发布生产前加「零元首期自动取消订阅并留审计」，或改为支持零元首期发放，需要确认。本 PR 没有改这部分。
- **已有的包不回填**。在本次改动之前创建、之后要线上售卖的包，需要在 Stripe 后台做两件事：给产品补税码；把价格的 `tax_behavior` 从 unspecified 设为 exclusive。实测托管会话不会回落到账号的默认税码，产品上必须显式有税码。
- 通用内部接口 `POST /internal/stripe/products`、`POST /internal/stripe/prices` 没有改。本仓库的前端没有调用方。通过它们创建的价格不带 `tax_behavior`，托管结账时会被新的校验拦下。
- Agent 商店订阅的 Stripe 结账（`pack_store/ecap_pack_subscription_service.py`）是另一条流程，没有改，仍是普通支付。
- `account.stripe_customer_id` 如果是旧 Stripe 账号遗留的客户 ID，创建会话会失败。这是现有问题，生产上只有 29 个账号带这个字段。

## Test plan

- [x] 新增 `test_enterprise_package_managed_checkout.py`。只对 Stripe、Mongo 仓储和归属查询打桩，价格校验、订单构造、审计构造都跑真实代码：
  - 启用时会话是托管的，不带 `payment_method_types`，使用托管 API 版本；
  - 未启用时仍是 card；
  - 两种情况都带优惠码；
  - 落库的订单和审计事件都带 `checkout_managed_payments`，Antom 订单不带；
  - addon 的价格不是 exclusive 时，在记录订单和创建会话之前被拒；未启用时不校验。
- [x] `test_vertical_pack_plan_service.py`、`test_stripe_client.py`：基础包、addon、改价三条路径都带税码和 `tax_behavior=exclusive`。
- [x] `test_stripe_enterprise_payment.py` 补结算测试：
  - 托管订阅的多行账单在「部分折扣 + 价外税」下通过，订单记录折扣和税额，发放的积分不变；
  - Stripe 没有标记为托管订阅时，带税账单不写任何记录；
  - 被优惠码全额抵扣的账单不写任何记录。
- [x] 变异检查：有 6 个测试属于「保持现状」或「只补测试」，不改代码就会通过。对每一个都临时改错实现，确认测试会失败。共 10 处改错，全部被发现。
- [x] 后端全量单测 `pytest tests/unit -n auto`：11996 passed, 5 skipped
- [x] `scripts/verify-py.sh`、`scripts/ci-lint` 01–08、jscpd（app 1.46%，tests 5.09%）、pre-commit、pre-push
- [x] 无新的查询形态：只复用现有 repo 方法，没有新增 CSFLE 风险
- [x] 接口级验证（staging 的 Stripe 测试账号，直接运行本次的建包和建会话代码，未经过后端部署）：
  - 建包代码创建的产品带 `tax_code=txcd_10105002`，价格是 `tax_behavior=exclusive`；
  - 真实的 Stripe 价格对象通过托管模式的价格校验，旧式资源（无税码、`unspecified`）被校验拦下；
  - Stripe 接受托管会话：`managed_payments.enabled=true`、`allow_promotion_codes=true`、两个行项目、使用 `customer_email`；
  - 绕过校验、用无税码的产品创建托管会话，Stripe 拒绝（`the product tax code is missing`）。

  测试中创建的会话已置为过期，产品和价格已归档。
- [ ] Staging E2E（需先部署本 PR）。上面的接口级验证没有覆盖付款和结算，第 3 步是「真实的托管账单能通过结算」的首次端到端验证，**发布生产前必须完成**：
  1. 在 Console 新建测试包，确认 Stripe 里的产品带税码、价格是 exclusive；
  2. 从结账页下单，确认会话启用了托管支付，付款页能输入优惠码并显示税额；
  3. 用一个部分折扣的测试优惠码付款，核对支付订单的折扣和税额、entitlement、团队钱包只发一次；
  4. 用 Test Clock 推进到下一期，核对续费账单结算；
  5. 通过产品接口取消，核对 agreement 投影。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(design-system): 补齐共享与旧版按钮的鼠标焦点边框修复 (#4058)

- **SHA**: `bd39f2d9115172db122a5a3e015e514bd7d3052c`
- **作者**: lynn Zhuang
- **日期**: 2026-10-13T09:55:15Z
- **PR**: #4058

### Commit Message

```
fix(design-system): 补齐共享与旧版按钮的鼠标焦点边框修复 (#4058)

## 修复内容

修复鼠标关闭 Agent 切换菜单后，按钮仍残留深色焦点边框的问题，覆盖共享 Button、应用旧 Button 和 Paper Focus
暗色侧栏。保留 Tab 导航的可见焦点、outline 按钮原本的边框和校验失败提示。

同时修复审查指出的反向回归：通过 Tab 聚焦按钮后，点击调用 `preventDefault()`
的外部拖拽区域，焦点仍停在原按钮上，此时继续显示键盘焦点边框。

## 根因与改动

- Radix 的 `asChild` 组合会覆盖 `data-slot="button"`。共享 Button 和旧
`components/ds/button.tsx` 增加稳定的 `data-zc-button` 标记，使组合触发器仍匹配边框清理规则。
- 非 overlay 的 pointerdown
清理前，记录当前元素是否已有鼠标标记；仅恢复已有标记，避免把保留的键盘焦点误改为鼠标焦点。真正失焦时清理标记，键盘输入恢复键盘焦点样式。
- Paper Focus 暗色侧栏根据元素自身的焦点来源标记决定是否显示焦点边框，不再仅依据页面最后的输入方式。
- 旧 outline Button 保留浅色 `--border` / 暗色
`--input`，并注明覆盖规则与共享规则同优先级、依赖声明顺序。
- 鼠标焦点清理排除 `aria-invalid="true"` 控件；InputGroup 中存在错误状态时保留组级提示。

本轮对应
[键盘焦点保留的审查意见](https://github.com/SerendipityOneInc/ecap-workspace/pull/4058#pullrequestreview-5498674681)，并补充
CSS 规则顺序注释。旧版 Button 已包含在修复范围中。

## 验证

- 新增 5 个反向回归场景均验证了修复前失败、修复后通过：普通区域及 overlay 取消的 pointerdown、共享组合
Button、旧 Button、暗色侧栏。
- 共享设计系统：60 个测试文件、367 项测试通过；TypeScript、ESLint、预览生产构建通过。构建保留既有的单块超过 500
KB 提示。
- 主应用：TypeScript、治理 guards、7 项 Button 聚焦测试与相关文件 ESLint 通过。
- 保留原有鼠标关闭菜单及焦点返回、外部点击未移动焦点、真实 blur、键盘恢复、outline 明暗主题、asChild 链接和错误状态测试。
- 最新提交 `fdfc38ba4`（修复提交 `5863298ed`，随后同步 main）的全部适用 CI
检查通过，包括主应用测试、类型检查、构建和 CodeQL；Claude 与 Codex 自动审查均通过，确认键盘焦点回归已修复。

本轮验证依据为真实组件 DOM、实际 CSS 选择器和 jsdom 计算样式，未进行完整应用的真实浏览器 E2E 或线上截图对照。
```

### PR Body

## 修复内容

修复鼠标关闭 Agent 切换菜单后，按钮仍残留深色焦点边框的问题，覆盖共享 Button、应用旧 Button 和 Paper Focus 暗色侧栏。保留 Tab 导航的可见焦点、outline 按钮原本的边框和校验失败提示。

同时修复审查指出的反向回归：通过 Tab 聚焦按钮后，点击调用 `preventDefault()` 的外部拖拽区域，焦点仍停在原按钮上，此时继续显示键盘焦点边框。

## 根因与改动

- Radix 的 `asChild` 组合会覆盖 `data-slot="button"`。共享 Button 和旧 `components/ds/button.tsx` 增加稳定的 `data-zc-button` 标记，使组合触发器仍匹配边框清理规则。
- 非 overlay 的 pointerdown 清理前，记录当前元素是否已有鼠标标记；仅恢复已有标记，避免把保留的键盘焦点误改为鼠标焦点。真正失焦时清理标记，键盘输入恢复键盘焦点样式。
- Paper Focus 暗色侧栏根据元素自身的焦点来源标记决定是否显示焦点边框，不再仅依据页面最后的输入方式。
- 旧 outline Button 保留浅色 `--border` / 暗色 `--input`，并注明覆盖规则与共享规则同优先级、依赖声明顺序。
- 鼠标焦点清理排除 `aria-invalid="true"` 控件；InputGroup 中存在错误状态时保留组级提示。

本轮对应 [键盘焦点保留的审查意见](https://github.com/SerendipityOneInc/ecap-workspace/pull/4058#pullrequestreview-5498674681)，并补充 CSS 规则顺序注释。旧版 Button 已包含在修复范围中。

## 验证

- 新增 5 个反向回归场景均验证了修复前失败、修复后通过：普通区域及 overlay 取消的 pointerdown、共享组合 Button、旧 Button、暗色侧栏。
- 共享设计系统：60 个测试文件、367 项测试通过；TypeScript、ESLint、预览生产构建通过。构建保留既有的单块超过 500 KB 提示。
- 主应用：TypeScript、治理 guards、7 项 Button 聚焦测试与相关文件 ESLint 通过。
- 保留原有鼠标关闭菜单及焦点返回、外部点击未移动焦点、真实 blur、键盘恢复、outline 明暗主题、asChild 链接和错误状态测试。
- 最新提交 `fdfc38ba4`（修复提交 `5863298ed`，随后同步 main）的全部适用 CI 检查通过，包括主应用测试、类型检查、构建和 CodeQL；Claude 与 Codex 自动审查均通过，确认键盘焦点回归已修复。

本轮验证依据为真实组件 DOM、实际 CSS 选择器和 jsdom 计算样式，未进行完整应用的真实浏览器 E2E 或线上截图对照。


---

## fix(console): unify billing language and row navigation (#4067)

- **SHA**: `716772edf30cb732ab3c553a4e498f1b0f0276ac`
- **作者**: finn-srp
- **日期**: 2026-10-13T07:58:06Z
- **PR**: #4067

### Commit Message

```
fix(console): unify billing language and row navigation (#4067)

## Summary
- Use English throughout Console Platform Billing: navigation,
organization search, balance, top-up confirmation, history, validation
and local error messages.
- Open details from non-interactive areas of an organization row. Retain
the native organization-name link and preserve search/pagination when
entering and leaving details.
- Add copy buttons beside Org ID and Owner UID that do not navigate.
Show a success checkmark, announce the result to screen readers, and
allow retry after clipboard failure.

## Root cause
The billing UI introduced Chinese copy into the English staff Console
and a separate detail action. Whole-row navigation subsequently made
double-click ID selection unreliable. Dedicated copy controls preserve
reliable ID copying alongside immediate row navigation.

## Test plan
- [x] Node 24, on the new branch based on current main: Console lint,
typecheck and build.
- [x] Focused billing route and dashboard shell tests: 22 passed,
including both ID copy actions, keyboard activation, failure/retry, row
navigation and search/pagination preservation.
- [x] Previous browser validation of this identical Console
implementation: actual clipboard values, copy without navigation,
desktop/mobile layout, keyboard copy, failure/retry, native link
behavior and row navigation.
- [x] No recharge was submitted by automated checks.

## Related review
Replaces https://github.com/SerendipityOneInc/ecap-workspace/pull/4065
at the author's request with a fresh PR and review request. Includes the
fix for Tim's ID-copy finding from the first submission.

## Review disposition
- CI passed on the new PR; CodeQL reports no open alerts on its merge
ref. Claude and Codex both returned APPROVE verdicts with no blocking
findings.
- Keep the persistent success checkmark: feedback is intentional and
copying remains available. Claude's concern about a selection elsewhere
suppressing row navigation was not reproduced in prior browser checks;
retain the drag-selection guard.
- A fresh review request was sent to `tim-srp` when this PR was created.
Formal reviewer approval is still pending.
```

### PR Body

## Summary
- Use English throughout Console Platform Billing: navigation, organization search, balance, top-up confirmation, history, validation and local error messages.
- Open details from non-interactive areas of an organization row. Retain the native organization-name link and preserve search/pagination when entering and leaving details.
- Add copy buttons beside Org ID and Owner UID that do not navigate. Show a success checkmark, announce the result to screen readers, and allow retry after clipboard failure.

## Root cause
The billing UI introduced Chinese copy into the English staff Console and a separate detail action. Whole-row navigation subsequently made double-click ID selection unreliable. Dedicated copy controls preserve reliable ID copying alongside immediate row navigation.

## Test plan
- [x] Node 24, on the new branch based on current main: Console lint, typecheck and build.
- [x] Focused billing route and dashboard shell tests: 22 passed, including both ID copy actions, keyboard activation, failure/retry, row navigation and search/pagination preservation.
- [x] Previous browser validation of this identical Console implementation: actual clipboard values, copy without navigation, desktop/mobile layout, keyboard copy, failure/retry, native link behavior and row navigation.
- [x] No recharge was submitted by automated checks.

## Related review
Replaces https://github.com/SerendipityOneInc/ecap-workspace/pull/4065 at the author's request with a fresh PR and review request. Includes the fix for Tim's ID-copy finding from the first submission.

## Review disposition
- CI passed on the new PR; CodeQL reports no open alerts on its merge ref. Claude and Codex both returned APPROVE verdicts with no blocking findings.
- Keep the persistent success checkmark: feedback is intentional and copying remains available. Claude's concern about a selection elsewhere suppressing row navigation was not reproduced in prior browser checks; retain the drag-selection guard.
- A fresh review request was sent to `tim-srp` when this PR was created. Formal reviewer approval is still pending.


---

## refactor(runtime): remove retired FastClaw V1 leftovers (#4064)

- **SHA**: `2dad59138f8e1f1442d412098fb9edcdd9485410`
- **作者**: kaka-srp
- **日期**: 2026-10-13T07:02:15Z
- **PR**: #4064

### Commit Message

```
refactor(runtime): remove retired FastClaw V1 leftovers (#4064)

## Summary

The FastClaw V1 migration is complete, but ECAP still contains unused
runtime hooks, obsolete account/channel/schedule branches, and a Google
OAuth Worker forwarding to a removed callback. Remove those exclusive
leftovers so current pages use the Engine paths and account settings
without V1 lifecycle requests.

- Delete unused Google connector/token storage, its direct PyJWT
dependency, OAuth Worker, unmounted release-admin routes, and deprecated
session credits logging. Billing Gateway metering and the registered
internal release API remain.
- Remove unused V1 initialization, WebSocket/recovery, image-version
polling, upgrade UI, and their exclusive helpers/tests. Simplify
settings, channels, schedules, Agent lists and session navigation while
preserving current Engine behavior.
- Remove ignored Pack runtime asset ID configuration and update
architecture/development documentation. Legacy Builder/Pack Test, shared
runtime types they still consume, historical records, native desktop and
iOS remain supported.

Design, usage evidence, acceptance and configuration retirement
checklist: [cleanup
plan](docs/superpowers/specs/2026-10-13-retired-runtime-cleanup.md).

## Validation

- [x] Synced against latest main; reviewed the local diff and verified
no changes to Legacy Builder/Pack Test implementations or iOS.
- [x] Frontend governance guards, TypeScript, changed-source/test ESLint
and 793 tests across 49 related files passed.
- [x] Backend ruff, formatting, pyright, import contracts and 117
focused tests passed.
- [x] Commit and push governance checks passed. Removed the obsolete
direct PyJWT requirement caught by deptry, then confirmed the dependency
gate passes.
- [x] Fixed CI's Knip findings by removing helpers/test stubs left
unused by the V1 deletion; preserved current error classification and
Sentry logout tag clearing. Knip, TypeScript, ESLint and 204 related
tests passed locally after this fix.
- [x] Following the channel-target review note, reproduced and fixed a
synthetic retired `main` bot option in manual Engine setup. Added
regression coverage for Engine-only options and switching between Engine
workspaces; 49 related tests passed. The real local Slack manual setup
form showed only the account's available Engine target, no retired
option, and no page errors.
- [x] Actual local web/API against staging dependencies: General
settings, Usage, retired Status deep-link fallback, Channels, Schedule
and Agents rendered without page errors or failing API responses. No
retired runtime requests; retained locale requests returned 200.
- [x] Real Engine Slack add dialog and schedule creation form opened
successfully.
- [x] Real staging Engine schedule create/read/update, run-history read
and delete through the local API passed. The fixture remained disabled,
never ran, and an independent list read confirmed removal.
- [ ] CI full suites and production frontend build are the remaining
automated gates.

External channel authorization/credential changes and provider message
delivery were not exercised. Current Engine setup/edit/remove, account
scoping and error handling have retained frontend test coverage. A
historical Builder Project returns the same `409
agent_builder.unsupported_runtime_layout` on both the changed local API
and deployed staging; this pre-existing issue is outside this cleanup.

Review: local self-review completed. Claude's automated review
identified a channel-target path to check; investigation reproduced an
obsolete option in the manual setup form, which is now fixed with a
regression test and real page validation. Stale deleted-hook comments
were also corrected. The error guard for an absent channel target
remains to fail safely, and schedules require an Engine Agent because V1
is retired. Codex's automated review was skipped because GitHub could
not generate the oversized diff; a green job for that path does not mean
it reviewed the code. Human approval is still required before merge.

## Release and configuration

Release both backend and web after merge. Delete Google/GOG Vault
entries only after the backend release in the corresponding environment;
remove remaining ignored Pack ID configuration after manifest rollout.
Previously shipped Nango configuration removal can be completed
separately. Preserve shared encryption/service tokens and all unrelated
settings. No live Vault, Cloudflare routes, credentials or historical
database records were deleted in this PR; Cloudflare shutdown still
requires live ownership/traffic checks and refreshed authentication.

## Size exception

Use `size-override`: this is the explicitly requested retirement sweep,
dominated by deleting complete unused modules and their exclusive tests
(about 19,700 deleted lines, including the retired Worker's lockfile).
The surviving Engine behavior changes and their tests belong with the
removed V1 branches so the result remains buildable and reviewable. The
exception applies only to the size budget; all code-quality, build, test
and review gates still apply.
```

### PR Body

## Summary

The FastClaw V1 migration is complete, but ECAP still contains unused runtime hooks, obsolete account/channel/schedule branches, and a Google OAuth Worker forwarding to a removed callback. Remove those exclusive leftovers so current pages use the Engine paths and account settings without V1 lifecycle requests.

- Delete unused Google connector/token storage, its direct PyJWT dependency, OAuth Worker, unmounted release-admin routes, and deprecated session credits logging. Billing Gateway metering and the registered internal release API remain.
- Remove unused V1 initialization, WebSocket/recovery, image-version polling, upgrade UI, and their exclusive helpers/tests. Simplify settings, channels, schedules, Agent lists and session navigation while preserving current Engine behavior.
- Remove ignored Pack runtime asset ID configuration and update architecture/development documentation. Legacy Builder/Pack Test, shared runtime types they still consume, historical records, native desktop and iOS remain supported.

Design, usage evidence, acceptance and configuration retirement checklist: [cleanup plan](docs/superpowers/specs/2026-10-13-retired-runtime-cleanup.md).

## Validation

- [x] Synced against latest main; reviewed the local diff and verified no changes to Legacy Builder/Pack Test implementations or iOS.
- [x] Frontend governance guards, TypeScript, changed-source/test ESLint and 793 tests across 49 related files passed.
- [x] Backend ruff, formatting, pyright, import contracts and 117 focused tests passed.
- [x] Commit and push governance checks passed. Removed the obsolete direct PyJWT requirement caught by deptry, then confirmed the dependency gate passes.
- [x] Fixed CI's Knip findings by removing helpers/test stubs left unused by the V1 deletion; preserved current error classification and Sentry logout tag clearing. Knip, TypeScript, ESLint and 204 related tests passed locally after this fix.
- [x] Following the channel-target review note, reproduced and fixed a synthetic retired `main` bot option in manual Engine setup. Added regression coverage for Engine-only options and switching between Engine workspaces; 49 related tests passed. The real local Slack manual setup form showed only the account's available Engine target, no retired option, and no page errors.
- [x] Actual local web/API against staging dependencies: General settings, Usage, retired Status deep-link fallback, Channels, Schedule and Agents rendered without page errors or failing API responses. No retired runtime requests; retained locale requests returned 200.
- [x] Real Engine Slack add dialog and schedule creation form opened successfully.
- [x] Real staging Engine schedule create/read/update, run-history read and delete through the local API passed. The fixture remained disabled, never ran, and an independent list read confirmed removal.
- [x] Final PR CI at `d12176c409`: all checks settled without failures. Frontend: 10,488 tests passed (1 skipped); backend: 12,233 passed (5 skipped), coverage 89.62%. Frontend production build, governance/type/lint checks, CodeQL and other affected quality gates passed.

External channel authorization/credential changes and provider message delivery were not exercised. Current Engine setup/edit/remove, account scoping and error handling have retained frontend test coverage. A historical Builder Project returns the same `409 agent_builder.unsupported_runtime_layout` on both the changed local API and deployed staging; this pre-existing issue is outside this cleanup.

Review: local self-review completed. Claude's automated review identified a channel-target path to check; investigation reproduced an obsolete option in the manual setup form, which is now fixed with a regression test and real page validation. Stale deleted-hook comments were also corrected. The final Claude review confirmed the fix and found no blocking defects, with `NEED_HUMAN_REVIEW` for the large retirement scope. The error guard for an absent channel target remains to fail safely, and schedules require an Engine Agent because V1 is retired. Codex's automated review was skipped because GitHub could not generate the oversized diff; a green job for that path does not mean it reviewed the code. The PR was merged by kaka-srp at `2dad59138f8e1f1442d412098fb9edcdd9485410`.

## Release and configuration

Release both backend and web after merge. Delete Google/GOG Vault entries only after the backend release in the corresponding environment; remove remaining ignored Pack ID configuration after manifest rollout. Previously shipped Nango configuration removal can be completed separately. Preserve shared encryption/service tokens and all unrelated settings. No live Vault, Cloudflare routes, credentials or historical database records were deleted in this PR; Cloudflare shutdown still requires live ownership/traffic checks and refreshed authentication.

## Size exception

Use `size-override`: this is the explicitly requested retirement sweep, dominated by deleting complete unused modules and their exclusive tests (about 19,700 deleted lines, including the retired Worker's lockfile). The surviving Engine behavior changes and their tests belong with the removed V1 branches so the result remains buildable and reviewable. The exception applies only to the size budget; all code-quality, build, test and review gates still apply.


---

## style(events): align page with ZooWork branding (#4063)

- **SHA**: `bdb8801b9a30bd24e64f16960343852905b82464`
- **作者**: shana-srp
- **日期**: 2026-10-13T06:49:55Z
- **PR**: #4063

### Commit Message

```
style(events): align page with ZooWork branding (#4063)

## Summary

Align `/events` with ZooWork's marketing design language and the
approved desktop/mobile layout. The upcoming event now groups its text
on the left and date on the right while keeping the same outer edges as
the archive.

- Reuse shared marketing containers, ZooWork tokens and design-system
buttons, with consistent 6px control / 12px card radii, hand cursors and
visible keyboard focus.
- Center the hero, simplify archive navigation into text filters, and
align the community section and its primary/secondary actions.
- Consolidate duplicate event copy, retain the original Didot event
typography and `#7D7895` announcement color, and remove unused upcoming
fields from the data, tests and maintenance guide.
- Hide both the Upcoming hero link and section when no upcoming events
exist, while keeping the archive and its filters available. Remove an
unused page marker and clarify the documented heading structure.

## Test plan

- [x] Updated to latest `main` (`b971edece7`) before committing.
- [x] `scripts/verify-web.sh` on affected Events source/tests:
TypeScript, targeted ESLint, governance guards and all 14 Events tests
passed, including empty-upcoming navigation and archive filtering.
- [x] Commit hook's full frontend lint, Prettier and `git diff --check`
passed.
- [x] Browser verification at 1280px and 393px: container alignment,
responsive card order, no horizontal overflow, filters/counts, section
anchors, links, keyboard focus and cursor styling.

## Screenshots

Desktop:

![Events
desktop](https://github.com/SerendipityOneInc/ecap-workspace/blob/fcc67e8135e327730134976454f7900c9ac6d5a8/docs/superpowers/specs/assets/events-visual-unification-desktop.png?raw=true)

Mobile upcoming card:

![Events
mobile](https://github.com/SerendipityOneInc/ecap-workspace/blob/fcc67e8135e327730134976454f7900c9ac6d5a8/docs/superpowers/specs/assets/events-visual-unification-mobile.png?raw=true)

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary

Align `/events` with ZooWork's marketing design language and the approved desktop/mobile layout. The upcoming event now groups its text on the left and date on the right while keeping the same outer edges as the archive.

- Reuse shared marketing containers, ZooWork tokens and design-system buttons, with consistent 6px control / 12px card radii, hand cursors and visible keyboard focus.
- Center the hero, simplify archive navigation into text filters, and align the community section and its primary/secondary actions.
- Consolidate duplicate event copy, retain the original Didot event typography and `#7D7895` announcement color, and remove unused upcoming fields from the data, tests and maintenance guide.
- Hide both the Upcoming hero link and section when no upcoming events exist, while keeping the archive and its filters available. Remove an unused page marker and clarify the documented heading structure.

## Test plan

- [x] Updated to latest `main` (`b971edece7`) before committing.
- [x] `scripts/verify-web.sh` on affected Events source/tests: TypeScript, targeted ESLint, governance guards and all 14 Events tests passed, including empty-upcoming navigation and archive filtering.
- [x] Commit hook's full frontend lint, Prettier and `git diff --check` passed.
- [x] Browser verification at 1280px and 393px: container alignment, responsive card order, no horizontal overflow, filters/counts, section anchors, links, keyboard focus and cursor styling.

## Screenshots

Desktop:

![Events desktop](https://github.com/SerendipityOneInc/ecap-workspace/blob/fcc67e8135e327730134976454f7900c9ac6d5a8/docs/superpowers/specs/assets/events-visual-unification-desktop.png?raw=true)

Mobile upcoming card:

![Events mobile](https://github.com/SerendipityOneInc/ecap-workspace/blob/fcc67e8135e327730134976454f7900c9ac6d5a8/docs/superpowers/specs/assets/events-visual-unification-mobile.png?raw=true)


---
