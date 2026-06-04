---
title: "新增 Agent Pack 管理后台（列表、CRUD、审核）"
type: "新功能上线"
priority: "高"
date: "2026-06-03"
status: "待审核"
channels: "站内弹窗, Use Case, Discord, changelog"
---
# 新增 Agent Pack 管理后台（列表、CRUD、审核）

## 核心宣传点

内部管理后台功能增强，提升 Agent 上架和审核效率。

## 原始内容

**Repo:** SerendipityOneInc/ecap-workspace  
**SHA:** `cfef79fea324aaf70d6d1ed0ebf2669bd6c7e3cd`  
**作者:** bill-srp  
**日期:** 2026-06-03T11:33:46Z  
**URL:** https://github.com/SerendipityOneInc/ecap-workspace/commit/cfef79fea324aaf70d6d1ed0ebf2669bd6c7e3cd

### Commit Message

```
feat(dashboard): agent packs admin — list, CRUD, submissions, claw API (#2189)

## Linear

https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

**PR 2 of 2** — the agent-packs feature, layered on the dashboard shell
merged in #2174.

- `/agent-packs` catalogue: list with create / edit / submit-version
flows (scrollable dialog editor), plus avatar + pack-archive upload (R2)
- `/agent-packs/:packId/submissions` history with approve / reject
actions
- Client-side data layer: a React Query hook fetching the claw-interface
`/internal/agent-packs` API directly from the browser
(`VITE_CLAW_INTERFACE_URL`, since the Worker is network-restricted),
plus the packs domain model and route view-models
- Feature UI primitives (`badge`, `card`, `dialog`, `table`) and 16 unit
tests (`packs`, `claw-url`)

Wires `QueryClientProvider`, the agent-packs routes, the sidebar nav
entry, and the home CTA into the shell. Validated by the
`dashboard-quality` CI job added in #2174.

## Known follow-ups (from ECA-886 / #2158 reviews)
- Backend CORS + admin auth on `/internal/agent-packs` — the
browser-direct fetch is currently unauthenticated. `TODO(ECA-886)`
- Real R2 upload — `r2-upload.ts` is still a mock. `TODO(ECA-886)`

## PR size
`size-override` applied (~3.4k lines). The feature shares one data layer
(`packs.ts` alone is 576 lines) so it can't be split under the 2000-line
gate without fragmenting a cohesive feature; a large share is vendored
shadcn primitives + tests.

## Test plan
- [x] dashboard `typecheck` passes (cf-typegen + react-router typegen +
`tsc -b`)
- [x] dashboard `test` — 16/16 pass
- [x] `pnpm install --frozen-lockfile` consistent
- [ ] CI green (`dashboard-quality` + `size-override`)
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

**PR 2 of 2** — the agent-packs feature, layered on the dashboard shell merged in #2174.

- `/agent-packs` catalogue: list with create / edit / submit-version flows (scrollable dialog editor), plus avatar + pack-archive upload (R2)
- `/agent-packs/:packId/submissions` history with approve / reject actions
- Client-side data layer: a React Query hook fetching the claw-interface `/internal/agent-packs` API directly from the browser (`VITE_CLAW_INTERFACE_URL`, since the Worker is network-restricted), plus the packs domain model and route view-models
- Feature UI primitives (`badge`, `card`, `dialog`, `table`) and 16 unit tests (`packs`, `claw-url`)

Wires `QueryClientProvider`, the agent-packs routes, the sidebar nav entry, and the home CTA into the shell. Validated by the `dashboard-quality` CI job added in #2174.

## Known follow-ups (from ECA-886 / #2158 reviews)
- Backend CORS + admin auth on `/internal/agent-packs` — the browser-direct fetch is currently unauthenticated. `TODO(ECA-886)`
- Real R2 upload — `r2-upload.ts` is still a mock. `TODO(ECA-886)`

## PR size
`size-override` applied (~3.4k lines). The feature shares one data layer (`packs.ts` alone is 576 lines) so it can't be split under the 2000-line gate without fragmenting a cohesive feature; a large share is vendored shadcn primitives + tests.

## Test plan
- [x] dashboard `typecheck` passes (cf-typegen + react-router typegen + `tsc -b`)
- [x] dashboard `test` — 16/16 pass
- [x] `pnpm install --frozen-lockfile` consistent
- [ ] CI green (`dashboard-quality` + `size-override`)

