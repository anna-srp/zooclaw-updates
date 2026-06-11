---
title: "Google 登录新增人机验证"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# Google 登录新增人机验证

## 核心宣传点
Google 登录入口新增人机验证（Turnstile），加强对恶意注册和滥用的防护，提升账号安全。

## 原始内容
```
fix(auth): add Turnstile to ECAP Google login (#2339)

## Summary
- add a Cloudflare Turnstile widget to the ECAP Google login entry point
- pass optional Turnstile captcha data through loginUser and
/auth/exchange
- keep email/phone login behavior unchanged; Turnstile is enabled only
by NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED and
NEXT_PUBLIC_TURNSTILE_SITE_KEY

## Root cause
Google login did not send a human-verification signal to
account-service, so the backend Turnstile + new-user rate-limit
protection could not be enforced from the ECAP frontend.

## Test plan
- [x] pnpm vitest run tests/unit/lib/auth/api.unit.spec.ts
tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/components/LoginForm.unit.spec.tsx
- [x] pnpm exec tsc --noEmit
- [x] pnpm exec eslint src/lib/auth/captcha.ts
src/components/TurnstileWidget.tsx src/lib/auth/api.ts
src/lib/auth/manager.ts src/components/LoginForm.tsx
tests/unit/lib/auth/api.unit.spec.ts
tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/components/LoginForm.unit.spec.tsx --quiet --cache
--cache-location .eslintcache --cache-strategy content
- [x] pnpm lint

---

### PR Description

## Summary
- add a Cloudflare Turnstile widget to the ECAP Google login entry point
- pass optional Turnstile captcha data through loginUser and /auth/exchange
- keep email/phone login behavior unchanged; Turnstile is enabled only by NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED and NEXT_PUBLIC_TURNSTILE_SITE_KEY

## Root cause
Google login did not send a human-verification signal to account-service, so the backend Turnstile + new-user rate-limit protection could not be enforced from the ECAP frontend.

## Test plan
- [x] pnpm vitest run tests/unit/lib/auth/api.unit.spec.ts tests/unit/lib/auth/manager.unit.spec.ts tests/unit/components/LoginForm.unit.spec.tsx
- [x] pnpm exec tsc --noEmit
- [x] pnpm exec eslint src/lib/auth/captcha.ts src/components/TurnstileWidget.tsx src/lib/auth/api.ts src/lib/auth/manager.ts src/components/LoginForm.tsx tests/unit/lib/auth/api.unit.spec.ts tests/unit/lib/auth/manager.unit.spec.ts tests/unit/components/LoginForm.unit.spec.tsx --quiet --cache --cache-location .eslintcache --cache-strategy content
- [x] pnpm lint
```
