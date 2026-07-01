---
title: "Agent Builder 测试预览自动重置为全新会话"
type: "体验优化"
priority: "中"
date: "2026-06-30"
status: "待审核"
channels: ""
---
# Agent Builder 测试预览自动重置为全新会话
## 核心宣传点
在 Agent Builder 打包测试时，预览对话会自动开启一次全新会话，创作者不用再每次手动输入 /new 清空上一次的测试上下文。
## 原始内容
fix(agent-builder): reset pack test chat sessions (#2656)

## Summary

- Automatically sends `/new` once when an Agent Builder Pack Test
preview chat is connected and its history is ready.
- Keeps the reset scoped to the current `test_run_id`, so rerenders of
the same preview do not send duplicate `/new` commands.
- Excludes `/new` / `/reset` / `/compact` control-command turns from
Agent Builder test feedback detection, so the automatic reset does not
get auto-reviewed back into the builder chat.

## Why

Pack Test preview chats can reuse an existing bot session. That leaves
stale conversation context in the test bot and forces the creator to
manually type `/new` after every Package & Test. The preview should
start from a fresh runtime session as soon as it is ready, without
requiring user input.

## Tests

- `corepack pnpm exec vitest run
tests/unit/app/agent-builder-test-chat.unit.spec.tsx --config
./vitest.config.mts`
- `bash scripts/verify-web.sh --no-test
web/app/src/app/[locale]/\(app\)/\(chat\)/agent-builder/AgentBuilderTestChat.tsx
web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx`
- pre-push `verify-changed`: passed

---

### PR Description

## Summary

- Automatically sends `/new` once when an Agent Builder Pack Test preview chat is connected and its history is ready.
- Keeps the reset scoped to the current `test_run_id`, so rerenders of the same preview do not send duplicate `/new` commands.
- Excludes `/new` / `/reset` / `/compact` control-command turns from Agent Builder test feedback detection, so the automatic reset does not get auto-reviewed back into the builder chat.

## Why

Pack Test preview chats can reuse an existing bot session. That leaves stale conversation context in the test bot and forces the creator to manually type `/new` after every Package & Test. The preview should start from a fresh runtime session as soon as it is ready, without requiring user input.

## Tests

- `corepack pnpm exec vitest run tests/unit/app/agent-builder-test-chat.unit.spec.tsx --config ./vitest.config.mts`
- `bash scripts/verify-web.sh --no-test web/app/src/app/[locale]/\(app\)/\(chat\)/agent-builder/AgentBuilderTestChat.tsx web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx`
- pre-push `verify-changed`: passed

