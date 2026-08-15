---
title: "Agent Builder 首页排版与操作全面优化"
type: "体验优化"
priority: "中"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

Agent 列表内容居中、阅读宽度更舒服；窄屏不再左右乱挤、操作按钮始终点得到；重命名弹窗也更简洁。

## 原始内容

fix(agent-builder): 优化首页响应式布局与交互 (#3390)

## 概要

- 将 Agent Builder 首页内容区居中，最大阅读宽度设为 896px，并按不同视口逐级调整页面边距。
- 使用容器断点优化列表响应式布局：窄屏将更新时间和发布状态收进 Agent 信息区，宽屏保持四列展示，操作按钮始终可见且不产生横向滚动。
- 简化列表排版：移除描述文字，Agent 名称改为常规字重；表头统一左对齐并降低视觉强调；同时优化行距、列间距和 hover 反馈。
- 优化 Edit、已发布 Agent 的 Chat 及 More 操作：使用紧凑的圆角矩形，窄屏只显示图标，宽屏显示文字，Edit 与
Chat 的间距调整为 12px。
- 简化 Rename 弹窗：移除重复展示的当前名称，只保留预填输入框；输入框和按钮统一为圆角矩形；Rename 菜单项的高亮仅在 Agent
Builder 页面内生效。
- 本 PR 严格限定在 Agent Builder 首页，不包含共享 Chat UI、Design System 包、Create
dialog 以及登录/认证改动。Preview composer 共享逻辑已通过 #3374 合入 `main`，本 PR 不重复提交。

## 根因

原 Agent Builder
首页使用全宽固定列布局，并直接继承共享组件的通用操作样式。宽屏下列表被过度拉伸，影响可读性；窄屏下更新时间、状态和右侧操作会争抢空间。Rename
弹窗同时重复展示当前名称，默认圆角和 hover 样式也让部分控件呈现胶囊感、交互反馈不够清晰。

## 测试计划

- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderHome.tsx'
web/app/tests/unit/app/agent-builder-entry.unit.spec.tsx
web/app/tests/unit/app/agent-builder-production-home.unit.spec.tsx`
- [x] 相关 Vitest：2 个测试文件、84 个测试全部通过
- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/check-pr-size.sh`（792 / 3000 行）
- [x] 范围审计确认没有 Chat UI、Design System、Create dialog 或登录/认证文件

---
### PR Body

## 概要

- 将 Agent Builder 首页内容区居中，最大阅读宽度设为 896px，并按不同视口逐级调整页面边距。
- 使用容器断点优化列表响应式布局：窄屏将更新时间和发布状态收进 Agent 信息区，宽屏保持四列展示，操作按钮始终可见且不产生横向滚动。
- 简化列表排版：移除描述文字，Agent 名称改为常规字重；表头统一左对齐并降低视觉强调；同时优化行距、列间距和 hover 反馈。
- 优化 Edit、已发布 Agent 的 Chat 及 More 操作：使用紧凑的圆角矩形，窄屏只显示图标，宽屏显示文字，Edit 与 Chat 的间距调整为 12px。
- 简化 Rename 弹窗：移除重复展示的当前名称，只保留预填输入框；输入框和按钮统一为圆角矩形；Rename 菜单项的高亮仅在 Agent Builder 页面内生效。
- 本 PR 严格限定在 Agent Builder 首页，不包含共享 Chat UI、Design System 包、Create dialog 以及登录/认证改动。Preview composer 共享逻辑已通过 #3374 合入 `main`，本 PR 不重复提交。

## 根因

原 Agent Builder 首页使用全宽固定列布局，并直接继承共享组件的通用操作样式。宽屏下列表被过度拉伸，影响可读性；窄屏下更新时间、状态和右侧操作会争抢空间。Rename 弹窗同时重复展示当前名称，默认圆角和 hover 样式也让部分控件呈现胶囊感、交互反馈不够清晰。

## 测试计划

- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderHome.tsx' web/app/tests/unit/app/agent-builder-entry.unit.spec.tsx web/app/tests/unit/app/agent-builder-production-home.unit.spec.tsx`
- [x] 相关 Vitest：2 个测试文件、84 个测试全部通过
- [x] `bash scripts/verify-changed.sh`
- [x] `bash scripts/check-pr-size.sh`（792 / 3000 行）
- [x] 范围审计确认没有 Chat UI、Design System、Create dialog 或登录/认证文件

