---
title: "首页移除 H1 下方的说明段落"
type: "体验优化"
priority: "低"
date: "2026-07-23"
status: "待审核"
channels: ""
---

## 核心宣传点

根据产品反馈，首页大标题（H1）下方那段说明文字已移除，页面更简洁。不影响首页标题、搜索用的 Meta 描述、任务输入框、快捷操作和页脚布局。

## 原始内容

**PR #3034 — fix(web): remove homepage hero description**
SHA: 131a4cd8acd40bdaae9c04416b54c18ef20aee1a ｜ 作者: Mori-srp

- Remove the visible homepage paragraph below the H1 after product feedback confirmed it is not needed.
- Remove the now-unused `landingV2.heroDescription` copy from all 10 locale dictionaries.
- Update the landing hero unit test to preserve the single `main` / single H1 contract and assert that the removed description is not rendered.

### Why
The paragraph was introduced in #2962 as proposed SEO-readable supporting copy rather than approved product messaging. The latest product review asked to remove it. The homepage Meta Description remains unchanged.
