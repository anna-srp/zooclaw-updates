---
title: "信用卡免费试用改由 Creem 承接，不再预扣 1 美元"
type: "体验优化"
priority: "中"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 信用卡免费试用改由 Creem 承接，不再预扣 1 美元

## 核心宣传点

Starter 信用卡免费试用改走 Creem 托管结算，提供 7 天官方试用期，取消原先的 1 美元验证扣款；支付宝试用流程不变。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `13a0e7d93123b6f338fa76af2390b0ca29829d55`
- PR: #3318

### Commit Message

```
feat(billing): move Card free trials to Creem (#3318)

## Linear

N/A

## Summary

- Route eligible Starter Card free trials through Creem Test Mode hosted
checkout with provider-managed 7-day trials and no $1 authorization.
- Keep the existing Alipay free-trial flow unchanged and hard-disable
the removed Stripe trial-authorization path.
- Project authenticated Creem trialing webhooks into Billing v2, support
cancellation, and reconcile Creem subscription state through the
existing hourly maintenance job.
- Add Test Mode trial product configuration, server-side eligibility and
product selection, typed webhook schemas, frontend trial
capability/copy, and comprehensive regression tests.

## Test plan

- [x] Backend targeted suite: 576 passed.
- [x] Creem lifecycle/checkout suite: 84 passed.
- [x] Frontend verification: TypeScript, governance checks, ESLint, and
359 unit tests passed (1 skipped).
- [x] Post-merge changed-surface gate: frontend checks, Ruff, Ruff
format, and import-linter passed.
- [ ] CI Pyright (local host selected Miniconda Pyright without project
dependencies, producing missing-import errors; commit checks and
targeted behavior tests passed).
- [x] Confirmed both Creem Test Mode Trial Product IDs are synchronized
from Vault into the staging Kubernetes Secret.

## Operational notes

- Trial products were created only in Creem Test Mode.
- Staging Vault contains `CREEM_PRODUCT_ID_STARTER_MONTHLY_TRIAL` and
`CREEM_PRODUCT_ID_STARTER_YEARLY_TRIAL`.
- Production configuration was not modified.
```

### PR Body

## Linear

N/A

## Summary

- Route eligible Starter Card free trials through Creem Test Mode hosted checkout with provider-managed 7-day trials and no $1 authorization.
- Keep the existing Alipay free-trial flow unchanged and hard-disable the removed Stripe trial-authorization path.
- Project authenticated Creem trialing webhooks into Billing v2, support cancellation, and reconcile Creem subscription state through the existing hourly maintenance job.
- Add Test Mode trial product configuration, server-side eligibility and product selection, typed webhook schemas, frontend trial capability/copy, and comprehensive regression tests.

## Test plan

- [x] Backend targeted suite: 576 passed.
- [x] Creem lifecycle/checkout suite: 84 passed.
- [x] Frontend verification: TypeScript, governance checks, ESLint, and 359 unit tests passed (1 skipped).
- [x] Post-merge changed-surface gate: frontend checks, Ruff, Ruff format, and import-linter passed.
- [ ] CI Pyright (local host selected Miniconda Pyright without project dependencies, producing missing-import errors; commit checks and targeted behavior tests passed).
- [x] Confirmed both Creem Test Mode Trial Product IDs are synchronized from Vault into the staging Kubernetes Secret.

## Operational notes

- Trial products were created only in Creem Test Mode.
- Staging Vault contains `CREEM_PRODUCT_ID_STARTER_MONTHLY_TRIAL` and `CREEM_PRODUCT_ID_STARTER_YEARLY_TRIAL`.
- Production configuration was not modified.

