---
title: "手机号登录新增人机验证，防止短信轰炸"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 手机号登录新增人机验证，防止短信轰炸

## 核心宣传点
手机号登录新增了人机验证（Turnstile），有效防止恶意短信轰炸，提升账号登录的安全性。

## 原始内容
```
fix(auth): add Turnstile to ECAP phone login (#2352)

## Summary
- Extends Cloudflare Turnstile (added to Google login in #2339) to
phone-number login. Same env flag
`NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED` gates both — email OTP
is intentionally excluded.
- Gate is at `handlePhoneSubmit` (before SMS send), not after OTP verify
— adds a user-visible captcha layer on top of Firebase's invisible
reCAPTCHA so SMS bombing through our UI requires solving Turnstile per
attempt. Solved token is stashed in
`sessionStorage['ecap:phone-login:captcha-token']` and forwarded to
`loginUser → /auth/exchange` on the verify page, mirroring the mobile
Google-redirect pattern.
- Backend support already in user-interface `v0.6.5-release` (PR
`SerendipityOneInc/user-interface#124`, deployed to production today).

## Root cause
The phone-login surface previously had **no user-visible captcha** —
only Firebase's invisible reCAPTCHA on `sendSMSVerification`, which
protects Firebase but not our `/auth/exchange` backend, and not against
SMS bombing where attackers iterate phone numbers through our login
page. PR #2339 closed this gap for Google login; this PR closes it for
phone.

Also fixes a #983-style half-login bug on `/user/verify` (phone branch):
`saveLoginInfo` ran **before** `loginUser`, so a thrown exchange would
leave a Firebase profile in `localStorage` with no backend session.
Adding captcha makes `loginUser` more likely to fail in production
(expired single-use Turnstile token, etc.), so this reorder ships
together. The same bug pattern on the email-magic-link path is left for
a separate PR — out of scope here.

## Test plan
- [x] `pnpm tsc --noEmit` — only stale `.next/types/validator.ts` cache
errors, none from touched source.
- [x] `pnpm eslint <touched files>` — clean.
- [x] `pnpm vitest run tests/unit/components/LoginForm.unit.spec.tsx` —
48/48 pass (44 existing + 4 new phone-captcha cases: flag-off baseline,
unsolved token blocks SMS, solved token persisted, Firebase error wipes
token + resets widget).
- [ ] Local manual smoke with mock backend + Cloudflare test sitekey
(`1x00000000000000000000AA`): walk phone login end-to-end on desktop +
mobile UA, confirm captcha required → SMS sent → exchange carries
`captcha_token`.
- [ ] Staging: backend flag off, frontend flag on — phone login should
succeed with `captcha_token` visible in `/auth/exchange` payload and
backend should ignore it (gradual rollout step 2 of the spec).
- [ ] After staging green: turn on backend
`ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED=true` per spec step 3 (covers both
Google + phone).

## Spec
docs/superpowers/specs/2026-06-10-ecap-phone-login-turnstile.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

---

### PR Description

## Summary
- Extends Cloudflare Turnstile (added to Google login in #2339) to phone-number login. Same env flag `NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED` gates both — email OTP is intentionally excluded.
- Gate is at `handlePhoneSubmit` (before SMS send), not after OTP verify — adds a user-visible captcha layer on top of Firebase's invisible reCAPTCHA so SMS bombing through our UI requires solving Turnstile per attempt. Solved token is stashed in `sessionStorage['ecap:phone-login:captcha-token']` and forwarded to `loginUser → /auth/exchange` on the verify page, mirroring the mobile Google-redirect pattern.
- Backend support already in user-interface `v0.6.5-release` (PR `SerendipityOneInc/user-interface#124`, deployed to production today).

## Root cause
The phone-login surface previously had **no user-visible captcha** — only Firebase's invisible reCAPTCHA on `sendSMSVerification`, which protects Firebase but not our `/auth/exchange` backend, and not against SMS bombing where attackers iterate phone numbers through our login page. PR #2339 closed this gap for Google login; this PR closes it for phone.

Also fixes a #983-style half-login bug on `/user/verify` (phone branch): `saveLoginInfo` ran **before** `loginUser`, so a thrown exchange would leave a Firebase profile in `localStorage` with no backend session. Adding captcha makes `loginUser` more likely to fail in production (expired single-use Turnstile token, etc.), so this reorder ships together. The same bug pattern on the email-magic-link path is left for a separate PR — out of scope here.

## Test plan
- [x] `pnpm tsc --noEmit` — only stale `.next/types/validator.ts` cache errors, none from touched source.
- [x] `pnpm eslint <touched files>` — clean.
- [x] `pnpm vitest run tests/unit/components/LoginForm.unit.spec.tsx` — 48/48 pass (44 existing + 4 new phone-captcha cases: flag-off baseline, unsolved token blocks SMS, solved token persisted, Firebase error wipes token + resets widget).
- [ ] Local manual smoke with mock backend + Cloudflare test sitekey (`1x00000000000000000000AA`): walk phone login end-to-end on desktop + mobile UA, confirm captcha required → SMS sent → exchange carries `captcha_token`.
- [ ] Staging: backend flag off, frontend flag on — phone login should succeed with `captcha_token` visible in `/auth/exchange` payload and backend should ignore it (gradual rollout step 2 of the spec).
- [ ] After staging green: turn on backend `ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED=true` per spec step 3 (covers both Google + phone).

## Spec
docs/superpowers/specs/2026-06-10-ecap-phone-login-turnstile.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```
