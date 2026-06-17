---
title: "已登录用户跳过新手引导，并新增管理后台入口"
type: "体验优化"
priority: "低"
date: "2026-06-16"
status: "待审核"
channels: ""
---
# 已登录用户跳过新手引导，并新增管理后台入口
## 核心宣传点
已登录用户不再被新手引导挡住对话，企业管理后台还新增了「Web App」入口，访问更便捷。
## 原始内容
fix(web): skip web onboarding and add admin app link (#2487)

## Summary

- add a `Web App` entry to the enterprise-admin sidebar and mobile nav,
defaulting to `https://zooclaw.ai/new-chat`
- disable web app onboarding as a chat blocker for logged-in users
- update regression coverage for the admin app link and onboarding
resolver behavior

## Local Checks

- `bash scripts/verify-changed.sh`
- `pnpm --dir web/app exec vitest run
tests/unit/components/onboarding/resolveOnboardingStatus.unit.spec.ts`
- `pnpm --dir web/enterprise-admin exec vitest run
components/layout/__tests__/Sidebar.test.tsx`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- `pnpm --dir web/enterprise-admin exec eslint
components/layout/Sidebar.tsx components/layout/MobileNav.tsx
components/layout/__tests__/Sidebar.test.tsx`
- `git diff --check origin/main...HEAD`

---

## PR Description

## Summary

- add a `Web App` entry to the enterprise-admin sidebar and mobile nav, defaulting to `https://zooclaw.ai/new-chat`
- disable web app onboarding as a chat blocker for logged-in users
- update regression coverage for the admin app link and onboarding resolver behavior

## Local Checks

- `bash scripts/verify-changed.sh`
- `pnpm --dir web/app exec vitest run tests/unit/components/onboarding/resolveOnboardingStatus.unit.spec.ts`
- `pnpm --dir web/enterprise-admin exec vitest run components/layout/__tests__/Sidebar.test.tsx`
- `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- `pnpm --dir web/enterprise-admin exec eslint components/layout/Sidebar.tsx components/layout/MobileNav.tsx components/layout/__tests__/Sidebar.test.tsx`
- `git diff --check origin/main...HEAD`

