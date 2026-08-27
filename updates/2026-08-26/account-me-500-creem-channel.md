---
title: "修复：部分老用户打开账号页报错 500，账号信息完全加载不出来"
type: "Bug Fix"
priority: "高"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 修复：部分老用户打开账号页报错 500，账号信息完全加载不出来

## 核心宣传点

历史上通过 Creem 渠道付过款的用户，账号接口会因为支付渠道字段对不上而直接报 500，导致账号相关页面整个打不开。现在这类历史渠道值会自动归一成通用的「银行卡」展示，账号信息恢复正常读取，历史订阅协议里的原始渠道记录保持不变，不需要做任何数据迁移。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `8650ee79a15ffdfde7b3cb903d21ebe74bcabdb7`
- PR: #3521
- 作者: tim-srp
- 日期: 2026-08-26T05:34:33Z

### Commit Message

```
fix(billing): normalize historical creem channels (#3521)

## Summary
- Normalize historical account `payment_channel=creem` values to public
`card` responses, preventing `/account/me` validation failures.
- Preserve the original provider in historical subscription agreements;
no production data migration is required.

## Root cause

Creem was removed from the public response literal while active
historical subscription agreements can still project `provider=creem`
into the account response. Pydantic therefore rejected affected
`/account/me` responses with HTTP 500.

## Test plan

- [x] `services/claw-interface/.venv/bin/pytest
services/claw-interface/tests/unit/test_billing_v2_user_public_response.py
-q`
- [x] `bash scripts/verify-py.sh`
```

### PR Description

```
## Summary
- Normalize historical account `payment_channel=creem` values to public `card` responses, preventing `/account/me` validation failures.
- Preserve the original provider in historical subscription agreements; no production data migration is required.

## Root cause

Creem was removed from the public response literal while active historical subscription agreements can still project `provider=creem` into the account response. Pydantic therefore rejected affected `/account/me` responses with HTTP 500.

## Test plan

- [x] `services/claw-interface/.venv/bin/pytest services/claw-interface/tests/unit/test_billing_v2_user_public_response.py -q`
- [x] `bash scripts/verify-py.sh`

```
