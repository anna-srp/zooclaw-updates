---
title: "修复 Agent Studio 积分耗尽时报错问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-21"
status: "待审核"
channels: "Discord, changelog"
---

# 修复 Agent Studio 积分耗尽时报错问题

## 核心宣传点

积分不足时，Agent Studio 现在会优雅降级到备用模型继续运行，而不是直接报错中断任务。

## 原始内容

```
fix(claw-interface): add Agent Studio model to degradation fallback table (#1815)

Root cause: Agent Studio uses internal model alias `agent-studio-sonnet-4-6` which was missing from MODEL_DEGRADATION_MAPPINGS. When user's credits are exhausted, billing-gateway has no fallback → request fails entirely → "Something went wrong while processing your request."

Fix: Add `agent-studio-sonnet-4-6: _CHAT_FALLBACK` (qwen35-122B) to the degradation mappings table, so Agent Studio degrades gracefully like all other chat agents.

Closes ECA-777
```
