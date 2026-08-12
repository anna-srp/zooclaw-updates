---
title: "弹窗视觉与关闭方式统一"
type: "体验优化"
priority: "中"
date: "2026-08-11"
status: "待审核"
channels: ""
---

## 核心宣传点

确认类弹窗（AlertDialog）改成和普通弹窗一致的实体浮层，新增右上角关闭按钮，遮罩、圆角、标题排版全部对齐，不再出现两种风格混用。

## 原始内容

### commit message

```
fix(design-system): 统一 Dialog 与 AlertDialog 的视觉和关闭交互 (#3332)

## 变更摘要

- 为 Dialog 与 AlertDialog 提取共享的 modal 视觉规则，统一遮罩、实体弹层、圆角、边框、阴影、标题、说明和操作区布局
- 将 AlertDialog 从低对比度玻璃表面调整为与 Dialog 一致的实体浮层，并移除突兀的底部分割线
- 为 AlertDialog 增加与 Dialog 一致的 Heroicon 关闭按钮，支持通过
`showCloseButton={false}` 隐藏
- 保持 AlertDialog 的取消语义：右上角关闭按钮使用 Cancel primitive，默认焦点落在底部
Cancel，关闭后焦点返回触发按钮
- 增加视觉契约、关闭交互、默认焦点及可选关闭按钮的回归测试

## 根因

AlertDialog 仍在独立使用旧的 Liquid Glass 表面、模糊遮罩、标题字体和带分割线的 footer，而普通 Dialog
已经切换到实体浮层语言。两套组件缺少共享视觉契约，导致同属 modal 家族的组件在亮暗模式、关闭入口和交互焦点上逐渐分叉。

## 测试计划

- [x] `pnpm --filter @zooclaw/design-system test --
alert-dialog.test.tsx dialog.test.tsx`（53 个测试文件、301 项测试通过）
- [x] `pnpm --filter @zooclaw/design-system tsc`
- [x] `pnpm --filter @zooclaw/design-system lint`
- [x] `pnpm --filter @zooclaw/design-system build:preview`
- [x] 浏览器走查亮色与暗色 AlertDialog
- [x] 验证右上角关闭、底部 Cancel 默认焦点以及关闭后焦点回归

## 备注

`scripts/verify-changed.sh` 当前未给 `web/packages` 提供独立本地入口，因此统一 verifier
提示由 CI 兜底；上述设计系统包级检查均已通过。
```

### PR body

## 变更摘要

- 为 Dialog 与 AlertDialog 提取共享的 modal 视觉规则，统一遮罩、实体弹层、圆角、边框、阴影、标题、说明和操作区布局
- 将 AlertDialog 从低对比度玻璃表面调整为与 Dialog 一致的实体浮层，并移除突兀的底部分割线
- 为 AlertDialog 增加与 Dialog 一致的 Heroicon 关闭按钮，支持通过 `showCloseButton={false}` 隐藏
- 保持 AlertDialog 的取消语义：右上角关闭按钮使用 Cancel primitive，默认焦点落在底部 Cancel，关闭后焦点返回触发按钮
- 增加视觉契约、关闭交互、默认焦点及可选关闭按钮的回归测试

## 根因

AlertDialog 仍在独立使用旧的 Liquid Glass 表面、模糊遮罩、标题字体和带分割线的 footer，而普通 Dialog 已经切换到实体浮层语言。两套组件缺少共享视觉契约，导致同属 modal 家族的组件在亮暗模式、关闭入口和交互焦点上逐渐分叉。

## 测试计划

- [x] `pnpm --filter @zooclaw/design-system test -- alert-dialog.test.tsx dialog.test.tsx`（53 个测试文件、301 项测试通过）
- [x] `pnpm --filter @zooclaw/design-system tsc`
- [x] `pnpm --filter @zooclaw/design-system lint`
- [x] `pnpm --filter @zooclaw/design-system build:preview`
- [x] 浏览器走查亮色与暗色 AlertDialog
- [x] 验证右上角关闭、底部 Cancel 默认焦点以及关闭后焦点回归

## 备注

`scripts/verify-changed.sh` 当前未给 `web/packages` 提供独立本地入口，因此统一 verifier 提示由 CI 兜底；上述设计系统包级检查均已通过。


