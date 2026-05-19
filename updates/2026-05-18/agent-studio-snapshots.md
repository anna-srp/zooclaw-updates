---
title: "Agent Studio 新增多 Agent 管理：/studio list 和 /studio open 命令上线"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-18"
status: "待审核"
channels: ""
---
# Agent Studio 新增多 Agent 管理：/studio list 和 /studio open 命令上线

## 核心宣传点
Agent Studio 现在支持管理多个 Agent Pack，通过 `/studio list` 查看所有已创建的 Agent，用 `/studio open <名字>` 随时切换回任意 Agent 继续编辑，不再担心新建时丢失之前的工作。

## 原始内容

**Commit**: `535a7f9f` | ecap-agent-pack | 2026-05-18T08:03:36Z  
**PR**: #130 | feat(agent-studio): multi-agent workflow via snapshots (/studio list, /studio open)

---

### 解决的核心痛点

**以前**：在 Agent Studio 中新建一个 Agent 需要 `/studio new`，这会清空工作区，丢失之前 Agent 的可编辑状态。之后想回来修改之前的 Agent 只能从头重建。

**现在**：
- **`/studio list`**：列出你所有已创建的 Agent Pack（包含阶段、最后修改时间、描述）
- **`/studio open <名字>`**：恢复任意 Agent 的完整工作区，包括 Studio 的叙事记忆 `context.md`
- **三个明确快照触发点**（不自动静默增长磁盘）：
  1. `/studio publish` 成功后
  2. `/studio new` 时工作区有未保存内容
  3. `/studio open` 时工作区有未保存内容

### 快照结构

```
snapshots/
  <pack-name>/
    context.md             ← 实时叙事，每个阶段门控时由 Studio 改写
    <version>/             ← 可编辑副本（每个发布/草稿版本一份）
      agent/ skills/ scripts/ data/
      context.md           ← publish 时的冻结归档副本
```

保留最多 5 个快照版本（草稿优先于正式版本被清理）。
