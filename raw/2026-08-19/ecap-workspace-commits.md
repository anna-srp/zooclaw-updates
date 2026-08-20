# SerendipityOneInc/ecap-workspace commits 2026-08-19

## b275b11d

- author: tim-srp
- date: 2026-08-19T15:15:52Z
- pr: 3447


### commit message

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


### PR body

## Summary
- 生产实锤：`payment_intent.succeeded` 事件比 Airwallex 写入 checkout `subscription_id` 早 ~5 秒到达，处理时 checkout 尚无订阅 → `event_not_supported` → 重投耗尽 → trial 订单永远 pending（`cardorder:034ef647`，checkout `bco_uspdfkhxhhlhq51leki` 15:01:43 事件 vs 15:01:48 订阅创建）。

## 修复
- checkout 检索在无 `subscription_id` 时短暂重试（3 次 × 2 秒），覆盖观测到的创建延迟窗口；重试后仍缺失才抛可重投错误。

## 验证
- [x] 新增回归测试：第一次读无订阅、第二次读有 → 结算成功且 checkout 读取 2 次（先红后绿）
- [x] payment_events / lifecycle / replacement 66 全绿
- [x] pre-commit 全过（ruff / pyright / import-linter）



### files

- services/claw-interface/app/services/airwallex/payment_events.py
- services/claw-interface/tests/unit/test_airwallex_payment_events.py

---

## 31c2611e

- author: tim-srp
- date: 2026-08-19T14:58:01Z
- pr: 3446


### commit message

```
fix(billing): advertise Airwallex as the vertical pack card provider (#3446)

## Summary
- 垂直包购买入口在 Airwallex 就绪时，**Restaurant 计划**默认走 Airwallex；其它计划保持原 Stripe
通道。

## Root cause
`purchase-capability` 路由硬编码 `card_provider="stripe"/"creem"`，从未查询
Airwallex 就绪 gate。生产 Stripe 账号未激活 → 购买 502。已验证生产与 staging 的 gate
输入全部满足——非配置问题，纯代码问题。

## 修复（含 P0 review 修正）
- capability：Airwallex 就绪 **且为 Restaurant 计划**时返回
`airwallex`（购买路径对其它计划会拒绝 Airwallex，宣告会使其确定性失败）；否则回退旧 stripe/creem 逻辑
- 前端：Airwallex 与 Creem 同规则——**带 add-on 时禁用 Card**（Airwallex catalog 拒绝非零
add-on）
- 前后端类型同步支持 `"airwallex"`

## 验证
- [x] capability 测试先红后绿：Restaurant+airwallex 就绪 → airwallex；非 Restaurant
计划 → 回退 stripe；未就绪回退旧逻辑（24 全绿）
- [x] 前端新增 Airwallex add-on 禁用测试（CI 把关）
- [x] ruff / pyright / import-linter 全过

---------

Co-authored-by: Claude <noreply@anthropic.com>
```


### PR body


## Summary
- 垂直包购买入口在 Airwallex 就绪时，**Restaurant 计划**默认走 Airwallex；其它计划保持原 Stripe 通道。

## Root cause
`purchase-capability` 路由硬编码 `card_provider="stripe"/"creem"`，从未查询 Airwallex 就绪 gate。生产 Stripe 账号未激活 → 购买 502。已验证生产与 staging 的 gate 输入全部满足——非配置问题，纯代码问题。

## 修复（含 P0 review 修正）
- capability：Airwallex 就绪 **且为 Restaurant 计划**时返回 `airwallex`（购买路径对其它计划会拒绝 Airwallex，宣告会使其确定性失败）；否则回退旧 stripe/creem 逻辑
- 前端：Airwallex 与 Creem 同规则——**带 add-on 时禁用 Card**（Airwallex catalog 拒绝非零 add-on）
- 前后端类型同步支持 `"airwallex"`

## 验证
- [x] capability 测试先红后绿：Restaurant+airwallex 就绪 → airwallex；非 Restaurant 计划 → 回退 stripe；未就绪回退旧逻辑（24 全绿）
- [x] 前端新增 Airwallex add-on 禁用测试（CI 把关）
- [x] ruff / pyright / import-linter 全过


### files

- services/claw-interface/app/routes/vertical_pack/plan.py
- services/claw-interface/app/schema/vertical_pack_plans.py
- services/claw-interface/tests/unit/test_vertical_pack_plans_routes.py
- web/enterprise-admin/app/vertical-pack-plan/[planId]/checkout/__tests__/checkout-page.test.tsx
- web/enterprise-admin/app/vertical-pack-plan/[planId]/checkout/useCheckoutViewModel.ts
- web/enterprise-admin/types/vertical-pack-checkout.ts

---

## bc29f78d

- author: tim-srp
- date: 2026-08-19T14:03:51Z
- pr: 3444


### commit message

```
fix(billing): make vertical pack settlement fences compatible with encryption (#3444)

## Summary
- Replace the initial-settlement CAS fence's `$or` predicates with `$in`
(containing `null`), which the MongoDB client-side field-level
encryption library (crypt_shared) accepts during query analysis on
encrypted collections.
- Carry `provider_status=completed` on the rebuilt payment-order
document so the post-record identity check passes.

## Root cause
Live staging verification of the vertical pack settlement (#3442's
routing fix) exposed two defects in the enterprise settlement itself.
After a successful Restaurant vertical pack payment, every
`payment_intent.succeeded` redelivery failed:

1. **`MongoCryptError: unknown operator: $or`** — `_cas_empty_or_equal`
built the empty-or-equal fence as an `$or` union of exists/null/equality
branches. crypt_shared rejects `$or` during query analysis on encrypted
collections, so the guarded payment-order write always failed. `$in`
containing `null` matches absent, null, and equal values identically and
passes the analysis (both verified live against the staging collection).
2. **`enterprise_payment_conflict` after a successful CAS write** — the
checkout binding writes `provider_status=completed` onto the pending
order, but the settlement's rebuilt payment-order document omitted it,
so `_initial_order_matches` always rejected the projection.

## Verification
The full settlement chain was verified live in staging (with the fixes
applied): order `succeeded`, agreement `active`, and 20 000 team credits
granted via billing-gateway (`bg_granted_at` recorded).

## Test plan
- [x] `pytest tests/unit/test_airwallex_enterprise_subscription.py` — 18
passed (2 new regression tests: fence contains no `$or`; record carries
`provider_status=completed`)
- [x] Regression: `test_airwallex_payment_events.py` +
`test_airwallex_lifecycle.py` + `test_airwallex_enterprise_checkout.py`
— 80 passed total
- [x] `ruff check` + `ruff format --check` clean
- [x] pyright clean on changed files (0 errors, 0 warnings)

Co-authored-by: Claude <noreply@anthropic.com>
```


### PR body

## Summary
- Replace the initial-settlement CAS fence's `$or` predicates with `$in` (containing `null`), which the MongoDB client-side field-level encryption library (crypt_shared) accepts during query analysis on encrypted collections.
- Carry `provider_status=completed` on the rebuilt payment-order document so the post-record identity check passes.

## Root cause
Live staging verification of the vertical pack settlement (#3442's routing fix) exposed two defects in the enterprise settlement itself. After a successful Restaurant vertical pack payment, every `payment_intent.succeeded` redelivery failed:

1. **`MongoCryptError: unknown operator: $or`** — `_cas_empty_or_equal` built the empty-or-equal fence as an `$or` union of exists/null/equality branches. crypt_shared rejects `$or` during query analysis on encrypted collections, so the guarded payment-order write always failed. `$in` containing `null` matches absent, null, and equal values identically and passes the analysis (both verified live against the staging collection).
2. **`enterprise_payment_conflict` after a successful CAS write** — the checkout binding writes `provider_status=completed` onto the pending order, but the settlement's rebuilt payment-order document omitted it, so `_initial_order_matches` always rejected the projection.

## Verification
The full settlement chain was verified live in staging (with the fixes applied): order `succeeded`, agreement `active`, and 20 000 team credits granted via billing-gateway (`bg_granted_at` recorded).

## Test plan
- [x] `pytest tests/unit/test_airwallex_enterprise_subscription.py` — 18 passed (2 new regression tests: fence contains no `$or`; record carries `provider_status=completed`)
- [x] Regression: `test_airwallex_payment_events.py` + `test_airwallex_lifecycle.py` + `test_airwallex_enterprise_checkout.py` — 80 passed total
- [x] `ruff check` + `ruff format --check` clean
- [x] pyright clean on changed files (0 errors, 0 warnings)



### files

- services/claw-interface/app/services/airwallex/enterprise_payment.py
- services/claw-interface/tests/unit/test_airwallex_enterprise_subscription.py

---

## 99d627f0

- author: rayhuang198212
- date: 2026-08-19T13:50:04Z
- pr: 3411


### commit message

```
test(e2e): align core suites with current application flows (#3411)

## Summary

- Align core E2E scenarios with the current chat, settings,
landing-page, theme, keyboard, and i18n behavior.
- Start `basic-usage` scenarios from `/new-chat` instead of sending the
legacy `/new` command.
- Support both launcher and session composers when entering messages,
uploading attachments, and detecting successful submission.
- Improve current-response tracking for asynchronous text and media
messages.
- Run landing-page coverage with anonymous browser state and remove
obsolete UI assertions and helpers.
- Allow the E2E LLM Judge model/service ID to be configured through
`LLM_JUDGE_MODEL`.

  ## Validation

  - ESLint passed for the updated E2E files.
  - TypeScript `tsc --noEmit` passed.
  - `git diff --check` passed.
- Core `basic-usage` flows successfully reached staging chat and
media-generation results from `/new-chat`.
```


### PR body

## Summary

  - Align core E2E scenarios with the current chat, settings, landing-page, theme, keyboard, and i18n behavior.
  - Start `basic-usage` scenarios from `/new-chat` instead of sending the legacy `/new` command.
  - Support both launcher and session composers when entering messages, uploading attachments, and detecting successful submission.
  - Improve current-response tracking for asynchronous text and media messages.
  - Run landing-page coverage with anonymous browser state and remove obsolete UI assertions and helpers.
  - Allow the E2E LLM Judge model/service ID to be configured through `LLM_JUDGE_MODEL`.

  ## Validation

  - ESLint passed for the updated E2E files.
  - TypeScript `tsc --noEmit` passed.
  - `git diff --check` passed.
  - Core `basic-usage` flows successfully reached staging chat and media-generation results from `/new-chat`.


### files

- .env.example
- web/app/playwright.config.ts
- web/app/tests/e2e/fixtures/shared-session.ts
- web/app/tests/e2e/page-objects/claw-settings.page.ts
- web/app/tests/e2e/page-objects/zooclaw-chat.page.ts
- web/app/tests/e2e/specs/chat-smoke.spec.ts
- web/app/tests/e2e/specs/claw-settings.spec.ts
- web/app/tests/e2e/specs/dark-mode-smoke.spec.ts
- web/app/tests/e2e/specs/dark-mode-tokens.spec.ts
- web/app/tests/e2e/specs/i18n-switching.spec.ts
- web/app/tests/e2e/specs/keyboard-accessibility.spec.ts
- web/app/tests/e2e/specs/landing-page.spec.ts
- web/app/tests/e2e/specs/scenarios/basic-usage.spec.ts
- web/app/tests/e2e/utils/llm-judge.ts
- web/app/tests/e2e/utils/onboarding.ts

---

## ac48e41a

- author: tim-srp
- date: 2026-08-19T13:38:47Z
- pr: 3443


### commit message

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


### PR body

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



### files

- services/claw-interface/app/services/airwallex/replacement.py
- services/claw-interface/tests/unit/test_airwallex_replacement.py

---

## d3e1701f

- author: tim-srp
- date: 2026-08-19T13:26:48Z
- pr: 3442


### commit message

```
fix(billing): settle vertical pack checkout payments on the enterprise path (#3442)

## Summary
- Route `payment_intent.succeeded` settlement for enterprise vertical
pack checkout orders to the enterprise projection instead of the
standard first-payment projection.
- Add a regression test pinning the routing (enterprise order →
enterprise settlement, standard projections untouched).

## Root cause
Real Airwallex delivery for a hosted checkout is payment-class: the
provider sends `payment_intent.succeeded` with `merchant_order_id`
shaped `"[bco]<checkout_id>"` and no subscription lifecycle event
(#3432). That handler always settled through
`settle_airwallex_first_subscription_payment`, which resolves the plan
from `order["plan"]`. Vertical pack checkout orders carry `plan=None`
(they read amount/credits from the enterprise package snapshot), so
every settlement attempt failed with:

```text
billing.airwallex.projection.unknown_plan — "The Card checkout order carries an unknown plan"
```

The webhook kept failing (observed live in staging after a successful
Restaurant vertical pack payment): the order stayed pending, no
agreement was created, and no team credits were granted.

## Fix
In `settle_airwallex_checkout_payment`, dispatch
`is_enterprise_package_order(order)` to the enterprise settlement path,
binding provider subscription facts to the checkout order first
(mirroring `_settle_enterprise_period_if_applicable` in the lifecycle
dispatcher) so the enterprise fences (`provider_subscription_id`,
`provider_status=completed`) hold.

## Test plan
- [x] `pytest tests/unit/test_airwallex_payment_events.py` — 13 passed
(1 new regression test)
- [x] Regression: `test_airwallex_enterprise_subscription.py` +
`test_airwallex_lifecycle.py` + `test_airwallex_enterprise_checkout.py`
+ `test_airwallex_config.py` — 117 passed total
- [x] `ruff check` + `ruff format --check` clean
- [x] pyright clean on changed files (0 errors, 0 warnings)

Co-authored-by: Claude <noreply@anthropic.com>
```


### PR body

## Summary
- Route `payment_intent.succeeded` settlement for enterprise vertical pack checkout orders to the enterprise projection instead of the standard first-payment projection.
- Add a regression test pinning the routing (enterprise order → enterprise settlement, standard projections untouched).

## Root cause
Real Airwallex delivery for a hosted checkout is payment-class: the provider sends `payment_intent.succeeded` with `merchant_order_id` shaped `"[bco]<checkout_id>"` and no subscription lifecycle event (#3432). That handler always settled through `settle_airwallex_first_subscription_payment`, which resolves the plan from `order["plan"]`. Vertical pack checkout orders carry `plan=None` (they read amount/credits from the enterprise package snapshot), so every settlement attempt failed with:

```text
billing.airwallex.projection.unknown_plan — "The Card checkout order carries an unknown plan"
```

The webhook kept failing (observed live in staging after a successful Restaurant vertical pack payment): the order stayed pending, no agreement was created, and no team credits were granted.

## Fix
In `settle_airwallex_checkout_payment`, dispatch `is_enterprise_package_order(order)` to the enterprise settlement path, binding provider subscription facts to the checkout order first (mirroring `_settle_enterprise_period_if_applicable` in the lifecycle dispatcher) so the enterprise fences (`provider_subscription_id`, `provider_status=completed`) hold.

## Test plan
- [x] `pytest tests/unit/test_airwallex_payment_events.py` — 13 passed (1 new regression test)
- [x] Regression: `test_airwallex_enterprise_subscription.py` + `test_airwallex_lifecycle.py` + `test_airwallex_enterprise_checkout.py` + `test_airwallex_config.py` — 117 passed total
- [x] `ruff check` + `ruff format --check` clean
- [x] pyright clean on changed files (0 errors, 0 warnings)



### files

- services/claw-interface/app/services/airwallex/payment_events.py
- services/claw-interface/tests/unit/test_airwallex_payment_events.py

---

## 122b4b58

- author: tim-srp
- date: 2026-08-19T13:08:21Z
- pr: 3441


### commit message

```
fix(billing): allow airwallex in vertical pack purchase response provider (#3441)

## Summary
- Allow `airwallex` in the vertical pack purchase response provider
(backend `VerticalPackCheckoutProvider` Literal + matching frontend
type).

## Root cause
`purchase_plan` routes the Restaurant vertical pack Card checkout to
AIRWALLEX and returns `provider=airwallex`, but the response schema
`VerticalPackCheckoutProvider` only allowed `stripe` / `creem` /
`antom`. Every successful checkout creation therefore failed at response
serialization with HTTP 500 (observed live in staging):

```text
pydantic_core._pydantic_core.ValidationError: 1 validation error for VerticalPackPlanPurchaseResponse
provider
  Input should be 'stripe', 'creem' or 'antom' [type=literal_error, input_value='airwallex', input_type=str]
```

The checkout itself was already created before the response crashed, so
the buyer also hit the same 500 on retry instead of the replayed URL.

## Test plan
- [x] `pytest tests/unit/test_vertical_pack_plans_routes.py` — 22 passed
(1 new test: purchase response accepts `provider=airwallex`)
- [x] `ruff check` + `ruff format --check` clean on changed files
- [ ] Frontend type change verified in CI (`enterprise-admin-quality`;
local tsc unavailable in this worktree)

Co-authored-by: Claude <noreply@anthropic.com>
```


### PR body

## Summary
- Allow `airwallex` in the vertical pack purchase response provider (backend `VerticalPackCheckoutProvider` Literal + matching frontend type).

## Root cause
`purchase_plan` routes the Restaurant vertical pack Card checkout to AIRWALLEX and returns `provider=airwallex`, but the response schema `VerticalPackCheckoutProvider` only allowed `stripe` / `creem` / `antom`. Every successful checkout creation therefore failed at response serialization with HTTP 500 (observed live in staging):

```text
pydantic_core._pydantic_core.ValidationError: 1 validation error for VerticalPackPlanPurchaseResponse
provider
  Input should be 'stripe', 'creem' or 'antom' [type=literal_error, input_value='airwallex', input_type=str]
```

The checkout itself was already created before the response crashed, so the buyer also hit the same 500 on retry instead of the replayed URL.

## Test plan
- [x] `pytest tests/unit/test_vertical_pack_plans_routes.py` — 22 passed (1 new test: purchase response accepts `provider=airwallex`)
- [x] `ruff check` + `ruff format --check` clean on changed files
- [ ] Frontend type change verified in CI (`enterprise-admin-quality`; local tsc unavailable in this worktree)



### files

- services/claw-interface/app/schema/vertical_pack_plans.py
- services/claw-interface/tests/unit/test_vertical_pack_plans_routes.py
- web/enterprise-admin/types/vertical-pack-checkout.ts

---

## 2afc8745

- author: kaka-srp
- date: 2026-08-19T12:55:15Z
- pr: 3438


### commit message

```
feat(chat): add Codex-style agent activity timeline (#3438)

## Linear

N/A — 按需求不创建 Linear issue。

## Summary

- 将 Main Chat、Session Thread、Agent Builder 和 Preview/Test Chat 统一为 Codex
风格的 `commentary → activity → final answer` 时间线，并复用
`zooclaw-design-system` 的 disclosure、item、spinner 和 alert 组件。
- 完成当前 v2 工具面与实际返回通道盘点；activity 只展示工具级正向 allowlist 中的调用意图，以及
command/patch/plan 的安全运行时投影，不再展示 Web、文件、MCP、Composio、内存等工具的 raw result
preview。
- 保留运行、完成、失败、取消、真实耗时、长步骤折叠和 Agent 身份连续性，并在消息区出现可渲染事件后接管 composer
activity 状态。
- 保持 Markdown、附件、Artifact、交互卡片、分享和 legacy Mattermost 历史兼容；设计与工具输出契约记录在本
PR 的 spec 中。

## Test plan

- [x] `bash scripts/verify-web.sh --no-clean <10 related unit specs>` —
10 files / 326 tests passed，包含 TypeScript、ESLint 与 governance guards。
- [x] `cd web/packages/chat-ui && pnpm test && pnpm tsc && pnpm lint` —
33 files / 431 tests passed。
- [x] `bash scripts/verify-changed.sh` — all changed surfaces passed
after merging latest `origin/main`。
- [x] `git diff --check origin/main...HEAD`。
```


### PR body

## Linear

N/A — 按需求不创建 Linear issue。

## Summary

- 将 Main Chat、Session Thread、Agent Builder 和 Preview/Test Chat 统一为 Codex 风格的 `commentary → activity → final answer` 时间线，并复用 `zooclaw-design-system` 的 disclosure、item、spinner 和 alert 组件。
- 完成当前 v2 工具面与实际返回通道盘点；activity 只展示工具级正向 allowlist 中的调用意图，以及 command/patch/plan 的安全运行时投影，不再展示 Web、文件、MCP、Composio、内存等工具的 raw result preview。
- 保留运行、完成、失败、取消、真实耗时、长步骤折叠和 Agent 身份连续性，并在消息区出现可渲染事件后接管 composer activity 状态。
- 保持 Markdown、附件、Artifact、交互卡片、分享和 legacy Mattermost 历史兼容；设计与工具输出契约记录在本 PR 的 spec 中。

## Test plan

- [x] `bash scripts/verify-web.sh --no-clean <10 related unit specs>` — 10 files / 326 tests passed，包含 TypeScript、ESLint 与 governance guards。
- [x] `cd web/packages/chat-ui && pnpm test && pnpm tsc && pnpm lint` — 33 files / 431 tests passed。
- [x] `bash scripts/verify-changed.sh` — all changed surfaces passed after merging latest `origin/main`。
- [x] `git diff --check origin/main...HEAD`。



### files

- docs/superpowers/specs/2026-08-19-codex-style-agent-interaction-timeline.md
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/[workspaceId]/sessions/[sessionId]/SessionThreadClient.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/components/ChatBody.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/components/OpenClawAssistantMessage.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/hooks/useOpenClawRuntime.ts
- web/app/src/lib/chat/chat-activity.ts
- web/app/src/lib/chat/mm-display-messages.ts
- web/app/src/lib/chat/tool-status-display.ts
- web/app/src/lib/chat/tool-status-parser.ts
- web/app/src/lib/openclaw/types.ts
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts
- web/app/tests/unit/app/agent-builder-client.unit.spec.tsx
- web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx
- web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx
- web/app/tests/unit/app/chat/OpenClawAssistantMessage.unit.spec.tsx
- web/app/tests/unit/app/chat/ToolGroup.unit.spec.tsx
- web/app/tests/unit/app/chat/chatActivity.unit.spec.ts
- web/app/tests/unit/app/chat/toolStatusParser.unit.spec.ts
- web/app/tests/unit/app/chat/useOpenClawRuntime.unit.spec.ts
- web/app/tests/unit/chat/mmDisplayMessages.unit.spec.ts
- web/packages/chat-ui/src/__tests__/assistant-message.test.tsx
- web/packages/chat-ui/src/__tests__/tool-group.test.tsx
- web/packages/chat-ui/src/__tests__/tool-presentation.test.ts
- web/packages/chat-ui/src/index.ts
- web/packages/chat-ui/src/messages/AssistantMessage.tsx
- web/packages/chat-ui/src/tools/ToolGroup.tsx
- web/packages/chat-ui/src/tools/index.ts
- web/packages/chat-ui/src/tools/tool-presentation.ts
- web/packages/chat-ui/src/types.ts

---

## 7046e182

- author: tim-srp
- date: 2026-08-19T12:52:22Z
- pr: 3440


### commit message

```
fix(billing): accept sandbox Airwallex checkout URLs for vertical pack replay (#3440)

## Summary
- Accept Airwallex sandbox hosted checkout URLs
(`checkout.sandbox.airwallex.com`) in
`is_official_airwallex_checkout_url`, so a pending vertical pack
checkout whose provider URL was issued by the sandbox replays correctly
instead of raising `billing.enterprise_package.card.outcome_unresolved`.
- Add regression tests: URL validation covers the sandbox host (and a
lookalike-host rejection), and the enterprise reservation path replays a
sandbox-issued checkout URL.

## Root cause
The Airwallex sandbox returns hosted checkout URLs on the
`checkout.sandbox.airwallex.com` host, but `_CHECKOUT_HOSTS` only
allowed `checkout.airwallex.com`. Consequence observed live in staging:
the first purchase attempt created a valid pending order with a sandbox
checkout URL and session id, then every retry hit
`resolve_enterprise_checkout_reservation`:

- `is_official_airwallex_checkout_url(checkout_url)` → False (sandbox
host not in the allowlist)
- `provider_request_unclaimed` → False (the provider request had already
started)
- → `ConflictError: billing.enterprise_package.card.outcome_unresolved`,
permanently blocking the buyer's team from purchasing (the pending order
also blocks every new checkout for the same team).

## Test plan
- [x] `pytest tests/unit/test_airwallex_client.py
tests/unit/test_airwallex_enterprise_checkout.py` — 66 passed (2 new
RED→GREEN tests)
- [x] `ruff check` + `ruff format --check` clean on all changed files
- [x] pyright clean on changed files

Co-authored-by: Claude <noreply@anthropic.com>
```


### PR body

## Summary
- Accept Airwallex sandbox hosted checkout URLs (`checkout.sandbox.airwallex.com`) in `is_official_airwallex_checkout_url`, so a pending vertical pack checkout whose provider URL was issued by the sandbox replays correctly instead of raising `billing.enterprise_package.card.outcome_unresolved`.
- Add regression tests: URL validation covers the sandbox host (and a lookalike-host rejection), and the enterprise reservation path replays a sandbox-issued checkout URL.

## Root cause
The Airwallex sandbox returns hosted checkout URLs on the `checkout.sandbox.airwallex.com` host, but `_CHECKOUT_HOSTS` only allowed `checkout.airwallex.com`. Consequence observed live in staging: the first purchase attempt created a valid pending order with a sandbox checkout URL and session id, then every retry hit `resolve_enterprise_checkout_reservation`:

- `is_official_airwallex_checkout_url(checkout_url)` → False (sandbox host not in the allowlist)
- `provider_request_unclaimed` → False (the provider request had already started)
- → `ConflictError: billing.enterprise_package.card.outcome_unresolved`, permanently blocking the buyer's team from purchasing (the pending order also blocks every new checkout for the same team).

## Test plan
- [x] `pytest tests/unit/test_airwallex_client.py tests/unit/test_airwallex_enterprise_checkout.py` — 66 passed (2 new RED→GREEN tests)
- [x] `ruff check` + `ruff format --check` clean on all changed files
- [x] pyright clean on changed files



### files

- services/claw-interface/app/services/airwallex/client.py
- services/claw-interface/tests/unit/test_airwallex_client.py
- services/claw-interface/tests/unit/test_airwallex_enterprise_checkout.py

---

## 1272c49b

- author: tim-srp
- date: 2026-08-19T12:33:36Z
- pr: 3437


### commit message

```
fix(billing): include subscription_data in Airwallex vertical pack checkout (#3437)

## Summary
- Include `subscription_data` (duration `MONTH` / `period=1`) when
creating the Airwallex Billing Checkout for the Restaurant vertical
pack, mirroring the #3421 fix for the standard subscription and upgrade
flows.
- Add a unit test asserting the SUBSCRIPTION-mode checkout request
carries the monthly subscription duration.

## Root cause
The Airwallex Billing Checkout API requires `subscription_data` for
every `SUBSCRIPTION`-mode checkout creation. The vertical pack checkout
flow added in #3422 constructed `AirwallexCreateCheckoutRequest` without
it, so every Restaurant vertical pack Card purchase returned HTTP 400:

```json
{"code":"validation_error","message":"subscription_data must be provided for SUBSCRIPTION mode in checkout.","source":"subscription_data"}
```

The client masks the 400 as `billing.card_checkout.unavailable` ("Card
checkout is temporarily unavailable"), so the frontend only saw a
generic error. Reproduced live against the Airwallex sandbox with
staging credentials (create request returned 400; with
`subscription_data` the shape matches the sandbox-verified #3421
request).

## Test plan
- [x] `pytest tests/unit/test_airwallex_enterprise_checkout.py` — 31
passed (1 new RED→GREEN test)
- [x] `pytest tests/unit/test_airwallex_enterprise_subscription.py
tests/unit/test_enterprise_package_subscription.py
tests/unit/test_airwallex_lifecycle.py
tests/unit/test_airwallex_config.py` — 137 passed total
- [x] `ruff check` + `ruff format --check` clean on both changed files
- [x] pyright clean on both changed files (0 errors, 0 warnings)
- [x] `bash scripts/verify-py.sh` — all checks passed (ruff /
ruff-format / pyright / import-linter)

Co-authored-by: Claude <noreply@anthropic.com>
```


### PR body

## Summary
- Include `subscription_data` (duration `MONTH` / `period=1`) when creating the Airwallex Billing Checkout for the Restaurant vertical pack, mirroring the #3421 fix for the standard subscription and upgrade flows.
- Add a unit test asserting the SUBSCRIPTION-mode checkout request carries the monthly subscription duration.

## Root cause
The Airwallex Billing Checkout API requires `subscription_data` for every `SUBSCRIPTION`-mode checkout creation. The vertical pack checkout flow added in #3422 constructed `AirwallexCreateCheckoutRequest` without it, so every Restaurant vertical pack Card purchase returned HTTP 400:

```json
{"code":"validation_error","message":"subscription_data must be provided for SUBSCRIPTION mode in checkout.","source":"subscription_data"}
```

The client masks the 400 as `billing.card_checkout.unavailable` ("Card checkout is temporarily unavailable"), so the frontend only saw a generic error. Reproduced live against the Airwallex sandbox with staging credentials (create request returned 400; with `subscription_data` the shape matches the sandbox-verified #3421 request).

## Test plan
- [x] `pytest tests/unit/test_airwallex_enterprise_checkout.py` — 31 passed (1 new RED→GREEN test)
- [x] `pytest tests/unit/test_airwallex_enterprise_subscription.py tests/unit/test_enterprise_package_subscription.py tests/unit/test_airwallex_lifecycle.py tests/unit/test_airwallex_config.py` — 137 passed total
- [x] `ruff check` + `ruff format --check` clean on both changed files
- [x] pyright clean on both changed files (0 errors, 0 warnings)
- [x] `bash scripts/verify-py.sh` — all checks passed (ruff / ruff-format / pyright / import-linter)



### files

- services/claw-interface/app/services/airwallex/enterprise_checkout.py
- services/claw-interface/tests/unit/test_airwallex_enterprise_checkout.py

---

## 644316ad

- author: tim-srp
- date: 2026-08-19T12:29:10Z
- pr: 3435


### commit message

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


### PR body

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



### files

- services/claw-interface/app/services/airwallex/replacement.py
- services/claw-interface/tests/unit/test_airwallex_first_payment.py
- services/claw-interface/tests/unit/test_airwallex_replacement.py

---

## b75a4b3f

- author: tim-srp
- date: 2026-08-19T12:28:47Z
- pr: 3436


### commit message

```
docs: require a dedicated worktree for every new task or branch (#3436)

## Summary
- 在 AGENTS.md 的 Worktrees 章节新增规则：每个新任务/新分支必须用 `scripts/worktree.sh
<name>` 开独立 worktree。

## 背景
- 实际事故：PR #3432 合并后（远程分支被自动删除），其分支上的后续 cleanup 修复 commit push 时复活了陈旧
ref，且该 commit 不在 main 上，导致需要补开 PR #3435。
- 规则同时补充 worktree 缺 `.venv` 软链时的处理（pre-push verify-py 会失败，需软链到主 checkout
的 venv）。

## 验证
- [x] 仅文档改动，1 file changed

Co-authored-by: Claude <noreply@anthropic.com>
```


### PR body

## Summary
- 在 AGENTS.md 的 Worktrees 章节新增规则：每个新任务/新分支必须用 `scripts/worktree.sh <name>` 开独立 worktree。

## 背景
- 实际事故：PR #3432 合并后（远程分支被自动删除），其分支上的后续 cleanup 修复 commit push 时复活了陈旧 ref，且该 commit 不在 main 上，导致需要补开 PR #3435。
- 规则同时补充 worktree 缺 `.venv` 软链时的处理（pre-push verify-py 会失败，需软链到主 checkout 的 venv）。

## 验证
- [x] 仅文档改动，1 file changed



### files

- AGENTS.md

---

## efce5f48

- author: tim-srp
- date: 2026-08-19T11:51:39Z
- pr: 3434


### commit message

```
fix(claw-interface): pin pyright type resolution to project venv (#3434)

## Summary
- Pin pyright third-party import resolution to the project venv and ship
pyright in requirements-dev.txt.

## Root cause
Local `pyright` runs resolved third-party imports against the default
Python on PATH (miniconda base), whose site-packages carry
`botocore-stubs 1.38.46` — built for botocore 1.38, while the installed
botocore is 1.34.131. The mismatched stub makes the `boto3.client()`
overloads fall back to `BaseClient`, whose stub has no `__getattr__`, so
every S3 client method (`put_object`, `get_object`, `head_object`,
`delete_object`, `generate_presigned_url`) fails with "Cannot access
attribute ... for class BaseClient" — 7 errors in
`app/services/r2_storage.py`.

CI and a clean project venv were unaffected: without stubs, pyright
infers from botocore source, where `BaseClient.__getattr__` returns
`Any`.

Changes:
- `pyproject.toml` `[tool.pyright]`: add `venvPath = "."` / `venv =
".venv"` so imports resolve against the project venv. CI installs deps
with `uv pip install --system` (no `.venv`); pyright then falls back to
the default env exactly as before, so CI behavior is unchanged (verified
by simulating a no-venv run).
- `requirements-dev.txt`: add `pyright` so `scripts/verify-py.sh` and
the pre-commit Pyright hook actually find it in the venv — previously
the hook silently skipped ("pyright not found, skipping") because the
venv never had pyright.
- deptry DEP002 allowlist: add `pyright` (CLI-only tool, never
imported).

## Test plan
- [x] `bash scripts/verify-py.sh` — ruff check + ruff format + `pyright
app/ tests/` + lint-imports all pass
- [x] `.venv/bin/pyright app/ tests/` → 0 errors (previously 7)
- [x] Bare global `pyright app/ tests/` → 0 errors (venvPath config
takes effect)
- [x] deptry guard (`scripts/ci-lint/04-deptry.sh`) — "Success! No
dependency issues found"
- [x] `pytest tests/unit/test_r2_storage.py` — 29 passed
- [x] Simulated CI environment (no `.venv` present): pyright falls back
to the default env without erroring
```


### PR body

## Summary
- Pin pyright third-party import resolution to the project venv and ship pyright in requirements-dev.txt.

## Root cause
Local `pyright` runs resolved third-party imports against the default Python on PATH (miniconda base), whose site-packages carry `botocore-stubs 1.38.46` — built for botocore 1.38, while the installed botocore is 1.34.131. The mismatched stub makes the `boto3.client()` overloads fall back to `BaseClient`, whose stub has no `__getattr__`, so every S3 client method (`put_object`, `get_object`, `head_object`, `delete_object`, `generate_presigned_url`) fails with "Cannot access attribute ... for class BaseClient" — 7 errors in `app/services/r2_storage.py`.

CI and a clean project venv were unaffected: without stubs, pyright infers from botocore source, where `BaseClient.__getattr__` returns `Any`.

Changes:
- `pyproject.toml` `[tool.pyright]`: add `venvPath = "."` / `venv = ".venv"` so imports resolve against the project venv. CI installs deps with `uv pip install --system` (no `.venv`); pyright then falls back to the default env exactly as before, so CI behavior is unchanged (verified by simulating a no-venv run).
- `requirements-dev.txt`: add `pyright` so `scripts/verify-py.sh` and the pre-commit Pyright hook actually find it in the venv — previously the hook silently skipped ("pyright not found, skipping") because the venv never had pyright.
- deptry DEP002 allowlist: add `pyright` (CLI-only tool, never imported).

## Test plan
- [x] `bash scripts/verify-py.sh` — ruff check + ruff format + `pyright app/ tests/` + lint-imports all pass
- [x] `.venv/bin/pyright app/ tests/` → 0 errors (previously 7)
- [x] Bare global `pyright app/ tests/` → 0 errors (venvPath config takes effect)
- [x] deptry guard (`scripts/ci-lint/04-deptry.sh`) — "Success! No dependency issues found"
- [x] `pytest tests/unit/test_r2_storage.py` — 29 passed
- [x] Simulated CI environment (no `.venv` present): pyright falls back to the default env without erroring



### files

- services/claw-interface/pyproject.toml
- services/claw-interface/requirements-dev.txt

---

## 5f2787b9

- author: tim-srp
- date: 2026-08-19T11:36:45Z
- pr: 3432


### commit message

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


### PR body

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



### files

- services/claw-interface/app/schema/airwallex.py
- services/claw-interface/app/services/airwallex/enterprise_checkout.py
- services/claw-interface/app/services/airwallex/event_facts.py
- services/claw-interface/app/services/airwallex/lifecycle.py
- services/claw-interface/app/services/airwallex/payment_events.py
- services/claw-interface/app/services/billing_v2/airwallex_upgrade_checkout.py
- services/claw-interface/app/services/billing_v2/card_checkout.py
- services/claw-interface/tests/unit/test_airwallex_enterprise_checkout.py
- services/claw-interface/tests/unit/test_airwallex_payment_events.py
- services/claw-interface/tests/unit/test_airwallex_schema.py

---

## f63f7ba6

- author: sam-srp
- date: 2026-08-19T11:15:05Z
- pr: 3383


### commit message

```
feat: add personal MCP management UI (#3383)

## Summary
- add a Personal MCP tab to Plugins with one JSON configuration per
remote server
- support automatic tool discovery, connection enable/disable, refresh,
edit, delete, and per-tool enable/disable
- add Claw Interface proxy routes to the Engine MCP control plane and a
mock-backend implementation for local UI development
- keep V2 Agent settings hidden; personal MCP is user-global in phase 1
- show MCP when the V2 install capability and Main Agent both use the
Engine runtime; specialist Agents may remain on the v1 runtime during
migration
- keep a successful MCP availability decision stable for the current
browser page lifetime, re-evaluate after a full refresh, and retry
failed checks instead of caching them as unavailable

## UX details
- new connections start enabled and show a pulsing pending state until
discovery completes
- expanded rows expose refresh/edit/delete actions and the real
discovered tool list
- secrets are sent only on create/update and are never returned to the
browser
- direct `?tab=mcp` navigation falls back to Connectors when the install
capability or Main Agent is not on Engine

## Validation
- Web lint and TypeScript checks passed
- targeted MCP and Plugins Web unit tests passed, including
mixed-runtime, Main-Agent eligibility, page-lifetime stability, and
failed-check retry coverage
- Claw Interface unit tests and Ruff checks passed
- local cross-service CloudBase MCP flow verified end to end

## Design
- repository phase 1 design spec updated with the Main-Agent eligibility
and mixed-runtime rollout contract
- [Feishu design
document](https://starquest.feishu.cn/docx/Ql4Qd1lc4oSMRExvzGgcPtWDntc)

## Dependency
- requires SerendipityOneInc/zooclaw-engine#748

## Deployment
- no new environment variables
- Claw Interface reuses `ZOOCLAW_ENGINE_URL`,
`ZOOCLAW_ENGINE_SERVICE_TOKEN`, and the existing V2
`ZOOCLAW_ENGINE_ADMIN_TOKEN`
```


### PR body

## Summary
- add a Personal MCP tab to Plugins with one JSON configuration per remote server
- support automatic tool discovery, connection enable/disable, refresh, edit, delete, and per-tool enable/disable
- add Claw Interface proxy routes to the Engine MCP control plane and a mock-backend implementation for local UI development
- keep V2 Agent settings hidden; personal MCP is user-global in phase 1
- show MCP when the V2 install capability and Main Agent both use the Engine runtime; specialist Agents may remain on the v1 runtime during migration
- keep a successful MCP availability decision stable for the current browser page lifetime, re-evaluate after a full refresh, and retry failed checks instead of caching them as unavailable

## UX details
- new connections start enabled and show a pulsing pending state until discovery completes
- expanded rows expose refresh/edit/delete actions and the real discovered tool list
- secrets are sent only on create/update and are never returned to the browser
- direct `?tab=mcp` navigation falls back to Connectors when the install capability or Main Agent is not on Engine

## Validation
- Web lint and TypeScript checks passed
- targeted MCP and Plugins Web unit tests passed, including mixed-runtime, Main-Agent eligibility, page-lifetime stability, and failed-check retry coverage
- Claw Interface unit tests and Ruff checks passed
- local cross-service CloudBase MCP flow verified end to end

## Design
- repository phase 1 design spec updated with the Main-Agent eligibility and mixed-runtime rollout contract
- [Feishu design document](https://starquest.feishu.cn/docx/Ql4Qd1lc4oSMRExvzGgcPtWDntc)

## Dependency
- requires SerendipityOneInc/zooclaw-engine#748

## Deployment
- no new environment variables
- Claw Interface reuses `ZOOCLAW_ENGINE_URL`, `ZOOCLAW_ENGINE_SERVICE_TOKEN`, and the existing V2 `ZOOCLAW_ENGINE_ADMIN_TOKEN`



### files

- docs/superpowers/specs/2026-08-12-personal-mcp-phase1.md
- services/claw-interface/app/create_app.py
- services/claw-interface/app/database/collections.py
- services/claw-interface/app/database/personal_mcp_connection_repo.py
- services/claw-interface/app/lifetime.py
- services/claw-interface/app/routes/mcp.py
- services/claw-interface/app/scheduler.py
- services/claw-interface/app/schema/engine.py
- services/claw-interface/app/schema/mcp.py
- services/claw-interface/app/services/agents/engine_agent_install_service.py
- services/claw-interface/app/services/engine_client/__init__.py
- services/claw-interface/app/services/engine_client/_agents.py
- services/claw-interface/app/services/engine_client/_credentials.py
- services/claw-interface/app/services/engine_client/_mcp.py
- services/claw-interface/app/services/mcp_secret_store.py
- services/claw-interface/app/services/mcp_service.py
- services/claw-interface/app/services/mcp_sync_service.py
- services/claw-interface/pyproject.toml
- services/claw-interface/tests/unit/test_engine_agent_install_service.py
- services/claw-interface/tests/unit/test_engine_client.py
- services/claw-interface/tests/unit/test_engine_client_mcp.py
- services/claw-interface/tests/unit/test_mcp_schema.py
- services/claw-interface/tests/unit/test_mcp_service.py
- services/claw-interface/tests/unit/test_mcp_sync_service.py
- services/claw-interface/tests/unit/test_personal_mcp_connection_repo.py
- services/claw-interface/tests/unit/test_scheduler.py
- web/app/package.json
- web/app/scripts/mock-backend.mjs
- web/app/scripts/mock-backend/mcp.mjs
- web/app/scripts/mock-backend/scenarios.mjs
- web/app/src/app/[locale]/(app)/plugins/PluginsClient.tsx
- web/app/src/app/[locale]/(app)/plugins/mcp/McpConnectionDialog.tsx
- web/app/src/app/[locale]/(app)/plugins/mcp/McpConnectionRow.tsx
- web/app/src/app/[locale]/(app)/plugins/mcp/McpConnectionsClient.tsx
- web/app/src/app/[locale]/(app)/plugins/mcp/McpDeleteDialog.tsx
- web/app/src/app/[locale]/(app)/plugins/mcp/McpJsonEditor.tsx
- web/app/src/app/[locale]/(app)/plugins/mcp/mcp-server-config.ts
- web/app/src/app/[locale]/(app)/plugins/plugin-tabs.ts
- web/app/src/app/[locale]/(app)/plugins/useViewModel.ts
- web/app/src/hooks/queries/mcp/useMcpConnections.ts
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts
- web/app/src/models/mcp.ts
- web/app/src/services/mcp.ts
- web/app/tests/unit/app/mcp-connection-row.unit.spec.tsx
- web/app/tests/unit/app/plugins/McpConnectionsClient.unit.spec.tsx
- web/app/tests/unit/app/plugins/PluginsClient.unit.spec.tsx
- web/app/tests/unit/app/plugins/mcp-server-config.unit.spec.ts
- web/app/tests/unit/app/plugins/plugin-tabs.unit.spec.ts
- web/app/tests/unit/hooks/useMcpConnections.unit.spec.tsx

---

## 8fa934cc

- author: shana-srp
- date: 2026-08-19T11:12:06Z
- pr: 3431


### commit message

```
feat(marketing): localize and refine pricing page (#3431)

## Linear

No linked issue.

## Summary

- align the public Pricing page typography with Figtree and the
refreshed marketing visual system
- remove the Pricing section kicker labels and tune responsive type
sizing
- complete the public Pricing dictionary for all supported non-English
locales
- add typography and translation-contract coverage

## Test plan

- [x] `bash scripts/verify-web.sh --no-test`
- [x] Pricing unit tests: 2 files / 23 tests passed
- [x] TypeScript passed
- [x] ESLint passed

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```


### PR body

## Linear

No linked issue.

## Summary

- align the public Pricing page typography with Figtree and the refreshed marketing visual system
- remove the Pricing section kicker labels and tune responsive type sizing
- complete the public Pricing dictionary for all supported non-English locales
- add typography and translation-contract coverage

## Test plan

- [x] `bash scripts/verify-web.sh --no-test`
- [x] Pricing unit tests: 2 files / 23 tests passed
- [x] TypeScript passed
- [x] ESLint passed



### files

- web/app/src/app/[locale]/(marketing)/MarketingChrome.tsx
- web/app/src/app/[locale]/(marketing)/pricing/PublicPricingClient.tsx
- web/app/src/app/[locale]/(marketing)/pricing/pricing.css
- web/app/src/locales/ar.ts
- web/app/src/locales/de.ts
- web/app/src/locales/es.ts
- web/app/src/locales/fr.ts
- web/app/src/locales/it.ts
- web/app/src/locales/ja.ts
- web/app/src/locales/ko.ts
- web/app/src/locales/pt.ts
- web/app/tests/unit/css/pricing-typography.unit.spec.ts
- web/app/tests/unit/locales/public-pricing-completeness.unit.spec.ts

---

## c40fccee

- author: shana-srp
- date: 2026-08-19T11:12:02Z
- pr: 3429


### commit message

```
feat(marketing): preserve legacy experience on features page (#3429)

## Linear

No linked issue.

## Summary

- preserve the previous landing hero experience at `/features`
- remove the retired standalone Features component tree and hooks
- update the homepage footer link to target the Features route directly

## Test plan

- [x] `bash scripts/verify-web.sh`
- [x] TypeScript passed
- [x] 651 test files passed (8,821 tests passed; 70 skipped; 1 todo)
- [x] ESLint passed

## Notes

- Contact is isolated in a separate PR.
- Pricing is isolated in a separate PR.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```


### PR body

## Linear

No linked issue.

## Summary

- preserve the previous landing hero experience at `/features`
- remove the retired standalone Features component tree and hooks
- update the homepage footer link to target the Features route directly

## Test plan

- [x] `bash scripts/verify-web.sh`
- [x] TypeScript passed
- [x] 651 test files passed (8,821 tests passed; 70 skipped; 1 todo)
- [x] ESLint passed

## Notes

- Contact is isolated in a separate PR.
- Pricing is isolated in a separate PR.



### files

- web/app/AGENTS.md
- web/app/src/app/[locale]/(marketing)/features/FeaturesClient.tsx
- web/app/src/app/[locale]/(marketing)/features/featuresContent.ts
- web/app/src/components/features/FeaturesCTA.tsx
- web/app/src/components/features/FeaturesComparison.tsx
- web/app/src/components/features/FeaturesDeepDive.tsx
- web/app/src/components/features/FeaturesFAQ.tsx
- web/app/src/components/features/FeaturesForExperts.tsx
- web/app/src/components/features/FeaturesHero.tsx
- web/app/src/components/features/FeaturesIntegrations.tsx
- web/app/src/components/features/FeaturesSection.tsx
- web/app/src/components/features/FeaturesSecurity.tsx
- web/app/src/components/features/FeaturesShowcase.tsx
- web/app/src/components/features/FeaturesSpecialists.tsx
- web/app/src/components/features/FeaturesSteps.tsx
- web/app/src/components/public/public-nav-data.ts
- web/app/src/hooks/features/useFeaturesParallax.ts
- web/app/src/hooks/features/useFeaturesScrollState.ts
- web/app/src/lib/landing-content.ts
- web/app/tests/unit/app/landing-client.unit.spec.tsx
- web/app/tests/unit/app/landing-content.unit.spec.ts

---

## ac5f6529

- author: lynn Zhuang
- date: 2026-08-19T10:09:16Z
- pr: 3392


### commit message

```
feat(chat): show v2 activity across interactive surfaces (#3392)

## Summary

- Add one shared V2 Chat activity model (`thinking | tool | responding |
null`) and neutral presentation for Main Chat, Session Thread, Agent
Builder, Agent Preview, and interactive Subagent Chat.
- Derive Mattermost/ACS activity from real `tool_status` and
`assistant_segment` events, and derive Gateway activity from
`chat.send`, scoped agent/tool/delta events, and terminal lifecycle
events.
- Preserve run/session isolation, ignore V1 `custom_turn_status`, and
keep replacement-run state safe from late abort confirmations and
retired-run events.
- Use exactly three localized global labels, with English fallback:
- English: `Thinking…`, `Working on the task…`, `Preparing the
response…`
  - Chinese: `正在思考…`, `正在执行任务…`, `正在组织回复…`
- Preserve connection-warning priority, read-only/replay suppression,
polite live-region semantics, and reduced-motion behavior in both main
and compact composers.

## Signal contracts

- Mattermost/ACS: pending, queued, or running `tool_status` events map
to working; nonterminal streaming/assistant segments map to preparing;
waiting maps to thinking. Final streams, terminal segments/status, and
ordinary visible replies are terminal boundaries. Pending ownership is
isolated by channel + root/session, including typing events, so one
thread cannot show or clear another thread or Main. Tool names and
arguments are never shown.
- Gateway: `chat.send` establishes the active run; scoped tool events
map to working; assistant deltas map to preparing. A transport-ambiguous
send replays on stable reconnect with the same idempotency key before
abort/reconciliation. Definitive not-sent/rejected failures remove only
their optimistic row and preserve the draft; ambiguous failures remain
visibly fenced. Terminal lifecycle, error, confirmed abort, and
disconnect paths clear per the implementation. Events from other
sessions or runs are ignored.
- Late abort confirmations are attempt- and run-scoped: they cannot
clear or otherwise mutate a replacement run.

## Visual treatment

- Neutral `#a1a1aa` text, regular weight, and a white shimmer are shared
by all five V2 surfaces.
- The fixed neutral color is an accepted product tradeoff against strict
contrast guidance for this transient status text.

## Verification

The branch previously merged `origin/main` at `5b15d93ad`. For fix round
1, `origin/main` was fetched at `ac6581ec`; GitHub CI validates the
current merge ref. These local commands passed at the final review-round
head:

```bash
cd web/app
pnpm exec vitest run \
  tests/unit/app/chat/chatActivity.unit.spec.ts \
  tests/unit/app/chat/ChatBody.unit.spec.tsx \
  tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx \
  tests/unit/app/agent-builder-client.unit.spec.tsx \
  tests/unit/app/agent-builder-test-chat.unit.spec.tsx \
  tests/unit/app/chat/GenClawInput.unit.spec.tsx \
  tests/unit/app/chat/OpenClawChatSurface.unit.spec.tsx \
  tests/unit/app/chat/useSubagentChat.unit.spec.ts \
  tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx
```

Result: 9 files and 394 tests passed. The complete directly impacted
suite passed 13 files and 492 tests.

```bash
cd web/packages/chat-ui
pnpm exec tsc --noEmit
pnpm exec vitest run src/__tests__/chat-composer.test.tsx
pnpm exec eslint src
```

Result: typecheck and lint passed; 1 file and 48 tests passed.

```bash
bash scripts/verify-web.sh \
  web/app/src/lib/chat/chat-activity.ts \
  web/app/src/app/[locale]/\(app\)/\(chat\)/chat \
  web/app/src/app/[locale]/\(app\)/\(chat\)/agent-builder \
  web/packages/chat-ui/src/composer/parts/ComposerNotices.tsx
bash scripts/verify-changed.sh
git diff --check
git diff --check origin/main...HEAD
```

Result: repository guards, TypeScript, 129 files / 1840 tests, ESLint,
changed-surface verification, and diff checks passed. ESLint retains one
unrelated existing `LandingStartupOverlay.tsx` accessibility warning;
the focused Vite runs retain the existing `vite-tsconfig-paths`
migration advisory.

## Review follow-up

- The earlier confirmed-abort defect is fixed: exact authoritative abort
confirmation releases only the matching direct or deferred attempt,
while false, malformed, or rejected responses remain fenced.
- Fix round 1 adds two deferred race regressions for confirmations that
arrive after old-run lifecycle end and a replacement send. Temporarily
removing the corresponding attempt-identity or run guard made each new
test fail; restoring the guards returned the suite to green. The current
production implementation was already correct, so this round required
test and evidence changes only.
- The final review fix wave addresses all six confirmed Important
findings test-first: nonfinal posted stream previews; root/session
pending isolation (including `parent_id` typing); stable reconnect
replay/reconciliation; successful hidden-Stop activity suppression;
visible terminal backfill boundaries (including attachment-only
`file_ids`); and definitive optimistic-row rollback with single-turn
retry. Main null-root behavior, acknowledged in-flight dedupe, and
ambiguous-send retention remain covered.
- Final automated feedback was checked against the supported OpenClaw
v2026.5.7 protocol: `agent` payloads require `runId`, `seq`, `stream`,
`ts`, and nested `data`, so accepting the older identity-free flat
lifecycle shape would break the run fence. Likewise, a non-throwing
`chat.send` result without `runId` is intentionally ambiguous rather
than definitive; it keeps the row/fence and is reconciled by the
same-key stable-reconnect replay. No further code change was warranted.

## Genuine local evidence

Validated with `bash scripts/dev-mock.sh --scenario ready-user` at the
actual printed URL and production routes; the standalone timer demo was
not used. Local ignored captures:

- `.screenshots/v2-chat-activity-main.png` — genuine Main Chat waiting
state after a real send.
- `.screenshots/v2-chat-activity-session.png` — genuine settled Session
Thread route/reply.
- `.screenshots/v2-chat-activity-builder.png` — genuine Agent Builder
waiting state.
- `.screenshots/v2-chat-activity-preview.png` — genuine Agent Preview
waiting state.
- `.screenshots/v2-chat-activity-subagent.png` — genuine interactive
Subagent Chat available state.

The deterministic `ready-user` fixture does not emit Mattermost
`tool_status` or nonterminal assistant segments, so working/preparing
could not be captured visually. Its Subagent Chat send returns no run id
or agent events, so an active subagent state is likewise unavailable.
The focused signal/state tests cover those paths; unavailable
screenshots were not fabricated.

## Scope notes

- Repository size-gate result against current `origin/main`: 4,415
filtered lines (`+4025 / -390`) across 49 files. The full text diff is
6,395 lines (`+6005 / -390`) across 56 files. The final six-finding fix
wave itself is 1,445 lines (`+1179 / -266`) across 32 files from its
fixed base.
- The `size-override` label remains justified because the shared state
adapter, five production surfaces, and focused regression coverage form
one atomic V2 contract.
- No backend API or persisted-data migration.
- No screenshots are tracked.
- `.impeccable.md` predates this V2 implementation on the existing
feature branch and is retained unchanged.
```


### PR body

## Summary

- Add one shared V2 Chat activity model (`thinking | tool | responding | null`) and neutral presentation for Main Chat, Session Thread, Agent Builder, Agent Preview, and interactive Subagent Chat.
- Derive Mattermost/ACS activity from real `tool_status` and `assistant_segment` events, and derive Gateway activity from `chat.send`, scoped agent/tool/delta events, and terminal lifecycle events.
- Preserve run/session isolation, ignore V1 `custom_turn_status`, and keep replacement-run state safe from late abort confirmations and retired-run events.
- Use exactly three localized global labels, with English fallback:
  - English: `Thinking…`, `Working on the task…`, `Preparing the response…`
  - Chinese: `正在思考…`, `正在执行任务…`, `正在组织回复…`
- Preserve connection-warning priority, read-only/replay suppression, polite live-region semantics, and reduced-motion behavior in both main and compact composers.

## Signal contracts

- Mattermost/ACS: pending, queued, or running `tool_status` events map to working; nonterminal streaming/assistant segments map to preparing; waiting maps to thinking. Final streams, terminal segments/status, and ordinary visible replies are terminal boundaries. Pending ownership is isolated by channel + root/session, including typing events, so one thread cannot show or clear another thread or Main. Tool names and arguments are never shown.
- Gateway: `chat.send` establishes the active run; scoped tool events map to working; assistant deltas map to preparing. A transport-ambiguous send replays on stable reconnect with the same idempotency key before abort/reconciliation. Definitive not-sent/rejected failures remove only their optimistic row and preserve the draft; ambiguous failures remain visibly fenced. Terminal lifecycle, error, confirmed abort, and disconnect paths clear per the implementation. Events from other sessions or runs are ignored.
- Late abort confirmations are attempt- and run-scoped: they cannot clear or otherwise mutate a replacement run.

## Visual treatment

- Neutral `#a1a1aa` text, regular weight, and a white shimmer are shared by all five V2 surfaces.
- The fixed neutral color is an accepted product tradeoff against strict contrast guidance for this transient status text.

## Verification

The branch previously merged `origin/main` at `5b15d93ad`. For fix round 1, `origin/main` was fetched at `ac6581ec`; GitHub CI validates the current merge ref. These local commands passed at the final review-round head:

```bash
cd web/app
pnpm exec vitest run \
  tests/unit/app/chat/chatActivity.unit.spec.ts \
  tests/unit/app/chat/ChatBody.unit.spec.tsx \
  tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx \
  tests/unit/app/agent-builder-client.unit.spec.tsx \
  tests/unit/app/agent-builder-test-chat.unit.spec.tsx \
  tests/unit/app/chat/GenClawInput.unit.spec.tsx \
  tests/unit/app/chat/OpenClawChatSurface.unit.spec.tsx \
  tests/unit/app/chat/useSubagentChat.unit.spec.ts \
  tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx
```

Result: 9 files and 394 tests passed. The complete directly impacted suite passed 13 files and 492 tests.

```bash
cd web/packages/chat-ui
pnpm exec tsc --noEmit
pnpm exec vitest run src/__tests__/chat-composer.test.tsx
pnpm exec eslint src
```

Result: typecheck and lint passed; 1 file and 48 tests passed.

```bash
bash scripts/verify-web.sh \
  web/app/src/lib/chat/chat-activity.ts \
  web/app/src/app/[locale]/\(app\)/\(chat\)/chat \
  web/app/src/app/[locale]/\(app\)/\(chat\)/agent-builder \
  web/packages/chat-ui/src/composer/parts/ComposerNotices.tsx
bash scripts/verify-changed.sh
git diff --check
git diff --check origin/main...HEAD
```

Result: repository guards, TypeScript, 129 files / 1840 tests, ESLint, changed-surface verification, and diff checks passed. ESLint retains one unrelated existing `LandingStartupOverlay.tsx` accessibility warning; the focused Vite runs retain the existing `vite-tsconfig-paths` migration advisory.

## Review follow-up

- The earlier confirmed-abort defect is fixed: exact authoritative abort confirmation releases only the matching direct or deferred attempt, while false, malformed, or rejected responses remain fenced.
- Fix round 1 adds two deferred race regressions for confirmations that arrive after old-run lifecycle end and a replacement send. Temporarily removing the corresponding attempt-identity or run guard made each new test fail; restoring the guards returned the suite to green. The current production implementation was already correct, so this round required test and evidence changes only.
- The final review fix wave addresses all six confirmed Important findings test-first: nonfinal posted stream previews; root/session pending isolation (including `parent_id` typing); stable reconnect replay/reconciliation; successful hidden-Stop activity suppression; visible terminal backfill boundaries (including attachment-only `file_ids`); and definitive optimistic-row rollback with single-turn retry. Main null-root behavior, acknowledged in-flight dedupe, and ambiguous-send retention remain covered.
- Final automated feedback was checked against the supported OpenClaw v2026.5.7 protocol: `agent` payloads require `runId`, `seq`, `stream`, `ts`, and nested `data`, so accepting the older identity-free flat lifecycle shape would break the run fence. Likewise, a non-throwing `chat.send` result without `runId` is intentionally ambiguous rather than definitive; it keeps the row/fence and is reconciled by the same-key stable-reconnect replay. No further code change was warranted.

## Genuine local evidence

Validated with `bash scripts/dev-mock.sh --scenario ready-user` at the actual printed URL and production routes; the standalone timer demo was not used. Local ignored captures:

- `.screenshots/v2-chat-activity-main.png` — genuine Main Chat waiting state after a real send.
- `.screenshots/v2-chat-activity-session.png` — genuine settled Session Thread route/reply.
- `.screenshots/v2-chat-activity-builder.png` — genuine Agent Builder waiting state.
- `.screenshots/v2-chat-activity-preview.png` — genuine Agent Preview waiting state.
- `.screenshots/v2-chat-activity-subagent.png` — genuine interactive Subagent Chat available state.

The deterministic `ready-user` fixture does not emit Mattermost `tool_status` or nonterminal assistant segments, so working/preparing could not be captured visually. Its Subagent Chat send returns no run id or agent events, so an active subagent state is likewise unavailable. The focused signal/state tests cover those paths; unavailable screenshots were not fabricated.

## Scope notes

- Repository size-gate result against current `origin/main`: 4,415 filtered lines (`+4025 / -390`) across 49 files. The full text diff is 6,395 lines (`+6005 / -390`) across 56 files. The final six-finding fix wave itself is 1,445 lines (`+1179 / -266`) across 32 files from its fixed base.
- The `size-override` label remains justified because the shared state adapter, five production surfaces, and focused regression coverage form one atomic V2 contract.
- No backend API or persisted-data migration.
- No screenshots are tracked.
- `.impeccable.md` predates this V2 implementation on the existing feature branch and is retained unchanged.



### files

- .impeccable.md
- docs/superpowers/plans/2026-08-14-agent-builder-activity-status.md
- docs/superpowers/plans/2026-08-18-v2-chat-activity-status.md
- docs/superpowers/specs/2026-08-14-agent-builder-activity-status-design.md
- docs/superpowers/specs/2026-08-18-v2-chat-activity-status-design.md
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/useSendBuilderMessage.ts
- web/app/src/app/[locale]/(app)/(chat)/chat/[workspaceId]/sessions/[sessionId]/SessionThreadClient.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/[workspaceId]/sessions/[sessionId]/hooks/useSendThreadReply.ts
- web/app/src/app/[locale]/(app)/(chat)/chat/[workspaceId]/sessions/[sessionId]/hooks/useSessionThreadStop.ts
- web/app/src/app/[locale]/(app)/(chat)/chat/components/ChatBody.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/components/GenClawInput.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/components/NeutralChatActivityIcon.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/components/OpenClawChatSurface.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/components/SubagentChatPanel.tsx
- web/app/src/app/[locale]/(app)/(chat)/chat/hooks/useChatMessaging.ts
- web/app/src/app/[locale]/(app)/(chat)/chat/hooks/useSubagentChat.ts
- web/app/src/app/globals.css
- web/app/src/components/providers/MattermostProvider.tsx
- web/app/src/hooks/chat/useSessionThreadWaitingReconciliation.ts
- web/app/src/hooks/mattermost/useMattermostTyping.ts
- web/app/src/hooks/useMattermost.ts
- web/app/src/hooks/useOpenClawWebSocket.ts
- web/app/src/lib/chat/chat-activity.ts
- web/app/src/lib/chat/turn-status-parser.ts
- web/app/src/lib/mattermost/post-status.ts
- web/app/src/lib/mattermost/thread-waiting.ts
- web/app/src/lib/mattermost/types.ts
- web/app/src/lib/openclaw/request-error.ts
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts
- web/app/src/services/conversation-threads.ts
- web/app/tests/unit/app/agent-builder-client.unit.spec.tsx
- web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx
- web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx
- web/app/tests/unit/app/chat-thread/thread-post-utils.unit.spec.ts
- web/app/tests/unit/app/chat-thread/useSendThreadReply.unit.spec.tsx
- web/app/tests/unit/app/chat/ChatBody.unit.spec.tsx
- web/app/tests/unit/app/chat/GenClawInput.unit.spec.tsx
- web/app/tests/unit/app/chat/OpenClawChatSurface.unit.spec.tsx
- web/app/tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx
- web/app/tests/unit/app/chat/chatActivity.unit.spec.ts
- web/app/tests/unit/app/chat/turnStatusParser.unit.spec.ts
- web/app/tests/unit/app/chat/useChatMessaging.unit.spec.ts
- web/app/tests/unit/app/chat/useSubagentChat.unit.spec.ts
- web/app/tests/unit/helpers/chatUiMocks.tsx
- web/app/tests/unit/hooks/mattermost/useMattermostTyping.unit.spec.ts
- web/app/tests/unit/hooks/useMattermost.unit.spec.ts
- web/app/tests/unit/hooks/useMattermost.unit.spec.tsx

---

## 9b79cc0b

- author: tim-srp
- date: 2026-08-19T09:31:09Z
- pr: 3428


### commit message

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


### PR body

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



### files

- services/claw-interface/app/routes/billing.py
- services/claw-interface/app/schema/airwallex.py
- services/claw-interface/app/services/airwallex/event_facts.py
- services/claw-interface/app/services/airwallex/webhook.py
- services/claw-interface/tests/unit/test_airwallex_event_facts.py
- services/claw-interface/tests/unit/test_airwallex_webhook.py
- services/claw-interface/tests/unit/test_airwallex_webhook_routes.py

---

## b3dec319

- author: tim-srp
- date: 2026-08-19T08:53:49Z
- pr: 3422


### commit message

```
feat(billing): add Airwallex vertical pack enterprise settlement flow (#3422)

## Summary
- Add the Airwallex vertical pack (Restaurant AI Team) enterprise
settlement flow: initial payment (`enterprise_payment.py`), active
confirmation/repair (`enterprise_active.py`), and renewal settlement
(`enterprise_renewal.py`), sharing common helpers in
`enterprise_payment_common.py` and the enterprise catalog lookup in
`enterprise_catalog.py`.
- Dispatch enterprise settlement from the Airwallex lifecycle webhook
handler: `_settle_enterprise_period_if_applicable` +
`_project_enterprise_active_if_applicable` inside `_settle_paid_period`,
gated by `is_enterprise_package_agreement` /
`is_enterprise_package_order`.
- Provider-parameterize the card checkout order repo with a `creem`
default (`find_unresolved_enterprise_checkout`, `claim_renewal_phase`,
`get_manual_review_subscription`) so enterprise settlement can claim
Airwallex orders.
- Add the `airwallex_vertical_pack_checkout_enabled` config gate (price
id + enterprise admin URL + environment prerequisites, with
price-collision and mismatched-environment guards) and the
`AIRWALLEX_PRICE_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY` setting.
- Surface `vertical_pack_package.py` checkout through the Airwallex
enterprise checkout path (price_id-based), rename the creem-only cleanup
helper to `_delete_unreferenced_vertical_pack_package`, and allow
Airwallex as an enterprise package provider.
- Cover the suite with 16 unit tests
(`test_airwallex_enterprise_subscription.py`) plus config gate tests,
all passing locally with ruff + pyright clean on every changed file.

## Test plan
- [x] `pytest tests/unit/test_airwallex_enterprise_subscription.py` — 16
passed
- [x] `pytest tests/unit/test_airwallex_config.py` — 39 passed
- [x] `pytest tests/unit/test_airwallex_lifecycle.py` — lifecycle
dispatch covered
- [x] `ruff check` + `ruff format --check` clean on all changed files
- [x] pyright clean on all changed files (pre-existing `r2_storage.py`
env errors untouched by this PR)
- [x] import-linter: 8/8 contracts kept

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude <noreply@anthropic.com>
```


### PR body

## Summary
- Add the Airwallex vertical pack (Restaurant AI Team) enterprise settlement flow: initial payment (`enterprise_payment.py`), active confirmation/repair (`enterprise_active.py`), and renewal settlement (`enterprise_renewal.py`), sharing common helpers in `enterprise_payment_common.py` and the enterprise catalog lookup in `enterprise_catalog.py`.
- Dispatch enterprise settlement from the Airwallex lifecycle webhook handler: `_settle_enterprise_period_if_applicable` + `_project_enterprise_active_if_applicable` inside `_settle_paid_period`, gated by `is_enterprise_package_agreement` / `is_enterprise_package_order`.
- Provider-parameterize the card checkout order repo with a `creem` default (`find_unresolved_enterprise_checkout`, `claim_renewal_phase`, `get_manual_review_subscription`) so enterprise settlement can claim Airwallex orders.
- Add the `airwallex_vertical_pack_checkout_enabled` config gate (price id + enterprise admin URL + environment prerequisites, with price-collision and mismatched-environment guards) and the `AIRWALLEX_PRICE_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY` setting.
- Surface `vertical_pack_package.py` checkout through the Airwallex enterprise checkout path (price_id-based), rename the creem-only cleanup helper to `_delete_unreferenced_vertical_pack_package`, and allow Airwallex as an enterprise package provider.
- Cover the suite with 16 unit tests (`test_airwallex_enterprise_subscription.py`) plus config gate tests, all passing locally with ruff + pyright clean on every changed file.

## Test plan
- [x] `pytest tests/unit/test_airwallex_enterprise_subscription.py` — 16 passed
- [x] `pytest tests/unit/test_airwallex_config.py` — 39 passed
- [x] `pytest tests/unit/test_airwallex_lifecycle.py` — lifecycle dispatch covered
- [x] `ruff check` + `ruff format --check` clean on all changed files
- [x] pyright clean on all changed files (pre-existing `r2_storage.py` env errors untouched by this PR)
- [x] import-linter: 8/8 contracts kept

🤖 Generated with [Claude Code](https://claude.com/claude-code)



### files

- .env.example
- docs/superpowers/specs/2026-08-18-airwallex-vertical-pack-payment-design.md
- services/claw-interface/.jscpd.src.json
- services/claw-interface/app/database/airwallex_checkout_repo.py
- services/claw-interface/app/database/card_checkout_order_repo.py
- services/claw-interface/app/schema/airwallex_settings.py
- services/claw-interface/app/services/airwallex/config.py
- services/claw-interface/app/services/airwallex/enterprise_active.py
- services/claw-interface/app/services/airwallex/enterprise_catalog.py
- services/claw-interface/app/services/airwallex/enterprise_checkout.py
- services/claw-interface/app/services/airwallex/enterprise_package_checkout.py
- services/claw-interface/app/services/airwallex/enterprise_payment.py
- services/claw-interface/app/services/airwallex/enterprise_payment_common.py
- services/claw-interface/app/services/airwallex/enterprise_renewal.py
- services/claw-interface/app/services/airwallex/first_payment.py
- services/claw-interface/app/services/airwallex/lifecycle.py
- services/claw-interface/app/services/airwallex/reconciliation.py
- services/claw-interface/app/services/enterprise_package_provider.py
- services/claw-interface/app/services/enterprise_package_subscription.py
- services/claw-interface/app/services/vertical_pack_package.py
- services/claw-interface/pyproject.toml
- services/claw-interface/tests/unit/test_airwallex_config.py
- services/claw-interface/tests/unit/test_airwallex_enterprise_checkout.py
- services/claw-interface/tests/unit/test_airwallex_enterprise_subscription.py
- services/claw-interface/tests/unit/test_airwallex_first_payment.py
- services/claw-interface/tests/unit/test_airwallex_lifecycle.py
- services/claw-interface/tests/unit/test_airwallex_reconciliation.py
- services/claw-interface/tests/unit/test_creem_enterprise_checkout.py
- services/claw-interface/tests/unit/test_enterprise_package_subscription.py
- services/claw-interface/tests/unit/test_vertical_pack_package_service.py

---

## bbd20fe2

- author: rayrain-srp
- date: 2026-08-19T08:09:48Z
- pr: 3416


### commit message

```
fix(billing): align credit balance displays (#3416)

## Summary

- correct every frontend billing mock so subscription and top-up fields
represent initial wallet capacity instead of remaining balance
- make the collapsed desktop sidebar use canonical `availableCredits`
instead of aliasing total wallet capacity
- preserve exhausted-trial warnings by checking canonical remaining
credits instead of subscription capacity
- add regression coverage for the mock credit invariants, the reported
`active-pro` display, and the sidebar prop mapping
- Linear:
https://linear.app/srpone/issue/ECA-1384/staging-billing-mock-shows-inconsistent-credit-balances-across-account

## Root cause

The staging `active-pro` mock mixed two different meanings for its
credit fields: `totalCredits` was 20,000, while `subscriptionCredits`
incorrectly contained the remaining 11,500. The account menu rendered
`availableCredits` directly, but Settings → Usage treated
`subscriptionCredits + topupCredits` as initial capacity and subtracted
the 8,500 usage again, producing 3,000 / 11,500.

Separately, the collapsed desktop sidebar renamed `walletTotal` to
`availableCredits`, so real accounts with consumed credits could see
total capacity in the tooltip.

The corrected mock semantics also exposed an existing consumer bug:
`SubscriptionPanel` used subscription capacity for its low-credit
warning. It now checks `availableCredits`, so an exhausted trial still
warns even when its initial capacity is non-zero.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to all six changed source and
test files (130 related tests)
- [x] pre-commit full frontend ESLint
- [x] pre-push size budget, governance guards, TypeScript, and full
frontend ESLint
```


### PR body

## Summary

- correct every frontend billing mock so subscription and top-up fields represent initial wallet capacity instead of remaining balance
- make the collapsed desktop sidebar use canonical `availableCredits` instead of aliasing total wallet capacity
- preserve exhausted-trial warnings by checking canonical remaining credits instead of subscription capacity
- add regression coverage for the mock credit invariants, the reported `active-pro` display, and the sidebar prop mapping
- Linear: https://linear.app/srpone/issue/ECA-1384/staging-billing-mock-shows-inconsistent-credit-balances-across-account

## Root cause

The staging `active-pro` mock mixed two different meanings for its credit fields: `totalCredits` was 20,000, while `subscriptionCredits` incorrectly contained the remaining 11,500. The account menu rendered `availableCredits` directly, but Settings → Usage treated `subscriptionCredits + topupCredits` as initial capacity and subtracted the 8,500 usage again, producing 3,000 / 11,500.

Separately, the collapsed desktop sidebar renamed `walletTotal` to `availableCredits`, so real accounts with consumed credits could see total capacity in the tooltip.

The corrected mock semantics also exposed an existing consumer bug: `SubscriptionPanel` used subscription capacity for its low-credit warning. It now checks `availableCredits`, so an exhausted trial still warns even when its initial capacity is non-zero.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to all six changed source and test files (130 related tests)
- [x] pre-commit full frontend ESLint
- [x] pre-push size budget, governance guards, TypeScript, and full frontend ESLint



### files

- web/app/src/components/billing/SubscriptionPanel.tsx
- web/app/src/components/sidenav/SideNavUserSection.tsx
- web/app/src/lib/billing/mock-billing-data.ts
- web/app/tests/unit/billing/mockBillingData.unit.spec.ts
- web/app/tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
- web/app/tests/unit/components/sidenav/SideNavUserSection.unit.spec.tsx

---

## ac6581ec

- author: kaka-srp
- date: 2026-08-19T07:10:57Z
- pr: 3427


### commit message

```
fix(pricing): align sandbox compute specs (#3427)

## Summary

- align pricing comparison CPU/RAM with the current sandbox classes:
Starter 2C/2GB, Pro 4C/4GB, Ultra 8C/8GB
- update subscription plan-card compute copy across all supported
locales
- preserve the existing Storage values: 40GB, 200GB, and 1TB

Follow-up to #3426, which corrected the account Usage resource card.

## Validation

- `pnpm exec vitest run tests/unit/billing/constants.unit.spec.ts
tests/unit/locales/index.unit.spec.ts` (29 tests passed)
- `pnpm exec tsc --noEmit`
- ESLint on all changed frontend files
- pre-push changed-surface verification (`verify-web.sh --no-test`)

Full local test suites were not run, per request; CI remains
authoritative.
```


### PR body

## Summary

- align pricing comparison CPU/RAM with the current sandbox classes: Starter 2C/2GB, Pro 4C/4GB, Ultra 8C/8GB
- update subscription plan-card compute copy across all supported locales
- preserve the existing Storage values: 40GB, 200GB, and 1TB

Follow-up to #3426, which corrected the account Usage resource card.

## Validation

- `pnpm exec vitest run tests/unit/billing/constants.unit.spec.ts tests/unit/locales/index.unit.spec.ts` (29 tests passed)
- `pnpm exec tsc --noEmit`
- ESLint on all changed frontend files
- pre-push changed-surface verification (`verify-web.sh --no-test`)

Full local test suites were not run, per request; CI remains authoritative.



### files

- web/app/src/components/billing/constants.ts
- web/app/src/locales/ar.ts
- web/app/src/locales/de.ts
- web/app/src/locales/en.ts
- web/app/src/locales/es.ts
- web/app/src/locales/fr.ts
- web/app/src/locales/it.ts
- web/app/src/locales/ja.ts
- web/app/src/locales/ko.ts
- web/app/src/locales/pt.ts
- web/app/src/locales/zh.ts
- web/app/tests/unit/billing/constants.unit.spec.ts
- web/app/tests/unit/locales/index.unit.spec.ts

---

## 9b9801ed

- author: kaka-srp
- date: 2026-08-19T06:50:19Z
- pr: 3426


### commit message

```
fix(settings): hide sandbox storage allocation (#3426)

## Summary

- update the account usage resource card to the current sandbox classes:
Starter 2C/2GB, Pro 4C/4GB, and Ultra 8C/8GB
- hide Storage until ECAP has a product-level storage entitlement to
display
- restrict the legacy resource diagnostics request to the Status tab

Scope: public pricing and subscription plan cards intentionally keep
their existing Storage copy.

## Validation

- `pnpm exec vitest run
tests/unit/components/claw-settings/UsageTab.unit.spec.tsx
tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx
tests/unit/hooks/queries/openclaw/useClawResources.unit.spec.ts` (56
tests passed)
- `pnpm exec tsc --noEmit`
- ESLint on all changed frontend files
- pre-push changed-surface verification (`verify-web.sh --no-test`)

Full local test suites were not run, per request; CI remains
authoritative.
```


### PR body

## Summary

- update the account usage resource card to the current sandbox classes: Starter 2C/2GB, Pro 4C/4GB, and Ultra 8C/8GB
- hide Storage until ECAP has a product-level storage entitlement to display
- restrict the legacy resource diagnostics request to the Status tab

Scope: public pricing and subscription plan cards intentionally keep their existing Storage copy.

## Validation

- `pnpm exec vitest run tests/unit/components/claw-settings/UsageTab.unit.spec.tsx tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx tests/unit/hooks/queries/openclaw/useClawResources.unit.spec.ts` (56 tests passed)
- `pnpm exec tsc --noEmit`
- ESLint on all changed frontend files
- pre-push changed-surface verification (`verify-web.sh --no-test`)

Full local test suites were not run, per request; CI remains authoritative.



### files

- web/app/src/app/[locale]/(app)/claw-settings/ClawSettingsClient.tsx
- web/app/src/app/[locale]/(app)/claw-settings/components/UsageTab.tsx
- web/app/src/hooks/queries/openclaw/keys.ts
- web/app/src/hooks/queries/openclaw/useClawResources.ts
- web/app/tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx
- web/app/tests/unit/components/claw-settings/UsageTab.unit.spec.tsx
- web/app/tests/unit/hooks/queries/openclaw/useClawResources.unit.spec.ts

---

## e3b9730a

- author: tim-srp
- date: 2026-08-19T05:37:53Z
- pr: 3425


### commit message

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


### PR body

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



### files

- services/claw-interface/app/database/card_checkout_binding_repo.py
- services/claw-interface/app/services/airwallex/trial_lifecycle.py
- services/claw-interface/pyproject.toml
- services/claw-interface/tests/unit/test_airwallex_trial_lifecycle.py
- services/claw-interface/tests/unit/test_creem_first_payment_repo.py

---

## 5b15d93a

- author: kaka-srp
- date: 2026-08-19T04:09:47Z
- pr: 3418


### commit message

```
fix(agent-builder): add bounded setup recovery (#3418)

## Summary
- bound Engine v2 Agent Builder setup to a fifteen-minute attempt
deadline shared by background execution and state refresh
- add stable timeout/failure codes plus an owner-scoped retry action
that reuses the current project, fences stale setup writes, and
preserves lifecycle state
- show delayed preparation guidance after one minute, slow delayed
polling, and resynchronize ambiguous retry results
- add backend and frontend regression coverage for timeout, retry,
concurrency, polling, and UI recovery

## Root cause
Retryable Engine v2 setup failures left the persisted workspace state at
`installing`. Project-state polling kept scheduling background setup,
but there was no attempt timestamp, bounded terminal transition, or
explicit retry action. The frontend therefore continued showing the
initial preparation state without time-based progress guidance or an
in-place recovery path.

The initial five-minute recovery window was also shorter than the Engine
environment-replacement client's 390-second timeout. The final
implementation uses one fifteen-minute attempt deadline for both the
background setup execution and persisted state convergence, while
retaining the one-minute delayed-preparation notice.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] related backend unit tests: 243 passed
- [x] related frontend unit tests: 94 passed
- [x] `bash scripts/verify-py.sh`
- [x] frontend TypeScript, ESLint, and governance guards
- [x] Python complexity check
- [x] `git diff --check`
```


### PR body

## Summary
- bound Engine v2 Agent Builder setup to a fifteen-minute attempt deadline shared by background execution and state refresh
- add stable timeout/failure codes plus an owner-scoped retry action that reuses the current project, fences stale setup writes, and preserves lifecycle state
- show delayed preparation guidance after one minute, slow delayed polling, and resynchronize ambiguous retry results
- add backend and frontend regression coverage for timeout, retry, concurrency, polling, and UI recovery

## Root cause
Retryable Engine v2 setup failures left the persisted workspace state at `installing`. Project-state polling kept scheduling background setup, but there was no attempt timestamp, bounded terminal transition, or explicit retry action. The frontend therefore continued showing the initial preparation state without time-based progress guidance or an in-place recovery path.

The initial five-minute recovery window was also shorter than the Engine environment-replacement client's 390-second timeout. The final implementation uses one fifteen-minute attempt deadline for both the background setup execution and persisted state convergence, while retaining the one-minute delayed-preparation notice.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] related backend unit tests: 243 passed
- [x] related frontend unit tests: 94 passed
- [x] `bash scripts/verify-py.sh`
- [x] frontend TypeScript, ESLint, and governance guards
- [x] Python complexity check
- [x] `git diff --check`



### files

- docs/superpowers/specs/2026-08-18-agent-builder-preparing-recovery.md
- services/claw-interface/app/database/agent_builder_project_repo.py
- services/claw-interface/app/routes/agent_builder_v2.py
- services/claw-interface/app/schema/agent_builder.py
- services/claw-interface/app/services/agent_builder_service.py
- services/claw-interface/app/services/agent_builder_v2_service.py
- services/claw-interface/tests/unit/test_agent_builder_project_repo.py
- services/claw-interface/tests/unit/test_agent_builder_routes.py
- services/claw-interface/tests/unit/test_agent_builder_service.py
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderChatConversation.tsx
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderRuntimeApi.tsx
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderRuntimePresentation.ts
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderStatusPane.tsx
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderV2Api.ts
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderV2Client.tsx
- web/app/src/app/[locale]/(app)/(chat)/agent-builder/useAgentBuilderProjectQuery.ts
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts
- web/app/src/models/agent-builder.ts
- web/app/src/services/agent-builder-v2.ts
- web/app/tests/unit/app/agent-builder-client.unit.spec.tsx
- web/app/tests/unit/app/agent-builder-project-query.unit.spec.ts
- web/app/tests/unit/app/agent-builder-status-pane.unit.spec.ts
- web/app/tests/unit/services/agent-builder-v2.unit.spec.ts

---

## 0bbe11e4

- author: bill-srp
- date: 2026-08-19T03:40:53Z
- pr: 3412


### commit message

```
feat(agents): grant agents v2 eligibility to all srp.one emails (#3412)

## Linear
<!-- No Linear issue — ad-hoc rollout-gate request from Bill (all
@srp.one emails can use v2 engine agents). -->

## Summary
- Hardcode a product rule in the v2 engine-agent gate: any account email
ending with `@srp.one` is eligible, independent of
`AGENTS_V2_EMAIL_ALLOWLIST`. This mirrors the existing SRP staff pattern
(`middleware/auth.py` `_SRP_EMAIL_DOMAIN` suffix gate); the constant is
redefined locally because `app.services` must stay FastAPI-free
(import-linter C3).
- Precedence: `AGENTS_V2_ENABLED` kill switch still blocks everyone
(including `@srp.one`, pinned by test); open-rollout environments stay
wide open; the email allowlist keeps its exact-match semantics for
non-SRP users.
- Look-alike domains are rejected: `foo@notsrp.one` and `foo@x.srp.one`
do not match (literal `@srp.one` suffix required); matching is trim +
casefold like the rest of the gate.
- No config change needed — takes effect for all `@srp.one` users as
soon as the backend releases. Frontend needs no change: it consumes the
server-authoritative capability verdict and the reason enum is
unchanged.

## Test plan
- [x] TDD in `tests/unit/test_agents_v2_access.py` (red first, then
green — 17 passed): `alice@srp.one` eligible with empty allowlist in
production; case/whitespace-insensitive; kill switch still returns
`agents_v2_disabled` for srp.one emails; `foo@notsrp.one` /
`foo@x.srp.one` blocked; exact allowlist behavior unchanged
- [x] `bash scripts/verify-py.sh` — ruff check, ruff format, pyright,
import-linter all green
- [ ] CI `claw-interface-quality` (full pytest + coverage)
```


### PR body

## Linear
<!-- No Linear issue — ad-hoc rollout-gate request from Bill (all @srp.one emails can use v2 engine agents). -->

## Summary
- Hardcode a product rule in the v2 engine-agent gate: any account email ending with `@srp.one` is eligible, independent of `AGENTS_V2_EMAIL_ALLOWLIST`. This mirrors the existing SRP staff pattern (`middleware/auth.py` `_SRP_EMAIL_DOMAIN` suffix gate); the constant is redefined locally because `app.services` must stay FastAPI-free (import-linter C3).
- Precedence: `AGENTS_V2_ENABLED` kill switch still blocks everyone (including `@srp.one`, pinned by test); open-rollout environments stay wide open; the email allowlist keeps its exact-match semantics for non-SRP users.
- Look-alike domains are rejected: `foo@notsrp.one` and `foo@x.srp.one` do not match (literal `@srp.one` suffix required); matching is trim + casefold like the rest of the gate.
- No config change needed — takes effect for all `@srp.one` users as soon as the backend releases. Frontend needs no change: it consumes the server-authoritative capability verdict and the reason enum is unchanged.

## Test plan
- [x] TDD in `tests/unit/test_agents_v2_access.py` (red first, then green — 17 passed): `alice@srp.one` eligible with empty allowlist in production; case/whitespace-insensitive; kill switch still returns `agents_v2_disabled` for srp.one emails; `foo@notsrp.one` / `foo@x.srp.one` blocked; exact allowlist behavior unchanged
- [x] `bash scripts/verify-py.sh` — ruff check, ruff format, pyright, import-linter all green
- [ ] CI `claw-interface-quality` (full pytest + coverage)



### files

- services/claw-interface/app/services/agents/agents_v2_access.py
- services/claw-interface/tests/unit/test_agents_v2_access.py

---

## acd64aa1

- author: tim-srp
- date: 2026-08-19T03:34:12Z
- pr: 3424


### commit message

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


### PR body

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


### files

- services/claw-interface/app/database/card_checkout_order_repo.py
- services/claw-interface/app/services/airwallex/first_payment.py
- services/claw-interface/tests/unit/test_airwallex_first_payment.py
- services/claw-interface/tests/unit/test_creem_first_payment_repo.py

---

## 8e54be3b

- author: tim-srp
- date: 2026-08-19T02:20:05Z
- pr: 3421


### commit message

```
fix(billing): include subscription_data when creating Airwallex checkout (#3421)

## Summary

The Airwallex Billing Checkout API (`POST
/api/v1/billing/billing_checkouts/create` in `SUBSCRIPTION` mode)
requires `subscription_data` in the request body. Our code was omitting
it, so every card checkout creation returned HTTP 400:

```json
{"code": "validation_error", "message": "subscription_data must be provided for SUBSCRIPTION mode in checkout.", "source": "subscription_data"}
```

The client masks this as `billing.card_checkout.unavailable` (`Card
checkout is temporarily unavailable`).

## Root cause

Both checkout flows construct `AirwallexCreateCheckoutRequest` with
`mode="SUBSCRIPTION"` but never pass `subscription_data`. The schema
field is optional, so nothing enforced it at build time.

This was masked in staging by the earlier misconfigured Product IDs
(`prd_` prefix); once those were fixed, this surfaced as the remaining
400.

## Fix

Add `subscription_data` with the `duration` derived from the billing
cycle to both flows:

- `card_checkout.py` — new subscription (incl. trial)
- `airwallex_upgrade_checkout.py` — upgrade

Shared helper `_subscription_duration` in `card_checkout_shared.py` maps
`MONTHLY → MONTH`, `YEARLY → YEAR` with `period=1`.

Verified against live Airwallex sandbox with staging credentials: the
exact request shape now returns 201.

## Tests

- `test_card_checkout.py`: assert `subscription_data.duration` on
new-subscription flow
- `test_card_checkout_upgrade.py`: assert `subscription_data.duration`
on upgrade flow
- 218 affected unit tests pass; ruff + pyright clean
```


### PR body

## Summary

The Airwallex Billing Checkout API (`POST /api/v1/billing/billing_checkouts/create` in `SUBSCRIPTION` mode) requires `subscription_data` in the request body. Our code was omitting it, so every card checkout creation returned HTTP 400:

```json
{"code": "validation_error", "message": "subscription_data must be provided for SUBSCRIPTION mode in checkout.", "source": "subscription_data"}
```

The client masks this as `billing.card_checkout.unavailable` (`Card checkout is temporarily unavailable`).

## Root cause

Both checkout flows construct `AirwallexCreateCheckoutRequest` with `mode="SUBSCRIPTION"` but never pass `subscription_data`. The schema field is optional, so nothing enforced it at build time.

This was masked in staging by the earlier misconfigured Product IDs (`prd_` prefix); once those were fixed, this surfaced as the remaining 400.

## Fix

Add `subscription_data` with the `duration` derived from the billing cycle to both flows:

- `card_checkout.py` — new subscription (incl. trial)
- `airwallex_upgrade_checkout.py` — upgrade

Shared helper `_subscription_duration` in `card_checkout_shared.py` maps `MONTHLY → MONTH`, `YEARLY → YEAR` with `period=1`.

Verified against live Airwallex sandbox with staging credentials: the exact request shape now returns 201.

## Tests

- `test_card_checkout.py`: assert `subscription_data.duration` on new-subscription flow
- `test_card_checkout_upgrade.py`: assert `subscription_data.duration` on upgrade flow
- 218 affected unit tests pass; ruff + pyright clean


### files

- services/claw-interface/app/services/billing_v2/airwallex_upgrade_checkout.py
- services/claw-interface/app/services/billing_v2/card_checkout.py
- services/claw-interface/app/services/billing_v2/card_checkout_shared.py
- services/claw-interface/tests/unit/test_card_checkout.py
- services/claw-interface/tests/unit/test_card_checkout_upgrade.py

---
