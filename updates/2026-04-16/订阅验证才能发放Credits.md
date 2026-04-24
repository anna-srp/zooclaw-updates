---
title: "Credits 发放前增加有效订阅验证"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-16"
status: "待审核"
channels: "Discord+changelog"
---
# Credits 发放前增加有效订阅验证

## 核心宣传点
Admin boost、admin grant 和礼品码兑换现在会先验证用户是否有有效订阅，避免向未订阅用户错误发放 Credits。

## 原始内容
feat: require active subscription before granting credits (#884)

Admin boost、admin grant 和 gift code redeem 均新增订阅状态前置检查，无有效订阅的用户无法获得 Credits 发放。
