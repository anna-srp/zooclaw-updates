---
title: "首页侧边栏玻璃质感 UI 打磨"
type: "体验优化"
priority: "低"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# 首页侧边栏玻璃质感 UI 打磨
## 核心宣传点
首页侧边栏整体视觉升级：玻璃质感表面、导航选中态、Logo 与个人资料卡都更精致，暗色下不再出现刺眼白块。
## 原始内容
### [ecap-workspace PR #2709]

style(sidenav): polish homepage sidebar glass UI (#2709)

## Summary
- Polish the homepage sidenav glass surface, nav row active states, logo
treatment, agent row density, and profile card styling.
- Move raw glass gradients into CSS modules so JSX stays within lint
rules and dark glass states avoid bright white blocks.
- Preserve visible keyboard focus states, keep the profile card styled
on non-glass app routes, and remove the now-unused legacy wordmark
export.
- Add a null-pathname guard in `PublicHeader` so the global TypeScript
check passes with current Next types.

## Test plan
- [x] `CI=true
PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin bash
scripts/verify-web.sh web/app/src/components/UserCard.tsx
web/app/src/components/UserCard.module.css
web/app/src/components/sidenav/NavItemComponent.tsx
web/app/src/components/sidenav/NavItemComponent.module.css
web/app/src/components/sidenav/SideNav.tsx
web/app/src/components/sidenav/SideNav.module.css
web/app/src/components/sidenav/SideNavAgentList.tsx
web/app/src/components/sidenav/SideNavAgentRow.tsx
web/app/src/components/sidenav/SideNavAgentSessions.tsx
web/app/src/components/sidenav/SideNavAgentSessions.module.css
web/app/src/components/sidenav/SideNavLogo.tsx
web/app/src/components/sidenav/SideNavUserSection.tsx
web/app/src/components/sidenav/constants.ts
web/app/src/components/public/PublicHeader.tsx`
- [x] `CI=true
PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin pnpm
run lint:ci` from `web/app`

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>

---

## PR Description

## Summary
- Polish the homepage sidenav glass surface, nav row active states, logo treatment, agent row density, and profile card styling.
- Move raw glass gradients into CSS modules so JSX stays within lint rules and dark glass states avoid bright white blocks.
- Preserve visible keyboard focus states, keep the profile card styled on non-glass app routes, and remove the now-unused legacy wordmark export.
- Add a null-pathname guard in `PublicHeader` so the global TypeScript check passes with current Next types.

## Test plan
- [x] `CI=true PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin bash scripts/verify-web.sh web/app/src/components/UserCard.tsx web/app/src/components/UserCard.module.css web/app/src/components/sidenav/NavItemComponent.tsx web/app/src/components/sidenav/NavItemComponent.module.css web/app/src/components/sidenav/SideNav.tsx web/app/src/components/sidenav/SideNav.module.css web/app/src/components/sidenav/SideNavAgentList.tsx web/app/src/components/sidenav/SideNavAgentRow.tsx web/app/src/components/sidenav/SideNavAgentSessions.tsx web/app/src/components/sidenav/SideNavAgentSessions.module.css web/app/src/components/sidenav/SideNavLogo.tsx web/app/src/components/sidenav/SideNavUserSection.tsx web/app/src/components/sidenav/constants.ts web/app/src/components/public/PublicHeader.tsx`
- [x] `CI=true PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin pnpm run lint:ci` from `web/app`

