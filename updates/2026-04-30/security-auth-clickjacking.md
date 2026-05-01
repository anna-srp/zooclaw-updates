---
title: "安全加固：防止点击劫持攻击，订阅错误自动重试"
type: "Bug Fix"
priority: "高"
date: "2026-04-30"
status: "待审核"
channels: ""
---
# 安全加固：防止点击劫持攻击，订阅错误自动重试

## 核心宣传点
修复了一个安全漏洞，防止恶意网站嵌套显示 ZooClaw 页面实施欺骗攻击；同时修复了购买订阅时偶发失败的问题，现在会自动重试。

## 原始内容
**Commit**: fix: defense-in-depth auth & clickjacking headers (exclude mini-chat embed) (#1436)
**Author**: （merge commit）
**Date**: 2026-04-29

```
fix: defense-in-depth auth & clickjacking headers (exclude mini-chat embed) (#1436)

## Summary
- admin_cron: add require_internal_service_key dependency to all 6 cron endpoints
- orders/admin/grant: add require_admin_user dependency
- next.config: add X-Frame-Options: DENY + Content-Security-Policy: frame-ancestors 'none' (clickjacking protection)
- billing_gateway: retry topup_wallet once on 5xx with 1s backoff
```

**PR #1436 Body**:
## Summary
- admin_cron: add require_internal_service_key dependency to all 6 cron trigger/query endpoints (defense-in-depth behind CF Zero Trust)
- orders/admin/grant: add require_admin_user dependency
- next.config: add X-Frame-Options: DENY + Content-Security-Policy: frame-ancestors 'none' (clickjacking protection)
- billing_gateway: retry topup_wallet once on 5xx with 1s backoff (Lago transient error resilience)

## Context
Production incident 2026-04-27: Lago returned a transient 500 on POST /api/v1/wallet_transactions during a user's subscription grant. The user saw "Failed to confirm order" and had to re-purchase on a lower plan. The topup retry prevents this class of failure from reaching the user.

Security hardening prompted by external vulnerability reports — CF Zero Trust already protects /admin/*, but application-layer auth adds defense-in-depth. X-Frame-Options addresses a reported clickjacking concern.
