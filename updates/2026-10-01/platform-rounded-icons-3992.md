---
title: "开发者平台浏览器标签页图标改为圆角透明"
type: "体验优化"
priority: "中"
date: "2026-10-01"
status: "待审核"
channels: ""
---

# 开发者平台浏览器标签页图标改为圆角透明

## 核心宣传点

开发者平台的浏览器标签页此前显示的是深蓝色方块图标。这次把 16px / 32px favicon 和 180px 触控图标都换成圆角透明边的版本，颜色和白色标识保持不变，生产与本地的共享配置同步更新。

## 分级

- 内部：P2
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

Platform browser tabs currently show square deep-blue icons. Replace the 16px/32px favicons and 180px touch icon with rounded transparent corners, preserving the existing color and white mark. Update the shared production and local-preview HTML entries to the new asset filenames, so every Platform route uses the rounded icons and browsers fetch fresh assets.

All changes are limited to `web/platform`. The black ZooWork icon used by `zoowork.ai` and its brand assets remain unchanged.

Validation:
- `corepack pnpm --filter @zooclaw/platform-app build` passed, including TypeScript checks; built icon files match the final source assets.
- Pixel checks confirmed transparent corners and unchanged fully opaque interior pixels at 16px, 32px, and 180px.
- In-browser local-preview checks confirmed the shared rounded icon links on login, API keys, and Terms routes; source inspection confirmed the production SPA shares one global entry without route-specific favicon overrides.
- `git diff --check` passed.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `3fab7255c1c63bad3abd078840e24ccdfd8129cc`
- PR: #3992
- 作者：ericma-srp
- 日期：2026-10-01T16:53:01Z

### Commit Message

```
fix(platform): use rounded icons across platform routes (#3992)

Platform browser tabs currently show square deep-blue icons. Replace the
16px/32px favicons and 180px touch icon with rounded transparent
corners, preserving the existing color and white mark. Update the shared
production and local-preview HTML entries to the new asset filenames, so
every Platform route uses the rounded icons and browsers fetch fresh
assets.

All changes are limited to `web/platform`. The black ZooWork icon used
by `zoowork.ai` and its brand assets remain unchanged.

Validation:
- `corepack pnpm --filter @zooclaw/platform-app build` passed, including
TypeScript checks; built icon files match the final source assets.
- Pixel checks confirmed transparent corners and unchanged fully opaque
interior pixels at 16px, 32px, and 180px.
- In-browser local-preview checks confirmed the shared rounded icon
links on login, API keys, and Terms routes; source inspection confirmed
the production SPA shares one global entry without route-specific
favicon overrides.
- `git diff --check` passed.
```

来源：SerendipityOneInc/ecap-workspace @ 3fab7255，PR #3992，作者 ericma-srp。
