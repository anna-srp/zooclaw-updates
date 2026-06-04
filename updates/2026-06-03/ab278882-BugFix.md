---
title: "清理旧版订阅 cron 写入逻辑"
type: "Bug Fix"
priority: "中"
date: "2026-06-03"
status: "待审核"
channels: "Discord, changelog"
---
# 清理旧版订阅 cron 写入逻辑

## 核心宣传点

清理旧版订阅定时任务，提升系统稳定性。

## 原始内容

**Repo:** SerendipityOneInc/ecap-workspace  
**SHA:** `ab2788826a2d45f70450af56f1970f7d3af05803`  
**作者:** kaka-srp  
**日期:** 2026-06-03T09:47:12Z  
**URL:** https://github.com/SerendipityOneInc/ecap-workspace/commit/ab2788826a2d45f70450af56f1970f7d3af05803

### Commit Message

```
fix(billing): remove legacy subscription cron writes (#2161)

## Summary
- Disable legacy trial-expiry cron writes and keep the endpoint as a
no-op for stale scheduler calls.
- Route subscription sync to Billing v2 maintenance only.
- Add Billing v2 yearly credit reset based on current provider-backed
agreements, with entitlement leases, retry deferral, and idempotent
wallet balance setting.
- Fix Stripe Billing v2 period extraction so active subscriptions do not
keep stale trial dates.

## Root cause
Legacy cron jobs were still scanning and mutating legacy account
subscription fields after the Billing v2 cutover. That allowed stale
Stripe subscription state to activate or mutate users outside the v2
agreement/order/entitlement model. Yearly credit reset also still
depended on legacy account cron fields instead of v2 provider-backed
agreement state.

## Size override rationale
This PR is over the 2000-line size gate because it removes the legacy
subscription cron branches and replaces the old broad cron test file
with narrow v2/no-op tests. Splitting the change would leave either
stale legacy cron writes enabled or the new v2 yearly reset path
unverified.

## Test plan
- [x] `ruff check .`
- [x] `pyright app tests`
- [x] Relevant backend unit tests: `146 passed`
- [x] Full `pytest --cov=app --cov-report=term-missing
--cov-fail-under=90 -q` started after rebasing; interrupted per request
before completion. It had one unrelated OpenClaw test failure/error
while running.

Linear: https://linear.app/srpone/issue/ECA-882/billing-v2-cron-cleanup
```

### PR Description

## Summary
- Disable legacy trial-expiry cron writes and keep the endpoint as a no-op for stale scheduler calls.
- Route subscription sync to Billing v2 maintenance only.
- Add Billing v2 yearly credit reset based on current provider-backed agreements, with entitlement leases, retry deferral, and idempotent wallet balance setting.
- Fix Stripe Billing v2 period extraction so active subscriptions do not keep stale trial dates.

## Root cause
Legacy cron jobs were still scanning and mutating legacy account subscription fields after the Billing v2 cutover. That allowed stale Stripe subscription state to activate or mutate users outside the v2 agreement/order/entitlement model. Yearly credit reset also still depended on legacy account cron fields instead of v2 provider-backed agreement state.

## Size override rationale
This PR is over the 2000-line size gate because it removes the legacy subscription cron branches and replaces the old broad cron test file with narrow v2/no-op tests. Splitting the change would leave either stale legacy cron writes enabled or the new v2 yearly reset path unverified.

## Test plan
- [x] `ruff check .`
- [x] `pyright app tests`
- [x] Relevant backend unit tests: `146 passed`
- [x] Full `pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` started after rebasing; interrupted per request before completion. It had one unrelated OpenClaw test failure/error while running.

Linear: https://linear.app/srpone/issue/ECA-882/billing-v2-cron-cleanup
