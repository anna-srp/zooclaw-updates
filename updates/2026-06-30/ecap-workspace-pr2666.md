---
title: "企业管理后台登录流程更稳（OTP 验证码登录修复）"
type: "Bug Fix"
priority: "中"
date: "2026-06-30"
status: "待审核"
channels: ""
---
# 企业管理后台登录流程更稳（OTP 验证码登录修复）
## 核心宣传点
企业管理后台用验证码登录时更稳定，已注册用户不再被误当成新用户重复注册，也不会在验证后被莫名弹回登录页。
## 原始内容
fix(enterprise-admin): stabilize otp login flow (#2666)

## Summary
- Check `/account/me` after OTP verification so existing
enterprise-admin users do not re-register `/account/team-org`.
- Stop `/verify` from using render-time pending OTP state as a redirect
guard; missing OTP state now surfaces as an inline submit-time error
instead of bouncing to `/login`.
- Update verify/auth tests around existing accounts and the
no-login-bounce behavior.

## Root cause
`completeLogin()` previously called `/account/team-org` unconditionally
after OTP verification, so already registered users hit
`account.already_exists`.

Separately, `/verify` read pending OTP state from localStorage during
render and redirected to `/login` whenever it was absent. Successful
verification clears that pending state before navigation completes, so a
later render could briefly observe `pending=null`, route back to the
email form, and then continue into the app.

## Test plan
- [x] `git diff --check`
- [x] `bash scripts/verify-changed.sh` (no locally verifiable surface
for `web/enterprise-admin`; CI covers it)
- [ ] `pnpm --dir web/enterprise-admin test --
app/verify/__tests__/verify.test.tsx lib/__tests__/auth.test.ts`
(blocked before Vitest by local pnpm install/status check:
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`)

---

### PR Description

## Summary
- Check `/account/me` after OTP verification so existing enterprise-admin users do not re-register `/account/team-org`.
- Stop `/verify` from using render-time pending OTP state as a redirect guard; missing OTP state now surfaces as an inline submit-time error instead of bouncing to `/login`.
- Update verify/auth tests around existing accounts and the no-login-bounce behavior.

## Root cause
`completeLogin()` previously called `/account/team-org` unconditionally after OTP verification, so already registered users hit `account.already_exists`.

Separately, `/verify` read pending OTP state from localStorage during render and redirected to `/login` whenever it was absent. Successful verification clears that pending state before navigation completes, so a later render could briefly observe `pending=null`, route back to the email form, and then continue into the app.

## Test plan
- [x] `git diff --check`
- [x] `bash scripts/verify-changed.sh` (no locally verifiable surface for `web/enterprise-admin`; CI covers it)
- [ ] `pnpm --dir web/enterprise-admin test -- app/verify/__tests__/verify.test.tsx lib/__tests__/auth.test.ts` (blocked before Vitest by local pnpm install/status check: `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`)

