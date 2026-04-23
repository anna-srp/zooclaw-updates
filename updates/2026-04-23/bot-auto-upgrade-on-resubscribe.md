---
title: "重新订阅后 Bot 自动升级到最新版本"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-23"
status: "待审核"
channels: ""
---
# 重新订阅后 Bot 自动升级到最新版本

## 核心宣传点
之前重新订阅后，你的 Bot 可能还在跑旧版本。现在重新订阅时会自动升级 Bot 到最新发布版本，一步到位，开箱即用最新能力。

## 原始内容
feat: auto-upgrade bot image on subscription recovery (#1221)

When a user resubscribes, `start_user_bots` now auto-upgrades the bot's deployment image to the latest published release before starting, so stopped bots always come back on the newest version.
