---
title: "修复：部分信用卡订单长期卡在处理中／人工审核，导致无法重新下单"
type: "Bug Fix"
priority: "高"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# 修复：部分信用卡订单长期卡在处理中／人工审核，导致无法重新下单

## 核心宣传点

少数历史信用卡订单会一直停在「处理中」或被锁进人工审核，账号因此无法再发起新的信用卡结算；现在这些订单会自动收敛到明确结果并释放占用，用户可以正常重新下单。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e82846e20dea8e59ea3fd4367204b34d0a53170d`
- PR: #3345

### Commit Message

```
fix(billing): recover stale Creem checkout reconciliation (#3345)

## Summary

- Accept authoritative Creem Checkout reads whose `order` object omits
`customer`: retrieval now uses a dedicated `CreemRetrievedOrder`
projection with an optional customer, and `completed_object()` backfills
`order.customer` from the top-level checkout customer so every existing
binding cross-check stays exact. The webhook schema (`CreemWebhookOrder`
in `checkout.completed` payloads) remains strict.
- Converge bound pending Card orders whose provider subscription is
terminally `canceled`/`expired` instead of raising `Bound Creem checkout
is not recoverable` on every hourly run: orders with no provider payment
are marked `failed` (`provider_subscription_canceled`) and the account
checkout lease is released; orders where the provider collected a
payment fail closed into sticky `manual_review`
(`provider_subscription_canceled_after_payment`).
- The retrieval models (`CreemRetrievedCheckout` + new
`CreemRetrievedOrder`) move to `app/schema/creem_retrieval.py` because
the addition pushed `app/schema/creem.py` past the 500-line CI guard;
the webhook schemas in `creem.py` are unchanged.

## Root cause

Staging's hourly `check-subscription-sync` reconciliation has been
failing on the same three historical records every run:

- Two unbound checkouts (`ch_x8ysu5Hs7wCAkXIxMln6E`,
`ch_5Pk8KZ7SQeGATYLvQ7Zv9M`) fail during `client.get_checkout()` with
`ValidationError: order.customer Field required` — Creem's `GET
/v1/checkouts` response genuinely omits `order.customer` for these
historical orders, while `CreemRetrievedCheckout` reused the strict
webhook order model.
- One bound pending order (`sub_6MehYopz16rL68tmOr15GR`) reaches
`project_bound_pending_order`, which only handled `trialing`/`active`
subscriptions, so a canceled subscription raised unconditionally with no
terminal transition and no retry backoff (the bound loop retries every
hour forever).

Besides the log noise (`failed >= 3` every run), the affected uids stay
permanently "unresolved" in `find_unresolved_subscription`, blocking
those accounts from ever starting a new Card checkout.

## Test plan

- [x] New unit tests: retrieved checkout without `order.customer` parses
and its completed projection backfills the customer; completed
projection still fails loudly when no customer identity exists at all.
- [x] New unit tests: canceled unpaid subscription → order failed +
checkout lease released; canceled subscription with a provider
transaction → sticky manual review, no release; unknown provider status
still raises; subscription identity / environment-mode mismatches are
rejected.
- [x] New repo CAS tests pin the exact filters for
`mark_bound_checkout_canceled` / `mark_bound_checkout_manual_review`.
- [x] Local focused regression: creem suite 738 passed; billing/checkout
suite 1407 passed, 5 skipped.
- [x] `ruff check` + `ruff format --check` + import-linter (8 contracts
kept) passed locally; local pyright reports only pre-existing
environment errors (missing `favie_common`/`stripe` in the host
interpreter — identical error set on a clean baseline); CI Pyright is
authoritative.
- [ ] CI Code Quality Check.
- [ ] Staging: next hourly `check-subscription-sync` run converges the
three historical records and the recurring WARNING tracebacks stop.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Summary

- Accept authoritative Creem Checkout reads whose `order` object omits `customer`: retrieval now uses a dedicated `CreemRetrievedOrder` projection with an optional customer, and `completed_object()` backfills `order.customer` from the top-level checkout customer so every existing binding cross-check stays exact. The webhook schema (`CreemWebhookOrder` in `checkout.completed` payloads) remains strict.
- Converge bound pending Card orders whose provider subscription is terminally `canceled`/`expired` instead of raising `Bound Creem checkout is not recoverable` on every hourly run: orders with no provider payment are marked `failed` (`provider_subscription_canceled`) and the account checkout lease is released; orders where the provider collected a payment fail closed into sticky `manual_review` (`provider_subscription_canceled_after_payment`).
- The retrieval models (`CreemRetrievedCheckout` + new `CreemRetrievedOrder`) move to `app/schema/creem_retrieval.py` because the addition pushed `app/schema/creem.py` past the 500-line CI guard; the webhook schemas in `creem.py` are unchanged.

## Root cause

Staging's hourly `check-subscription-sync` reconciliation has been failing on the same three historical records every run:

- Two unbound checkouts (`ch_x8ysu5Hs7wCAkXIxMln6E`, `ch_5Pk8KZ7SQeGATYLvQ7Zv9M`) fail during `client.get_checkout()` with `ValidationError: order.customer Field required` — Creem's `GET /v1/checkouts` response genuinely omits `order.customer` for these historical orders, while `CreemRetrievedCheckout` reused the strict webhook order model.
- One bound pending order (`sub_6MehYopz16rL68tmOr15GR`) reaches `project_bound_pending_order`, which only handled `trialing`/`active` subscriptions, so a canceled subscription raised unconditionally with no terminal transition and no retry backoff (the bound loop retries every hour forever).

Besides the log noise (`failed >= 3` every run), the affected uids stay permanently "unresolved" in `find_unresolved_subscription`, blocking those accounts from ever starting a new Card checkout.

## Test plan

- [x] New unit tests: retrieved checkout without `order.customer` parses and its completed projection backfills the customer; completed projection still fails loudly when no customer identity exists at all.
- [x] New unit tests: canceled unpaid subscription → order failed + checkout lease released; canceled subscription with a provider transaction → sticky manual review, no release; unknown provider status still raises; subscription identity / environment-mode mismatches are rejected.
- [x] New repo CAS tests pin the exact filters for `mark_bound_checkout_canceled` / `mark_bound_checkout_manual_review`.
- [x] Local focused regression: creem suite 738 passed; billing/checkout suite 1407 passed, 5 skipped.
- [x] `ruff check` + `ruff format --check` + import-linter (8 contracts kept) passed locally; local pyright reports only pre-existing environment errors (missing `favie_common`/`stripe` in the host interpreter — identical error set on a clean baseline); CI Pyright is authoritative.
- [ ] CI Code Quality Check.
- [ ] Staging: next hourly `check-subscription-sync` run converges the three historical records and the recurring WARNING tracebacks stop.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `1fd5620ee68aad34c4268247ece711d7ce9799bb`
- PR: #3353

### Commit Message

```
fix(billing): converge null Creem terminal trial orders (#3353)

## Summary
- allow terminal Creem Trial reconciliation to treat a missing or
explicit-null provider transaction ID as unsettled
- fail closed when the terminal order CAS misses, while accepting an
exact concurrent terminal replay
- add focused regression coverage for both historical storage shapes and
CAS convergence outcomes

## Root cause
Historical Card Trial orders can store `provider_transaction_id` as an
explicit null. The terminal reconciliation CAS only accepted a missing
field, so it left those orders pending. The service also treated every
CAS miss as success, which let the cron count an unchanged order as
processed and retain its checkout lease.

## Test plan
- [x] `PYTHONPATH=services/claw-interface pytest
services/claw-interface/tests/unit/test_billing_v2_repos.py
services/claw-interface/tests/unit/test_creem_reconciliation.py -q`
(`132 passed`)
- [x] commit hooks: Ruff, Ruff format, dependency checks, complexity
checks, import contracts, repository contracts, and Pyright
- [x] changed-file Pyright with the local Conda interpreter (`0 errors`)
- [x] PR size gate (`112 / 3000` business/test lines)
- [ ] GitHub Actions in the complete CI environment
- [ ] controlled staging reconciliation for the verified historical
explicit-null order shape after deployment

## Local environment note
The standalone `verify-py.sh` invocation in this new worktree selected a
global Pyright process without the project dependency search path. Ruff,
format, and import-linter passed; explicit changed-file Pyright and the
repository's commit-hook Pyright passed. GitHub Actions remains the
authoritative full-environment type check.
```

### PR Body

## Summary
- allow terminal Creem Trial reconciliation to treat a missing or explicit-null provider transaction ID as unsettled
- fail closed when the terminal order CAS misses, while accepting an exact concurrent terminal replay
- add focused regression coverage for both historical storage shapes and CAS convergence outcomes

## Root cause
Historical Card Trial orders can store `provider_transaction_id` as an explicit null. The terminal reconciliation CAS only accepted a missing field, so it left those orders pending. The service also treated every CAS miss as success, which let the cron count an unchanged order as processed and retain its checkout lease.

## Test plan
- [x] `PYTHONPATH=services/claw-interface pytest services/claw-interface/tests/unit/test_billing_v2_repos.py services/claw-interface/tests/unit/test_creem_reconciliation.py -q` (`132 passed`)
- [x] commit hooks: Ruff, Ruff format, dependency checks, complexity checks, import contracts, repository contracts, and Pyright
- [x] changed-file Pyright with the local Conda interpreter (`0 errors`)
- [x] PR size gate (`112 / 3000` business/test lines)
- [ ] GitHub Actions in the complete CI environment
- [ ] controlled staging reconciliation for the verified historical explicit-null order shape after deployment

## Local environment note
The standalone `verify-py.sh` invocation in this new worktree selected a global Pyright process without the project dependency search path. Ruff, format, and import-linter passed; explicit changed-file Pyright and the repository's commit-hook Pyright passed. GitHub Actions remains the authoritative full-environment type check.


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `238a4957e7f141cbc151c692ab38a556fb883376`
- PR: #3352

### Commit Message

```
fix(billing): converge unpaid terminal Creem trials (#3352)

## Summary

- Stop routing terminated `$0` Trial subscriptions into `manual_review`:
before failing closed, terminal settlement now reads the authoritative
transaction (`client.get_transaction`) and only holds the order for
operator review when `amount_paid > 0`. A `$0` Trial invoice converges
as an unpaid termination (`failed`/`expired` + checkout release), so the
user is unblocked instead of stuck behind a sticky review lock. The
transaction is cross-checked against the subscription identity and
environment mode before it is trusted.
- Let legacy expired Checkouts converge: the unbound-checkout identity
gate no longer requires `payment_order_id == local_order_id` (a
newer-flow invariant that legacy orders predate). It still requires the
exact checkout session id, environment mode, `request_id ==
local_order_id`, and signed-metadata uid/order matches; all repo writes
remain keyed by exact `payment_order_id` CAS filters, so the relaxation
removes no safety.

## Root cause

Both gaps were left by #3345/#3348 and confirmed against latest `main`:

1. `settle_terminal_bound_order` used `last_transaction_id` presence as
the "provider collected money" signal. Creem issues a `$0` invoice
transaction at Trial start (`CreemTransaction.amount_paid` is
`NonNegativeInt`, and the Trial's first webhook is `subscription.paid`
with status `trialing`), so a canceled unpaid Trial also carries a
transaction id and was misrouted to `manual_review` with reason
`..._after_payment` — wrong customer-facing state, wrong operator alert,
and the user is blocked from checking out again.
2. `_unbound_checkout_matches_order` required `checkout.request_id ==
local_order_id == payment_order_id`. Legacy orders where the two local
ids differ failed this identity check before the expired branch could
run, so an expired legacy Checkout retried forever and
`create_card_checkout` kept replaying its dead checkout URL for that
user.

## Test plan

- [x] TDD: `$0` transaction (`amount_paid=0`) on a canceled/expired
subscription → `mark_bound_checkout_terminal` + checkout release, no
manual review.
- [x] `amount_paid > 0` still fails closed into manual review with the
existing terminal-status reason codes (both `canceled` and `expired`).
- [x] Transaction/subscription identity or environment-mode mismatch is
rejected; missing reconciliation client is rejected.
- [x] Legacy order with `payment_order_id != local_order_id` + expired
Checkout → marked expired against its exact `payment_order_id` and the
checkout lease released.
- [x] Backend regression: creem suite 751 passed; billing/checkout suite
1417 passed, 5 skipped.
- [x] `ruff check` + `ruff format --check` clean on changed files.
- [ ] CI Code Quality Check.
- [ ] Staging: hourly `check-subscription-sync` converges the remaining
stale records without new `manual_review` entries for unpaid Trials.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Summary

- Stop routing terminated `$0` Trial subscriptions into `manual_review`: before failing closed, terminal settlement now reads the authoritative transaction (`client.get_transaction`) and only holds the order for operator review when `amount_paid > 0`. A `$0` Trial invoice converges as an unpaid termination (`failed`/`expired` + checkout release), so the user is unblocked instead of stuck behind a sticky review lock. The transaction is cross-checked against the subscription identity and environment mode before it is trusted.
- Let legacy expired Checkouts converge: the unbound-checkout identity gate no longer requires `payment_order_id == local_order_id` (a newer-flow invariant that legacy orders predate). It still requires the exact checkout session id, environment mode, `request_id == local_order_id`, and signed-metadata uid/order matches; all repo writes remain keyed by exact `payment_order_id` CAS filters, so the relaxation removes no safety.

## Root cause

Both gaps were left by #3345/#3348 and confirmed against latest `main`:

1. `settle_terminal_bound_order` used `last_transaction_id` presence as the "provider collected money" signal. Creem issues a `$0` invoice transaction at Trial start (`CreemTransaction.amount_paid` is `NonNegativeInt`, and the Trial's first webhook is `subscription.paid` with status `trialing`), so a canceled unpaid Trial also carries a transaction id and was misrouted to `manual_review` with reason `..._after_payment` — wrong customer-facing state, wrong operator alert, and the user is blocked from checking out again.
2. `_unbound_checkout_matches_order` required `checkout.request_id == local_order_id == payment_order_id`. Legacy orders where the two local ids differ failed this identity check before the expired branch could run, so an expired legacy Checkout retried forever and `create_card_checkout` kept replaying its dead checkout URL for that user.

## Test plan

- [x] TDD: `$0` transaction (`amount_paid=0`) on a canceled/expired subscription → `mark_bound_checkout_terminal` + checkout release, no manual review.
- [x] `amount_paid > 0` still fails closed into manual review with the existing terminal-status reason codes (both `canceled` and `expired`).
- [x] Transaction/subscription identity or environment-mode mismatch is rejected; missing reconciliation client is rejected.
- [x] Legacy order with `payment_order_id != local_order_id` + expired Checkout → marked expired against its exact `payment_order_id` and the checkout lease released.
- [x] Backend regression: creem suite 751 passed; billing/checkout suite 1417 passed, 5 skipped.
- [x] `ruff check` + `ruff format --check` clean on changed files.
- [ ] CI Code Quality Check.
- [ ] Staging: hourly `check-subscription-sync` converges the remaining stale records without new `manual_review` entries for unpaid Trials.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
