---
title: "安全修复：订阅码管理接口添加管理员权限验证"
type: "Bug Fix"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 安全修复：订阅码管理接口添加管理员权限验证

## 核心宣传点

修复了订阅码管理 API 缺少后台权限校验的漏洞，防止越权访问。

## 原始内容

**Commit**: `af5acef7637753d9f7da21ebe95945d2e6afb85a`
**仓库**: ecap-workspace
**作者**: tim-srp
**时间**: 2026-04-28T11:25:32Z

### 完整 Commit Message

```
fix(web): add subscription-codes to ADMIN_ROUTES middleware guard (#1442)

## Summary
- Add `/api/admin/subscription-codes/list` and
`/api/admin/subscription-codes/create` to `ADMIN_ROUTES` and
`UID_VALIDATION_EXEMPT` in `auth-middleware.ts`

## Root Cause
These two endpoints were missing from the middleware's admin route guard
list. When the BFF's `proxyToBackend` call fails (e.g. transient network
issue to backend), routes **in** `ADMIN_ROUTES` fail with a clean 403
JSON from the middleware's fail-closed admin check, while routes **not**
in the list bypass that check entirely — the BFF handler's catch block
returns a 500, which Cloudflare's edge replaces with an HTML error page,
causing the frontend JSON parse to fail with `Unexpected token '<'`.

## Test plan
- [ ] CI passes
- [ ] Deploy to staging → open Admin Dashboard → Subscription Code tab
loads correctly
- [ ] Verify non-admin users get 403 (not 500) when accessing these
endpoints

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1442 完整描述

## Summary
- Add `/api/admin/subscription-codes/list` and `/api/admin/subscription-codes/create` to `ADMIN_ROUTES` and `UID_VALIDATION_EXEMPT` in `auth-middleware.ts`

## Root Cause
These two endpoints were missing from the middleware's admin route guard list. When the BFF's `proxyToBackend` call fails (e.g. transient network issue to backend), routes **in** `ADMIN_ROUTES` fail with a clean 403 JSON from the middleware's fail-closed admin check, while routes **not** in the list bypass that check entirely — the BFF handler's catch block returns a 500, which Cloudflare's edge replaces with an HTML error page, causing the frontend JSON parse to fail with `Unexpected token '<'`.

## Test plan
- [ ] CI passes
- [ ] Deploy to staging → open Admin Dashboard → Subscription Code tab loads correctly
- [ ] Verify non-admin users get 403 (not 500) when accessing these endpoints

🤖 Generated with [Claude Code](https://claude.com/claude-code)
