---
title: "首页 Hero 输入框体验优化：保留提示词、智能推荐专家、默认模型更新"
type: "体验优化"
priority: "中"
date: "2026-07-23"
status: "待审核"
channels: ""
---

## 核心宣传点

首页的任务输入框更聪明了：现在你选好的提示词在切换不同专家（specialist）时会保留，不会被覆盖；选了幻灯片模板会自动推荐 PPT Master 专家；默认模型更新为 Claude Sonnet 5，模型倍率与公布值对齐；「Build Agents」分类补齐了中文翻译。

## 原始内容

**PR #3042 — fix(landing): refine hero composer behavior**
SHA: 8dd1b8eca0218ee3019d71de2aeaa56142607eed ｜ 作者: shana-srp

- keep the selected landing-page prompt while allowing visitors to switch specialists
- recommend PPT Master when a slide template is selected
- set Claude Sonnet 5 as the default model and align model multipliers with the published values
- translate the Build Agents category in Chinese

### Root cause
The prompt recommendation always took precedence over a visitor's explicit specialist choice, while template-only selection had no displayed specialist fallback. The landing model metadata and Chinese category copy were also stale.
