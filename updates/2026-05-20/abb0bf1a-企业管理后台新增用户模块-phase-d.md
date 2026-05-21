---
title: "企业管理后台新增用户模块（Phase D）"
type: "新功能上线"
priority: "中"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "abb0bf1ade36f58ded418aea04d3fd25290993ee"
pr: 1772
---
# 企业管理后台新增用户模块（Phase D）

## 核心宣传点

企业管理员可在后台查看和管理组织成员，支持用户列表展示和详情查看。

## 原始内容

### Commit Message

```
feat(enterprise-admin): Phase D Users module + MVVM refactor (#1772)

## Linear


https://linear.app/srpone/issue/ECA-749/admin-console-web-phase-1-users-module

## Backend dependency

This PR wires the Users module frontend against the `claw-interface`
endpoints listed in section 6.5 of the implementation spec:
- `GET /orgs/{orgId}/users` (paginated, with `status` + `role` filters)
- `POST /orgs/{orgId}/invite`
- `POST /orgs/{orgId}/users/{uid}/{suspend,resume,remove}`

These endpoints are not yet implemented in `services/claw-interface`
(Phase 1 backend #1748 shipped only Org CRUD). The frontend will 404 at
runtime until a corresponding backend phase lands. The codex-review bot
correctly flags this — it is expected per the phased rollout.

The `/users` route is admin-only (gated by `(dashboard)/layout.tsx`
route guards) so non-admin users cannot reach it. The Sidebar entry is
visible to all members but clicking through it will hit the same backend
404 until the corresponding backend phase ships.

## Summary

Phase D of the enterprise admin console: the Users module + an MVVM
refactor across all existing pages + three HIGH-severity fixes from
in-tree code review.

### Phase D — Users module
- `hooks/useUsers.ts` — `useUsersQuery` + `useInviteUserMutation` /
`useSuspendUserMutation` / `useResumeUserMutation` /
`useRemoveUserMutation`. Partial-key invalidation (`["users", orgId]`)
so a single mutation refreshes every active filter/page combo.
`placeholderData: keepPreviousData` keeps the previous page visible
during transitions (proper pagination UX, no flicker).
- `components/users/UserTable.tsx` — Name / Email / Role / Status /
Quota / Actions columns. Status badges (Active=green, Pending=amber,
Suspended=red). Skeleton loading rows. Empty state distinguishes _no
users yet_ from _no users match filters_.
- `components/users/UserActions.tsx` — status-aware admin-only Suspend /
Resume / Remove. Hidden entirely for `role=user`. Self-actions disabled.
- `components/users/InviteDialog.tsx` — email / role (native `<select>`)
/ quota form. 30-day expiration note. Server error rendered inline.
- `app/(dashboard)/users/page.tsx` — server-side pagination (25/50/100),
status filter (All/Active/Pending/Suspended), role filter
(All/Admin/User). Filter changes reset to page 1.

### MVVM refactor
All routable client components hold only JSX + Tailwind classes; state,
effects, derived values, and handlers live in a co-located
`useXxxViewModel` hook. Applied to:
- `app/(dashboard)/users/` → `useUsersViewModel`
- `app/login/` → `useLoginViewModel`
- `app/verify/` → `useVerifyViewModel`
- `app/` (entry redirect) → `useEntryViewModel`
- `app/(dashboard)/layout.tsx` → `useDashboardLayoutViewModel` (with
discriminated `state: "loading" | "error" | "ready"` for clean
three-state rendering)

The convention is documented in user memory so future phases follow it
without re-litigation.

### Code-review HIGH fixes (applied in this PR)
1. **URL encoding** (`hooks/useUsers.ts`): `encodeURIComponent` for
`orgId` and `uid` in every users endpoint — defense-in-depth against
`OrgMembershipSchema.org_id` accepting arbitrary strings.
2. **Remove confirmation** (`components/users/UserActions.tsx` + new
`components/ui/alert-dialog.tsx`): Remove now opens a Radix
`AlertDialog` requiring explicit confirmation; previously a single
misclick was destructive.
3. **Surface mutation errors** (`useUsersViewModel.ts` +
`users/page.tsx`): suspend / resume / remove failures were silently
swallowed; now expose `actionError` and `dismissActionError()` from the
VM, rendered as a dismissable `role="alert"` banner.

### Deferred follow-ups (MEDIUM)
- A11y `aria-live` / `aria-describedby` on form errors in Login / Verify
/ InviteDialog.
- `signOut()` should call `queryClient.clear()` (cache hygiene; not
exploitable today since orgIds change per session).
- Double-submit `useRef` guard in Login / Verify.
- `orgId as string` cast in `useUsersQuery` queryFn → tighten to
`skipToken` or runtime guard.

## Test plan

- [x] `pnpm test` — 57/57 passing (26 new tests across hook / 3
component / 2 page / 1 VM unit files)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; `/users` route prerendered as static content
- [ ] Manual: sign in as admin → /users renders members; filters reset
to page 1 on change; Invite opens dialog; Remove requires confirm;
failed mutation shows banner with Dismiss
- [ ] Manual: sign in as `role=user` → no Invite button, no action
column
- [ ] Manual: pagination Next/Previous clamps correctly (no flicker
thanks to keepPreviousData)
```

### PR Description

## Linear

https://linear.app/srpone/issue/ECA-749/admin-console-web-phase-1-users-module

## Backend dependency

This PR wires the Users module frontend against the `claw-interface` endpoints listed in section 6.5 of the implementation spec:
- `GET /orgs/{orgId}/users` (paginated, with `status` + `role` filters)
- `POST /orgs/{orgId}/invite`
- `POST /orgs/{orgId}/users/{uid}/{suspend,resume,remove}`

These endpoints are not yet implemented in `services/claw-interface` (Phase 1 backend #1748 shipped only Org CRUD). The frontend will 404 at runtime until a corresponding backend phase lands. The codex-review bot correctly flags this — it is expected per the phased rollout.

The `/users` route is admin-only (gated by `(dashboard)/layout.tsx` route guards) so non-admin users cannot reach it. The Sidebar entry is visible to all members but clicking through it will hit the same backend 404 until the corresponding backend phase ships.

## Summary

Phase D of the enterprise admin console: the Users module + an MVVM refactor across all existing pages + three HIGH-severity fixes from in-tree code review.

### Phase D — Users module
- `hooks/useUsers.ts` — `useUsersQuery` + `useInviteUserMutation` / `useSuspendUserMutation` / `useResumeUserMutation` / `useRemoveUserMutation`. Partial-key invalidation (`["users", orgId]`) so a single mutation refreshes every active filter/page combo. `placeholderData: keepPreviousData` keeps the previous page visible during transitions (proper pagination UX, no flicker).
- `components/users/UserTable.tsx` — Name / Email / Role / Status / Quota / Actions columns. Status badges (Active=green, Pending=amber, Suspended=red). Skeleton loading rows. Empty state distinguishes _no users yet_ from _no users match filters_.
- `components/users/UserActions.tsx` — status-aware admin-only Suspend / Resume / Remove. Hidden entirely for `role=user`. Self-actions disabled.
- `components/users/InviteDialog.tsx` — email / role (native `<select>`) / quota form. 30-day expiration note. Server error rendered inline.
- `app/(dashboard)/users/page.tsx` — server-side pagination (25/50/100), status filter (All/Active/Pending/Suspended), role filter (All/Admin/User). Filter changes reset to page 1.

### MVVM refactor
All routable client components hold only JSX + Tailwind classes; state, effects, derived values, and handlers live in a co-located `useXxxViewModel` hook. Applied to:
- `app/(dashboard)/users/` → `useUsersViewModel`
- `app/login/` → `useLoginViewModel`
- `app/verify/` → `useVerifyViewModel`
- `app/` (entry redirect) → `useEntryViewModel`
- `app/(dashboard)/layout.tsx` → `useDashboardLayoutViewModel` (with discriminated `state: "loading" | "error" | "ready"` for clean three-state rendering)

The convention is documented in user memory so future phases follow it without re-litigation.

### Code-review HIGH fixes (applied in this PR)
1. **URL encoding** (`hooks/useUsers.ts`): `encodeURIComponent` for `orgId` and `uid` in every users endpoint — defense-in-depth against `OrgMembershipSchema.org_id` accepting arbitrary strings.
2. **Remove confirmation** (`components/users/UserActions.tsx` + new `components/ui/alert-dialog.tsx`): Remove now opens a Radix `AlertDialog` requiring explicit confirmation; previously a single misclick was destructive.
3. **Surface mutation errors** (`useUsersViewModel.ts` + `users/page.tsx`): suspend / resume / remove failures were silently swallowed; now expose `actionError` and `dismissActionError()` from the VM, rendered as a dismissable `role="alert"` banner.

### Deferred follow-ups (MEDIUM)
- A11y `aria-live` / `aria-describedby` on form errors in Login / Verify / InviteDialog.
- `signOut()` should call `queryClient.clear()` (cache hygiene; not exploitable today since orgIds change per session).
- Double-submit `useRef` guard in Login / Verify.
- `orgId as string` cast in `useUsersQuery` queryFn → tighten to `skipToken` or runtime guard.

## Test plan

- [x] `pnpm test` — 57/57 passing (26 new tests across hook / 3 component / 2 page / 1 VM unit files)
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm build` — clean; `/users` route prerendered as static content
- [ ] Manual: sign in as admin → /users renders members; filters reset to page 1 on change; Invite opens dialog; Remove requires confirm; failed mutation shows banner with Dismiss
- [ ] Manual: sign in as `role=user` → no Invite button, no action column
- [ ] Manual: pagination Next/Previous clamps correctly (no flicker thanks to keepPreviousData)


