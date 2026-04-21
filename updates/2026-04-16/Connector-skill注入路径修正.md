---
title: "Connector skill 注入路径修正至 ~/.agents/skills"
type: "Bug Fix"
priority: "低"
date: "2026-04-16"
status: "待审核"
channels: ""
---
# Connector skill 注入路径修正至 ~/.agents/skills

## 核心宣传点
修复了 Nango connector skill 注入到错误路径的问题，现在统一注入至 ~/.agents/skills，connector 技能加载更可靠。

## 原始内容
fix: change connector skill injection path to ~/.agents/skills (#878)

将 Nango connector skill 注入路径从 ~/.openclaw/skills 改为 ~/.agents/skills，与平台约定保持一致。
