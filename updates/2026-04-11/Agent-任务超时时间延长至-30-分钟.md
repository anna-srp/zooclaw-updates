---
title: "Agent 任务超时时间延长至 30 分钟"
type: "Bug Fix"
priority: "中"
date: "2026-04-11"
status: "待审核"
channels: ""
---

# Agent 任务超时时间延长至 30 分钟

## 核心宣传点

复杂长任务不再被超时打断，Agent 能完整执行更复杂的工作

## 原始内容

openclaw-docker v2026.3.13.35: agent 运行时配置 — agents.defaults.timeoutSeconds: 1800（30分钟），原默认 timeout 过短，复杂任务易被打断；升至 30 分钟后长任务可跑完

