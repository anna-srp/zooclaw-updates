---
title: "结账弹窗被拦截问题修复"
type: "Bug Fix"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 结账弹窗被拦截问题修复

## 核心宣传点
修复了订阅/充值结账时弹窗被浏览器拦截的问题，结账页面现在能稳定打开。

## 原始内容
```
fix(billing): pre-open checkout tabs across async flows (#2320)

## Summary

- Replaces old PR #1961 on latest `main`.
- Adds a fail-closed `openCheckoutPopup()` helper that pre-opens
checkout tabs synchronously, clears `opener`, verifies it stayed
cleared, and refuses to navigate unsafe popups.
- Preserves the old `noreferrer` privacy contract by navigating checkout
popups through a no-referrer redirect document instead of assigning the
external URL directly.
- Uses the helper in paywall checkout and billing subscription/top-up
checkout flows so async order creation does not lose browser user
activation.
- Adds production acceptance notes in
`docs/staging-validation/2026-06-10-billing-popup-checkout-validation.md`.

## Out of scope

- Customer portal and invoice download popup handling remain follow-up
work for the old #1965 scope.

## Validation

- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/lib/window-open.unit.spec.ts
tests/unit/components/PaywallContent.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx`
passed: 4 files, 91 tests.
- `pnpm --dir web run lint` passed with existing enterprise-app warnings
only.
- `pnpm --dir web/app exec tsc --noEmit` passed.
- `pnpm --dir web run tsc` did not reach TypeScript locally because
local pnpm 10.26.2 rejects the workspace script option `--if-present`.
- `pnpm --dir web/app run dev:staging` browser validation covered
`/new-chat`, `/chat`, desktop/mobile billing layouts, and popup-blocked
behavior through a temporary local-only billing harness that was not
committed.

---

### PR Description

## Summary

- Replaces old PR #1961 on latest `main`.
- Adds a fail-closed `openCheckoutPopup()` helper that pre-opens checkout tabs synchronously, clears `opener`, verifies it stayed cleared, and refuses to navigate unsafe popups.
- Preserves the old `noreferrer` privacy contract by navigating checkout popups through a no-referrer redirect document instead of assigning the external URL directly.
- Uses the helper in paywall checkout and billing subscription/top-up checkout flows so async order creation does not lose browser user activation.
- Adds production acceptance notes in `docs/staging-validation/2026-06-10-billing-popup-checkout-validation.md`.

## Out of scope

- Customer portal and invoice download popup handling remain follow-up work for the old #1965 scope.

## Validation

- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/lib/window-open.unit.spec.ts tests/unit/components/PaywallContent.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx` passed: 4 files, 91 tests.
- `pnpm --dir web run lint` passed with existing enterprise-app warnings only.
- `pnpm --dir web/app exec tsc --noEmit` passed.
- `pnpm --dir web run tsc` did not reach TypeScript locally because local pnpm 10.26.2 rejects the workspace script option `--if-present`.
- `pnpm --dir web/app run dev:staging` browser validation covered `/new-chat`, `/chat`, desktop/mobile billing layouts, and popup-blocked behavior through a temporary local-only billing harness that was not committed.

```
