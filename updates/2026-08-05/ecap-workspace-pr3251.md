---
title: "修复企业账号迁移后权益丢失"
type: "Bug Fix"
priority: "高"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 修复企业账号迁移后权益丢失

## 核心宣传点

修复部分企业账号在支付渠道迁移后被误降级为免费版的问题，企业模型、OpenClaw 与套餐权益已恢复。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`e8d9f34d6c0f98a6ee775167713a7f862bf843f7`
- 作者：tim-srp
- 日期：2026-08-05T12:43:19Z
- PR：#3251

### Commit Message

```
fix(billing): preserve enterprise access after Stripe cutover (#3251)

## Summary

- preserve enterprise model, OpenClaw, billing-summary, and Vertical
package access for the exact legacy Stripe account-cutover recovery
state
- prefer ordinary effective enterprise agreements and fail closed for
expired, ambiguous, near-match, or successor-owned recovery records
- extend the Vertical reconciliation migration to cover retained cutover
agreements and verify production-shaped LiteLLM team responses
- keep stored subscription status, credits, Stripe identifiers, and Lago
state unchanged

## Root cause

The Stripe account cutover intentionally retained some
enterprise-package agreements as non-current manual-review records.
Existing access surfaces only recognized current agreements in normal
provider statuses, so those teams fell back to Starter/free behavior
even though their retained enterprise period and team billing remained
valid.

## Test plan

- [x] Project backend static gate: ruff check, ruff format, pyright, and
import-linter
- [x] Targeted unit suite: 147 passed
- [x] Pre-commit backend checks, including dependency consistency and
architecture contracts
- [x] Diff and PR-size checks
```

### PR Body

## Summary

- preserve enterprise model, OpenClaw, billing-summary, and Vertical package access for the exact legacy Stripe account-cutover recovery state
- prefer ordinary effective enterprise agreements and fail closed for expired, ambiguous, near-match, or successor-owned recovery records
- extend the Vertical reconciliation migration to cover retained cutover agreements and verify production-shaped LiteLLM team responses
- keep stored subscription status, credits, Stripe identifiers, and Lago state unchanged

## Root cause

The Stripe account cutover intentionally retained some enterprise-package agreements as non-current manual-review records. Existing access surfaces only recognized current agreements in normal provider statuses, so those teams fell back to Starter/free behavior even though their retained enterprise period and team billing remained valid.

## Test plan

- [x] Project backend static gate: ruff check, ruff format, pyright, and import-linter
- [x] Targeted unit suite: 147 passed
- [x] Pre-commit backend checks, including dependency consistency and architecture contracts
- [x] Diff and PR-size checks

