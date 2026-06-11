---
title: "侧边栏新增 Agent 私信入口"
type: "体验优化"
priority: "低"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 侧边栏新增 Agent 私信入口

## 核心宣传点
在每个 Agent 会话列表顶部新增「私信」入口，可一键直达与该 Agent 的对话，找入口更方便。

## 原始内容
```
fix(web): add agent direct message sidebar link (#2326)

## Summary
- Add a Direct Message entry at the top of each expanded agent session
list
- Route Direct Message to /chat with the current agent_id query
parameter
- Cover ordering and navigation with SideNavAgentSessions unit test

## Local checks
- pnpm --dir web run lint (passes with existing enterprise-app warnings)
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit

## Notes
- pnpm --dir web run tsc currently fails in the workspace script before
typechecking with: Unknown option: if-present

---

### PR Description

## Summary
- Add a Direct Message entry at the top of each expanded agent session list
- Route Direct Message to /chat with the current agent_id query parameter
- Cover ordering and navigation with SideNavAgentSessions unit test

## Local checks
- pnpm --dir web run lint (passes with existing enterprise-app warnings)
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit

## Notes
- pnpm --dir web run tsc currently fails in the workspace script before typechecking with: Unknown option: if-present
```
