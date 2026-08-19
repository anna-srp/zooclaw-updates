---
title: "频道页「添加频道」按钮统一样式，全局加载动画换新"
type: "体验优化"
priority: "中"
date: "2026-08-18"
status: "待审核"
channels: ""
---

# 频道页「添加频道」按钮统一样式，全局加载动画换新

## 核心宣传点

「添加频道」按钮与 Agent Builder 保持一致的形状并去掉了突兀的玻璃阴影；频道页加载状态改为在右侧内容区居中显示，全局加载动画换成新的 ZooClaw 动效，页面专属加载文案也不会再和通用文案重复。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `71195904121902ee07a6c641fc8ae1c8874dec54`
- PR: #3369
- 作者: shana-srp
- 日期: 2026-08-18T09:14:40Z

### Commit Message

```
feat(web): refresh channel action and global loading (#3369)

## Linear

N/A — no Linear issue was provided for this UI polish request.

## Summary

- align the Channel “Add Channel” action with the Agent Builder button
shape and remove its glass-like shadow
- center Channel loading states within the right-side content panel
- replace the shared global loader with the new ZooClaw animation at
90×90 and 50% opacity
- preserve page-specific loading messages while preventing duplicate
generic labels

## Test plan

- [x] `bash scripts/verify-web.sh` for all changed frontend files
- [x] TypeScript and ESLint checks
- [x] 86 related Vitest tests
- [x] pre-push changed-surface verification

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

```
## Linear

N/A — no Linear issue was provided for this UI polish request.

## Summary

- align the Channel “Add Channel” action with the Agent Builder button shape and remove its glass-like shadow
- center Channel loading states within the right-side content panel
- replace the shared global loader with the new ZooClaw animation at 90×90 and 50% opacity
- preserve page-specific loading messages while preventing duplicate generic labels

## Test plan

- [x] `bash scripts/verify-web.sh` for all changed frontend files
- [x] TypeScript and ESLint checks
- [x] 86 related Vitest tests
- [x] pre-push changed-surface verification

```
