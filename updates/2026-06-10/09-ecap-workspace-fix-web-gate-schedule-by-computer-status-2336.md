---
title: "定时任务页面按机器状态加载修复"
type: "Bug Fix"
priority: "低"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 定时任务页面按机器状态加载修复

## 核心宣传点
修复了定时任务页面的任务加载逻辑，现在按机器就绪状态加载，定时任务列表显示更准确。

## 原始内容
```
fix(web): gate schedule by computer status (#2336)

## Summary
- gate the schedule page jobs query on FastClaw computer status instead
of OpenClaw WebSocket status
- resolve the schedule page computer id from the hydrated bot, falling
back to the computers list
- keep WebSocket cron fallback/write paths intact while allowing REST
reads when the computer is ready

## Tests
- pnpm --dir web --filter @zooclaw/web-app exec vitest run --config
./vitest.config.mts tests/unit/app/schedule/cron-client.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app exec eslint
'src/app/[locale]/(app)/(chat)/schedule/CronClient.tsx'
tests/unit/app/schedule/cron-client.unit.spec.tsx --quiet

Note: initial dependency install with lifecycle scripts failed on sharp
source build; reran pnpm install --frozen-lockfile --ignore-scripts to
link workspace test binaries without modifying tracked files.

---

### PR Description

## Summary
- gate the schedule page jobs query on FastClaw computer status instead of OpenClaw WebSocket status
- resolve the schedule page computer id from the hydrated bot, falling back to the computers list
- keep WebSocket cron fallback/write paths intact while allowing REST reads when the computer is ready

## Tests
- pnpm --dir web --filter @zooclaw/web-app exec vitest run --config ./vitest.config.mts tests/unit/app/schedule/cron-client.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app exec eslint 'src/app/[locale]/(app)/(chat)/schedule/CronClient.tsx' tests/unit/app/schedule/cron-client.unit.spec.tsx --quiet

Note: initial dependency install with lifecycle scripts failed on sharp source build; reran pnpm install --frozen-lockfile --ignore-scripts to link workspace test binaries without modifying tracked files.
```
