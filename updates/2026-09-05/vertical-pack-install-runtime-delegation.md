---
title: "修复：从旧版迁移过来的账号装不了垂直行业 Agent 包"
type: "Bug Fix"
priority: "高"
date: "2026-09-05"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：从旧版迁移过来的账号装不了垂直行业 Agent 包

## 核心宣传点

一部分老用户点「安装垂直行业 Agent 包」时，按钮点下去像是没反应——请求压根没发到后端。原因在前端：它自己从新手引导状态里去猜这个账号该走 v1 还是 v2，并且要求名下有一台「已就绪」的 v1 计算机，才肯发出安装请求。可是迁移过来的账号常常还留着一条已停止的 v1 计算机记录，于是前端判定「环境没准备好」，直接把安装请求吞掉了——而后端其实一直认为这个账号完全有资格安装。

这次把判断权还给后端：前端不再做 OpenClaw 初始化、新手引导状态、计算机就绪这三道拦截，运行时选哪一套、以及最终的幂等去重，全部交给本来就负责这件事的后端安装接口。前端只保留一件轻活——在统一的 Agent 列表里按 `pack_id` 做一次预检去重，避免你重复点出两个一样的 Agent；这个去重不再按计算机或运行时过滤，所以不会再出现「明明装过了却看不见、于是又装一遍」的错位。后端接受安装之后，统一 Agent 列表会立即刷新，装完就能看到。

## 原始内容

### fix(web): delegate vertical pack runtime selection (#3658)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `36f3f818b53bc33aa9f8573848deb7ac0c6f3fa8`
- PR: #3658
- 作者: bill-srp
- 日期: 2026-09-05T00:55:18Z

### Commit Message

```
fix(web): delegate vertical pack runtime selection (#3658)

## Summary
- Remove frontend OpenClaw init, onboarding status, and computer
readiness gates from vertical pack installation.
- Retain the frontend `pack_id` preflight dedupe across the unified
Agent list, without filtering by computer or runtime.
- Delegate runtime selection and final idempotency enforcement to the
existing backend install endpoint.
- Refresh the unified Agent list after the backend accepts the package
install.

## Root cause
The frontend inferred v1/v2 mode from onboarding state and required a
ready v1 computer before it would call the vertical pack install
endpoint. Migrated users can retain a stopped v1 computer record,
causing the frontend to suppress the install request even though the
backend considers the account eligible for Engine.

## Test plan
- [x] Run targeted web verification (governance guards, TypeScript,
Vitest, ESLint).
- [x] Verify 8 related test files and 114 tests pass.
- [x] Verify the changed-surface pre-push gate passes.
```

### PR Body

```
## Summary
- Remove frontend OpenClaw init, onboarding status, and computer readiness gates from vertical pack installation.
- Retain the frontend `pack_id` preflight dedupe across the unified Agent list, without filtering by computer or runtime.
- Delegate runtime selection and final idempotency enforcement to the existing backend install endpoint.
- Refresh the unified Agent list after the backend accepts the package install.

## Root cause
The frontend inferred v1/v2 mode from onboarding state and required a ready v1 computer before it would call the vertical pack install endpoint. Migrated users can retain a stopped v1 computer record, causing the frontend to suppress the install request even though the backend considers the account eligible for Engine.

## Test plan
- [x] Run targeted web verification (governance guards, TypeScript, Vitest, ESLint).
- [x] Verify 8 related test files and 114 tests pass.
- [x] Verify the changed-surface pre-push gate passes.

```
