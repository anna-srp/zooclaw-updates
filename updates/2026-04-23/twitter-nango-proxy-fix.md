---
title: "修复 Twitter Connector 连接卡死问题"
type: "Bug Fix"
priority: "中"
date: "2026-04-23"
status: "待审核"
channels: ""
---
# 修复 Twitter Connector 连接卡死问题

## 核心宣传点
修复了 Twitter-v2 Nango proxy 连接偶发卡死（hang）的问题，Twitter 相关功能现在更稳定。

## 原始内容
fix: add identity encoding for twitter-v2 Nango proxy hang (#1174)

Add `Nango-Proxy-Accept-Encoding: identity` header for twitter-v2 proxy requests to prevent connection hang caused by encoding negotiation issues.
