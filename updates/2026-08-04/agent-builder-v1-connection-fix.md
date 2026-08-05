---
title: "Agent Builder 连接状态显示错误与 Pack Test 预览无法连接修复"
type: "Bug Fix"
priority: "中"
date: "2026-08-04"
status: "待审核"
channels: ""
commit: "5f1ee0e1c12afaa9147b0f04767eab33d799ff7d"
repo: "SerendipityOneInc/ecap-workspace"
---

## 核心宣传点

修复 v1 Agent Builder 顶栏显示了错误的连接状态（此前误读全局 WebSocket），以及 Pack Test 预览因等待过期的 Bot 在线状态而一直连不上的问题，测试预览即开即用。

## 原始内容

```
fix(agent-builder): correct v1 connection handling (#3213)

## Summary

- make the v1 Agent Builder header report the builder computer's
Mattermost transport instead of the unrelated global OpenClaw WebSocket
- let ready v1 Pack Test previews connect without waiting on stale
Mattermost bot presence
- preserve the existing Engine v2 presence gate and hidden Builder
connection status

## Root cause

The v1 Builder supplied no explicit connection source, so
`/agent-builder` fell back to the global OpenClaw WebSocket and computer
even though Builder messaging uses Mattermost. Separately, v1 Test
passed `botUserId` to the shared Mattermost `autoConnect`, which blocked
WebSocket setup while Mattermost presence remained `offline` even after
the preview bot had connected.

## Scope

- frontend only
- v1 Agent Builder project header and v1 Pack Test preview connection
only
- no backend or shared presence-polling behavior changes
- Engine v2 behavior remains unchanged

## Test plan

- [x] targeted Agent Builder and connection-status unit tests (82
passed)
- [x] `bash scripts/verify-local.sh --web-static ...`
- [x] TypeScript and ESLint
- [x] import-boundary and test-duplication checks
- [x] pre-push changed-surface verification

---

### PR Body

## Summary

- make the v1 Agent Builder header report the builder computer's Mattermost transport instead of the unrelated global OpenClaw WebSocket
- let ready v1 Pack Test previews connect without waiting on stale Mattermost bot presence
- preserve the existing Engine v2 presence gate and hidden Builder connection status

## Root cause

The v1 Builder supplied no explicit connection source, so `/agent-builder` fell back to the global OpenClaw WebSocket and computer even though Builder messaging uses Mattermost. Separately, v1 Test passed `botUserId` to the shared Mattermost `autoConnect`, which blocked WebSocket setup while Mattermost presence remained `offline` even after the preview bot had connected.

## Scope

- frontend only
- v1 Agent Builder project header and v1 Pack Test preview connection only
- no backend or shared presence-polling behavior changes
- Engine v2 behavior remains unchanged

## Test plan

- [x] targeted Agent Builder and connection-status unit tests (82 passed)
- [x] `bash scripts/verify-local.sh --web-static ...`
- [x] TypeScript and ESLint
- [x] import-boundary and test-duplication checks
- [x] pre-push changed-surface verification

```
