---
title: "修复 Stripe 续费积分重复发放问题"
type: "Bug Fix"
priority: "高"
date: "2026-05-21"
status: "待审核"
channels: "Discord, changelog"
---

# 修复 Stripe 续费积分重复发放问题

## 核心宣传点

修复了 Stripe 续费时积分可能被多次发放的 Bug，账户积分记录更准确。

## 原始内容

```
fix(billing): dedupe Stripe renewal credit grants (#1829)

Prevent duplicate credit grants when Stripe renewal webhooks are retried or delivered multiple times. Idempotency key added to credit grant operations.
```
