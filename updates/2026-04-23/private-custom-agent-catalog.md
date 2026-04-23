---
title: "支持私有自定义 Agent 目录"
type: "新功能上线"
priority: "高"
date: "2026-04-23"
status: "待审核"
channels: ""
---
# 支持私有自定义 Agent 目录

## 核心宣传点
新增 owner 级别的私有 Agent 目录，支持读取和完整 CRUD 操作，团队可以管理自己专属的私有 Agent 列表，不对外公开。

## 原始内容
feat(openclaw): add private custom agent catalog flow (#1147)

Add owner-scoped private custom agent catalog reads and CRUD endpoints. Agents in private catalog are only visible to the owner.
