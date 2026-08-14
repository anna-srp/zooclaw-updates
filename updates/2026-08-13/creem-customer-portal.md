---
title: "信用卡用户可自助管理支付方式和账单记录"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-13"
status: "待审核"
channels: ""
---

## 核心宣传点

用信用卡付费的用户现在能在账单页进入自助门户，自己更换银行卡、查看历史账单和发票，不用再联系客服。

## 原始内容

仓库：SerendipityOneInc/ecap-workspace
commit：9422d78324d18d454226533c00673cc34d7d30c5
作者：tim-srp
日期：2026-08-13T09:24:25Z

**Commit message**

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

**PR #3364 body**

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


