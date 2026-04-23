---
title: "Stripe SDK 版本锁定，修复订阅对象报错"
type: "Bug Fix"
priority: "中"
date: "2026-04-16"
status: "待审核"
channels: ""
---
# Stripe SDK 版本锁定，修复订阅对象报错

## 核心宣传点
修复了因 Stripe Python SDK 15.0.0 破坏性升级导致的订阅/会话对象方法报错，计费流程恢复正常。

## 原始内容
fix(claw-interface): pin stripe<15 to restore .get() on Session/Subscription (#908)

Stripe Python SDK 15.0.0 移除了 .get() 方法，导致订阅和会话对象访问异常。锁定 stripe<15 版本，计费相关功能恢复正常。
