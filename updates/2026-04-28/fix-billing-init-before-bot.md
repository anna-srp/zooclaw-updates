---
title: "修复：新用户注册后创建 Bot 失败的问题"
type: "Bug Fix"
priority: "高"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 修复：新用户注册后创建 Bot 失败的问题

## 核心宣传点

修复了部分新用户注册后因计费初始化失败导致无法创建 Bot 的问题，注册流程更稳定。

## 原始内容

**Commit**: `ee2f2abee20b8e02a67c3f06221037d163ceaf49`
**仓库**: ecap-workspace
**作者**: bryce-srp
**时间**: 2026-04-28T11:22:51Z

### 完整 Commit Message

```
fix(claw-interface): ensure billing initialized before bot creation (#1432)

## Summary
- Bot creation fails with "team_key missing in MongoDB" when billing
init silently failed during signup
- Added `ensure_billing_initialized()` call before Case 3 (no bot →
create) in `/openclaw/init`
- Same pattern already used in `/user/get`, `/user/create`,
`/credits/*`, `/orders/*`

## Root cause
- `POST /user/create` calls `ensure_billing_initialized()` but
fail-opens on Billing Gateway errors
- User ends up with `billing_initialized=False`, `team_key=None`
- Frontend immediately calls `POST /openclaw/init` → bot creation needs
`team_key` → fails
- 3 users affected in 14 days (4/23 and 4/27)

## Test plan
- [ ] CI passes (pyright + pytest)
- [ ] New user signup → bot creation should work even if first billing
init was slow

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR #1432 完整描述

## Summary
- Bot creation fails with "team_key missing in MongoDB" when billing init silently failed during signup
- Added `ensure_billing_initialized()` call before Case 3 (no bot → create) in `/openclaw/init`
- Same pattern already used in `/user/get`, `/user/create`, `/credits/*`, `/orders/*`

## Root cause
- `POST /user/create` calls `ensure_billing_initialized()` but fail-opens on Billing Gateway errors
- User ends up with `billing_initialized=False`, `team_key=None`
- Frontend immediately calls `POST /openclaw/init` → bot creation needs `team_key` → fails
- 3 users affected in 14 days (4/23 and 4/27)

## Test plan
- [ ] CI passes (pyright + pytest)
- [ ] New user signup → bot creation should work even if first billing init was slow

🤖 Generated with [Claude Code](https://claude.com/claude-code)
