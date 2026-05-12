---
title: "订阅状态修复：解决「无法取消订阅」报错及计费数据漂移"
type: "Bug Fix"
priority: "高"
date: "2026-05-09"
status: "待审核"
channels: "Discord, changelog"
---
# 订阅状态修复：解决「无法取消订阅」报错及计费数据漂移

## 核心宣传点
修复了部分用户点击「取消订阅」时报错"Failed to cancel subscription"的问题，同时清理了因历史 Webhook 故障导致的订阅状态不一致（影响约 47% 的有效订阅用户），保障续费和取消操作的准确性。

## 原始内容

**Commit**: `55601761` | **PR**: #1579

### Commit Message

```
fix(stripe): ECA-643 — Stripe ↔ Mongo subscription drift hotfix bundle (#1-#5 + 5 review rounds) (#1579)

## Summary

修复 ECA-643 报障 "Failed to cancel subscription. Please try again":挖出 2 个独立代码缺陷 + 1 次 webhook 域名 outage(已恢复)联合造成的 Stripe ↔ Mongo 状态漂移。
```

### PR Body

## Summary

修复 ECA-643 报障 "Failed to cancel subscription. Please try again":挖出 2 个独立代码缺陷 + 1 次 webhook 域名 outage(已恢复)联合造成的 Stripe ↔ Mongo 状态漂移。完整 RCA + 修复方案见 `docs/superpowers/specs/2026-05-08-stripe-mongo-drift-rca.md`。

生产实测影响范围:53 个有 stripe_subscription_id 的用户中，**25 个有漂移(47%)**，其中 5 例 P1 + 已 wash 完成，代码层修复 + 长期对账机制随本 PR ship。

## Hotfix Bundle（按 commit 顺序）

| # | 修复内容 |
|---|---|
| #1 | saga refund 现在会取消底层 Stripe subscription（防止退款后订阅继续自动扣款） |
| #2 | `handle_invoice_paid` 拒绝已 canceled/expired/unpaid 的 sub（防止 webhook outage 期间堆积的事件 flush 后误授 entitlement） |
| #3 | `cancel-subscription` 端点对已死 sub 不再 500，转而同步 mongo 后返回 success（原报障的直接 fix） |
| #4 | 新增 `charge.refunded` webhook handler，Dashboard 退款后兜底取消孤儿 sub |
| #5 | 周期性 reconciler cron（read-only 默认），pass-1 用户扫 + pass-2 saga-orphan 订单扫 |

## 数据洗（已在调查会话内完成）

| Wash | 类别 | 数量 | 状态 |
|---|---|---|---|
| Wash 0 | saga 孤儿 sub | 3 | ✅ |
| Wash 1 | 白嫖用户完整 expire | 2 | ✅ |
| Wash 2 | cap drift mongo 同步 | 4 | ✅ |
| Wash 3 | 小漂移 | 2 | ✅ |
| Wash 5 | 内部账号清理 | 1 | ✅ |
| Wash 4 | 残留 sub_id | 15 | ⏳ reconciler 上线写模式后自动处理 |

## Test plan

- [x] 142 hotfix unit tests 全过（120 stripe + 22 subscription_cron）
- [x] ruff + pyright + import-linter + 项目所有 pre-commit checks 全过
- [x] 端到端验证：Wash 0/1/2/3/5 在 prod mongo 已实操执行，生产用户漂移已修

## Linear

[ECA-643](https://linear.app/srpone/issue/ECA-643/stripe-mongo-订阅状态漂移-rca-修复)
