---
title: "聊天页可以单独更新某个 Agent，侧边栏交互重做并支持会话归档"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-28"
status: "待审核"
channels: ""
---

# 聊天页可以单独更新某个 Agent，侧边栏交互重做并支持会话归档

## 核心宣传点

Chat Session 顶部新增了针对单个 Agent 的 Update 按钮，文案、按钮样式和更新状态与 Agent Marketplace 完全一致——发现某个 Agent 有新版本时不用再绕回市场页去更新。Agent 有可用更新时头像上会出现提示点，Chat Header、Marketplace、侧边栏三处共享同一份更新进度。侧边栏本身也重做了：Agent 行的 Hover 背景覆盖完整区域（包括 New Task 铅笔按钮），每个 Session 都有 Hover 背景，选中的 Session 在 Hover 时保持选中态只露出 More 按钮。Session 的 More 菜单精简为 Rename 和 Archive 两项（Pin 暂时移除），会话归档这次补齐了前端请求、后端 API 和多语言文案，可以真正用了。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `72eea03af29bc49cbea7ac3d1ca624fffeafbc8d`
- PR: #3573
- 作者: lynn Zhuang
- 日期: 2026-08-28T09:55:55Z

### Commit Message

```
feat(chat): 统一 Agent 更新与会话侧边栏交互 (#3573)

## 概要

- 在 Chat Session 顶部增加单个 Agent 的 **Update** 操作，并与 Agent Marketplace
统一文案、按钮样式与更新状态
- 优化侧边栏 Agent 与 Session 交互：更新提示、选中态、Hover 背景、More 菜单、Rename 和 Archive
- 补齐会话归档的前端请求、后端 API、Mock 场景和多语言文案

## 交互细节

- Update 按钮使用统一的品牌色和更新图标，与相邻工具按钮保持 12px 间距、8px 圆角
- Agent 行的 Hover 背景覆盖完整区域，包括 New Task 铅笔按钮；离开 Hover 后收起操作按钮
- 每个 Session 都有 Hover 背景；选中的 Session 在 Hover 时继续保持选中背景，只显示 More 按钮
- Session 的 More 菜单仅保留 Rename 和 Archive，暂时移除 Pin
- Agent 有可用更新时，在头像显示提示点，并在 Chat Header、Marketplace 和侧边栏共享一致的更新进度

## 验证

- `bash scripts/verify-web.sh --no-test`
- 前端目标测试：16 个测试文件、452 个用例通过
- 前端完整测试：678 个测试文件、9308 个用例通过；依赖本地监听端口的 Mock Backend 测试在非沙箱环境 34/34 通过
- `bash scripts/verify-py.sh`
- 后端目标测试：87/87 通过
- 本地浏览器验证了 Update/工具按钮样式、按钮间距、Session 选中态与 Hover 状态

<img width="2588" height="2102" alt="update1"
src="https://github.com/user-attachments/assets/20135f54-78cf-41e8-8ba1-8aa80bf59893"
/>
<img width="2584" height="1990" alt="image"
src="https://github.com/user-attachments/assets/536c4b71-65f9-42ed-bd02-874c6c5cb0c5"
/>
```

### PR Description

```
## 概要

- 在 Chat Session 顶部增加单个 Agent 的 **Update** 操作，并与 Agent Marketplace 统一文案、按钮样式与更新状态
- 优化侧边栏 Agent 与 Session 交互：更新提示、选中态、Hover 背景、More 菜单、Rename 和 Archive
- 补齐会话归档的前端请求、后端 API、Mock 场景和多语言文案

## 交互细节

- Update 按钮使用统一的品牌色和更新图标，与相邻工具按钮保持 12px 间距、8px 圆角
- Agent 行的 Hover 背景覆盖完整区域，包括 New Task 铅笔按钮；离开 Hover 后收起操作按钮
- 每个 Session 都有 Hover 背景；选中的 Session 在 Hover 时继续保持选中背景，只显示 More 按钮
- Session 的 More 菜单仅保留 Rename 和 Archive，暂时移除 Pin
- Agent 有可用更新时，在头像显示提示点，并在 Chat Header、Marketplace 和侧边栏共享一致的更新进度

## 验证

- `bash scripts/verify-web.sh --no-test`
- 前端目标测试：16 个测试文件、452 个用例通过
- 前端完整测试：678 个测试文件、9308 个用例通过；依赖本地监听端口的 Mock Backend 测试在非沙箱环境 34/34 通过
- `bash scripts/verify-py.sh`
- 后端目标测试：87/87 通过
- 本地浏览器验证了 Update/工具按钮样式、按钮间距、Session 选中态与 Hover 状态

<img width="2588" height="2102" alt="update1" src="https://github.com/user-attachments/assets/20135f54-78cf-41e8-8ba1-8aa80bf59893" />
<img width="2584" height="1990" alt="image" src="https://github.com/user-attachments/assets/536c4b71-65f9-42ed-bd02-874c6c5cb0c5" />

```
