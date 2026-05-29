---
title: "修复 Slack 连接设置时因 Token 格式错误导致连接失败的问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-28"
status: "待审核"
channels: ""
---

# 修复 Slack 连接设置时因 Token 格式错误导致连接失败的问题

## 核心宣传点

添加 Slack 账号时，如果 Token 中含有多余空格或格式不对，系统现在会立即提示错误，避免看似成功但实际无法工作的情况。

## 原始内容

fix(claw-settings): reject malformed Slack tokens (#2026)

Reject Slack channel credentials that include pasted-together tokens or internal whitespace. Trim edge whitespace before writing Slack channel config to FastClaw.

Root cause: Slack channel setup previously validated only token prefix and rough length on the frontend, while the backend forwarded channel config as-is. A malformed Bot Token containing an internal space could be persisted, causing Slack auth to fail at runtime even though setup appeared connected.
