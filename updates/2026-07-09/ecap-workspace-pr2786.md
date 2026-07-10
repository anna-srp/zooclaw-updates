---
title: "免费体验改为绑卡后 7 天免费，订阅用户流程不变"
type: "产品基础功能更新"
priority: "中"
date: "2026-07-09"
status: "待审核"
channels: ""
---

## 核心宣传点

新用户通过邀请绑定后，将获得绑卡后 7 天免费访问（不再直接发放试用额度）；已订阅的正式用户体验保持不变。首次进入聊天页会引导完成绑卡，让免费体验与后续付费衔接更顺畅。

## 原始内容

**fix(billing): gate free-access users on card binding (#2786)**

SHA: `00aff2ab017266fdb38aa438454f4a03ebe41ae5` | 作者: tim-srp | PR #2786

```
fix(billing): gate free-access users on card binding (#2786)

## Summary
- Change invite binding from trial-credit grant to zero-credit seven-day
free access.
- Add a provider-backed subscription gate so real Stripe/Antom
subscribers keep the existing low-credit banner flow.
- Auto-open the existing card-binding paywall once per browser session
on `/chat` and `/new-chat` for providerless users.
- Block every chat/new-chat send attempt for providerless users when the
real-time credits check is insufficient.
- Add a conservative positive credits cache: 30-minute TTL, cache only
when `available_credits >= 50`, locally reserve expected credits, and
fail open after a 3-second credits-check timeout.

## Testing
- `NODE_OPTIONS=--no-deprecation ./node_modules/.bin/vitest run --config
./vitest.config.mts tests/unit/lib/billing/card-bind-gate.unit.spec.ts
tests/unit/hooks/useBillingSendGate.unit.spec.ts
tests/unit/components/GiftPaywallFab.unit.spec.tsx
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/new-chat/useViewModel.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx`
- `NODE_OPTIONS=--no-deprecation ./node_modules/.bin/tsc --noEmit
--pretty false`
- `pnpm lint:imports`
- `pnpm run lint` from `web` (0 errors; existing enterprise-app
warnings)
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit --pretty false`
- `pnpm --filter @zooclaw/web-app run test:unit`
- `pytest
services/claw-interface/tests/unit/test_user_bind_invite_trial.py
services/claw-interface/tests/unit/test_user_free_access_service.py -q`
- `ruff check .` from `services/claw-interface`
- `pyright --pythonpath "$(which python)"
tests/unit/test_user_bind_invite_trial.py` from
`services/claw-interface`

## Notes
- I also started the full backend coverage command locally, but stopped
it after several minutes because this local Python/protobuf warning
configuration was producing unrelated admin cron setup errors; the
affected backend tests above pass.
```

**PR body:**

## Summary
- Change invite binding from trial-credit grant to zero-credit seven-day free access.
- Add a provider-backed subscription gate so real Stripe/Antom subscribers keep the existing low-credit banner flow.
- Auto-open the existing card-binding paywall once per browser session on `/chat` and `/new-chat` for providerless users.
- Block every chat/new-chat send attempt for providerless users when the real-time credits check is insufficient.
- Add a conservative positive credits cache: 30-minute TTL, cache only when `available_credits >= 50`, locally reserve expected credits, and fail open after a 3-second credits-check timeout.

## Testing
- `NODE_OPTIONS=--no-deprecation ./node_modules/.bin/vitest run --config ./vitest.config.mts tests/unit/lib/billing/card-bind-gate.unit.spec.ts tests/unit/hooks/useBillingSendGate.unit.spec.ts tests/unit/components/GiftPaywallFab.unit.spec.tsx tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/new-chat/useViewModel.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx`
- `NODE_OPTIONS=--no-deprecation ./node_modules/.bin/tsc --noEmit --pretty false`
- `pnpm lint:imports`
- `pnpm run lint` from `web` (0 errors; existing enterprise-app warnings)
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit --pretty false`
- `pnpm --filter @zooclaw/web-app run test:unit`
- `pytest services/claw-interface/tests/unit/test_user_bind_invite_trial.py services/claw-interface/tests/unit/test_user_free_access_service.py -q`
- `ruff check .` from `services/claw-interface`
- `pyright --pythonpath "$(which python)" tests/unit/test_user_bind_invite_trial.py` from `services/claw-interface`

## Notes
- I also started the full backend coverage command locally, but stopped it after several minutes because this local Python/protobuf warning configuration was producing unrelated admin cron setup errors; the affected backend tests above pass.

