---
title: "网页端侧边栏 Logo 更新，展开收起动画更顺滑"
type: 体验优化
priority: 低
date: 2026-08-17
status: "待审核"
channels: ""
---

## 核心宣传点

网页端侧边栏换上了新的展开态 Logo（深浅色主题各一套），收起时的小图标保持不变。展开/收起时 Logo 采用交叉淡入淡出，宽度与内容位移动画同步，收起后的图标也居中对齐，来回切换不再出现闪跳或错位。

## 原始内容

**Commit**: `03222a3b` — fix(web): update and smooth sidebar logo (#3393)
**作者**: lynn Zhuang ｜ **日期**: 2026-08-17T03:59:31Z

```
fix(web): update and smooth sidebar logo (#3393)

## Summary
- replace the expanded web sidebar logo with the supplied ZooWork navy and white assets for light and dark themes
- keep the collapsed web icon and Electron branding unchanged while cross-fading persistent logo layers
- synchronize sidebar width and content offset motion, respect reduced-motion preferences, and compensate the Liquid Glass border for accurate centering

## Root cause
The expanded and collapsed logo variants were conditionally mounted, so the compact mark could appear a frame late during the sidebar width transition. Broad `transition-all` rules also animated unrelated properties with a different easing curve, while the Liquid Glass border shifted the apparent center by one pixel.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/components/sidenav/SideNavLogo.tsx web/app/src/components/sidenav/SideNav.tsx web/app/src/components/AppLayout.tsx web/app/tests/unit/components/sidenav/SideNavLogo.unit.spec.tsx`
- [x] `bash scripts/verify-changed.sh`
- [x] manually verified light/dark expanded logos, repeated collapse/expand transitions, centered collapsed mark, and unchanged collapsed asset at `http://localhost:3005/chat`
```
