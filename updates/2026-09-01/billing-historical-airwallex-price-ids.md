---
title: "修复：老价格档位的订阅在升级/续费/降级时被拦下来"
type: "Bug Fix"
priority: "中"
date: "2026-09-01"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：老价格档位的订阅在升级/续费/降级时被拦下来

## 核心宣传点

早期按已下线价格档位签的个人订阅，在做升级、续费、降级和取消后恢复时会因为价格 ID 已不在当前配置里而被判定为非法请求。现在这些已知的历史个人订阅 Price ID 在上述存量协议流程里被接受，覆盖 Starter、Pro、Ultra 三档以及 Starter 试用 ID。

新建结账仍然只允许使用当前配置的 Price ID，未知的或语义不匹配的 Price ID 照旧拒绝。充值和垂类 Pack 走的是另一套流程，不在本次范围内。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `6992ea2da9ed5edd46a71fcbd7fcd47ab83cf20c`
- PR: #3611
- 作者: tim-srp
- 日期: 2026-09-01T12:49:39Z

### Commit Message

```
fix(billing): support historical airwallex price ids (#3611)

## Summary

- Accept known retired individual-subscription Airwallex Price IDs for
existing agreement upgrade, renewal, downgrade, and
cancellation-restoration flows.
- Keep new checkout creation on the currently configured Price IDs only.
- Continue rejecting unknown or semantically mismatched Price IDs.

## Scope

- Covers Starter, Pro, and Ultra individual subscription IDs, including
Starter trial IDs.
- Top-up and Vertical Pack use separate flows and are intentionally
outside this PR.

## Validation

- `python -m pytest tests/unit/test_airwallex_catalog.py
tests/unit/test_card_checkout_upgrade.py
tests/unit/test_airwallex_renewal.py
tests/unit/test_airwallex_subscription_plan_changes.py -q` (75 passed)
- `bash scripts/verify-py.sh`
- Pre-push changed-surface verification

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

```
## Summary

- Accept known retired individual-subscription Airwallex Price IDs for existing agreement upgrade, renewal, downgrade, and cancellation-restoration flows.
- Keep new checkout creation on the currently configured Price IDs only.
- Continue rejecting unknown or semantically mismatched Price IDs.

## Scope

- Covers Starter, Pro, and Ultra individual subscription IDs, including Starter trial IDs.
- Top-up and Vertical Pack use separate flows and are intentionally outside this PR.

## Validation

- `python -m pytest tests/unit/test_airwallex_catalog.py tests/unit/test_card_checkout_upgrade.py tests/unit/test_airwallex_renewal.py tests/unit/test_airwallex_subscription_plan_changes.py -q` (75 passed)
- `bash scripts/verify-py.sh`
- Pre-push changed-surface verification

```
