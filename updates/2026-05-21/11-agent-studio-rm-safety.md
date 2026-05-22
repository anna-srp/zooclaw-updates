---
title: "Agent Studio 安全加固：禁止静默删除文件"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-21"
status: "待审核"
channels: "Discord, changelog"
---

# Agent Studio 安全加固：禁止静默删除文件

## 核心宣传点

Agent Studio 现在会在删除文件前要求明确确认，防止 AI 误删重要文件。

## 原始内容

```
fix(agent-studio): forbid silent rm; require approval for plain rm (#138)

- Forbid silent `rm` commands that could accidentally delete files without user awareness
- Require explicit approval before executing plain `rm` operations
- Adds safety guardrails to prevent AI-initiated file deletions

PR Description: This change ensures Agent Studio cannot silently delete files. The `rm` command now requires explicit user approval, preventing accidental data loss during automated tasks.
```
