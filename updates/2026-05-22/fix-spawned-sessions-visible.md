---
title: "修复子 Agent 会话消失的问题：派生对话现在稳定可见"
type: "Bug Fix"
priority: "高"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 修复子 Agent 会话消失的问题：派生对话现在稳定可见

## 核心宣传点

修复了 Agent 自动派生子任务对话后，这些子对话在界面上消失看不到的问题，现在所有活跃对话都能正常显示在侧边栏。

## 原始内容

**Commit**: 4e23d254e53ece8ff062e9883a205c737a2f8fbe
**Author**: bill-srp
**Date**: 2026-05-22T08:38:06Z
**PR**: #1847

### Commit Message
```
fix(chat): keep spawned sessions visible (#1847)

## Summary
- Keep spawned subagent sessions visible after they reach terminal
status.
- Remove the local auto-collapse timer that made completed spawned
sessions disappear after switching agents.
- Update focused hook tests to cover persistent terminal sessions.

## Root cause
The chat rail locally marked terminal spawned sessions as
fading/collapsed after a short timeout. When a user switched to another
agent and returned after that timeout, the session was still known
locally but no longer in the visible rail, so it appeared to disappear.

Linear:
https://linear.app/srpone/issue/ECA-737/spawn-的-session-显示不稳定切换-agent-后消失

## Test plan
- [x] pnpm --dir web/app run lint
- [x] pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/chat/useSubagentSessions.unit.spec.ts
tests/unit/app/chat/useChatSubagentRail.unit.spec.ts
- [ ] pnpm --dir web run lint (blocked outside app:
web/packages/auth-client cannot resolve typescript-eslint)
- [ ] pnpm --dir web run tsc (workspace script fails: pnpm exec rejects
--if-present)
- [ ] pnpm --dir web/app exec tsc --noEmit (blocked:
src/lib/heic-image.ts cannot resolve heic-to/csp)
- [ ] pnpm --dir web/app run test:unit (blocked: heic-to/csp resolution
failure in unrelated heic/upload/Mattermost suites)
```

### PR Description
## Summary
- Keep spawned subagent sessions visible after they reach terminal status.
- Remove the local auto-collapse timer that made completed spawned sessions disappear after switching agents.
- Update focused hook tests to cover persistent terminal sessions.

## Root cause
The chat rail locally marked terminal spawned sessions as fading/collapsed after a short timeout. When a user switched to another agent and returned after that timeout, the session was still known locally but no longer in the visible rail, so it appeared to disappear.

Linear: https://linear.app/srpone/issue/ECA-737/spawn-的-session-显示不稳定切换-agent-后消失

## Test plan
- [x] pnpm --dir web/app run lint
- [x] pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/chat/useSubagentSessions.unit.spec.ts tests/unit/app/chat/useChatSubagentRail.unit.spec.ts
- [ ] pnpm --dir web run lint (blocked outside app: web/packages/auth-client cannot resolve typescript-eslint)
- [ ] pnpm --dir web run tsc (workspace script fails: pnpm exec rejects --if-present)
- [ ] pnpm --dir web/app exec tsc --noEmit (blocked: src/lib/heic-image.ts cannot resolve heic-to/csp)
- [ ] pnpm --dir web/app run test:unit (blocked: heic-to/csp resolution failure in unrelated heic/upload/Mattermost suites)

