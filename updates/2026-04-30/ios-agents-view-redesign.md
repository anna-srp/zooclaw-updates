---
title: "iOS Agent 广场全新改版，支持一键更新 Agent"
type: "产品基础功能更新"
priority: "中"
date: "2026-04-30"
status: "待审核"
channels: ""
---
# iOS Agent 广场全新改版，支持一键更新 Agent

## 核心宣传点
iOS 应用的 Agent 目录界面焕然一新，探索和更新 Agent 更流畅；当你的 Agent 有新版本时，会有明显提示并支持一键升级。

## 原始内容
**Commit**: feat(ios): redesign AgentsView, add agent update flow (#1469)
**Author**: （merge commit）
**Date**: 2026-04-29

```
feat(ios): redesign AgentsView, add agent update flow (#1469)

## Summary

Redesigns AgentsView (the agent catalog) to match the Zoo Square v2
EXPLORE design and adds a new agent-update affordance plus a global
"agent hired" toast that survives tab switches.

### Key changes
- EXPLORE-style row layout: gradient background, HankenGrotesk typography, dark nav
- Liquid glass menu button (iOS 26)
- API-driven categories: removed hardcoded AgentCategory enum
- Reusable Toast component with optional avatar/icon/emoji + action button
- Agent update flow: when UserAgent.has_update == true, row shows update indicator
```

**PR #1469 Body**:
Redesigns AgentsView (the agent catalog) to match the Zoo Square v2 EXPLORE design and adds a new agent-update affordance plus a global "agent hired" toast that survives tab switches.

Key changes:
- EXPLORE-style row layout: gradient background, HankenGrotesk typography, dark navy active pill, dynamic category tabs driven by the catalog response
- Liquid glass menu button (iOS 26) — fixed a latent #if swift(>=6.2) gate
- API-driven categories: removed the hardcoded AgentCategory enum
- Reusable Toast component with optional avatar/icon/emoji + action button
- Agent update flow: when UserAgent.has_update == true, row shows plus.arrow.trianglehead.clock + a "NEW" pill; tap calls POST /openclaw API to update
