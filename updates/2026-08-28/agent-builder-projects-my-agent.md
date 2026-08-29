---
title: "Agent Builder 改为「项目」制，新增 My Agent 页面，Marketplace 只留公开市场"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-28"
status: "待审核"
channels: ""
---

# Agent Builder 改为「项目」制，新增 My Agent 页面，Marketplace 只留公开市场

## 核心宣传点

Agent Builder 里的构建会话正式改名为「项目」，「从空白创建」和「从现有 Agent 创建」两个入口直接摆在 Builder 首页，不用再进二级页面找。新增的 My Agent 页面把你的 Agent 分成「Owned by me」和「Shared with me」两栏：所有已发布的 Agent（不论发布范围）都会出现在 Owned by me，没发布的草稿仍然只作为项目留在 Agent Builder 首页，两边职责终于分清楚了。Agent Marketplace 则收窄为纯粹的公开 Agent 市场，不再混着你自己的东西。创建卡片、状态标签、详情字段、复制按钮和弹窗操作区也全部按 ZooWork Design System 重做了一遍。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `4e00d51e0d5ee9e7c68a72564d8e06d3c4d613dc`
- PR: #3554
- 作者: lynn Zhuang
- 日期: 2026-08-28T03:48:39Z

### Commit Message

```
feat(agent-builder): agent builder 和 marketplace 优化 (#3554)

## 改动概要

- 将 Agent Builder 中的构建会话重新定义为项目，并把“从空白创建”和“从现有 Agent 创建”两种入口直接放到 Builder
首页。
- 新增 My Agent 页面，分别展示 Owned by me 和 Shared with me；Owned by me
包含所有已发布范围的 Agent，未发布的草稿仍仅作为项目保留在 Agent Builder 首页。
- Agent Marketplace 仅保留公开 Agent 市场，并抽取 Marketplace 与 My Agent 共用的目录展示能力。
- 按照 ZooWork Design System 统一创建卡片、状态标签、详情字段、复制操作和弹窗操作区的样式。

## 测试计划

- [x] `bash scripts/verify-changed.sh`
- [x] 相关 Web 单元测试：36 个文件，473 项测试通过
- [x] Agent Builder / My Agent 定向单元测试：2 个文件，41 项测试通过
- [x] `pnpm --filter @zooclaw/design-system test`：53 个文件，306 项测试通过
- [x] `pnpm --filter @zooclaw/chat-ui test`：33 个文件，441 项测试通过
- [x] 在本地 Mock 预览中手动验证 Agent Builder、My Agent 的 Tab 与卡片、Agent 详情弹窗和
Agent Marketplace

## 备注

- 本次仅涉及前端与本地 Mock 预览，不修改后端 API 契约。
- 验证前已将分支 rebase 到最新的 `origin/main`。
- 按仓库排除规则统计，本次完整迁移共 3,934 行；Builder 路由、My Agent 范围和公开 Marketplace
目录保持在同一个 PR 中，避免出现功能不一致的中间状态。
<img width="2572" height="1986" alt="image"
src="https://github.com/user-attachments/assets/770ddb54-8732-426f-a5e7-f76675a49b10"
/>
<img width="2574" height="1998" alt="image"
src="https://github.com/user-attachments/assets/52db2006-40f6-4cbc-91ff-64f41429376f"
/>
<img width="2568" height="1998" alt="image"
src="https://github.com/user-attachments/assets/6d7a50d2-c283-4855-9870-17231a801491"
/>
![Uploading image.png…]()

![Uploading 3eb44054-4528-4cf9-8afe-945114c5d7d8.jpeg…]()
```

### PR Description

```
## 改动概要

- 将 Agent Builder 中的构建会话重新定义为项目，并把“从空白创建”和“从现有 Agent 创建”两种入口直接放到 Builder 首页。
- 新增 My Agent 页面，分别展示 Owned by me 和 Shared with me；Owned by me 包含所有已发布范围的 Agent，未发布的草稿仍仅作为项目保留在 Agent Builder 首页。
- Agent Marketplace 仅保留公开 Agent 市场，并抽取 Marketplace 与 My Agent 共用的目录展示能力。
- 按照 ZooWork Design System 统一创建卡片、状态标签、详情字段、复制操作和弹窗操作区的样式。

## 测试计划

- [x] `bash scripts/verify-changed.sh`
- [x] 相关 Web 单元测试：36 个文件，473 项测试通过
- [x] Agent Builder / My Agent 定向单元测试：2 个文件，41 项测试通过
- [x] `pnpm --filter @zooclaw/design-system test`：53 个文件，306 项测试通过
- [x] `pnpm --filter @zooclaw/chat-ui test`：33 个文件，441 项测试通过
- [x] 在本地 Mock 预览中手动验证 Agent Builder、My Agent 的 Tab 与卡片、Agent 详情弹窗和 Agent Marketplace

## 备注

- 本次仅涉及前端与本地 Mock 预览，不修改后端 API 契约。
- 验证前已将分支 rebase 到最新的 `origin/main`。
- 按仓库排除规则统计，本次完整迁移共 3,934 行；Builder 路由、My Agent 范围和公开 Marketplace 目录保持在同一个 PR 中，避免出现功能不一致的中间状态。
<img width="2572" height="1986" alt="image" src="https://github.com/user-attachments/assets/770ddb54-8732-426f-a5e7-f76675a49b10" />
<img width="2574" height="1998" alt="image" src="https://github.com/user-attachments/assets/52db2006-40f6-4cbc-91ff-64f41429376f" />
<img width="2568" height="1998" alt="image" src="https://github.com/user-attachments/assets/6d7a50d2-c283-4855-9870-17231a801491" />
![Uploading image.png…]()

![Uploading 3eb44054-4528-4cf9-8afe-945114c5d7d8.jpeg…]()

```
