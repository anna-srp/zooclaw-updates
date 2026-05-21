---
title: "订阅套餐变更时同步更新 LiteLLM 可用模型"
type: "产品基础功能更新"
priority: "高"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "bb391bf623102b3219a3bc8b7c066d19752cc60e"
pr: 1765
---
# 订阅套餐变更时同步更新 LiteLLM 可用模型

## 核心宣传点

用户升级或变更订阅套餐后，AI 模型列表会立即同步更新，确保立刻能使用新套餐对应的模型。

## 原始内容

### Commit Message

```
ECA-738 Sync LiteLLM key models on plan changes (#1765)

## Summary
- add a shared LiteLLM model-access sync helper for plan changes
- update both team models and persisted key models when a user has a
team id and keys
- support personal/user key fields so future non-team keys get the same
plan access updates
- route Stripe, Apple, subscription-code, expiry, and cron plan updates
through the shared sync path

## Testing
- `ruff check .`
- `pyright --pythonpath /home/node/.venvs/claw-interface/bin/python app
tests`
- focused pytest for affected billing/subscription paths (335 passed)

## Deploy order
Requires billing-gateway PR
https://github.com/SerendipityOneInc/billing-gateway/pull/37 to be
deployed first because this change calls `/admin/litellm/keys/models`.

Note: full `pytest --cov=app --cov-report=term-missing
--cov-fail-under=90 -q` was run and currently fails on unrelated
local-suite issues plus coverage at 87.69%. The focused affected suite
passes.
```

### PR Description

## Summary
- add a shared LiteLLM model-access sync helper for plan changes
- update both team models and persisted key models when a user has a team id and keys
- support personal/user key fields so future non-team keys get the same plan access updates
- route Stripe, Apple, subscription-code, expiry, and cron plan updates through the shared sync path

## Testing
- `ruff check .`
- `pyright --pythonpath /home/node/.venvs/claw-interface/bin/python app tests`
- focused pytest for affected billing/subscription paths (335 passed)

## Deploy order
Requires billing-gateway PR https://github.com/SerendipityOneInc/billing-gateway/pull/37 to be deployed first because this change calls `/admin/litellm/keys/models`.

Note: full `pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` was run and currently fails on unrelated local-suite issues plus coverage at 87.69%. The focused affected suite passes.

