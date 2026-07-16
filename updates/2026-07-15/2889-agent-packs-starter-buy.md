---
title: "所有 Starter 用户均可购买 Agent Pack"
type: "产品基础功能更新"
priority: "高"
date: "2026-07-15"
status: "待审核"
channels: ""
tags: []
---

# 所有 Starter 用户均可购买 Agent Pack

## 核心宣传点
现在所有 Starter 用户（含试用、订阅码、手动调整获得的有效 Starter 权益）都可以直接购买付费 Agent Pack，无需额外的付费主订阅门槛，付费包购买入口对更多用户开放。

## 原始内容
### PR #2889 — feat(agent-packs): allow all Starter users to buy packs (#2889)
作者: bill-srp | https://github.com/SerendipityOneInc/ecap-workspace/pull/2889

## Linear
https://linear.app/srpone/issue/ECA-1246/enable-pack-purchases-for-all-starter-users

## Summary
- Resolve paid agent-pack checkout eligibility through the Billing v2 current-access summary.
- Allow effective providerless Starter access from trials, subscription codes, and manual adjustments while preserving provider-backed main subscriptions.
- Add regression coverage and update the English and Chinese architecture docs.

## Test plan
- [x] `python -m pytest services/claw-interface/tests/unit/test_ecap_pack_subscription_service.py -q` (23 passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`

## 备注
外部A级。本条为 2026-07-15 每日同步补录（原 cron 仅写入 raw，未落 updates/ 与多维表）。
