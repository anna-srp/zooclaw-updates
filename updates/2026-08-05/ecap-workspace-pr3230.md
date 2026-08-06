---
title: "Agent Builder 测试布局更稳定"
type: "体验优化"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# Agent Builder 测试布局更稳定

## 核心宣传点

编辑与测试面板保持等宽并排，不会再被挤压或上下错位，窄屏下也能正常工作。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`405e420909ee0b28a3a31dfac3c6e9f2eccc3b0c`
- 作者：lynn Zhuang
- 日期：2026-08-05T06:14:58Z
- PR：#3230

### Commit Message

```
fix(agent-builder): stabilize builder test layout (#3230)

## Summary
- keep the Agent Builder chat and test preview side by side in an
equal-width, 1120px-minimum workspace
- compact the model selector while the test panel is open so header
controls do not crowd the split view
- hide the Auto review control row while preserving automatic feedback
and the manual fallback after failures

## Root cause
The workspace switched to a vertical stack below the desktop breakpoint
and used asymmetric pane widths above it. The model status and Auto
review row also consumed scarce space, which made the builder chat
dominate while the test preview appeared squeezed or displaced.

## Test plan
- [x] `bash scripts/verify-web.sh <changed Agent Builder files>`
- [x] `bash scripts/verify-changed.sh`
- [x] verified the local preview uses a 1120px canvas with two 560px
panes sharing the same top position
```

### PR Body

## Summary
- keep the Agent Builder chat and test preview side by side in an equal-width, 1120px-minimum workspace
- compact the model selector while the test panel is open so header controls do not crowd the split view
- hide the Auto review control row while preserving automatic feedback and the manual fallback after failures

## Root cause
The workspace switched to a vertical stack below the desktop breakpoint and used asymmetric pane widths above it. The model status and Auto review row also consumed scarce space, which made the builder chat dominate while the test preview appeared squeezed or displaced.

## Test plan
- [x] `bash scripts/verify-web.sh <changed Agent Builder files>`
- [x] `bash scripts/verify-changed.sh`
- [x] verified the local preview uses a 1120px canvas with two 560px panes sharing the same top position

