---
title: "修复已订阅企业邀请成员时被误判为「未开通计费」"
type: "Bug Fix"
priority: "高"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

部分已完成订阅、钱包正常的企业在邀请成员时会被错误拦截，现已修复，邀请可正常完成。

## 原始内容

fix(org): accept nested team models for invite handoff (#3391)

## Summary
- Accept the production Billing Gateway team response shape when
validating enterprise invitation handoffs.
- Add a regression test using the nested team_info model allowlist
returned in production.

## Root cause
The handoff readiness check only read models from team.models. Billing
Gateway returns production team models under team.team_info.models, so a
fully subscribed enterprise with an active wallet was incorrectly
rejected as billing-not-ready.

## Test plan
- [x] pytest tests/unit/test_enterprise_invite_handoff.py -q (19 passed)
- [x] bash scripts/verify-py.sh

---
### PR Body

## Summary
- Accept the production Billing Gateway team response shape when validating enterprise invitation handoffs.
- Add a regression test using the nested team_info model allowlist returned in production.

## Root cause
The handoff readiness check only read models from team.models. Billing Gateway returns production team models under team.team_info.models, so a fully subscribed enterprise with an active wallet was incorrectly rejected as billing-not-ready.

## Test plan
- [x] pytest tests/unit/test_enterprise_invite_handoff.py -q (19 passed)
- [x] bash scripts/verify-py.sh

