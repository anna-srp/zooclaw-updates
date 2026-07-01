---
title: "BossClaw 企业微信/飞书绑定不再显示微信专属提示"
type: "体验优化"
priority: "低"
date: "2026-06-30"
status: "待审核"
channels: ""
---
# BossClaw 企业微信/飞书绑定不再显示微信专属提示
## 核心宣传点
用 BossClaw 绑定企业微信或飞书时，不再错误显示「怎么确认绑定成功」这类只针对个人微信的说明，提示更贴合你实际用的渠道。
## 原始内容
fix(bossclaw): hide bind guide for work channels (#2665)

## Summary
- Hide the “怎么确认绑定成功” guide when BossClaw bind channel is 企业微信 or 飞书.
- Keep the guide visible for personal WeChat only.
- Add a unit test covering personal WeChat, WeCom, and Feishu channel
switching.

## Root cause
The bind confirmation guide was rendered unconditionally in the QR step,
so all binding channels inherited the personal WeChat confirmation
instructions.

## Test plan
- [x] pnpm --dir web/app test:unit
tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx
tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts
tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx
- [x] pnpm --dir web lint
- [x] pnpm --dir web exec tsc --noEmit --project app/tsconfig.json
- [x] git diff --check
- [x] GitHub CI for PR #2665

---

### PR Description

## Summary
- Hide the “怎么确认绑定成功” guide when BossClaw bind channel is 企业微信 or 飞书.
- Keep the guide visible for personal WeChat only.
- Add a unit test covering personal WeChat, WeCom, and Feishu channel switching.

## Root cause
The bind confirmation guide was rendered unconditionally in the QR step, so all binding channels inherited the personal WeChat confirmation instructions.

## Test plan
- [x] pnpm --dir web/app test:unit tests/unit/bossclaw/wechat-bind-step.unit.spec.tsx tests/unit/bossclaw/bossclaw-layout-css.unit.spec.ts tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx
- [x] pnpm --dir web lint
- [x] pnpm --dir web exec tsc --noEmit --project app/tsconfig.json
- [x] git diff --check
- [x] GitHub CI for PR #2665
