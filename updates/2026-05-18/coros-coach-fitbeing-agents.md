---
title: "新 Agent 上架：COROS Coach（运动健康教练）和 Febe（Fitbeing 健康伴侣）"
type: "Agent 上架/更新"
priority: "高"
date: "2026-05-18"
status: "待审核"
channels: ""
---
# 新 Agent 上架：COROS Coach（运动健康教练）和 Febe（Fitbeing 健康伴侣）

## 核心宣传点
两款健康 Agent 正式上线：COROS Coach 连接 COROS 运动手表，提供基于睡眠/HRV/恢复/训练负荷的个性化运动建议；Febe 连接 Fitbeing 可穿戴设备，每天主动汇报你的健康状态并支持对话式健康咨询。

## 原始内容

**Commit**: `fb24dc4a` | ecap-agent-pack | 2026-05-18T07:14:04Z  
**PR**: #128 | feat: add coros-coach and fitbeing-health-agent packs

---

### COROS Coach

Personal health & training coach powered by the COROS MCP.

- Region-aware OAuth 认证
- 早/午/晚三次数据汇报
- 按需生成 HTML 健康仪表盘
- 基于以下数据回答训练问题：睡眠 / HRV / 恢复评分 / 训练负荷

### fitbeing-health-agent（Febe）

Warm health companion connecting to the Fitbeing wearable API via a user-supplied login token.

数据维度：
- 睡眠 / 心率 / HRV / SpO2 / 压力
- 活动量 / 运动记录 / 体温 / 呼吸频率

功能：
- 三次定时健康简报（早/午/晚）
- 工作时间段每 30 分钟主动 poll 提醒
- 交互式 HTML 健康仪表盘
