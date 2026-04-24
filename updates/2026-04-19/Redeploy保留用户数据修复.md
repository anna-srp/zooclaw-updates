---
title: "Agent Redeploy 不再覆盖用户数据"
type: "Bug Fix"
priority: "高"
date: "2026-04-19"
status: "待审核"
channels: "Discord+changelog"
---

# Agent Redeploy 不再覆盖用户数据

## 核心宣传点

修复了 agent 重新部署时会误覆盖用户个人数据（SOUL.md、IDENTITY.md、memory/ 等）的问题，重部署更安全。

## 原始内容

fix(openclaw): correct redeploy allowlist to preserve user data (#1060) — tim-srp

之前 allowlist 保护的是模板文件（TOOLS.md、AGENTS.md），反而暴露了用户数据。修复后：
- 永不覆盖：MEMORY.md、USER.md、SOUL.md、IDENTITY.md
- BOOTSTRAP.md 改为"不存在时才复制"
