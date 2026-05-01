---
title: "Stock Analyst Agent 上架 — AI 量化分析师帮你做投资决策"
type: "Agent 上架/更新"
priority: "高"
date: "2026-04-30"
status: "待审核"
channels: ""
---
# Stock Analyst Agent 上架 — AI 量化分析师帮你做投资决策

## 核心宣传点
只需输入一个股票代码，AI 分析师团队自动帮你分析基本面、技术面、市场情绪、风险，最终输出 BUY / HOLD / SELL 建议和完整推理链。

## 原始内容
**Commit**: feat(stock-analyst): add stock-analyst 0.3.0 agent pack (#113)
**Author**: vincent-srp
**Date**: 2026-04-29T05:24:22Z

```
feat(stock-analyst): add stock-analyst 0.3.0 agent pack (#113)

Unpacked from build/stock-analyst-0.3.0.tar.gz. Multi-agent AI financial
analyst that plays all trading-firm roles (analysts, researchers, risk,
portfolio manager) on top of yfinance data, producing a final BUY/HOLD/SELL
decision with full reasoning chain.

Co-authored-by: vincent-srp <180138700+vincent-srp@users.noreply.github.com>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR #113 Body**:
## Summary
- Unpacked `build/stock-analyst-0.3.0.tar.gz` into `stock-analyst/` at the repo root, following the existing pack convention (e.g. `tvc-studio/`).
- Multi-agent AI financial analyst: the agent plays Market/Fundamentals/Sentiment/News analysts, Bull/Bear researchers, Research Manager, Trader, Risk team, and Portfolio Manager.
- Raw data via `yfinance`; final output is BUY / OVERWEIGHT / HOLD / UNDERWEIGHT / SELL with full reasoning chain.

## Test plan
- [ ] Verify `stock-analyst/agent-pack.yaml` parses and matches the v0.3.0 manifest
- [ ] Smoke-test pack install into `~/.openclaw/workspace-stock-analyst`
- [ ] Run `pack-onboarding` first-session flow
- [ ] Run `trading-decision` end-to-end on a sample ticker
