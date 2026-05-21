---
title: "企业管理后台支持邮箱 OTP 登录（Phase C）"
type: "新功能上线"
priority: "中"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "6da1795172e4be665ffd5b7ff0b2018100d8d525"
pr: 1768
---
# 企业管理后台支持邮箱 OTP 登录（Phase C）

## 核心宣传点

企业管理后台现在支持通过邮箱一次性密码（OTP）登录，提升企业账户安全性和登录便利性。

## 原始内容

### Commit Message

```
feat(enterprise-admin): Phase C — email-OTP login + auth-client alignment (#1768)

## Summary

Phase C of the enterprise admin console plan. Wires up the real
email-OTP login flow on top of the Phase B shell, plus an alignment pass
on `@zooclaw/auth-client` after cross-referencing the iOS and web/app
reference implementations.

**Login + verify UI**
- `app/login/page.tsx` — email entry → `startLogin()` → `/verify`
- `app/verify/page.tsx` — 6-digit OTP → `completeLogin()` → `/`, with
60s resend cooldown that reuses `startLogin` (single source of truth for
"send OTP + persist pending")
- `app/(dashboard)/packs/page.tsx` + `app/(dashboard)/org/page.tsx` —
placeholder pages so the Sidebar links from PR #1761 no longer 404
- `test-utils/render.tsx` — `renderWithProviders` now wraps
`AuthProvider` so any consumer of `useAuth` works in tests without extra
wiring

**`/user/me` routing fixed**

`/user/me` lives on **account-service**, not claw-interface. Verified
against `web/app/src/lib/api/{token-verifier,config}.ts` and
`ios/.../AccountService.swift:105-161`. Previous Phase B implementation
incorrectly sent it to `NEXT_PUBLIC_CLAW_INTERFACE_URL`.

`lib/auth.ts` now does two parallel fetches inside `fetchUserMe()`:
- account-service `GET /user/me?business=ecap` → `AccountUser` (uid,
email, name)
- claw-interface `GET /v2/users/me` → `OrgMembership | null` (org_id,
name, org_type, role, computer_quota, status)

Composite shape changed from `{ user, org, role }` to `{ user,
membership }`. `useAuth()` still exposes `{ user, org, role }` on the
public side — all consumers (Sidebar, TopBar, layout guards, entry
redirect) are unchanged.

**`@zooclaw/auth-client` aligned with the real account-service
contract**

Cross-checked against iOS
(`Services/Authentication/AccountService.swift`) and web/app
(`src/lib/auth/api.ts`). Three fixes:

1. **`getUserMe(accessToken)` moved into AccountClient** — `/user/me` is
account-service plumbing, naturally belongs alongside `sendEmailOTP` /
`verifyEmailOTP`. Earlier "shared package must not call /user/me" rule
was written assuming /user/me lived on claw-interface — reverses cleanly
once we have the correct routing.
2. **`business` is a required config param** on `createAccountClient` —
all three endpoints append `?business=<encoded>`. Both iOS and web/app
append this on every account-service request; previous auth-client was
missing it on send + verify (would silently mis-scope).
3. **`UserTokenSchema` matches the real wire shape** — `{ access_token,
token_type: 'bearer', expires_in }`. Dropped required `uid` (server
returns it from `/user/me`, not the token endpoint) and unused optional
`refresh_token`. First real verify call would have zod-failed under the
old schema.

## Test plan

- [x] `pnpm --filter @zooclaw/auth-client run test` — 31/31 (added:
empty-business reject, URL-encoded business, token_type literal,
expires_in required, getUserMe happy/401/null-coerce/schema-miss)
- [x] `pnpm --filter @zooclaw/enterprise-admin run test` — 22/22 (login
submit/error, verify success + redirect-when-no-pending-otp, /user/me
401 from either service)
- [x] `pnpm exec tsc --noEmit` clean across both packages
- [x] `pnpm --filter @zooclaw/enterprise-admin run lint` clean
- [x] `pnpm --filter @zooclaw/enterprise-admin run build` — 8 static
routes prerender: /, /login, /verify, /onboarding, /users, /packs, /org,
/_not-found
- [ ] Manual smoke test against staging account-service (login → OTP →
dashboard)

## Next phases

D (Users) → E (Packs) → F (Org settings) → G (Onboarding) → H (Polish).
```

### PR Description

## Summary

Phase C of the enterprise admin console plan. Wires up the real email-OTP login flow on top of the Phase B shell, plus an alignment pass on `@zooclaw/auth-client` after cross-referencing the iOS and web/app reference implementations.

**Login + verify UI**
- `app/login/page.tsx` — email entry → `startLogin()` → `/verify`
- `app/verify/page.tsx` — 6-digit OTP → `completeLogin()` → `/`, with 60s resend cooldown that reuses `startLogin` (single source of truth for "send OTP + persist pending")
- `app/(dashboard)/packs/page.tsx` + `app/(dashboard)/org/page.tsx` — placeholder pages so the Sidebar links from PR #1761 no longer 404
- `test-utils/render.tsx` — `renderWithProviders` now wraps `AuthProvider` so any consumer of `useAuth` works in tests without extra wiring

**`/user/me` routing fixed**

`/user/me` lives on **account-service**, not claw-interface. Verified against `web/app/src/lib/api/{token-verifier,config}.ts` and `ios/.../AccountService.swift:105-161`. Previous Phase B implementation incorrectly sent it to `NEXT_PUBLIC_CLAW_INTERFACE_URL`.

`lib/auth.ts` now does two parallel fetches inside `fetchUserMe()`:
- account-service `GET /user/me?business=ecap` → `AccountUser` (uid, email, name)
- claw-interface `GET /v2/users/me` → `OrgMembership | null` (org_id, name, org_type, role, computer_quota, status)

Composite shape changed from `{ user, org, role }` to `{ user, membership }`. `useAuth()` still exposes `{ user, org, role }` on the public side — all consumers (Sidebar, TopBar, layout guards, entry redirect) are unchanged.

**`@zooclaw/auth-client` aligned with the real account-service contract**

Cross-checked against iOS (`Services/Authentication/AccountService.swift`) and web/app (`src/lib/auth/api.ts`). Three fixes:

1. **`getUserMe(accessToken)` moved into AccountClient** — `/user/me` is account-service plumbing, naturally belongs alongside `sendEmailOTP` / `verifyEmailOTP`. Earlier "shared package must not call /user/me" rule was written assuming /user/me lived on claw-interface — reverses cleanly once we have the correct routing.
2. **`business` is a required config param** on `createAccountClient` — all three endpoints append `?business=<encoded>`. Both iOS and web/app append this on every account-service request; previous auth-client was missing it on send + verify (would silently mis-scope).
3. **`UserTokenSchema` matches the real wire shape** — `{ access_token, token_type: 'bearer', expires_in }`. Dropped required `uid` (server returns it from `/user/me`, not the token endpoint) and unused optional `refresh_token`. First real verify call would have zod-failed under the old schema.

## Test plan

- [x] `pnpm --filter @zooclaw/auth-client run test` — 31/31 (added: empty-business reject, URL-encoded business, token_type literal, expires_in required, getUserMe happy/401/null-coerce/schema-miss)
- [x] `pnpm --filter @zooclaw/enterprise-admin run test` — 22/22 (login submit/error, verify success + redirect-when-no-pending-otp, /user/me 401 from either service)
- [x] `pnpm exec tsc --noEmit` clean across both packages
- [x] `pnpm --filter @zooclaw/enterprise-admin run lint` clean
- [x] `pnpm --filter @zooclaw/enterprise-admin run build` — 8 static routes prerender: /, /login, /verify, /onboarding, /users, /packs, /org, /_not-found
- [ ] Manual smoke test against staging account-service (login → OTP → dashboard)

## Next phases

D (Users) → E (Packs) → F (Org settings) → G (Onboarding) → H (Polish).
