---
title: "工具执行状态展示更丰富、可点击查看详情"
type: "体验优化"
priority: "中"
date: "2026-07-08"
status: "待审核"
channels: ""
---

# 工具执行状态展示更丰富、可点击查看详情

## 核心宣传点

Agent 执行工具时的状态展示更丰富，能看到工具参数、进度和摘要，还能点开单个步骤查看详细信息，Agent 在做什么一目了然。

## 原始内容

```
feat(web): improve tool status display (#2768)

## Summary
- Parse Mattermost tool status props into richer tool step display data,
including tool args, item metadata, status, summaries, and progress
text.
- Format tool arguments with official-style concise previews, including
multiline update_plan step/status output.
- Let users click an individual tool row to expand full long content and
click again to collapse, while keeping update_plan multiline by default.

## Impact
- Tool rows stay compact by default but remain inspectable when
command/path/url details are long.
- update_plan no longer exposes raw JSON in the chat UI.
- Same tool_call_id updates merge into the original tool row instead of
creating duplicate rows.

## Validation
- Passed: git diff --check.
- Blocked: CI=true pnpm --dir web/app test:unit --
tests/unit/app/chat/toolStatusParser.unit.spec.ts
tests/unit/app/chat/ToolGroup.unit.spec.tsx fails before running tests
because pnpm reports ERR_PNPM_LOCKFILE_CONFIG_MISMATCH for the current
lockfile overrides config.

---

**PR Description:**

## Summary
- Parse Mattermost tool status props into richer tool step display data, including tool args, item metadata, status, summaries, and progress text.
- Format tool arguments with official-style concise previews, including multiline update_plan step/status output.
- Let users click an individual tool row to expand full long content and click again to collapse, while keeping update_plan multiline by default.

## Impact
- Tool rows stay compact by default but remain inspectable when command/path/url details are long.
- update_plan no longer exposes raw JSON in the chat UI.
- Same tool_call_id updates merge into the original tool row instead of creating duplicate rows.

## Validation
- Passed: git diff --check.
- Blocked: CI=true pnpm --dir web/app test:unit -- tests/unit/app/chat/toolStatusParser.unit.spec.ts tests/unit/app/chat/ToolGroup.unit.spec.tsx fails before running tests because pnpm reports ERR_PNPM_LOCKFILE_CONFIG_MISMATCH for the current lockfile overrides config.
```
