---
title: "开发者平台新增组织用量页：按 24 小时 / 7 天 / 30 天查看消费与调用明细"
type: "新功能"
priority: "高"
date: "2026-10-01"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# 开发者平台新增组织用量页：按 24 小时 / 7 天 / 30 天查看消费与调用明细

## 核心宣传点

开发者平台的 Usage 原先一直是延后状态，而且被绑在当前选中的 Project 上，实际上可用的用量接口报的是整个组织的数据。这次开出一个顶层的组织用量页：展示完整快照的美元消费、模型与工具调用次数，以及按游标分页的活动明细，支持滚动的 24 小时 / 7 天 / 30 天三个区间；翻页时保持快照和 as_of 不变，手动刷新才开新快照。项目筛选固定为 All projects 并给出「Filter unavailable」提示，共享和未归属的费用会保留，错误、权限不足、账单未就绪和确认为零用量这几种情况会区分开，且查看用量不会触发账单初始化。侧栏和登录页的品牌标识同时换成新的 ZooWork logo，窄屏和暗色模式都适配了。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

Platform Usage was deferred and tied to the selected Project even though the available Usage API reports the entire Organization. Expose one top-level Organization Usage page using the existing read-only API; switching the active Project leaves Usage unchanged.

- Show complete snapshot spend in USD, model/tool calls, and cursor-paged activity for rolling 24h/7d/30d ranges. Preserve snapshot and as_of across pages; refresh starts a new snapshot.
- Keep All projects fixed and show a concise “Filter unavailable” notice. Preserve shared/unattributed costs and distinguish errors, permissions, billing readiness, and verified zero usage without initializing billing.
- Replace the sidebar and sign-in branding with the supplied ZooWork logo, including narrow-screen and dark-mode styling.

Frontend only; no service, API contract, or deployment changes. Future Project attribution/filtering remains tracked in https://github.com/SerendipityOneInc/ecap-workspace/issues/3958 (this PR does not close it). Activity loads 50 rows at a time; loaded rows remain in the DOM.

## Test plan

- [x] Rebased onto current main, then ran Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test` (37 passed), and `pnpm build` in `web/platform`.
- [x] MSW coverage for Organization scope independent of Project selection, snapshot pagination/refresh/expiry, time ranges, shared costs, incomplete totals, errors, permission denial, billing readiness, and zero usage.
- [x] Desktop and mobile visual checks; synthetic 2,000-record preview and long model/session strings render without outer horizontal overflow.
- [x] Local dev connects to the existing staging API. Fixture stress preview is gitignored and excluded from the shipped entry point.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `7f1deae1e938df1541c3fe4154f6794f5693e5c5`
- PR: #3970
- 作者：finn-srp
- 日期：2026-10-01T03:48:13Z

### Commit Message

```
feat(platform): expose organization usage and update branding (#3970)

## Summary

Platform Usage was deferred and tied to the selected Project even though
the available Usage API reports the entire Organization. Expose one
top-level Organization Usage page using the existing read-only API;
switching the active Project leaves Usage unchanged.

- Show complete snapshot spend in USD, model/tool calls, and
cursor-paged activity for rolling 24h/7d/30d ranges. Preserve snapshot
and as_of across pages; refresh starts a new snapshot.
- Keep All projects fixed and show a concise “Filter unavailable”
notice. Preserve shared/unattributed costs and distinguish errors,
permissions, billing readiness, and verified zero usage without
initializing billing.
- Replace the sidebar and sign-in branding with the supplied ZooWork
logo, including narrow-screen and dark-mode styling.

Frontend only; no service, API contract, or deployment changes. Future
Project attribution/filtering remains tracked in
https://github.com/SerendipityOneInc/ecap-workspace/issues/3958 (this PR
does not close it). Activity loads 50 rows at a time; loaded rows remain
in the DOM.

## Test plan

- [x] Rebased onto current main, then ran Node 24 `pnpm lint`, `pnpm
typecheck`, `pnpm test` (37 passed), and `pnpm build` in `web/platform`.
- [x] MSW coverage for Organization scope independent of Project
selection, snapshot pagination/refresh/expiry, time ranges, shared
costs, incomplete totals, errors, permission denial, billing readiness,
and zero usage.
- [x] Desktop and mobile visual checks; synthetic 2,000-record preview
and long model/session strings render without outer horizontal overflow.
- [x] Local dev connects to the existing staging API. Fixture stress
preview is gitignored and excluded from the shipped entry point.
```

来源：SerendipityOneInc/ecap-workspace @ 7f1deae1，PR #3970，作者 finn-srp。
