---
title: "会话历史页新增返回按钮"
type: "产品基础功能更新"
priority: "低"
date: "2026-04-24"
status: "待审核"
channels: "Discord+changelog"
---
# 会话历史页新增返回按钮

## 核心宣传点
会话历史页顶部新增返回箭头，点击直接回到设置页，导航更顺畅。

## 原始内容

feat(web): add back button to session history page (#1261)
- Add a BackButton component to the session history page header
- Navigates back to `/claw-settings` when clicked
- Applied consistently across all page states (loading, empty, normal)
