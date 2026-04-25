---
title: "结账性能优化：减少重复数据库查询"
type: "产品基础功能更新"
priority: "低"
date: "2026-04-25"
status: "待审核"
channels: "Discord + changelog"
---

# 结账性能优化：减少重复数据库查询

## 核心宣传点

优化了结账流程中的数据库查询，减少重复请求，提升支付响应速度。

## 原始内容

Commit: 67ade1e90293cbaa2a37bd2fd4b30a04d0a9c2d1

Message:
perf(api): cache user doc on _CheckoutCtx to eliminate duplicate Mongo reads (#746) (#773)

## Summary

Caches the user doc on `_CheckoutCtx` to eliminate duplicate user reads
on the `checkout.session.completed` path.

**Before:** up to 3 calls to `user_repo.get_user(ctx.uid)` per event —
one in `_apply_base_order_update` (for the `old_stripe_sub_id` snapshot
fallback), plus one each in `_try_invite_trial_path` and
`_try_stripe_trial_path`.

**After:** 1 call, issued once by `_load_checkout_context` and reused by
every path helper via `ctx.user`. Saves ~5-20ms per webhook on the hot
billing path.

## Why a pre-update snapshot is sufficient

`user_repo.update_subscription_info` only mirrors Stripe IDs
(`subscription_id` / `customer_id` / `product_id`). The fields the
downstream helpers inspect (`subscription_status`, `team_id`,
`wallet_subscription_id`, `billing_customer_id`) are untouched, so a
single pre-update snapshot is valid for every downstream check. The
`_CheckoutCtx.user` docstring records this invariant so future edits
don't silently regress it.

For the `old_stripe_sub_id` snapshot, retry safety is preserved:
`_apply_base_order_update` still prefers
`ctx.order.get("old_stripe_sub_id")` (persisted on the order by a prior
attempt) over the cached user doc, so a retry after
`user`-update-success / `order`-update-fail still enters the upgrade
path.

## Rebase note

This PR was originally drafted against a pre-#771 tree where handlers
read user docs via raw `mongo.read_one(ACCOUNT_COLLECTION, ...)`. After
rebase onto main, the "migrate to `user_repo`" portion is already in
place (#771 PR B2), so this PR is now a single-concern change: add the
`ctx.user` cache and route the three path helpers through it.

## Test plan
- [x] `ruff format .` / `ruff check .` — clean
- [x] `ruff format --check .` — clean
- [x] `pyright app/ tests/` — 0 errors
- [x] `lint-imports` — all 8 contracts KEPT (C1 `mongo` import boundary
preserved)
- [x] `pytest tests/unit/test_checkout_*
tests/unit/test_subscription_manager.py
tests/bdd/step_defs/test_stripe_webhooks.py
tests/bdd/step_defs/test_stripe_webhook_dispatch.py
tests/bdd/step_defs/test_stripe_order_confirm.py` — 47 passed
- [x] BDD with `TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER=
MONGODB_PASSWORD=` — 16 passed on checkout/order scope (memory:
`reference_local_bdd_mongo`)
- [ ] CI green

Resolves #746. Related: #771, #776.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Developer <dev@srp.one>
Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
