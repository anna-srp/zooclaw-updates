---
title: "修复：Agent 安装/卸载操作更稳定可靠"
type: "Bug Fix"
priority: "中"
date: "2026-04-29"
status: "待审核"
channels: "Discord, changelog"
---

# 修复：Agent 安装/卸载操作更稳定可靠

## 核心宣传点

优化了 Agent 安装和卸载的异步处理流程，操作结果更及时准确，减少安装后状态不同步的问题。

## 原始内容

**Commit:** `1bbc071d` — 2026-04-29T12:20:18Z
**Repo:** ecap-workspace
**Author:** nolan-srp

**Commit Message:**
```
fix(openclaw): wait for async agent operations (#1475)

## Summary
- switch incremental hire and fire flows to the async install and
uninstall endpoints
- wait for agent operations to finish before refreshing frontend agent
state
- centralize async operation polling and failure handling in the
OpenClaw API client
```

**PR #1475:** fix(openclaw): wait for async agent operations

**PR Body:**
## Summary
- switch incremental hire and fire flows to the async install and uninstall endpoints
- wait for agent operations to finish before refreshing frontend agent state
- centralize async operation polling and failure handling in the OpenClaw API client
