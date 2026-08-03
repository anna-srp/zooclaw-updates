---
title: "任务卡片交互优化：一键带入 Prompt 与 Agent"
type: "体验优化"
priority: "中"
外部: "B"
date: "2026-07-31"
status: "待审核"
channels: ""
---

## 核心宣传点

点击示例任务卡片时会同时带入对应的 Prompt 和 Agent，未雇佣的 Agent 会自动完成雇佣并发送；雇佣进度用一个统一 Toast 展示「检查→雇佣→启动」，失败时保留你的输入并可一键重试，交互更顺畅、不再丢内容。

## 原始内容

**fix(chat): 同步任务卡片的提示词、Agent、模型与分类布局 (#3153)**

- SHA: `6600fd431de5750275a93f5bc64b4d6f856f4831`
- PR: #3153
- 日期: 2026-07-31T09:43:28Z

（本次仅为 frontmatter 补充外部等级字段；完整 commit / PR 正文见仓库历史。核心变更：统一示例卡片的 Prompt/Agent/模型带入逻辑，自动 Hire 流程用单一可更新 Toast 展示进度，失败保留输入并可重试，computer runtime 显式模型写入等待重启 ready 后再发送。）
