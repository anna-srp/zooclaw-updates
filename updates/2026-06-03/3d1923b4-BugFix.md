---
title: "修复 Firebase Token 交换认证流程"
type: "Bug Fix"
priority: "中"
date: "2026-06-03"
status: "待审核"
channels: "Discord, changelog"
---
# 修复 Firebase Token 交换认证流程

## 核心宣传点

修复部分用户 Firebase 登录失败的问题。

## 原始内容

**Repo:** SerendipityOneInc/ecap-workspace  
**SHA:** `3d1923b47d180a24fcf18f5155163c9d222da6a6`  
**作者:** bill-srp  
**日期:** 2026-06-03T07:48:08Z  
**URL:** https://github.com/SerendipityOneInc/ecap-workspace/commit/3d1923b47d180a24fcf18f5155163c9d222da6a6

### Commit Message

```
fix(auth-client): support Firebase token exchange (#2163)

## Linear
Not applicable: PR title is `fix`, not `feat`.

## Summary
- Add `AccountClient.exchangeFirebaseToken()` for account-service
`/auth/exchange`.
- Send Firebase ID tokens through the expected `fb-token` bearer header.
- Cover successful exchange and non-2xx error behavior in auth-client
tests.

## Test plan
- [x] `pnpm --filter @zooclaw/auth-client test`
- [x] `pnpm --filter @zooclaw/auth-client lint`
```

### PR Description

## Linear
Not applicable: PR title is `fix`, not `feat`.

## Summary
- Add `AccountClient.exchangeFirebaseToken()` for account-service `/auth/exchange`.
- Send Firebase ID tokens through the expected `fb-token` bearer header.
- Cover successful exchange and non-2xx error behavior in auth-client tests.

## Test plan
- [x] `pnpm --filter @zooclaw/auth-client test`
- [x] `pnpm --filter @zooclaw/auth-client lint`

