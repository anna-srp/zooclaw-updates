---
title: "新用户首次进入新增「欢迎」引导：依次填写称呼、角色、使用场景"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-22"
status: "待审核"
channels: "站内弹窗 + Use Case + Discord + changelog"
---
# 新用户首次进入新增「欢迎」引导：依次填写称呼、角色、使用场景
## 核心宣传点
首次登录的新用户现在会看到一个全屏的欢迎引导页，按「称呼 → 角色 → 使用场景」三步完成基础信息填写，替代原来的弹窗形式；过程中可随时跳过、可返回上一步，未填完刷新页面 30 分钟内还能接着填，开局体验更清晰顺手。
## 原始内容
feat(onboarding): add /welcome first-run 3-step flow (name → role → scenario) (#2502)

## Summary

Adds a new full-screen first-run onboarding flow at `/en/welcome`, replacing the modal pattern for collecting `name → role → scenario` from new users. Implemented per Figma nodes 1840-26232 / 1840-26254 / 1840-24672 / 3135-1300 (background).

## What landed

- **Route**: `web/app/src/app/[locale]/welcome/` — `page.tsx` (server, noindex) + `WelcomeClient.tsx` (client wrapper + step state) + 3 step components (`NameStep` / `RoleStep` / `ScenarioStep`) + `wizard-state.ts` (localStorage with 30-min TTL for resume-after-refresh).
- **Assets**: `web/app/public/welcome/` — 2 role illustration sprite sheets + 4 scenario SVG icons (sourced from Figma). Background is a CSS radial gradient (no SVG dependency).
- **Branded palette** registered in `globals.css` `@theme inline` as `--color-welcome-*` and `--shadow-welcome-cta*` tokens — components stay 100% Tailwind utility classes (`bg-welcome-ink`, `shadow-welcome-cta`, etc.). No module CSS file.
- **Background gradient** added as a Tailwind v4 `@utility welcome-bg` block in `globals.css` — composes with all variants.
- **Interactions**: Continue (primary CTA, filled black with subtle shadow + hover lift), Skip (text link with hover opacity), Back on steps 2/3 (secondary linear button, light gray border matching the cards). Cards have hover lift + shadow-md + tint.
- **State**: localStorage draft survives reload for 30 min; submit clears it and routes to `/[locale]/chat`.

## What is intentionally NOT in this PR

- **Backend** persistence of the collected name/role/scenario (this PR is the frontend flow + state only).
