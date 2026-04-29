---
title: "安全修复：礼品码管理接口添加管理员权限验证"
type: "Bug Fix"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 安全修复：礼品码管理接口添加管理员权限验证

## 核心宣传点

修复了礼品码管理 API 缺少后台权限校验的漏洞，防止越权访问。

## 原始内容

**Commit**: `3e036047d76cb9d0a4009799962da92e0ab775bb`
**仓库**: ecap-workspace
**作者**: tim-srp
**时间**: 2026-04-28T12:53:41Z

### 完整 Commit Message

```
fix(web): add gift-codes to ADMIN_ROUTES middleware guard (#1448)

## Summary
- Same byte-for-byte twin pattern as #1442 (subscription-codes):
`/api/admin/gift-codes/{list,create}` BFF handlers proxy to
`/admin/gift-codes`, whose backend `Depends(require_admin_user)` rejects
non-admins, but the BFF middleware was silently letting requests through
because the routes weren't whitelisted in `ADMIN_ROUTES` /
`UID_VALIDATION_EXEMPT`.
- Adds 4 lines (2 in each list) so the BFF returns a deterministic 403
for non-admins / CF-Access-rejected requests instead of falling through
to a `response.json()` parse failure caught as 500.

## Why this was missed in #1442
There's no enforcement that `ADMIN_ROUTES` stays in sync with
`web/src/app/api/admin/**/route.ts` — each new admin page has to
remember to update the whitelist by hand, and the existing
`isAdminRoute` unit tests only spot-check 4 specific routes rather than
asserting the full file-tree ↔ list parity. A follow-up to add that
guard would prevent the next occurrence; tracked separately.

## Test plan
- [ ] Manual: log in as a non-admin user, hit the admin gift-codes page
→ expect BFF 403 "Admin access required" (previously: 500 "Failed to
list gift codes" via the JSON-parse-error path)
- [ ] Admin user: page continues to work (BFF now performs an extra
`/users/get` permission check before proxying)
- [ ] CI: `code-quality / lint-and-test` passes (lint already green
locally)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1448 完整描述

## Summary
- Same byte-for-byte twin pattern as #1442 (subscription-codes): `/api/admin/gift-codes/{list,create}` BFF handlers proxy to `/admin/gift-codes`, whose backend `Depends(require_admin_user)` rejects non-admins, but the BFF middleware was silently letting requests through because the routes weren't whitelisted in `ADMIN_ROUTES` / `UID_VALIDATION_EXEMPT`.
- Adds 4 lines (2 in each list) so the BFF returns a deterministic 403 for non-admins / CF-Access-rejected requests instead of falling through to a `response.json()` parse failure caught as 500.

## Why this was missed in #1442
There's no enforcement that `ADMIN_ROUTES` stays in sync with `web/src/app/api/admin/**/route.ts` — each new admin page has to remember to update the whitelist by hand, and the existing `isAdminRoute` unit tests only spot-check 4 specific routes rather than asserting the full file-tree ↔ list parity. A follow-up to add that guard would prevent the next occurrence; tracked separately.

## Test plan
- [ ] Manual: log in as a non-admin user, hit the admin gift-codes page → expect BFF 403 "Admin access required" (previously: 500 "Failed to list gift codes" via the JSON-parse-error path)
- [ ] Admin user: page continues to work (BFF now performs an extra `/users/get` permission check before proxying)
- [ ] CI: `code-quality / lint-and-test` passes (lint already green locally)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
