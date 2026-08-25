---
title: "修复：Team Plan 成员在个人订阅过期后被挡在 OpenClaw 门外"
type: "Bug Fix"
priority: "中"
date: "2026-08-24"
status: "待审核"
channels: ""
---

# 修复：Team Plan 成员在个人订阅过期后被挡在 OpenClaw 门外

## 核心宣传点

OpenClaw 的准入校验以前先看个人订阅，个人订阅一过期就只认「Vertical 套餐有效」的团队，普通 Team Plan 成员即使团队订阅正常也会被拦下来用不了。现在普通 Team Plan 会被正确识别为有效访问权限，可用模型清单也按同一套规则解析；Vertical 套餐有效的团队照常放行，Vertical 套餐已过期的团队仍然拦截。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `ebd9b4f41cfc40e93915fe35c973c78d6620b0c3`
- PR: #3483
- 作者: bill-srp
- 日期: 2026-08-24T03:18:33Z

### Commit Message

```
fix(openclaw): allow ordinary Team Plan access (#3483)

## Summary
- allow ordinary Team Plan members to pass the OpenClaw access gate when
their personal Billing Summary is expired
- keep active Vertical packages allowed and expired Vertical-package
teams blocked
- share the ordinary Team Plan contract with effective model catalog
resolution

## Root cause
The OpenClaw gate checked a user's personal Billing Summary first and,
for an expired personal summary, only accepted `vertical_active` team
access. Ordinary Team Plan membership was therefore ignored even though
the team billing context reports it as active. The shared resolver now
distinguishes ordinary Team Plans from teams with a historical but
inactive Vertical agreement.

## Test plan
- [x] `pytest tests/unit/test_openclaw_subscription_gate.py
tests/unit/test_effective_model_access.py -q` — 18 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] `git diff --check`
```

### PR Body

## Summary
- allow ordinary Team Plan members to pass the OpenClaw access gate when their personal Billing Summary is expired
- keep active Vertical packages allowed and expired Vertical-package teams blocked
- share the ordinary Team Plan contract with effective model catalog resolution

## Root cause
The OpenClaw gate checked a user's personal Billing Summary first and, for an expired personal summary, only accepted `vertical_active` team access. Ordinary Team Plan membership was therefore ignored even though the team billing context reports it as active. The shared resolver now distinguishes ordinary Team Plans from teams with a historical but inactive Vertical agreement.

## Test plan
- [x] `pytest tests/unit/test_openclaw_subscription_gate.py tests/unit/test_effective_model_access.py -q` — 18 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] `git diff --check`

