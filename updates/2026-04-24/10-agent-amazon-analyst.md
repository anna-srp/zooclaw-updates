---
title: "新 Agent 上架：Amazon Analyst — 亚马逊选品与运营智能顾问"
type: "Agent 上架/更新"
priority: "高"
date: "2026-04-24"
status: "待审核"
channels: ""
---
# 新 Agent 上架：Amazon Analyst — 亚马逊选品与运营智能顾问

## 核心宣传点
专为亚马逊卖家打造的 AI 顾问，用自然语言提问，自动调用 10 个专业分析工具——覆盖 Listing 审核、机会发现、市场准入、竞品监控、定价、评论分析等，数据驱动决策，不再需要在多个工具间切换。

## 原始内容

feat(amazon-analyst): new agent pack with proxy-based auth (#100)

### 包含 10 个专业技能
- `amazon-listing-audit-pro` — Listing 审核
- `amazon-opportunity-discoverer` — 机会发现
- `amazon-market-entry-analyzer` — 市场准入分析
- `amazon-competitor-intelligence-monitor` — 竞品情报监控
- `amazon-daily-market-radar` — 每日市场雷达
- `amazon-market-trend-scanner` — 市场趋势扫描
- `amazon-pricing-command-center` — 定价指挥中心
- `amazon-review-intelligence-extractor` — 评论智能分析
- `amazon-analysis` — 通用分析（兜底）
- `apiclaw` — 基础数据层（11 个 API 端点）

### 安全
所有 APIClaw 流量通过 ecap-proxy-service 中转，服务端持有 API Key，不在 Agent 包内硬编码凭证。
