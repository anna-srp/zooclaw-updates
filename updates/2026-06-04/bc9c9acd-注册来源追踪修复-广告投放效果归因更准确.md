---
title: "注册来源追踪修复，广告投放效果归因更准确"
type: "Bug Fix"
priority: "中"
date: "2026-06-04"
status: "待审核"
channels: ""
sha: "bc9c9acd91111c6912137d261c12874de622f122"
repo: "ecap-workspace"
pr: "2200"
---

# 注册来源追踪修复，广告投放效果归因更准确

## 核心宣传点

修复了注册时 UTM 参数和广告点击 ID 可能丢失的问题，营销投放的注册转化归因更准确。

## 原始内容

### Commit Message

```
fix(web): preserve signup attribution context (#2200)

## Summary
- capture a first-session attribution snapshot for landing URLs, UTM
params, and Google Ads auto-tagging click IDs
- attach attribution diagnostics to sign_up GA4 and Google Ads
conversion events
- track page views when query params change so UTM-only route changes
are observable
- sanitize referrer URLs before sending diagnostics

## Safety
- does not change login, OTP, user creation, routing, backend API,
payment, or onboarding logic
- storage and URL parsing failures are swallowed so attribution
diagnostics cannot block registration
- no email, phone, user ID, token, or arbitrary query params are sent

## Tests
- pnpm exec vitest run --config ./vitest.config.mts
tests/unit/lib/attribution-snapshot.unit.spec.ts
tests/unit/lib/tracking.unit.spec.ts
- pnpm run test:unit
- pnpm run lint
```

### PR Description

## Summary
- capture a first-session attribution snapshot for landing URLs, UTM params, and Google Ads auto-tagging click IDs
- attach attribution diagnostics to sign_up GA4 and Google Ads conversion events
- track page views when query params change so UTM-only route changes are observable
- sanitize referrer URLs before sending diagnostics

## Safety
- does not change login, OTP, user creation, routing, backend API, payment, or onboarding logic
- storage and URL parsing failures are swallowed so attribution diagnostics cannot block registration
- no email, phone, user ID, token, or arbitrary query params are sent

## Tests
- pnpm exec vitest run --config ./vitest.config.mts tests/unit/lib/attribution-snapshot.unit.spec.ts tests/unit/lib/tracking.unit.spec.ts
- pnpm run test:unit
- pnpm run lint
