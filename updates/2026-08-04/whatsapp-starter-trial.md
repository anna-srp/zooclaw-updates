---
title: "WhatsApp 新用户绑定即送 500 积分 7 天试用"
type: "新功能上线"
priority: "高"
date: "2026-08-04"
status: "待审核"
channels: ""
commit: "140138d97ef299cf6c0c175546e27d6dfa43b605"
repo: "SerendipityOneInc/ecap-workspace"
---

## 核心宣传点

新用户首次绑定 WhatsApp 即自动获得 7 天 500 积分的免费试用，绑定即用，零门槛体验 ZooClaw 全部能力；曾付费后过期的用户也可获得，作为回流福利。

## 原始内容

```
feat(whatsapp): grant 500-credit starter trial to new WhatsApp-bound users (#3218)

## Summary
- Users receive a **7-day starter trial with 500 credits** on their
**first genuine WhatsApp bind**. The grant fires in `POST
/whatsapp/users/bind` — a route authenticated with the connector service
token that only the WhatsApp bridge holds, and which the bridge only
calls while processing a real inbound WhatsApp message. Caller-supplied
registration metadata can no longer mint credits (addresses the review's
forgery finding).
- `whatsapp_repo.bind_user` now returns `(binding, freshly_bound)`: the
flag is true only for the atomic `pending_binding → bound` transition,
so Meta webhook replays and idempotent re-binds never re-evaluate the
grant. The entitlement operation key `trial:whatsapp_bind:{uid}` and the
deterministic billing-gateway transaction id remain the second lock.
- Eligibility (owner-confirmed, identical to the long-standing
invite-trial recipient set): no prior trial of any kind, current billing
status `free` or `expired`, zero subscription wallet balance. `expired`
deliberately includes lapsed ex-paying users — the grant doubles as a
win-back incentive. At most once per user for life (the unique bound-uid
index means a user can only ever complete one WhatsApp bind, and the
trial operation key is per-uid).
- Reuses the invite-trial machinery: `grant_trial_credits_if_eligible`
gained keyword-only `trial_key` / `credits` / `duration_days` /
`actor_id` (defaults preserve the legacy invite flow byte-for-byte). New
constants `WHATSAPP_BIND_TRIAL_CREDITS = 500`,
`WHATSAPP_BIND_TRIAL_DURATION_DAYS = 7` (either ≤ 0 disables).
- Grant is best-effort and fail-closed: a billing-gateway failure logs
with context, never fails the bind response (no Meta webhook retry
storms), and deliberately leaves the recorded trial row consuming the
one-trial slot — repair is the manual admin grant flow (comment at call
site + contract tests).

## Review history
- Cross-flow double-grant race with the invite trial: resolved by
product fact — the invite-bind route has no callers (dead surface);
whatsapp_bind is the sole live onboarding-trial writer. If invite
binding is ever revived, re-establish a uid-level unique invariant first
(reference implementation in 9b72b868f, deliberately reverted in
79fbc79fa).
- Forgeable registration metadata (grant under user bearer token): fixed
in c773ff7cb by moving the grant behind the bridge-authenticated bind
step as described above.

## Test plan
- [x] TDD: repo contract tests for `(binding, freshly_bound)` (fresh
transition / idempotent replay / failure); service tests: fresh bind
grants with exact whatsapp kwargs, idempotent re-bind never grants,
grant failure leaves the bind response unchanged; trial-service tests
for generalized params, invite defaults, disable switches, fail-closed
(no entitlement mutation on billing-gateway failure)
- [x] `pytest` on touched files — 139 passed
- [x] `bash scripts/verify-py.sh` — ruff, ruff format, pyright,
import-linter green
- [x] Pre-commit + pre-push hook gates passed

## Deployment
Backend-only (`services/claw-interface`); no bridge or web changes.
Requires Billing Gateway reachable (same dependency as the invite
trial).

---

### PR Body

## Summary
- Users receive a **7-day starter trial with 500 credits** on their **first genuine WhatsApp bind**. The grant fires in `POST /whatsapp/users/bind` — a route authenticated with the connector service token that only the WhatsApp bridge holds, and which the bridge only calls while processing a real inbound WhatsApp message. Caller-supplied registration metadata can no longer mint credits (addresses the review's forgery finding).
- `whatsapp_repo.bind_user` now returns `(binding, freshly_bound)`: the flag is true only for the atomic `pending_binding → bound` transition, so Meta webhook replays and idempotent re-binds never re-evaluate the grant. The entitlement operation key `trial:whatsapp_bind:{uid}` and the deterministic billing-gateway transaction id remain the second lock.
- Eligibility (owner-confirmed, identical to the long-standing invite-trial recipient set): no prior trial of any kind, current billing status `free` or `expired`, zero subscription wallet balance. `expired` deliberately includes lapsed ex-paying users — the grant doubles as a win-back incentive. At most once per user for life (the unique bound-uid index means a user can only ever complete one WhatsApp bind, and the trial operation key is per-uid).
- Reuses the invite-trial machinery: `grant_trial_credits_if_eligible` gained keyword-only `trial_key` / `credits` / `duration_days` / `actor_id` (defaults preserve the legacy invite flow byte-for-byte). New constants `WHATSAPP_BIND_TRIAL_CREDITS = 500`, `WHATSAPP_BIND_TRIAL_DURATION_DAYS = 7` (either ≤ 0 disables).
- Grant is best-effort and fail-closed: a billing-gateway failure logs with context, never fails the bind response (no Meta webhook retry storms), and deliberately leaves the recorded trial row consuming the one-trial slot — repair is the manual admin grant flow (comment at call site + contract tests).

## Review history
- Cross-flow double-grant race with the invite trial: resolved by product fact — the invite-bind route has no callers (dead surface); whatsapp_bind is the sole live onboarding-trial writer. If invite binding is ever revived, re-establish a uid-level unique invariant first (reference implementation in 9b72b868f, deliberately reverted in 79fbc79fa).
- Forgeable registration metadata (grant under user bearer token): fixed in c773ff7cb by moving the grant behind the bridge-authenticated bind step as described above.

## Test plan
- [x] TDD: repo contract tests for `(binding, freshly_bound)` (fresh transition / idempotent replay / failure); service tests: fresh bind grants with exact whatsapp kwargs, idempotent re-bind never grants, grant failure leaves the bind response unchanged; trial-service tests for generalized params, invite defaults, disable switches, fail-closed (no entitlement mutation on billing-gateway failure)
- [x] `pytest` on touched files — 139 passed
- [x] `bash scripts/verify-py.sh` — ruff, ruff format, pyright, import-linter green
- [x] Pre-commit + pre-push hook gates passed

## Deployment
Backend-only (`services/claw-interface`); no bridge or web changes. Requires Billing Gateway reachable (same dependency as the invite trial).

```
