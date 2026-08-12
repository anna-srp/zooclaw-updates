---
title: "信用卡试用期内可直接升级到 Pro / Ultra"
type: "新功能上线"
priority: "高"
date: "2026-08-11"
status: "待审核"
channels: ""
---

## 核心宣传点

还在 Starter 信用卡免费试用期，就能立刻升级到 Pro 或 Ultra 正式版，原有试用积分照常保留，旧试用订阅自动取消，不用等试用结束。

## 原始内容

### commit message

```
feat(billing): support Card trial upgrades (#3327)
```

### PR body

## Summary

- complete Creem trial payment orders and preserve exact idempotent replay for webhook and reconciliation retries
- allow eligible Starter Card Trial subscriptions to upgrade immediately to paid Pro or Ultra on either billing cycle
- atomically promote the paid replacement, retain existing Trial credits, and immediately cancel the superseded Creem Trial
- persist replacement cleanup intent and retry incomplete provider cancellation from hourly reconciliation
- recover legacy partial Trial orders after Creem has already transitioned the subscription to `active`
- keep immediate cleanup pending until Creem reports terminal `canceled`, and block expired Trial upgrades in the client
- keep existing active Card upgrade rules and Antom/Alipay behavior unchanged

## Behavior

- Eligible Trial upgrade: current Creem/Card agreement is `trialing`, Starter, unexpired, current, and not scheduled for cancellation
- Paid replacement checkout: `expects_trial=false` and `checkout_intent=upgrade`
- Entitlements: the paid subscription becomes current; Trial credits are not revoked or duplicated
- Provider cleanup: Trial replacement uses Creem `mode=immediate`; active paid replacement remains `mode=scheduled`
- Recovery: atomic handoff stores an immutable cleanup mode; hourly reconciliation retries incomplete cleanup and narrowly repairs identity-matched partial Trial projections without issuing duplicate entitlements

## Validation

- `bash scripts/verify-web.sh ...` — TypeScript passed; 89 frontend tests passed; ESLint passed with one pre-existing warning
- targeted backend unit suite — 355 passed
- targeted Pyright for all changed backend files and tests — 0 errors
- `bash scripts/verify-py.sh --no-types` — Ruff, formatting, and import-linter passed
- all eight custom Python lint guards passed (line limit, architecture, complexity, dependency, collection, repo-list, dead-code and database-return checks)
- `bash scripts/check-pr-size.sh` — 1256 / 3000 lines
- real Mongo transaction test remains opt-in and was not run locally; its updated call contract passes Pyright

## Risk

Medium. The change touches Card/Creem subscription replacement and reconciliation, with strict current-agreement, provider, environment, plan, cycle, expiry, cancellation, and immutable-linkage guards. Antom/Alipay files and behavior are unchanged.


