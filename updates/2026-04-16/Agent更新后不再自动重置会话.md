---
title: "Agent 更新后不再自动重置会话，需用户手动确认"
type: "Bug Fix"
priority: "中"
date: "2026-04-16"
status: "待审核"
channels: "Discord+changelog"
---
# Agent 更新后不再自动重置会话，需用户手动确认

## 核心宣传点
Agent 更新/Redeploy 后不再自动发送 /new 重置当前会话，用户可以继续原有对话，避免意外丢失上下文。

## 原始内容
fix(agents-manager): require explicit session reset after updates (#879)

停止在 redeploy 后自动 POST /new，改为要求用户显式触发 session reset。保留 redeploy 文件，确保更新内容不被覆盖。
