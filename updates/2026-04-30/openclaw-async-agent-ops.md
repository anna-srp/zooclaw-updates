---
title: "修复：安装/卸载 Agent 时界面卡住的问题"
type: "Bug Fix"
priority: "中"
date: "2026-04-30"
status: "待审核"
channels: ""
---
# 修复：安装/卸载 Agent 时界面卡住的问题

## 核心宣传点
安装或删除 Agent 时，界面现在会等待操作真正完成后再刷新，不再出现状态不同步的问题。

## 原始内容
**Commit**: fix(openclaw): wait for async agent operations (#1475)
**Author**: （merge commit）
**Date**: 2026-04-29

```
fix(openclaw): wait for async agent operations (#1475)

## Summary
- switch incremental hire and fire flows to the async install and
  uninstall endpoints
- wait for agent operations to finish before refreshing frontend agent state
- centralize async operation polling and failure handling in the OpenClaw API client
```

**PR #1475 Body**:
## Summary
- switch incremental hire and fire flows to the async install and uninstall endpoints
- wait for agent operations to finish before refreshing frontend agent state
- centralize async operation polling and failure handling in the OpenClaw API client
