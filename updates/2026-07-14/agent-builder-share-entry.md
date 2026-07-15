---
title: "Agent Builder 无对话时保留（禁用）分享入口"
type: "体验优化"
priority: "低"
date: "2026-07-14"
status: "待审核"
channels: ""
---

# Agent Builder 无对话时保留（禁用）分享入口

## 核心宣传点
Agent Builder 的分享入口在没有可分享对话时改为置灰保留，不再直接消失。

## 原始内容
### PR #2859 — fix(agent-builder): 无对话时保留禁用的分享入口 (#2859)
作者: lynn-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2859

## Summary
- 在 Agent Builder 的 `More` 菜单中始终保留 `Share conversation`
- 没有可分享对话时显示为 disabled，有消息时继续使用现有分享流程
- 更新回归测试，覆盖无消息时的禁用状态

## Root cause
`canShareConversation` 同时控制菜单项是否渲染和是否可点击，因此没有可分享消息时入口会直接消失。

## Test plan
- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderProjectActionControls.tsx' web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- [x] 本地 Mock 无对话项目中确认 `Share conversation` 可见且 disabled
