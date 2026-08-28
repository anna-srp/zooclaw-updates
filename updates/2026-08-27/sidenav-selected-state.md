---
title: "侧边栏选中态改为纯色块，去掉左侧指示条和多余描边"
type: "体验优化"
priority: "低"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# 侧边栏选中态改为纯色块，去掉左侧指示条和多余描边

## 核心宣传点

侧边栏的选中效果之前叠了左侧指示条、边框和内描边，视觉上过重也不够统一。现在当前所在模块只用一块背景色表示选中，并补上了无障碍朗读所需的「当前页」标记；「New Task」作为操作入口不再显示持久选中态，只在点击和悬停时给反馈。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `8c889ecb35bb2fb3aacd3fc7e5da4890ce1f0452`
- PR: #3555
- 作者: lynn Zhuang
- 日期: 2026-08-27T11:22:59Z

### Commit Message

```
fix(sidenav): 优化侧边栏选中态 (#3555)

## 变更说明

- `New Task` 保持操作入口语义，仅提供点击和悬停反馈，不显示持久选中态
- 当前路由对应的侧边栏模块只使用背景色块表示选中，并添加 `aria-current="page"`
- 移除左侧指示条、边框和内描边，同时将遗留 CSS Module 迁移为 Tailwind 工具类

## 验证

- `bash scripts/verify-changed.sh`
- `pnpm exec vitest run
tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts
tests/unit/components/sidenav/NavItemComponent.unit.spec.tsx`
- 使用本地 Mock 在 Paper Focus 浅色模式下完成浏览器验证：选中模块无边框、阴影和指示条；`New Task`
仅在悬停时显示背景
```

### PR Description

```
## 变更说明

- `New Task` 保持操作入口语义，仅提供点击和悬停反馈，不显示持久选中态
- 当前路由对应的侧边栏模块只使用背景色块表示选中，并添加 `aria-current="page"`
- 移除左侧指示条、边框和内描边，同时将遗留 CSS Module 迁移为 Tailwind 工具类

## 验证

- `bash scripts/verify-changed.sh`
- `pnpm exec vitest run tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts tests/unit/components/sidenav/NavItemComponent.unit.spec.tsx`
- 使用本地 Mock 在 Paper Focus 浅色模式下完成浏览器验证：选中模块无边框、阴影和指示条；`New Task` 仅在悬停时显示背景

```

---
