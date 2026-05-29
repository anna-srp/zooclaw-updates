---
title: "付费系统 v2 核心服务架构升级（后台准备中）"
type: "产品基础功能更新"
priority: "低"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# 付费系统 v2 核心服务架构升级（后台准备中）

## 核心宣传点

ZooClaw 付费订阅系统后台正在升级到 v2 架构，为更稳定、准确的订阅管理和权益计算奠定基础，暂不影响现有用户使用。

## 原始内容

feat(billing): add v2 payment core services (#1994)

Add dormant Billing v2 core services for deterministic payment orders, subscription agreements, entitlement ledger records, and BG grant/revoke transaction ids. Enforce paid amount/currency validation, provider subscription ownership, one-current-agreement guard, scheduled downgrade/cancel/apply behavior, subscription-code redemption guard, trial entitlement paths, and refund revoke idempotency.
