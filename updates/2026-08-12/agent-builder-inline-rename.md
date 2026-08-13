---
title: "Agent Builder 聊天页支持直接改名"
type: "体验优化"
priority: "中"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# Agent Builder 聊天页支持直接改名

## 核心宣传点

在 Agent Builder 的对话页顶部点一下就能改 Agent 名字，失焦或回车保存、Esc 取消，不用再退回列表页操作。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e1ae26e5a06075243742e0f41ef416fc3e0411dc`
- PR: #3351

### Commit Message

```
feat(agent-builder): Agent builder 支持聊天页内联重命名 (#3351)

## Linear

N/A

## 变更摘要

- 参考 PR #3192，在 Agent Builder 聊天页顶部增加 Agent 名称内联重命名，支持点击全选、失焦或 Enter
保存、Escape 取消、中文输入法保护以及保存失败后保留草稿
- 根据当前 v1/v2 运行时调用对应的重命名接口，同步当前项目缓存并刷新首页列表；编辑期间暂时隐藏状态 Tag
- 在标题末尾使用渐变遮罩叠加 hover 铅笔，缩短标题与状态 Tag 的间距；同时将 Agent Builder 首页 Rename
菜单换成单支铅笔图标

## 测试计划

- [x] `bash scripts/verify-web.sh <本次变更的 Web 文件>`：TypeScript、103
个定向测试、ESLint 和治理检查通过
- [x] `bash scripts/verify-changed.sh`：变更 surface 的前端检查通过
- [x] 本地 mock 浏览器验证：hover/focus 铅笔、点击全选、失焦保存、Escape 取消、状态 Tag 显隐、渐变间距及首页
Rename 图标
```

### PR Body

## Linear

N/A

## 变更摘要

- 参考 PR #3192，在 Agent Builder 聊天页顶部增加 Agent 名称内联重命名，支持点击全选、失焦或 Enter 保存、Escape 取消、中文输入法保护以及保存失败后保留草稿
- 根据当前 v1/v2 运行时调用对应的重命名接口，同步当前项目缓存并刷新首页列表；编辑期间暂时隐藏状态 Tag
- 在标题末尾使用渐变遮罩叠加 hover 铅笔，缩短标题与状态 Tag 的间距；同时将 Agent Builder 首页 Rename 菜单换成单支铅笔图标

## 测试计划

- [x] `bash scripts/verify-web.sh <本次变更的 Web 文件>`：TypeScript、103 个定向测试、ESLint 和治理检查通过
- [x] `bash scripts/verify-changed.sh`：变更 surface 的前端检查通过
- [x] 本地 mock 浏览器验证：hover/focus 铅笔、点击全选、失焦保存、Escape 取消、状态 Tag 显隐、渐变间距及首页 Rename 图标


---
