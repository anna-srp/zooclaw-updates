---
title: "修复：Mattermost 连接时顶栏状态异常显示已断开"
type: "Bug Fix"
priority: "中"
date: "2026-06-07"
status: "待审核"
channels: ""
---
# 修复：Mattermost 连接时顶栏状态异常显示已断开

## 核心宣传点
修复了顶部状态栏在 Mattermost 已连接时错误显示"已断开"的问题，连接状态展示现在更准确。

## 原始内容
**PR:** #2241
**Author:** bill-srp
**Date:** 2026-06-07T07:37:53Z
**SHA:** fa5dbed07738f74fb324cf607ce647a8ab2eea4b

### Commit Message
```
fix(web): show connected topbar from Mattermost status (#2241)

## Summary
- Use Mattermost connection state as the topbar status source when
Mattermost context is present.
- Keep OpenClaw websocket status as the fallback for pages without
Mattermost context.
- Update the header unit expectation for MM-connected /
gateway-WS-disconnected state.

## Root cause
The topbar still required the old OpenClaw gateway websocket status to
be connected. After removing the status-connect token-check dependency,
that websocket can remain disconnected while Mattermost is connected, so
the header incorrectly showed the disconnected state.

## Test plan
- [x] Commit created: 3d2c25225
- [ ] pnpm --dir web run lint — blocked locally by ESLint config/tooling
error: eslint-config-next/plugin:@next/next reports unexpected top-level
property "name".
- [ ] pnpm --dir web run tsc — blocked locally by pnpm command dispatch
error: Unknown option "if-present".
- [ ] pnpm --dir web run test:unit — blocked locally by incomplete
node_modules; many suites fail to resolve declared deps including
usehooks-ts, zustand, and @tanstack/query-sync-storage-persister.
```

### PR Description
## Summary
- Use Mattermost connection state as the topbar status source when Mattermost context is present.
- Keep OpenClaw websocket status as the fallback for pages without Mattermost context.
- Update the header unit expectation for MM-connected / gateway-WS-disconnected state.

## Root cause
The topbar still required the old OpenClaw gateway websocket status to be connected. After removing the status-connect token-check dependency, that websocket can remain disconnected while Mattermost is connected, so the header incorrectly showed the disconnected state.

## Test plan
- [x] Commit created: 3d2c25225
- [ ] pnpm --dir web run lint — blocked locally by ESLint config/tooling error: eslint-config-next/plugin:@next/next reports unexpected top-level property "name".
- [ ] pnpm --dir web run tsc — blocked locally by pnpm command dispatch error: Unknown option "if-present".
- [ ] pnpm --dir web run test:unit — blocked locally by incomplete node_modules; many suites fail to resolve declared deps including usehooks-ts, zustand, and @tanstack/query-sync-storage-persister.

