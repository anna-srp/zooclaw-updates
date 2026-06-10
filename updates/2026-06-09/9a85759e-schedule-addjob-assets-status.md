---
title: "日程页新增「添加任务」入口、资产页连接状态更准"
type: "体验优化"
priority: "中"
date: "2026-06-09"
status: "待审核"
channels: ""
---

# 日程页新增「添加任务」入口、资产页连接状态更准

## 核心宣传点

日程页在空状态和列表头新增了显眼的「添加任务」按钮，资产页的连接状态也会实时反映机器人在线情况。

## 原始内容

完整 commit message：

```
fix(web): address refactor validation follow-ups (#2317)

## Summary
- Add visible Add Job entry points for the schedule empty state and All
Jobs header.
- Activate the shared OpenClaw provider on `/assets` so the connection
pill reflects live Claw status instead of staying disconnected while
uploads render.
- Add focused unit coverage and a local validation report for the two
follow-up fixes.

## Root Cause
- `/schedule` already had a create handler, but no visible empty-state
control invoked it.
- `/assets` rendered the shared Claw header while only reading passive
OpenClaw context, so the provider was never activated on the default
uploads view.

## Validation
- `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/assets/AssetsClient.unit.spec.tsx
tests/unit/components/ClawPageHeader.unit.spec.ts
tests/unit/app/schedule/cron-client.unit.spec.tsx`
- `pnpm run lint`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `env NODE_OPTIONS="--no-deprecation --no-experimental-webstorage" pnpm
exec vitest run --config ./vitest.config.mts`
- Browser CDP against local `pnpm dev:staging`: `/assets` shows `Claw
Connected`; `/schedule` empty state Add Job opens the New Job form
without submitting a job.

## PR Structure
Stacked on #2316 (`fix/new-chat-session-status`) so this PR only
contains the report follow-up fixes. After #2316 merges, this PR can be
retargeted to `main`.
```

PR 描述：

## Summary
- Add visible Add Job entry points for the schedule empty state and All Jobs header.
- Activate the shared OpenClaw provider on `/assets` so the connection pill reflects live Claw status instead of staying disconnected while uploads render.
- Add focused unit coverage and a local validation report for the two follow-up fixes.

## Root Cause
- `/schedule` already had a create handler, but no visible empty-state control invoked it.
- `/assets` rendered the shared Claw header while only reading passive OpenClaw context, so the provider was never activated on the default uploads view.

## Validation
- `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/assets/AssetsClient.unit.spec.tsx tests/unit/components/ClawPageHeader.unit.spec.ts tests/unit/app/schedule/cron-client.unit.spec.tsx`
- `pnpm run lint`
- `pnpm exec tsc --noEmit --project app/tsconfig.json`
- `env NODE_OPTIONS="--no-deprecation --no-experimental-webstorage" pnpm exec vitest run --config ./vitest.config.mts`
- Browser CDP against local `pnpm dev:staging`: `/assets` shows `Claw Connected`; `/schedule` empty state Add Job opens the New Job form without submitting a job.

## PR Structure
Stacked on #2316 (`fix/new-chat-session-status`) so this PR only contains the report follow-up fixes. After #2316 merges, this PR can be retargeted to `main`.

