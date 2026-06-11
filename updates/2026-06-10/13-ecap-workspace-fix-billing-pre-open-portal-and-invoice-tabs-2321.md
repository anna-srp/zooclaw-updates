---
title: "账单门户与发票弹窗修复"
type: "Bug Fix"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 账单门户与发票弹窗修复

## 核心宣传点
修复了客户账单门户和发票下载时弹窗被拦截的问题，账单管理和发票下载现在能正常打开。

## 原始内容
```
fix(billing): pre-open portal and invoice tabs (#2321)

## Summary

- Replaces old PR #1965 on top of the latest `main`.
- Adds a fail-closed `openCheckoutPopup` path for hosted billing
redirects: the tab is opened synchronously, `window.opener` is cleared
before navigation, and redirects use a `no-referrer` document.
- Migrates `InvoiceHistory` customer portal, `InvoiceHistory` invoice
download, and `SubscriptionPanel` customer portal to the pre-opened
popup flow.
- Adds regression coverage for popup-blocked, opener-clearing failure,
redirect document failure, and successful no-referrer navigation.
- Adds an acceptance guide:
`docs/staging-validation/2026-06-10-billing-portal-popup-validation.md`.

## Out of scope

- Checkout/top-up flows from old PR #1961 are handled separately by PR
#2320.
- Non-Stripe billing channels keep their existing informational behavior
and do not pre-open a popup.

## Validation

- `pnpm --dir web install --config.minimumReleaseAge=0`
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/lib/window-open.unit.spec.ts
tests/unit/components/billing/InvoiceHistory.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx`
  - Passed: 3 files, 86 tests.
- `pnpm --dir web run lint`
  - Passed with existing enterprise app warnings only.
- `pnpm --dir web/app exec tsc --noEmit`
  - Passed.
- `pnpm --dir web run tsc`
- Not completed locally: the local pnpm script failed before TypeScript
with `Unknown option: 'if-present'`. CI remains the source of truth for
the workspace script.
- Local `dev:staging` browser validation through Chrome CDP:
- Desktop and mobile billing popup harness rendered without positive
horizontal overflow.
- `InvoiceHistory` payment-method portal, invoice download, and
`SubscriptionPanel` portal all showed the blocked-popup toast
immediately when popups were blocked.
  - Buttons returned to enabled state after blocked-popup handling.
  - Both `/new-chat` and `/chat` loaded in the same local run.

---

### PR Description

## Summary

- Replaces old PR #1965 on top of the latest `main`.
- Adds a fail-closed `openCheckoutPopup` path for hosted billing redirects: the tab is opened synchronously, `window.opener` is cleared before navigation, and redirects use a `no-referrer` document.
- Migrates `InvoiceHistory` customer portal, `InvoiceHistory` invoice download, and `SubscriptionPanel` customer portal to the pre-opened popup flow.
- Adds regression coverage for popup-blocked, opener-clearing failure, redirect document failure, and successful no-referrer navigation.
- Adds an acceptance guide: `docs/staging-validation/2026-06-10-billing-portal-popup-validation.md`.

## Out of scope

- Checkout/top-up flows from old PR #1961 are handled separately by PR #2320.
- Non-Stripe billing channels keep their existing informational behavior and do not pre-open a popup.

## Validation

- `pnpm --dir web install --config.minimumReleaseAge=0`
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/lib/window-open.unit.spec.ts tests/unit/components/billing/InvoiceHistory.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx`
  - Passed: 3 files, 86 tests.
- `pnpm --dir web run lint`
  - Passed with existing enterprise app warnings only.
- `pnpm --dir web/app exec tsc --noEmit`
  - Passed.
- `pnpm --dir web run tsc`
  - Not completed locally: the local pnpm script failed before TypeScript with `Unknown option: 'if-present'`. CI remains the source of truth for the workspace script.
- Local `dev:staging` browser validation through Chrome CDP:
  - Desktop and mobile billing popup harness rendered without positive horizontal overflow.
  - `InvoiceHistory` payment-method portal, invoice download, and `SubscriptionPanel` portal all showed the blocked-popup toast immediately when popups were blocked.
  - Buttons returned to enabled state after blocked-popup handling.
  - Both `/new-chat` and `/chat` loaded in the same local run.

```
