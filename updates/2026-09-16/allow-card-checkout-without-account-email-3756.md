---
title: "fix(billing): allow card checkout without account email (#3756)"
type: "Bug 修复"
priority: "高"
date: "2026-09-16"
status: "待审核"
channels: ""
---

# fix(billing): allow card checkout without account email (#3756)

## 核心宣传点

手机号登录的账号现在也能直接用信用卡下单：订阅、试用、升级、充值都不再因为缺少账号邮箱而卡住，邮箱在 Airwallex 托管收银台里补填。

## PR 说明

## Summary
- Allow phone-login accounts to create subscription, trial, upgrade, and top-up Card checkouts without an account email.
- Prefill Airwallex `customer_data.email` when an email is available; otherwise omit `customer_data` so hosted checkout can collect it. Do not send phone numbers.
- Preserve UID validation, order ownership, trial eligibility, and checkout replay/idempotency behavior.

## Root cause
The route and service required a non-empty authenticated email even though the existing Airwallex checkout request did not use it. Phone-login accounts therefore received HTTP 400 before reaching checkout creation.

Airwallex supports optional email prefill and collects email on the hosted page when omitted: https://www.airwallex.com/docs/api/billing/billing_checkouts/api

## Test plan
- [x] 211 targeted tests passed across Card routes, subscription/trial, upgrade, top-up, Airwallex client, and schemas.
- [x] Cover missing/blank email, email prefill, monthly/yearly trials, checkout reuse, invalid UID rejection, and outgoing JSON omission.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8 import contracts passed.
- [x] `git diff --check`.
- [ ] Staging smoke test after backend deployment; no live checkout or payment was created during local validation.

Backend-only change. No frontend deployment required.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `f8ebfc194ca27597dc0aec87adb3916342db6d8f`
- PR: #3756
- 作者：tim-srp
- 日期：2026-09-16T11:15:21Z

### Commit Message

```
fix(billing): allow card checkout without account email (#3756)

## Summary
- Allow phone-login accounts to create subscription, trial, upgrade, and
top-up Card checkouts without an account email.
- Prefill Airwallex `customer_data.email` when an email is available;
otherwise omit `customer_data` so hosted checkout can collect it. Do not
send phone numbers.
- Preserve UID validation, order ownership, trial eligibility, and
checkout replay/idempotency behavior.

## Root cause
The route and servic
```
