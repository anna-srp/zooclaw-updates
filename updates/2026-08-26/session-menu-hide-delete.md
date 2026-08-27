---
title: "会话菜单里那个点了也没用的「删除」按钮已隐藏"
type: "体验优化"
priority: "低"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 会话菜单里那个点了也没用的「删除」按钮已隐藏

## 核心宣传点

会话右侧的「⋯」菜单里一直挂着一个「删除」项，但它背后其实没有任何实现，点了永远不会成功。现在这个按钮先隐藏起来，菜单只保留「重命名」，宽度和样式保持不变；等删除功能真正做好了再放出来。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `fdcd34db3ff42415400000f173021415039f3c04`
- PR: #3534
- 作者: sharplee-srp
- 日期: 2026-08-26T13:42:03Z

### Commit Message

```
fix(web): hide unsupported session delete action (#3534)

## Summary
- Hide the unsupported Delete action from the session overflow menu
until its dependencies are implemented.
- Keep the existing Delete item behind a temporary off switch and a TODO
so it can be restored without reconstructing the UI.
- Let the menu collapse to its single Rename action while preserving its
existing width and styling.
- Add a regression assertion that the Delete action is not rendered.

## Root cause
The session menu rendered a disabled Delete item even though no frontend
mutation or backend service exists for deleting sessions. This exposed
an action that could never succeed.

## Test plan
- [x] `bash scripts/verify-web.sh
web/app/src/components/sidenav/SideNavSessionRow.tsx
web/app/tests/unit/components/sidenav/SideNavSessionRow.unit.spec.tsx`
- [x] `pnpm exec vitest run
tests/unit/components/sidenav/SideNavSessionRow.unit.spec.tsx` (24
tests)
- [x] Pre-push changed-surface verification (`bash
scripts/verify-changed.sh`)
```

### PR Description

```
## Summary
- Hide the unsupported Delete action from the session overflow menu until its dependencies are implemented.
- Keep the existing Delete item behind a temporary off switch and a TODO so it can be restored without reconstructing the UI.
- Let the menu collapse to its single Rename action while preserving its existing width and styling.
- Add a regression assertion that the Delete action is not rendered.

## Root cause
The session menu rendered a disabled Delete item even though no frontend mutation or backend service exists for deleting sessions. This exposed an action that could never succeed.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/components/sidenav/SideNavSessionRow.tsx web/app/tests/unit/components/sidenav/SideNavSessionRow.unit.spec.tsx`
- [x] `pnpm exec vitest run tests/unit/components/sidenav/SideNavSessionRow.unit.spec.tsx` (24 tests)
- [x] Pre-push changed-surface verification (`bash scripts/verify-changed.sh`)

```
