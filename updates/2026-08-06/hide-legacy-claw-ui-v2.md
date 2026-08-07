---
title: "V2 用户界面清理：不再显示已失效的旧版 Claw 控件"
type: "体验优化"
priority: "中"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

已迁移到 V2（Engine 运行时）的账号，不会再看到断连的旧版 Claw 连接状态、状态页、会话页和统计面板，渠道页也只展示当前可用的平台，界面不再有无效入口和闪烁。

## 原始内容

**fix(web): hide all legacy Claw UI after V2 migration (#3273)**

- sha: `0e2b9ca8f56a1784d5d2d984f8b3c50270d92879`
- PR: #3273

```
fix(web): hide all legacy Claw UI after V2 migration (#3273)

## Summary

- hide the shared legacy Claw connection status on every authenticated
page once canonical Main uses the Engine runtime
- resolve runtime ownership once in the persistent app layout so
page-header remounts do not refetch `/agents` or flicker for legacy
users
- keep failed ownership lookups in an explicit unknown state instead of
falling back to legacy UI
- show only Engine-configurable Channel platforms after migration while
preserving every legacy platform before migration

## Root cause

The first V2 migration cleanup only hid Claw status and operational
pages in Channel and Settings. Other pages still rendered the shared
`ClawPageHeader`, whose legacy connection control had no migration-aware
ownership gate.

A first follow-up placed ownership resolution inside each page header.
Because the unified agents query deliberately revalidates on mount, that
approach added a request on route changes and temporarily hid then
restored the status for unmigrated users. It also treated a terminal
agents-query error as confirmed legacy ownership.

This change moves the ownership observer to the persistent authenticated
app layout and exposes a narrow context to all headers. Ownership is now
`unknown`, `legacy`, or `engine`; legacy controls render only after
legacy ownership is positively confirmed.

## Performance

- native V2 users still short-circuit from the Engine onboarding
snapshot without an agents request
- existing accounts use one app-layout ownership observer rather than
one observer per page header
- page navigation no longer causes header-owned `/agents` revalidation
or connection-status flicker
- Channel retains its feature-specific agents observer because it needs
the actual Engine workspace list; concurrent initial observers share the
same React Query request

## Test plan

- [x] `bash scripts/verify-web.sh <19 changed frontend paths>` after
merging current `origin/main`
- [x] 19 targeted test files: 237 passed, 66 existing skips
- [x] `bash scripts/verify-changed.sh`
- [x] TypeScript, ESLint, import-boundary, dead-code, and diff checks
- [x] full Vitest run: 8298 passed; two unrelated concurrent
timeout/hydration failures passed when rerun independently (48/48 and
8/8)
```

**PR Body:**

## Summary

- hide the shared legacy Claw connection status on every authenticated page once canonical Main uses the Engine runtime
- resolve runtime ownership once in the persistent app layout so page-header remounts do not refetch `/agents` or flicker for legacy users
- keep failed ownership lookups in an explicit unknown state instead of falling back to legacy UI
- show only Engine-configurable Channel platforms after migration while preserving every legacy platform before migration

## Root cause

The first V2 migration cleanup only hid Claw status and operational pages in Channel and Settings. Other pages still rendered the shared `ClawPageHeader`, whose legacy connection control had no migration-aware ownership gate.

A first follow-up placed ownership resolution inside each page header. Because the unified agents query deliberately revalidates on mount, that approach added a request on route changes and temporarily hid then restored the status for unmigrated users. It also treated a terminal agents-query error as confirmed legacy ownership.

This change moves the ownership observer to the persistent authenticated app layout and exposes a narrow context to all headers. Ownership is now `unknown`, `legacy`, or `engine`; legacy controls render only after legacy ownership is positively confirmed.

## Performance

- native V2 users still short-circuit from the Engine onboarding snapshot without an agents request
- existing accounts use one app-layout ownership observer rather than one observer per page header
- page navigation no longer causes header-owned `/agents` revalidation or connection-status flicker
- Channel retains its feature-specific agents observer because it needs the actual Engine workspace list; concurrent initial observers share the same React Query request

## Test plan

- [x] `bash scripts/verify-web.sh <19 changed frontend paths>` after merging current `origin/main`
- [x] 19 targeted test files: 237 passed, 66 existing skips
- [x] `bash scripts/verify-changed.sh`
- [x] TypeScript, ESLint, import-boundary, dead-code, and diff checks
- [x] full Vitest run: 8298 passed; two unrelated concurrent timeout/hydration failures passed when rerun independently (48/48 and 8/8)


---

**fix(web): hide legacy Claw surfaces for V2 users (#3268)**

- sha: `89350c6f4f689e0a980cec2c34446d593f02089e`
- PR: #3268

```
fix(web): hide legacy Claw surfaces for V2 users (#3268)

## Summary
- detect Claw-independent accounts from the uid-scoped Engine onboarding
state or a freshly revalidated canonical Main Engine agent
- hide the legacy Claw connection control on Channel and Settings, and
remove Status, Sessions, and Statistics Dashboard for V2 users
- keep Engine channel management available without synthetic Claw
targets, start warnings, restart prompts, or legacy settings/runtime
requests
- preserve Usage plan allocation while disabling and masking legacy Claw
resource data, including cached values

## Root cause
Channel and Settings mounted legacy Claw state and operational pages
unconditionally. The UI did not distinguish native or migrated Engine
accounts from accounts whose canonical Main agent still uses the
computer runtime, so V2 users saw disconnected Claw controls and could
trigger legacy runtime/settings requests.

## Performance
- native Engine Settings short-circuits without an ownership agent
request
- Channel reuses one unified agent query instead of mounting a second
agent-list observer
- no polling was added; legacy settings, computer, init, and resource
queries remain disabled for Claw-independent accounts

## Test plan
- [x] `bash scripts/verify-web.sh <16 changed frontend paths>`
- [x] TypeScript and ESLint
- [x] 16 targeted test files: 308 passed, 66 existing skips
- [x] `bash scripts/verify-changed.sh` after merging current
`origin/main`
- [x] local code review, including a regression test for non-empty
cached Claw resources in Engine mode
```

**PR Body:**

## Summary
- detect Claw-independent accounts from the uid-scoped Engine onboarding state or a freshly revalidated canonical Main Engine agent
- hide the legacy Claw connection control on Channel and Settings, and remove Status, Sessions, and Statistics Dashboard for V2 users
- keep Engine channel management available without synthetic Claw targets, start warnings, restart prompts, or legacy settings/runtime requests
- preserve Usage plan allocation while disabling and masking legacy Claw resource data, including cached values

## Root cause
Channel and Settings mounted legacy Claw state and operational pages unconditionally. The UI did not distinguish native or migrated Engine accounts from accounts whose canonical Main agent still uses the computer runtime, so V2 users saw disconnected Claw controls and could trigger legacy runtime/settings requests.

## Performance
- native Engine Settings short-circuits without an ownership agent request
- Channel reuses one unified agent query instead of mounting a second agent-list observer
- no polling was added; legacy settings, computer, init, and resource queries remain disabled for Claw-independent accounts

## Test plan
- [x] `bash scripts/verify-web.sh <16 changed frontend paths>`
- [x] TypeScript and ESLint
- [x] 16 targeted test files: 308 passed, 66 existing skips
- [x] `bash scripts/verify-changed.sh` after merging current `origin/main`
- [x] local code review, including a regression test for non-empty cached Claw resources in Engine mode

