---
title: "用量与任务消耗统计改走聚合接口：不再超时或只显示被截断的总额"
type: "Improvement"
priority: "高"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 用量与任务消耗统计改走聚合接口：不再超时或只显示被截断的总额

## 核心宣传点

任务消耗以前要按分页把整个账号的会话用量全捞一遍，用量页则是直接扫计费事件，数据一多就超时，或者算出一个被截断的、看起来偏小的总额。现在这两处都改走带范围限定的计费聚合接口：任务页只请求当前计费周期内、当前可见那一页的会话，失败时给出明确的重试态；用量页把自定义日期区间下推到聚合侧，包含全部归因维度，分组数据用缓存快照、明细分页用游标。范围沿用服务端解析出的客户/成员/API Key 身份，失败时绝不退回扫事件、也绝不把失败伪装成「总额为 0」的完整结果。需要按依赖顺序先部署计费网关再部署接口层和前端。

## 分级

- 内部：P0
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary
Task credits previously fetched paginated account-wide session usage, while Usage views scanned Lago events and could time out or truncate totals. Route these reads through the scoped Billing Gateway aggregate API.

- Task requests only the visible page's session IDs for the current billing period, with an explicit retry state.
- Usage pushes custom dates to BG, includes all attribution categories, and uses cached group snapshots plus cursors for record pages.
- Reuse server-resolved customer/member/API-key scope; failures never fall back to event scans or appear as complete zero totals. ECAP adds no configuration or feature flag.

## Dependencies and rollout
Depends on https://github.com/SerendipityOneInc/billing-gateway/pull/76. Deploy BG first, then claw-interface, then Web. BG staging Vault is configured (KV v4 → v5), and the Kubernetes Secret has synchronized all four fields. A dedicated staging read role was provisioned and verified using 12/12 real queries from local BG PR code (232–773 ms). Existing Pods were not restarted. The production read role and session index remain rollout prerequisites; no production DDL or deployment is included.

## Validation
- PR review correction: preserve BG snapshot-scope denials as HTTP 403 / `usage.access_denied`, rather than retryable 503. All 16 gateway delegation tests pass, including authorization status/code assertions.
- ECAP: 69 related Python tests and 78 related Web tests passed during implementation; frontend/backend static gates passed. Browser-discovered copy/column issues were subsequently fixed and checked with ESLint and real browser validation.
- Local changed code → actual staging auth/Mongo → new local BG → actual staging Lago/PostgreSQL 16.13/Redis: Task visible-page batching, pagination, personal Usage Time/Session/API-key views and drill-down passed.
- Three BG account samples reconcile to Lago current-period consumption with zero difference. Largest 30-day sample: 107,801 events; first reads approximately 0.9–1.9 s, cached reads 34–150 ms.
- Two BG processes: eight cold Task batches make one Lago call; admission is bounded. A 30-second uncached run completed 52/52 requests. BG's companion isolated suite passes 673 tests at 92.87% coverage.

See `docs/superpowers/specs/2026-09-28-bg-usage-aggregation.md` and `docs/validation/2026-09-28-bg-usage-staging-validation.md` for the design, timings, rollout, and evidence limits. Team-admin/member browser acceptance remains pending. The staging sample also has three unrelated Agent session-list `agent not found` errors; Task displays partial-load status while credits queries succeed. CI, merge, deployment, and production acceptance are separate gates.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `7102c19fff98cdda6c2204c36c23d2bbe4f4d613`
- PR: #3908
- 作者：kaka-srp
- 日期：2026-09-28T08:36:55Z

### Commit Message

```
perf(credits): use scoped BG aggregation for Task and Usage (#3908)

## Summary
Task credits previously fetched paginated account-wide session usage,
while Usage views scanned Lago events and could time out or truncate
totals. Route these reads through the scoped Billing Gateway aggregate
API.

- Task requests only the visible page's session IDs for the current
billing period, with an explicit retry state.
- Usage pushes custom dates to BG, includes all attribution categories,
and uses cached group snapshots plus cursors for record pages.
- Reuse server-resolved customer/member/API-key scope; failures never
fall back to event scans or appear as complete zero totals. ECAP adds no
configuration or feature flag.

## Dependencies and rollout
Depends on https://github.com/SerendipityOneInc/billing-gateway/pull/76.
Deploy BG first, then claw-interface, then Web. BG staging Vault is
configured (KV v4 → v5), and the Kubernetes Secret has synchronized all
four fields. A dedicated staging read role was provisioned and verified
using 12/12 real queries from local BG PR code (232–773 ms). Existing
Pods were not restarted. The production read role and session index
remain rollout prerequisites; no production DDL or deployment is
included.

## Validation
- PR review correction: preserve BG snapshot-scope denials as HTTP 403 /
`usage.access_denied`, rather than retryable 503. All 16 gateway
delegation tests pass, including authorization status/code assertions.
- ECAP: 69 related Python tests and 78 related Web tests passed during
implementation; frontend/backend static gates passed. Browser-discovered
copy/column issues were subsequently fixed and checked with ESLint and
real browser validation.
- Local changed code → actual staging auth/Mongo → new local BG → actual
staging Lago/PostgreSQL 16.13/Redis: Task visible-page batching,
pagination, personal Usage Time/Session/API-key views and drill-down
passed.
- Three BG account samples reconcile to Lago current-period consumption
with zero difference. Largest 30-day sample: 107,801 events; first reads
approximately 0.9–1.9 s, cached reads 34–150 ms.
- Two BG processes: eight cold Task batches make one Lago call;
admission is bounded. A 30-second uncached run completed 52/52 requests.
BG's companion isolated suite passes 673 tests at 92.87% coverage.

See `docs/superpowers/specs/2026-09-28-bg-usage-aggregation.md` and
`docs/validation/2026-09-28-bg-usage-staging-validation.md` for the
design, timings, rollout, and evidence limits. Team-admin/member browser
acceptance remains pending. The staging sample also has three unrelated
Agent session-list `agent not found` errors; Task displays partial-load
status while credits queries succeed. CI, merge, deployment, and
production acceptance are separate gates.
```

来源：SerendipityOneInc/ecap-workspace @ 7102c19f，PR #3908，作者 kaka-srp。
