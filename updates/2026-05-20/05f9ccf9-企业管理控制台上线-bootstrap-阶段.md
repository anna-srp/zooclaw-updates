---
title: "企业管理控制台上线（Bootstrap 阶段）"
type: "新功能上线"
priority: "高"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "05f9ccf94dd8856cc02fd83aa2382aac46725db3"
pr: 1757
---
# 企业管理控制台上线（Bootstrap 阶段）

## 核心宣传点

企业管理控制台正式启动，企业客户现在有专属的管理界面来管理账户、用户和配置，为企业版全面开放打基础。

## 原始内容

### Commit Message

```
feat(web): Bootstrap enterprise admin console + auth-client package (#1757)

## Summary

- **Scaffold `@zooclaw/enterprise-admin`** — new Next.js 16 + OpenNext +
Cloudflare Workers app at `web/enterprise-admin/`, wired into the
workspace, CI code-quality gates, asset-size gates, lockfile-refresh,
auto-merge, and a deploy workflow.
- **Spec + implementation plan** for the Enterprise Admin Console
frontend at
`docs/superpowers/specs/2026-05-19-enterprise-admin-console-frontend.md`
and
`docs/superpowers/plans/2026-05-19-enterprise-admin-console-frontend.md`
(54 tasks, 8 phases, TDD-driven). Spec pivots from Firebase Auth to an
account-service bearer-token model and extracts a shared
`@zooclaw/auth-client` workspace package so neither deployable app
imports the other.
- **`@zooclaw/auth-client` foundation (Phase A1–A5)** — new
`web/packages/auth-client` workspace package with Vitest + jsdom, zod
schemas for account-service responses, token/pending-OTP/device-id
storage helpers, an injectable `getAccountBaseUrl()` (URL passed by the
consumer instead of reading env inside the package), and an ESLint flat
config so the package's `lint` script can run in CI.

Out of scope (follow-up PRs per the plan):
- Phase A6–A9: implement `sendEmailOTP` / `verifyEmailOTP` /
`getUserMe`, barrel finalization, migrate `web/app` consumers
- Phases B–H: Enterprise Admin app routes, components, hooks, polish,
deploy verification

## Test plan

- [x] `pnpm --filter @zooclaw/auth-client run test` — 15/15 passing
(types, storage, config)
- [x] `pnpm --filter @zooclaw/auth-client exec tsc --noEmit` — clean
- [x] `pnpm --filter @zooclaw/auth-client run lint` — zero warnings
- [ ] CI `code-quality / lint-and-test` passes on `web/**` changes
- [ ] CI `auto-review` passes
- [ ] No regressions in `@zooclaw/web-app` (no production code paths
touched yet)
```

### PR Description

## Summary

- **Scaffold `@zooclaw/enterprise-admin`** — new Next.js 16 + OpenNext + Cloudflare Workers app at `web/enterprise-admin/`, wired into the workspace, CI code-quality gates, asset-size gates, lockfile-refresh, auto-merge, and a deploy workflow.
- **Spec + implementation plan** for the Enterprise Admin Console frontend at `docs/superpowers/specs/2026-05-19-enterprise-admin-console-frontend.md` and `docs/superpowers/plans/2026-05-19-enterprise-admin-console-frontend.md` (54 tasks, 8 phases, TDD-driven). Spec pivots from Firebase Auth to an account-service bearer-token model and extracts a shared `@zooclaw/auth-client` workspace package so neither deployable app imports the other.
- **`@zooclaw/auth-client` foundation (Phase A1–A5)** — new `web/packages/auth-client` workspace package with Vitest + jsdom, zod schemas for account-service responses, token/pending-OTP/device-id storage helpers, an injectable `getAccountBaseUrl()` (URL passed by the consumer instead of reading env inside the package), and an ESLint flat config so the package's `lint` script can run in CI.

Out of scope (follow-up PRs per the plan):
- Phase A6–A9: implement `sendEmailOTP` / `verifyEmailOTP` / `getUserMe`, barrel finalization, migrate `web/app` consumers
- Phases B–H: Enterprise Admin app routes, components, hooks, polish, deploy verification

## Test plan

- [x] `pnpm --filter @zooclaw/auth-client run test` — 15/15 passing (types, storage, config)
- [x] `pnpm --filter @zooclaw/auth-client exec tsc --noEmit` — clean
- [x] `pnpm --filter @zooclaw/auth-client run lint` — zero warnings
- [ ] CI `code-quality / lint-and-test` passes on `web/**` changes
- [ ] CI `auto-review` passes
- [ ] No regressions in `@zooclaw/web-app` (no production code paths touched yet)
