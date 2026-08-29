---
title: "Agent Builder 项目列表整行可点，操作列不再挤成一团"
type: "体验优化"
priority: "低"
date: "2026-08-28"
status: "待审核"
channels: ""
---

# Agent Builder 项目列表整行可点，操作列不再挤成一团

## 核心宣传点

项目列表以前同时提供整行进入编辑器、Edit 按钮和 Chat 快捷按钮三个入口，操作列拥挤、表头也难对齐。现在整行点击就能进编辑器，More 保留为唯一的显式行操作。同时收拾了一批视觉细节：列宽和行间距重排、骨架屏更贴合真实内容、Hover 填充减轻、项目名称去掉链接下划线、创建卡片的箭头不再贴着边缘，「我的 Agent」范围计数也从对比度不足的矩形改成了更清楚的圆形徽标。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `eea665533acbffb5379281550557ec659487e85b`
- PR: #3572
- 作者: lynn Zhuang
- 日期: 2026-08-28T10:52:06Z

### Commit Message

```
fix(agent-builder): 优化agent builder 项目列表交互 (#3572)

## 变更概要
- Agent Builder 项目列表支持点击整行进入编辑器，并将 More 保留为唯一显式行操作
- 优化列表列宽、行间距、骨架屏、Hover 表面、创建卡片箭头间距和项目标题样式
- 将“我的 Agent”范围计数优化为对比度更清晰的圆形徽标

## 问题原因
项目列表同时提供整行编辑入口以及 Edit、Chat 快捷按钮，导致操作列拥挤且表头难以稳定对齐。部分交互表面也存在视觉层级问题，包括过重的
Hover 填充、项目名称的链接下划线、对比度不足的矩形计数徽标，以及距离卡片边缘过近的箭头。

## 测试计划
- [x] `bash scripts/verify-web.sh <本次变更的 Agent Builder 文件>`
- [x] `bash scripts/verify-changed.sh`
- [x] 93 个 Agent Builder 定向单元测试
- [x] 在本地浏览器中手动验证整行点击、More 对齐、Hover 透明度、箭头边距、标题装饰和计数徽标尺寸
```

### PR Description

```
## 变更概要
- Agent Builder 项目列表支持点击整行进入编辑器，并将 More 保留为唯一显式行操作
- 优化列表列宽、行间距、骨架屏、Hover 表面、创建卡片箭头间距和项目标题样式
- 将“我的 Agent”范围计数优化为对比度更清晰的圆形徽标

## 问题原因
项目列表同时提供整行编辑入口以及 Edit、Chat 快捷按钮，导致操作列拥挤且表头难以稳定对齐。部分交互表面也存在视觉层级问题，包括过重的 Hover 填充、项目名称的链接下划线、对比度不足的矩形计数徽标，以及距离卡片边缘过近的箭头。

## 测试计划
- [x] `bash scripts/verify-web.sh <本次变更的 Agent Builder 文件>`
- [x] `bash scripts/verify-changed.sh`
- [x] 93 个 Agent Builder 定向单元测试
- [x] 在本地浏览器中手动验证整行点击、More 对齐、Hover 透明度、箭头边距、标题装饰和计数徽标尺寸

```
