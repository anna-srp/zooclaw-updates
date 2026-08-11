---
title: "企业管理后台：用量页可直接编辑成员 AI 额度"
type: "体验优化"
priority: "中"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 企业管理后台：用量页可直接编辑成员 AI 额度

## 核心宣传点

管理员在「用量」页看到某位成员额度吃紧时，可以就地点笔形图标改额度，不必再跳回用户页。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `03545f57cb2d9376f3ffadc9c877fce642aaf9e1`
- PR: #3316

### Commit Message

```
feat(enterprise-admin): edit member AI quotas from the usage page (#3316)

## Linear
<!-- no Linear issue for this feature -->

## Summary
- Let org admins edit a member's AI-credit quota directly from the
**Usage** page (follow-up to #3315), reusing the exact editing flow from
the Users page.
- Extracts the quota-dialog logic (state, validation, submit with toast,
per-row retryable issues, `reset_pending` retry) out of
`useUsersViewModel` into a shared `hooks/useQuotaEditor.ts`; the Users
view model now delegates to it with its **public contract unchanged** —
the Users page component and all its existing tests pass unmodified,
which is the regression proof for the extraction.
- `useUsageViewModel` composes the editor and exposes `openQuotaForRow`
(resolves the full org user for a row; rows without an active org user
are a no-op); `MemberUsageTable` gains a per-row pencil action plus a
Retry affordance on rows with a quota issue; the page renders the shared
`QuotaDialog`.
- The existing mutation's invalidation of `["member-llm-quotas", orgId]`
already refreshes both pages' tables — no new cache wiring. No backend
changes.

Design spec:
`docs/superpowers/specs/2026-08-10-usage-page-quota-edit-design.md`
(committed here with the implementation plan).

## Test plan
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm run lint` — clean (`--max-warnings=0`)
- [x] Full vitest suite — 352/352 pass (14 new: 9 `useQuotaEditor` hook
cases, 2 usage view-model cases, 3 usage page cases)
- [x] Changed-file allow-list verified: no Users page/component/test
files modified — only `useUsersViewModel.ts` internals
- [ ] Staging smoke after web release: as a team-org admin, edit a quota
from the Usage page, confirm the Users page quota dialog shows the same
value, and retry a `reset_pending` row
```

### PR Body

## Linear
<!-- no Linear issue for this feature -->

## Summary
- Let org admins edit a member's AI-credit quota directly from the **Usage** page (follow-up to #3315), reusing the exact editing flow from the Users page.
- Extracts the quota-dialog logic (state, validation, submit with toast, per-row retryable issues, `reset_pending` retry) out of `useUsersViewModel` into a shared `hooks/useQuotaEditor.ts`; the Users view model now delegates to it with its **public contract unchanged** — the Users page component and all its existing tests pass unmodified, which is the regression proof for the extraction.
- `useUsageViewModel` composes the editor and exposes `openQuotaForRow` (resolves the full org user for a row; rows without an active org user are a no-op); `MemberUsageTable` gains a per-row pencil action plus a Retry affordance on rows with a quota issue; the page renders the shared `QuotaDialog`.
- The existing mutation's invalidation of `["member-llm-quotas", orgId]` already refreshes both pages' tables — no new cache wiring. No backend changes.

Design spec: `docs/superpowers/specs/2026-08-10-usage-page-quota-edit-design.md` (committed here with the implementation plan).

## Test plan
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm run lint` — clean (`--max-warnings=0`)
- [x] Full vitest suite — 352/352 pass (14 new: 9 `useQuotaEditor` hook cases, 2 usage view-model cases, 3 usage page cases)
- [x] Changed-file allow-list verified: no Users page/component/test files modified — only `useUsersViewModel.ts` internals
- [ ] Staging smoke after web release: as a team-org admin, edit a quota from the Usage page, confirm the Users page quota dialog shows the same value, and retry a `reset_pending` row

