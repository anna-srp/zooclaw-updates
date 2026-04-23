---
title: "新功能：未雇佣 Agent 深链智能引导雇佣流程"
type: "新功能上线"
priority: "中"
date: "2026-04-22"
status: "待审核"
channels: ""
---

# 新功能：未雇佣 Agent 深链智能引导雇佣流程

## 核心宣传点

访问未雇佣 Agent 的深链不再静默回退，而是智能引导到 Agent Studio 雇佣流程，降低用户探索 Agent 的门槛。

## 原始内容

feat(chat): 深链未雇佣/未知 agent 跳转 Agent Studio hire 面板 (#1020)

/chat?agent_id=<slug> 深链兜底改造，把原本「静默回退到 main agent」的断头路改成两条有意义的引导路径：
- 目标 slug 在 official catalog 但未雇佣 → toast 提示并跳转 hire 面板
- 未知 agent → 建议浏览 Agent Specialists Hub
