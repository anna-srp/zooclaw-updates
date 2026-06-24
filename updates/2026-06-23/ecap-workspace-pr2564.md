---
title: "恢复邮箱验证码登录入口"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-23"
status: "待审核"
channels: ""
---
# 恢复邮箱验证码登录入口

## 核心宣传点
登录页重新提供「使用邮箱继续」入口，可直接用邮箱验证码登录，无需再走隐藏链接。

## 原始内容
```
fix(web): restore email otp login captcha (#2564)

## Summary
- Restore the email OTP login entrypoint and remove the extra
`showEmailLogin` URL/prop gate.
- Gate `Continue with Email` behind the shared login Turnstile challenge
and forward captcha fields through the email OTP send BFF to
account-service.
- Rename the public login captcha flag to
`NEXT_PUBLIC_ECAP_LOGIN_CAPTCHA_REQUIRED` and update docs/workflow
wiring.

## Root cause
Email OTP login was still implemented, but `LoginModal` hid the
entrypoint behind `?email_login=1`. The existing Turnstile wiring only
covered Google/phone and used a Google-specific public flag name.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web exec tsc --noEmit --project app/tsconfig.json`
- [x] `pnpm --filter @zooclaw/web-app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`

Note: `pnpm --dir web run tsc` currently fails before typechecking
because the workspace script expands to `pnpm -r
--workspace-concurrency=1 --if-present exec tsc --noEmit`, and this pnpm
version rejects `--if-present` for `exec`. The CI workflow uses `tsc
--noEmit --project app/tsconfig.json`, which passes locally.
```

### PR description
## Summary
- Restore the email OTP login entrypoint and remove the extra `showEmailLogin` URL/prop gate.
- Gate `Continue with Email` behind the shared login Turnstile challenge and forward captcha fields through the email OTP send BFF to account-service.
- Rename the public login captcha flag to `NEXT_PUBLIC_ECAP_LOGIN_CAPTCHA_REQUIRED` and update docs/workflow wiring.

## Root cause
Email OTP login was still implemented, but `LoginModal` hid the entrypoint behind `?email_login=1`. The existing Turnstile wiring only covered Google/phone and used a Google-specific public flag name.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web exec tsc --noEmit --project app/tsconfig.json`
- [x] `pnpm --filter @zooclaw/web-app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`

Note: `pnpm --dir web run tsc` currently fails before typechecking because the workspace script expands to `pnpm -r --workspace-concurrency=1 --if-present exec tsc --noEmit`, and this pnpm version rejects `--if-present` for `exec`. The CI workflow uses `tsc --noEmit --project app/tsconfig.json`, which passes locally.
