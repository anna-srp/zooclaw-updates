---
title: "修复登录问题：Google / 手机号登录不再被邮箱验证码拦住"
type: "Bug Fix"
priority: "高"
date: "2026-07-20"
status: "待审核"
channels: ""
---

## 核心宣传点

此前登录页的人机验证会误挡住 Google 和手机号登录，导致按钮看似可点却无反应。现在验证码只作用于邮箱验证码登录，Google 和手机号登录可直接进行，登录更顺畅。

### 原始内容

**Commit message:**

```
fix(auth): scope login captcha to email (#2970)

## Summary

- scope the shared login Turnstile challenge to email OTP only
- let Google and phone authentication proceed without forwarding or
persisting the email captcha token
- keep Firebase phone reCAPTCHA intact and add regressions for both
login layouts, widget lifecycle, and phone OTP exchange

## Root cause

`LoginForm` treated one Turnstile token as a prerequisite for Google,
phone, and email login. Google and phone buttons looked enabled, but
their click handlers returned before starting authentication while the
challenge was unresolved. Those flows also forwarded the shared token
through `/auth/exchange`, coupling unrelated login methods to the email
OTP protection.

This change gives the captcha an email-only state and visual boundary.
It removes the Google/phone token handoffs, keeps the email OTP payload
unchanged, and ignores script-load failures that arrive after the widget
has unmounted.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/src/components/LoginForm.tsx
web/app/src/components/TurnstileWidget.tsx
'web/app/src/app/[locale]/(app)/user/verify/page.tsx'
web/app/src/lib/auth/captcha.ts
web/app/tests/unit/components/LoginForm.unit.spec.tsx
web/app/tests/unit/components/TurnstileWidget.unit.spec.tsx
web/app/tests/unit/app/user-verify-phone.unit.spec.tsx` — 12 files, 178
tests; TypeScript, ESLint, and frontend guards passed
- [x] `bash scripts/verify-changed.sh`
- [x] pre-push PR size and changed-surface gates
- [x] regression test observed RED before the stale Turnstile callback
guard and GREEN afterward

## Known limitation

This PR intentionally does not change
`SerendipityOneInc/user-interface`. Environments that still enforce
Turnstile for Google or phone `/auth/exchange` require separate backend
configuration or implementation coordination before deploying this
frontend behavior.
```

**PR body:**

## Summary

- scope the shared login Turnstile challenge to email OTP only
- let Google and phone authentication proceed without forwarding or persisting the email captcha token
- keep Firebase phone reCAPTCHA intact and add regressions for both login layouts, widget lifecycle, and phone OTP exchange

## Root cause

`LoginForm` treated one Turnstile token as a prerequisite for Google, phone, and email login. Google and phone buttons looked enabled, but their click handlers returned before starting authentication while the challenge was unresolved. Those flows also forwarded the shared token through `/auth/exchange`, coupling unrelated login methods to the email OTP protection.

This change gives the captcha an email-only state and visual boundary. It removes the Google/phone token handoffs, keeps the email OTP payload unchanged, and ignores script-load failures that arrive after the widget has unmounted.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/src/components/LoginForm.tsx web/app/src/components/TurnstileWidget.tsx 'web/app/src/app/[locale]/(app)/user/verify/page.tsx' web/app/src/lib/auth/captcha.ts web/app/tests/unit/components/LoginForm.unit.spec.tsx web/app/tests/unit/components/TurnstileWidget.unit.spec.tsx web/app/tests/unit/app/user-verify-phone.unit.spec.tsx` — 12 files, 178 tests; TypeScript, ESLint, and frontend guards passed
- [x] `bash scripts/verify-changed.sh`
- [x] pre-push PR size and changed-surface gates
- [x] regression test observed RED before the stale Turnstile callback guard and GREEN afterward

## Known limitation

This PR intentionally does not change `SerendipityOneInc/user-interface`. Environments that still enforce Turnstile for Google or phone `/auth/exchange` require separate backend configuration or implementation coordination before deploying this frontend behavior.

