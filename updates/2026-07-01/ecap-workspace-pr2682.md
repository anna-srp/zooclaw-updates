---
title: "Agent Builder 操作区布局优化，主次操作更清晰"
type: "体验优化"
priority: "中"
date: "2026-07-01"
status: "待审核"
channels: ""
---
# Agent Builder 操作区布局优化，主次操作更清晰
## 核心宣传点
Agent Builder 顶部操作区重新整理：次要操作收进 More 菜单、项目状态标签移到标题栏、打包/测试按钮移到输入框上方，草稿状态下自动隐藏测试区，界面更清爽、操作更顺手。
## 原始内容
style(agent-builder): 调整Agent  Builder 操作区布局 (#2682)

## 变更摘要
- 将 Agent Builder 右上角的次级操作收进 More 菜单，并统一为 icon + 文案的菜单项。
- 将项目状态标签放到顶部标题栏，保留 New project 在 More 菜单左侧。
- 将 Package/Test 操作放到输入框上方；drafting 状态下隐藏右侧测试区域，并禁用顶部测试模式按钮。
- 增加 composer prefix 的复用路径，让 Agent Builder 可以替换默认输入框快捷操作，同时不影响其他聊天页面行为。

## 验证
- `bash scripts/verify-web.sh web/app/src/components/ClawPageHeader.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/chat/components/GenClawInput.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/chat/components/OpenClawChatSurface.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderClient.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderProjectActionControls.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderProjectActions.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderStatusPane.tsx
web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderTestPane.tsx
web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- `pnpm --dir web/app lint:ci`
- GitHub PR checks：`43/43 passed`

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: kaka-srp <kaka@srp.one>

---

### PR Description

## 变更摘要
- 将 Agent Builder 右上角的次级操作收进 More 菜单，并统一为 icon + 文案的菜单项。
- 将项目状态标签放到顶部标题栏，保留 New project 在 More 菜单左侧。
- 将 Package/Test 操作放到输入框上方；drafting 状态下隐藏右侧测试区域，并禁用顶部测试模式按钮。
- 增加 composer prefix 的复用路径，让 Agent Builder 可以替换默认输入框快捷操作，同时不影响其他聊天页面行为。

## 验证
- `bash scripts/verify-web.sh web/app/src/components/ClawPageHeader.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/chat/components/GenClawInput.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/chat/components/OpenClawChatSurface.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderClient.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderProjectActionControls.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderProjectActions.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderStatusPane.tsx web/app/src/app/'[locale]'/'(app)'/'(chat)'/agent-builder/AgentBuilderTestPane.tsx web/app/tests/unit/app/agent-builder-client.unit.spec.tsx`
- `pnpm --dir web/app lint:ci`
- GitHub PR checks：`43/43 passed`

