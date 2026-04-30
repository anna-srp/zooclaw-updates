---
title: "安全加固：多层认证防护升级"
type: "Bug Fix"
priority: "高"
date: "2026-04-29"
status: "待审核"
channels: "Discord, changelog"
---

# 安全加固：多层认证防护升级

## 核心宣传点

平台安全性全面加固：新增防点击劫持响应头、收紧内部服务认证（仅 @srp.one 账户可访问），让你的账户和数据更安全。

## 原始内容

**Commit:** `7d0dd6b2` — 2026-04-29T09:59:06Z
**Repo:** ecap-workspace
**Author:** tim-srp

**Commit Message:**
```
fix: defense-in-depth auth & clickjacking headers (exclude mini-chat embed) (#1436)

## Summary
- **admin_cron**: add `require_internal_service_key` dependency to all 6
cron trigger/query endpoints (defense-in-depth behind CF Zero Trust)
- **orders/admin/grant**: add `require_admin_user` dependency
- **next.config**: add `X-Frame-Options: DENY` +
`Content-Security-Policy: frame-ancestors 'none'` (clickjacking
protection)
- **billing_gateway**: retry `topup_wallet` once on 5xx with 1s backoff
(Lago transient error resilience)

## Context
Production incident 2026-04-27: Lago returned a transient 500 on `POST
/api/v1/wallet_transactions` during a user's subscription grant. The
user saw "Failed to confirm order" and had to re-purchase on a lower
plan. The topup retry prevents this class of failure from reaching the
user.

Security hardening prompted by external vulnerability reports — CF Zero
Trust already protects `/admin/*`, but application-layer auth adds
defense-in-depth. `X-Frame-Options` addresses a reported clickjacking
concern.

## Test plan
- [ ] `pytest tests/unit/test_stripe_billing_gateway.py` — 15 tests pass
(2 new: 500 retry success + 500 retry then raise)
- [ ] `pyright` clean on all changed files
- [ ] Verify cron scheduler passes `X-Internal-Service-Key` header
(otherwise cron triggers will 401)
- [ ] Verify `/admin/grant` still works from admin UI (JWT auth)
- [ ] Verify `zooclaw.ai` pages return `X-Frame-Options: DENY` header
after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

**PR #1436:** fix: defense-in-depth auth & clickjacking headers (exclude mini-chat embed)

**PR Body:**
## Summary
- **admin_cron**: add `require_internal_service_key` dependency to all 6 cron trigger/query endpoints (defense-in-depth behind CF Zero Trust)
- **orders/admin/grant**: add `require_admin_user` dependency
- **next.config**: add `X-Frame-Options: DENY` + `Content-Security-Policy: frame-ancestors 'none'` (clickjacking protection)
- **billing_gateway**: retry `topup_wallet` once on 5xx with 1s backoff (Lago transient error resilience)

## Context
Production incident 2026-04-27: Lago returned a transient 500 on `POST /api/v1/wallet_transactions` during a user's subscription grant. The user saw "Failed to confirm order" and had to re-purchase on a lower plan. The topup retry prevents this class of failure from reaching the user.

Security hardening prompted by external vulnerability reports — CF Zero Trust already protects `/admin/*`, but application-layer auth adds defense-in-depth. `X-Frame-Options` addresses a reported clickjacking concern.

## Test plan
- [ ] `pytest tests/unit/test_stripe_billing_gateway.py` — 15 tests pass (2 new: 500 retry success + 500 retry then raise)
- [ ] `pyright` clean on all changed files
- [ ] Verify cron scheduler passes `X-Internal-Service-Key` header (otherwise cron triggers will 401)
- [ ] Verify `/admin/grant` still works from admin UI (JWT auth)
- [ ] Verify `zooclaw.ai` pages return `X-Frame-Options: DENY` header after deploy

🤖 Generated with [Claude Code](https://claude.com/claude-code)
