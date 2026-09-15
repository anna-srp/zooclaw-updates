---
title: "修复：最近会话侧栏被长标题撑爆，Show more 按钮被挤到看不见的地方"
type: "Bug Fix"
priority: "中"
date: "2026-09-14"
status: "待审核"
channels: "changelog"
---

# 修复：最近会话侧栏被长标题撑爆，Show more 按钮被挤到看不见的地方

## 核心宣传点

会话标题一长，最近历史侧栏就会被横向撑开：标题被裁掉一截，选中行的背景色跑偏，「Show more / Show less」直接被顶到可视区域外面——想收起列表都点不到。

根因藏在组件库里：Radix 的 ScrollArea 会把内容包进一个 `display: table` 元素，长标题不换行时的固有宽度会把这个元素顶大。实测一个 224px 宽的视口里，行和按钮被撑到了 744px。修法是在 `AgentWorkspaceNav` 里用一个最小宽度为零的单列 grid 把内容在局部约束住，让所有滚动导航内容都留在侧栏范围内——标题正常截断，控件始终可见。紧凑模式的侧栏上，「Load more」改用了一个无障碍图标，和已有的折叠控件保持一致。

只需要发布前端。

## 原始内容

### fix(agents): keep recent conversation controls within sidebar (#3725)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `f756f8c8`
- PR: #3725
- 作者: kaka-srp
- 日期: 2026-09-14

验证（PR 原文）：已有导航单元测试 9 项通过；`bash scripts/verify-web.sh --no-test` 的治理守卫、TypeScript 和 ESLint 通过。Chromium fixture 渲染的是真实导航组件、设计系统的 ScrollArea/Button 和编译后的应用 CSS（翻译和视图模型数据为 fixture），前后几何对比确认内容宽度从 744px 收到 224px、标题截断生效。真实浏览器点击验证了 8 → 13 → 8 条最近会话、在矮窗口里滚动到底部控件、以及桌面和移动宽度下的 Load more 回调，含长渠道名和状态徽标。独立 Agent 审查无发现。

带鉴权的 staging 浏览器验收待部署后进行。

## 备注

发布状态：已合并待发版（尚未包含在任何 `ecap-*-release` tag 中）。

对外发布注意：纯前端 UI 修复，量级较小，建议并入 changelog 的「体验优化」合并条目，不单独发社交媒体。
