---
title: "修复：新用户首次订阅 Starter 试用被误判「上一笔支付审核中」"
type: "Bug Fix"
priority: "高"
date: "2026-08-18"
status: "待审核"
channels: ""
---

# 修复：新用户首次订阅 Starter 试用被误判「上一笔支付审核中」

## 核心宣传点

新用户点「Try Starter for free」时，会被错误提示「上一笔卡支付仍在审核中」而无法下单，且重试永远卡住。现已修复，新用户首次订阅可一次成功。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `4371cce5ce365b3887c0589fb942a19b14e5f026`
- PR: #3420
- 作者: tim-srp
- 日期: 2026-08-18T17:40:34Z

### Commit Message

```
fix(billing): scope Card checkout provider CAS to the active provider (#3420)

## Summary

Fixes a staging bug where a brand-new user clicking "Try Starter for
free" was rejected with `billing.card_checkout.outcome_unresolved` ("A
previous Card checkout is still being reviewed") on their **first**
attempt.

The Airwallex switch (#3419) updated the checkout orchestration to
create orders with `provider=airwallex`, but the persistence layer still
hard-coded `provider=creem` in the provider-create CAS, checkout
attachment, and manual-review/fail markers. A new user's first trial
checkout therefore failed its provider claim against its own Airwallex
order, returned unresolved, and every retry hit the same unresolved
checkout.

## Root cause

- `claim_provider_request` (provider Create CAS) filtered on
`provider=creem`, so an Airwallex order never matched → claim returned
`False` → `_unresolved_error()` raised. First attempt fails immediately.
- `attach_checkout` / `mark_manual_review` / `mark_failed` had the same
`provider=creem` filter, so a successful Create could not attach, and
failures could not be marked correctly.
- Because the failed order stayed `pending` with
`provider_checkout_requested_at` set, every retry hit
`find_unresolved_subscription` (which correctly passes
`provider=airwallex`) and was permanently stuck.

## Change

- **repo layer** (`card_checkout_order_repo.py`): thread `provider`
(default `"creem"`) through `claim_provider_request`, `attach_checkout`,
`mark_manual_review`, `mark_failed`. Legacy Creem paths keep their exact
previous behavior.
- **wrapper layer** (`card_checkout_orders.py`):
`claim_card_checkout_request` accepts a `provider`;
`attach_card_checkout` and the status marker helper read the provider
from the persisted order.
- **callers**: Airwallex checkout flows (`card_checkout.py`,
`airwallex_upgrade_checkout.py`) pass `BillingProvider.AIRWALLEX`; the
Creem enterprise path keeps the default.

## Tests

- 625 card/airwallex/creem-related unit tests pass, including new repo
regression tests asserting the provider-scoped CAS filters.
- ruff + pyright clean.

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

```
## Summary

Fixes a staging bug where a brand-new user clicking "Try Starter for free" was rejected with `billing.card_checkout.outcome_unresolved` ("A previous Card checkout is still being reviewed") on their **first** attempt.

The Airwallex switch (#3419) updated the checkout orchestration to create orders with `provider=airwallex`, but the persistence layer still hard-coded `provider=creem` in the provider-create CAS, checkout attachment, and manual-review/fail markers. A new user's first trial checkout therefore failed its provider claim against its own Airwallex order, returned unresolved, and every retry hit the same unresolved checkout.

## Root cause

- `claim_provider_request` (provider Create CAS) filtered on `provider=creem`, so an Airwallex order never matched → claim returned `False` → `_unresolved_error()` raised. First attempt fails immediately.
- `attach_checkout` / `mark_manual_review` / `mark_failed` had the same `provider=creem` filter, so a successful Create could not attach, and failures could not be marked correctly.
- Because the failed order stayed `pending` with `provider_checkout_requested_at` set, every retry hit `find_unresolved_subscription` (which correctly passes `provider=airwallex`) and was permanently stuck.

## Change

- **repo layer** (`card_checkout_order_repo.py`): thread `provider` (default `"creem"`) through `claim_provider_request`, `attach_checkout`, `mark_manual_review`, `mark_failed`. Legacy Creem paths keep their exact previous behavior.
- **wrapper layer** (`card_checkout_orders.py`): `claim_card_checkout_request` accepts a `provider`; `attach_card_checkout` and the status marker helper read the provider from the persisted order.
- **callers**: Airwallex checkout flows (`card_checkout.py`, `airwallex_upgrade_checkout.py`) pass `BillingProvider.AIRWALLEX`; the Creem enterprise path keeps the default.

## Tests

- 625 card/airwallex/creem-related unit tests pass, including new repo regression tests asserting the provider-scoped CAS filters.
- ruff + pyright clean.

```
