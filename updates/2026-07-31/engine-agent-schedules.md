---
title: "定时任务页面新增引擎 Agent 计划展示"
type: "产品基础功能更新"
priority: "中"
外部: "B"
date: "2026-07-31"
status: "待审核"
channels: ""
---

## 核心宣传点

/schedule 定时任务页现在把引擎 Agent（v2）的计划与原有 bot 定时任务合并展示：一个列表带 Agent 标识、创建/编辑表单支持选择 Agent，并按运行时提供对应操作。

## 原始内容

**feat(schedule): render engine-agent schedules alongside bot cron (#3174)**

- SHA: `6c6b050770b6dbe145aad997f5721d136cc15bf4`
- PR: #3174
- 日期: 2026-07-31T11:02:19Z

```
feat(schedule): render engine-agent schedules alongside bot cron (#3174)

## Summary

PR 2 of 2 implementing
`docs/superpowers/plans/2026-07-30-schedule-v2-frontend.md` (spec merged
in #3151; backend API merged in #3164). Renders engine-agent (v2)
schedules on the `/schedule` page alongside the untouched v1 bot cron:
one merged list with per-row agent badges, an agent selector in the
create/edit form, and per-runtime row actions. v1 flows (REST reads via
`/openclaw/cron/*`, WebSocket `cron.*` writes, historical-ghost merge)
are byte-for-byte unchanged — every pre-existing schedule test stays
green.

Commits map to plan tasks (B3–B5 share the same page files, so they land
as one integration commit):

- **B1** `src/models/agent-schedule.ts` +
`src/services/agent-schedules.ts` — wire types and data access over the
generic claw proxy (no BFF route).
- **B2** `src/hooks/queries/agent-schedules/` —
`useEngineSchedules(uid)`: meta query (`listAgentsMeta` surfaces
`agents_v2_enabled` via a service-local type; the shared
`OpenClawAgentListResponse` model is untouched) → per-agent fan-out.
`enabled` is scope-gated (`!!uid && storage uid matches`) with the
post-await re-check as second layer; scope-aborts are excluded from
`failedAgentNames`; `metaFailed` + `refetchMeta` keep a failed
agents-list distinct from "zero engine agents".
- **B3–B5** schedule page integration — engine rows merged via explicit
`runtime`/`workspaceId`/`engineScheduleId` fields (no id parsing; the
namespaced id is only a React key), agent badges, `jobsLoading` folds in
engine loading, the full-page `computerReady` gate applies only to
pure-v1 accounts (with engine agents the page renders and v1 shows an
inline status notice; empty states suppressed while v1 is unread),
`scheduleUnmappable` rows are excluded from day/week projections and
listed read-only ("Unsupported schedule"), engine targets render only
the round-trippable form fields (name/schedule/message/enabled), engine
mutations go through REST with list-key invalidation, run history uses
limit-grow paging (no offset upstream) and refreshes the open panel
after Run-now. Codex additionally hardened races its own review found:
latest-request-wins for the runs panel and runtime-scoped busy/edit
identities.
- **B6 (step 1)** mock backend — `scripts/mock-backend/schedules.mjs`
route module with in-memory mutations (list reflects CUD),
duplicate/reserved-name responses matching the merged backend contract,
seeded into `ready-user` with one engine agent owning cron + every
schedules.

Backend contract deviations from the original plan are honored:
duplicate names surface the 409 `schedule.conflict` message through the
existing `formError` path (no client-side suffixing), and create/update
responses are full projections, so `schedule: null` genuinely means an
unmappable upstream spec.

## Test plan
- [x] Full local gate `bash scripts/verify-web.sh`: 7 CI guards, tsc,
**7,779 vitest tests across 570 files**, eslint — all green
- [x] Coverage ratchet holds: statements 88.65 (floor 83) / branches
81.92 (75) / functions 87.43 (81) / lines 91 (85)
- [x] New suites: services 4, hooks 15, engine-rows + CronClient 85,
form-target 48, row-actions 18, mock handlers 59
- [ ] Staging smoke (after backend staging deploy — the engine Schedules
API is only Temporal-wired in staging): create / toggle / trigger /
delete one engine schedule end-to-end from the UI
- Browser validation against the local mock stack was intentionally
skipped (owner decision); the staging smoke above covers the live path
before release.
```
