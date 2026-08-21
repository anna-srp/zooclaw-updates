---
title: "信用卡充值切换到 Airwallex 通道，卡单问题一并修复"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-20"
status: "待审核"
channels: ""
---

# 信用卡充值切换到 Airwallex 通道，卡单问题一并修复

## 核心宣传点

信用卡一次性充值（1000 / 5000 / 10000 credits）整体迁移到 Airwallex 支付通道，同时修掉了迁移过程中暴露的两个卡单问题：充值页创建失败，以及支付成功后订单长期停在「处理中」、额度不到账。现在用卡充值可以一次走通。注意：Airwallex 没有客户自助账单门户，信用卡用户的「Edit billing / View billing」入口已随之下线。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `15ac660120fbbf26e53aa8c950638423b1d80a53`
- PR: #3449
- 作者: tim-srp
- 日期: 2026-08-20T02:34:12Z

### Commit Message

```
feat(billing): move card top-up checkout to Airwallex and remove Creem portal (#3449)

## Summary

Completes the card channel migration to Airwallex: one-time top-up
checkouts now run on Airwallex PAYMENT mode, and the Creem top-up stack
+ customer portal are removed (no Creem users exist).

Design spec:
`docs/superpowers/specs/2026-08-19-airwallex-topup-design.md`

## Changes

**Airwallex top-up stack (backend)**
- `AirwallexCreateCheckoutRequest.mode` widened to `SUBSCRIPTION |
PAYMENT`; PAYMENT rejects `subscription_data`
- `AirwallexCatalog.resolve_topup(credits)` + top-up config completeness
(`airwallex_topup_configuration_complete`) and availability gate
(`airwallex_topup_checkout_enabled`)
- New `airwallex/topup_payment.py`: settles a PAYMENT checkout against
its local order, grants TOPUP_CREDITS once via billing gateway
(idempotent entitlement replay), operation key
`airwallex:checkout:<id>:topup`
- `payment_events.py`: `payment_intent.succeeded` without a
`subscription_id` settles top-up orders instead of raising
`event_not_supported`
- `card_topup_checkout.py` rewritten as Airwallex-only (create PAYMENT
checkout, confirm via `get_billing_checkout` → settle; replay via
`is_official_airwallex_checkout_url`)
- `card_topup_checkout_repo.py` provider filters now `airwallex`;
capability `topup.card_available` driven by the Airwallex top-up gate

**Creem removal**
- Deleted `creem/topup_payment.py`, `creem/topup_loss.py`,
`creem/portal.py`; top-up branches in `creem/lifecycle.py`;
`resolve_topup`/top-up config in creem catalog/config;
`CREEM_PRODUCT_ID_TOPUP_*` settings; portal schemas and client surface
(`create_customer_billing_link` etc.)
- `POST /billing/creem-customer-portal` route removed; frontend
`createCreemCustomerPortal` + InvoiceHistory card-portal branch removed
(card users no longer see Edit billing / View billing — Airwallex has no
customer portal); mock-backend portal mock removed

**Frontend top-up flow unchanged** — contracts preserved: `{order_id,
checkout_url}` response, `?channel=card&local_order_id=...&type=topup`
success URL, confirm `status + entitlement_granted`, capability
`topup.card_available`.

## Not in this PR (follow-ups)

- **Refund/dispute revoke** (top-up loss) — deferred until the Airwallex
refund event shape is sandbox-verified
- **Sandbox verification of the PAYMENT-mode event shape** —
`payment_intent.succeeded` handling is reused from the subscription
channel; the top-up branch validates the retrieved checkout, so only
event-name/field extraction would change
- **Ops**: create the three one-time payment prices in the Airwallex
dashboard (sandbox + prod) and set
`AIRWALLEX_PRICE_ID_TOPUP_1000/5000/10000`
- Creem subscription/vertical-pack legacy teardown (separate work)

## Local checks

- `bash scripts/verify-py.sh` — passed (ruff, ruff-format, pyright,
import-linter)
- Backend targeted tests: billing/airwallex/creem/card/topup suites —
all passed
- Frontend: vitest 9009 passed, eslint passed, changed-file tsc clean
- Note: local full `tsc` and full pytest runs hit pre-existing
environment issues (stale `node_modules` codemirror resolution identical
to the main checkout; `test_stripe_billing_v2.py` segfaults at
collection in the main checkout too). CI's fresh install should be
clean.

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary

Completes the card channel migration to Airwallex: one-time top-up checkouts now run on Airwallex PAYMENT mode, and the Creem top-up stack + customer portal are removed (no Creem users exist).

Design spec: `docs/superpowers/specs/2026-08-19-airwallex-topup-design.md`

## Changes

**Airwallex top-up stack (backend)**
- `AirwallexCreateCheckoutRequest.mode` widened to `SUBSCRIPTION | PAYMENT`; PAYMENT rejects `subscription_data`
- `AirwallexCatalog.resolve_topup(credits)` + top-up config completeness (`airwallex_topup_configuration_complete`) and availability gate (`airwallex_topup_checkout_enabled`)
- New `airwallex/topup_payment.py`: settles a PAYMENT checkout against its local order, grants TOPUP_CREDITS once via billing gateway (idempotent entitlement replay), operation key `airwallex:checkout:<id>:topup`
- `payment_events.py`: `payment_intent.succeeded` without a `subscription_id` settles top-up orders instead of raising `event_not_supported`
- `card_topup_checkout.py` rewritten as Airwallex-only (create PAYMENT checkout, confirm via `get_billing_checkout` → settle; replay via `is_official_airwallex_checkout_url`)
- `card_topup_checkout_repo.py` provider filters now `airwallex`; capability `topup.card_available` driven by the Airwallex top-up gate

**Creem removal**
- Deleted `creem/topup_payment.py`, `creem/topup_loss.py`, `creem/portal.py`; top-up branches in `creem/lifecycle.py`; `resolve_topup`/top-up config in creem catalog/config; `CREEM_PRODUCT_ID_TOPUP_*` settings; portal schemas and client surface (`create_customer_billing_link` etc.)
- `POST /billing/creem-customer-portal` route removed; frontend `createCreemCustomerPortal` + InvoiceHistory card-portal branch removed (card users no longer see Edit billing / View billing — Airwallex has no customer portal); mock-backend portal mock removed

**Frontend top-up flow unchanged** — contracts preserved: `{order_id, checkout_url}` response, `?channel=card&local_order_id=...&type=topup` success URL, confirm `status + entitlement_granted`, capability `topup.card_available`.

## Not in this PR (follow-ups)

- **Refund/dispute revoke** (top-up loss) — deferred until the Airwallex refund event shape is sandbox-verified
- **Sandbox verification of the PAYMENT-mode event shape** — `payment_intent.succeeded` handling is reused from the subscription channel; the top-up branch validates the retrieved checkout, so only event-name/field extraction would change
- **Ops**: create the three one-time payment prices in the Airwallex dashboard (sandbox + prod) and set `AIRWALLEX_PRICE_ID_TOPUP_1000/5000/10000`
- Creem subscription/vertical-pack legacy teardown (separate work)

## Local checks

- `bash scripts/verify-py.sh` — passed (ruff, ruff-format, pyright, import-linter)
- Backend targeted tests: billing/airwallex/creem/card/topup suites — all passed
- Frontend: vitest 9009 passed, eslint passed, changed-file tsc clean
- Note: local full `tsc` and full pytest runs hit pre-existing environment issues (stale `node_modules` codemirror resolution identical to the main checkout; `test_stripe_billing_v2.py` segfaults at collection in the main checkout too). CI's fresh install should be clean.


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `c276c08a17a115c34fef00039fbdb4565166bad8`
- PR: #3452
- 作者: tim-srp
- 日期: 2026-08-20T04:05:15Z

### Commit Message

```
fix(billing): send invoice_data on Airwallex PAYMENT topup checkouts (#3452)

## Summary

Staging verification of #3449 found that Airwallex rejects PAYMENT-mode
`billing_checkouts/create` without `invoice_data`:

```json
{"code":"validation_error","message":"invoice_data must be provided for PAYMENT mode in checkout.","source":"invoice_data"}
```

This closes the [VERIFY sandbox] request-shape open item in the design
spec.

## Changes

- `app/schema/airwallex.py` — add `AirwallexInvoiceData`
(`days_until_due` / `default_tax_percent` / `due_at` / `memo` /
`metadata`, all optional per the [Airwallex Billing Checkouts
API](https://www.airwallex.com/docs/api/billing/billing_checkouts/retrieve#2));
`AirwallexCreateCheckoutRequest` gains `invoice_data` and the mode
validator now **requires** it for PAYMENT mode (alongside the existing
no-`subscription_data` rule)
- `app/services/billing_v2/card_topup_checkout.py` — top-up checkout
creation sends `invoice_data=AirwallexInvoiceData(days_until_due=0)`
(invoice due immediately on completion)
- Spec + tests updated (schema PAYMENT-mode rules, checkout request
assertion)

## Verification

- Empirical sandbox repro inside the staging pod: without `invoice_data`
→ 400 `validation_error`; with `invoice_data={days_until_due: 0}` →
**201**, `bco_...` checkout with hosted URL on
`checkout.sandbox.airwallex.com` (already in the official-host
allowlist)
- `pytest -k "airwallex or topup or card"` → 688 passed; `bash
scripts/verify-py.sh` → all checks passed

## Remaining open item

`payment_intent.succeeded` event shape for PAYMENT-mode checkouts (the
completion-event side) — verifiable end-to-end once this fix is on
staging and a real top-up payment is completed with a sandbox test card.
```

### PR Body

## Summary

Staging verification of #3449 found that Airwallex rejects PAYMENT-mode `billing_checkouts/create` without `invoice_data`:

```json
{"code":"validation_error","message":"invoice_data must be provided for PAYMENT mode in checkout.","source":"invoice_data"}
```

This closes the [VERIFY sandbox] request-shape open item in the design spec.

## Changes

- `app/schema/airwallex.py` — add `AirwallexInvoiceData` (`days_until_due` / `default_tax_percent` / `due_at` / `memo` / `metadata`, all optional per the [Airwallex Billing Checkouts API](https://www.airwallex.com/docs/api/billing/billing_checkouts/retrieve#2)); `AirwallexCreateCheckoutRequest` gains `invoice_data` and the mode validator now **requires** it for PAYMENT mode (alongside the existing no-`subscription_data` rule)
- `app/services/billing_v2/card_topup_checkout.py` — top-up checkout creation sends `invoice_data=AirwallexInvoiceData(days_until_due=0)` (invoice due immediately on completion)
- Spec + tests updated (schema PAYMENT-mode rules, checkout request assertion)

## Verification

- Empirical sandbox repro inside the staging pod: without `invoice_data` → 400 `validation_error`; with `invoice_data={days_until_due: 0}` → **201**, `bco_...` checkout with hosted URL on `checkout.sandbox.airwallex.com` (already in the official-host allowlist)
- `pytest -k "airwallex or topup or card"` → 688 passed; `bash scripts/verify-py.sh` → all checks passed

## Remaining open item

`payment_intent.succeeded` event shape for PAYMENT-mode checkouts (the completion-event side) — verifiable end-to-end once this fix is on staging and a real top-up payment is completed with a sandbox test card.


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `3b8e1eae308eec0e5a36192881100f1349f86e57`
- PR: #3453
- 作者: tim-srp
- 日期: 2026-08-20T04:23:08Z

### Commit Message

```
fix(billing): tolerate missing request_id on retrieved Airwallex topup checkouts (#3453)

## Summary

Staging end-to-end testing found completed top-up payments stuck in
`pending` with `billing.card_topup_checkout.order_conflict` on confirm.

**Root cause (sandbox-verified)**: Airwallex's checkout **retrieval**
endpoint omits `request_id` (creation responses carry it, retrievals
return `null`). Both `confirm_card_topup_order` and
`settle_airwallex_topup_checkout` required `checkout.request_id ==
local_order_id`, so every completed top-up was rejected with a conflict
— via the success-page confirm poll and via the webhook settlement path
alike.

## Changes

- Tolerate a missing `request_id` on retrieved checkouts in both
validation sites; only a present-but-mismatched value is rejected.
Ownership authority stays with the metadata `uid`/`local_order_id`
binding (still strictly validated).
- Tests: confirm settles when the retrieved checkout omits `request_id`;
settlement likewise accepts it; existing present-mismatch conflict cases
unchanged.

## Evidence

- Staging order `ORD-20260820-AE2C9987` (status `pending`) → retrieved
checkout: `request_id: null`, all other identity fields match → conflict
reproduced from logs.
- Local: 46 targeted tests pass; `verify-py` green.

## Note

A separate staging issue (all Airwallex webhook deliveries rejected with
`invalid_payload` — signature verifies, envelope parse fails) is under
investigation in parallel and is not fixed by this PR.
```

### PR Body

## Summary

Staging end-to-end testing found completed top-up payments stuck in `pending` with `billing.card_topup_checkout.order_conflict` on confirm.

**Root cause (sandbox-verified)**: Airwallex's checkout **retrieval** endpoint omits `request_id` (creation responses carry it, retrievals return `null`). Both `confirm_card_topup_order` and `settle_airwallex_topup_checkout` required `checkout.request_id == local_order_id`, so every completed top-up was rejected with a conflict — via the success-page confirm poll and via the webhook settlement path alike.

## Changes

- Tolerate a missing `request_id` on retrieved checkouts in both validation sites; only a present-but-mismatched value is rejected. Ownership authority stays with the metadata `uid`/`local_order_id` binding (still strictly validated).
- Tests: confirm settles when the retrieved checkout omits `request_id`; settlement likewise accepts it; existing present-mismatch conflict cases unchanged.

## Evidence

- Staging order `ORD-20260820-AE2C9987` (status `pending`) → retrieved checkout: `request_id: null`, all other identity fields match → conflict reproduced from logs.
- Local: 46 targeted tests pass; `verify-py` green.

## Note

A separate staging issue (all Airwallex webhook deliveries rejected with `invalid_payload` — signature verifies, envelope parse fails) is under investigation in parallel and is not fixed by this PR.


