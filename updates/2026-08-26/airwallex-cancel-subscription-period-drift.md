---
title: "修复：取消订阅时报「订阅周期不一致」，取消操作被拒绝"
type: "Bug Fix"
priority: "高"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 修复：取消订阅时报「订阅周期不一致」，取消操作被拒绝

## 核心宣传点

处于试用期的订阅在点「取消订阅」时，会因为本地记录的计费周期和支付服务商返回的周期对不上而被直接拒绝，用户根本取消不掉。现在以支付服务商的周期为准，遇到周期修正就接受并同步回本地记录。受影响的用户重新点一次「取消订阅」即可正常完成，无需人工处理数据。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `c699341914c4dddc02233de390644c92b1dcd08e`
- PR: #3538
- 作者: tim-srp
- 日期: 2026-08-26T14:45:28Z

### Commit Message

```
fix(billing): tolerate Airwallex period correction on scheduled cancellation (#3538)

## Summary

- 用户在 zooclaw.ai 取消 Airwallex 订阅时报错 `Airwallex returned a different
subscription period`,取消操作被本地拒绝
- 放宽 `_validate_provider_response` 的 period 校验:provider
是计费周期的权威来源,period 漂移时接受并以 provider 为准回写,同时记录
`airwallex_provider_period_drift` warning 日志便于观测
- 受影响用户重新点一次「取消订阅」即可自动对齐本地与 provider 的周期,无需数据修补

## Root cause

Airwallex 对 trial 订阅,`current_period_ends_at` 定义为「当前已开票周期的结束」= trial
结束后第一个付费周期结束(trial_ends_at + 一个计费月)。本地在创建时(webhook
快照)忠实记录该值。取消订阅(`cancel_at_period_end=true`)后,Airwallex 把
`current_period_ends_at` 修正为实际到期日(trial 结束)——字段是动态变化的,并非稳定周期边界。本地取消路径对
provider 返回的 period 做严格相等校验 → 对 trial 订阅必然失败(差 30 天整,2592000 秒)。

## Changes

- `app/services/airwallex/subscription_changes.py` —
`_validate_provider_response`:保持 identity / terminal status / period
缺失校验严格;period 与本地不一致改为接受 + 回写 provider 值 +
`airwallex_provider_period_drift` warning 日志
- `tests/unit/test_airwallex_subscription_changes.py` — 移除「period 漂移 →
拒绝」case;新增 cancel 接受修正周期并写回、resume 恢复完整周期并写回 2 个测试

## Test plan

- [x] `verify-py.sh`(ruff + pyright + import-linter)通过
- [x] `test_airwallex_subscription_changes.py` +
`test_airwallex_subscription_plan_changes.py` 46 个测试全部通过(plan change
复用同一校验函数,语义一致)

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Description

```
## Summary

- 用户在 zooclaw.ai 取消 Airwallex 订阅时报错 `Airwallex returned a different subscription period`,取消操作被本地拒绝
- 放宽 `_validate_provider_response` 的 period 校验:provider 是计费周期的权威来源,period 漂移时接受并以 provider 为准回写,同时记录 `airwallex_provider_period_drift` warning 日志便于观测
- 受影响用户重新点一次「取消订阅」即可自动对齐本地与 provider 的周期,无需数据修补

## Root cause

Airwallex 对 trial 订阅,`current_period_ends_at` 定义为「当前已开票周期的结束」= trial 结束后第一个付费周期结束(trial_ends_at + 一个计费月)。本地在创建时(webhook 快照)忠实记录该值。取消订阅(`cancel_at_period_end=true`)后,Airwallex 把 `current_period_ends_at` 修正为实际到期日(trial 结束)——字段是动态变化的,并非稳定周期边界。本地取消路径对 provider 返回的 period 做严格相等校验 → 对 trial 订阅必然失败(差 30 天整,2592000 秒)。

## Changes

- `app/services/airwallex/subscription_changes.py` — `_validate_provider_response`:保持 identity / terminal status / period 缺失校验严格;period 与本地不一致改为接受 + 回写 provider 值 + `airwallex_provider_period_drift` warning 日志
- `tests/unit/test_airwallex_subscription_changes.py` — 移除「period 漂移 → 拒绝」case;新增 cancel 接受修正周期并写回、resume 恢复完整周期并写回 2 个测试

## Test plan

- [x] `verify-py.sh`(ruff + pyright + import-linter)通过
- [x] `test_airwallex_subscription_changes.py` + `test_airwallex_subscription_plan_changes.py` 46 个测试全部通过(plan change 复用同一校验函数,语义一致)

```
