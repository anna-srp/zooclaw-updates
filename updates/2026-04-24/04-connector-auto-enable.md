---
title: "第三方连接器授权完成后自动启用 Skill"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-24"
status: "待审核"
channels: "Discord+changelog"
---
# 第三方连接器授权完成后自动启用 Skill

## 核心宣传点
完成 OAuth 授权后，相关 Skill 自动启用，无需手动开关——连接即用，减少配置步骤。

## 原始内容

feat: auto-enable connector on connect + remove Claw Tools toggle (#1232)
- Auto-enable and inject skill when OAuth completes (polling + webhook)
- Remove Claw Tools toggle — connected cards now match Google Workspace style
