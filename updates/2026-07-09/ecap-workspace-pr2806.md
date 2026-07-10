---
title: "低余额付费提示体验优化：不打断发送、提示不再频繁弹出"
type: "体验优化"
priority: "中"
date: "2026-07-09"
status: "待审核"
channels: ""
---

## 核心宣传点

余额不足时弹出的订阅提示不再打断你当前的发送，消息会继续送出；同时该提示做了 30 分钟冷却限流，不会频繁弹窗，提示文案也更清晰、不会让人误以为消息被拦截。

## 原始内容

**合并两条相关改动（低余额付费提示体验）**

1. **fix(billing): keep sends after low-credit prompt (#2806)**
SHA: `ac7076eacfc658849b652c8229296e4a75cf59ab` | 作者: tim-srp | PR #2806

```
fix(billing): keep sends after low-credit prompt (#2806)

## Summary
- Keep the current message/task send going after the low-credit billing
prompt is shown.
- Preserve the 30-minute prompt cooldown behavior: first send can open
the subscription panel, cooldown sends show a toast.
- Update the cooldown toast copy so it does not imply the message was
blocked.

## Product decision
This PR intentionally makes the frontend billing send gate advisory:
providerless low-credit and billing-not-ready users should still have
the current send proceed after seeing a subscription panel or cooldown
toast. The same advisory behavior applies to later sends during the
30-minute cooldown window; the goal is frequent subscription visibility
without dropping user messages.

## Root cause
The previous billing gate treated providerless low-credit and
billing-not-ready states as hard blockers by returning false after
showing the panel/toast. Chat and new-chat callers interpret false as
canceling the in-flight send.

## Test plan
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/hooks/useBillingSendGate.unit.spec.ts
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/hooks/useBillingSendGate.unit.spec.ts
tests/unit/components/GiftPaywallFab.unit.spec.tsx
tests/unit/lib/billing/card-bind-gate.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/new-chat/useViewModel.unit.spec.tsx
- [x] pnpm --dir web/app run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
- [x] pnpm --dir web/app run lint:ci
- [x] pnpm --dir web/app run test:unit
- [x] git diff --check

Note: pnpm --dir web run tsc currently fails before typechecking because
the aggregate script calls pnpm exec with unsupported --if-present under
pnpm 10; web/app tsc passed.
```

**PR body:**

## Summary
- Keep the current message/task send going after the low-credit billing prompt is shown.
- Preserve the 30-minute prompt cooldown behavior: first send can open the subscription panel, cooldown sends show a toast.
- Update the cooldown toast copy so it does not imply the message was blocked.

## Product decision
This PR intentionally makes the frontend billing send gate advisory: providerless low-credit and billing-not-ready users should still have the current send proceed after seeing a subscription panel or cooldown toast. The same advisory behavior applies to later sends during the 30-minute cooldown window; the goal is frequent subscription visibility without dropping user messages.

## Root cause
The previous billing gate treated providerless low-credit and billing-not-ready states as hard blockers by returning false after showing the panel/toast. Chat and new-chat callers interpret false as canceling the in-flight send.

## Test plan
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/hooks/useBillingSendGate.unit.spec.ts
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/hooks/useBillingSendGate.unit.spec.ts tests/unit/components/GiftPaywallFab.unit.spec.tsx tests/unit/lib/billing/card-bind-gate.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/new-chat/useViewModel.unit.spec.tsx
- [x] pnpm --dir web/app run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
- [x] pnpm --dir web/app run lint:ci
- [x] pnpm --dir web/app run test:unit
- [x] git diff --check

Note: pnpm --dir web run tsc currently fails before typechecking because the aggregate script calls pnpm exec with unsupported --if-present under pnpm 10; web/app tsc passed.

---

2. **fix(billing): rate-limit low-credit paywall prompts (#2800)**
SHA: `d6ec8cfe24d6a2334eabdf600372b70363a2e1c3` | 作者: tim-srp | PR #2800

```
fix(billing): rate-limit low-credit paywall prompts (#2800)

## Summary
- Keep the existing billing send-gate result for low-credit/providerless
users: blocked paths still return false.
- Rate-limit the subscription panel prompt to once per uid per 30-minute
browser session window.
- Add unit coverage for blocked-result preservation, cooldown
boundaries, and cross-hook-instance cooldown.

## Verification
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/hooks/useBillingSendGate.unit.spec.ts
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/new-chat/useViewModel.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit --pretty false
- pnpm --dir web/app run lint
- git diff --check
```

**PR body:**

## Summary
- Keep the existing billing send-gate result for low-credit/providerless users: blocked paths still return false.
- Rate-limit the subscription panel prompt to once per uid per 30-minute browser session window.
- Add unit coverage for blocked-result preservation, cooldown boundaries, and cross-hook-instance cooldown.

## Verification
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/hooks/useBillingSendGate.unit.spec.ts tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/new-chat/useViewModel.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit --pretty false
- pnpm --dir web/app run lint
- git diff --check
