---
title: "修复：邀请码试用期正确终止，新增订阅对账机制"
type: "Bug Fix"
priority: "高"
date: "2026-05-09"
status: "待审核"
channels: "Discord, changelog"
---
# 修复：邀请码试用期正确终止，新增订阅对账机制

## 核心宣传点
修复了通过邀请码领取试用的用户，在试用期结束后无法正常续费订阅的问题。同时新增了自动对账机制，持续检测并修复后台计费与数据库之间的状态不一致。

## 原始内容

**Commit**: `17cd6725` | **PR**: #1583

### Commit Message

```
feat(cron): trial BG terminate fix + BG/Lago↔Mongo reconciler (ECA-647 follow-ups) (#1583)

## Summary

Two ECA-647 follow-ups bundled, both stemming from the same Apple-webhook RCA sweep:

Fix #1: trial BG terminate gated on `billing_initialized`, not external sub id
ECA-543's `has_external_sub` guard (skip BG terminate when no Stripe/Apple sub id) silently skipped trial users redeemed via invite-code — they have no Stripe/Apple ID but do have a `free_month` BG sub from `ensure_billing_initialized`. Their trial cron expiry flipped mongo to `expired` while leaving Lago holding the sub alive, blocking their next subscribe attempt with the same 400.

Fix #2: BG/Lago ↔ Mongo subscription drift reconciler
```

### PR Body

## Summary

Two ECA-647 follow-ups bundled, both stemming from the same Apple-webhook RCA sweep:

### Fix #1: trial BG terminate gated on `billing_initialized`, not external sub id

ECA-543's `has_external_sub` guard (skip BG terminate when no Stripe/Apple sub id) silently skipped trial users redeemed via invite-code — they have no Stripe/Apple ID but **do** have a `free_month` BG sub from `ensure_billing_initialized`. Their trial cron expiry flipped mongo to `expired` while leaving Lago holding the sub alive, blocking their next subscribe attempt with the same 400 fixed in #1582.

7 prod users affected (already wash-cleaned). Switch the predicate from `has_external_sub` → `billing_initialized`. Preserves ECA-543's noise-suppression intent while correctly covering invite-code trials.

### Fix #2: BG/Lago ↔ Mongo subscription drift reconciler

Companion to `stripe_reconcile.py` — together they cover both sides of the three-way contract Mongo/Stripe/Lago that this codebase has accumulated drift between.

Detects accounts whose mongo `subscription_status` is terminal (`expired` / `free` / `canceled`) but whose Lago team still holds an `active` subscription — the precondition behind every variant of the ECA-647 `start_date is only supported when creating a new subscription` 400.

- New cron: `app/cron/bg_reconcile.py` (`check_bg_mongo_reconcile`)
- New endpoint: `POST /admin/cron/check-bg-mongo-reconcile?batch_limit=500&write_mode=false`
- Read-only by default; `write_mode=true` calls `terminate_subscription` per orphan
- Per-team BG lookup is async with `asyncio.Semaphore(50)` — 50/sec is well within BG tolerance
- Greppable log markers: `[DRIFT]` / `[APPLIED]` / `[SUMMARY]`

## Test plan

- [x] `tests/unit/test_subscription_cron.py` — 2 new tests on the trial guard fix
- [x] `tests/unit/test_bg_reconcile.py` — 8 new tests: empty result, aligned-no-drift, drift-read-only, drift-write-mode, terminate-failure-soft-retry, lookup-failure-counted, no-billing-url-skip, missing-external-id fallback
- [x] 101 tests pass across all related test files

Linear-issue: Refs ECA-647
