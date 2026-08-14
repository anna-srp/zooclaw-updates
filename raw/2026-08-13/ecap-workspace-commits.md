# SerendipityOneInc/ecap-workspace commits 2026-08-13

## 5200a600

- sha: `5200a6006d99e33361cab26aa54ba2b28d87daaf`
- 作者: tim-srp
- 日期: 2026-08-13T13:45:12Z
- PR: 3376

### Commit message

```
feat(billing): make restaurant vertical pack plan id configurable (#3376)

## 背景

Restaurant vertical pack 的 Card 支付按硬编码 `RESTAURANT_VERTICAL_PACK_PLAN_ID
= "d1d634df7fed439cbcdb499671a83adc"` 判断是否走 Creem。staging 和 production
各自有不同的 vertical pack Plan ID，无法使用该路径。

## 变更

把 plan id 改为环境配置项，逻辑完全不变，只改取值来源：

- **`settings.py`**：新增
`CREEM_PLAN_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY: str = ""`
-
**`enterprise_catalog.py`**：删除硬编码常量，`resolve_restaurant_vertical_pack_product`
从 settings 读取 plan id（配置非空、无前后空格校验，与 product id 同模式）
- **`enterprise_package_provider.py` / `plan.py`**：判断改读
`SETTINGS.CREEM_PLAN_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY`

其余契约（金额 $299、20,000 credits、USD、monthly、不允许 add-on、Creem product
实时校验）不变。

## 部署

staging/production 各自配置
`CREEM_PLAN_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY` 为对应环境的
Restaurant vertical pack Plan ID 即可。

## 测试

- `test_creem_enterprise_catalog.py`：新增「环境配置的 plan id 可
resolve」「配置缺失/带空格时 reject」用例
- 所有直接/间接依赖全局 SETTINGS 的测试文件补齐 plan id 配置 patch
- 1160 个相关单元测试全部通过；ruff/ruff-format/import-linter 通过

本地 pyright 对 `r2_storage.py` 的 boto3 误报（与本次改动无关）需 `SKIP_VERIFY=1` 绕过；CI
无此问题。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR body

## 背景

Restaurant vertical pack 的 Card 支付按硬编码 `RESTAURANT_VERTICAL_PACK_PLAN_ID = "d1d634df7fed439cbcdb499671a83adc"` 判断是否走 Creem。staging 和 production 各自有不同的 vertical pack Plan ID，无法使用该路径。

## 变更

把 plan id 改为环境配置项，逻辑完全不变，只改取值来源：

- **`settings.py`**：新增 `CREEM_PLAN_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY: str = ""`
- **`enterprise_catalog.py`**：删除硬编码常量，`resolve_restaurant_vertical_pack_product` 从 settings 读取 plan id（配置非空、无前后空格校验，与 product id 同模式）
- **`enterprise_package_provider.py` / `plan.py`**：判断改读 `SETTINGS.CREEM_PLAN_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY`

其余契约（金额 $299、20,000 credits、USD、monthly、不允许 add-on、Creem product 实时校验）不变。

## 部署

staging/production 各自配置 `CREEM_PLAN_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY` 为对应环境的 Restaurant vertical pack Plan ID 即可。

## 测试

- `test_creem_enterprise_catalog.py`：新增「环境配置的 plan id 可 resolve」「配置缺失/带空格时 reject」用例
- 所有直接/间接依赖全局 SETTINGS 的测试文件补齐 plan id 配置 patch
- 1160 个相关单元测试全部通过；ruff/ruff-format/import-linter 通过

本地 pyright 对 `r2_storage.py` 的 boto3 误报（与本次改动无关）需 `SKIP_VERIFY=1` 绕过；CI 无此问题。

🤖 Generated with [Claude Code](https://claude.com/claude-code)


## d0368608

- sha: `d0368608ccc089dd67079411c8e0788484fd862c`
- 作者: tim-srp
- 日期: 2026-08-13T12:14:57Z
- PR: 3373

### Commit message

```
fix(enterprise-admin): accept card channel and manual-review status in auth/me (#3373)

<!-- PR 标题：fix(enterprise-admin): accept card channel and manual-review
status in auth/me -->

## Summary
- Enterprise Admin `/api/auth/me` 返回 502 的场景:用户通过 Creem
银行卡(Card)支付后,`GET /account/me` 返回 `payment_channel: "card"`;或订阅处于人工审核时返回
`subscription_status: "manual_review"`。前端 zod 契约只允许
`stripe/antom/apple/offline` 和旧的 subscription status 集合,校验失败后 BFF 兜底成
502,checkout 页面错误显示 "We couldn't start checkout"。
- 修复:`types/user-me.ts` 两个枚举对齐后端 `UserMeResponse` Literal(`card` +
`manual_review`),并补契约测试(客户端登录流 + BFF 路由两层)。

## Root cause
- `account_api.py` 的 `UserMeResponse`(后端契约)已支持 `payment_channel:
"card"`(Creem card checkout 的 `creem → "card"` 映射在 `order_requests.py` /
`billing_summary/adapters.py`,均为 main 上已有行为)和 `subscription_status:
"manual_review"`。
- enterprise-admin 的 zod schema(`types/user-me.ts`)未跟随该契约更新;ZodError 无
HTTP status,`app/api/auth/me/route.ts` catch 后兜底返回 502。
- web/app(main app)的模型已包含 `"card"`,仅 enterprise-admin 遗漏。

## Test plan
- [x] `pnpm test`:52 files / 375 tests 通过(含新增 3 个契约用例)
- [x] `pnpm run lint`、`pnpm exec tsc --noEmit` 通过
- [x] 新增用例:
- 客户端 `completeLogin`:`payment_channel: "card"` / `subscription_status:
"manual_review"` 解析成功
  - BFF `GET /api/auth/me`:claw 返回上述字段时响应 200(而非 502)

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR body

<!-- PR 标题：fix(enterprise-admin): accept card channel and manual-review status in auth/me -->

## Summary
- Enterprise Admin `/api/auth/me` 返回 502 的场景:用户通过 Creem 银行卡(Card)支付后,`GET /account/me` 返回 `payment_channel: "card"`;或订阅处于人工审核时返回 `subscription_status: "manual_review"`。前端 zod 契约只允许 `stripe/antom/apple/offline` 和旧的 subscription status 集合,校验失败后 BFF 兜底成 502,checkout 页面错误显示 "We couldn't start checkout"。
- 修复:`types/user-me.ts` 两个枚举对齐后端 `UserMeResponse` Literal(`card` + `manual_review`),并补契约测试(客户端登录流 + BFF 路由两层)。

## Root cause
- `account_api.py` 的 `UserMeResponse`(后端契约)已支持 `payment_channel: "card"`(Creem card checkout 的 `creem → "card"` 映射在 `order_requests.py` / `billing_summary/adapters.py`,均为 main 上已有行为)和 `subscription_status: "manual_review"`。
- enterprise-admin 的 zod schema(`types/user-me.ts`)未跟随该契约更新;ZodError 无 HTTP status,`app/api/auth/me/route.ts` catch 后兜底返回 502。
- web/app(main app)的模型已包含 `"card"`,仅 enterprise-admin 遗漏。

## Test plan
- [x] `pnpm test`:52 files / 375 tests 通过(含新增 3 个契约用例)
- [x] `pnpm run lint`、`pnpm exec tsc --noEmit` 通过
- [x] 新增用例:
  - 客户端 `completeLogin`:`payment_channel: "card"` / `subscription_status: "manual_review"` 解析成功
  - BFF `GET /api/auth/me`:claw 返回上述字段时响应 200(而非 502)


## ffc55541

- sha: `ffc555410b240fb0484c906ee769f5d84d195bdc`
- 作者: tim-srp
- 日期: 2026-08-13T11:44:29Z
- PR: 3359

### Commit message

```
feat(billing): support Creem vertical pack checkout (#3359)

## Linear

N/A — requested directly for the Restaurant AI Agent Team checkout
rollout.

## Summary

- route only Restaurant AI Agent Team Card checkout through Creem while
keeping other vertical Card checkouts on Stripe
- keep Alipay/Antom request and lifecycle behavior unchanged
- validate the server-owned $299 monthly Product and immutable package
snapshot before creating a Checkout
- add team/environment reservation, exact replay, signed-webhook binding
recovery, and hourly reconciliation support
- soft-delete only the newly created package that loses the team
reservation insert race
- project initial payment, renewals, `past_due`, recoverable `expired`,
and terminal `canceled` into enterprise Agreements and deterministic
20,000-credit team entitlements
- expose typed Card capability/provider data to Enterprise Admin and
fail Restaurant Card checkout closed when Creem is unavailable or
add-ons are selected

## Test plan

- [x] `python -m pytest -q tests/unit/test_creem*.py
tests/unit/test_antom*.py tests/unit/test_orders_antom*.py
tests/unit/test_enterprise_package*.py tests/unit/test_vertical_pack*.py
tests/unit/test_schema_vertical_pack*.py` — 1,061 passed
- [x] `pnpm test` in `web/enterprise-admin` — 368 passed
- [x] `pnpm run lint` and `pnpm exec tsc --noEmit` in
`web/enterprise-admin`
- [x] `pnpm build` in `web/enterprise-admin`
- [x] Ruff check/format, import-linter, complexity, deptry,
collection-name, repo-sync, dead-code, and database-return guards
- [x] Pyright on all changed Python files — 0 errors
- [x] `git diff --check`

Local full-repository Pyright is limited by the workstation boto typing
baseline: it reports the same seven `BaseClient` attribute errors in
unchanged `app/services/r2_storage.py`; no changed file reports a type
error. CI remains authoritative.

## Rollout

- requires `CREEM_VERTICAL_PACK_CARD_CHECKOUT_ENABLED=true`
- requires environment-specific
`CREEM_PRODUCT_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY`
- disabling the vertical feature flag stops only new Restaurant Card
sales; existing webhook/reconciliation handling remains enabled
- no Product ID or credential is committed

## Size rationale

This is one payment-lifecycle unit: checkout creation, webhook
settlement, renewal, cancellation, and reconciliation must deploy
together to avoid accepting money without a complete entitlement or
recovery path. The diff is approximately 2,499 lines of business code,
1,725 lines of tests, and 165 lines of design/plan documentation; the PR
therefore needs the repository `size-override` label.

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR body

## Linear

N/A — requested directly for the Restaurant AI Agent Team checkout rollout.

## Summary

- route only Restaurant AI Agent Team Card checkout through Creem while keeping other vertical Card checkouts on Stripe
- keep Alipay/Antom request and lifecycle behavior unchanged
- validate the server-owned $299 monthly Product and immutable package snapshot before creating a Checkout
- add team/environment reservation, exact replay, signed-webhook binding recovery, and hourly reconciliation support
- soft-delete only the newly created package that loses the team reservation insert race
- project initial payment, renewals, `past_due`, recoverable `expired`, and terminal `canceled` into enterprise Agreements and deterministic 20,000-credit team entitlements
- expose typed Card capability/provider data to Enterprise Admin and fail Restaurant Card checkout closed when Creem is unavailable or add-ons are selected

## Test plan

- [x] `python -m pytest -q tests/unit/test_creem*.py tests/unit/test_antom*.py tests/unit/test_orders_antom*.py tests/unit/test_enterprise_package*.py tests/unit/test_vertical_pack*.py tests/unit/test_schema_vertical_pack*.py` — 1,061 passed
- [x] `pnpm test` in `web/enterprise-admin` — 368 passed
- [x] `pnpm run lint` and `pnpm exec tsc --noEmit` in `web/enterprise-admin`
- [x] `pnpm build` in `web/enterprise-admin`
- [x] Ruff check/format, import-linter, complexity, deptry, collection-name, repo-sync, dead-code, and database-return guards
- [x] Pyright on all changed Python files — 0 errors
- [x] `git diff --check`

Local full-repository Pyright is limited by the workstation boto typing baseline: it reports the same seven `BaseClient` attribute errors in unchanged `app/services/r2_storage.py`; no changed file reports a type error. CI remains authoritative.

## Rollout

- requires `CREEM_VERTICAL_PACK_CARD_CHECKOUT_ENABLED=true`
- requires environment-specific `CREEM_PRODUCT_ID_VERTICAL_PACK_RESTAURANT_AI_TEAM_MONTHLY`
- disabling the vertical feature flag stops only new Restaurant Card sales; existing webhook/reconciliation handling remains enabled
- no Product ID or credential is committed

## Size rationale

This is one payment-lifecycle unit: checkout creation, webhook settlement, renewal, cancellation, and reconciliation must deploy together to avoid accepting money without a complete entitlement or recovery path. The diff is approximately 2,499 lines of business code, 1,725 lines of tests, and 165 lines of design/plan documentation; the PR therefore needs the repository `size-override` label.


## 39e04324

- sha: `39e04324d8136134434deaef51adc7e092b40ca3`
- 作者: tim-srp
- 日期: 2026-08-13T10:52:49Z
- PR: 3365

### Commit message

```
feat(billing): migrate Card topups to Creem (#3365)

## Linear

N/A

## Summary

- Route the existing three Card add-on packs (1,000 / 5,000 / 10,000
credits) through Creem one-time products while preserving the current
order admission and pricing rules.
- Add server-owned Creem top-up catalog validation, idempotent Checkout
creation, signed webhook settlement, and one-time entitlement
fulfillment.
- Add success-page active Checkout confirmation so completed payments
can recover immediately when the webhook is delayed, while leaving
subscription Card and Antom flows unchanged.
- Document the scoped migration design and implementation plan.

## Test plan

- [x] Backend top-up, Card route, Creem fulfillment, and reconciliation
tests: 87 passed.
- [x] Frontend selected verification: TypeScript, ESLint, 359 passed / 1
skipped.
- [x] Ruff formatting/lint and import contracts passed.
- [x] Pre-commit Pyright passed in the configured hook environment.
- [ ] GitHub Actions run in the authoritative CI environment.

## Deployment configuration

- Configure `CREEM_PRODUCT_ID_TOPUP_1000`,
`CREEM_PRODUCT_ID_TOPUP_5000`, and `CREEM_PRODUCT_ID_TOPUP_10000` with
the corresponding environment's Creem one-time Product IDs before
enabling the flow.
- No hourly top-up reconciliation fallback is included in this PR;
recovery is webhook-first with success-page active confirmation.
```

### PR body

## Linear

N/A

## Summary

- Route the existing three Card add-on packs (1,000 / 5,000 / 10,000 credits) through Creem one-time products while preserving the current order admission and pricing rules.
- Add server-owned Creem top-up catalog validation, idempotent Checkout creation, signed webhook settlement, and one-time entitlement fulfillment.
- Add success-page active Checkout confirmation so completed payments can recover immediately when the webhook is delayed, while leaving subscription Card and Antom flows unchanged.
- Document the scoped migration design and implementation plan.

## Test plan

- [x] Backend top-up, Card route, Creem fulfillment, and reconciliation tests: 87 passed.
- [x] Frontend selected verification: TypeScript, ESLint, 359 passed / 1 skipped.
- [x] Ruff formatting/lint and import contracts passed.
- [x] Pre-commit Pyright passed in the configured hook environment.
- [ ] GitHub Actions run in the authoritative CI environment.

## Deployment configuration

- Configure `CREEM_PRODUCT_ID_TOPUP_1000`, `CREEM_PRODUCT_ID_TOPUP_5000`, and `CREEM_PRODUCT_ID_TOPUP_10000` with the corresponding environment's Creem one-time Product IDs before enabling the flow.
- No hourly top-up reconciliation fallback is included in this PR; recovery is webhook-first with success-page active confirmation.


## 61cb4710

- sha: `61cb471047acd03427c7feb38862e7ade72e1534`
- 作者: kaka-srp
- 日期: 2026-08-13T10:48:54Z
- PR: 3370

### Commit message

```
feat(agent-builder): restore v2 fork and test attachments (#3370)

## Linear

N/A

## Summary

- restore the V2-only “Start from an existing agent” flow in the Create
Agent dialog, using every current-user-accessible Pack as an eligible
starting point
- filter and revalidate sources against immutable Engine runtime assets,
pin the complete asset identity on the Project, and preserve production
V2 Pack root files during import
- add attachment upload to the V2 Test Agent composer, including
attachment-only turns and feedback handling

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh <affected Agent Builder and Pack
service paths>`
- [x] targeted backend tests: 37 passed
- [x] targeted frontend tests: 157 passed
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks
```

### PR body

## Linear

N/A

## Summary

- restore the V2-only “Start from an existing agent” flow in the Create Agent dialog, using every current-user-accessible Pack as an eligible starting point
- filter and revalidate sources against immutable Engine runtime assets, pin the complete asset identity on the Project, and preserve production V2 Pack root files during import
- add attachment upload to the V2 Test Agent composer, including attachment-only turns and feedback handling

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh <affected Agent Builder and Pack service paths>`
- [x] targeted backend tests: 37 passed
- [x] targeted frontend tests: 157 passed
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push hooks


## 9422d783

- sha: `9422d78324d18d454226533c00673cc34d7d30c5`
- 作者: tim-srp
- 日期: 2026-08-13T09:24:25Z
- PR: 3364

### Commit message

```
feat(billing): add Creem customer portal (#3364)

## Linear

N/A

## Summary

- add an authenticated, strictly typed Creem Customer Portal endpoint
that resolves customer identity and environment from the
caller-manageable Subscription Agreement
- route Card payment-method and billing-history actions to Creem while
keeping Stripe Billing Portal and per-order hosted invoice downloads
unchanged
- validate official credential-free Creem portal URLs, add all supported
locale strings, local mock support, and backend/frontend regression
coverage

## Test plan

- [x] production read-only validation: the restricted current Stripe
account can retrieve a post-cutover invoice and its hosted invoice URL
returns HTTP 200
- [x] `services/claw-interface/.venv/bin/python -m pytest
tests/unit/test_creem_client.py tests/unit/test_creem_portal.py
tests/unit/test_billing_card_routes.py
tests/unit/test_stripe_endpoints.py tests/unit/test_invoice_lookup.py
-q` (173 passed)
- [x] `pyright --pythonpath .venv/bin/python app/ tests/` (0 errors)
- [x] `bash scripts/verify-web.sh src/services/billing.ts
src/components/billing/InvoiceHistory.tsx
tests/unit/services/billing.unit.spec.ts
tests/unit/components/billing/InvoiceHistory.unit.spec.tsx` (324 passed,
1 skipped; typecheck and lint passed)
- [x] pre-commit frontend lint, Ruff, Ruff format, import contracts,
complexity checks, and Pyright passed

## Notes

- `bash scripts/verify-changed.sh` selected the host Miniconda Pyright
and reported missing worktree dependencies. Running the same full
Pyright scope with the worktree virtualenv explicitly selected completed
with 0 errors.
```

### PR body

## Linear

N/A

## Summary

- add an authenticated, strictly typed Creem Customer Portal endpoint that resolves customer identity and environment from the caller-manageable Subscription Agreement
- route Card payment-method and billing-history actions to Creem while keeping Stripe Billing Portal and per-order hosted invoice downloads unchanged
- validate official credential-free Creem portal URLs, add all supported locale strings, local mock support, and backend/frontend regression coverage

## Test plan

- [x] production read-only validation: the restricted current Stripe account can retrieve a post-cutover invoice and its hosted invoice URL returns HTTP 200
- [x] `services/claw-interface/.venv/bin/python -m pytest tests/unit/test_creem_client.py tests/unit/test_creem_portal.py tests/unit/test_billing_card_routes.py tests/unit/test_stripe_endpoints.py tests/unit/test_invoice_lookup.py -q` (173 passed)
- [x] `pyright --pythonpath .venv/bin/python app/ tests/` (0 errors)
- [x] `bash scripts/verify-web.sh src/services/billing.ts src/components/billing/InvoiceHistory.tsx tests/unit/services/billing.unit.spec.ts tests/unit/components/billing/InvoiceHistory.unit.spec.tsx` (324 passed, 1 skipped; typecheck and lint passed)
- [x] pre-commit frontend lint, Ruff, Ruff format, import contracts, complexity checks, and Pyright passed

## Notes

- `bash scripts/verify-changed.sh` selected the host Miniconda Pyright and reported missing worktree dependencies. Running the same full Pyright scope with the worktree virtualenv explicitly selected completed with 0 errors.


## 0985af06

- sha: `0985af06d0ec7a100a81110e3a3bd84efd3c0726`
- 作者: kaka-srp
- 日期: 2026-08-13T08:31:49Z
- PR: 3363

### Commit message

```
fix(channels): normalize access and reconnect Weixin (#3363)

## Summary

- create managed Mattermost channels with the currently supported `open`
DM policy and `allow_from=["*"]`
- reconcile existing Mattermost rows from the legacy effective-open
configuration through ACS update after a strict create conflict
- add an always-available Weixin reauthorization action for Engine
channels using the existing in-place QR refresh flow
- pass through ACS `status_code`; display the explicit “login expired”
prompt only when ACS reports `SESSION_EXPIRED`
- pair with SerendipityOneInc/agent-channel-service#72, which validates
outbound results and exposes structured gateway status

This implements the narrowed conclusions recorded on
SerendipityOneInc/agent-channel-service#53 and
SerendipityOneInc/agent-channel-service#54. Pairing, allowlist,
plugin-native command parity, directory listing, and mention aliases
remain demand-driven follow-ups.

## Root cause

Mattermost provisioning omitted DM policy fields and inherited ACS's
`pairing + ["*"]` defaults. The wildcard made the runtime effectively
open, but the persisted policy was misleading. Existing rows also
require reconciliation because ACS create is intentionally strict and
rejects configuration drift.

The Weixin provider already detects `errcode=-14` as `SESSION_EXPIRED`,
and the ECAP backend already updates an existing default channel after a
successful QR scan. Previously ACS reduced the provider status to
`health=unhealthy`, so ECAP could neither distinguish token expiry nor
explain the required action. The linked ACS PR preserves the structured
code; this PR passes it through and maps it to the user-facing
reauthorization prompt.

## Test plan

- [x] 93 related claw-interface tests passed
- [x] `bash scripts/verify-py.sh`
- [x] channel-targeted frontend suite: 19 passed
- [x] TypeScript and ESLint passed
- [x] pre-commit and pre-push changed-surface gates passed

An incidental broad Vitest selection hit one unrelated `MarkdownContent`
hydration timeout while 5,142 tests passed; the channel-targeted tests
and static gates passed, and CI remains authoritative for the full
suite.
```

### PR body

## Summary

- create managed Mattermost channels with the currently supported `open` DM policy and `allow_from=["*"]`
- reconcile existing Mattermost rows from the legacy effective-open configuration through ACS update after a strict create conflict
- add an always-available Weixin reauthorization action for Engine channels using the existing in-place QR refresh flow
- pass through ACS `status_code`; display the explicit “login expired” prompt only when ACS reports `SESSION_EXPIRED`
- pair with SerendipityOneInc/agent-channel-service#72, which validates outbound results and exposes structured gateway status

This implements the narrowed conclusions recorded on SerendipityOneInc/agent-channel-service#53 and SerendipityOneInc/agent-channel-service#54. Pairing, allowlist, plugin-native command parity, directory listing, and mention aliases remain demand-driven follow-ups.

## Root cause

Mattermost provisioning omitted DM policy fields and inherited ACS's `pairing + ["*"]` defaults. The wildcard made the runtime effectively open, but the persisted policy was misleading. Existing rows also require reconciliation because ACS create is intentionally strict and rejects configuration drift.

The Weixin provider already detects `errcode=-14` as `SESSION_EXPIRED`, and the ECAP backend already updates an existing default channel after a successful QR scan. Previously ACS reduced the provider status to `health=unhealthy`, so ECAP could neither distinguish token expiry nor explain the required action. The linked ACS PR preserves the structured code; this PR passes it through and maps it to the user-facing reauthorization prompt.

## Test plan

- [x] 93 related claw-interface tests passed
- [x] `bash scripts/verify-py.sh`
- [x] channel-targeted frontend suite: 19 passed
- [x] TypeScript and ESLint passed
- [x] pre-commit and pre-push changed-surface gates passed

An incidental broad Vitest selection hit one unrelated `MarkdownContent` hydration timeout while 5,142 tests passed; the channel-targeted tests and static gates passed, and CI remains authoritative for the full suite.


## ddfe97f4

- sha: `ddfe97f4d5bf290eebd02b6595539721f0b24685`
- 作者: Chris@ZooClaw
- 日期: 2026-08-13T06:27:41Z
- PR: 3362

### Commit message

```
docs(architecture): add v2 ACS data plane (#3362)

## Summary
- The main architecture diagram stays the production OpenClaw /
Mattermost path.
- Add the parallel v2 data plane: `web → claw-interface →
zooclaw-engine` for lifecycle, `IM provider → agent-channel-service →
zooclaw-engine` for chat.
- Channel CRUD goes to ACS (`AGENT_CHANNEL_SERVICE_URL`), not through
`ZOOCLAW_ENGINE_URL`.
- Inventory, deploy-version exceptions, and env-var tables now include
ACS.

## Test plan
- [x] Docs-only change; no runtime or test files touched.
- [ ] Review the new mermaid against `engine_client/` and
`channel_service_client/`.
```

### PR body

## Summary
- The main architecture diagram stays the production OpenClaw / Mattermost path.
- Add the parallel v2 data plane: `web → claw-interface → zooclaw-engine` for lifecycle, `IM provider → agent-channel-service → zooclaw-engine` for chat.
- Channel CRUD goes to ACS (`AGENT_CHANNEL_SERVICE_URL`), not through `ZOOCLAW_ENGINE_URL`.
- Inventory, deploy-version exceptions, and env-var tables now include ACS.

## Test plan
- [x] Docs-only change; no runtime or test files touched.
- [ ] Review the new mermaid against `engine_client/` and `channel_service_client/`.


## d872e4f4

- sha: `d872e4f44bf1ff5c58f0bc92089c5dd13e576c8e`
- 作者: siqiao-srp
- 日期: 2026-08-13T06:18:00Z
- PR: 3360

### Commit message

```
fix(openclaw): align Auto capability with image .21 (#3360)

## Summary
- lower the Agent-scoped Auto capability boundary from bot image
`2026.6.11.22` to `2026.6.11.21`
- exercise the exact `.20` rejected / `.21` accepted boundary across
capability and OpenClaw settings tests
- align the English/Chinese architecture docs and backend operator
guidance with the deployed image contract

## Root cause
The capability gate added with #3307 was set one image too high.
`2026.6.11.21` is the first official bot image that bundles
`@zooclaw/model-router` `20260611.4.3`; the companion infrastructure
rollout in SerendipityOneInc/gcp-foundation#486 also uses `.21`. As a
result, compatible `.21` bots incorrectly hid and rejected Auto.

The gate remains fail-closed: `.20`, missing images, mutable tags such
as `latest`, and non-numeric tags remain unsupported.

Companion rollout references:
- SerendipityOneInc/openclaw-docker#186
- SerendipityOneInc/gcp-foundation#486
- #3307

## Test plan
- [x] `pytest tests/unit/test_model_router_capability.py
tests/unit/test_agent_settings_effective_model.py -q` (19 passed)
- [x] `pytest tests/unit/test_openclaw_settings_routes.py -q` (314
passed)
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, import
contracts)
- [x] `git diff --check`
```

### PR body

## Summary
- lower the Agent-scoped Auto capability boundary from bot image `2026.6.11.22` to `2026.6.11.21`
- exercise the exact `.20` rejected / `.21` accepted boundary across capability and OpenClaw settings tests
- align the English/Chinese architecture docs and backend operator guidance with the deployed image contract

## Root cause
The capability gate added with #3307 was set one image too high. `2026.6.11.21` is the first official bot image that bundles `@zooclaw/model-router` `20260611.4.3`; the companion infrastructure rollout in SerendipityOneInc/gcp-foundation#486 also uses `.21`. As a result, compatible `.21` bots incorrectly hid and rejected Auto.

The gate remains fail-closed: `.20`, missing images, mutable tags such as `latest`, and non-numeric tags remain unsupported.

Companion rollout references:
- SerendipityOneInc/openclaw-docker#186
- SerendipityOneInc/gcp-foundation#486
- #3307

## Test plan
- [x] `pytest tests/unit/test_model_router_capability.py tests/unit/test_agent_settings_effective_model.py -q` (19 passed)
- [x] `pytest tests/unit/test_openclaw_settings_routes.py -q` (314 passed)
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, import contracts)
- [x] `git diff --check`


## 5ecbb443

- sha: `5ecbb44378ed59d0e27c036e23db34ee64c2de15`
- 作者: bill-srp
- 日期: 2026-08-13T05:34:55Z
- PR: 3361

### Commit message

```
fix(whatsapp): align engine session event contracts (#3361)

## Summary

- align Engine session event write acknowledgements with the current `{
events: [{ id, type, accepted }] }` response
- model session event reads separately and translate `agent.assistant`
payloads into the WhatsApp delivery contract
- send WhatsApp message IDs through Engine's supported `idempotency_key`
field
- remove stale bridge fields and add regressions for write/read contract
drift
- audit the remaining Engine client surfaces against current Engine
routes; no additional response-shape mismatches were found

## Root cause

The WhatsApp ingress reached staging successfully, but claw-interface
parsed the Engine event-write acknowledgement as though it were a
session event read row requiring `seq`. Pydantic rejected the valid
acknowledgement, claw-interface classified it as an invalid upstream
response, and returned 502.

The same integration also used the obsolete `agent.message` delivery
type and sent `external_msg_id`, which Engine does not consume. Without
correcting those latent mismatches, replies would still fail after the
initial 502 was removed.

## Test plan

- [x] Engine client contract tests: 141 passed
- [x] focused claw-interface session tests: 23 passed
- [x] full claw-interface Pyright with project interpreter: 0 errors
- [x] Ruff check and format check
- [x] import-linter architecture contracts
- [x] WhatsApp service tests: 42 passed
- [x] WhatsApp service typecheck and production build

`scripts/verify-changed.sh` could not discover packages installed in the
project virtual environment when invoking Pyright without an explicit
interpreter. Running the same full Pyright target with
`.venv/bin/python` passed with zero errors; CI remains authoritative.
```

### PR body

## Summary

- align Engine session event write acknowledgements with the current `{ events: [{ id, type, accepted }] }` response
- model session event reads separately and translate `agent.assistant` payloads into the WhatsApp delivery contract
- send WhatsApp message IDs through Engine's supported `idempotency_key` field
- remove stale bridge fields and add regressions for write/read contract drift
- audit the remaining Engine client surfaces against current Engine routes; no additional response-shape mismatches were found

## Root cause

The WhatsApp ingress reached staging successfully, but claw-interface parsed the Engine event-write acknowledgement as though it were a session event read row requiring `seq`. Pydantic rejected the valid acknowledgement, claw-interface classified it as an invalid upstream response, and returned 502.

The same integration also used the obsolete `agent.message` delivery type and sent `external_msg_id`, which Engine does not consume. Without correcting those latent mismatches, replies would still fail after the initial 502 was removed.

## Test plan

- [x] Engine client contract tests: 141 passed
- [x] focused claw-interface session tests: 23 passed
- [x] full claw-interface Pyright with project interpreter: 0 errors
- [x] Ruff check and format check
- [x] import-linter architecture contracts
- [x] WhatsApp service tests: 42 passed
- [x] WhatsApp service typecheck and production build

`scripts/verify-changed.sh` could not discover packages installed in the project virtual environment when invoking Pyright without an explicit interpreter. Running the same full Pyright target with `.venv/bin/python` passed with zero errors; CI remains authoritative.


## ca3563a9

- sha: `ca3563a9dcbd189b0abeb99c3974abcd19b22681`
- 作者: kaka-srp
- 日期: 2026-08-13T02:57:31Z
- PR: 3354

### Commit message

```
feat(org): support existing-account enterprise org switching (#3354)

## Summary

- Unify personal-account and enterprise-account invitation handoff into
one V2 flow with explicit user confirmation.
- Stop all source V2 Agents, schedules, and managed channels before
switching; stop every non-terminal personal subscription renewal while
preserving enterprise package agreements.
- Rebind and verify the canonical Billing V2 key before atomically
swapping the active membership.
- Allow the first/only or last administrator to leave a mistakenly
created organization without changing that organization subscription or
promoting another member.
- Support inactive former-member reinvitation and B → C → B, plus
authenticated invite preview and enterprise-admin confirmation UX.
- Add owner-renewed transition leases, stale-owner fencing, key-bind
crash recovery, compensation, and retry-safe invite handling.

## Scope and safety

- V2 architecture only; no OpenClaw/V1 or iOS changes.
- No new collection, index, migration, or backfill.
- Source enterprise subscriptions remain unchanged.
- Personal subscriptions in pending/manual-review/unknown states fail
closed.
- Lost lease owners cannot mutate the canonical key or invitation
checkpoint.

## Verification

- Backend focused regression: 350 passed.
- Enterprise-admin test suite: 365 passed; ESLint passed.
- `verify-py.sh`: Ruff, Pyright, and all import contracts passed.
- All Python pre-commit/CI custom lint guards passed.
- Real Mongo org lifecycle BDD: 4 passed.
- Real Mongo B → C → B membership transaction and multiple historical
personal-subscription lookup verified.
- Final agent code review: no findings.

## Size override

This cohesive end-to-end change spans the backend coordinator, Billing
V2 cancellation adapters, invitation API, admin confirmation UI,
documentation, and failure-injection tests. Splitting it would create
intermediate revisions where the wire contract or safety invariants are
incomplete, so this PR intentionally uses the repository size override.
```

### PR body

## Summary

- Unify personal-account and enterprise-account invitation handoff into one V2 flow with explicit user confirmation.
- Stop all source V2 Agents, schedules, and managed channels before switching; stop every non-terminal personal subscription renewal while preserving enterprise package agreements.
- Rebind and verify the canonical Billing V2 key before atomically swapping the active membership.
- Allow the first/only or last administrator to leave a mistakenly created organization without changing that organization subscription or promoting another member.
- Support inactive former-member reinvitation and B → C → B, plus authenticated invite preview and enterprise-admin confirmation UX.
- Add owner-renewed transition leases, stale-owner fencing, key-bind crash recovery, compensation, and retry-safe invite handling.

## Scope and safety

- V2 architecture only; no OpenClaw/V1 or iOS changes.
- No new collection, index, migration, or backfill.
- Source enterprise subscriptions remain unchanged.
- Personal subscriptions in pending/manual-review/unknown states fail closed.
- Lost lease owners cannot mutate the canonical key or invitation checkpoint.

## Verification

- Backend focused regression: 350 passed.
- Enterprise-admin test suite: 365 passed; ESLint passed.
- `verify-py.sh`: Ruff, Pyright, and all import contracts passed.
- All Python pre-commit/CI custom lint guards passed.
- Real Mongo org lifecycle BDD: 4 passed.
- Real Mongo B → C → B membership transaction and multiple historical personal-subscription lookup verified.
- Final agent code review: no findings.

## Size override

This cohesive end-to-end change spans the backend coordinator, Billing V2 cancellation adapters, invitation API, admin confirmation UI, documentation, and failure-injection tests. Splitting it would create intermediate revisions where the wire contract or safety invariants are incomplete, so this PR intentionally uses the repository size override.
