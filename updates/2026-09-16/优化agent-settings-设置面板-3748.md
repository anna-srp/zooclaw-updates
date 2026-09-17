---
title: "feat(agents): 优化Agent Settings 设置面板 (#3748)"
type: "新功能"
priority: "高"
date: "2026-09-16"
status: "待审核"
channels: ""
---

# feat(agents): 优化Agent Settings 设置面板 (#3748)

## 核心宣传点

## 变更摘要

Agent 编辑页的设置原先使用弹窗，内容组织、间距与设计稿不一致。本次改为默认展开的右侧面板，按 Figma 拆分 Settings / Profile 两个 tab，并统一各模块的布局和交互。

- **Settings**：按设计稿调整 Agent Preferences、Skills 与 Danger zone；统一模块分割线、字号、浅灰色输入区域和按钮尺寸。
- **Profile**：对齐头像与名称、描述、Agent Details 和四个 Quick commands 的布局；显示创建者头像与相对更新时间；保留旧版超出四条命令的显式迁移提示。
- **编辑体验**：切换 tab 保留草稿；设置面板默认展开，展开/收起带过渡；折叠后简介和建议提示与输入框居中对齐。
- **顶部与创建流程**：标题统一为 Edit Agent，编辑历史移入 More 菜单；创建中的 loading 在原有区域覆盖显示，不再撑高弹窗。
- **复用现有入口**：Add skill 与 Skills 页面使用同一个 ZIP 上传弹窗；Instructions 和已有 Skill 的正文通过编辑弹窗修改。

## 设计稿

- [Settings（789:2094）](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=789-2094)
- [Profile（798:3511）](https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=798-3511)

## 能力边界

本次为前端面板和交互调整，没有新增后端能力。ZIP 上传沿用现有页面的预览状态，尚不可提交；Self-update 开关已移除；AI Skill Editing 显示为不可用。Knowledge Sources 与 Connectors 暂无 Agent 级后端支持，已移除模块和相关请求、弹窗。Tools 因缺少 Agent 级真实调用数据，暂不展示，也不保留占位提示。模型与用户资料使用实际数据，不硬编码设计稿示例。

## 验证

- 提交前全量 ESLint 通过。
- 已同步最新 main，治理检查、TypeScript 和变更文件 ESLint 通过。测试选择器扩展运行了 454 个文件：453 个通过，另一个文件的旧界面断言已更新，定向复跑 3 个用例全部通过。
- 本地浏览器检查 Settings / Profile、设置展开与收起、Instructions 编辑、共享 Skill 上传弹窗、资源模块及 Tools 区块移除。
- 检查 628px 面板及 390px 窄屏布局，无面板横向溢出；Profile 三个模块高度与设计稿对齐。
- 未运行本地生产构建，由 CI 继续验证。

## 部署

仅需前端部署。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `95f5c6d669e8940b607ccb48a066491aeb198806`
- PR: #3748
- 作者：lynn Zhuang
- 日期：2026-09-16T07:59:50Z

### Commit Message

```
feat(agents): 优化Agent Settings 设置面板 (#3748)

## 变更摘要

Agent 编辑页的设置原先使用弹窗，内容组织、间距与设计稿不一致。本次改为默认展开的右侧面板，按 Figma 拆分 Settings /
Profile 两个 tab，并统一各模块的布局和交互。

- **Settings**：按设计稿调整 Agent Preferences、Skills 与 Danger
zone；统一模块分割线、字号、浅灰色输入区域和按钮尺寸。
- **Profile**：对齐头像与名称、描述、Agent Details 和四个 Quick commands
的布局；显示创建者头像与相对更新时间；保留旧版超出四条命令的显式迁移提示。
- **编辑体验**：切换 tab 保留草稿；设置面板默认展开，展开/收起带过渡；折叠后简介和建议提示与输入框居中对齐。
- **顶部与创建流程**：标题统一为 Edit Agent，编辑历史移入 More 菜单；创建中的 loading
在原有区域覆盖显示，不再撑高弹窗。
- **复用现有入口**：Add skill 与 Skills 页面使用同一个 ZIP 上传弹窗；Instructions 和已有 Skill
的正文通过编辑弹窗修改。

## 设计稿

-
[Settings（789:2094）](https://w
```
