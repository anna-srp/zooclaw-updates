---
title: "修复：信用卡支付成功后订单卡住、免费试用额度不到账、升级后旧订阅未取消"
type: "Bug Fix"
priority: "高"
date: "2026-08-19"
status: "待审核"
channels: ""
---

# 修复：信用卡支付成功后订单卡住、免费试用额度不到账、升级后旧订阅未取消

## 核心宣传点

信用卡支付通道切换到 Airwallex 后出现的一批线上支付故障已全部修复：支付成功却跳转回来失败、订单一直停在「处理中」、免费试用的 1000 credits 不到账、升级套餐后旧订阅没被取消可能重复扣费——现在下单、试用、升级都能一次走通。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5f2787b923c6cec7ffbda409a29227433cc90f66`
- PR: #3432
- 作者: tim-srp
- 日期: 2026-08-19T11:36:45Z

### Commit Message

```
fix(billing): settle checkout orders from payment_intent.succeeded events (#3432)

## Summary
- 处理 Airwallex 真实投递的 `payment_intent.succeeded` 事件，按 checkout 绑定本地订单并通过
provider API 补全订阅 facts 后走既有 trial / first_payment 投影结算，修复「Airwallex
支付成功后跳转回来失败」。

## Root cause
托管 checkout 的支付，Airwallex **只投递 payment
类事件**（`payment_intent.created/succeeded`、`payment_attempt.*` 等），从不投递
`subscription.in_trial` / `subscription.active`。旧 dispatcher 只认
subscription 类事件，payment 事件全部落入 `else → IGNORED`，订单永远停留 `pending`，成功页轮询
60 秒超时失败。

staging 实锤（2026-08-19 真实订阅）：
- 支付后 13 个 payment 事件全部到达、签名验证通过、入库，状态全部 `ignored`
- 订单 `cardorder:7f9516b8-5e91-5e62-9c64-a766ec541bc5` 一直
`pending`；Airwallex 端订阅 `sub_sgpvzhm8ghlhhnobad8` 已 ACTIVE

## 修复方案
新增 `app/services/airwallex/payment_events.py`，dispatcher 增加
`payment_intent.succeeded` 分支：

1. 事件 `merchant_order_id`（形如 `"[bco]<checkout_id>"`）→ 解析 checkout id →
`get_by_provider_checkout_session_id` 绑定本地订单（无订单/终态订单 → IGNORED；已
`succeeded` → 幂等 PROCESSED）
2. `GET /billing/billing_checkouts/{id}` 取 `subscription_id` +
`metadata` + `line_items[0].price_id`（已实调 sandbox API 验证字段）
3. `GET /billing/subscriptions/{id}` 取 period / status / customer
4. 订单 `is_trial=true` → trial 投影（provider 报 ACTIVE 时规范化为
`trialing`，本地订单是 trial 的权威）；否则 first-payment 投影

Schema 同步扩展（真实 API 响应格式）：
- checkout 检索响应可无 `url`、可带 `subscription_id` / `metadata` / `line_items`
- 订阅检索响应接受官方 `current_period_starts_at` / `current_period_ends_at` 字段名
- RFC3339 时间戳校验接受紧凑时区 `+0000`（Airwallex 真实返回格式）

## 上线后验证
1. 部署 staging 后，用新账号走真实免费试用订阅，支付成功后应自动落账，成功页不再超时
2. 重放同一 checkout 的 `payment_intent.succeeded` 事件应幂等（不重复授 credit）
3. Airwallex 后台 webhook 配置**无需改动**

## Test plan
- [x] 新增 `tests/unit/test_airwallex_payment_events.py` 12
个用例：真实事件形状绑定、trial/paid 分发、幂等、无绑定忽略、终态订单忽略、订阅缺失重投、lifecycle 分发
- [x] `test_airwallex*` + `test_card_checkout*` 共 413 个用例全绿
- [x] `ruff check` / `ruff format` / `import-linter` 通过
- [x] `pyright` 仅剩预存在 `r2_storage.py` botocore stub 错误（与本次改动无关）

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary
- 处理 Airwallex 真实投递的 `payment_intent.succeeded` 事件，按 checkout 绑定本地订单并通过 provider API 补全订阅 facts 后走既有 trial / first_payment 投影结算，修复「Airwallex 支付成功后跳转回来失败」。

## Root cause
托管 checkout 的支付，Airwallex **只投递 payment 类事件**（`payment_intent.created/succeeded`、`payment_attempt.*` 等），从不投递 `subscription.in_trial` / `subscription.active`。旧 dispatcher 只认 subscription 类事件，payment 事件全部落入 `else → IGNORED`，订单永远停留 `pending`，成功页轮询 60 秒超时失败。

staging 实锤（2026-08-19 真实订阅）：
- 支付后 13 个 payment 事件全部到达、签名验证通过、入库，状态全部 `ignored`
- 订单 `cardorder:7f9516b8-5e91-5e62-9c64-a766ec541bc5` 一直 `pending`；Airwallex 端订阅 `sub_sgpvzhm8ghlhhnobad8` 已 ACTIVE

## 修复方案
新增 `app/services/airwallex/payment_events.py`，dispatcher 增加 `payment_intent.succeeded` 分支：

1. 事件 `merchant_order_id`（形如 `"[bco]<checkout_id>"`）→ 解析 checkout id → `get_by_provider_checkout_session_id` 绑定本地订单（无订单/终态订单 → IGNORED；已 `succeeded` → 幂等 PROCESSED）
2. `GET /billing/billing_checkouts/{id}` 取 `subscription_id` + `metadata` + `line_items[0].price_id`（已实调 sandbox API 验证字段）
3. `GET /billing/subscriptions/{id}` 取 period / status / customer
4. 订单 `is_trial=true` → trial 投影（provider 报 ACTIVE 时规范化为 `trialing`，本地订单是 trial 的权威）；否则 first-payment 投影

Schema 同步扩展（真实 API 响应格式）：
- checkout 检索响应可无 `url`、可带 `subscription_id` / `metadata` / `line_items`
- 订阅检索响应接受官方 `current_period_starts_at` / `current_period_ends_at` 字段名
- RFC3339 时间戳校验接受紧凑时区 `+0000`（Airwallex 真实返回格式）

## 上线后验证
1. 部署 staging 后，用新账号走真实免费试用订阅，支付成功后应自动落账，成功页不再超时
2. 重放同一 checkout 的 `payment_intent.succeeded` 事件应幂等（不重复授 credit）
3. Airwallex 后台 webhook 配置**无需改动**

## Test plan
- [x] 新增 `tests/unit/test_airwallex_payment_events.py` 12 个用例：真实事件形状绑定、trial/paid 分发、幂等、无绑定忽略、终态订单忽略、订阅缺失重投、lifecycle 分发
- [x] `test_airwallex*` + `test_card_checkout*` 共 413 个用例全绿
- [x] `ruff check` / `ruff format` / `import-linter` 通过
- [x] `pyright` 仅剩预存在 `r2_storage.py` botocore stub 错误（与本次改动无关）


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `9b79cc0b77231703005f0cffa8f6106bca929504`
- PR: #3428
- 作者: tim-srp
- 日期: 2026-08-19T09:31:09Z

### Commit Message

```
fix(billing): match real Airwallex webhook delivery shape and signing (#3428)

## 背景

Airwallex 真实 webhook 投递全部被拒（`invalid_payload` /
`invalid_signature`），导致用户订阅（免费试用 1000 credits）无法落账。经抓包捕获真实投递请求体后，确认根因：

### 请求体结构不匹配
Airwallex 实际投递结构为：
```json
{
  "id": "evt_...",
  "name": "subscription.in_trial",
  "source_id": "sub_...",
  "account_id": "...",
  "created_at": "...",
  "data": { "object": { ... } }
}
```
- 事件类型在 `name` 字段（旧实现读 `event_type`/`type`，恒为 `None`）
- 业务对象在 `data.object`（旧实现读顶层 `object`，恒为 `{}`）

## 改动

- `app/schema/airwallex.py`：`AirwallexWebhookEnvelope` 增加
`name`、`source_id`、`data`（`AirwallexWebhookEventData.object`）；`event_type_of`
优先读 `name`，新增 `event_object_of` 优先读 `data.object`，均保留旧
`event_type`/`type`/`object` 兼容。
- `app/services/airwallex/webhook.py`：签名验证**仅信任服务器端配置的
`AIRWALLEX_WEBHOOK_SECRET`**，绝不接受请求提供的 HMAC 密钥。
- `app/routes/billing.py`：`claim_provider_event` payload 改用
`event_object_of`；路由不读取/不透传任何请求提供的密钥。
- `app/services/airwallex/event_facts.py`：用 `event_object_of` 读
payload；字段支持真实名
`current_period_starts_at`/`current_period_ends_at`、`period_starts_at`/`period_ends_at`、`trial_end_at`，并保留旧名
fallback。
- 单元测试：新增真实结构（`name` + `data.object`）用例，以及安全回归用例（请求提供的 HMAC
密钥必须被拒绝、路由绝不转发请求密钥），共 35 个全部通过。

## 安全说明

早期版本曾尝试接受 `Client-Secret-Key` 请求头作为 HMAC 候选密钥以兼容测试事件 —— 这等于移除了 webhook
认证：攻击者可自选 header 值伪造签名，伪造 `subscription.in_trial` 等生命周期事件并获取已持久化的
entitlement/credits。本 PR **已移除该路径**，签名验证只使用服务器端配置的
secret。若测试事件确实使用独立密钥，应在服务器端配置（而非从请求读取），或单独隔离测试处理。

## 验证

- ✅ 35 个 airwallex webhook / event_facts / routes 单元测试通过（含 2 个安全回归测试）
- ✅ `ruff check` / `ruff format` / `import-linter` 通过
- ℹ️ `pyright` 仅剩 `r2_storage.py` 的 7 个预存在 botocore stub 类型错误（与本改动无关）

## 上线后验证

1. 将 Airwallex webhook URL 指回
`https://ecap.gensmo.nosay.live/api/airwallex/webhook`
2. 控制台发一次 "send test event"，确认返回 200（真实投递使用通知 URL secret 签名，可正常验证）
3. 走一遍真实订阅流程，确认 `subscription.in_trial` / `subscription.active` 落账

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## 背景

Airwallex 真实 webhook 投递全部被拒（`invalid_payload` / `invalid_signature`），导致用户订阅（免费试用 1000 credits）无法落账。经抓包捕获真实投递请求体后，确认根因：

### 请求体结构不匹配
Airwallex 实际投递结构为：
```json
{
  "id": "evt_...",
  "name": "subscription.in_trial",
  "source_id": "sub_...",
  "account_id": "...",
  "created_at": "...",
  "data": { "object": { ... } }
}
```
- 事件类型在 `name` 字段（旧实现读 `event_type`/`type`，恒为 `None`）
- 业务对象在 `data.object`（旧实现读顶层 `object`，恒为 `{}`）

## 改动

- `app/schema/airwallex.py`：`AirwallexWebhookEnvelope` 增加 `name`、`source_id`、`data`（`AirwallexWebhookEventData.object`）；`event_type_of` 优先读 `name`，新增 `event_object_of` 优先读 `data.object`，均保留旧 `event_type`/`type`/`object` 兼容。
- `app/services/airwallex/webhook.py`：签名验证**仅信任服务器端配置的 `AIRWALLEX_WEBHOOK_SECRET`**，绝不接受请求提供的 HMAC 密钥。
- `app/routes/billing.py`：`claim_provider_event` payload 改用 `event_object_of`；路由不读取/不透传任何请求提供的密钥。
- `app/services/airwallex/event_facts.py`：用 `event_object_of` 读 payload；字段支持真实名 `current_period_starts_at`/`current_period_ends_at`、`period_starts_at`/`period_ends_at`、`trial_end_at`，并保留旧名 fallback。
- 单元测试：新增真实结构（`name` + `data.object`）用例，以及安全回归用例（请求提供的 HMAC 密钥必须被拒绝、路由绝不转发请求密钥），共 35 个全部通过。

## 安全说明

早期版本曾尝试接受 `Client-Secret-Key` 请求头作为 HMAC 候选密钥以兼容测试事件 —— 这等于移除了 webhook 认证：攻击者可自选 header 值伪造签名，伪造 `subscription.in_trial` 等生命周期事件并获取已持久化的 entitlement/credits。本 PR **已移除该路径**，签名验证只使用服务器端配置的 secret。若测试事件确实使用独立密钥，应在服务器端配置（而非从请求读取），或单独隔离测试处理。

## 验证

- ✅ 35 个 airwallex webhook / event_facts / routes 单元测试通过（含 2 个安全回归测试）
- ✅ `ruff check` / `ruff format` / `import-linter` 通过
- ℹ️ `pyright` 仅剩 `r2_storage.py` 的 7 个预存在 botocore stub 类型错误（与本改动无关）

## 上线后验证

1. 将 Airwallex webhook URL 指回 `https://ecap.gensmo.nosay.live/api/airwallex/webhook`
2. 控制台发一次 "send test event"，确认返回 200（真实投递使用通知 URL secret 签名，可正常验证）
3. 走一遍真实订阅流程，确认 `subscription.in_trial` / `subscription.active` 落账


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e3b9730a315e6aa51aa290a407530a64df1b01be`
- PR: #3425
- 作者: tim-srp
- 日期: 2026-08-19T05:37:53Z

### Commit Message

```
fix(billing): bind Airwallex subscription before trial projection (#3425)

## 问题

新注册账号走 free trial 支付订阅后，订单卡在 `pending` 状态无法完成。

根因：Airwallex checkout 创建时只写入 `provider_checkout_session_id`，**没有**
`checkout.completed` webhook 事件（Creem
有）。订阅身份信息（`provider_subscription_id` / `provider_status`）从未被绑定。

而 `attach_trial_projection` 要求订单同时满足：
- `status: "pending"` + `is_trial: True`
- `provider_status: "completed"` + `provider_subscription_id`

这两个字段永远缺失 → 每次 trial 投影都报 `projection lost` → 订单卡在 pending。

## 修复

在 `settle_airwallex_trial_subscription` 中，拿到订阅事实（subscription
facts）后、执行需要这两个字段的投影之前，先绑定订阅身份：

新增 `app/database/card_checkout_binding_repo.py` 的
`bind_subscription_checkout`：
- 写入 `provider_subscription_id` + `provider_status="completed"` +
`provider_customer_id`
- 幂等：只匹配 `provider_subscription_id: {"$in": [None]}` 的订单，重放安全

## 影响范围

- 仅影响 Airwallex **trial** 路径
- `first_payment` 路径不需要绑定（`record_payment_order` 已写
`provider_subscription_id`；`attach_settlement_projection` 不要求
`provider_status`）

## 测试

- 新增 3 个测试：trial 绑定调用、绑定写入 provider 身份、绑定幂等
- 全量 37 个测试通过；ruff / import-linter / pyright（改动文件）全部通过

## 说明

- `r2_storage.py` 有 7 个 pre-existing pyright 错误（本地 miniconda boto3
1.34.131 无 `py.typed` 标记），与本次改动无关，main 分支同样存在，CI 环境（uv 装最新 boto3）不会触发。

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## 问题

新注册账号走 free trial 支付订阅后，订单卡在 `pending` 状态无法完成。

根因：Airwallex checkout 创建时只写入 `provider_checkout_session_id`，**没有** `checkout.completed` webhook 事件（Creem 有）。订阅身份信息（`provider_subscription_id` / `provider_status`）从未被绑定。

而 `attach_trial_projection` 要求订单同时满足：
- `status: "pending"` + `is_trial: True`
- `provider_status: "completed"` + `provider_subscription_id`

这两个字段永远缺失 → 每次 trial 投影都报 `projection lost` → 订单卡在 pending。

## 修复

在 `settle_airwallex_trial_subscription` 中，拿到订阅事实（subscription facts）后、执行需要这两个字段的投影之前，先绑定订阅身份：

新增 `app/database/card_checkout_binding_repo.py` 的 `bind_subscription_checkout`：
- 写入 `provider_subscription_id` + `provider_status="completed"` + `provider_customer_id`
- 幂等：只匹配 `provider_subscription_id: {"$in": [None]}` 的订单，重放安全

## 影响范围

- 仅影响 Airwallex **trial** 路径
- `first_payment` 路径不需要绑定（`record_payment_order` 已写 `provider_subscription_id`；`attach_settlement_projection` 不要求 `provider_status`）

## 测试

- 新增 3 个测试：trial 绑定调用、绑定写入 provider 身份、绑定幂等
- 全量 37 个测试通过；ruff / import-linter / pyright（改动文件）全部通过

## 说明

- `r2_storage.py` 有 7 个 pre-existing pyright 错误（本地 miniconda boto3 1.34.131 无 `py.typed` 标记），与本次改动无关，main 分支同样存在，CI 环境（uv 装最新 boto3）不会触发。


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `acd64aa14440cce16d08798b220513132fe3ad83`
- PR: #3424
- 作者: tim-srp
- 日期: 2026-08-19T03:34:12Z

### Commit Message

```
fix(billing): attach settlement projection without provider transaction (#3424)

## Summary
Fix Airwallex `subscription.active` webhook settlement: the order was
fully
settled (credits granted, agreement + entitlement written) but the final
settlement-projection attach failed, so the webhook returned
`billing.airwallex.projection.conflict` and the user-facing status
stayed
`pending` / "Something went wrong".

## Root cause
A `subscription.active` webhook carries **no invoice**, so:
- `record_payment_order` writes the order **without**
`provider_transaction_id`
(the field is absent — `replay_safe_update_fields` skips `None` values)
- `attach_settlement_projection` then used the **payment order id** as a
  fallback `transaction_id`, which never matches the absent field

The Mongo query `{provider_transaction_id: <payment_order_id>}` matches
nothing, so `attach_settlement_projection` returned `False` → the
webhook
re-raised `projection.conflict` → Airwallex redelivered forever while
credits
had already been granted exactly once (idempotent).

## Fix
- `first_payment.py`: pass `transaction_id=None` when no invoice exists
(matches the written state) instead of fabricating a payment-order-id
fallback
- `card_checkout_order_repo.py`: widen `transaction_id` to `str | None`
so a
  null value matches both a missing and an explicit-null stored field
- Regression tests:
- `test_airwallex_first_payment.py`: `subscription.active` (no invoice)
    now asserts the projection attach receives `transaction_id=None`
- `test_creem_first_payment_repo.py`: adds a repo-level case proving an
order without a transaction id still attaches; keeps the strict-match
guarantee for callers that do pass a transaction id (Creem unchanged)

## Test plan
- [x] `test_airwallex_first_payment.py` — 14 passed
- [x] `test_creem_first_payment_repo.py` — 12 passed
- [x] Airwallex suite (`test_airwallex_*.py`) — 271 passed
- [x] Creem callers of `attach_settlement_projection` — 220 passed
- [x] ruff check / format, pyright, import-linter, pre-commit hooks

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary
Fix Airwallex `subscription.active` webhook settlement: the order was fully
settled (credits granted, agreement + entitlement written) but the final
settlement-projection attach failed, so the webhook returned
`billing.airwallex.projection.conflict` and the user-facing status stayed
`pending` / "Something went wrong".

## Root cause
A `subscription.active` webhook carries **no invoice**, so:
- `record_payment_order` writes the order **without** `provider_transaction_id`
  (the field is absent — `replay_safe_update_fields` skips `None` values)
- `attach_settlement_projection` then used the **payment order id** as a
  fallback `transaction_id`, which never matches the absent field

The Mongo query `{provider_transaction_id: <payment_order_id>}` matches
nothing, so `attach_settlement_projection` returned `False` → the webhook
re-raised `projection.conflict` → Airwallex redelivered forever while credits
had already been granted exactly once (idempotent).

## Fix
- `first_payment.py`: pass `transaction_id=None` when no invoice exists
  (matches the written state) instead of fabricating a payment-order-id fallback
- `card_checkout_order_repo.py`: widen `transaction_id` to `str | None` so a
  null value matches both a missing and an explicit-null stored field
- Regression tests:
  - `test_airwallex_first_payment.py`: `subscription.active` (no invoice)
    now asserts the projection attach receives `transaction_id=None`
  - `test_creem_first_payment_repo.py`: adds a repo-level case proving an
    order without a transaction id still attaches; keeps the strict-match
    guarantee for callers that do pass a transaction id (Creem unchanged)

## Test plan
- [x] `test_airwallex_first_payment.py` — 14 passed
- [x] `test_creem_first_payment_repo.py` — 12 passed
- [x] Airwallex suite (`test_airwallex_*.py`) — 271 passed
- [x] Creem callers of `attach_settlement_projection` — 220 passed
- [x] ruff check / format, pyright, import-linter, pre-commit hooks

---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `644316ad8b65e9acd7d0449b22842ede64a0b991`
- PR: #3435
- 作者: tim-srp
- 日期: 2026-08-19T12:29:10Z

### Commit Message

```
fix(billing): take new subscription id from context in replacement cleanup (#3435)

## Summary
- 修复 Airwallex 升级结算最后一步"取消旧订阅"的确定性失败：新订阅 id 改由已验证的 replacement context
携带，不再从支付前的订单快照读取。

## Root cause
升级的结算事件（`payment_intent.succeeded`）到达时，本地订单仍是 **支付前的 pending
快照**——`provider_subscription_id` 字段不存在（订阅是支付后才创建的，settle
时才写回订单）。`cancel_replaced_subscription` 从这个快照读新订阅 id
得到空字符串，`_old_replacement_identity_matches` 的"新订阅 id 非空"校验失败 →
`billing.airwallex.replacement_cleanup_identity_conflict` → 旧订阅的 cancel
API 从未被调用。

staging 实锤：同一 uid 两次真实升级（starter→pro→ultra），两个前任订阅在 Airwallex 端均保持
ACTIVE，两次 webhook 事件均 failed 于同一错误码。用真实 staging 数据形状在单测中 100%
复现（错误码与文案逐字一致）。

## 修复
- `AirwallexPaidReplacement` 增加 `new_provider_subscription_id` 字段，在
prepare（正常 + replay 分支）与 `retry_cleanup` 构造 context 时传入。
- `cancel_replaced_subscription` 从 context 读新订阅 id（不再读旧订单快照）。
- 新增回归测试
`test_cancel_uses_context_subscription_id_for_pending_order_snapshot`：用真实
pending 订单形状（无 `provider_subscription_id`）断言 cancel
正常调用且旧订阅在周期末取消（`proration_behavior="NONE"`）。

## 验证
- [x] 回归测试先红后绿（修复前复现 staging 同款 `cleanup_identity_conflict`）
- [x] 修复后完整 first_payment 路径复现：cancel 正确指向旧订阅 id
- [x] `test_airwallex_replacement.py`（34）+
`test_airwallex_first_payment.py`（49）全绿；airwallex + card_checkout 全套 415
绿
- [x] ruff check / ruff format / import-linter 通过；pyright 零新增错误（仅预存在
r2_storage.py）

## 上线后验证
1. 部署后新升级：旧订阅应收到 cancel 调用并在周期末取消（`cancel_at_period_end=true`），本地旧
agreement 转 `canceling` + `replacement_cleanup_required=false`
2. 历史脏数据由每小时 `check-subscription-sync`
对账（`reconcile_current_airwallex_subscriptions` → `retry_cleanup`）自动收敛

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary
- 修复 Airwallex 升级结算最后一步"取消旧订阅"的确定性失败：新订阅 id 改由已验证的 replacement context 携带，不再从支付前的订单快照读取。

## Root cause
升级的结算事件（`payment_intent.succeeded`）到达时，本地订单仍是 **支付前的 pending 快照**——`provider_subscription_id` 字段不存在（订阅是支付后才创建的，settle 时才写回订单）。`cancel_replaced_subscription` 从这个快照读新订阅 id 得到空字符串，`_old_replacement_identity_matches` 的"新订阅 id 非空"校验失败 → `billing.airwallex.replacement_cleanup_identity_conflict` → 旧订阅的 cancel API 从未被调用。

staging 实锤：同一 uid 两次真实升级（starter→pro→ultra），两个前任订阅在 Airwallex 端均保持 ACTIVE，两次 webhook 事件均 failed 于同一错误码。用真实 staging 数据形状在单测中 100% 复现（错误码与文案逐字一致）。

## 修复
- `AirwallexPaidReplacement` 增加 `new_provider_subscription_id` 字段，在 prepare（正常 + replay 分支）与 `retry_cleanup` 构造 context 时传入。
- `cancel_replaced_subscription` 从 context 读新订阅 id（不再读旧订单快照）。
- 新增回归测试 `test_cancel_uses_context_subscription_id_for_pending_order_snapshot`：用真实 pending 订单形状（无 `provider_subscription_id`）断言 cancel 正常调用且旧订阅在周期末取消（`proration_behavior="NONE"`）。

## 验证
- [x] 回归测试先红后绿（修复前复现 staging 同款 `cleanup_identity_conflict`）
- [x] 修复后完整 first_payment 路径复现：cancel 正确指向旧订阅 id
- [x] `test_airwallex_replacement.py`（34）+ `test_airwallex_first_payment.py`（49）全绿；airwallex + card_checkout 全套 415 绿
- [x] ruff check / ruff format / import-linter 通过；pyright 零新增错误（仅预存在 r2_storage.py）

## 上线后验证
1. 部署后新升级：旧订阅应收到 cancel 调用并在周期末取消（`cancel_at_period_end=true`），本地旧 agreement 转 `canceling` + `replacement_cleanup_required=false`
2. 历史脏数据由每小时 `check-subscription-sync` 对账（`reconcile_current_airwallex_subscriptions` → `retry_cleanup`）自动收敛


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `ac48e41a737c3e7ababe7179a350363c19c50486`
- PR: #3443
- 作者: tim-srp
- 日期: 2026-08-19T13:38:47Z

### Commit Message

```
fix(billing): converge local cleanup for cancelled subscriptions without periods (#3443)

## Summary
- 修复：旧订阅在 Airwallex 端取消成功后，本地 agreement
因"已取消订阅响应无周期字段"抛错，永远无法收敛（`replacement_cleanup_required` 不清除）。

## Root cause
`project_superseded_subscription_state` 用 cancel
读回响应校验周期：`_timestamp_seconds(subscription.current_period_start)`。完全取消的订阅返回
`current_period_starts_at: null`（staging 实锤：uid `7495832530386423808`
升级后旧 trial 订阅在 Airwallex 端已 `CANCELLED`，cancel API 修复 #3435
生效），`_timestamp_seconds(None)` 抛 `ValueError` → 对账每次 cancel 成功但本地投影失败，旧
agreement 永远停留在 `trialing` + `replacement_cleanup_required=true`。

## 修复
- 响应周期缺失（`current_period_starts_at`/`current_period_start`
均为空）时**跳过周期校验**，以本地 agreement 周期为权威继续写库（status →
`canceling`、`replacement_cleanup_required → false`）。
- 响应报告了周期时仍必须与本地一致才投影（原有防线保留）。

## 验证
- [x] 新增回归测试
`test_cancel_converges_when_cancelled_subscription_carries_no_period`
先红后绿（修复前复现 staging 同款 `ValueError: Airwallex replacement response is
missing its current period`）
- [x] `test_airwallex_replacement.py` 35 全绿；airwallex + card_checkout 全套
421 全绿
- [x] pre-commit 全过（ruff / pyright / import-linter 等）

## 上线后验证
1. 部署后下一次每小时对账（`check-subscription-sync`）会自动收敛历史脏数据：uid
`7495808292011118592`（starter/pro 两条）与 `7495832530386423808`（starter
一条）的旧 agreement 应转为 `canceling` + `replacement_cleanup_required=false`
2. 新升级流程验证不变：支付后 cleanup 一次完成

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary
- 修复：旧订阅在 Airwallex 端取消成功后，本地 agreement 因"已取消订阅响应无周期字段"抛错，永远无法收敛（`replacement_cleanup_required` 不清除）。

## Root cause
`project_superseded_subscription_state` 用 cancel 读回响应校验周期：`_timestamp_seconds(subscription.current_period_start)`。完全取消的订阅返回 `current_period_starts_at: null`（staging 实锤：uid `7495832530386423808` 升级后旧 trial 订阅在 Airwallex 端已 `CANCELLED`，cancel API 修复 #3435 生效），`_timestamp_seconds(None)` 抛 `ValueError` → 对账每次 cancel 成功但本地投影失败，旧 agreement 永远停留在 `trialing` + `replacement_cleanup_required=true`。

## 修复
- 响应周期缺失（`current_period_starts_at`/`current_period_start` 均为空）时**跳过周期校验**，以本地 agreement 周期为权威继续写库（status → `canceling`、`replacement_cleanup_required → false`）。
- 响应报告了周期时仍必须与本地一致才投影（原有防线保留）。

## 验证
- [x] 新增回归测试 `test_cancel_converges_when_cancelled_subscription_carries_no_period` 先红后绿（修复前复现 staging 同款 `ValueError: Airwallex replacement response is missing its current period`）
- [x] `test_airwallex_replacement.py` 35 全绿；airwallex + card_checkout 全套 421 全绿
- [x] pre-commit 全过（ruff / pyright / import-linter 等）

## 上线后验证
1. 部署后下一次每小时对账（`check-subscription-sync`）会自动收敛历史脏数据：uid `7495808292011118592`（starter/pro 两条）与 `7495832530386423808`（starter 一条）的旧 agreement 应转为 `canceling` + `replacement_cleanup_required=false`
2. 新升级流程验证不变：支付后 cleanup 一次完成


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `b275b11d4d0a44193bae13740148cfa6cc4592bc`
- PR: #3447
- 作者: tim-srp
- 日期: 2026-08-19T15:15:52Z

### Commit Message

```
fix(billing): retry checkout read when the succeeded event races subscription creation (#3447)

## Summary
- 生产实锤：`payment_intent.succeeded` 事件比 Airwallex 写入 checkout
`subscription_id` 早 ~5 秒到达，处理时 checkout 尚无订阅 → `event_not_supported` →
重投耗尽 → trial 订单永远 pending（`cardorder:034ef647`，checkout
`bco_uspdfkhxhhlhq51leki` 15:01:43 事件 vs 15:01:48 订阅创建）。

## 修复
- checkout 检索在无 `subscription_id` 时短暂重试（3 次 × 2
秒），覆盖观测到的创建延迟窗口；重试后仍缺失才抛可重投错误。

## 验证
- [x] 新增回归测试：第一次读无订阅、第二次读有 → 结算成功且 checkout 读取 2 次（先红后绿）
- [x] payment_events / lifecycle / replacement 66 全绿
- [x] pre-commit 全过（ruff / pyright / import-linter）

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary
- 生产实锤：`payment_intent.succeeded` 事件比 Airwallex 写入 checkout `subscription_id` 早 ~5 秒到达，处理时 checkout 尚无订阅 → `event_not_supported` → 重投耗尽 → trial 订单永远 pending（`cardorder:034ef647`，checkout `bco_uspdfkhxhhlhq51leki` 15:01:43 事件 vs 15:01:48 订阅创建）。

## 修复
- checkout 检索在无 `subscription_id` 时短暂重试（3 次 × 2 秒），覆盖观测到的创建延迟窗口；重试后仍缺失才抛可重投错误。

## 验证
- [x] 新增回归测试：第一次读无订阅、第二次读有 → 结算成功且 checkout 读取 2 次（先红后绿）
- [x] payment_events / lifecycle / replacement 66 全绿
- [x] pre-commit 全过（ruff / pyright / import-linter）

