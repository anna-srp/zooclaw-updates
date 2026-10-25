# SerendipityOneInc/ecap-workspace — commits 2026-10-12

## fix(billing): switch vertical packs to Stripe with invoice-period settlement (#4061)

- **SHA**: `b971edece751235d024374d86b41ba38f81abcf2`
- **作者**: tim-srp
- **日期**: 2026-10-12T15:19:25Z
- **PR**: #4061

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

### PR Body

## Summary

取代 #4056（不合并）。#4056 的路由改动（`af644cb87`）保留原作者身份 cherry-pick 进来，并按 #4056 的评审补齐业务逻辑。设计见 `docs/superpowers/specs/2026-10-12-vertical-pack-stripe-settlement.md`。

- **支付入口**：所有垂直包（含 Restaurant）的 purchase-capability 都返回 Stripe，下单走 Stripe Checkout。两个前端（`web/app`、`web/enterprise-admin`）的结账页都只保留一个 Card 按钮：移除 Alipay 按钮、Alipay 处理函数和「Card 或 Alipay」文案。
- **发放**：企业包的首付（`checkout.session.completed`）、续费（`invoice.paid`）、`order_confirm` 和 reconcile 兜底，都分流到新的 `stripe/enterprise_payment.py`。按「已支付 Invoice」的明细周期给团队钱包发积分，幂等键沿用 `(subscription, period_start, period_end)`，同一期只发一次。
- **金额校验对齐 Pro**：复用 `monthly_invoice._validate_amounts`，目录价换成套餐快照总价（新增带默认值的 `price_cents` 参数，Pro 调用点不变）。另外逐行核对：
  - base + addon 的 price 与金额；
  - 订阅归属、非 proration、数量为 1；
  - 各行周期一致。

  明细超过一页时拉取全量。
- **重复订阅（结算层，对齐 Pro `_record_agreement`）**：同一购买人已有另一个未终止的 current 订阅时，抛 `billing.overlapping_subscription` 转人工。不发权益，也不取消任何 Stripe 订阅。下单 / Checkout 层的防重复另见 #4060。
- **生命周期由 Stripe 管理**：企业 agreement 收到 `customer.subscription.updated/deleted` 时，重新 retrieve 最新订阅再投影（与 Pro 一致）。写入时带上 `team_id / subscription_kind / enterprise_package_id`。
- **禁止 Stripe 套餐变更**：`POST /subscription/enterprise-package/change` 对 Stripe 订阅直接拒绝（`billing_v2.enterprise_package.change.unsupported_provider`），在调用 Stripe、写订单之前返回。否则 Stripe 会按新价格扣款，结算却按原套餐快照拒绝这张账单（Codex review）。Antom 不变。

## Root cause

- Restaurant plan 的 capability / provider 被改写到 Airwallex（#4056 已修，本 PR 沿用）。
- 企业包付款走 legacy 写入，带来两个问题（#4056 评审 P1-3）：
  - 发放周期取的是 Stripe Subscription 的当前周期（`subscription_period_start/end`），不是这张已支付 Invoice 的周期。账单迟到或乱序时会记错期，或占用下一期的幂等键；
  - 金额只比对事件总额，不核对明细，也不识别 Stripe 折扣。
- 生命周期事件写企业 agreement 时没带团队身份字段，触发 `billing_v2.subscription_agreement.team_owner_conflict`，webhook 失败（#4056 评审 P1-2）。修复前，新增的 3 个企业用例都以这个错误失败。

## 部署前提

1. 每个垂直包 plan 的基础包和每个 addon，在当前 Stripe 账号里都要有可用的价格。staging（test mode）和 production（live mode）各确认一次。
   - 不需要手动建：`POST /internal/vertical-pack-plans/{plan_id}` 会为缺少 id 的基础包 / addon 自动创建 product 和按月 USD 价格。
   - 下单时 `validate_stripe_prices_for_snapshot` 会逐条校验 active、USD、按月、product、金额，不通过就在付款前报错。
2. Stripe webhook（与 Pro 共用的 `/stripe/webhook`）订阅以下事件：
   - `checkout.session.completed`
   - `invoice.paid`
   - `invoice.payment_failed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
3. 前后端都要部署，建议先后端、后前端。

## 不在本 PR 范围 / 已知事项

- 下单 / Checkout 层防重复支付：见 #4060。
- 实付为 0 的企业包账单（100% 折扣、余额全额抵扣）会被明确拒绝（`billing.invoice_mismatch`），需要人工处理。Pro 有专门的零元发放门槛，这次没有扩展到企业包。
- 企业包退款（`charge.refunded`）：`billing_v2_refunds._record_refunded_subscription_loss` 仍是旧投影，对企业 agreement 同样会触发 `team_owner_conflict`。这不在本次「购买 → 发放 → 续费」范围内，确认后另行修复。
- `invoice.payment_failed` 只解析旧版 payload 的 `invoice.subscription`。这是现有行为，Pro 也一样。新版 payload 下由 `customer.subscription.updated` 重新 retrieve 来同步 `past_due`。
- 套餐变更：Stripe 订阅不再允许变更，`change_enterprise_package` 中的 Stripe 分支（价格校验、修改 Stripe 订阅项）因此走不到。按「不做清理」保留，未删除。
- Airwallex 代码清理与重构：按要求这次不做。jscpd 报告 `enterprise_payment` ↔ `monthly_payment` 有两处小段重复（15 + 18 行）。app 重复率 1.47%（阈值 3%），tests 5.2%（阈值 7.5%）。

## Test plan

- [x] 新增单测 `test_stripe_enterprise_invoice.py`、`test_stripe_enterprise_payment.py`、`test_stripe_enterprise_lifecycle.py`，覆盖：
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
  - `web/enterprise-admin` 全量单测（451 passed）和 lint，结账页测试断言只渲染 Card、没有 Alipay。
- [x] 无新的查询形态：只复用现有 repo 方法，没有新增 CSFLE 风险
- [ ] Staging（需先完成部署前提）：用 Stripe Test Clock 走一遍：
  1. 真实 Checkout 付款，首期发放；
  2. 推进时钟，续扣后发放下一期；
  3. 取消订阅。

  每一步都核对团队钱包和 agreement。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(platform): add audited manual organization top-ups (#4059)

- **SHA**: `f2b0205e377afb4913133ffc997d77c22089b5d5`
- **作者**: finn-srp
- **日期**: 2026-10-12T12:54:48Z
- **PR**: #4059

### Commit Message

```
feat(platform): add audited manual organization top-ups (#4059)

## Summary
Customers who pay for Platform usage through an offline contract can now
receive the purchased balance through the staff Console. Staff find an
active Platform Organization in a paginated, searchable list, enter a
USD amount and internal note, and confirm the recharge. The Org detail
view shows its current balance and individual recharge records. Recharge
history loads independently of the balance lookup, so staff can inspect
manual-review records during a wallet or gateway failure; recharge
controls remain hidden until the first balance lookup succeeds.

The API requires verified SRP staff identity plus the current superadmin
email allowlist. Manual credits use the existing Org wallet and durable
fulfillment flow: the order and operator audit are recorded before
delivery, a persisted claim allows only one wallet POST, and an
uncertain result is reconciled rather than reposted. The Console
generates and retains the operation reference for same-attempt retries
and reloads. Offline paid credits count as prior paid purchases without
starting Stripe Checkout or granting a card reward; complimentary
credits remain a separate API/storage source.

Customer billing displays both online and offline purchases as
**Top-up**. Internal source, operator, reference and note remain
separate; staff details are not returned to customers. No commercial
subscription or changes to Billing Gateway/account-service APIs are
introduced.

## Test plan
- [x] Rebase onto current `origin/main`; run local `ecap-verify-py-ci`:
12,213 passed / 5 skipped, 89.57% coverage; Linux dependency resolution,
static checks, ci-lint and source/test duplication checks passed.
- [x] Console: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test` (685
passed), `pnpm build`.
- [x] Platform: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test` (283
passed), `pnpm build`. Two render-wait failures during concurrent local
verification passed on targeted and full reruns without code or timeout
changes.
- [x] Verify actual repository operations through staging CSFLE:
manual-order insert/read/CAS/history/list in an isolated disposable
fixture, plus read-only Org pagination and literal name/ID/owner search.
- [x] Devcontainer integration: authenticated staff lookup, isolated
test Org with its real staging wallet, customer top-up history, and
desktop/mobile Console flow. The tester confirmed a $1 offline top-up
and its customer balance/history.

## Rollout
Deploy the backend on every API replica and recovery worker before
exposing the Console action: older strict order readers cannot decode
manual-credit fields. New Stripe orders retain their existing persisted
shape. No deployment or production data write is included in this PR.

## Review disposition
Previous GitHub CI checks passed. Codex review reported no findings.
Claude noted that a concurrent `updated_at` change can prevent the
redundant order-local `manual.repeated_confirmation` history entry from
being appended. This is left unchanged: every `grant()` invocation
separately appends global requested/outcome audit events with distinct
audit IDs, so the retry operator, target, reference and outcome remain
durably recorded even on that CAS miss; delivery also re-reads current
state and retains the one-POST guarantee. The order-local history caveat
is retained for human review.


Tim's first-load balance failure finding is fixed in `0b0916eb0`:
history is mounted directly from the selected Org ID, while the balance
error and reload action remain visible and the recharge form is withheld
without account data. Added a regression test returning
`wallet_changed_before_credit` history alongside a rejected initial
lookup; all 685 Console tests and lint/typecheck/build pass in the Node
24 devcontainer.
```

### PR Body

## Summary
Customers who pay for Platform usage through an offline contract can now receive the purchased balance through the staff Console. Staff find an active Platform Organization in a paginated, searchable list, enter a USD amount and internal note, and confirm the recharge. The Org detail view shows its current balance and individual recharge records. Recharge history loads independently of the balance lookup, so staff can inspect manual-review records during a wallet or gateway failure; recharge controls remain hidden until the first balance lookup succeeds.

The API requires verified SRP staff identity plus the current superadmin email allowlist. Manual credits use the existing Org wallet and durable fulfillment flow: the order and operator audit are recorded before delivery, a persisted claim allows only one wallet POST, and an uncertain result is reconciled rather than reposted. The Console generates and retains the operation reference for same-attempt retries and reloads. Offline paid credits count as prior paid purchases without starting Stripe Checkout or granting a card reward; complimentary credits remain a separate API/storage source.

Customer billing displays both online and offline purchases as **Top-up**. Internal source, operator, reference and note remain separate; staff details are not returned to customers. No commercial subscription or changes to Billing Gateway/account-service APIs are introduced.

## Test plan
- [x] Rebase onto current `origin/main`; run local `ecap-verify-py-ci`: 12,213 passed / 5 skipped, 89.57% coverage; Linux dependency resolution, static checks, ci-lint and source/test duplication checks passed.
- [x] Console: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test` (685 passed), `pnpm build`.
- [x] Platform: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test` (283 passed), `pnpm build`. Two render-wait failures during concurrent local verification passed on targeted and full reruns without code or timeout changes.
- [x] Verify actual repository operations through staging CSFLE: manual-order insert/read/CAS/history/list in an isolated disposable fixture, plus read-only Org pagination and literal name/ID/owner search.
- [x] Devcontainer integration: authenticated staff lookup, isolated test Org with its real staging wallet, customer top-up history, and desktop/mobile Console flow. The tester confirmed a $1 offline top-up and its customer balance/history.

## Rollout
Deploy the backend on every API replica and recovery worker before exposing the Console action: older strict order readers cannot decode manual-credit fields. New Stripe orders retain their existing persisted shape. No deployment or production data write is included in this PR.

## Review disposition
Previous GitHub CI checks passed. Codex review reported no findings. Claude noted that a concurrent `updated_at` change can prevent the redundant order-local `manual.repeated_confirmation` history entry from being appended. This is left unchanged: every `grant()` invocation separately appends global requested/outcome audit events with distinct audit IDs, so the retry operator, target, reference and outcome remain durably recorded even on that CAS miss; delivery also re-reads current state and retains the one-POST guarantee. The order-local history caveat is retained for human review.


Tim's first-load balance failure finding is fixed in `0b0916eb0`: history is mounted directly from the selected Org ID, while the balance error and reload action remain visible and the recharge form is withheld without account data. Added a regression test returning `wallet_changed_before_credit` history alongside a rejected initial lookup; all 685 Console tests and lint/typecheck/build pass in the Node 24 devcontainer.


---

## fix(claw-interface): release Mattermost seats on agent uninstall (#4025)

- **SHA**: `cd4fca3ecdc6c0c5db2c614021a91f378365b695`
- **作者**: tim-srp
- **日期**: 2026-10-12T11:20:47Z
- **PR**: #4025

### Commit Message

```
fix(claw-interface): release Mattermost seats on agent uninstall (#4025)

## Summary

Release the Mattermost Org-team seat held by an Agent Bot when a user
uninstalls an Engine Agent or deletes it from Agent development **after
this release**, without raising the Team member limit. Historical orphan
data is out of scope. This is a **draft** until the staging/CSFLE gates
below are checked.

- **Covered paths:** the ordinary Engine Agent uninstall and the
Agent-development delete. Both finish in `uninstall_engine_agent`, which
now persists an `integration_cleanup` record atomically with the
terminal workspace state. One attempt runs inline; the existing
scheduler pattern retries due rows with a Mongo lease, backoff and
recorded stage/error; rows past 12 attempts stay queryable and keep
retrying daily.
- Cleanup removes the Agent's ACS channel binding and leaves the Org
Team unless a live Pack Test run or another workspace row that is or can
become active still names the Bot (any computer-runtime row keeps the
seat, fail-safe). Retired Engine co-owners never block, because Engine
tombstones are never reclaimed. For an Engine sole owner the Bot's
access tokens are also revoked. Bot accounts, channels and historical
posts are retained.
- Cleanups that fail 12 times keep retrying daily and raise one
aggregate PagerDuty incident (`agent-integration-cleanup-stuck`) that
auto-resolves when they converge.
- **Not covered:** the service-token `DELETE /service/v1/agents/{id}`
route is unchanged from `main` (Engine delete plus best-effort ACS
channel cleanup). An Agent deleted there does not enter this cleanup;
that route is left for a separate change.

## Scope changes after merging main

- **Merged `origin/main` (#4028, FastClaw V1 removal).** #4028 deleted
the retired computer-runtime uninstall path
(`agent_uninstall_service.py`) and `mattermost_reconcile.py`, so this
PR's computer-runtime pieces went with them: the channel stage is
Engine-only (a no-op for computer-runtime rows), and the
computer-runtime reinstall fence (`install_claim_filter` /
`_INSTALL_SET_FIELDS` changes and the reinstall-race test) was reverted
to `main`, since no retained flow reinstalls those rows.
- **`ed811e17`: the service-token delete route is left unchanged.** The
earlier delete-intent flow for that route was removed to keep this PR to
the uninstall paths: `engine_delete_intent_service` and its tests, the
`reconcile_engine_delete_intents` job, the `engine_delete_intent` field
and index, and the retire/intent repo functions.
`app/routes/service_api/_agents.py` is identical to `main`, and the
stuck alert counts integration cleanups only.

## Root cause

Normal Agent uninstalls stopped the Agent and removed or soft-deleted
channel resources but never removed the associated Mattermost Bot from
the Org Team. Repeated create → chat → uninstall cycles accumulated Team
members and eventually blocked a new Bot's first Team join. Old open PR
#3567 documents the same leak for Pack Test and explicitly notes
ordinary Agent uninstalls as a separate gap; this PR addresses the
ordinary uninstall paths on current `main`.

## Test plan

Re-run on `ed811e17` unless noted:

- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, import-linter)
- [x] Backend ci-lint guards (8/8)
- [x] Full backend unit suite: 11,962 passed, 5 skipped, 0 failed
- [x] Full BDD suite against local MongoDB: 255 passed, 0 failed, 0
skipped
- [x] Focused tests for shared Bots (incl. retired Engine co-owners),
Engine token revocation, Pack Test ownership, idempotency, partial
failure / backoff / daily retry / alerting, lease exclusion and stage
fencing
- [x] Staging CSFLE validation on the existing claw-interface Pod, run
on the pre-merge sources (`b667c5c6`): PR database sources exercised
against two isolated, randomly named temporary collections (74/74 query,
CAS, write, and index checks passed); both collections were dropped and
their absence verified. A separate read-only check found no collection
validators or field-encryption rules on the two real collections. The PR
application code itself is not deployed. Since then the remaining query
forms are unchanged; the delete-intent queries were removed and the
install claim filter is back to `main`.
- [ ] Staging acceptance: repeat create → chat → uninstall, and create →
chat → Agent-development delete; verify Team count returns to baseline
for sole-owner Bots, history remains and an Engine reinstall provisions
a fresh Bot. Shared Bot seats should remain.

## Known limitations

- **The service-token `DELETE /service/v1/agents/{id}` route is out of
scope.** It keeps `main`'s behavior, so an Engine Agent deleted through
it still keeps its Org-team seat.
- **Bot accounts are not deactivated or deleted, and computer-runtime
Bot tokens are kept.** Engine sole-owner tokens are revoked. Account
deactivation awaits a product decision.
- **A shared Bot whose remaining co-owner is a computer-runtime row
keeps its seat** (fail-safe). A V1-to-V2 migration writer outside this
repository could create a new owner during cleanup; that operational
race is not controlled here.
- Pre-terminal `uninstall_failed` (for example Engine stop failure)
still requires a user retry. Engine uninstall stays stop-only (Sandbox
paused, not released via `:cleanup`) pending a product decision.
- ACS listing of soft-deleted channels still needs staging confirmation.

No real business collections or production data were mutated, and the PR
was not deployed. The staging probe created and removed only two
isolated temporary collections; zero remained after verification.

🤖 Implemented and reviewed with [Claude
Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Release the Mattermost Org-team seat held by an Agent Bot when a user uninstalls an Engine Agent or deletes it from Agent development **after this release**, without raising the Team member limit. Historical orphan data is out of scope. This is a **draft** until the staging/CSFLE gates below are checked.

- **Covered paths:** the ordinary Engine Agent uninstall and the Agent-development delete. Both finish in `uninstall_engine_agent`, which now persists an `integration_cleanup` record atomically with the terminal workspace state. One attempt runs inline; the existing scheduler pattern retries due rows with a Mongo lease, backoff and recorded stage/error; rows past 12 attempts stay queryable and keep retrying daily.
- Cleanup removes the Agent's ACS channel binding and leaves the Org Team unless a live Pack Test run or another workspace row that is or can become active still names the Bot (any computer-runtime row keeps the seat, fail-safe). Retired Engine co-owners never block, because Engine tombstones are never reclaimed. For an Engine sole owner the Bot's access tokens are also revoked. Bot accounts, channels and historical posts are retained.
- Cleanups that fail 12 times keep retrying daily and raise one aggregate PagerDuty incident (`agent-integration-cleanup-stuck`) that auto-resolves when they converge.
- **Not covered:** the service-token `DELETE /service/v1/agents/{id}` route is unchanged from `main` (Engine delete plus best-effort ACS channel cleanup). An Agent deleted there does not enter this cleanup; that route is left for a separate change.

## Scope changes after merging main

- **Merged `origin/main` (#4028, FastClaw V1 removal).** #4028 deleted the retired computer-runtime uninstall path (`agent_uninstall_service.py`) and `mattermost_reconcile.py`, so this PR's computer-runtime pieces went with them: the channel stage is Engine-only (a no-op for computer-runtime rows), and the computer-runtime reinstall fence (`install_claim_filter` / `_INSTALL_SET_FIELDS` changes and the reinstall-race test) was reverted to `main`, since no retained flow reinstalls those rows.
- **`ed811e17`: the service-token delete route is left unchanged.** The earlier delete-intent flow for that route was removed to keep this PR to the uninstall paths: `engine_delete_intent_service` and its tests, the `reconcile_engine_delete_intents` job, the `engine_delete_intent` field and index, and the retire/intent repo functions. `app/routes/service_api/_agents.py` is identical to `main`, and the stuck alert counts integration cleanups only.

## Root cause

Normal Agent uninstalls stopped the Agent and removed or soft-deleted channel resources but never removed the associated Mattermost Bot from the Org Team. Repeated create → chat → uninstall cycles accumulated Team members and eventually blocked a new Bot's first Team join. Old open PR #3567 documents the same leak for Pack Test and explicitly notes ordinary Agent uninstalls as a separate gap; this PR addresses the ordinary uninstall paths on current `main`.

## Test plan

Re-run on `ed811e17` unless noted:

- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, import-linter)
- [x] Backend ci-lint guards (8/8)
- [x] Full backend unit suite: 11,962 passed, 5 skipped, 0 failed
- [x] Full BDD suite against local MongoDB: 255 passed, 0 failed, 0 skipped
- [x] Focused tests for shared Bots (incl. retired Engine co-owners), Engine token revocation, Pack Test ownership, idempotency, partial failure / backoff / daily retry / alerting, lease exclusion and stage fencing
- [x] Staging CSFLE validation on the existing claw-interface Pod, run on the pre-merge sources (`b667c5c6`): PR database sources exercised against two isolated, randomly named temporary collections (74/74 query, CAS, write, and index checks passed); both collections were dropped and their absence verified. A separate read-only check found no collection validators or field-encryption rules on the two real collections. The PR application code itself is not deployed. Since then the remaining query forms are unchanged; the delete-intent queries were removed and the install claim filter is back to `main`.
- [ ] Staging acceptance: repeat create → chat → uninstall, and create → chat → Agent-development delete; verify Team count returns to baseline for sole-owner Bots, history remains and an Engine reinstall provisions a fresh Bot. Shared Bot seats should remain.

## Known limitations

- **The service-token `DELETE /service/v1/agents/{id}` route is out of scope.** It keeps `main`'s behavior, so an Engine Agent deleted through it still keeps its Org-team seat.
- **Bot accounts are not deactivated or deleted, and computer-runtime Bot tokens are kept.** Engine sole-owner tokens are revoked. Account deactivation awaits a product decision.
- **A shared Bot whose remaining co-owner is a computer-runtime row keeps its seat** (fail-safe). A V1-to-V2 migration writer outside this repository could create a new owner during cleanup; that operational race is not controlled here.
- Pre-terminal `uninstall_failed` (for example Engine stop failure) still requires a user retry. Engine uninstall stays stop-only (Sandbox paused, not released via `:cleanup`) pending a product decision.
- ACS listing of soft-deleted channels still needs staging confirmation.

No real business collections or production data were mutated, and the PR was not deployed. The staging probe created and removed only two isolated temporary collections; zero remained after verification.

🤖 Implemented and reviewed with [Claude Code](https://claude.com/claude-code)


---

## fix(schedules): attest owner-checked Web cron writes (#4055)

- **SHA**: `38521dc252fce583d6b3e2607312afc64dde147f`
- **作者**: kaka-srp
- **日期**: 2026-10-12T09:16:36Z
- **PR**: #4055

### Commit Message

```
fix(schedules): attest owner-checked Web cron writes (#4055)

Web-created schedules currently reach Engine as unproved management
writes, so the worker cannot distinguish the authenticated Agent owner
from an org service-API caller. Send `x-zooclaw-owner-driven: true` only
from the existing Web schedule create/update service after its workspace
UID/org ownership check succeeds.

The client option defaults to false; generic org service-API forwarding
continues to rebuild upstream headers and cannot relay a caller-supplied
owner assertion. No frontend changes or database migration.

Companion Engine implementation:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1961 (related
to Engine #1738 and the cron part of #1739). New owner-checked Web
creation records owner authority; updates only preserve an existing
mark, never add or restore a missing one. Old tasks require owner
recreation. Heartbeat is outside this change.

Validation: 76 targeted schedule client/service/routes and authenticated
service-API tests passed; `scripts/verify-py.sh` and
`scripts/verify-changed.sh` passed (ruff, formatting, pyright and import
boundaries). Tests cover workspace owner/org mismatch, explicit header
emission and stripping forged headers from service API requests. CI
passed, including 12,192 Python tests (5 existing skips) and both
automated reviews.

Rollout: Engine controld support → this backend header → Engine worker
memory gate. All old workers must be replaced to close the runtime
vulnerability. Neither PR is a deployment.
```

### PR Body

Web-created schedules currently reach Engine as unproved management writes, so the worker cannot distinguish the authenticated Agent owner from an org service-API caller. Send `x-zooclaw-owner-driven: true` only from the existing Web schedule create/update service after its workspace UID/org ownership check succeeds.

The client option defaults to false; generic org service-API forwarding continues to rebuild upstream headers and cannot relay a caller-supplied owner assertion. No frontend changes or database migration.

Companion Engine implementation: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1961 (related to Engine #1738 and the cron part of #1739). New owner-checked Web creation records owner authority; updates only preserve an existing mark, never add or restore a missing one. Old tasks require owner recreation. Heartbeat is outside this change.

Validation: 76 targeted schedule client/service/routes and authenticated service-API tests passed; `scripts/verify-py.sh` and `scripts/verify-changed.sh` passed (ruff, formatting, pyright and import boundaries). Tests cover workspace owner/org mismatch, explicit header emission and stripping forged headers from service API requests. CI passed, including 12,192 Python tests (5 existing skips) and both automated reviews.

Rollout: Engine controld support → this backend header → Engine worker memory gate. All old workers must be replaced to close the runtime vulnerability. Neither PR is a deployment.


---

## fix(chat-ui): avoid Windows file-type dropdown hang (#4051)

- **SHA**: `115f5c10e987fd243f06ddebfa35b939599dbfa5`
- **作者**: siqiao-srp
- **日期**: 2026-10-12T08:05:24Z
- **PR**: #4051

### Commit Message

```
fix(chat-ui): avoid Windows file-type dropdown hang (#4051)

## Summary
- On Windows, open the chat attachment picker with All files instead of
the long Custom Files filter. A user reported that hovering/clicking the
native file-type dropdown freezes Edge before selecting or uploading a
file.
- Remove the accept attribute synchronously before opening the picker;
retain existing filters on other platforms and preserve attachment
callbacks and disabled/uploading guards.
- This applies to all Windows chat-composer pickers. The existing upload
handlers continue to check size/count; this change does not add
file-type validation. The original native picker already offered All
files.

## Root cause
The chat accept list contains image/audio/video wildcards plus
document/archive extensions. Chromium expands these into a long native
filter. Mozilla bug 1881950 documents the same dropdown/tooltip hang in
Edge and Chromium when the resulting window crosses monitors with
different DPI scaling:
https://bugzilla.mozilla.org/show_bug.cgi?id=1881950#c9

This is a matching upstream failure mode, not a confirmed diagnosis of
the customer's machine: monitor configuration and Windows/Edge versions
have not yet been supplied. The patch avoids that filter path and needs
native Windows validation before production release.

## Test plan
- [x] Composer regression suite: 54 tests passed.
- [x] Chat UI TypeScript and targeted ESLint checks passed.
- [x] Real Chrome on macOS: 30 repeated ZIP+PNG selections across
Windows, macOS, and Android user-agent scenarios; default/custom
actions, changed accept prop, input reset, and disabled/uploading guards
passed. Platform identities were simulated and filechooser events
intercepted; these tests do not exercise native Windows dialogs or
backend upload delivery.
- [x] Deployed commit 0f2e22c to staging; /api/version confirms the
revision and the page returns HTTP 200.
- [ ] On the affected Windows Edge machine, repeatedly hover/click the
All files dropdown, including near monitor boundaries, then upload the
original ZIPs and an image and send the message.

Staging: https://ecap.gensmo.nosay.live/
Deployment:
https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/38031648866
```

### PR Body

## Summary
- On Windows, open the chat attachment picker with All files instead of the long Custom Files filter. A user reported that hovering/clicking the native file-type dropdown freezes Edge before selecting or uploading a file.
- Remove the accept attribute synchronously before opening the picker; retain existing filters on other platforms and preserve attachment callbacks and disabled/uploading guards.
- This applies to all Windows chat-composer pickers. The existing upload handlers continue to check size/count; this change does not add file-type validation. The original native picker already offered All files.

## Root cause
The chat accept list contains image/audio/video wildcards plus document/archive extensions. Chromium expands these into a long native filter. Mozilla bug 1881950 documents the same dropdown/tooltip hang in Edge and Chromium when the resulting window crosses monitors with different DPI scaling:
https://bugzilla.mozilla.org/show_bug.cgi?id=1881950#c9

This is a matching upstream failure mode, not a confirmed diagnosis of the customer's machine: monitor configuration and Windows/Edge versions have not yet been supplied. The patch avoids that filter path and needs native Windows validation before production release.

## Test plan
- [x] Composer regression suite: 54 tests passed.
- [x] Chat UI TypeScript and targeted ESLint checks passed.
- [x] Real Chrome on macOS: 30 repeated ZIP+PNG selections across Windows, macOS, and Android user-agent scenarios; default/custom actions, changed accept prop, input reset, and disabled/uploading guards passed. Platform identities were simulated and filechooser events intercepted; these tests do not exercise native Windows dialogs or backend upload delivery.
- [x] Deployed commit 0f2e22c to staging; /api/version confirms the revision and the page returns HTTP 200.
- [ ] On the affected Windows Edge machine, repeatedly hover/click the All files dropdown, including near monitor boundaries, then upload the original ZIPs and an image and send the message.

Staging: https://ecap.gensmo.nosay.live/
Deployment: https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/38031648866


---
