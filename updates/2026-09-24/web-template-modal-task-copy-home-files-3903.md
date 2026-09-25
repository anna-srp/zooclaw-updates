---
title: "模板弹窗底部加渐隐、侧栏改为 Recent tasks，首页去掉重复的 Agent 模块"
type: "体验优化"
priority: "中"
date: "2026-09-24"
status: "待审核"
channels: ""
---

# 模板弹窗底部加渐隐、侧栏改为 Recent tasks，首页去掉重复的 Agent 模块

## 核心宣传点

一组前端展示优化。模板选择弹窗底部加了 32px 渐隐和留白，只在下方还有内容时出现，滚到底就去掉渐隐、把最后一排卡片完整露出来——之前列表在滚动容器边界直接被切掉，过渡很突兀。Agent 侧栏的 Recents 改成 Recent tasks，中文和空状态文案同步统一成「任务」的说法，和新建入口的命名对齐。首页保留 Most Used Agents，移除了重复的 Agents You Recently Chatted With 模块以及它专用的排序、文案和双列布局逻辑（这两组本来基于同一份数据排序，很容易展示成一样的内容），Recent Activity 和 Schedule 都保留。Artifacts 浏览页去掉了来源 Tab，直接加载 AI 生成的文件，页面说明同步调整，聊天附件选择器的来源切换保持原样。纯前端展示调整，模板仍从现有 API 取真实内容，无后端或模板目录数据变更。

## 分级

- 内部：P2
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## 修改内容

- 模板选择弹窗底部增加 32px 渐隐和留白，仅在下方仍有内容时显示；滚到底后移除渐隐，完整展示最后一排卡片。
- Agent 侧栏将 `Recents` 改为 `Recent tasks`，中文及空状态同步统一为任务表述。
- 首页保留 `Most Used Agents`，移除重复的 `Agents You Recently Chatted With` 模块，并清理其专用排序、文案和双列布局逻辑；保留 `Recent Activity` 和 `Schedule`。

- Artifacts 浏览页移除来源 Tab，直接加载 AI 生成文件；页面说明同步调整，聊天附件选择器维持原有来源切换。

## 原因与范围

模板列表原先在滚动容器边界直接裁切，视觉过渡突兀；侧栏的新建入口与历史列表命名不一致；首页两组 Agent 基于同一份数据排序，容易出现重复展示。

仅调整前端展示，模板继续从现有 API 获取真实内容，无后端或模板目录数据变更。

## 验证

- Artifacts 页面和附件选择器相关 9 项测试通过。
- TypeScript、ESLint、仓库前端治理检查通过。
- 模板弹窗和侧栏相关 23 项测试通过；首页相关 155 项测试通过。
- 浏览器验证内容不足一屏、桌面溢出、滚到底、手机宽度变化等状态。
- 已启动连接真实 staging 后端的本地预览，用户确认展示效果。


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `9367ad27376a384c638b8ceffbb0a02f94dc2569`
- PR: #3903
- 作者：lynn Zhuang
- 日期：2026-09-24T11:13:20Z

### Commit Message

```
fix(web): 优化模板弹窗、任务文案及首页与文件页展示 (#3903)

## 修改内容

- 模板选择弹窗底部增加 32px 渐隐和留白，仅在下方仍有内容时显示；滚到底后移除渐隐，完整展示最后一排卡片。
- Agent 侧栏将 `Recents` 改为 `Recent tasks`，中文及空状态同步统一为任务表述。
- 首页保留 `Most Used Agents`，移除重复的 `Agents You Recently Chatted With`
模块，并清理其专用排序、文案和双列布局逻辑；保留 `Recent Activity` 和 `Schedule`。

- Artifacts 浏览页移除来源 Tab，直接加载 AI 生成文件；页面说明同步调整，聊天附件选择器维持原有来源切换。

## 原因与范围

模板列表原先在滚动容器边界直接裁切，视觉过渡突兀；侧栏的新建入口与历史列表命名不一致；首页两组 Agent
基于同一份数据排序，容易出现重复展示。

仅调整前端展示，模板继续从现有 API 获取真实内容，无后端或模板目录数据变更。

## 验证

- Artifacts 页面和附件选择器相关 9 项测试通过。
- TypeScript、ESLint、仓库前端治理检查通过。
- 模板弹窗和侧栏相关 23 项测试通过；首页相关 155 项测试通过。
- 浏览器验证内容不足一屏、桌面溢出、滚到底、手机宽度变化等状态。
- 已启动连接真实 staging 后端的本地预览，用户确认展示效果。
```

来源：SerendipityOneInc/ecap-workspace @ 9367ad27，PR #3903，作者 lynn Zhuang。