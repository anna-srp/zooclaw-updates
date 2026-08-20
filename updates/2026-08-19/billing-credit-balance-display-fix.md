---
title: "修复：账户额度显示不一致，侧边栏把总额当成了剩余额度"
type: "Bug Fix"
priority: "中"
date: "2026-08-19"
status: "待审核"
channels: ""
---

# 修复：账户额度显示不一致，侧边栏把总额当成了剩余额度

## 核心宣传点

收起状态的侧边栏原本把「钱包总容量」当成「可用额度」显示，设置→用量页也会把已用额度重复扣一次，导致同一个账号在不同位置看到不同数字。现已统一为真实剩余额度；试用额度用尽时的提醒也恢复正常触发。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `bbd20fe2b58a63952a30ba00b86eeddd58b25a78`
- PR: #3416
- 作者: rayrain-srp
- 日期: 2026-08-19T08:09:48Z

### Commit Message

```
fix(billing): align credit balance displays (#3416)

## Summary

- correct every frontend billing mock so subscription and top-up fields
represent initial wallet capacity instead of remaining balance
- make the collapsed desktop sidebar use canonical `availableCredits`
instead of aliasing total wallet capacity
- preserve exhausted-trial warnings by checking canonical remaining
credits instead of subscription capacity
- add regression coverage for the mock credit invariants, the reported
`active-pro` display, and the sidebar prop mapping
- Linear:
https://linear.app/srpone/issue/ECA-1384/staging-billing-mock-shows-inconsistent-credit-balances-across-account

## Root cause

The staging `active-pro` mock mixed two different meanings for its
credit fields: `totalCredits` was 20,000, while `subscriptionCredits`
incorrectly contained the remaining 11,500. The account menu rendered
`availableCredits` directly, but Settings → Usage treated
`subscriptionCredits + topupCredits` as initial capacity and subtracted
the 8,500 usage again, producing 3,000 / 11,500.

Separately, the collapsed desktop sidebar renamed `walletTotal` to
`availableCredits`, so real accounts with consumed credits could see
total capacity in the tooltip.

The corrected mock semantics also exposed an existing consumer bug:
`SubscriptionPanel` used subscription capacity for its low-credit
warning. It now checks `availableCredits`, so an exhausted trial still
warns even when its initial capacity is non-zero.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to all six changed source and
test files (130 related tests)
- [x] pre-commit full frontend ESLint
- [x] pre-push size budget, governance guards, TypeScript, and full
frontend ESLint
```

### PR Body

## Summary

- correct every frontend billing mock so subscription and top-up fields represent initial wallet capacity instead of remaining balance
- make the collapsed desktop sidebar use canonical `availableCredits` instead of aliasing total wallet capacity
- preserve exhausted-trial warnings by checking canonical remaining credits instead of subscription capacity
- add regression coverage for the mock credit invariants, the reported `active-pro` display, and the sidebar prop mapping
- Linear: https://linear.app/srpone/issue/ECA-1384/staging-billing-mock-shows-inconsistent-credit-balances-across-account

## Root cause

The staging `active-pro` mock mixed two different meanings for its credit fields: `totalCredits` was 20,000, while `subscriptionCredits` incorrectly contained the remaining 11,500. The account menu rendered `availableCredits` directly, but Settings → Usage treated `subscriptionCredits + topupCredits` as initial capacity and subtracted the 8,500 usage again, producing 3,000 / 11,500.

Separately, the collapsed desktop sidebar renamed `walletTotal` to `availableCredits`, so real accounts with consumed credits could see total capacity in the tooltip.

The corrected mock semantics also exposed an existing consumer bug: `SubscriptionPanel` used subscription capacity for its low-credit warning. It now checks `availableCredits`, so an exhausted trial still warns even when its initial capacity is non-zero.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to all six changed source and test files (130 related tests)
- [x] pre-commit full frontend ESLint
- [x] pre-push size budget, governance guards, TypeScript, and full frontend ESLint

