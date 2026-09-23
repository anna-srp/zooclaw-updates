---
title: "Agent 设置面板优化：Skills / 知识源 / Connectors / MCP 样式统一，添加弹窗交互更稳"
type: "体验优化"
priority: "中"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# Agent 设置面板优化：Skills / 知识源 / Connectors / MCP 样式统一，添加弹窗交互更稳

## 核心宣传点

Agent 设置面板里 Skills、Knowledge Sources、Connectors 和 MCP 四类资源的展示和交互按设计稿统一了图标、行高、间距和操作按钮。全局 Knowledge 保持卡片布局并换用新的书本图标。资源行现在会明确显示 Connect / Connected 状态，支持连接、断开以及 Save / Undo，连接前会校验最新的资源目录，遇到未授权的资源会引导去全局库里配置。四类添加弹窗的组件、宽度、标题、内容和底部操作区做成一致的；点遮罩或按 Escape 不会误关弹窗，关闭按钮和明确的取消/确认操作都保留。已添加 Skill 的列表样式也优化了，三点菜单改成单行短文案 Manage / 管理。注意 ZIP 上传仍保持原有的禁用状态，这次没有实现上传后端。

## 分级

- 内部：P1
- 外部：C
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## 修改内容

优化 Agent 设置面板中 Skills、Knowledge Sources、Connectors 和 MCP
的展示及交互，按设计稿统一图标、行高、间距和操作按钮。

- 全局 Knowledge 保持卡片布局，使用新的书本图标；修正本地 mock 数据导致误入旧版列表的问题。
- 资源行展示 Connect / Connected 状态，支持连接、断开及 Save /
Undo；连接前校验最新资源目录。未授权资源引导至全局库配置。
- 统一四类添加弹窗的组件、宽度、标题、内容和底部操作区；点击遮罩或按 Escape 不关闭，保留关闭按钮及明确的取消/确认操作。
- 优化已添加 Skill 的列表样式；三点菜单使用单行短文案 Manage / 管理。

## 验证

- TypeScript、ESLint 及前端治理检查通过。
- 资源行、连接草稿、弹窗关闭行为和 mock 数据及设置页签相关的 27 项单元测试通过。
- 本地预览已检查全局 Knowledge 卡片、Agent 资源行、添加弹窗及含三个 Skill 的状态。
- Skill 示例仅存在于本地 mock 数据中；ZIP 上传功能仍保持原有禁用状态，本 PR 不实现上传后端。

## 设计与范围

[Figma
设计稿](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=976-4676)

涉及前端、共享设计系统、相关测试及 mock 数据，无后端接口变更。


## 分支同步

已合入 2026-09-22 拉取的最新 main（`fbd175874`），合并提交为
`a510248f0`，无冲突；合并后相关测试、TypeScript 和 ESLint 均通过。


## 公共组件焦点样式


统一移除双层焦点框，键盘焦点使用单条内侧细线，保留鼠标操作后的焦点抑制及菜单正常焦点恢复；输入框组合仅在外层提示焦点。该公共样式同时覆盖使用设计系统样式的其他页面。

验证：设计系统 354 项测试、TypeScript 和 ESLint 通过；本地预览检查了菜单关闭后的效果。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `e63c6a8627ac59e9ee7b060b2b07b70aca78d563`
- PR: #3844
- 作者：lynn Zhuang
- 日期：2026-09-22T06:33:04Z

### Commit Message

```
fix(agents): agent设置面板资源样式与添加弹窗交互 (#3844)

## 修改内容

优化 Agent 设置面板中 Skills、Knowledge Sources、Connectors 和 MCP
的展示及交互，按设计稿统一图标、行高、间距和操作按钮。

- 全局 Knowledge 保持卡片布局，使用新的书本图标；修正本地 mock 数据导致误入旧版列表的问题。
- 资源行展示 Connect / Connected 状态，支持连接、断开及 Save /
Undo；连接前校验最新资源目录。未授权资源引导至全局库配置。
- 统一四类添加弹窗的组件、宽度、标题、内容和底部操作区；点击遮罩或按 Escape 不关闭，保留关闭按钮及明确的取消/确认操作。
- 优化已添加 Skill 的列表样式；三点菜单使用单行短文案 Manage / 管理。

## 验证

- TypeScript、ESLint 及前端治理检查通过。
- 资源行、连接草稿、弹窗关闭行为和 mock 数据及设置页签相关的 27 项单元测试通过。
- 本地预览已检查全局 Knowledge 卡片、Agent 资源行、添加弹窗及含三个 Skill 的状态。
- Skill 示例仅存在于本地 mock 数据中；ZIP 上传功能仍保持原有禁用状态，本 PR 不实现上传后端。

## 设计与范围

[Figma
设计稿](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=976-4676)

涉及前端、共享设计系统、相关测试及 mock 数据，无后端接口变更。


## 分支同步

已合入 2026-09-22 拉取的最新 main（`fbd175874`），合并提交为
`a510248f0`，无冲突；合并后相关测试、TypeScript 和 ESLint 均通过。


## 公共组件焦点样式


统一移除双层焦点框，键盘焦点使用单条内侧细线，保留鼠标操作后的焦点抑制及菜单正常焦点恢复；输入框组合仅在外层提示焦点。该公共样式同时覆盖使用设计系统样式的其他页面。

验证：设计系统 354 项测试、TypeScript 和 ESLint 通过；本地预览检查了菜单关闭后的效果。
```

来源：SerendipityOneInc/ecap-workspace @ e63c6a86，PR #3844，作者 lynn Zhuang。
