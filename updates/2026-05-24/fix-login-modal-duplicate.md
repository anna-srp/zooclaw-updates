---
title: "修复已登录状态下登录弹窗重复弹出问题"
type: "Bug Fix"
priority: "高"
date: "2026-05-24"
status: "待审核"
channels: ""
---

# 修复已登录状态下登录弹窗重复弹出问题

## 核心宣传点

修复了用户已登录时仍会弹出登录框的 Bug，特别是 ECA-800 反馈的手机验证码登录后反复出现登录界面的问题。

## 原始内容

**Commit**: `d4ca757a336ebff479e506bc75d7a4fbfa8290d6`
**Title**: fix(web): guard login modal after auth (#1885)
**Author**: tim-srp
**Date**: 2026-05-24T10:36:39Z

**Commit Message**:
```
fix(web): guard login modal after auth (#1885)

## Summary
- Prevent the global login modal from opening after auth state is
already logged in
- Close any open login modal when `auth-state-changed` reports a
logged-in user
- Add regression coverage for both post-auth modal paths

## Verification
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/components/LoginCheckProvider.unit.spec.tsx`
- `pnpm --dir web/app exec eslint
src/components/providers/LoginCheckProvider.tsx
tests/unit/components/LoginCheckProvider.unit.spec.tsx --quiet`
- `pnpm --dir web run lint`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web run test:unit`

Note: `pnpm --dir web run tsc` currently fails before TypeScript starts
because the workspace script invokes `pnpm ... --if-present exec`, which
this local pnpm 10.26.2 rejects as `Unknown option: if-present`. I ran
the app-level `tsc --noEmit` check directly instead.


## Linear
- ECA-800:
https://linear.app/srpone/issue/ECA-800/bug-手机验证码登录后重复出现验证码输入框并进入-unable-to-connect-页面
```

**PR Description**:

## Summary
- Prevent the global login modal from opening after auth state is already logged in
- Close any open login modal when `auth-state-changed` reports a logged-in user
- Add regression coverage for both post-auth modal paths

## Verification
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/components/LoginCheckProvider.unit.spec.tsx`
- `pnpm --dir web/app exec eslint src/components/providers/LoginCheckProvider.tsx tests/unit/components/LoginCheckProvider.unit.spec.tsx --quiet`
- `pnpm --dir web run lint`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web run test:unit`

Note: `pnpm --dir web run tsc` currently fails before TypeScript starts because the workspace script invokes `pnpm ... --if-present exec`, which this local pnpm 10.26.2 rejects as `Unknown option: if-present`. I ran the app-level `tsc --noEmit` check directly instead.


## Linear
- ECA-800: https://linear.app/srpone/issue/ECA-800/bug-手机验证码登录后重复出现验证码输入框并进入-unable-to-connect-页面

