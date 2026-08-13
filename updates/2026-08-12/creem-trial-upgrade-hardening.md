---
title: "试用转正式订阅更稳：额度保留、状态不再错乱"
type: "Bug Fix"
priority: "高"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# 试用转正式订阅更稳：额度保留、状态不再错乱

## 核心宣传点

信用卡 Starter 试用期内升级为正式付费订阅时，原有试用额度完整保留、旧试用订阅可靠取消；即使支付回调乱序或丢失，订阅状态也会自动对齐，不会出现重复扣费或权益丢失。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `54f9d4e0ee3382477cd19349c54c94aeefc93284`
- PR: #3341

### Commit Message

```
fix(billing): harden Creem trial upgrades and reconciliation (#3341)

## Summary

- Allow an active Creem Starter Card Trial to be replaced by a paid Card
subscription while retaining the existing Trial credits, matching the
Antom/Alipay upgrade behavior.
- Make the replacement handoff durable across missed, duplicated, and
reordered Creem webhooks with exact admission fingerprints, provider
watermarks, reconciliation leases, and sticky manual-review handling for
ambiguous financial outcomes.
- Prevent terminal cleanup from deleting a successor subscription's
shared wallet, and require authoritative provider cancellation before
immediate cleanup completes.
- Surface pending/manual-review Card checkout state consistently in
Billing Summary and the frontend, while isolating those records by Creem
environment.
- Validate the complete paid + Trial Creem catalog used by the
staging/Test Mode path.

## Root cause

The original Card Trial upgrade path assumed an in-order happy path:
checkout completion, provider activation, local projection, and
old-Trial cleanup. A missed or reordered webhook could leave the local
order pending after Creem was already active, or clean up shared billing
state belonging to the successor subscription. The UI also treated Trial
as an ordinary effective subscription and blocked upgrades.

This change records the replacement intent and provider observations
durably, then lets webhook handling and hourly reconciliation converge
on the same idempotent state machine. Ambiguous cases fail closed into
`manual_review` instead of retrying a potentially duplicate cancellation
or charge transition.

## Risk and rollout

- High-risk billing state-machine change, limited to the currently
enabled staging / Creem Test Mode Card path.
- Production Card checkout remains disabled. Remaining Test
Mode-specific binding and settlement guards must be parameterized before
enabling Creem Card in production.
- Antom/Alipay behavior is unchanged; regression tests cover its
existing Trial and paid-order paths.
- No production purchase was initiated during validation.

## Size override rationale

The diff is large because the same replacement transaction spans
checkout admission, first-payment settlement, webhook recovery, hourly
reconciliation, terminal cleanup, Billing Summary, and frontend
presentation. Splitting those pieces would temporarily ship incompatible
state contracts. More than half of the added lines are unit tests
covering event-order permutations and failure recovery.

## Test plan

- [x] Backend focused regression: 740 tests passed.
- [x] Antom/Alipay regression: 163 tests passed.
- [x] Final reconciliation/manual-review/cleanup regression: 197 tests
passed.
- [x] Frontend focused regression: 372 passed, 1 skipped.
- [x] Frontend governance, TypeScript, and ESLint checks passed.
- [x] Ruff check + format, import contracts, repository guards,
file-length/complexity guards, and changed-file Pyright passed.
- [x] Two independent code reviews completed; both blocking findings
were fixed and re-tested.
- [ ] CI full Code Quality Check.
- [ ] Staging E2E: Card Starter Trial creation and entitlement grant.
- [ ] Staging E2E: Trial to paid Card upgrade, old Trial cleanup, and
retained credits.
- [ ] Staging E2E: cancellation and hourly reconciliation recovery.

Note: one local attempt to run the entire Python unit suite hit a
Miniconda interpreter segmentation fault during `unittest.mock` garbage
collection. The focused suites above and commit hooks completed
successfully; CI remains the authoritative full-suite run.
```

### PR Body

## Summary

- Allow an active Creem Starter Card Trial to be replaced by a paid Card subscription while retaining the existing Trial credits, matching the Antom/Alipay upgrade behavior.
- Make the replacement handoff durable across missed, duplicated, and reordered Creem webhooks with exact admission fingerprints, provider watermarks, reconciliation leases, and sticky manual-review handling for ambiguous financial outcomes.
- Prevent terminal cleanup from deleting a successor subscription's shared wallet, and require authoritative provider cancellation before immediate cleanup completes.
- Surface pending/manual-review Card checkout state consistently in Billing Summary and the frontend, while isolating those records by Creem environment.
- Validate the complete paid + Trial Creem catalog used by the staging/Test Mode path.

## Root cause

The original Card Trial upgrade path assumed an in-order happy path: checkout completion, provider activation, local projection, and old-Trial cleanup. A missed or reordered webhook could leave the local order pending after Creem was already active, or clean up shared billing state belonging to the successor subscription. The UI also treated Trial as an ordinary effective subscription and blocked upgrades.

This change records the replacement intent and provider observations durably, then lets webhook handling and hourly reconciliation converge on the same idempotent state machine. Ambiguous cases fail closed into `manual_review` instead of retrying a potentially duplicate cancellation or charge transition.

## Risk and rollout

- High-risk billing state-machine change, limited to the currently enabled staging / Creem Test Mode Card path.
- Production Card checkout remains disabled. Remaining Test Mode-specific binding and settlement guards must be parameterized before enabling Creem Card in production.
- Antom/Alipay behavior is unchanged; regression tests cover its existing Trial and paid-order paths.
- No production purchase was initiated during validation.

## Size override rationale

The diff is large because the same replacement transaction spans checkout admission, first-payment settlement, webhook recovery, hourly reconciliation, terminal cleanup, Billing Summary, and frontend presentation. Splitting those pieces would temporarily ship incompatible state contracts. More than half of the added lines are unit tests covering event-order permutations and failure recovery.

## Test plan

- [x] Backend focused regression: 740 tests passed.
- [x] Antom/Alipay regression: 163 tests passed.
- [x] Final reconciliation/manual-review/cleanup regression: 197 tests passed.
- [x] Frontend focused regression: 372 passed, 1 skipped.
- [x] Frontend governance, TypeScript, and ESLint checks passed.
- [x] Ruff check + format, import contracts, repository guards, file-length/complexity guards, and changed-file Pyright passed.
- [x] Two independent code reviews completed; both blocking findings were fixed and re-tested.
- [ ] CI full Code Quality Check.
- [ ] Staging E2E: Card Starter Trial creation and entitlement grant.
- [ ] Staging E2E: Trial to paid Card upgrade, old Trial cleanup, and retained credits.
- [ ] Staging E2E: cancellation and hourly reconciliation recovery.

Note: one local attempt to run the entire Python unit suite hit a Miniconda interpreter segmentation fault during `unittest.mock` garbage collection. The focused suites above and commit hooks completed successfully; CI remains the authoritative full-suite run.


---
