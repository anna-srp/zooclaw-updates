---
title: "修复：更新 Agent 后正确跳转到对话页面"
type: "Bug Fix"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 修复：更新 Agent 后正确跳转到对话页面

## 核心宣传点

修复了更新 Agent 设置后，页面没有自动跳转到 Agent 对话页的问题，操作体验更流畅。

## 原始内容

**Commit**: `9455b9e43a94527a98f66696e2638e3eb63bbd31`
**仓库**: ecap-workspace
**作者**: nolan-srp
**时间**: 2026-04-28T12:12:21Z

### 完整 Commit Message

```
fix(web): redirect after /new in agent update flow (#1447)

## Summary
- navigate to the agent chat page after the update success modal sends
/new
- align both agents manager entry points on the same post-reset behavior
- keep the update flow focused on the refreshed agent session
```

### PR #1447 完整描述

## Summary
- navigate to the agent chat page after the update success modal sends /new
- align both agents manager entry points on the same post-reset behavior
- keep the update flow focused on the refreshed agent session
