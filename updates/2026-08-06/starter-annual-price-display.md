---
title: "修正 Starter 年付价格显示"
type: "Bug Fix"
priority: "中"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

定价页 Starter 年付原先误显示为 $20/月，现更正为 $17/月，并明确试用期后按 $200/年 收取。

## 原始内容

**fix(pricing): correct starter annual price display (#3279)**

- sha: `6c1ac8ed84baba80a8f6b579d0da290194e84c46`
- PR: #3279

```
fix(pricing): correct starter annual price display (#3279)

## Summary

- update the Starter annual billing display from `$20/month` to
`$17/month`
- clarify that the post-trial annual charge is `$200/year`
- leave the monthly price and Stripe billing configuration unchanged

## Testing

- `bash scripts/verify-web.sh
'src/app/[locale]/(marketing)/pricing/PublicPricingClient.tsx'
src/locales/en.ts`
- `bash scripts/verify-changed.sh`
- local `/en/pricing` preview verified successfully

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

**PR Body:**

## Summary

- update the Starter annual billing display from `$20/month` to `$17/month`
- clarify that the post-trial annual charge is `$200/year`
- leave the monthly price and Stripe billing configuration unchanged

## Testing

- `bash scripts/verify-web.sh 'src/app/[locale]/(marketing)/pricing/PublicPricingClient.tsx' src/locales/en.ts`
- `bash scripts/verify-changed.sh`
- local `/en/pricing` preview verified successfully

