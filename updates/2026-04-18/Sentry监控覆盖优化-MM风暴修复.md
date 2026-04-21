---
title: "Sentry 监控优化 + Mattermost 事件风暴修复"
type: "Bug Fix"
priority: "高"
date: "2026-04-18"
status: "待审核"
channels: ""
---

# Sentry 监控优化 + Mattermost 事件风暴修复

## 核心宣传点

修复了 Mattermost 连接事件引发 9.3 万条 Sentry 日志风暴的 bug，系统监控更稳定，不再产生无效报警噪音。

## 原始内容

fix(sentry): eliminate MM connection 93K event storm — infinite loop + Logs migration (#944)
fix(sentry): throttle MM connection reports + global rate limit (#910) — peter-srp
