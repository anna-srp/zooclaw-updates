---
title: "修复续费订单历史与发票下载"
type: "Bug Fix"
priority: "高"
date: "2026-06-09"
status: "待审核"
channels: ""
---

# 修复续费订单历史与发票下载

## 核心宣传点

续费后能正确看到每一笔订单并下载对应发票，第二次扣款不再被旧订单覆盖隐藏。

## 原始内容

完整 commit message：

```
fix(billing): preserve renewal history and retry bg idempotency (#2291)

## Summary
- Fix Stripe renewal invoice handling so renewal `invoice.paid` events
create distinct Billing v2 payment orders instead of overwriting the
original checkout order.
- Make invoice download V2-only by reading Billing v2 payment orders
only, with support for provider-created renewal rows addressed by
`payment_order_id`.
- Retry only Billing Gateway's explicit in-progress idempotency `409`
response for `subscribe()` / `topup_wallet()` instead of surfacing
transient webhook 500s.
- Include the PR workflow skill update requested in this branch.

Linear:
https://linear.app/srpone/issue/ECA-928/fix-stripe-renewal-order-history

## Root cause
Stripe renewal invoices can carry the original checkout metadata
`order_id`. The previous `invoice.paid` resolver used that metadata for
renewal invoices too, so the June renewal updated the May checkout
payment order and hid the second payment from the order list / invoice
download flow.

Separately, concurrent webhook fulfillment can send the same BG
`transaction_id` while another worker is still processing it. BG
correctly returns `409 duplicate request still in progress`, but
claw-interface treated that as a terminal HTTP error and returned
webhook 500.

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff format --check .`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check .`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_client.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_invoice_lookup.py tests/unit/test_stripe_billing_v2.py
tests/unit/test_orders_endpoints.py -q` (156 passed)
- [ ] `cd services/claw-interface && pyright app tests` currently fails
in the local devcontainer because installed `favie-common v0.3.62` lacks
`favie_common.logging` and `favie_common.middleware.request_context`;
this is unrelated to the changed files and is expected to be covered by
CI's pinned environment.
```

PR 描述：

## Summary
- Fix Stripe renewal invoice handling so renewal `invoice.paid` events create distinct Billing v2 payment orders instead of overwriting the original checkout order.
- Make invoice download V2-only by reading Billing v2 payment orders only, with support for provider-created renewal rows addressed by `payment_order_id`.
- Retry only Billing Gateway's explicit in-progress idempotency `409` response for `subscribe()` / `topup_wallet()` instead of surfacing transient webhook 500s.
- Include the PR workflow skill update requested in this branch.

Linear: https://linear.app/srpone/issue/ECA-928/fix-stripe-renewal-order-history

## Root cause
Stripe renewal invoices can carry the original checkout metadata `order_id`. The previous `invoice.paid` resolver used that metadata for renewal invoices too, so the June renewal updated the May checkout payment order and hid the second payment from the order list / invoice download flow.

Separately, concurrent webhook fulfillment can send the same BG `transaction_id` while another worker is still processing it. BG correctly returns `409 duplicate request still in progress`, but claw-interface treated that as a terminal HTTP error and returned webhook 500.

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff format --check .`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check .`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_client.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_invoice_lookup.py tests/unit/test_stripe_billing_v2.py tests/unit/test_orders_endpoints.py -q` (156 passed)
- [ ] `cd services/claw-interface && pyright app tests` currently fails in the local devcontainer because installed `favie-common v0.3.62` lacks `favie_common.logging` and `favie_common.middleware.request_context`; this is unrelated to the changed files and is expected to be covered by CI's pinned environment.

