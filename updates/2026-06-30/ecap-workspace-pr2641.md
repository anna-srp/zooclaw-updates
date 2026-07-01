---
title: "修复 BossClaw 手机端注册与扫码弹窗体验"
type: "Bug Fix"
priority: "中"
date: "2026-06-30"
status: "待审核"
channels: ""
---
# 修复 BossClaw 手机端注册与扫码弹窗体验
## 核心宣传点
手机端注册 BossClaw 时不再复用过期的落地页上下文，App/渠道扫码弹窗在小屏 Safari 上可正常滚动，兑换码兑换也保持在当前注册流程内完成。
## 原始内容
fix(onboarding): handle bossclaw mobile registration (#2641)

## Summary
- Refresh BossClaw landing context when a new URL payload arrives so
cached WeChat WebView state does not reuse an old context.
- Make mobile app and channel QR modals scrollable on short Safari
viewports.
- Keep gift-code redemption inside the current registration flow without
navigating to chat.

## Root cause
Cached landing context could be preserved even when a fresh BossClaw URL
payload was present, so WeChat WebView users could continue with stale
registration context. QR modals also used centered fixed overlays
without scroll bounds, which clipped content on short iPhone screens.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web -r --workspace-concurrency=1 --if-present run tsc`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`
- [x] Targeted mobile/onboarding tests: `pnpm --dir web/app test:unit
tests/unit/components/UserMenu.unit.spec.tsx
tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts
tests/unit/components/MobileAppModal.unit.spec.tsx
tests/unit/app/claw-settings/WeixinSetupModal.unit.spec.tsx
tests/unit/app/claw-settings/WecomSetupModal.unit.spec.tsx
tests/unit/app/claw-settings/FeishuSetupModal.unit.spec.tsx`

Note: `pnpm --dir web run tsc` currently fails because the repo script
invokes `pnpm ... exec` with unsupported `--if-present`; the equivalent
workspace run-command plus `web/app` tsc passed.

---

### PR Description

## Summary
- Refresh BossClaw landing context when a new URL payload arrives so cached WeChat WebView state does not reuse an old context.
- Make mobile app and channel QR modals scrollable on short Safari viewports.
- Keep gift-code redemption inside the current registration flow without navigating to chat.

## Root cause
Cached landing context could be preserved even when a fresh BossClaw URL payload was present, so WeChat WebView users could continue with stale registration context. QR modals also used centered fixed overlays without scroll bounds, which clipped content on short iPhone screens.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web -r --workspace-concurrency=1 --if-present run tsc`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`
- [x] Targeted mobile/onboarding tests: `pnpm --dir web/app test:unit tests/unit/components/UserMenu.unit.spec.tsx tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts tests/unit/components/MobileAppModal.unit.spec.tsx tests/unit/app/claw-settings/WeixinSetupModal.unit.spec.tsx tests/unit/app/claw-settings/WecomSetupModal.unit.spec.tsx tests/unit/app/claw-settings/FeishuSetupModal.unit.spec.tsx`

Note: `pnpm --dir web run tsc` currently fails because the repo script invokes `pnpm ... exec` with unsupported `--if-present`; the equivalent workspace run-command plus `web/app` tsc passed.
