---
title: "修复：信用卡免费试用的赠送额度按试用标准发放"
type: "Bug Fix"
priority: "中"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# 修复：信用卡免费试用的赠送额度按试用标准发放

## 核心宣传点

信用卡免费试用开通时会准确发放 1,000 试用额度；试用结束后首次付费仍照常发放完整的 Starter 4,800 额度，试用剩余额度不会被扣掉。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e1c932d2eba11817f48bebac5085c70e7c802cf6`
- PR: #3358

### Commit Message

```
fix(billing): cap Creem trial credits (#3358)

## Summary
- Grant exactly 1,000 credits for a Creem Card subscription trial
instead of the Starter paid-plan allowance.
- Keep the first successful paid Starter transaction at the full
4,800-credit grant.
- Add regression assertions for both the trial entitlement and the
Billing Gateway paid entitlement payload.

## Root cause
The Creem trial projection reused `credits_for_plan("starter")`, which
returns the paid Starter allowance of 4,800. Other subscription trials
use the dedicated 1,000-credit trial allowance.

## Test plan
- [x] Red test observed `4800 != 1000` before the fix.
- [x] 60 focused Creem Trial and first-payment tests pass.
- [x] 118 broader Trial/first-payment/reconciliation tests passed before
the paid-handoff assertion was strengthened.
- [x] Ruff check and format pass.
- [x] Commit-time Pyright and repository policy hooks pass.
- [ ] GitHub Code Quality Check passes.

## Expected behavior
- Trial activation adds 1,000 credits.
- The first successful charge after the seven-day trial adds a separate
full 4,800-credit Starter entitlement; remaining trial credits are not
deducted.
```

### PR Body

## Summary
- Grant exactly 1,000 credits for a Creem Card subscription trial instead of the Starter paid-plan allowance.
- Keep the first successful paid Starter transaction at the full 4,800-credit grant.
- Add regression assertions for both the trial entitlement and the Billing Gateway paid entitlement payload.

## Root cause
The Creem trial projection reused `credits_for_plan("starter")`, which returns the paid Starter allowance of 4,800. Other subscription trials use the dedicated 1,000-credit trial allowance.

## Test plan
- [x] Red test observed `4800 != 1000` before the fix.
- [x] 60 focused Creem Trial and first-payment tests pass.
- [x] 118 broader Trial/first-payment/reconciliation tests passed before the paid-handoff assertion was strengthened.
- [x] Ruff check and format pass.
- [x] Commit-time Pyright and repository policy hooks pass.
- [ ] GitHub Code Quality Check passes.

## Expected behavior
- Trial activation adds 1,000 credits.
- The first successful charge after the seven-day trial adds a separate full 4,800-credit Starter entitlement; remaining trial credits are not deducted.


---
