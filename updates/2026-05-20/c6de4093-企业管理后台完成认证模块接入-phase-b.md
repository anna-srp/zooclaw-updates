---
title: "企业管理后台完成认证模块接入（Phase B）"
type: "新功能上线"
priority: "中"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "c6de4093fff7b180e957fce2cd40942a0b561906"
pr: 1761
---
# 企业管理后台完成认证模块接入（Phase B）

## 核心宣传点

企业管理后台完成身份验证模块搭建，为企业用户安全访问管理功能提供基础。

## 原始内容

### Commit Message

```
feat(enterprise-admin): Add Phase B shell, types, and auth wiring (#1761)

## Summary

Phase B of the enterprise admin console plan ([merged in
#1757](https://github.com/SerendipityOneInc/ecap-workspace/pull/1757);
Phase A auth-client foundation merged in #1759). Lands the buildable
shell for `web/enterprise-admin/` plus a couple of
`@zooclaw/auth-client` refinements that surfaced during implementation.

**What's now in place**

- Runtime deps + workspace wiring: `@zooclaw/auth-client` (workspace
dep), TanStack Query, zod, shadcn (radix-ui meta + 11 copy-paste
components in `components/ui/`), lucide icons, tailwind-merge/clsx/cva.
Workspace root scripts switched to `pnpm -r --if-present` recursion so
every package participates in lint/test/tsc/build.
- Domain types under `types/` — Org, OrgUser, Pack, PackSubmission,
PackVersion, Paginated, plus `UserMe` (moved out of the shared package
per spec §9.2).
- `lib/api.ts` — fetch wrapper around `NEXT_PUBLIC_CLAW_INTERFACE_URL`,
auto-attaches the stored bearer, throws typed `ApiError` on non-2xx.
- `lib/auth.ts` — `startLogin` / `completeLogin` / `loadCurrentUser` /
`logout` composing `@zooclaw/auth-client` primitives with
`api('/user/me')` for the backend's current-user composition.
- `hooks/useAuth.tsx` — `AuthProvider` backed by TanStack Query (avoids
Next 16's `react-hooks/set-state-in-effect` rule). Exposes `{ user, org,
role, isLoading, error, refresh, signOut }`.
- App shell — `app/providers.tsx`, `app/layout.tsx`, `app/page.tsx`
(entry redirect), `app/error.tsx` (global boundary, 401 → /login),
`(dashboard)/layout.tsx` with route guards,
`components/layout/Sidebar.tsx` + `TopBar.tsx`.

**Refinements to `@zooclaw/auth-client`**

- New `AccountServiceError extends Error` with `.status` and `.code` so
callers branch on HTTP status rather than regex-matching messages.
- Removed `getUserMe` + `UserMeSchema` from the shared package. Per spec
§9.2 "must not call GET /user/me; those are product/backend composition
steps owned by each app." Each consuming app composes its own
current-user lookup. Spec contradiction fixed.
- Bumped to zod ^4 to align with enterprise-admin and avoid a v3/v4
schema-composition type mismatch when consumers re-use
`AccountUserSchema`.

**Layout choice**

`web/enterprise-admin/` does **not** use `src/` (`app/`, `components/`,
`lib/`, etc. live at the project root). Diverges from `web/app`'s
convention but greenfield apps get the flatter layout — only four config
touchpoints affected (tsconfig paths, vitest alias/include,
components.json css path, lint script).

**In-tree code-review pass**

After writing the shell, I ran a security + quality review on the diff.
One MEDIUM finding fixed in the final commit: `AuthProvider` was
silently swallowing non-401 errors from `loadCurrentUser`, making
backend outages look identical to "logged out" and triggering a useless
redirect to `/login`. Now there's a three-state auth UI (loading / error
/ not-authenticated) — error state renders a "Couldn't load your
session" panel with a Retry button instead of bouncing the user.

## Test plan

- [x] `pnpm --filter @zooclaw/auth-client run test` — 23/23 passing (4
files)
- [x] `pnpm --filter @zooclaw/enterprise-admin run test` — 16/16 passing
(2 files: api + auth glue)
- [x] `pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit` —
clean
- [x] `pnpm run lint` (recursive workspace lint) — clean across web-app,
auth-client, enterprise-admin
- [x] `pnpm --filter @zooclaw/enterprise-admin run build` — production
OpenNext build succeeds
- [x] `pnpm dev:enterprise` boots and `GET /` returns 200 (entry page
renders, then client-side redirects to `/login` which 404s — Phase C
will add that page)
- [ ] CI `code-quality / lint-and-test`
- [ ] CI `auto-review` + `codex-review`
- [ ] Apply `size-override` label (PR exceeds the 2000-line cap due to
shadcn copy-paste + plan amendment)

**Out of scope (deferred per plan):**
- Phase C: `/login` + `/verify` pages
- Phase D-G: users / packs / org / onboarding modules
- Phase H: component tests for the shell (route-guard test, RTL coverage
of Sidebar/TopBar)
- `web/app` migration to consume `@zooclaw/auth-client` (Task A8 skipped
— see plan; revisit when web/app's account-service protocol next
changes)
```

### PR Description

## Summary

Phase B of the enterprise admin console plan ([merged in #1757](https://github.com/SerendipityOneInc/ecap-workspace/pull/1757); Phase A auth-client foundation merged in #1759). Lands the buildable shell for `web/enterprise-admin/` plus a couple of `@zooclaw/auth-client` refinements that surfaced during implementation.

**What's now in place**

- Runtime deps + workspace wiring: `@zooclaw/auth-client` (workspace dep), TanStack Query, zod, shadcn (radix-ui meta + 11 copy-paste components in `components/ui/`), lucide icons, tailwind-merge/clsx/cva. Workspace root scripts switched to `pnpm -r --if-present` recursion so every package participates in lint/test/tsc/build.
- Domain types under `types/` — Org, OrgUser, Pack, PackSubmission, PackVersion, Paginated, plus `UserMe` (moved out of the shared package per spec §9.2).
- `lib/api.ts` — fetch wrapper around `NEXT_PUBLIC_CLAW_INTERFACE_URL`, auto-attaches the stored bearer, throws typed `ApiError` on non-2xx.
- `lib/auth.ts` — `startLogin` / `completeLogin` / `loadCurrentUser` / `logout` composing `@zooclaw/auth-client` primitives with `api('/user/me')` for the backend's current-user composition.
- `hooks/useAuth.tsx` — `AuthProvider` backed by TanStack Query (avoids Next 16's `react-hooks/set-state-in-effect` rule). Exposes `{ user, org, role, isLoading, error, refresh, signOut }`.
- App shell — `app/providers.tsx`, `app/layout.tsx`, `app/page.tsx` (entry redirect), `app/error.tsx` (global boundary, 401 → /login), `(dashboard)/layout.tsx` with route guards, `components/layout/Sidebar.tsx` + `TopBar.tsx`.

**Refinements to `@zooclaw/auth-client`**

- New `AccountServiceError extends Error` with `.status` and `.code` so callers branch on HTTP status rather than regex-matching messages.
- Removed `getUserMe` + `UserMeSchema` from the shared package. Per spec §9.2 "must not call GET /user/me; those are product/backend composition steps owned by each app." Each consuming app composes its own current-user lookup. Spec contradiction fixed.
- Bumped to zod ^4 to align with enterprise-admin and avoid a v3/v4 schema-composition type mismatch when consumers re-use `AccountUserSchema`.

**Layout choice**

`web/enterprise-admin/` does **not** use `src/` (`app/`, `components/`, `lib/`, etc. live at the project root). Diverges from `web/app`'s convention but greenfield apps get the flatter layout — only four config touchpoints affected (tsconfig paths, vitest alias/include, components.json css path, lint script).

**In-tree code-review pass**

After writing the shell, I ran a security + quality review on the diff. One MEDIUM finding fixed in the final commit: `AuthProvider` was silently swallowing non-401 errors from `loadCurrentUser`, making backend outages look identical to "logged out" and triggering a useless redirect to `/login`. Now there's a three-state auth UI (loading / error / not-authenticated) — error state renders a "Couldn't load your session" panel with a Retry button instead of bouncing the user.

## Test plan

- [x] `pnpm --filter @zooclaw/auth-client run test` — 23/23 passing (4 files)
- [x] `pnpm --filter @zooclaw/enterprise-admin run test` — 16/16 passing (2 files: api + auth glue)
- [x] `pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit` — clean
- [x] `pnpm run lint` (recursive workspace lint) — clean across web-app, auth-client, enterprise-admin
- [x] `pnpm --filter @zooclaw/enterprise-admin run build` — production OpenNext build succeeds
- [x] `pnpm dev:enterprise` boots and `GET /` returns 200 (entry page renders, then client-side redirects to `/login` which 404s — Phase C will add that page)
- [ ] CI `code-quality / lint-and-test`
- [ ] CI `auto-review` + `codex-review`
- [ ] Apply `size-override` label (PR exceeds the 2000-line cap due to shadcn copy-paste + plan amendment)

**Out of scope (deferred per plan):**
- Phase C: `/login` + `/verify` pages
- Phase D-G: users / packs / org / onboarding modules
- Phase H: component tests for the shell (route-guard test, RTL coverage of Sidebar/TopBar)
- `web/app` migration to consume `@zooclaw/auth-client` (Task A8 skipped — see plan; revisit when web/app's account-service protocol next changes)
