---
title: "修复：侧边栏底部导航不再被 Agent 列表遮挡"
type: "Bug Fix"
priority: "低"
date: "2026-04-22"
status: "待审核"
channels: ""
---

# 修复：侧边栏底部导航不再被 Agent 列表遮挡

## 核心宣传点

修复 Agent 列表过长时底部导航（AI Specialists Hub 等）被推出视野的问题，侧边栏操作更流畅。

## 原始内容

fix(web): sticky sidebar bottom nav with scrollable agent list (ECA-520) (#1132)

When the agent list grows long, it was pushing the fixed sidebar entries (AI Specialists Hub, settings, etc.) out of the viewport. Fixed by making the agent list scrollable independently while keeping the bottom nav always visible.
