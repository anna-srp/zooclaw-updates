---
title: "餐饮 AI 团队套餐支持信用卡下单"
type: "新功能上线"
priority: "中"
date: "2026-08-13"
status: "待审核"
channels: ""
---

## 核心宣传点

Restaurant AI Agent Team 套餐（$299/月、20,000 额度）现在可以直接用信用卡下单，支付、续费、逾期与退订状态都会自动同步到企业权益。

## 原始内容

仓库：SerendipityOneInc/ecap-workspace
commit：ffc555410b240fb0484c906ee769f5d84d195bdc
作者：tim-srp
日期：2026-08-13T11:44:29Z

**Commit message**

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

**PR #3359 body**

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


