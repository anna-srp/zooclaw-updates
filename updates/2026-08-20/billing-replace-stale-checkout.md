---
title: "修复：支付未成功后改选套餐可以重新下单"
type: "Bug Fix"
priority: "中"
date: "2026-08-20"
status: "待审核"
channels: ""
---

# 修复：支付未成功后改选套餐可以重新下单

## 核心宣传点

以前一次信用卡支付没成功后，如果换个套餐再下单，会被之前那笔挂着的旧支付单挡住。现在系统会自动替换掉这类失效的待支付单，改选套餐后能直接重新发起支付；确实失败或状态不明的单子仍保留供人工核查，不会重复扣款。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `059948fcd842a91c9c65069cfd1802eb929e4115`
- PR: #3471
- 作者: tim-srp
- 日期: 2026-08-20T14:23:50Z

### Commit Message

```
fix(billing): replace stale Airwallex checkout (#3471)
```

### PR Body

## Summary

- replace a stale pending Airwallex checkout when a user changes subscription selection after an unsuccessful payment
- retain failed/ambiguous checkout outcomes for manual review and prevent duplicate provider mutations
- keep completed subscriptions outside this flow; plan changes continue through upgrade/downgrade handling

## Validation

- 193 focused backend tests passed
- ruff, formatting, import-linter, and project-venv Pyright pre-commit checks passed


