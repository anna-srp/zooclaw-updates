---
title: "修复新手引导状态错误：多账号使用不再互相干扰"
type: "Bug Fix"
priority: "中"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 修复新手引导状态错误：多账号使用不再互相干扰

## 核心宣传点

修复了多个账号在同一设备上使用时，新手引导完成状态相互干扰的问题，每个账号现在有独立的引导流程。

## 原始内容

**Commit**: 2e388e717c16c6e4b39101707adead53d261d22c
**Author**: Chris@ZooClaw
**Date**: 2026-05-22T13:46:47Z
**PR**: #1860

### Commit Message
```
fix(web): scope onboarding status by user (#1860)

## Summary
- Scope cached onboarding backend status snapshots by uid so login-time
status events survive auth uid transitions.
- Filter stale onboarding snapshots in OnboardingProvider instead of
clearing the shared cache on every uid change.
- Add regression coverage for the ECA-800 login/onboarding race and
phone verify duplicate-click behavior.

## Linear

https://linear.app/srpone/issue/ECA-800/bug-手机验证码登录后重复出现验证码输入框并进入-unable-to-connect-页面

## Tests
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/app exec vitest run tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/components/providers/OnboardingProvider.unit.spec.tsx
tests/unit/app/user-verify-phone.unit.spec.tsx
tests/unit/components/LoginForm.unit.spec.tsx --config
./vitest.config.mts`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/app exec tsc --noEmit --project app/tsconfig.json`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/app run lint`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/app run test:unit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web run lint`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web run test:unit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/enterprise-admin exec tsc --noEmit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir
web/packages/auth-client exec tsc --noEmit`

Note: `pnpm --dir web run tsc` currently exits before typechecking with
pnpm `Unknown option: if-present`; package-level tsc checks above were
used as the workaround.
```

### PR Description
## Summary
- Scope cached onboarding backend status snapshots by uid so login-time status events survive auth uid transitions.
- Filter stale onboarding snapshots in OnboardingProvider instead of clearing the shared cache on every uid change.
- Add regression coverage for the ECA-800 login/onboarding race and phone verify duplicate-click behavior.

## Linear
https://linear.app/srpone/issue/ECA-800/bug-手机验证码登录后重复出现验证码输入框并进入-unable-to-connect-页面

## Tests
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/app exec vitest run tests/unit/lib/auth/manager.unit.spec.ts tests/unit/components/providers/OnboardingProvider.unit.spec.tsx tests/unit/app/user-verify-phone.unit.spec.tsx tests/unit/components/LoginForm.unit.spec.tsx --config ./vitest.config.mts`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/app exec tsc --noEmit --project app/tsconfig.json`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/app run lint`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/app run test:unit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web run lint`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web run test:unit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/enterprise-admin exec tsc --noEmit`
- `PATH=/Users/xuwenhao/.nvm/versions/node/v24.15.0/bin:$PATH pnpm --dir web/packages/auth-client exec tsc --noEmit`

Note: `pnpm --dir web run tsc` currently exits before typechecking with pnpm `Unknown option: if-present`; package-level tsc checks above were used as the workaround.


