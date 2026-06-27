---
title: "BossClaw 兑换码可从链接自动填充"
type: "体验优化"
priority: "低"
date: "2026-06-26"
status: "待审核"
channels: ""
---
# BossClaw 兑换码可从链接自动填充

## 核心宣传点
通过带兑换码的 BossClaw 邀请链接进入时，兑换码会自动填好，少一步手动输入，兑换更顺畅。

## 原始内容
```
fix(bossclaw): prefill subscription code from url (#2618)

## Summary
- Support `subscription_code=...` on the BossClaw onboarding URL.
- Prefill the redeem-code input from the server-provided query param or
browser URL fallback.
- Keep the typed value intact if the user has already entered a code
before the initial code arrives.

## Root cause
The BossClaw campaign page only forwarded `boss_key`; the redeem step
always initialized with an empty code and did not react to a
late-arriving initial value.

## Test plan
- [x] `pnpm --dir web/app test:unit tests/unit/bossclaw`
- [x] `pnpm --dir web/app exec eslint
'src/app/[locale]/bossclaw/BossclawClient.tsx'
'src/app/[locale]/bossclaw/components/RedeemStep.tsx'
'src/app/[locale]/bossclaw/page.tsx'
tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx
tests/unit/bossclaw/page.unit.spec.tsx
tests/unit/bossclaw/redeem-step.unit.spec.tsx --quiet`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `git diff --check origin/main..HEAD`
```

### PR description

## Summary
- Support `subscription_code=...` on the BossClaw onboarding URL.
- Prefill the redeem-code input from the server-provided query param or browser URL fallback.
- Keep the typed value intact if the user has already entered a code before the initial code arrives.

## Root cause
The BossClaw campaign page only forwarded `boss_key`; the redeem step always initialized with an empty code and did not react to a late-arriving initial value.

## Test plan
- [x] `pnpm --dir web/app test:unit tests/unit/bossclaw`
- [x] `pnpm --dir web/app exec eslint 'src/app/[locale]/bossclaw/BossclawClient.tsx' 'src/app/[locale]/bossclaw/components/RedeemStep.tsx' 'src/app/[locale]/bossclaw/page.tsx' tests/unit/bossclaw/bossclaw-client-intro.unit.spec.tsx tests/unit/bossclaw/page.unit.spec.tsx tests/unit/bossclaw/redeem-step.unit.spec.tsx --quiet`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `git diff --check origin/main..HEAD`

