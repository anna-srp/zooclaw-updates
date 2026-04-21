---
title: "用 IQ 进度条直观展示 AI 能力状态"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-21"
status: "待审核"
channels: "站内弹窗+Discord"
---

# 用 IQ 进度条直观展示 AI 能力状态

## 核心宣传点

当积分不足使用基础模型时，界面不再显示难懂的文字提示，而是以渐变色 IQ 进度条直观表示 AI 当前的能力水位，让你一眼了解当前 AI 的"聪明程度"。

## 原始内容

feat(web): replace degraded banner with IQ bar (#1123)

## Summary
- Replace the text-only "积分已用完，正在使用基础模型运行中" degraded banner with a visual intelligence bar (gradient red→green, indicator at 25/100)
- New messaging: "AI 变笨了" / "AI is underpowered" — users immediately understand quality trade-off instead of being confused by "basic model" wording
- Theme-aware: IQ bar gradient colors defined as CSS vars (ecap-iq-bar-*) with dark mode support
- 3 new i18n keys (degradedTitle, degradedScore, boostAI) across all 7 languages
