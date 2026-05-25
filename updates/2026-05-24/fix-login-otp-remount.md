---
title: "修复手机/邮箱验证码登录后页面闪烁问题"
type: "Bug Fix"
priority: "高"
date: "2026-05-24"
status: "待审核"
channels: ""
---

# 修复手机/邮箱验证码登录后页面闪烁问题

## 核心宣传点

修复了登录时验证码输入框在完成登录后短暂重新弹出的问题，登录流程更流畅稳定。

## 原始内容

**Commit**: `f6c87a4b589539f8d0975ba3737ed87a42aad3c2`
**Title**: fix(web): avoid premature email OTP auth event (#1895)
**Author**: tim-srp
**Date**: 2026-05-24T16:49:13Z

**Commit Message**:
```
fix(web): avoid premature email OTP auth event (#1895)

## Summary
- Prevent email OTP login from dispatching `auth-state-changed` before
`_completeLogin` finishes.
- Add a regression test that holds `/users/create` pending and asserts
no auth event fires mid-login.

## Why
The email OTP verification screen could briefly remount with an empty
code input while login was still loading because global auth listeners
reacted to token-only user state before `getUserMe` and
business/onboarding sync completed.

## Verification
- `pnpm run test:unit tests/unit/lib/auth/manager.unit.spec.ts`
- `pnpm run test:unit tests/unit/components/LoginForm.unit.spec.tsx
tests/unit/components/LoginCheckProvider.unit.spec.tsx`
- `pnpm exec eslint src/lib/auth/manager.ts
tests/unit/lib/auth/manager.unit.spec.ts --quiet`
- `pnpm run lint`
```

**PR Description**:

## Summary
- Prevent email OTP login from dispatching `auth-state-changed` before `_completeLogin` finishes.
- Add a regression test that holds `/users/create` pending and asserts no auth event fires mid-login.

## Why
The email OTP verification screen could briefly remount with an empty code input while login was still loading because global auth listeners reacted to token-only user state before `getUserMe` and business/onboarding sync completed.

## Verification
- `pnpm run test:unit tests/unit/lib/auth/manager.unit.spec.ts`
- `pnpm run test:unit tests/unit/components/LoginForm.unit.spec.tsx tests/unit/components/LoginCheckProvider.unit.spec.tsx`
- `pnpm exec eslint src/lib/auth/manager.ts tests/unit/lib/auth/manager.unit.spec.ts --quiet`
- `pnpm run lint`
