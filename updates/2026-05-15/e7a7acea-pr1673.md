---
title: "accept order.is_trial as local truth for checkout trial escape"
type: "Bug Fix"
priority: "中"
date: "2026-05-15"
status: "待审核"
channels: ""
repo: "SerendipityOneInc/ecap-workspace"
sha: "e7a7aceaf5bf9cd9179b6e2cb2ef3318e821918d"
---

# accept order.is_trial as local truth for checkout trial escape

## 核心宣传点

修复问题：accept order.is_trial as local truth for checkout trial escape

## 原始内容

**Commit**: `e7a7aceaf5bf9cd9179b6e2cb2ef3318e821918d`
**Author**: kaka-srp
**Date**: 2026-05-15T10:57:39Z
**PR**: #1673 — https://github.com/SerendipityOneInc/ecap-workspace/pull/1673

### Commit Message

```
fix(stripe): accept order.is_trial as local truth for checkout trial escape (#1673)

## Summary

Phase 1 (ECA-681, #1629) added Stripe checkout session validation that
rejects any session whose `amount_total` does not match `order.amount`.
The trial escape was keyed on `payment_status == "no_payment_required"`,
which Stripe **only** returns for setup-mode sessions; subscription
trials that collect a card against a $0 invoice return
`payment_status="paid"` with `amount_total=0`.

**Result**: yearly (and monthly) trial checkouts after Phase 1 deploy
fell into `manual_review` with `stripe.checkout.amount_mismatch`,
leaving the Stripe sub created but unlinked from mongo. User reported
"trial didn't take effect"; the orphan `trialing` sub would auto-charge
$200 at trial end with no entitlement granted in our system.

## Fix

Trust `order.is_trial` as the local truth for the trial shape. The
subscription-level price/product/interval check below still catches SKU
swaps, so the original Phase 1 protection against client-side SKU
tampering is preserved.

```python
is_free_trial = order.get("product_type") == "subscription" and (
    payment_status == "no_payment_required" or bool(order.get("is_trial"))
)
```

## Production impact (pre-fix)

- 1 user, 2 stuck `manual_review` orders (5-15 retries) → orphan
trialing subs on Stripe (need manual cancel before 5-22 to avoid $400
auto-charge)
- Phase 1 was deployed ~6 hours before the first reported user;
**monthly trial would have hit the same bug** once a monthly-trial user
came through

## Test plan

- [x] 7 new focused unit tests in
`tests/unit/test_payment_validation.py`:
- trial escape: `payment_status="paid"` + `amount_total=0` (yearly +
monthly)
- trial escape: `payment_status="no_payment_required"` (pre-existing
setup-mode case)
- non-trial: `amount_mismatch` still raises (Phase 1 protection
preserved)
- SKU swap safety net: product/price_amount/interval mismatches still
raise
- [x] 275/275 stripe/payment/checkout unit tests pass — no regressions
- [x] ruff, ruff-format, pyright, import-linter (8/8), file-length,
complexity, deptry, collection-name guard, dead-code — all clean
- [ ] CI full suite + coverage gate

## Ops follow-up (out of scope for this PR)

Affected user `7457396451488833536` has 2 orphan `trialing` yearly subs
on Stripe with `trial_end=2026-05-22`. Need to cancel them (and
optionally manually wire a trial sub into mongo) before then.
```

### PR Description

## Summary

Phase 1 (ECA-681, #1629) added Stripe checkout session validation that rejects any session whose `amount_total` does not match `order.amount`. The trial escape was keyed on `payment_status == "no_payment_required"`, which Stripe **only** returns for setup-mode sessions; subscription trials that collect a card against a $0 invoice return `payment_status="paid"` with `amount_total=0`.

**Result**: yearly (and monthly) trial checkouts after Phase 1 deploy fell into `manual_review` with `stripe.checkout.amount_mismatch`, leaving the Stripe sub created but unlinked from mongo. User reported "trial didn't take effect"; the orphan `trialing` sub would auto-charge $200 at trial end with no entitlement granted in our system.

## Fix

Trust `order.is_trial` as the local truth for the trial shape. The subscription-level price/product/interval check below still catches SKU swaps, so the original Phase 1 protection against client-side SKU tampering is preserved.

```python
is_free_trial = order.get("product_type") == "subscription" and (
    payment_status == "no_payment_required" or bool(order.get("is_trial"))
)
```

## Production impact (pre-fix)

- 1 user, 2 stuck `manual_review` orders (5-15 retries) → orphan trialing subs on Stripe (need manual cancel before 5-22 to avoid $400 auto-charge)
- Phase 1 was deployed ~6 hours before the first reported user; **monthly trial would have hit the same bug** once a monthly-trial user came through

## Test plan

- [x] 7 new focused unit tests in `tests/unit/test_payment_validation.py`:
  - trial escape: `payment_status="paid"` + `amount_total=0` (yearly + monthly)
  - trial escape: `payment_status="no_payment_required"` (pre-existing setup-mode case)
  - non-trial: `amount_mismatch` still raises (Phase 1 protection preserved)
  - SKU swap safety net: product/price_amount/interval mismatches still raise
- [x] 275/275 stripe/payment/checkout unit tests pass — no regressions
- [x] ruff, ruff-format, pyright, import-linter (8/8), file-length, complexity, deptry, collection-name guard, dead-code — all clean
- [ ] CI full suite + coverage gate

## Ops follow-up (out of scope for this PR)

Affected user `7457396451488833536` has 2 orphan `trialing` yearly subs on Stripe with `trial_end=2026-05-22`. Need to cancel them (and optionally manually wire a trial sub into mongo) before then.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
