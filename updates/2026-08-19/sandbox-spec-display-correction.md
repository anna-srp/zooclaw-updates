---
title: "定价页与账户用量页的沙箱配置更正为真实规格"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-19"
status: "待审核"
channels: ""
---

# 定价页与账户用量页的沙箱配置更正为真实规格

## 核心宣传点

定价对比表和订阅套餐卡的 CPU/内存改为与当前沙箱实际规格一致：Starter 2 核 2GB、Pro 4 核 4GB、Ultra 8 核 8GB（各语言版本同步更新）；账户用量页在产品尚未提供存储权益前先隐藏「存储」一项，避免展示误导性数字。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `ac6581ec012be6d16854c59832b5bb09f424efca`
- PR: #3427
- 作者: kaka-srp
- 日期: 2026-08-19T07:10:57Z

### Commit Message

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

### PR Body

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


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `9b9801ede7a7af1bd2a3d5526edb6bef5a8f99f5`
- PR: #3426
- 作者: kaka-srp
- 日期: 2026-08-19T06:50:19Z

### Commit Message

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

### PR Body

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

