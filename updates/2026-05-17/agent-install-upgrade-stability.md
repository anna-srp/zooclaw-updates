---
title: "重新安装 Agent 时数据不再丢失，安装更稳定"
type: "Bug Fix"
priority: "中"
date: "2026-05-17"
status: "待审核"
channels: ""
---
# 重新安装 Agent 时数据不再丢失，安装更稳定

## 核心宣传点
重新安装或更新已有 Agent 时，你的聊天数据、记忆和自定义文件会被保留下来，不再因为更新而丢失。同时安装过程更稳定，即使遇到临时网络问题也不会导致 Agent 消失。

## 原始内容
**Commit**: fix(claw-interface): install-endpoint platform follow-ups #2 + #3 + #4 (#1714)
**Repo**: SerendipityOneInc/ecap-workspace
**SHA**: 230d261d
**Author**: 后端团队
**Date**: 2026-05-17

**Commit Message**:
fix(claw-interface): install-endpoint platform follow-ups #2 + #3 + #4 (#1714)

Three platform-side fixes for the `install/async` flow:

**#3 — Upgrade-in-place for custom-agent re-install**
Re-installing an already-installed custom or import agent replaces the existing entry instead of raising 409 Conflict. Upgrade preserves user data via preserve_user_data=True branch + backup-on-overwrite. User's data/, memory/, media/, artifacts/shares/ files survive across upgrades.

**#4 — Post-commit activation failure must not roll back the install**
Once deploy writes the new bot config to FastClaw DB, activation failures are non-fatal — the agent stays installed. A post-deploy MM-bot-entry race no longer rolls back the hire.

**#2 — Wire avatar_url to the pod's artifact host on install**
After deploy unpacks the archive, the platform patches the user's private catalog row with the correct avatar URL so the Agent card shows the right avatar image.

**PR Description**:
Three platform-side fixes for the install/async flow. One conceptual shift: install used to be implicitly atomic. After this PR, the contract is partial commit-forward:
- Mongo state is always rolled back on deploy failure (catalog reflects what's actually deployable)
- Runtime cleanup is skipped on upgrade failure so the prior workspace survives
- Post-deploy activation failures don't trigger any rollback (deploy is the commit point)
- User-data files overwritten during upgrade are backed up before the overwrite

Shipping together makes the agent-studio fix testable end-to-end: re-publishes no longer accumulate channels, transient activate failures no longer phantom-install, the resulting card shows the avatar, and user state survives upgrades.
