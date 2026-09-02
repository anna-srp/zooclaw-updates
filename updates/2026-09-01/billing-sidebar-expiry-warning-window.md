---
title: "修复：订阅还有大半年到期，侧边栏就一直挂着红色到期警告"
type: "Bug Fix"
priority: "中"
date: "2026-09-01"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：订阅还有大半年到期，侧边栏就一直挂着红色到期警告

## 核心宣传点

侧边栏那条红色的「订阅即将结束」提醒以前不看时间远近，只要处于会到期的状态就一直显示，离到期还有很久也在提示，久而久之就被忽略了。现在改成只在当前计费周期距结束 30 天以内才亮出来。账单页的到期与续费展示逻辑保持不变，到期日期改为显示四位年份，跨年的日期不会再看着有歧义。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `374be8b587b7de364bd28a48fd585945bc80aa94`
- PR: #3613
- 作者: tim-srp
- 日期: 2026-09-01T11:30:13Z

### Commit Message

```
fix(billing): limit sidebar expiry warning (#3613)

## Summary

- Show the sidebar's red subscription-ending warning only when the
current period ends within 30 days.
- Preserve Billing-page ending and renewal behavior, while displaying
four-digit years for ending dates.
- Add regression coverage for the 30-day boundary and cross-year date
labels.

## Test Plan

- [x] `pnpm exec vitest run
tests/unit/components/billing/subscription-expiry.unit.spec.ts
tests/unit/components/UserCard.unit.spec.tsx
tests/unit/components/billing/SharedPlanCard.unit.spec.tsx --config
./vitest.config.mts`
- [x] `bash scripts/verify-changed.sh`
- [ ] Full `pnpm test` remains blocked by unrelated
`mock-backend-agent-builder` jsdom navigation failures.
```

### PR Body

```
## Summary

- Show the sidebar's red subscription-ending warning only when the current period ends within 30 days.
- Preserve Billing-page ending and renewal behavior, while displaying four-digit years for ending dates.
- Add regression coverage for the 30-day boundary and cross-year date labels.

## Test Plan

- [x] `pnpm exec vitest run tests/unit/components/billing/subscription-expiry.unit.spec.ts tests/unit/components/UserCard.unit.spec.tsx tests/unit/components/billing/SharedPlanCard.unit.spec.tsx --config ./vitest.config.mts`
- [x] `bash scripts/verify-changed.sh`
- [ ] Full `pnpm test` remains blocked by unrelated `mock-backend-agent-builder` jsdom navigation failures.

```
