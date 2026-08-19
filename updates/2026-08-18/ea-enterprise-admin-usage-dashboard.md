---
title: "企业管理后台「用量」页升级：趋势图表、日期区间筛选、批量配额管理"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-18"
status: "待审核"
channels: ""
---

# 企业管理后台「用量」页升级：趋势图表、日期区间筛选、批量配额管理

## 核心宣传点

企业管理员现在能看到组织用量趋势图（24 小时 / 7 天 / 30 天预设 + 日历自定义区间）、按模型的 Top5 消耗拆分，以及成员用量管理：支持搜索、超额/接近超额筛选、排序、CSV 导出，还能多选成员一次性批量设置 AI 配额，失败行可重试。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `6682311863ebc73a3a815f959f077cd61c082652`
- PR: #3397
- 作者: david-srp
- 日期: 2026-08-18T02:28:30Z

### Commit Message

```
feat(enterprise-admin): org usage dashboard with trend analytics, calendar range picker, and bulk quota management (#3397)

## Linear
<!-- 无关联 issue -->

## Summary

Rebuild the enterprise-admin `/usage` page into a full org usage
dashboard + member usage management surface. **Frontend-only** — zero
`services/claw-interface` changes; every panel runs on existing
endpoints (design spec:
`docs/superpowers/specs/2026-08-14-enterprise-admin-usage-dashboard.md`).

**Org usage analytics (new)**
- Usage trend card: recharts daily/10-minute bar chart with 24h / 7d /
30d presets **plus a calendar date-range picker** (react-day-picker +
Radix Popover, zc theming) — custom ranges are client-side slices of the
30d daily dataset, bounded to the last 30 days; Credits / Requests /
Peak-window KPIs recompute per selection; truncation (`meta.truncated`)
surfaces as a banner; range switches dim stale data (keepPreviousData)
- Usage-by-model card: top-5 split with share bars, credits, requests
- Data source: the existing self-scoped `GET
/users/credits/usage/records` — team-first billing resolution means an
org admin's own call already returns org-wide aggregates
- Each section labels its time scope (trend = selected range, models =
fetched window, member table = current credit period) since the date
filter can only govern the trend card

**Member usage management (new)**
- Search (name/email/uid), filters (over quota / near quota ≥80% /
unlimited / no usage), column sorting, share-of-spend column,
near/over-quota badges, client-side pagination
- CSV export of the filtered view (RFC 4180 quoting + formula-injection
guard + UTF-8 BOM)
- **Bulk AI-quota apply**: multi-select rows → one dialog applies the
same limit sequentially via the existing single-member endpoint, with
progress and failed-row retry
- LLM-only scope footnote (member usage excludes search/video drawn from
the org wallet)

**Structure**: strict MVVM (`useUsageViewModel` owns all
state/derivation); new reusable primitives `Popover`, `DateRangePicker`;
new hooks `useUsageRecords`, `useBulkQuota`; `lib/csv`,
`lib/local-date`; chart tokens `--color-chart-1..5` aligned with
dashboard-console; full zh catalog coverage; `/usage` TopBar title fix.
New deps: `recharts@3.9.2` (exact pin matching web/app),
`react-day-picker@^9.14.0`.

**Known limits (by existing API contract, documented in the spec)**: no
token totals, no billing-period range, no period-over-period deltas,
model split capped at top-5 and not sliceable by custom dates, member
usage is a current-period scalar (no history — upstream ECA-1352).

## Test plan
- [x] `pnpm exec tsc --noEmit`, `pnpm run lint`, `pnpm test` in
`web/enterprise-admin` — 58 files / 416 tests green (new coverage: view
model slicing/filters/selection/deltas suppression, bulk quota state
machine incl. retry, CSV quoting + injection, date-range picker wiring,
trend/model cards, page wiring)
- [x] Browser validation against a local mock backend (real dev server +
real auth flow): KPI cards, trend chart + tooltip, preset & calendar
range selection/apply/clear with client-side re-aggregation, model card
window note, member search/filter/sort, bulk quota apply end-to-end with
live row updates, over/near-quota badges, reset-pending retry
- [x] 16-agent adversarial review pass; all 12 confirmed findings fixed
(select-all scoping, pagination clamping, bulk retry denominators, CSV
injection, stale-data dimming, MVVM cleanup, dead-code removal)
- [x] `git diff origin/main -- services/` is empty — backend untouched
- [ ] CI (`enterprise-admin-quality`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

```
## Linear
<!-- 无关联 issue -->

## Summary

Rebuild the enterprise-admin `/usage` page into a full org usage dashboard + member usage management surface. **Frontend-only** — zero `services/claw-interface` changes; every panel runs on existing endpoints (design spec: `docs/superpowers/specs/2026-08-14-enterprise-admin-usage-dashboard.md`).

**Org usage analytics (new)**
- Usage trend card: recharts daily/10-minute bar chart with 24h / 7d / 30d presets **plus a calendar date-range picker** (react-day-picker + Radix Popover, zc theming) — custom ranges are client-side slices of the 30d daily dataset, bounded to the last 30 days; Credits / Requests / Peak-window KPIs recompute per selection; truncation (`meta.truncated`) surfaces as a banner; range switches dim stale data (keepPreviousData)
- Usage-by-model card: top-5 split with share bars, credits, requests
- Data source: the existing self-scoped `GET /users/credits/usage/records` — team-first billing resolution means an org admin's own call already returns org-wide aggregates
- Each section labels its time scope (trend = selected range, models = fetched window, member table = current credit period) since the date filter can only govern the trend card

**Member usage management (new)**
- Search (name/email/uid), filters (over quota / near quota ≥80% / unlimited / no usage), column sorting, share-of-spend column, near/over-quota badges, client-side pagination
- CSV export of the filtered view (RFC 4180 quoting + formula-injection guard + UTF-8 BOM)
- **Bulk AI-quota apply**: multi-select rows → one dialog applies the same limit sequentially via the existing single-member endpoint, with progress and failed-row retry
- LLM-only scope footnote (member usage excludes search/video drawn from the org wallet)

**Structure**: strict MVVM (`useUsageViewModel` owns all state/derivation); new reusable primitives `Popover`, `DateRangePicker`; new hooks `useUsageRecords`, `useBulkQuota`; `lib/csv`, `lib/local-date`; chart tokens `--color-chart-1..5` aligned with dashboard-console; full zh catalog coverage; `/usage` TopBar title fix. New deps: `recharts@3.9.2` (exact pin matching web/app), `react-day-picker@^9.14.0`.

**Known limits (by existing API contract, documented in the spec)**: no token totals, no billing-period range, no period-over-period deltas, model split capped at top-5 and not sliceable by custom dates, member usage is a current-period scalar (no history — upstream ECA-1352).

## Test plan
- [x] `pnpm exec tsc --noEmit`, `pnpm run lint`, `pnpm test` in `web/enterprise-admin` — 58 files / 416 tests green (new coverage: view model slicing/filters/selection/deltas suppression, bulk quota state machine incl. retry, CSV quoting + injection, date-range picker wiring, trend/model cards, page wiring)
- [x] Browser validation against a local mock backend (real dev server + real auth flow): KPI cards, trend chart + tooltip, preset & calendar range selection/apply/clear with client-side re-aggregation, model card window note, member search/filter/sort, bulk quota apply end-to-end with live row updates, over/near-quota badges, reset-pending retry
- [x] 16-agent adversarial review pass; all 12 confirmed findings fixed (select-all scoping, pagination clamping, bulk retry denominators, CSV injection, stale-data dimming, MVVM cleanup, dead-code removal)
- [x] `git diff origin/main -- services/` is empty — backend untouched
- [ ] CI (`enterprise-admin-quality`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

```
