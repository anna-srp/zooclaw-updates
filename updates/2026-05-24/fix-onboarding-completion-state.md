---
title: "修复新用户引导流程完成状态丢失问题"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-24"
status: "待审核"
channels: ""
---

# 修复新用户引导流程完成状态丢失问题

## 核心宣传点

新用户完成引导流程后，系统现在会正确记录并保持完成状态，不再反复出现引导步骤。

## 原始内容

**Commit**: `24046a354d2448f0d42f92d66d2e0ed94a9a4d39`
**Title**: fix(onboarding): persist completion state (#1893)
**Author**: tim-srp
**Date**: 2026-05-24T13:30:48Z

**Commit Message**:
```
fix(onboarding): persist completion state (#1893)

## Summary
- Add explicit onboarding_completed lifecycle state for ecap accounts
and default new accounts to false
- Add authenticated /users/onboarding/complete backend endpoint plus
Next API proxy
- Make frontend onboarding resolver prioritize onboardingCompleted over
bot/credits readiness, with legacy null fallback
- Patch cached backend onboarding status after complete endpoint
succeeds

## Tests
- pnpm --dir web/app run lint
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app run test:unit --
tests/unit/components/onboarding/resolveOnboardingStatus.unit.spec.ts
tests/unit/lib/api/user.unit.spec.ts
tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
- cd services/claw-interface && ruff check app
tests/unit/test_user_routes_coverage.py && pytest -W
ignore::PendingDeprecationWarning -q
tests/unit/test_user_routes_coverage.py

Note: local manual pyright without the backend venv reports dependency
missing imports; CI/pre-commit standard environment covers pyright.
```

**PR Description**:

## Summary
- Add explicit onboarding_completed lifecycle state for ecap accounts and default new accounts to false
- Add authenticated /users/onboarding/complete backend endpoint plus Next API proxy
- Make frontend onboarding resolver prioritize onboardingCompleted over bot/credits readiness, with legacy null fallback
- Patch cached backend onboarding status after complete endpoint succeeds

## Tests
- pnpm --dir web/app run lint
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app run test:unit -- tests/unit/components/onboarding/resolveOnboardingStatus.unit.spec.ts tests/unit/lib/api/user.unit.spec.ts tests/unit/lib/auth/manager.unit.spec.ts tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
- cd services/claw-interface && ruff check app tests/unit/test_user_routes_coverage.py && pytest -W ignore::PendingDeprecationWarning -q tests/unit/test_user_routes_coverage.py

Note: local manual pyright without the backend venv reports dependency missing imports; CI/pre-commit standard environment covers pyright.
