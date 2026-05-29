---
title: "Specialist Agent 快捷指令不再被截断，全部显示"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# Specialist Agent 快捷指令不再被截断，全部显示

## 核心宣传点

Specialist 配置的所有快捷指令现在都会在对话界面显示，不再被限制为最多 4 条，支持更灵活的功能入口展示。

## 原始内容

feat(web): render all configured Specialist quick commands (#2050)

跟进已合并的 #2021（main Assistant 快捷指令重做）：移除 MAX_QUICK_COMMAND_COUNT 与 configuredCommands.slice(0, 4)，Specialist 后端配置的 quick_commands 不再被静默截断到 4 个，全部渲染。dropdown 宽度改为自适应 max-w-[min(42rem,var(--radix-dropdown-menu-content-available-width))]：桌面端 cap 在 42rem，让多个 chip 换成紧凑多行块而非拉满整屏；窄屏自动收缩到视口宽度。
