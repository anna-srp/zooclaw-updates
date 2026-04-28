---
title: "切换 Agent 时保留输入框草稿"
type: "体验优化"
priority: "中"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 切换 Agent 时保留输入框草稿

## 核心宣传点
在 /chat 页面切换不同 Agent 时，输入框中已写好的内容不再丢失，切回来后草稿还在。

## 原始内容
**Commit**: fix: preserve /chat draft when switching agents (#1389)  
**PR Body**:  
切换 Agent 时保留 /chat 输入框的草稿内容（存入 sessionStorage）。修复此前切换 Agent 会清空草稿的问题，仅在发送后或用户手动清空时才清除草稿。新增 GenClawInput 草稿恢复和清除行为的单元测试。
