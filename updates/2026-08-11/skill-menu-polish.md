---
title: "Skill 菜单更好找、更好翻"
type: "体验优化"
priority: "中"
date: "2026-08-11"
status: "待审核"
channels: ""
---

## 核心宣传点

输入框的 Skill 子菜单一次能看到更多条目、内容多时有渐变提示并可独立滚动，小窗口也不会被裁切；重复的 Skill Store 入口已从头像菜单移除，统一走 Plugins 页面。

## 原始内容

### commit message

```
fix(chat): 优化 Skill 菜单入口与溢出提示 (#3335)

## 变更摘要
- 移除 Profile 菜单中重复的 Skill Store 入口；Skills 已可通过 Plugins 页面访问
- Composer 的 Skill 子菜单最多展示 4.5 行，并在内容溢出时显示渐变提示
- 子菜单支持短视口自适应，Skill 列表可独立滚动，底部操作入口保持可见
- 统一 Skill 行与父级菜单的 Hover 圆角，并让子菜单底部对齐、向上展开

## 问题原因
Profile 菜单与 Plugins 页面重复提供了 Skill Store 入口。Composer 的 Skill
子菜单原先只有固定的三行高度，缺少“还有更多内容”的视觉提示；同时 Radix
默认使用顶部对齐，列表变高后会继续向下延伸，在较矮视口中可能裁切内容。

## 测试计划
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui test` (351 tests)
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] `bash scripts/verify-web.sh web/app/src/components/UserMenu.tsx
web/app/tests/unit/components/UserMenu.unit.spec.tsx` (67 tests)
- [x] `bash scripts/verify-web.sh --test-only
web/app/tests/unit/app/agent-builder-create-dialog.unit.spec.tsx` (19
tests)
- [x] `bash scripts/verify-changed.sh`
- [x] 浏览器验证：子菜单与触发行底边偏差为 0px；滚动到底部后渐变消失
- [x] 短视口验证：窗口高度为 280px 时，菜单限制为 280px，Skill 列表在 191px
高度内滚动，两个底部操作入口均完整可见
```

### PR body

## 变更摘要
- 移除 Profile 菜单中重复的 Skill Store 入口；Skills 已可通过 Plugins 页面访问
- Composer 的 Skill 子菜单最多展示 4.5 行，并在内容溢出时显示渐变提示
- 子菜单支持短视口自适应，Skill 列表可独立滚动，底部操作入口保持可见
- 统一 Skill 行与父级菜单的 Hover 圆角，并让子菜单底部对齐、向上展开

## 问题原因
Profile 菜单与 Plugins 页面重复提供了 Skill Store 入口。Composer 的 Skill 子菜单原先只有固定的三行高度，缺少“还有更多内容”的视觉提示；同时 Radix 默认使用顶部对齐，列表变高后会继续向下延伸，在较矮视口中可能裁切内容。

## 测试计划
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui test` (351 tests)
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] `bash scripts/verify-web.sh web/app/src/components/UserMenu.tsx web/app/tests/unit/components/UserMenu.unit.spec.tsx` (67 tests)
- [x] `bash scripts/verify-web.sh --test-only web/app/tests/unit/app/agent-builder-create-dialog.unit.spec.tsx` (19 tests)
- [x] `bash scripts/verify-changed.sh`
- [x] 浏览器验证：子菜单与触发行底边偏差为 0px；滚动到底部后渐变消失
- [x] 短视口验证：窗口高度为 280px 时，菜单限制为 280px，Skill 列表在 191px 高度内滚动，两个底部操作入口均完整可见


