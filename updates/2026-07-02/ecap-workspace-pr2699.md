---
title: "Agent Builder 在 Claw 未运行时给出明确提示"
type: "体验优化"
priority: "低"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# Agent Builder 在 Claw 未运行时给出明确提示
## 核心宣传点
Agent Builder 检测到没有正在运行的 Claw 时，不再一直显示「工作区准备中」，而是给出清晰的原因说明和可操作的提示。
## 原始内容
### [ecap-workspace PR #2699]

fix(agent-builder): show no-running-bot notice (#2699)

## Summary
- Show a clear Agent Builder notice when the builder workspace reports
`computer_not_ready` or `missing_computer`.
- Reuse the chat-page-style dormant wording for the no-running-Claw
state.
- Share the same workspace notice between the status pane and the Build
fallback card.

## Root cause
Agent Builder treated a non-running or missing Claw bot as a generic
preparing state, so users saw an indefinite workspace preparation
message instead of an actionable explanation.

## Test plan
- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderStatusPane.tsx'
web/app/src/locales/en.ts web/app/src/locales/zh.ts`
- [x] pre-push changed-surface check (`verify-web.sh --no-test` via
hook)

---

## PR Description

## Summary
- Show a clear Agent Builder notice when the builder workspace reports `computer_not_ready` or `missing_computer`.
- Reuse the chat-page-style dormant wording for the no-running-Claw state.
- Share the same workspace notice between the status pane and the Build fallback card.

## Root cause
Agent Builder treated a non-running or missing Claw bot as a generic preparing state, so users saw an indefinite workspace preparation message instead of an actionable explanation.

## Test plan
- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderClient.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderStatusPane.tsx' web/app/src/locales/en.ts web/app/src/locales/zh.ts`
- [x] pre-push changed-surface check (`verify-web.sh --no-test` via hook)

