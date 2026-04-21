---
title: "Oura Ring Connector + podcast-pal 配置持久化修复"
type: "Bug Fix"
priority: "低"
date: "2026-04-16"
status: "待审核"
channels: ""
---
# Oura Ring Connector + podcast-pal 配置持久化修复

## 核心宣传点
修复了 Oura Ring Connector 和 podcast-pal 重启后配置丢失的问题，运行时数据路径统一迁移至 ~/.config，Agent 重启后设置不再重置。

## 原始内容
fix(oura-ring-connector, podcast-pal): move config to ~/.config for persistence across claw restarts (#83)

将 oura-ring-connector 和 podcast-pal 的所有运行时数据路径从 ~/.oura、~/.podcast-pal 迁移至标准的 ~/.config/oura-ring-connector 和 ~/.config/podcast-pal，确保 Agent 重启后配置持久化。
