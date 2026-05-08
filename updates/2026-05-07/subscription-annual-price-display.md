---
title: "订阅页面补充年付总价展示"
type: "体验优化"
priority: "中"
date: "2026-05-07"
status: "待审核"
channels: ""
---
# 订阅页面补充年付总价展示

## 核心宣传点
选择年付套餐时，现在可以清晰看到每年实际扣款金额（如 "Billed annually, $200/year"），订阅更透明，不再只看月均价。

## 原始内容

### Commit Message
```
feat(web): 订阅价格 + paywall 全量补 "Billed annually, $X/year" + dev FAB 可拖拽 (#1570)
```

### PR Description
## Summary

订阅展示全链路补齐 **Billed annually, $X/year** 年总价行，让用户一眼看到年付实际扣多少钱，而不是只显示折算后的月单价。

### 三个价格展示入口都加了年付明细行（yearly cycle 下）

| 入口 | 文件 | 套餐 | 显示 |
|---|---|---|---|
| 订阅升级 modal | `src/components/billing/PlanCard.tsx` | Starter / Pro / Ultra | $200 / $1,000 / $2,000 |
| 官网 Pricing 页面 | `src/app/[locale]/pricing/PublicPricingClient.tsx` | Starter / Pro / Ultra | 同上，**接 i18n 10 个 locale** |
| Starter 试用 paywall | `src/components/PaywallContent.tsx` | Starter | $200（月单价 + 年总价合并到同一行，中间用 · 分隔）|

### 实现要点

- **价格单一 source of truth**：三处都从 `src/lib/stripe/stripe.ts` 的 `PLAN_PRICING`（cents）读出，UI 层 `/100` + `toLocaleString('en-US')` 拿千分位逗号 — Pro `$1,000`、Ultra `$2,000` 都带逗号。将来改套餐价只需要改 `stripe.ts`，三处 UI 自动同步。
- **i18n 覆盖**：新增 `publicPricing.billedAnnually` key 覆盖 10 个 locale（en/zh/ja/ko/de/es/fr/it/pt/ar），用 `{total}` 占位符接已格式化好的字符串，翻译只控制句式不重做数字格式化。
