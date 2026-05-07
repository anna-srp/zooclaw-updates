---
title: "Stock Analyst Agent 上架 — AI 量化分析师帮你做投资决策"
type: "Agent 上架/更新"
priority: "高"
date: "2026-04-29"
status: "待审核"
channels: "站内弹窗, 社媒素材, Use Case, Discord, changelog, KOL, EDM"
---

# Stock Analyst Agent 上架 — AI 量化分析师帮你做投资决策

## 核心宣传点

只需输入一个股票代码，AI 分析师团队自动帮你分析基本面、技术面、市场情绪、风险，最终输出 BUY / HOLD / SELL 建议和完整推理链。

## 原始内容

**Commit:** `9c5474a3` — 2026-04-29T05:24:22Z
**Repo:** ecap-agent-pack
**Author:** vincent-srp

**Commit Message:**
```
feat(stock-analyst): add stock-analyst 0.3.0 agent pack (#113)

Unpacked from build/stock-analyst-0.3.0.tar.gz. Multi-agent AI financial
analyst that plays all trading-firm roles (analysts, researchers, risk,
portfolio manager) on top of yfinance data, producing a final BUY/HOLD/SELL
decision with full reasoning chain.
```

**PR #113:** feat(stock-analyst): add stock-analyst 0.3.0 agent pack

**PR Body:**
## Summary
- Unpacked `build/stock-analyst-0.3.0.tar.gz` into `stock-analyst/` at the repo root
- Multi-agent AI financial analyst: plays Market/Fundamentals/Sentiment/News analysts, Bull/Bear researchers, Research Manager, Trader, Risk team, and Portfolio Manager
- Raw data via `yfinance`; final output is BUY / OVERWEIGHT / HOLD / UNDERWEIGHT / SELL with full reasoning chain
