---
title: "聊天输入框统一，Connectors 改为弹窗打开"
type: "体验优化"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 聊天输入框统一，Connectors 改为弹窗打开

## 核心宣传点

New Task、会话与 Agent Builder 的输入框样式终于统一；点「添加」直接弹窗打开 Connectors，暗色模式下模型图标也不再消失。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`3d39daf86a857ce4b1a0c0df2008aa0b4692f9ad`
- 作者：lynn Zhuang
- 日期：2026-08-05T07:20:17Z
- PR：#3226

### Commit Message

```
fix(chat): 统一聊天输入框样式与连接器交互 (#3226)

## 改动说明

- 基于共享的 `UnifiedChatComposer`，统一 New Task、Chat Session 和 Agent Builder
中的聊天输入框样式
- 将 Chat Session 的发送按钮图标和输入框卡片样式与 New Task 对齐，并将输入框距页面底部的间距从 48px 减少到
24px
- 点击输入框的添加菜单后，以懒加载的 Skill Store 尺寸弹窗打开 Connectors，并复用 #3220 的响应式布局
- 修复暗色模式下部分模型厂商图标不可见的问题，同时保留不同输入框场景所需的发送按钮样式
- 移除从 #3230 迁入、但与本任务无关的 Agent Builder 布局改动

## 问题原因

New Task、Chat Session 和 Agent Builder
原先分别使用不同的输入框变体和局部样式覆盖，导致输入框高度、底部间距、发送按钮图标与模型展示逐渐不一致。Connectors
入口原先还采用独立页面跳转，没有复用已有的弹窗交互。

## 验证结果

- [x] 共享输入框与 Connector 相关定向测试通过：6 个测试文件，共 140 个测试
- [x] Agent Builder 输入框相关定向测试通过：2 个测试文件，共 45 个测试
- [x] 合并最新 `main` 后运行 `bash
scripts/verify-changed.sh`，TypeScript、代码治理检查与 ESLint 均通过
- [x] 已手动预览 `/new-chat` 和
`/chat/mock-workspace-main/sessions/main-session-1`，确认输入框、添加菜单与
Connectors 入口样式
- [ ] Agent Builder 项目页的浏览器预览受仓库 mock 后端限制：mock 尚未实现最新的
`/agent-builder/entry/*` 接口；相关单元测试与静态检查均已通过

## 预览效果

输入框点击“添加”后，Connector 以弹窗形式打开：

<img width="2570" height="1842" alt="Connector 弹窗预览"
src="https://github.com/user-attachments/assets/09ce9881-879d-464d-8473-d82caa2a2ef7"
/>
```

### PR Body

## 改动说明

- 基于共享的 `UnifiedChatComposer`，统一 New Task、Chat Session 和 Agent Builder 中的聊天输入框样式
- 将 Chat Session 的发送按钮图标和输入框卡片样式与 New Task 对齐，并将输入框距页面底部的间距从 48px 减少到 24px
- 点击输入框的添加菜单后，以懒加载的 Skill Store 尺寸弹窗打开 Connectors，并复用 #3220 的响应式布局
- 修复暗色模式下部分模型厂商图标不可见的问题，同时保留不同输入框场景所需的发送按钮样式
- 移除从 #3230 迁入、但与本任务无关的 Agent Builder 布局改动

## 问题原因

New Task、Chat Session 和 Agent Builder 原先分别使用不同的输入框变体和局部样式覆盖，导致输入框高度、底部间距、发送按钮图标与模型展示逐渐不一致。Connectors 入口原先还采用独立页面跳转，没有复用已有的弹窗交互。

## 验证结果

- [x] 共享输入框与 Connector 相关定向测试通过：6 个测试文件，共 140 个测试
- [x] Agent Builder 输入框相关定向测试通过：2 个测试文件，共 45 个测试
- [x] 合并最新 `main` 后运行 `bash scripts/verify-changed.sh`，TypeScript、代码治理检查与 ESLint 均通过
- [x] 已手动预览 `/new-chat` 和 `/chat/mock-workspace-main/sessions/main-session-1`，确认输入框、添加菜单与 Connectors 入口样式
- [ ] Agent Builder 项目页的浏览器预览受仓库 mock 后端限制：mock 尚未实现最新的 `/agent-builder/entry/*` 接口；相关单元测试与静态检查均已通过

## 预览效果

输入框点击“添加”后，Connector 以弹窗形式打开：

<img width="2570" height="1842" alt="Connector 弹窗预览" src="https://github.com/user-attachments/assets/09ce9881-879d-464d-8473-d82caa2a2ef7" />


