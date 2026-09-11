---
title: "付费套餐的 Agent 安装上限大幅放开：Starter / Pro / Ultra 提到 20 / 40 / 100"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-10"
status: "待审核"
channels: "站内弹窗+Discord+changelog+社媒素材+push"
---

# 付费套餐的 Agent 安装上限大幅放开：Starter / Pro / Ultra 提到 20 / 40 / 100

## 核心宣传点

付费套餐能装的 Agent 数量**翻了四到五倍**：

| 套餐 | 原上限 | 新上限 |
| --- | --- | --- |
| Starter | 5 | **20** |
| Pro | 10 | **40** |
| Ultra | 20 | **100** |

之前的问题挺尴尬：付费订阅还在用最早那套很低的上限，Starter 用户建到第 6 个 Agent 定义就会直接撞上 `agent.limit_exceeded`——花了钱，却和免费版几乎一样紧。

这次放开的范围是**后端共享策略**，所以四个入口一起生效：Agent 定义创建、Engine 安装、Computer 安装、批量安装。

**边界说明**：免费版和已过期订阅仍然是 5 个上限；已有的垂直行业 Pack 豁免规则不变；未知套餐仍然 fallback 到 Starter 策略——现在也就是 20。

## 原始内容

### fix(agents): raise paid plan install limits to 20/40/100 (#3684)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `3e232907`
- PR: #3684
- 作者: tim-srp
- 日期: 2026-09-10T06:43:53Z

### Summary（PR 原文）

- Raise Starter / Pro / Ultra installed-agent caps from 5 / 10 / 20 to 20 / 40 / 100.
- The shared backend policy covers agent-definition creation, engine installs, computer installs, and batch installs. Free and expired subscriptions remain capped at 5; existing vertical-pack exemptions remain intact.
- Preserve the existing unknown-plan fallback to Starter, now 20.

### 根因（PR 原文）

Paid subscriptions still used the original low install caps, so agent-definition creation could fail with `agent.limit_exceeded` after only 5 agents on Starter.

### 验证

- 224 项针对性配额/安装测试，含 24 个边界用例，覆盖每个档位与三个配额入口。
- 13 项 agent-development creation-claim 测试。
- `bash scripts/verify-py.sh`：Ruff、格式化、Pyright 与全部 8 项 import 合约通过。
- 仅需后端部署，无数据库迁移、无前端部署。

## 备注

发布状态：已上线（已包含在 `ecap-v0.19.3-release` 正式发布中）。

对外发布注意：这是明确的付费价值提升，适合做站内弹窗和社媒素材。文案里要带上「免费版仍为 5 个」，否则容易被理解成全员放开。
