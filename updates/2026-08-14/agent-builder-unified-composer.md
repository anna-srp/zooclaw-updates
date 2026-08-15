---
title: "Agent Builder 与预览窗口共用同一套输入框"
type: "体验优化"
priority: "中"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

构建区和预览区的输入框现在完全一致：同样的快捷操作、模型选择、发送/停止和技能与 Connectors 入口，不再有两套割裂的体验。

## 原始内容

fix(agent-builder): unify chat composers (#3374)

## Summary

- Route both Agent Builder and Preview through the same `GenClawInput` /
`UnifiedChatComposer` / `@zooclaw/chat-ui` composer path.
- Align composer width, page inset, quick actions, model picker,
send/stop action, disabled state, copy, accessibility labels, and test
hooks.
- Preserve Engine V2-only attachments, transactional attachment
recovery, in-flight submit locking, and Preview auto-feedback behavior.
- Keep Skills and Connectors available when a runtime does not support
file attachments, while hiding Local and Recent file actions.

## Root cause

Builder and Preview rendered separate composer implementations. The
Preview-specific `AgentBuilderTestComposer` duplicated layout and
interaction behavior, so styling and capabilities drifted from the
Builder composer. The fix removes that parallel renderer and passes
Preview-specific runtime capabilities through the shared chat surface
instead.

## Test plan

- [x] `bash scripts/verify-local.sh --changed` (governance guards, app
TypeScript, app ESLint)
- [x] Targeted app Vitest suites: 6 files / 205 tests passed
- [x] `pnpm --filter @zooclaw/chat-ui test` (32 files / 354 tests
passed)
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] Authenticated staging route loaded for the real Agent Builder
project; the shared Preview composer rendered in its unavailable state
because the staging Preview build itself was failed. No Retry, Publish,
or message-send mutation was triggered.

---
### PR Body

## Summary

- Route both Agent Builder and Preview through the same `GenClawInput` / `UnifiedChatComposer` / `@zooclaw/chat-ui` composer path.
- Align composer width, page inset, quick actions, model picker, send/stop action, disabled state, copy, accessibility labels, and test hooks.
- Preserve Engine V2-only attachments, transactional attachment recovery, in-flight submit locking, and Preview auto-feedback behavior.
- Keep Skills and Connectors available when a runtime does not support file attachments, while hiding Local and Recent file actions.

## Root cause

Builder and Preview rendered separate composer implementations. The Preview-specific `AgentBuilderTestComposer` duplicated layout and interaction behavior, so styling and capabilities drifted from the Builder composer. The fix removes that parallel renderer and passes Preview-specific runtime capabilities through the shared chat surface instead.

## Test plan

- [x] `bash scripts/verify-local.sh --changed` (governance guards, app TypeScript, app ESLint)
- [x] Targeted app Vitest suites: 6 files / 205 tests passed
- [x] `pnpm --filter @zooclaw/chat-ui test` (32 files / 354 tests passed)
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] Authenticated staging route loaded for the real Agent Builder project; the shared Preview composer rendered in its unavailable state because the staging Preview build itself was failed. No Retry, Publish, or message-send mutation was triggered.

