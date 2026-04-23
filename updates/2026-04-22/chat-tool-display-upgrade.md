---
title: "聊天工具调用展示升级：更丰富的文字、emoji、折叠和计时器"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-22"
status: "待审核"
channels: ""
---

# 聊天工具调用展示升级：更丰富的文字、emoji、折叠和计时器

## 核心宣传点

聊天界面中 Agent 调用工具的展示全面升级：动作描述更丰富、支持折叠、显示耗时计时器，让你清楚知道 Agent 在做什么。

## 原始内容

feat(web): enrich chat tool display — richer text, emoji, collapse, timer (#1100)

Expand action text variants from 4→8 per tool type with longer narrative phrasing; add withQuery for exec/process/write so all tools carry context. Add emoji prefixes, collapsible sections, and elapsed-time timer for long-running tool calls.
