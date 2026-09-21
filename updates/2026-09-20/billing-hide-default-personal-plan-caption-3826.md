---
title: "fix(billing): hide default personal plan billing caption (#3826)"
type: "Bug Fix"
priority: "低"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 修复：非 Team 账号不再显示多余的按月计费说明

## 核心宣传点

Pro 订阅按钮下方的「Billed monthly. Cancel anytime.」以及它占的空白，在非 Team 账号上会被隐藏；Team 账号仍然保留「Contact Sales to manage your team plan.」。这是默认个人套餐场景下的一处文案冗余，属于纯展示层修正。

## 分级

- 内部：P3
- 外部：C
- 发布状态：已合并待发版

## PR 说明

## Summary
Hide “Billed monthly. Cancel anytime.” below the Pro subscription button for non-Team accounts, including its empty spacing. Team accounts retain “Contact Sales to manage your team plan.”

## Root cause
The default personal plan state supplied a billing caption that is no longer needed. Renewal dates, expiration notices, purchase restrictions, and checkout behavior remain unchanged.

## Test plan
- [x] ProPlanAction unit suite: 21 tests passed.
- [x] TypeScript and ESLint checks.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `d147e180e071fc208a453354c021cf60576fcde0`
- PR: #3826
- 作者：sam-srp
- 日期：2026-09-20T14:06:58Z

### Commit Message

```
fix(billing): hide default personal plan billing caption (#3826)

## Summary
Hide “Billed monthly. Cancel anytime.” below the Pro subscription button
for non-Team accounts, including its empty spacing. Team accounts retain
“Contact Sales to manage your team plan.”

## Root cause
The default personal plan state supplied a billing caption that is no
longer needed. Renewal dates, expiration notices, purchase restrictions,
and checkout behavior remain unchanged.

## Test plan
- [x] ProPlanAction unit suite: 21 tests passed.
- [x] TypeScript and ESLint checks.
```

来源：SerendipityOneInc/ecap-workspace @ d147e180，PR #3826，作者 sam-srp。