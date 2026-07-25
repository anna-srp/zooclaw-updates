---
title: "修复：试用到期后无法进入付费购买的问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-24"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了已用完免费试用的用户无法继续付费购买的问题。现在试用到期后可正常进入 Stripe / Antom 付费结算，付费与试用模式区分清晰，定价与提示文案也已对齐，不会再卡在无法支付的状态。

## 原始内容

**Commit**: `e5334430c2` — sharplee-srp — 2026-07-24T10:07:18Z

### Commit Message

```
fix(payments): allow paid checkout after trial expiry (#3061)

## Summary

- distinguish free-trial and paid modes in the chat paywall using the
authenticated subscription snapshot
- allow users who already consumed their trial to continue into Stripe
or Antom paid checkout
- preserve the trial-denial guard and require an explicit paid retry
when backend eligibility changes at checkout time
- update pricing, CTA copy, and trial authorization notice to match the
actual checkout mode

## Root cause

The chat paywall assumed every expired user was starting a free trial.
It created a local order and then unconditionally stopped when the
backend correctly returned `is_trial=false`, so no provider checkout
session was created and the local order remained providerless and
pending.

## Test plan

- `bash scripts/verify-web.sh web/app/src/components/PaywallContent.tsx
web/app/tests/unit/components/PaywallContent.unit.spec.tsx`
- `bash scripts/verify-changed.sh`
- targeted PaywallContent unit suite: 22 tests passed

## Risk controls

- a user who was shown a free-trial offer is never silently moved into a
paid checkout
- backend `is_trial` remains authoritative for last-moment eligibility
changes
- the existing free-trial authorization flow remains unchanged for
eligible users
```

### PR Body

## Summary

- distinguish free-trial and paid modes in the chat paywall using the authenticated subscription snapshot
- allow users who already consumed their trial to continue into Stripe or Antom paid checkout
- preserve the trial-denial guard and require an explicit paid retry when backend eligibility changes at checkout time
- update pricing, CTA copy, and trial authorization notice to match the actual checkout mode

## Root cause

The chat paywall assumed every expired user was starting a free trial. It created a local order and then unconditionally stopped when the backend correctly returned `is_trial=false`, so no provider checkout session was created and the local order remained providerless and pending.

## Test plan

- `bash scripts/verify-web.sh web/app/src/components/PaywallContent.tsx web/app/tests/unit/components/PaywallContent.unit.spec.tsx`
- `bash scripts/verify-changed.sh`
- targeted PaywallContent unit suite: 22 tests passed

## Risk controls

- a user who was shown a free-trial offer is never silently moved into a paid checkout
- backend `is_trial` remains authoritative for last-moment eligibility changes
- the existing free-trial authorization flow remains unchanged for eligible users

