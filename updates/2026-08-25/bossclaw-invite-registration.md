---
title: "BossClaw 注册改为邀请码准入：老账号手机/邮箱验证码直接登录，新用户先验邀请码"
type: "产品基础功能更新"
priority: "中"
date: "2026-08-25"
status: "待审核"
channels: ""
---

# BossClaw 注册改为邀请码准入：老账号手机/邮箱验证码直接登录，新用户先验邀请码

## 核心宣传点

BossClaw 的入口现在分成两条路：已经有 ZooClaw 账号的用户，直接用手机号或邮箱收验证码登录即可，不用再走一遍注册；全新用户则要先输入一张有效的邀请码才能开始注册。整个流程被拆成「填手机号/邮箱 → 验邀请码 → 收验证码 → 完成」四步，页面会先自动判断你这个号码或邮箱是不是老用户，再决定要不要拦你验邀请码，省掉了新老用户走错入口来回折腾。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `1a1a610960b7b4b5cd7c3834d18a83270df510b8`
- PR: #3513
- 作者: tim-srp
- 日期: 2026-08-25T12:31:41Z

### Commit Message

```
feat(bossclaw): add invite-gated registration flow (#3513)

## Summary

Implement invite-gated registration for BossClaw (design:
`docs/superpowers/specs/2026-08-25-bossclaw-invite-registration-design.md`):
existing ZooClaw accounts can sign in with email/phone OTP, while new
users must first validate an invitation code.

**Backend (`services/claw-interface`)**
- `subscription_code.py` — extract shared subscription-code validation
(`_assert_code_redeemable` / `check_subscription_code_usable`) reused by
the new read-only `POST /api/subscription-code/validate` endpoint
(request/response Pydantic schemas).
- `user_repo.py` — add `get_by_email` (normalized) and
`get_by_phone_number` lookups with a `gem_account` (profile store)
fallback when the `ecap-account` doc lacks top-level contact fields
(mirrors `knowledge_base._resolve_grantee_uid`: ambiguous or failing
lookups return `None`, never an arbitrary match). Adds non-unique
identifier indexes (log-only) plus
`profile_repo.find_uid_by_identifier`.
- `bossclaw.py` — new public `POST /api/bossclaw/account-status`
endpoint returning `{registered}` for email/phone identifiers (E.164
phone validation).

**Frontend (`web/app`)**
- `middleware.ts` — public-route allowlist for the two new endpoints.
- `services/boss.ts` — `checkBossclawAccountStatus` /
`validateSubscriptionCode` with fail-closed error mapping
(`SubscriptionCodeError`).
- `auth/manager.ts` — `loginExistingWithEmailOTP` plus a named
`loginWithSmsOTP` re-export for the login flow.
- `useBossclawLoginFlow` — four-step state machine hook (identifier →
invitation → verification → success) driving the render-only
`BossclawLoginClient` (4 screens).

## Test plan

- Backend: `env NODE_OPTIONS= bash scripts/verify-py.sh` — ruff +
pyright + import-linter 8/8 KEPT; branch test files 156 passed
(subscription_code, routes, bossclaw account-status, user_repo,
profile_repo, main_app).
- Frontend: `env NODE_OPTIONS= bash scripts/verify-web.sh` — full-app
tsc + vitest 9207 passed | 70 skipped | 1 todo + eslint clean.
- Manual: fresh phone/email → invitation-code gate; existing account
(incl. warm-pool-claimed, contact only in profile store) → OTP sign-in
with `registered: true`.

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Description

```
## Summary

Implement invite-gated registration for BossClaw (design: `docs/superpowers/specs/2026-08-25-bossclaw-invite-registration-design.md`): existing ZooClaw accounts can sign in with email/phone OTP, while new users must first validate an invitation code.

**Backend (`services/claw-interface`)**
- `subscription_code.py` — extract shared subscription-code validation (`_assert_code_redeemable` / `check_subscription_code_usable`) reused by the new read-only `POST /api/subscription-code/validate` endpoint (request/response Pydantic schemas).
- `user_repo.py` — add `get_by_email` (normalized) and `get_by_phone_number` lookups with a `gem_account` (profile store) fallback when the `ecap-account` doc lacks top-level contact fields (mirrors `knowledge_base._resolve_grantee_uid`: ambiguous or failing lookups return `None`, never an arbitrary match). Adds non-unique identifier indexes (log-only) plus `profile_repo.find_uid_by_identifier`.
- `bossclaw.py` — new public `POST /api/bossclaw/account-status` endpoint returning `{registered}` for email/phone identifiers (E.164 phone validation).

**Frontend (`web/app`)**
- `middleware.ts` — public-route allowlist for the two new endpoints.
- `services/boss.ts` — `checkBossclawAccountStatus` / `validateSubscriptionCode` with fail-closed error mapping (`SubscriptionCodeError`).
- `auth/manager.ts` — `loginExistingWithEmailOTP` plus a named `loginWithSmsOTP` re-export for the login flow.
- `useBossclawLoginFlow` — four-step state machine hook (identifier → invitation → verification → success) driving the render-only `BossclawLoginClient` (4 screens).

## Test plan

- Backend: `env NODE_OPTIONS= bash scripts/verify-py.sh` — ruff + pyright + import-linter 8/8 KEPT; branch test files 156 passed (subscription_code, routes, bossclaw account-status, user_repo, profile_repo, main_app).
- Frontend: `env NODE_OPTIONS= bash scripts/verify-web.sh` — full-app tsc + vitest 9207 passed | 70 skipped | 1 todo + eslint clean.
- Manual: fresh phone/email → invitation-code gate; existing account (incl. warm-pool-claimed, contact only in profile store) → OTP sign-in with `registered: true`.

```
