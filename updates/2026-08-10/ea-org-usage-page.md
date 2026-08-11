---
title: "企业管理后台新增「用量」页，成员 Credits 消耗一目了然"
type: "新功能上线"
priority: "高"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 企业管理后台新增「用量」页，成员 Credits 消耗一目了然

## 核心宣传点

管理员可查看组织的余额、本周期已用量、订阅与充值钱包拆分，以及每位成员的已用/配额进度条，额度分配终于有据可依。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `63bc8b983d9d0f520435517e2e0bad39d4351feb`
- PR: #3315

### Commit Message

```
feat(enterprise-admin): add org usage page with per-member credits breakdown (#3315)

## Linear
<!-- no Linear issue for this feature -->

## Summary
- Add an admin-only **Usage** page to the enterprise-admin console
showing the current org's credit usage: balance, used-this-period,
subscription/topup wallet split, credit period range, and a per-member
usage table (used vs quota, progress bar, unlimited state,
`reset_pending` badge).
- Frontend-only: composes three existing claw-interface endpoints
through the claw proxy — `GET /users/credits/check` (org pool via
team-first resolution), `GET /orgs/{org_id}/users/llm-quotas`
(per-member used/quota + period bounds), and the org users list for the
uid→name/email join. No backend changes.
- Follows the app's MVVM contract: `page.tsx` renders purely from a
co-located `useUsageViewModel`; new `useCreditsCheckQuery` hook +
`types/credits.ts`; `formatCredits` helper; zh catalog entries for all
new copy.
- Access control: nav entry is `adminOnly`, and `/usage` is added to
`ADMIN_ONLY_PREFIXES` so non-admin members are redirected to `/users`.
- States: per-section loading skeletons, independent stats/members error
alerts, and a billing-not-ready notice for orgs without an initialized
billing profile (`billing_initialized: false` or backend 503
`billing_not_ready`).

Design spec:
`docs/superpowers/specs/2026-08-10-enterprise-admin-org-usage-page-design.md`
(included in this PR along with the implementation plan).

## Test plan
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm run lint` — clean (`--max-warnings=0`)
- [x] `pnpm run test:coverage` — 51 suites, 337 tests pass; new
co-located specs cover the credits hook (fetch URL + disabled states),
view model (wallet filtering, uid join, sort, quota/unlimited/pct,
billing-not-ready, independent errors), page rendering (cards, table,
skeletons, notices, alerts), sidebar visibility, and the `/usage` guard
redirect
- [ ] Staging smoke after web release: log in as a team-org admin, open
**Usage**, verify balance/used figures match `/users/credits` data and
the member table matches the Users page quota dialog
```

### PR Body

## Linear
<!-- no Linear issue for this feature -->

## Summary
- Add an admin-only **Usage** page to the enterprise-admin console showing the current org's credit usage: balance, used-this-period, subscription/topup wallet split, credit period range, and a per-member usage table (used vs quota, progress bar, unlimited state, `reset_pending` badge).
- Frontend-only: composes three existing claw-interface endpoints through the claw proxy — `GET /users/credits/check` (org pool via team-first resolution), `GET /orgs/{org_id}/users/llm-quotas` (per-member used/quota + period bounds), and the org users list for the uid→name/email join. No backend changes.
- Follows the app's MVVM contract: `page.tsx` renders purely from a co-located `useUsageViewModel`; new `useCreditsCheckQuery` hook + `types/credits.ts`; `formatCredits` helper; zh catalog entries for all new copy.
- Access control: nav entry is `adminOnly`, and `/usage` is added to `ADMIN_ONLY_PREFIXES` so non-admin members are redirected to `/users`.
- States: per-section loading skeletons, independent stats/members error alerts, and a billing-not-ready notice for orgs without an initialized billing profile (`billing_initialized: false` or backend 503 `billing_not_ready`).

Design spec: `docs/superpowers/specs/2026-08-10-enterprise-admin-org-usage-page-design.md` (included in this PR along with the implementation plan).

## Test plan
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm run lint` — clean (`--max-warnings=0`)
- [x] `pnpm run test:coverage` — 51 suites, 337 tests pass; new co-located specs cover the credits hook (fetch URL + disabled states), view model (wallet filtering, uid join, sort, quota/unlimited/pct, billing-not-ready, independent errors), page rendering (cards, table, skeletons, notices, alerts), sidebar visibility, and the `/usage` guard redirect
- [ ] Staging smoke after web release: log in as a team-org admin, open **Usage**, verify balance/used figures match `/users/credits` data and the member table matches the Users page quota dialog

