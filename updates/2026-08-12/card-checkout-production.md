---
title: "信用卡支付正式上线：可用 Card 订阅 ZooClaw"
type: "新功能上线"
priority: "高"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# 信用卡支付正式上线：可用 Card 订阅 ZooClaw

## 核心宣传点

ZooClaw 正式开放信用卡（Card）支付，结算方式弹窗里可以在支付宝之外直接选信用卡，订阅与免费试用全流程走通。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `cb75b029cc28d52f675cce0b59542bdb2a0ac855`
- PR: #3355

### Commit Message

```
feat(billing): enable Card checkout in production (#3355)

## Summary

- show Card alongside Alipay in the payment-method modal in production
- request the backend Card checkout capability for authenticated
production users
- allow production runtime only with Creem production mode, while
retaining test-mode staging/dev pairing
- treat `card_available=false` as a hard Card gate without falling back
new users to legacy Stripe

## Why

The Creem Card trial and subscription flows are now implemented and
validated, but both frontend and backend still contained
staging/test-only rollout guards. Production Creem products and Vault
configuration are now ready.

## Validation

- 155 related frontend tests passed
- 77 related backend tests passed
- TypeScript, ESLint, Ruff, Ruff format, import contracts, and
pre-commit Pyright passed
- PR size: 326 changed lines across 15 files (+146/-180), mostly
regression-test migration from new-user Stripe to Creem semantics

## Deployment note

Production is enabled only for the `production` runtime paired with
`CREEM_ENVIRONMENT=production`. Staging/dev/local remain paired with
Creem test mode. Incomplete or mismatched configuration returns
`card_available=false` and Card is disabled/rejected safely. Existing
Stripe subscribers retain their legacy compatibility path; Alipay is
unchanged.
```

### PR Body

## Summary

- show Card alongside Alipay in the payment-method modal in production
- request the backend Card checkout capability for authenticated production users
- allow production runtime only with Creem production mode, while retaining test-mode staging/dev pairing
- treat `card_available=false` as a hard Card gate without falling back new users to legacy Stripe

## Why

The Creem Card trial and subscription flows are now implemented and validated, but both frontend and backend still contained staging/test-only rollout guards. Production Creem products and Vault configuration are now ready.

## Validation

- 155 related frontend tests passed
- 77 related backend tests passed
- TypeScript, ESLint, Ruff, Ruff format, import contracts, and pre-commit Pyright passed
- PR size: 326 changed lines across 15 files (+146/-180), mostly regression-test migration from new-user Stripe to Creem semantics

## Deployment note

Production is enabled only for the `production` runtime paired with `CREEM_ENVIRONMENT=production`. Staging/dev/local remain paired with Creem test mode. Incomplete or mismatched configuration returns `card_available=false` and Card is disabled/rejected safely. Existing Stripe subscribers retain their legacy compatibility path; Alipay is unchanged.


---

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `b4a99063c9732902c6403fba46181e137bea1432`
- PR: #3357

### Commit Message

```
fix(billing): preserve Creem checkout environment (#3357)

## Summary
- Persist the current Creem billing environment on newly created Card
Checkout orders.
- Validate Checkout and Trial webhook provider modes against the order
environment: sandbox accepts test/sandbox and production accepts prod.
- Pass the dynamic environment through checkout binding, first-payment,
settlement, trial projection, and reconciliation CAS operations.
- Keep legacy orders unchanged; this PR does not add historical-order
migration or manual MongoDB repair.

## Root cause
Card Checkout orders were always persisted with `environment=sandbox`,
and Checkout/Trial projection code only accepted Creem test/sandbox
provider modes. In production, Creem emits `mode=prod`, so a successful
production checkout could not bind or project the trial and the local
order remained pending.

## Test plan
- [x] 218 targeted Card Checkout and Creem lifecycle unit tests pass.
- [x] Production Checkout webhook binds a production order.
- [x] Production Trial webhook records the agreement and trial
projection with production environment.
- [x] Ruff check and format pass.
- [x] Commit-time Pyright and repository policy hooks pass.
- [ ] GitHub Code Quality Check passes in the dependency-complete CI
environment.

## Local environment note
The pre-push changed-surface verifier could not resolve the worktree's
Python dependencies and reported repository-wide missing imports. The
commit hook's Pyright check passed, and the branch was pushed with
`--no-verify` so GitHub CI can run the authoritative dependency-complete
checks.
```

### PR Body

## Summary
- Persist the current Creem billing environment on newly created Card Checkout orders.
- Validate Checkout and Trial webhook provider modes against the order environment: sandbox accepts test/sandbox and production accepts prod.
- Pass the dynamic environment through checkout binding, first-payment, settlement, trial projection, and reconciliation CAS operations.
- Keep legacy orders unchanged; this PR does not add historical-order migration or manual MongoDB repair.

## Root cause
Card Checkout orders were always persisted with `environment=sandbox`, and Checkout/Trial projection code only accepted Creem test/sandbox provider modes. In production, Creem emits `mode=prod`, so a successful production checkout could not bind or project the trial and the local order remained pending.

## Test plan
- [x] 218 targeted Card Checkout and Creem lifecycle unit tests pass.
- [x] Production Checkout webhook binds a production order.
- [x] Production Trial webhook records the agreement and trial projection with production environment.
- [x] Ruff check and format pass.
- [x] Commit-time Pyright and repository policy hooks pass.
- [ ] GitHub Code Quality Check passes in the dependency-complete CI environment.

## Local environment note
The pre-push changed-surface verifier could not resolve the worktree's Python dependencies and reported repository-wide missing imports. The commit hook's Pyright check passed, and the branch was pushed with `--no-verify` so GitHub CI can run the authoritative dependency-complete checks.


---
