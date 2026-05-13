---
title: "修复深链进入时登录弹窗意外关闭的问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-12"
status: "待审核"
channels: ""
---

# 修复深链进入时登录弹窗意外关闭的问题

## 核心宣传点

通过带参数链接访问应用时，登录弹窗不再意外自动关闭，用户可以正常完成登录流程。

## 原始内容

**Commit:** `2026-05-12T12:37:39Z` by bill-srp
**SHA:** 0e081954ad8c229a1ea796676eda96076113ebf3
**PR:** #1600

### Commit Message

```
fix(web): normalize locale prefix in login modal pathname guard (#1600)

## Summary

Login modal opened by `LandingScreen` on unauth `/chat?sp=…` deep links
flashed closed because `usePathname()` oscillates between `/chat` and
`/{locale}/chat` during the middleware locale rewrite, and the existing
close-on-navigation guard in `LoginCheckProvider` only covered the `null
→ real` transition. The guard treated `/en/chat → /chat` as cross-route
navigation and closed the just-opened modal.

The reproduction is DevTools-sensitive: with DevTools closed (cache
enabled), the prefetched/cached JS path through the rewrite reliably
oscillates; with DevTools open + "Disable cache" enabled, the bug masks
because fresh chunks load past the race.

## Fix

Normalize both stored and incoming pathname via
`removeLocaleFromPathname` from `@/lib/i18n/config` before comparing —
locale-equivalent paths now compare equal, so the close only fires on
actual cross-route navigation.

## Test plan

- [x] 3 new regression tests in `LoginCheckProvider.unit.spec.tsx`:
- `does NOT close modal when pathname oscillates between /en/chat and
/chat (locale rewrite)`
- `does NOT close modal when pathname oscillates from /chat to /en/chat
(locale rewrite, reverse)`
- `closes modal on real navigation across distinct routes despite locale
prefix asymmetry` — pins the positive case so a future regression that
disables the close effect can't slip through
- [x] Existing 12 tests in the file remain green (15/15 total)
- [x] `pnpm lint` clean
- [x] `pnpm tsc --noEmit` clean
- [ ] Manual: visit `/chat?sp=test-id` logged out, modal stays open
- [ ] Manual: navigate `/canvas → /chat` while modal open, modal closes
(real navigation contract preserved)

## Related

Extends the guard introduced in #1020 (which fixed the `null → /en/chat`
half of the same bug class for `?agent_id=` deep links). PR #1020's
regression test left the `real → real` locale oscillation uncovered;
this PR closes that gap.
```

### PR Body

## Summary

Login modal opened by `LandingScreen` on unauth `/chat?sp=…` deep links flashed closed because `usePathname()` oscillates between `/chat` and `/{locale}/chat` during the middleware locale rewrite, and the existing close-on-navigation guard in `LoginCheckProvider` only covered the `null → real` transition. The guard treated `/en/chat → /chat` as cross-route navigation and closed the just-opened modal.

The reproduction is DevTools-sensitive: with DevTools closed (cache enabled), the prefetched/cached JS path through the rewrite reliably oscillates; with DevTools open + "Disable cache" enabled, the bug masks because fresh chunks load past the race.

## Fix

Normalize both stored and incoming pathname via `removeLocaleFromPathname` from `@/lib/i18n/config` before comparing — locale-equivalent paths now compare equal, so the close only fires on actual cross-route navigation.

## Test plan

- [x] 3 new regression tests in `LoginCheckProvider.unit.spec.tsx`:
  - `does NOT close modal when pathname oscillates between /en/chat and /chat (locale rewrite)`
  - `does NOT close modal when pathname oscillates from /chat to /en/chat (locale rewrite, reverse)`
  - `closes modal on real navigation across distinct routes despite locale prefix asymmetry` — pins the positive case so a future regression that disables the close effect can't slip through
- [x] Existing 12 tests in the file remain green (15/15 total)
- [x] `pnpm lint` clean
- [x] `pnpm tsc --noEmit` clean
- [ ] Manual: visit `/chat?sp=test-id` logged out, modal stays open
- [ ] Manual: navigate `/canvas → /chat` while modal open, modal closes (real navigation contract preserved)

## Related

Extends the guard introduced in #1020 (which fixed the `null → /en/chat` half of the same bug class for `?agent_id=` deep links). PR #1020's regression test left the `real → real` locale oscillation uncovered; this PR closes that gap.

